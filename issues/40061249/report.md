# stack-use-after-return in gpu::gles2::ProgramInfoManager::Program::UpdateES2

| Field | Value |
|-------|-------|
| **Issue ID** | [40061249](https://issues.chromium.org/issues/40061249) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>GPU>Internals |
| **Platforms** | Mac |
| **Reporter** | em...@gmail.com |
| **Assignee** | ba...@chromium.org |
| **Created** | 2022-10-06 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

os:ubuntu 22.04  

chrome version  

Chromium 108.0.5327.0  

Chromium 106.0.5231.2

1. ./chrome --disable-gpu <http://localhost:8001/crash.html>
2. ctlr+c or click close icon to close the browser.
3. asan will immediately reprp stack-user-after-return or heap-buffer-overflow.

**Problem Description:**  

According to a simple analysis, input->name\_length triggered an underflow in the previous operations, resulting in oob on this line[0].  

before crash:  

LOG(ERROR)<<"UpdateES2input->name\_length:"<<input->name\_length;  

[3333090:3333090:1006/202212.502243:ERROR:program\_info\_manager.cc(401)] UpdateES2input->name\_length:24  

[3333090:3333090:1006/202212.502275:ERROR:program\_info\_manager.cc(401)] UpdateES2input->name\_length:1  

[3333090:3333090:1006/202212.502292:ERROR:program\_info\_manager.cc(401)] UpdateES2input->name\_length:1852795251

<https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/program_info_manager.cc;l=401?q=%20program_info_manager.cc:401>  

std::string name(name\_buf, input->name\_length);  

UniformInfo info(input->size, input->type, name);->[0]  

max\_uniform\_name\_length\_ = std::max(  

static\_cast<GLsizei>(name.size() + 1), max\_uniform\_name\_length\_);  

for (int32\_t jj = 0; jj < input->size; ++jj) {  

info.element\_locations.push\_back(locations[jj]);  

}  

uniform\_infos\_.push\_back(info);  

++input;

**Additional Comments:**

\*\*Chrome version: \*\* 106.0.5231.2 \*\*Channel: \*\* Not sure

**OS:** Mac OS

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.4 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.6 KB)
- [asan2.log](attachments/asan2.log) (text/plain, 21.1 KB)
- [repro.mov](attachments/repro.mov) (video/quicktime, 875.0 KB)

## Timeline

### [Deleted User] (2022-10-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-10-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6197079259152384.

### em...@gmail.com (2022-10-06)

I'm not sure cf could repro this issue.
I enter ctrl+c to manually triggered.

### an...@chromium.org (2022-10-06)

Thanks for pointing that out. I forgot the Ctrl+C step in your repro instructions.
I'm curious why this step is required for the problem to occur? Does this mean its essentially a shutdown bug?

### em...@gmail.com (2022-10-06)

I haven't done a detailed analysis yet, so I can't tell if it's a shutdown bug. 
Currently it seems to only reappear when the browser is closed(ctrl+c or click close button).

### an...@chromium.org (2022-10-07)

Unfortunately, I have not been able to reproduce this crash. I'm going to go ahead and set the component in the hopes that people CC'd can chime in.

emilykim8708@, can you try reproducing on the latest linux asan build as well? Does the crash happen every time?

[Monorail components: Internals>GPU>Internals]

### an...@chromium.org (2022-10-07)

Adding a component did not automatically add CCs. Adding some manually based on OWNERs file of relevant directory.
To the CC list, would appreciate a review and any routing as appropriate. Thanks!

### em...@gmail.com (2022-10-08)

@anunoy@chromium.org  
I'm sorry.
I realized that in ubuntu you need to add 2 more flags,--no-sandbox --no-zygote to reproduce. These flags are not needed on macOS. Sorry for the confusion.
tested with new latest linux asan build(gs://chromium-browser-asan/linux-release/asan-linux-release-1056570.zip)

### an...@chromium.org (2022-10-08)

@emilykim8708, still not able to repro on linux with the 2 additional flags and the exact same build.
To the CC list, can you look at the attached asan logs and see if there is anything to be gleaned from them? Thanks!

### an...@chromium.org (2022-10-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-09)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2022-10-10)

I have made a repro video, and I hope it can provide some help for repro.

### an...@chromium.org (2022-10-10)

Assigning to bajones@ based on //gpu/command_buffer/OWNERS.
Setting severity to medium is PoC requires a shutdown.
FoundIn to 106.

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-11)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-12)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-20)

