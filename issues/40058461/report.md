# Security: [ANGLE] Vulkan : Out-of-bounds memory can be accessed using bound offsets

| Field | Value |
|-------|-------|
| **Issue ID** | [40058461](https://issues.chromium.org/issues/40058461) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ne...@nesk.kr |
| **Assignee** | ro...@google.com |
| **Created** | 2022-01-10 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

When processing the `glDrawArrays` method in the Vulkan renderer, `VertexArrayVk::updateStreamedAttribs` is called.

```
// Handle copying client attribs and/or expanding attrib buffer in case where attribute  
//  divisor value has to be emulated.  
angle::Result VertexArrayVk::updateStreamedAttribs(const gl::Context \*context,  
                                                   GLint firstVertex,  
                                                   GLsizei vertexOrIndexCount,  
                                                   GLsizei instanceCount,  
                                                   gl::DrawElementsType indexTypeOrInvalid,  
                                                   const void \*indices)  
{  
...  
        // Emulated attrib  
        BufferVk \*bufferVk = nullptr;  
        if (binding.getBuffer().get() != nullptr)  
        {  
            // Map buffer to expand attribs for divisor emulation  
            bufferVk      = vk::GetImpl(binding.getBuffer().get());  
            void \*buffSrc = nullptr;  
            ANGLE_TRY(bufferVk->mapImpl(contextVk, &buffSrc));  
            src = reinterpret_cast<const uint8_t \*>(buffSrc) + binding.getOffset();                 // [1]  
        }  
  
        ANGLE_TRY(StreamVertexData(contextVk, &mDynamicVertexData, src, bytesToAllocate, 0,         // [2]  
                                    instanceCount, binding.getStride(), stride,  
                                    vertexFormat.getVertexLoadFunction(compressed),  
                                    &mCurrentArrayBuffers[attribIndex],  
                                    &mCurrentArrayBufferOffsets[attribIndex], divisor));  

```

When setting the source buffer pointer (`src`) in this method, the bound offset is used. [1]

This offset can be specified with the `glVertexAttribPointer` method.

```
void gl.vertexAttribPointer(index, size, type, normalized, stride, offset);  

```

Since there is no verification of this offset, it is possible to access memory outside the bounds.

This particular situation seems to arise when two programs are used (see poc.html).

The source pointer is used when copying memory and the following crash occurs. [2]

```
0:018> g  
(37d0.3110): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
rax=000001f495b66c10 rbx=0000000000000fff rcx=0000000000000000  
rdx=0000000000000008 rsi=0000000000000008 rdi=00007ff973dc3d90  
rip=00007ff973dc3dab rsp=000000aab03fde38 rbp=0000000000001000  
 r8=0000000000000001  r9=000001f49d2fc150 r10=000001f4a5c50290  
r11=000001f4959ca0f8 r12=0000000000000001 r13=0000000000000001  
r14=0000000000000000 r15=000001f4a5c50290  
iopl=0         nv up ei pl zr na po nc  
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010246  
libglesv2!rx::CopyNativeVertexData<unsigned char,1,1,0>+0x1b:  
00007ff9`73dc3dab 418a02          mov     al,byte ptr [r10] ds:000001f4`a5c50290=??  
0:000> kb  
 # RetAddr               : Args to Child                                                           : Call Site  
00 00007ff9`73f6fb93     : 000001f4`95d43e70 000000aa`b03fdec8 000001f4`95d43e30 00000000`00000000 : libglesv2!rx::CopyNativeVertexData<unsigned char,1,1,0>+0x1b [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\copyvertex.inc.h @ 33]   
01 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : libglesv2!rx::`anonymous namespace'::StreamVertexData+0x8e [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\VertexArrayVk.cpp @ 107]   
02 00007ff9`73f13a2c     : 00000000`00000000 000001f4`95dadb10 00000000`00000001 000001f4`95b73e00 : libglesv2!rx::VertexArrayVk::updateStreamedAttribs+0x4f3 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\VertexArrayVk.cpp @ 833]   
03 00007ff9`73f1684a     : 000001f4`95b75fc8 000001f4`95b76028 00000000`00000000 000001f4`00000000 : libglesv2!rx::ContextVk::setupDraw+0x9c [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 847]   
04 00007ff9`73b241c2     : aaaaaaaa`aaaaaaaa 0000c668`3fbb9f9d 000000aa`b03fe128 000000aa`b03fe130 : libglesv2!rx::ContextVk::drawArrays+0x13a [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\vulkan\ContextVk.cpp @ 2540]   
05 (Inline Function)     : --------`-------- --------`-------- --------`-------- --------`-------- : libglesv2!gl::Context::drawArrays+0x1bc [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.inl.h @ 132]   
06 00007ff9`6d46f5e3     : 00001ace`000b3a30 00001ace`00131000 000000aa`b03fe2a0 00007ff9`6d474d3f : libglesv2!GL_DrawArrays+0x242 [C:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_2_0_autogen.cpp @ 1063]  

```

