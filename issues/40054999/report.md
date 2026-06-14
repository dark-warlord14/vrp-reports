# Security: webgl2 BlitFramebuffer Stencil Attachment heap-overflow

| Field | Value |
|-------|-------|
| **Issue ID** | [40054999](https://issues.chromium.org/issues/40054999) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Windows |
| **Reporter** | [Deleted User] |
| **Assignee** | ge...@chromium.org |
| **Created** | 2021-02-27 |
| **Bounty** | $7,500.00 |

## Description

#BlitFramebuffer Stencil Attachment 

##Crash Environment:
Google Chrome build version 88.0.4324.190 (Official Build) (64-bit)
Google Chrome Canary build version 90.0.4430.0 (Official Build) canary (64-bit)
on Windows

##Crash Analysis:
Crash occurs at libglesv2!memcpy+0xa2 at the following instruction:

> mov     byte ptr [rax],cl

**libglesv2!memcpy** function is called by **libglesv2!rx::`anonymous namespace'::StretchedBlitNearest_PixelByPixel**. The following code snippet from **libglesv2!rx::`anonymous namespace'::StretchedBlitNearest_PixelByPixel** function shows the code at which crash occurs:

>for (int writeColumn = clippedDestArea.x; writeColumn < xMax; writeColumn++)
>        {
>            float xPerc    = static_cast<float>(writeColumn - destArea.x) / (destArea.width - 1);
>            float xRounded = floor(xPerc * (sourceArea.width - 1) + 0.5f);
>            unsigned int readColumn = static_cast<unsigned int>(
>                gl::clamp(sourceArea.x + xRounded, 0, sourceSize.height - 1));
>
>            const uint8_t *sourcePixel =
>                sourceData + readRow * sourceRowPitch + readColumn * srcPixelStride + readOffset;
>
>            uint8_t *destPixel =
>                destData + writeRow * destRowPitch + writeColumn * destPixelStride + writeOffset;
>
>            memcpy(destPixel, sourcePixel, copySize);
>        }

From the above code **memcpy** function causes the crash as **destPixel** points out of bounds. **destPixel** is calculated using user supplied values and hence can be controlled.

The syntax for **blitFrambuffer** is:

> void gl.blitFramebuffer(srcX0, srcY0, srcX1, srcY1, dstX0, dstY0, dstX1, dstY1,mask, filter);

For the calculation of **destPixel**, **writeRow** and **wrietColumn** are used which correspond to **dstX0** and **dstY0** respectively from **blitFramebuffer**.

The crash occurs due to incorrect mapping and clamping of destination which results in out of bounds write into the destination. From the crash instruction it is clear that **rax** register contains **destPixel** pointer. 

##Register values at crash:
```
3:046> r
rax=000001922dc8c343 rbx=000001922dc8c343 rcx=0000000000000000
rdx=000001922da90c03 rsi=0000008ae81fddc8 rdi=0000008ae81fde40
rip=00007ffe0aef3ea2 rsp=0000008ae81fd828 rbp=000001922da90c03
 r8=0000000000000001  r9=00007ffe0aa40000 r10=000001922da90c03
r11=000001922dc8c343 r12=00000000000020d0 r13=00000000000020d1
r14=00000000000020d5 r15=0000000000000003
iopl=0         nv up ei pl nz na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010206
libglesv2!memcpy+0xa2:
00007ffe`0aef3ea2 8808            mov     byte ptr [rax],cl ds:00000192`2dc8c343=??
```

The following function call from the PoC causes crash:
> gl1.blitFramebuffer( 0,0,30,4,8400, 16000, 8440, 16400, gl1.STENCIL_BUFFER_BIT, gl1.NEAREST );

From the above register values and the values in **blitFramebuffer** function it is observed:
**r12** contains user supplied value **dstX0** (8400) which is the value for **clippedDestArea.x**.
**r13** contains the value of **writeColumn** (8401) which is initialized with **dstX0** value and then incremented in for loop.
**rax** and **rbx** contain the **destPixel** pointer.


##Call Stack:
```  Child-SP          RetAddr               Call Site
00 0000008a`e81fd828 00007ffe`0abb1179     libglesv2!memcpy+0xa2 [d:\A01\_work\6\s\src\vctools\crt\vcruntime\src\string\amd64\memcpy.asm @ 255] 
01 (Inline Function) --------`--------     libglesv2!rx::`anonymous namespace'::StretchedBlitNearest_PixelByPixel+0x18b [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp @ 124] 
02 0000008a`e81fd830 00007ffe`0abb1471     libglesv2!rx::`anonymous namespace'::StretchedBlitNearest+0x339 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp @ 158] 
03 0000008a`e81fd930 00007ffe`0abb0b8f     libglesv2!rx::Blit11::copyAndConvertImpl+0x271 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp @ 1271] 
04 0000008a`e81fda70 00007ffe`0abb0686     libglesv2!rx::Blit11::copyAndConvert+0x1af [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp @ 1308] 
05 0000008a`e81fdba0 00007ffe`0abb053f     libglesv2!rx::Blit11::copyDepthStencilImpl+0x136 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp @ 1211] 
06 0000008a`e81fdc80 00007ffe`0abda5a6     libglesv2!rx::Blit11::copyStencil+0x4f [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Blit11.cpp @ 1060] 
07 0000008a`e81fdcf0 00007ffe`0abc3550     libglesv2!rx::Renderer11::blitRenderbufferRect+0xb66 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Renderer11.cpp @ 3756] 
08 0000008a`e81fdf40 00007ffe`0ac0fe3f     libglesv2!rx::Framebuffer11::blitImpl+0x450 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\d3d11\Framebuffer11.cpp @ 374] 
09 0000008a`e81fe040 00007ffe`0aae29c7     libglesv2!rx::FramebufferD3D::blit+0x6f [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\renderer\d3d\FramebufferD3D.cpp @ 245] 
0a 0000008a`e81fe0c0 00007ffe`0aabf508     libglesv2!gl::Framebuffer::blit+0x27 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Framebuffer.cpp @ 1546] 
0b 0000008a`e81fe110 00007ffe`0aa5985d     libglesv2!gl::Context::blitFramebuffer+0x208 [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libANGLE\Context.cpp @ 4052] 
0c 0000008a`e81fe1e0 00007ffd`fa218b0f     libglesv2!GL_BlitFramebuffer+0x12d [c:\b\s\w\ir\cache\builder\src\third_party\angle\src\libGLESv2\entry_points_gles_3_0_autogen.cpp @ 232] 
0d 0000008a`e81fe290 00007ffd`f8c0cb6d     chrome!gl::GLApiBase::glBlitFramebufferFn+0x6f [c:\b\s\w\ir\cache\builder\src\ui\gl\gl_bindings_autogen_gl.cc @ 3223] 
0e 0000008a`e81fe310 00007ffd`f8c0cae8     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoBlitFramebufferCHROMIUM+0x6d [c:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_doers.cc @ 3359] 
0f 0000008a`e81fe3a0 00007ffd`f360181d     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::HandleBlitFramebufferCHROMIUM+0x68 [c:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough_handlers_autogen.cc @ 3707] 
10 (Inline Function) --------`--------     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl+0xc1 [c:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 856] 
11 0000008a`e81fe430 00007ffd`f1c20495     chrome!gpu::gles2::GLES2DecoderPassthroughImpl::DoCommands+0xed [c:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\gles2_cmd_decoder_passthrough.cc @ 794] 
12 0000008a`e81fe4b0 00007ffd`f1c201ba     chrome!gpu::CommandBufferService::Flush+0xe5 [c:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\command_buffer_service.cc @ 72] 
13 0000008a`e81fe5c0 00007ffd`f3fb8616     chrome!gpu::CommandBufferStub::OnAsyncFlush+0xea [c:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc @ 518] 
14 (Inline Function) --------`--------     chrome!base::DispatchToMethodImpl+0x18 [c:\b\s\w\ir\cache\builder\src\base\tuple.h @ 52] 
15 (Inline Function) --------`--------     chrome!base::DispatchToMethod+0x18 [c:\b\s\w\ir\cache\builder\src\base\tuple.h @ 60] 
16 (Inline Function) --------`--------     chrome!IPC::DispatchToMethod+0x18 [c:\b\s\w\ir\cache\builder\src\ipc\ipc_message_templates.h @ 52] 
17 (Inline Function) --------`--------     chrome!IPC::MessageT<GpuCommandBufferMsg_AsyncFlush_Meta,std::tuple<int,unsigned int,std::vector<gpu::SyncToken,std::allocator<gpu::SyncToken> > >,void>::Dispatch+0x52 [c:\b\s\w\ir\cache\builder\src\ipc\ipc_message_templates.h @ 140] 
18 0000008a`e81fe6c0 00007ffd`f4e77a08     chrome!gpu::CommandBufferStub::OnMessageReceived+0x2a6 [c:\b\s\w\ir\cache\builder\src\gpu\ipc\service\command_buffer_stub.cc @ 166] 
19 (Inline Function) --------`--------     chrome!gpu::GpuChannel::HandleMessageHelper+0x1a [c:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc @ 630] 
1a 0000008a`e81fe860 00007ffd`f3fac960     chrome!gpu::GpuChannel::HandleMessage+0xf8 [c:\b\s\w\ir\cache\builder\src\gpu\ipc\service\gpu_channel.cc @ 588] 
1b (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x7 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 101] 
1c 0000008a`e81fe8f0 00007ffd`f460bd4e     chrome!gpu::Scheduler::RunNextTask+0x470 [c:\b\s\w\ir\cache\builder\src\gpu\command_buffer\service\scheduler.cc @ 577] 
1d (Inline Function) --------`--------     chrome!base::OnceCallback<void ()>::Run+0x10 [c:\b\s\w\ir\cache\builder\src\base\callback.h @ 101] 
1e 0000008a`e81fea20 00007ffd`f460b179     chrome!base::TaskAnnotator::RunTask+0x1ce [c:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc @ 163] 
1f (Inline Function) --------`--------     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0x31c [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 351] 
20 0000008a`e81feb60 00007ffd`f3448304     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x3c9 [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 264] 
21 0000008a`e81fed20 00007ffd`f21cd9cc     chrome!base::MessagePumpDefault::Run+0xb4 [c:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_default.cc @ 41] 
22 0000008a`e81fedc0 00007ffd`f23df798     chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x7c [c:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 463] 
23 0000008a`e81fee20 00007ffd`f2ae248d     chrome!base::RunLoop::Run+0x1a8 [c:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 135] 
24 0000008a`e81fef70 00007ffd`f3f6c434     chrome!content::GpuMain+0x4ad [c:\b\s\w\ir\cache\builder\src\content\gpu\gpu_main.cc @ 453] 
25 (Inline Function) --------`--------     chrome!content::RunOtherNamedProcessTypeMain+0x5a8 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 607] 
26 0000008a`e81ff2d0 00007ffd`f216e86d     chrome!content::ContentMainRunnerImpl::Run+0x764 [c:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 946] 
27 (Inline Function) --------`--------     chrome!content::RunContentProcess+0x336 [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 372] 
28 0000008a`e81ff400 00007ffd`f216b831     chrome!content::ContentMain+0x37d [c:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 398] 
29 0000008a`e81ff610 00007ff6`0608866e     chrome!ChromeMain+0x1a1 [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 144] 
2a 0000008a`e81ff730 00007ff6`06088266     chrome_exe!MainDllLoader::Launch+0x2ee [c:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169] 
2b 0000008a`e81ff9b0 00007ff6`060e2b22     chrome_exe!wWinMain+0xb96 [c:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 370] 
2c (Inline Function) --------`--------     chrome_exe!invoke_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 118] 
2d 0000008a`e81ffdb0 00007ffe`7b607034     chrome_exe!__scrt_common_main_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl @ 288] 
2e 0000008a`e81ffdf0 00007ffe`7bffd241     KERNEL32!BaseThreadInitThunk+0x14
2f 0000008a`e81ffe20 00000000`00000000     ntdll!RtlUserThreadStart+0x21
```