bajones: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-03)

bajones: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### em...@gmail.com (2022-11-03)

Is anyone following this issue?I can trigger dheck in the new debug version(Chromium 108.0.5355.0).
According to the stack trace, it is assumed that the data comes from the gpu side is trusted data that has implemented boundary checking. On the client side, due to performance considerations, only dcheck is enabled.

[1325362:1325362:0100/000000.790332:ERROR:command_buffer_proxy_impl.cc(325)] GPU state invalid after WaitForGetOffsetInRange.

[1325362:1325362:0100/000000.794048:FATAL:program_info_manager.cc(17)] Check failed: offset + size <= data.size() (3772047254 vs. 142682)

    #0 0x555852e78797 in backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4434:13
    #1 0x5558689e539c in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:879:7
    #2 0x55586869bd22 in StackTrace ./../../base/debug/stack_trace.cc:221:12
    #3 0x55586869bd22 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack_trace.cc:218:28
    #4 0x5558686fcfa6 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:718:29
    #5 0x5558686ff84d in logging::LogMessage::~LogMessage() ./../../base/logging.cc:712:27
    #6 0x55586e443b4a in char const* (anonymous namespace)::LocalGetAs<char const*>(base::span<signed char const, 18446744073709551615ul>, unsigned int, unsigned long) ./../../gpu/command_buffer/client/program_info_manager.cc:17:3
    #7 0x55586e44288d in gpu::gles2::ProgramInfoManager::Program::UpdateES2(base::span<signed char const, 18446744073709551615ul>) ./../../gpu/command_buffer/client/program_info_manager.cc:399:28
    #8 0x55586e44901f in gpu::gles2::ProgramInfoManager::GetProgramInfo(gpu::gles2::GLES2Implementation*, unsigned int, gpu::gles2::ProgramInfoManager::ProgramInfoType) ./../../gpu/command_buffer/client/program_info_manager.cc:634:13
    #9 0x55586e449dbd in gpu::gles2::ProgramInfoManager::GetProgramiv(gpu::gles2::GLES2Implementation*, unsigned int, unsigned int, int*) ./../../gpu/command_buffer/client/program_info_manager.cc:708:19
    #10 0x55586e324ded in gpu::gles2::GLES2Implementation::GetProgramivHelper(unsigned int, unsigned int, int*) ./../../gpu/command_buffer/client/gles2_implementation.cc:1840:58
    #11 0x55586e3aa2ce in gpu::gles2::GLES2Implementation::GetProgramiv(unsigned int, unsigned int, int*) ./../../gpu/command_buffer/client/gles2_implementation_impl_autogen.h:1154:7
    #12 0x555880e0efb9 in CacheInfoIfNeeded ./../../third_party/blink/renderer/modules/webgl/webgl_program.cc:144:7
    #13 0x555880e0efb9 in blink::WebGLProgram::LinkStatus(blink::WebGLRenderingContextBase*) ./../../third_party/blink/renderer/modules/webgl/webgl_program.cc:63:3
    #14 0x55588095f5ba in blink::WebGLRenderingContextBase::useProgram(blink::WebGLProgram*) ./../../third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc:6898:28
    #15 0x555880c4ba31 in blink::(anonymous namespace)::v8_webgl2_rendering_context::UseProgramOperationCallback(v8::FunctionCallbackInfo<v8::Value> const&) ./gen/third_party/blink/renderer/bindings/modules/v8/v8_webgl2_rendering_context.cc:24245:17
    #16 0x5558597b04dc in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) ./../../v8/src/api/api-arguments-inl.h:146:3
    #17 0x5558597ac544 in v8::internal::MaybeHandle<v8::internal::Object> v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate*, v8::internal::Handle<v8::internal::HeapObject>, v8::internal::Handle<v8::internal::FunctionTemplateInfo>, v8::internal::Handle<v8::internal::Object>, unsigned long*, int) ./../../v8/src/builtins/builtins-api.cc:112:36
    #18 0x5558597a797d in v8::internal::Builtin_Impl_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:143:5
    #19 0x5558597a6200 in v8::internal::Builtin_HandleApiCall(int, unsigned long*, v8::internal::Isolate*) ./../../v8/src/builtins/builtins-api.cc:130:1