**VERSION**  

Chrome Version: [96.0.4664.110] + [stable]  

Operating System: [Windows, Linux]

**REPRODUCTION CASE**  

See attached files

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: GPU Proces  

Crash State: See crash.log

**CREDIT INFORMATION**  

Reporter credit: Jaehun Jeong(@n3sk) of Theori

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 1.5 KB)
- [crash.log](attachments/crash.log) (text/plain, 8.6 KB)

## Timeline

### [Deleted User] (2022-01-10)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2022-01-10)

[Comment Deleted]

### ne...@nesk.kr (2022-01-10)

In the chromium Asan build, the bug seems to be triggered, but no logs are printed.
If anyone knows a solution to this problem, please let me know.

```
[2424:11336:0111/013935.278:ERROR:command_buffer_proxy_impl.cc(328)] GPU state invalid after WaitForGetOffsetInRange.
[7820:2304:0111/013935.283:ERROR:gpu_process_host.cc(972)] GPU process exited unexpectedly: exit_code=-1073741819
```

https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-956972.zip?generation=1641802642057403&alt=media

### cl...@chromium.org (2022-01-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5766916010213376.

### ne...@nesk.kr (2022-01-11)

Also tested on 97.0.4692.71 (stable), 99.0.4820.0 (dev build)

### ct...@chromium.org (2022-01-11)

Looking at the clusterfuzz testcase, it shows a similar error log:

[18532:6872:0110/144725.903:VERBOSE1:media_stream_manager.cc(873)] RFAOSF::Core() [process_id=5, frame_id=1]
[18532:13028:0110/144726.087:INFO:CONSOLE(48)] "WebGL: INVALID_OPERATION: getAttribLocation: program not linked", source: file:///C:/clusterfuzz/bot/inputs/fuzzer-testcases/poc1.html (48)
[17788:7976:0110/144726.156:ERROR:command_buffer_proxy_impl.cc(328)] GPU state invalid after WaitForGetOffsetInRange.
[18532:13028:0110/144726.168:ERROR:gpu_process_host.cc(972)] GPU process exited unexpectedly: exit_code=-1073741819
[18532:13028:0110/144726.168:WARNING:gpu_process_host.cc(1277)] The GPU process has crashed 1 time(s)
[18532:13028:0110/144726.229:INFO:CONSOLE(0)] "WebGL: CONTEXT_LOST_WEBGL: loseContext: context lost", source: file:///C:/clusterfuzz/bot/inputs/fuzzer-testcases/poc1.html (0)
[18532:13028:0110/144726.765:WARNING:gpu_process_host.cc(1000)] Reinitialized the GPU process after a crash. The reported initialization time was 167 ms

However it is not triggering any ASAN failure so clusterfuzz is treating this as unrepropducible.

Reporter: Is this the expected behavior? From your included crash.log it looks like you were able to trigger an access violation. Could you provide your exact reproduction steps?

[Monorail components: Internals>GPU>Vulkan]

### pe...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

[Monorail components: Internals>GPU>ANGLE]

### jm...@chromium.org (2022-01-11)

One of the ANGLE team who works primarily on Vulkan should look into this. I won't be available today or tomorrow.

[Monorail components: -Internals>GPU>Vulkan]

### lf...@google.com (2022-01-11)

[Empty comment from Monorail migration]

### ro...@google.com (2022-01-11)

Hmm, seems odd that ASAN wouldn't catch a subprocess crash. Maybe --single-process would help?

The crash log looks like WinDbg so I'm guessing it was obtained by attaching debugger to the subprocess.

I don't see boundary checks in the code indeed.

### ne...@nesk.kr (2022-01-12)

[Comment Deleted]

### ro...@google.com (2022-01-12)