## Attachments

- poc-blit-stencil.html (text/plain, 741 B)

## Timeline

### [Deleted User] (2021-02-27)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-03-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5180207217311744.

### cl...@chromium.org (2021-03-02)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5151825125507072.

### [Deleted User] (2021-03-04)

Since the ASAN builds do not catch this crash, it's probable that clusterfuzz will not be able to reproduce this. Can someone manually verify this please. 

### do...@chromium.org (2021-03-05)

+capn/+sugoi, is this another issue in a soon to be deprecated backend?

[Monorail components: Internals>GPU>ANGLE]

### me...@google.com (2021-03-10)

Tentatively assigning labels.

### ca...@chromium.org (2021-03-10)

This is in ANGLE's Direct3D 11 backend.

### [Deleted User] (2021-03-10)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-13)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@google.com (2021-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-03-28)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-19)

Any human update to this bug would be nice. 

### ge...@chromium.org (2021-04-20)

Sorry this fell off my radar. It was just fixed by https://chromium.googlesource.com/angle/angle/+/b574643ef28c92fcea5122dd7a72acb42a514eed but not tagged with this bug.

### ge...@chromium.org (2021-04-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-20)

Was this bug a duplicate because I see another id being referenced in the fix?

### ge...@chromium.org (2021-04-20)

Yes, this one was reported first though.

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-21)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M90. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to future beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M91. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-21)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-04-21)

Possibly duplicate of https://crbug.com/chromium/1199402?

### ad...@google.com (2021-04-21)

Merges are being tracked on https://crbug.com/chromium/1199402.

### ad...@google.com (2021-04-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-23)

Updating to merge https://crbug.com/chromium/1199402 into this one since work and fix landed there (as well as merge), but also note for self/VRP this is the earlier reported bug (which is to be credited and reviewed by the VRP Panel).  

### am...@chromium.org (2021-04-23)

[Comment Deleted]

### am...@google.com (2021-04-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-27)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-04-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-04-28)

Congratulations, Omair. The VRP Panel has decided to award you $7500 for this report. Nice work! 

### [Deleted User] (2021-04-29)

Thanks!
Amy, can you credit the vulnerability to both of us Abraruddin Khan and Omair.

### am...@chromium.org (2021-04-29)

Sure thing, Omair! Updated and will be reflected accordingly in the release notes for the release this fix is shipped in. 

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-30)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1182937?no_tracker_redirect=1

[Monorail mergedinto: crbug.com/chromium/1199402]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-12)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054999)*