#18 0x5557dfea85b8 <unknown>
Task trace:
    #0 0x55587aa69484 in blink::HTMLDocumentParser::SchedulePumpTokenizer(bool) ./../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:982:7
    #1 0x55586a6fc3c8 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::Accept(mojo::Message*) ./../../ipc/ipc_mojo_bootstrap.cc:952:13
Crash keys:
  "gpu-gl-renderer" = "ANGLE (Google, Vulkan 1.3.0 (SwiftShader Device (Subzero) (0x0000C0DE)), SwiftShader driver-5.0.0)"
  "gpu-gl-vendor" = "Google Inc. (Google)"
  "gpu-generation-intel" = "0"
  "gpu-vsver" = "1.00"
  "gpu-psver" = "1.00"
  "gpu-driver" = "5.0.0"
  "gpu-devid" = "0xffff"
  "gpu-venid" = "0xffff"
  "view-count" = "2"
  "loaded-origin-0" = "http://localhost:8001"
  "web-frame-count" = "2"
  "top-origin" = "null"
  "url-chunk" = "http://localhost:8001/poc.html"
  "blink_scheduler_async_stack" = "0x55587AA69484 0x55586A6FC3C8"
  "v8_ro_space_firstpage_address" = "0x7d8300000000"
  "v8_isolate_address" = "0x630000000400"
  "variations" = "313957be-3ef44cd2,2510663e-3f4a17df,df319cb2-27e0e1e8,13e2821-46a4c4e1,eddd0d82-3f4a17df,f2855e3d-de2b6078,cae31965-2f8546fe,7301b698-3f4a17df,ffe207ef-3f4a17df,4d936449-fd549ada,f0f05f6-3f4a17df,250dda8b-3f4a17df,4749874c-455e925b,7c2504d0-3f4a17df,c98a686c-3f4a17df,1acce950-3f4a17df,dbf7a8af-3f4a17df,a2fd384c-cc71bb94,e521d2ef-3f4a17df,5c4d440e-58c8ac88,65570806-377be55a,42f1f10d-98837767,18324944-3f4a17df,4d40c903-20e31142,4852ec7f-3f4a17df,d16d5274-3f4a17df,5f2c0f7c-3f4a17df,3fd33f16-da51fc56,8b5e9272-5124c949,80a52ca2-9c6dd96d,62cb9b8b-41986bdd,f588ef31-3f4a17df,c7053c9f-9a93b053,911e33b9-3f4a17df,36d5ee52-3f4a17df,391562d6-3f4a17df,e79de56c-dee0823,8bccc03b-3f4a17df,69d4ebd5-3f4a17df,5349039a-3f4a17df,9e5c75f1-30e1b12b,15ee6537-3f4a17df,b30184e3-3f4a17df,255dfea8-cf12f279,da493d3c-3f4a17df,e28cd73c-3f4a17df,df4ed2c4-aa3d81ae,3482a891-410c5d63,b7a22696-2cd5fcd8,d3566fbd-c6f74b94,a779bb20-3f4a17df,646a148-6847cb89,5f36436a-f799c15e,7fb629a1-60fdb59,2da2abac-b7f59038,59e098fc-3f4a17df,baee3c29-3f4a17df,9fe21c85-3f4a17df,7d74eac0-7d74eac0,d990c4ac-3f4a17df,a18444ea-a18444ea,b0ca2a47-3f4a17df,6e69a63-3f4a17df,ef4764d7-c9f4d4ef,9909b8ac-3f4a17df,1fce7d57-3f4a17df,7760b5b2-3f4a17df,e8c68789-49a20295,caa76e48-caa76e48,b0f15b33-b0f15b33,34a9ddc3-54a64e37,ad4acdda-3f4a17df,931c5f72-3f4a17df,ade3efeb-e1cc0f14,b1ceb06f-3f4a17df,5e7b62b9-3f4a17df,1d0518a-3f4a17df,38ac144c-3f4a17df,1166396-1166396,8d7344de-3f4a17df,b53f3ef9-3f4a17df,2856aa31-3f4a17df,1bb6a450-3f4a17df,e9e64bcb-3f4a17df,f406744f-3f4a17df,ef1cfe77-3f4a17df,363012bc-3f4a17df,483d5a5e-d379aaa3,13494a51-3f4a17df,a79ba57a-3d47f4f4,4949c1d8-3f4a17df,9f7bb00b-3f4a17df,55c6e56f-a1ba80e8,f6e27768-f695fd79,3b96a1d-3f4a17df,6b5336a9-3f4a17df,6becb1e-a6ea97a2,595f5eb0-f23d1dea,dba92675-f23d1dea,abbcc82f-3d47f4f4,a393b0ae-d47548ba,88e143f7-c7440213,d0143dc1-3f4a17df,15d3083e-5ce60213,57675af7-3f4a17df,7a97dfab-3f4a17df,234de0a0-ace4e138,19ca6892-3f4a17df,c9e4cf65-802823a4,e5726113-3f4a17df,6fbe2188-3f4a17df,eabb590b-3f4a17df,e711bfd-3f4a17df,4e3ec83a-aa9b29e7,4ea303a6-3f4a17df,3042ad4b-ad2fa222,7d6e65a8-89a4b7af,bdb15e19-3f4a17df,f654ad46-c94f66c2,cbc04857-3f4a17df,42f0e0ea-75d6947c,bde7927d-bab20a64,55ba4cfa-3f4a17df,fc7e4d22-3f4a17df,7b9d3e0c-1dfe4688,2b0207ee-2b0207ee,31af02a2-3f4a17df,3e7d7783-f38a9353,c11c16b-3f4a17df,ba227809-3f4a17df,53879ff4-3f4a17df,58155072-3f4a17df,357a64de-dee0823,1a80e9be-3898461f,1b69a7e4-3f4a17df,"
  "num-experiments" = "135"
  "switch-16" = "--field-trial-handle=0,i,10266690410397985417,173880824022083217"
  "switch-15" = "--shared-files=v8_context_snapshot_data:100"
  "switch-14" = "--launch-time-ticks=35298866910"
  "switch-13" = "--time-ticks-at-unix-epoch=-1667466990678321"
  "switch-12" = "--renderer-client-id=5"
  "switch-11" = "--enable-main-frame-before-activation"
  "switch-10" = "--num-raster-threads=4"
  "switch-9" = "--lang=en-US"
  "switch-8" = "--disable-gpu-compositing"
  "switch-7" = "--no-sandbox"
  "switch-6" = "--change-stack-guard-on-fork=enable"
  "osarch" = "x86_64"
  "pid" = "1325362"
  "ptype" = "renderer"
  "switch-5" = "--event-path-policy=0"
  "switch-4" = "--display-capture-permissions-policy-allowed"
  "switch-3" = "--user-data-dir=/tmp/xx2"
  "switch-2" = "--enable-crash-reporter=,"
  "switch-1" = "--crashpad-handler-pid=1325284"
  "num-switches" = "17"