I'm told that robust buffers in WebGL should supposedly do validation like that but I also see this fall through when robustness is not supported:
https://source.chromium.org/chromium/chromium/src/+/main:ui/gl/gl_context_egl.cc;l=195;drc=f2717498331fee0d5df8409e2b3b3dfec9670f27

Not sure if this might be the case here or I'm totally off track?

### cl...@chromium.org (2022-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4961416395948032.

### ct...@chromium.org (2022-01-13)

Thanks for the further investigation into getting a reliable ASAN reproduction. I've started a new clusterfuzz testcase which should hopefully reproduce now.

### jm...@chromium.org (2022-01-14)

[Empty comment from Monorail migration]

### ro...@google.com (2022-01-14)

Ok, so I think I understand this a bit better now - thanks for the info and the fix Jamie.

These crash would be acceptable in a non-WebGL context as it's undefined behavior, but in a WebGL context robust buffer access handling is required, and it is normally enabled - the Vulkan backend isn't even normally used by ANGLE (D3D on Windows or GL on Mac/Linux). However, it does get used for the SwiftShader fallback and then we're hitting this code path and then ANGLE isn't behaving correctly in a couple of spots where special handling is required and it would crash instead of doing what robust buffer access rules require (out-of-bound reads returning values from anywhere within the buffer object, or 0 or 1 etc). So the fix would be to follow those rules in the ANGLE Vulkan backend (when in the WebGL context), by making sure StreamVertexData calls only make reads within the buffer (however it is given a raw pointer so at least some of validation would have to happen at the call sites).

I reproduced this with an ANGLE end2end test by invoking calls similarly to what poc.html does.

### aj...@google.com (2022-01-20)

setting labels based on possible RCE in the gpu process. Please let us know if this is not exploitable.

### [Deleted User] (2022-01-20)

[Empty comment from Monorail migration]

### ne...@nesk.kr (2022-01-20)

I think this issue is exploitable since the attacker has full control over the offset of the memory pointer. It would require some heap grooming for exploitation.

### [Deleted User] (2022-01-20)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/5f0badf4541ba52659c937cfe9190d3735a76c10

commit 5f0badf4541ba52659c937cfe9190d3735a76c10
Author: Roman Lavrov <romanl@google.com>
Date: Tue Jan 18 20:05:55 2022

Vulkan: Prevent out of bounds read in divisor emulation path.

Split the replicated part of StreamVertexData out to
StreamVertexDataWithDivisor, there is only a partial argument
overlap between the two.

Bug: chromium:1285885
Change-Id: Ibf6ab3efc6b12b430b1d391c6ae61bd9668b4407
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3398816
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Roman Lavrov <romanl@google.com>

[modify] https://crrev.com/5f0badf4541ba52659c937cfe9190d3735a76c10/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp
[modify] https://crrev.com/5f0badf4541ba52659c937cfe9190d3735a76c10/src/tests/gl_tests/RobustBufferAccessBehaviorTest.cpp


### gi...@appspot.gserviceaccount.com (2022-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/79d1d335f7adaa4cedcd333b30395648d525a1ff

commit 79d1d335f7adaa4cedcd333b30395648d525a1ff
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Jan 25 20:04:11 2022

Roll ANGLE from 8fc4d3b1e618 to 5f0badf4541b (3 revisions)

https://chromium.googlesource.com/angle/angle.git/+log/8fc4d3b1e618..5f0badf4541b

2022-01-25 romanl@google.com Vulkan: Prevent out of bounds read in divisor emulation path.
2022-01-25 lubosz.sarnecki@collabora.com FrameCapture: Detect GL_MAP_COHERENT_BIT_EXT correctly.
2022-01-25 angle-autoroll@skia-public.iam.gserviceaccount.com Roll vulkan-deps from 238eaa6f9d25 to 4ec99dddf407 (7 revisions)

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/angle-chromium-autoroll
Please CC ynovikov@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86
Bug: chromium:1285885
Tbr: ynovikov@google.com
Change-Id: I24e4a583ecf435556cc1b73b2899f67b3476e0d7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3415531
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#963146}

[modify] https://crrev.com/79d1d335f7adaa4cedcd333b30395648d525a1ff/DEPS


### [Deleted User] (2022-01-30)

romanl: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2022-01-31)

[Empty comment from Monorail migration]