### ke...@chromium.org (2022-11-07)

bajones@: Friendly ping, can you have a look at this or help find a different owner to have a look?

### em...@gmail.com (2022-11-17)

Friendly ping.I'm just wondering. Is there any progress?

### an...@chromium.org (2022-11-18)

Pinging CC list @geofflang, @vmiura and zmo@. Are anyone you able to help take a look? Thanks!

### em...@gmail.com (2022-11-27)

I analyzed the issue today and found the cause of the issue. Here I update the information.
In function GetBucketContents[0], if |size| is greater than 32768 (kStartSize = 32 * 1024), the while loop will be executed twice [1]. For the first time, call memcpy[4] to copy the data obtained from helper_->GetBucketStart[2].The second time, call memcpy[4] again to copy the data obtained from helper_->GetBucketData[3].

The data copied for the first time contains ProgramInfoHeader[5] + part of the Inputs data (ProgramInput* (header->num_attribs + header->num_uniforms)), and the data copied for the second time contains the remaining Inputs data.
The normal call chain is as follows:
GetBucketContents >> helper_->GetBucketStart >> CommonDecoder::HandleGetBucketStart(GPU Process) >> memcpy[4] >> helper_->GetBucketData >> CommonDecoder::HandleGetBucketData(GPU Process) memcpy[4] >> ProgramInfoManager::Program::UpdateES2

If the browser is closed at the end of the first while loop (the gpu service is terminated), helper_->GetBucketData[3] will not be called, and the data after offset 32768 in [data] will be filled with invalid data, which is the valid ProgramInfoHeader+ Composition of invalid inputs data, resulting in subsequent oob.
The call chain is as follows, the call of CommonDecoder::HandleGetBucketData is missing.
GetBucketContents >> helper_->GetBucketStart >> CommonDecoder::HandleGetBucketStart(GPU Process) >> memcpy[4] >> helper_->GetBucketData >>  memcpy[4] >> ProgramInfoManager::Program::UpdateES2(oob)

bool ImplementationBase::GetBucketContents(uint32_t bucket_id,
                                           std::vector<int8_t>* data) {
  TRACE_EVENT0("gpu", "ImplementationBase::GetBucketContents");
  DCHECK(data);
  const uint32_t kStartSize = 32 * 1024;
  ScopedTransferBufferPtr buffer(kStartSize, helper_, transfer_buffer_);
  if (!buffer.valid()) {
    return false;
  }
  uint32_t size = 0;
  {
    // The Result pointer must be scoped to this block because it can be
    // invalidated below if resizing the ScopedTransferBufferPtr causes the
    // transfer buffer to be reallocated.
    typedef cmd::GetBucketStart::Result Result;
    auto result = GetResultAs<Result>();
    if (!result) {
      return false;
    }
    *result = 0;
    helper_->GetBucketStart(bucket_id, GetResultShmId(), result.offset(),
                            buffer.size(), buffer.shm_id(), buffer.offset());  -->[2]
    WaitForCmd();
    size = *result;
  }
  data->resize(size);
  uint32_t ii = 0;
  if (size > 0u) {
    uint32_t offset = 0;
    while (size) {            -->[1]
      if (!buffer.valid()) {
        buffer.Reset(size);
        if (!buffer.valid()) {
          return false;
        }
        helper_->GetBucketData(bucket_id, offset, buffer.size(),
                               buffer.shm_id(), buffer.offset());[3]
        WaitForCmd();           
      }
      ii++;
      uint32_t size_to_copy = std::min(size, buffer.size());
      memcpy(&(*data)[offset], buffer.address(), size_to_copy);[4]
      offset += size_to_copy;
      size -= size_to_copy;
      buffer.Release();
    }
[0]https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/implementation_base.cc;drc=df32cca3141ae8a74c1910b51f8c779480255be4;l=268
[5]https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/common/gles2_cmd_format.h;drc=df32cca3141ae8a74c1910b51f8c779480255be4;l=97





### [Deleted User] (2022-11-30)

[Empty comment from Monorail migration]

### ba...@chromium.org (2022-12-02)

Thank you for this detailed analysis of the issue! I'm sure it'll make a fix much easier.

I am able to reproduce the issue locally using the steps in the first comment, and can confirm that your breakdown of the problem seems accurate. I don't have much experience with this specific area of the command buffer, but it seems like the fix should be relatively straightforward? Put up https://chromium-review.googlesource.com/c/chromium/src/+/4076865 for review and I'll loop in developers with more experience in this area to help verify.

### gi...@appspot.gserviceaccount.com (2022-12-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4af6ef2fbe59c6a85f2f8fb3fb917906116ba02b

commit 4af6ef2fbe59c6a85f2f8fb3fb917906116ba02b
Author: Brandon Jones <bajones@chromium.org>
Date: Fri Dec 02 21:34:35 2022

Early terminate GetBucketContents if WaitForCmd fails

This should avoid the scenario outlined in crbug.com/1371859 where the
command isn't run due to the GPU process shutting down, but the memcpy
is attempted anyway.

Bug: 1371859
Change-Id: Ib2a4b735365f29d092be8003ba668854be1d5c3b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4076865
Reviewed-by: Victor Miura <vmiura@chromium.org>
Commit-Queue: Brandon Jones <bajones@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1078779}

[modify] https://crrev.com/4af6ef2fbe59c6a85f2f8fb3fb917906116ba02b/gpu/command_buffer/client/implementation_base.cc
[modify] https://crrev.com/4af6ef2fbe59c6a85f2f8fb3fb917906116ba02b/gpu/command_buffer/client/implementation_base.h


### ba...@chromium.org (2022-12-02)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-12-03)

Hi,@bajones,Thanks for the quick response.
After above patch,although memory corruption is no longer triggered, but the |result|[0] in subsequent executions info->UpdateES2(result) will still contain invalid data.
  switch (type) {
    case kES2:
      {
        base::AutoUnlock unlock(lock_);
        // lock_ can't be held across IPC call or else it may deadlock in
        // pepper. http://crbug.com/418651
        gl->GetProgramInfoCHROMIUMHelper(program, &result);
      }
      info->UpdateES2(result);[0]
      break;
https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/client/program_info_manager.cc;drc=05dfbc82b07e06f610b8f2fecaa4d272430cc451;l=634

I suggest that the above patch can be improved, clean up the vector when early terminate GetBucketContents.


diff --git a/gpu/command_buffer/client/implementation_base.cc b/gpu/command_buffer/client/implementation_base.cc
index 4af30994b8ce9..c9936be0430aa 100644
--- a/gpu/command_buffer/client/implementation_base.cc
+++ b/gpu/command_buffer/client/implementation_base.cc
@@ -301,9 +301,13 @@ bool ImplementationBase::GetBucketContents(uint32_t bucket_id,
         }
         helper_->GetBucketData(bucket_id, offset, buffer.size(),
                                buffer.shm_id(), buffer.offset());
       if (!WaitForCmd()) {
+          data->clear();
          return false;
       }
       }
       uint32_t size_to_copy = std::min(size, buffer.size());


### [Deleted User] (2022-12-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7023e1fafcd55f31c4150328d8afbf38b28ade39

commit 7023e1fafcd55f31c4150328d8afbf38b28ade39
Author: Brandon Jones <bajones@chromium.org>
Date: Wed Dec 07 01:45:54 2022

Clear data if GetBucketContents early terminates

Follow up to
https://chromium-review.googlesource.com/c/chromium/src/+/4076865

Bug: 1371859
Change-Id: I33dbcd6e7e8094d44fe3d7623dc9c152224342e2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4083922
Commit-Queue: Brandon Jones <bajones@chromium.org>
Reviewed-by: Victor Miura <vmiura@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1080121}

[modify] https://crrev.com/7023e1fafcd55f31c4150328d8afbf38b28ade39/gpu/command_buffer/client/implementation_base.cc


### ba...@chromium.org (2022-12-07)

Thanks for the suggestion!

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $3,000 for this report of a highly mitigated security bug, including patch bonus and also some appreciation for the all the information you provided to help move this bug alone in the process to get it fixed and resolved. Thank you for all your efforts here all the way to patch suggestion -- they were all much appreciated! 

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-12-14)

Note to future self when fix ships in stable channel release -- credit / acknowledgement for this issue to go to: 7o8v and Cassidy Kim(@cassidy6564)

### am...@chromium.org (2023-02-03)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1371859?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061249)*