### jm...@chromium.org (2022-01-31)

Roman: OS-Chrome means ChromeOS-related bugs. Because this is a SwiftShader bug it affects Windows, Linux, and some pre-stable versions of Mac IIUC.

### ro...@google.com (2022-01-31)

Thanks Jamie, noted for future.

### jm...@chromium.org (2022-01-31)

NP, nice work on the fix!

### [Deleted User] (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-31)

Requesting merge to extended stable M96 because latest trunk commit (963146) appears to be after extended stable branch point (929512).

Requesting merge to stable M97 because latest trunk commit (963146) appears to be after stable branch point (938553).

Requesting merge to beta M98 because latest trunk commit (963146) appears to be after beta branch point (950365).

Requesting merge to dev M99 because latest trunk commit (963146) appears to be after dev branch point (961656).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-31)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), cindyb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-31)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-31)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: benmason (Android), harrysouders (iOS), ceb (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-31)

Merge review required: a commit with DEPS changes was detected.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-02)

merge-na for M96 and M97 as M98 is now stable channel

romanl@ please respond to the merge questionnaire (it's not necessary to do so in full since this is not at all related to a new feature and there is clearly a single CL for merge), but it would be helpful if you could verify this has been tested and verified locally or on Canary. Since this change is rather sizable and textually large, it would be helpful if you could verify there's not stability issues or other concerns before I review this for merge to M99 and M98. Thank you! 

### ro...@google.com (2022-02-02)

I am new to Chrome processes so I don't think I'll be able to help with answering those questions or properly testing Chrome. Would it be possible to have someone else help with that?

The fix was tested using tests added in https://chromium-review.googlesource.com/c/angle/angle/+/3398816 that replicate the crash reported on this bug. I didn't find a good way to test this in Chrome.

### am...@google.com (2022-02-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-04)

Congratulations, the VRP Panel has decided to award you $7,000 for this report. This is a bit higher on average for a VRP reward for an OOB read; however, this was in memory access was in the GPU process, which we are wanting to incentivize the reporting of security bugs in, so this was judged under the criteria of baseline memory corruption in the GPU process and falls under the new reward amounts for GPU and other bugs in highly privileged processes (g.co/chrome/vrp). Thank you for your report and nice work! 

### am...@google.com (2022-02-04)

[Empty comment from Monorail migration]

### ro...@google.com (2022-02-07)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-08)

[Empty comment from Monorail migration]

### ad...@google.com (2022-02-08)

Reopening because https://crbug.com/chromium/1295423 says that we also need to merge https://crrev.com/c/3445528.


### am...@chromium.org (2022-02-09)

Since https://chromium-review.googlesource.com/c/angle/angle/+/3445528/ was just landed, let's give this some more bake time in Canary and evaluate merging both CLs in concert to beta (M99) and Stable (M98) slightly later in the week 

### [Deleted User] (2022-02-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-02-10)

please confirm there are no stability issues introduced on canary since these two CLs landed and please merge both CLs to relevant M99 and M98 branches (go/chrome-branches) by EOD today so this fix can be included in tomorrow's cut of the Stable channel refresh 

### ro...@google.com (2022-02-11)

Hi Amy,

I'm looking into it, but just FYI this wouldn't have been a realistic expectation on such a short notice even if I wasn't OOO on Thu:

> Thu, Feb 10, 2022, 3:39 PM EST
> ... by EOD today ...

### ro...@google.com (2022-02-11)

> please confirm there are no stability issues introduced on canary since these two CLs landed

What does this entail? I just checked that the original issue reproduces on stable Chrome on a windows cloudtop, and doesn't reproduce on canary. How do I know if this might have caused "stability issues" ?

### am...@chromium.org (2022-02-11)

Hi Roman, thanks for the feedback about timelines. The timing with the later CL was a little late/tight for the forthcoming stable respin (RC cut happening today) and we needed to ensure there was sufficient time on Canary before approving the merge. Please let me know what type of lead time I need to request merges on before cut deadlines so I can better partner with your team from a security perspective. 

>>> What does this entail? I just checked that the original issue reproduces on stable Chrome on a windows cloudtop, and doesn't reproduce on canary. How do I know if this might have caused "stability issues" ?

Checking that no stability issues means checking that there were was not a sufficient amount of crashes introduced from the fix commit. There is a many dashboards and data against which to provide stability checks, but I am not the authoritative voice of stability processes or stability sheriffing and don't want to overstep, so I would check with the Release team go/chrome-sheriffing. 
What I can convey is one of the first places I start is checking the commit against the chromium dashboard >commits with https://chromiumdash.appspot.com/commit/79d1d335f7adaa4cedcd333b30395648d525a1ff that provides relevant links to stability metrics from the chrome crash logs for the instance of canary and dev your commit landed on. 

### ro...@google.com (2022-02-11)

Chatted with Amy and srinivassista@ offline (thanks for your help!) - stability seems to be ok, but merge conflicts + short timelines + fairly obscure vulnerability -> will skip from M98. Merge in M99 early next week, before Tuesday, to let the fixes sit a bit.

### sr...@google.com (2022-02-11)

[Empty comment from Monorail migration]

### ro...@google.com (2022-02-11)

Amy,
It seems that this might be out of date?
"When prompted for a branch, enter refs/branch-heads/####, where #### corresponds to the release branch you are merging to (available on Chromium Dash)."
https://chromium.googlesource.com/chromium/src/+/HEAD/docs/process/merge_request.md#using-gerrit-ui

srinivassista@ suggested the entry should be:
chromium/####

* Is that always the case regardless of the project? (e.g. angle)
* Also note that typing in just the number shows this popup: http://screen/6tAcXY3vmMKKKf7.png, so maybe that could be the suggestion in the doc

### [Deleted User] (2022-02-14)

[Comment Deleted]

### am...@chromium.org (2022-02-14)

I don't own that process or documentation, but I'd be happy to LGTM a CL, if you'd like to land a suggestion/update to the owners. 

The branch for a given milestone ##/### (eg. M98) is generally consistent across commits to Chromium and other projects, such as Dawn, ANGLE, and devtools, but there are different branches for other projects, such as V8 and Skia. The listing of active branches for given milestones are listed at go/chrome-branches. 

### gi...@appspot.gserviceaccount.com (2022-02-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/ca32852e4f162ad41afc1df0e0efaeeb5f4e520f

commit ca32852e4f162ad41afc1df0e0efaeeb5f4e520f
Author: Roman Lavrov <romanl@google.com>
Date: Tue Jan 18 20:05:55 2022

M99: Vulkan: Prevent out of bounds read in divisor emulation path.

Split the replicated part of StreamVertexData out to
StreamVertexDataWithDivisor, there is only a partial argument
overlap between the two.

Bug: chromium:1285885
Change-Id: Ibf6ab3efc6b12b430b1d391c6ae61bd9668b4407
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3398816
Reviewed-by: Jamie Madill <jmadill@chromium.org>
Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org>
Commit-Queue: Roman Lavrov <romanl@google.com>
(cherry picked from commit 5f0badf4541ba52659c937cfe9190d3735a76c10)
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3461414

[modify] https://crrev.com/ca32852e4f162ad41afc1df0e0efaeeb5f4e520f/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp
[modify] https://crrev.com/ca32852e4f162ad41afc1df0e0efaeeb5f4e520f/src/tests/gl_tests/RobustBufferAccessBehaviorTest.cpp


### ro...@google.com (2022-02-14)

Merged both CLs into M99 with this topic: https://chromium-review.googlesource.com/q/topic:crbug%252F1285885

### gi...@appspot.gserviceaccount.com (2022-02-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/angle/angle/+/abdccddb7534a11e62c062ff1320f4bbcc6ce45b

commit abdccddb7534a11e62c062ff1320f4bbcc6ce45b
Author: Geoff Lang <geofflang@google.com>
Date: Tue Feb 15 01:03:06 2022

Fix compile error due to renamed BufferHelper method.

This method was renamed in
https://chromium-review.googlesource.com/c/angle/angle/+/3402882
without any functional change.

Bug: chromium:1285885, chromium:1297266
Change-Id: Id12339f133d167473850622eba1cf1ec005b372f
Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/3461554
Reviewed-by: Kenneth Russell <kbr@chromium.org>

[modify] https://crrev.com/abdccddb7534a11e62c062ff1320f4bbcc6ce45b/src/libANGLE/renderer/vulkan/VertexArrayVk.cpp


### am...@chromium.org (2022-02-28)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1285885?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/angleproject/6897]
[Monorail mergedwith: crbug.com/chromium/1295423]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058461)*
