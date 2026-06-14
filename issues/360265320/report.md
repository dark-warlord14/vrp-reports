# [Skia] Integer overflow in MeshOp::onCombineIfPossible

| Field | Value |
|-------|-------|
| **Issue ID** | [360265320](https://issues.chromium.org/issues/360265320) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2023-6345 |
| **Reporter** | hy...@gmail.com |
| **Assignee** | mi...@google.com |
| **Created** | 2024-08-16 |
| **Bounty** | $15,000.00 |

## Description

### Steps to reproduce

(Chromium)

1. Apply the `chromium.diff` renderer patch to chromium.
2. Run `genskpic.py` to generate `drawable_picture.skp.hh`, then move the generated file to `src/gpu/command_buffer/client`.
3. Build and start the browser.
4. Open `index.html`.
5. The GPU process will crash.

(Skia standalone)

1. Run `genskpic.py` to generate a `.skp` file.
2. You can now run it in skpbench using: `./out/asan/skpbench --src pic.skp --config gles`.
3. UBSAN crash will happen.

### Vulnerability Details

In Skia, when drawing Skia Picture with many `DRAW_VERTICES_OBJECT` operations, `MeshOp::onCombineIfPossible` will be called to test how many meshes are allowed to be combined into a single operation.
This is done by concatenating vertices and indices counts of all possible meshes:

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/DrawMeshOp.cpp;l=1216>

However, while there are checks to prevent `fVertexCount` from overflowing, no checks are made to ensure that the addition of `fIndexCount` and `that->fIndexCount` in [1] will not overflow.
So by drawing a triangular mesh with, for example, 3 vertices and 3000000 indices where each indice is an index to a vertice we can easily make `fIndexCount` (a 32-bit integer) overflow.

(The reason I'm keeping the number of vertices low (3) is to avoid the check at [2] when merging meshes and because I need to optimize size for PoC).

```
GrOp::CombineResult MeshOp::onCombineIfPossible(GrOp* t, SkArenaAlloc*, const GrCaps& caps) {
    auto that = t->cast<MeshOp>();
    ...
    if (SkToBool(fIndexCount) && fVertexCount > SkToInt(UINT16_MAX) - that->fVertexCount) { // <-- [2]
        return CombineResult::kCannotCombine;
    }
    ...
    fMeshes.move_back_n(that->fMeshes.size(), that->fMeshes.begin());
    fVertexCount += that->fVertexCount;
    fIndexCount  += that->fIndexCount; // <-- [1]
    return CombineResult::kMerged;
}

```

Later, `MeshOp::onPrepareDraws` will be called to allocate enough space for all index data using the overflowed `fIndexCount` [3], and then will copy each individual mesh to the allocated buffer [4] which ends up in an OOB write.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/ops/DrawMeshOp.cpp;l=1119>

```
void MeshOp::onPrepareDraws(GrMeshDrawTarget* target) {
    ...

    std::tie(indexBuffer, firstIndex) = fMeshes[0].gpuIB();
    if (fIndexCount && !indexBuffer) {
        uint16_t* indices = nullptr;
        indices = target->makeIndexSpace(fIndexCount, &indexBuffer, &firstIndex); // <-- [3]
        if (!indices) {
            SkDebugf("Could not allocate indices.\n");
            return;
        }
        // We can just copy the first mesh's indices. Subsequent meshes need their indices adjusted.
        std::copy_n(fMeshes[0].indices(), fMeshes[0].indexCount(), indices);
        int voffset = fMeshes[0].vertexCount();
        int ioffset = fMeshes[0].indexCount();
        for (int m = 1; m < fMeshes.size(); ++m) {
            for (int i = 0; i < fMeshes[m].indexCount(); ++i) {
                indices[ioffset++] = fMeshes[m].indices()[i] + voffset; // <-- [4]
            }
            voffset += fMeshes[m].vertexCount();
        }
        SkASSERT(voffset == fVertexCount);
        SkASSERT(ioffset == fIndexCount);
    } else if (indexBuffer) {
        SkASSERT(fMeshes.size() == 1);
        SkASSERT(firstIndex % sizeof(uint16_t) == 0);
        firstIndex /= sizeof(uint16_t);
    }

    ...
}

```

This could be achieved by a compromised renderer.

Having to keep the number of vertices low affects a bit the control of the attacker of the value being written since each indice must be an index to a vertice. I'm only doing this here for demonstration purposes (optimizing size of PoC), in a real attack scenario an attacker *might* prefer to have some bigger meshes to have better control of the value where one of the first meshes will have more vertices than the remaining meshes.

Fix:

```
diff --git a/src/gpu/ganesh/ops/DrawMeshOp.cpp b/src/gpu/ganesh/ops/DrawMeshOp.cpp
index eaa3c7d85f..f4f5625fff 100644
--- a/src/gpu/ganesh/ops/DrawMeshOp.cpp
+++ b/src/gpu/ganesh/ops/DrawMeshOp.cpp
@@ -1232,7 +1232,7 @@ GrOp::CombineResult MeshOp::onCombineIfPossible(GrOp* t, SkArenaAlloc*, const Gr
         return CombineResult::kCannotCombine;
     }
 
-    if (fVertexCount > INT32_MAX - that->fVertexCount) {
+    if (fVertexCount > INT32_MAX - that->fVertexCount || fIndexCount > INT32_MAX - that->fIndexCount) {
         return CombineResult::kCannotCombine;
     }
     if (SkToBool(fIndexCount) != SkToBool(that->fIndexCount)) {

```
### Type of crash

GPU Process

### Environment

Chrome version: 129.0.6661.0 (Developer Build) (64-bit).

OS: Linux.

### Reporter Credit

Renan Rios (@hyhy\_100)

Thanks!

## Attachments

- [CHROME_ASAN_LOG.txt](attachments/CHROME_ASAN_LOG.txt) (text/plain, 19.4 KB)
- [chromium.diff](attachments/chromium.diff) (text/x-diff, 6.7 KB)
- [index.html](attachments/index.html) (text/html, 191 B)
- [genskpic.py](attachments/genskpic.py) (text/x-python, 3.4 KB)

## Timeline

### xi...@chromium.org (2024-08-16)

Thanks for the detailed report. +michaelludwig@ who touched the function recently.

Setting severity to S1 since it is OOB in GPU process that requires compromised renderer. Since the function hasn't been changed recently, setting the Found-in label to the latest extended Stable milestone.

### pe...@google.com (2024-08-17)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-08-17)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-08-19)

Project: skia
Branch: main

commit fdc8c2d593f7dc95b3a98216ec6a4ffa23489516
Author: Michael Ludwig <michaelludwig@google.com>
Date:   Mon Aug 19 10:12:20 2024

    [ganesh] Fix MeshOp index combination logic
    
    Check total index count in onCombineIfPossible.
    
    Bug: b/360265320
    Change-Id: I02f04593b60dcd2470580110d0a555ed4bf47280
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/890322
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/DrawMeshOp.cpp

https://skia-review.googlesource.com/890322


### pe...@google.com (2024-08-20)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127, 128].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.

### mi...@google.com (2024-08-20)

1. <https://skia-review.googlesource.com/890322> needs to be backmerged; it is a CL in the Skia repo which manages its own branches for the chrome releases that it can be cherry picked to.
2. Yes
3. Extremely unlikely
4. No
5. Yes, follow the instructions in [comment #1](https://issues.chromium.org/issues/360265320#comment1) under the (chromium) instruction section:

```
(Chromium)

Apply the chromium.diff renderer patch to chromium.
Run genskpic.py to generate drawable_picture.skp.hh, then move the generated file to src/gpu/command_buffer/client.
Build and start the browser.
Open index.html.
The GPU process will crash.

```

### pe...@google.com (2024-08-21)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M126. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to other stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M127. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M128. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [126, 127, 128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### mi...@google.com (2024-08-22)

Not sure why [comment #8](https://issues.chromium.org/issues/360265320#comment8) posted again, but answers to questions are in [comment #7](https://issues.chromium.org/issues/360265320#comment7), OSes are marked appropriately.

### am...@chromium.org (2024-08-22)

The roll of Skia with the fix landed on 129, so only merge to M128 should be needed here.
Not seeing any issues related to this fix on Canary or Beta, please go ahead and merge this fix to M128, branch 6613 at your earliest convenience / before 10 am Pacific time on Monday, 26 August so this fix can be included in the next M128 Stable update

### ap...@google.com (2024-08-23)

Project: skia
Branch: chrome/m128

commit e0b8a057ab17f2870a8f956252ef385c76c56c28
Author: Michael Ludwig <michaelludwig@google.com>
Date:   Mon Aug 19 10:12:20 2024

    [ganesh] Fix MeshOp index combination logic
    
    Check total index count in onCombineIfPossible.
    
    Bug: b/360265320
    Change-Id: I02f04593b60dcd2470580110d0a555ed4bf47280
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/890322
    Reviewed-by: Brian Osman <brianosman@google.com>
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>
    (cherry picked from commit fdc8c2d593f7dc95b3a98216ec6a4ffa23489516)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/892079
    Commit-Queue: Brian Osman <brianosman@google.com>
    Auto-Submit: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/DrawMeshOp.cpp

https://skia-review.googlesource.com/892079


### go...@google.com (2024-08-23)

Looks like this is merged to M128. 
Please adjust merge labels if nothing else is pending. 


### pe...@google.com (2024-08-23)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### mi...@google.com (2024-08-23)

1. The underlying issue was present before M126
2. No

### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
$15,000 for high quality report of memory corruption in the GPU process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations on another one, Renan! Thank you for your efforts and reporting this issue to us -- great work!

### hy...@gmail.com (2024-08-29)

Hi, thank you all!

I have a question, in the new [bounty table](https://bughunters.google.com/about/rules/chrome-friends/5745167867576320/chrome-vulnerability-reward-program-rules#memory-corruption-vulnerabilities), GPU process is being considered sandbox escape on Android since it cannot be sandboxed there, "Sandbox escape / Memory corruption / RCE in a non-sandboxed process [1], [2]", where "[1]" says "[1] Also includes the GPU process on Android." (where only the report of memory corruption bug alone would be a higher tier, "android" is also being listed in the "OS" label here).

Skia Ganesh is the default Skia backend on Android, is it possible to review the reward again based on that? (I also provided an android GPU process stacktrace for [crbug.com/360758697](https://issues.chromium.org/issues/360758697#comment24)).

Android stacktrace of this bug after attaching lldb to the GPU process on Android using `out/androidx86_64/bin/chrome_public_apk lldb --debug-process-name privileged_process0` (memory corruption has already been proven by the previous ASAN stacktrace, just proving that the bug is also reachable on Android using a release build I have here):

```
* thread #14, name = 'CrGpuMain', stop reason = signal SIGSEGV: address access protected (fault address: 0x7310d04a7000)
  * frame #0: 0x0000731181cfad57 libskia.cr.so`(anonymous namespace)::MeshOp::onPrepareDraws(this=0x00007312cd4a7b10, target=0x000073119c015190) at DrawMeshOp.cpp:1105:36
    frame #1: 0x0000731181d12409 libskia.cr.so`GrOp::prepare(this=0x00007312cd4a7b10, state=0x000073119c015190) at GrOp.h:187:15
    frame #2: 0x0000731181d1225e libskia.cr.so`skgpu::ganesh::OpsTask::onPrepare(this=0x000073133d4b2960, flushState=0x000073119c015190) at OpsTask.cpp:531:27
    frame #3: 0x0000731181c83464 libskia.cr.so`GrRenderTask::prepare(this=0x000073133d4b2960, flushState=0x000073119c015190) at GrRenderTask.cpp:111:11
    frame #4: 0x0000731181c62631 libskia.cr.so`GrDrawingManager::executeRenderTasks(this=0x000073128d486850, flushState=0x000073119c015190) at GrDrawingManager.cpp:260:21
    frame #5: 0x0000731181c61b76 libskia.cr.so`GrDrawingManager::flush(this=0x000073128d486850, proxies=SkSpan @ 0x000073119c015140, access=kNoAccess, info=0x0000731181881b48, newState=0x0000000000000000) at GrDrawingManager.cpp:203:34
    frame #6: 0x0000731181c62f2e libskia.cr.so`GrDrawingManager::flushSurfaces(this=0x000073128d486850, proxies=SkSpan @ 0x000073119c016c48, access=kNoAccess, info=0x0000731181881b48, newState=0x0000000000000000) at GrDrawingManager.cpp:530:27
    frame #7: 0x0000731181c5bd42 libskia.cr.so`GrDirectContextPriv::flushSurfaces(this=0x000073119c016dc0, proxies=SkSpan @ 0x000073119c016cf8, access=kNoAccess, info=0x0000731181881b48, newState=0x0000000000000000) at GrDirectContextPriv.cpp:92:47
    frame #8: 0x0000731181c58e38 libskia.cr.so`GrDirectContextPriv::flushSurface(this=0x000073119c016dc0, proxy=0x00007312dd487510, access=kNoAccess, info=0x0000731181881b48, newState=0x0000000000000000) at GrDirectContextPriv.h:106:22
    frame #9: 0x0000731181c58ecc libskia.cr.so`GrDirectContext::flush(this=0x00007312bd4a9250, surface=0x000073125d488cd0, info=0x0000731181881b48, newState=0x0000000000000000) at GrDirectContext.cpp:516:25
    frame #10: 0x0000731181d2b7d2 libskia.cr.so`skgpu::ganesh::Flush(surface=0x000073125d488cd0) at SkSurface_Ganesh.cpp:782:45
    frame #11: 0x000073116c440442 libgpu_gles2.cr.so`gpu::SharedContextState::FlushWriteAccess(this=<unavailable>, access=0x000073126d47b450) at shared_context_state.cc:798:9
    frame #12: 0x000073116c429529 libgpu_gles2.cr.so`gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM(this=0x00007312fd4837d0) at raster_decoder.cc:3128:30
    frame #13: 0x000073116c428158 libgpu_gles2.cr.so`gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(this=<unavailable>, immediate_data_size=<unavailable>, cmd_data=<unavailable>) at raster_decoder_autogen.h:162:3
    frame #14: 0x000073116c42ab68 libgpu_gles2.cr.so`gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(this=0x00007312fd4837d0, num_commands=<unavailable>, buffer=<unavailable>, num_entries=111, entries_processed=0x000073119c0170d0) at raster_decoder.cc:1510:18
    frame #15: 0x000073116efdfca6 libgpu.cr.so`gpu::CommandBufferService::Flush(this=0x000073127d4b9b80, put_offset=<unavailable>, handler=0x00007312fd4837d0) at command_buffer_service.cc:231:35
    frame #16: 0x000073115271e3c7 libgpu_ipc_service.cr.so`gpu::CommandBufferStub::OnAsyncFlush(this=0x00007312fd495750, put_offset=111, flush_id=4, sync_token_fences=<unavailable>) at command_buffer_stub.cc:503:22
    frame #17: 0x000073115271dfef libgpu_ipc_service.cr.so`gpu::CommandBufferStub::ExecuteDeferredRequest(this=0x00007312fd495750, params=0x000073121d483bf0) at command_buffer_stub.cc:154:7
    frame #18: 0x0000731152728790 libgpu_ipc_service.cr.so`gpu::GpuChannel::ExecuteDeferredRequest(this=0x00007312bd4b4890, params=gpu::mojom::DeferredRequestParamsPtr @ 0x000073119c017578, release_count=1) at gpu_channel.cc:932:13
    frame #19: 0x000073115272c32a libgpu_ipc_service.cr.so`void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(method=<unavailable>, receiver_ptr=<unavailable>, args=0x000073125d4856b0, args=0x000073125d4856b8) at bind_internal.h:738:12
    frame #20: 0x000073116efe743d libgpu.cr.so`base::OnceCallback<void ()>::Run(this=0x000073119c017610) && at callback.h:156:12
    frame #21: 0x000073116efef544 libgpu.cr.so`gpu::SchedulerDfs::ExecuteSequence(this=0x000073125d486ab0, sequence_id=gpu::SequenceId @ 0x000073119c017604) at scheduler_dfs.cc:600:24
    frame #22: 0x000073116efeeaf7 libgpu.cr.so`gpu::SchedulerDfs::RunNextTask(this=0x000073125d486ab0) at scheduler_dfs.cc:524:3
    frame #23: 0x000073118f1457c1 libbase.cr.so`base::OnceCallback<void ()>::Run(this=0x000073135d494358) && at callback.h:156:12
    frame #24: 0x000073118f1d2fce libbase.cr.so`base::TaskAnnotator::RunTaskImpl(this=<unavailable>, pending_task=<unavailable>) at task_annotator.cc:203:34
    frame #25: 0x000073118f1f683a libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) [inlined] void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(this=0x000073130d46b698, event_name=<unavailable>, pending_task=0x000073135d4942e0, args=0x000073119c017bd0) at task_annotator.h:90:5
    frame #26: 0x000073118f1f6811 libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(this=0x000073130d46b3d0, continuation_lazy_now=0x000073119c017c80) at thread_controller_with_message_pump_impl.cc:484:23
    frame #27: 0x000073118f1f62b1 libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork(this=0x000073130d46b3d0) at thread_controller_with_message_pump_impl.cc:346:40
    frame #28: 0x000073118f1f6c22 libbase.cr.so`non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() at thread_controller_with_message_pump_impl.cc:0
    frame #29: 0x000073118f16e559 libbase.cr.so`base::MessagePumpDefault::Run(this=<unavailable>, delegate=0x000073130d46b3d0) at message_pump_default.cc:40:55
    frame #30: 0x000073118f1f6f23 libbase.cr.so`base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(this=0x000073130d46b3d0, application_tasks_allowed=true, timeout=<unavailable>) at thread_controller_with_message_pump_impl.cc:654:12
    frame #31: 0x000073118f1a9beb libbase.cr.so`base::RunLoop::Run(this=0x000073119c017f18, location=<unavailable>) at run_loop.cc:134:14
    frame #32: 0x00007310e70663c7 libcontent.cr.so`content::GpuMain(parameters=<unavailable>) at gpu_main.cc:431:14
    frame #33: 0x00007310e8baa4d7 libcontent.cr.so`content::RunOtherNamedProcessTypeMain(process_type="gpu-process", main_function_params=<unavailable>, delegate=<unavailable>) at content_main_runner_impl.cc:798:14
    frame #34: 0x00007310e8bab0da libcontent.cr.so`content::ContentMainRunnerImpl::Run(this=0x000073126d472620) at content_main_runner_impl.cc:1175:10
    frame #35: 0x00007310e8ba8cb0 libcontent.cr.so`content::RunContentProcess(params=ContentMainParams @ 0x000073119c018520, content_main_runner=0x000073126d472620) at content_main.cc:333:36
    frame #36: 0x00007310e8ba9b67 libcontent.cr.so`::Java_org_jni_1zero_GEN_1JNI_org_1chromium_1content_1app_1ContentMain_1start(JNIEnv *, jclass, jboolean) [inlined] content::JNI_ContentMain_Start(env=<unavailable>, start_minimal_browser='\0') at content_main_android.cc:65:10
    frame #37: 0x00007310e8ba9ae3 libcontent.cr.so`Java_org_jni_1zero_GEN_1JNI_org_1chromium_1content_1app_1ContentMain_1start(env=<unavailable>, jcaller=<unavailable>, startMinimalBrowser='\0') at ContentMain_jni.h:36:15
    frame #38: 0x000073120937d70c libart.so`art_quick_generic_jni_trampoline + 220
    frame #39: 0x0000731209368c96 libart.so`NterpCommonInvokeStatic + 131

```

### am...@chromium.org (2024-08-29)

re c#17; Since this was reported and not demonstrated before the new reward structure was announced, we'll need to take this under specific consideration to determine if a reward adjustment is appropriate here.

We do, however, greatly appreciate you going ahead and providing the requisite information up front, in tandem to your reassessment request. In the future, impact in a given process and platform will be expected to be demonstrated in the original report, not after reward decision.

We'll take a look at a future panel session, and will update here with a decision after that discussion has occurred.

### pe...@google.com (2024-09-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### pe...@google.com (2024-09-04)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-04)

1. <http://review.skia.org/894465> for 120, <http://review.skia.org/894464> for 126.
   Note: CQ isn't running for 120, doing the request based on the 126 CQ results, since no modifications were needed for the backmerged CLs in both branches.
2. Low, no conflicts
3. 128
4. Yes

### gm...@google.com (2024-09-04)

@rzanoni, let's hold off on 120 for now.

### am...@chromium.org (2024-09-04)

Following up on c#17 and c#18, while we appreciate you attempting to demonstrate this issue on Android, your stacktrace that you have provided only demonstrates a segfault. While this issue in Ganesh, and transitively Android is impacted, to be eligible for the memory corruption in a non-sandboxed process level rewards you would need to fully demonstrate that exploitable memory corruption on Android in the same manner as other platforms.
This will be expected to be included *as part of the original report* in future reports.

### hy...@gmail.com (2024-09-07)

Hi, thanks for reviewing it and answering my questions in [c#17](https://issues.chromium.org/issues/360265320#comment17).

Let me also clarify the situation here, the Android stacktrace ends up with:

```
* thread #14, name = 'CrGpuMain', stop reason = signal SIGSEGV: address access protected (fault address: 0x7310d04a7000)
  * frame #0: 0x0000731181cfad57 libskia.cr.so`(anonymous namespace)::MeshOp::onPrepareDraws(this=0x00007312cd4a7b10, target=0x000073119c015190) at DrawMeshOp.cpp:1105:36

void MeshOp::onPrepareDraws(GrMeshDrawTarget* target) {
    ...
    std::tie(indexBuffer, firstIndex) = fMeshes[0].gpuIB();
    if (fIndexCount && !indexBuffer) {
        uint16_t* indices = nullptr;
        indices = target->makeIndexSpace(fIndexCount, &indexBuffer, &firstIndex); // <-- [2]
        if (!indices) {
            SkDebugf("Could not allocate indices.\n");
            return;
        }
        // We can just copy the first mesh's indices. Subsequent meshes need their indices adjusted.
        std::copy_n(fMeshes[0].indices(), fMeshes[0].indexCount(), indices); // <-- [3]
        int voffset = fMeshes[0].vertexCount();
        int ioffset = fMeshes[0].indexCount();
        for (int m = 1; m < fMeshes.size(); ++m) {
            for (int i = 0; i < fMeshes[m].indexCount(); ++i) {
                indices[ioffset++] = fMeshes[m].indices()[i] + voffset; // <-- [4]
            }
            voffset += fMeshes[m].vertexCount();
        }
        ...
}

```

This is a write into memory that is not currently mapped, `MeshOp::onCombineIfPossible` will sum all index counts of all meshes referenced from each `DRAW_VERTICES_OBJECT` drawing operation into `fIndexCount` [1] and will later, in `MeshOp::onPrepareDraws`, pre-allocate a buffer (stored as C pointer, `indices`, see [2]) using the overflowed `fIndexCount` and write them all at once to the allocated buffer [3] [4] which eventually ends up writing to unmapped memory in [4] as more index data is copied, this was already explained previously in the bug writeup, furthermore, PartitionAlloc is predictable, and since an attacker has control of how many indices each mesh has, it's possible to manipulate the final `fIndexCount` (and consequently, the allocation size), to make the allocation fall into a predictable memory layout, which also makes doable to manipulate the write to end up in controlled memory.

We have a wild copy happening here, `MeshOp::onPrepareDraws` will copy indices of all meshes we previously combined to the final allocation (where size is attacker controlled), however, again, wild copy (and similar scenarios) exploitation isn't unrealistic as it has been done a few times, [5][6][7], taking in consideration the multi-thread nature of modern browsers (we have IO/UI/Thread pool etc.), there are potentially multiple ways to exploit it. Interestingly, the previous ITW CVE-2023-6345 reported by Google TAG in `MeshOp::onCombineIfPossible` [8], by combining vertices instead of indices, shares very similar characteristics to this one and it was used in the wild last year against chrome users.

Let me know why this doesn't meet the bar, always happy to follow-up with any extra information if needed!

Thanks.

Reference:

[1] <https://source.chromium.org/chromium/_/skia/skia/+/297b50d8609775bf7e33ae4be6a74697ce9f3546:src/gpu/ganesh/ops/DrawMeshOp.cpp;l=1283;bpv=1>

[2] [3] [4] <https://source.chromium.org/chromium/_/skia/skia/+/297b50d8609775bf7e33ae4be6a74697ce9f3546:src/gpu/ganesh/ops/DrawMeshOp.cpp;l=1151;bpv=1>

[5] <https://googleprojectzero.blogspot.com/2015/03/taming-wild-copy-parallel-thread.html>

[6] <https://blog.ret2.io/2022/05/19/pwn2own-2021-parallels-desktop-exploit/>

[7] <https://saaramar.github.io/IOMFB_integer_overflow_poc/#wildcopy-exploitation>

[8] <https://googleprojectzero.github.io/0days-in-the-wild//0day-RCAs/2023/CVE-2023-6345.html>

### hy...@gmail.com (2024-09-11)

Following [c#24](https://issues.chromium.org/issues/360265320#comment24), I initially submitted a release stacktrace because 'x86\_64' ASAN builds are broken on Android due to 'libclang\_rt.asan-x86\_64-android.so' not being present in 'third\_party/llvm-build/Release+Asserts', however, I got access to an ARM64 Android device today, so here is a GPU process ASAN stacktrace from logcat on ARM Android:

```
09-11 00:47:24.601 13469 13469 I wrap.sh : =================================================================
09-11 00:47:24.601 13469 13469 I wrap.sh : ==13470==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x00702510c820 at pc 0x00716f6638b4 bp 0x00707c306560 sp 0x00707c305d50
09-11 00:47:24.601 13469 13469 I wrap.sh : WRITE of size 6000000 at 0x00702510c820 thread T16 (CrGpuMain)
I 00:47:24.611  273.680s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpbit4673t --quiet /tmp/tmpvwl_7xhl
09-11 00:47:24.710 13469 13469 I wrap.sh : 
09-11 00:47:24.711 13469 13469 I wrap.sh : Stack Trace:
09-11 00:47:24.711 13469 13469 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-11 00:47:24.711 13469 13469 I wrap.sh :   v------>  unsigned short* std::__Cr::__constexpr_memmove<unsigned short, unsigned short const, 0>(unsigned short*, unsigned short const*, std::__Cr::__element_count)  ../../third_party/libc++/src/include/__string/constexpr_c_functions.h:227:5
09-11 00:47:24.711 13469 13469 I wrap.sh :   v------>  std::__Cr::pair<unsigned short const*, unsigned short*> std::__Cr::__copy_trivial_impl<unsigned short const, unsigned short>(unsigned short const*, unsigned short const*, unsigned short*)  ../../third_party/libc++/src/include/__algorithm/copy_move_common.h:65:3
09-11 00:47:24.711 13469 13469 I wrap.sh :   v------>  std::__Cr::pair<unsigned short const*, unsigned short*> std::__Cr::__copy_impl<std::__Cr::_ClassicAlgPolicy>::operator()<unsigned short const, unsigned short, 0>(unsigned short const*, unsigned short const*, unsigned short*) const  ../../third_party/libc++/src/include/__algorithm/copy.h:102:12
09-11 00:47:24.711 13469 13469 I wrap.sh :   v------>  std::__Cr::pair<unsigned short const*, unsigned short*> std::__Cr::__copy_move_unwrap_iters<std::__Cr::__copy_impl<std::__Cr::_ClassicAlgPolicy>, unsigned short const*, unsigned short const*, unsigned short*, 0>(unsigned short const*, unsigned short const*, unsigned short*)  ../../third_party/libc++/src/include/__algorithm/copy_move_common.h:95:19
09-11 00:47:24.711 13469 13469 I wrap.sh :   v------>  std::__Cr::pair<unsigned short const*, unsigned short*> std::__Cr::__copy<std::__Cr::_ClassicAlgPolicy, unsigned short const*, unsigned short const*, unsigned short*>(unsigned short const*, unsigned short const*, unsigned short*)  ../../third_party/libc++/src/include/__algorithm/copy.h:109:10
09-11 00:47:24.711 13469 13469 I wrap.sh :   v------>  unsigned short* std::__Cr::copy<unsigned short const*, unsigned short*>(unsigned short const*, unsigned short const*, unsigned short*)  ../../third_party/libc++/src/include/__algorithm/copy.h:116:10
09-11 00:47:24.712 13469 13469 I wrap.sh :   v------>  unsigned short* std::__Cr::copy_n<unsigned short const*, int, unsigned short*, 0>(unsigned short const*, int, unsigned short*)  ../../third_party/libc++/src/include/__algorithm/copy_n.h:55:10
09-11 00:47:24.712 13469 13469 I wrap.sh :   24b7d1c8  (anonymous namespace)::MeshOp::onPrepareDraws(GrMeshDrawTarget*)                  ../../third_party/skia/src/gpu/ganesh/ops/DrawMeshOp.cpp:1100:9
09-11 00:47:24.712 13469 13469 I wrap.sh :   24bcba98  GrOp::prepare(GrOpFlushState*)                                                    ../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:187:15
09-11 00:47:24.712 13469 13469 I wrap.sh :   24bcafe0  skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*)                                ../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:531:27
09-11 00:47:24.712 13469 13469 I wrap.sh :   249f40c8  GrRenderTask::prepare(GrOpFlushState*)                                            ../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
09-11 00:47:24.712 13469 13469 I wrap.sh :   2499ac58  GrDrawingManager::executeRenderTasks(GrOpFlushState*)                             ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
09-11 00:47:24.712 13469 13469 I wrap.sh :   24998d98  GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
09-11 00:47:24.712 13469 13469 I wrap.sh :   2499c8e4  GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
09-11 00:47:24.713 13469 13469 I wrap.sh :   2498afb0  GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
09-11 00:47:24.713 13469 13469 I wrap.sh :   v------>  GrDirectContextPriv::flushSurface(GrSurfaceProxy*, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
09-11 00:47:24.713 13469 13469 I wrap.sh :   24983fc0  GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
09-11 00:47:24.713 13469 13469 I wrap.sh :   24c22444  skgpu::ganesh::Flush(SkSurface*)                                                  ../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
09-11 00:47:24.713 13469 13469 I wrap.sh :   2a1cfaac  gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*)  ../../gpu/command_buffer/service/shared_context_state.cc:798:9
09-11 00:47:24.713 13469 13469 I wrap.sh :   2a184c54  gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM()                             ../../gpu/command_buffer/service/raster_decoder.cc:3128:30
09-11 00:47:24.714 13469 13469 I wrap.sh :   2a17f3c8  gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/raster_decoder_autogen.h:162:3
09-11 00:47:24.714 13469 13469 I wrap.sh :   2a18e488  gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/raster_decoder.cc:1510:18
09-11 00:47:24.714 13469 13469 I wrap.sh :   2829ff1c  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:231:35
09-11 00:47:24.714 13469 13469 I wrap.sh :   2a4673e0  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:503:22
09-11 00:47:24.714 13469 13469 I wrap.sh :   2a4662a4  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)  ../../gpu/ipc/service/command_buffer_stub.cc:154:7
09-11 00:47:24.714 13469 13469 I wrap.sh :   2a47ecac  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long)  ../../gpu/ipc/service/gpu_channel.cc:932:13
09-11 00:47:24.714 13469 13469 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   2a48bf84  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&)  ../../base/functional/bind_internal.h:954:5
09-11 00:47:24.715 13469 13469 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0ul, 1ul, 2ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:47:24.715 13469 13469 I wrap.sh :   2a48bd68  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   282cf2b8  gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler_dfs.cc:600:24
09-11 00:47:24.715 13469 13469 I wrap.sh :   282cd2ac  gpu::SchedulerDfs::RunNextTask()                                                  ../../gpu/command_buffer/service/scheduler_dfs.cc:524:3
09-11 00:47:24.715 13469 13469 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>::Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>(void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, void, 0ul>::MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:930:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:47:24.715 13469 13469 I wrap.sh :   282d0ad4  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   22f457cc  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:203:34
09-11 00:47:24.715 13469 13469 I wrap.sh :   v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:90:5
09-11 00:47:24.715 13469 13469 I wrap.sh :   22fc3acc  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:484:23
09-11 00:47:24.715 13469 13469 I wrap.sh :   22fc28bc  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
09-11 00:47:24.715 13469 13469 I wrap.sh :   22e49990  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:40:55
09-11 00:47:24.715 13469 13469 I wrap.sh :   22fc5930  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:654:12
09-11 00:47:24.715 13469 13469 I wrap.sh :   22ee07ec  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:134:14
09-11 00:47:24.715 13469 13469 I wrap.sh :   35071528  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:431:14
09-11 00:47:24.715 13469 13469 I wrap.sh :   22006d70  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:798:14
09-11 00:47:24.715 13469 13469 I wrap.sh :   22008be0  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1175:10
09-11 00:47:24.715 13469 13469 I wrap.sh :   22003080  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:333:36
09-11 00:47:24.715 13469 13469 I wrap.sh :   v------>  content::JNI_ContentMain_Start(_JNIEnv*, unsigned char)                           ../../content/app/android/content_main_android.cc:65:10
09-11 00:47:24.715 13469 13469 I wrap.sh :   22005798  Java_org_1chromium_1content_1app_1ContentMain_1start                              gen/jni_headers/content/public/android/content_app_jni/ContentMain_jni.h:36:15
09-11 00:47:24.716 13469 13469 I wrap.sh : : 
09-11 00:47:24.716 13469 13469 I wrap.sh : 0x00702510c820 is located 0 bytes after 2097184-byte region [0x007024f0c800,0x00702510c820)
09-11 00:47:24.716 13469 13469 I wrap.sh : allocated by thread T16 (CrGpuMain) here:
I 00:47:27.554  276.623s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpbit4673t --quiet /tmp/tmpgvqo8kaa
09-11 00:47:24.716 13469 13469 I wrap.sh : 
09-11 00:47:24.716 13469 13469 I wrap.sh : Stack Trace:
09-11 00:47:24.716 13469 13469 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-11 00:47:24.716 13469 13469 I wrap.sh :   v------>  GrCpuBuffer::Make(unsigned long)                                                  ../../third_party/skia/src/gpu/ganesh/GrCpuBuffer.h:29:20
09-11 00:47:24.717 13469 13469 I wrap.sh :   24963018  GrBufferAllocPool::CpuBufferCache::makeBuffer(unsigned long, bool)                ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:56:30
09-11 00:47:24.717 13469 13469 I wrap.sh :   24964b24  GrBufferAllocPool::resetCpuData(unsigned long)                                    ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:389:60
09-11 00:47:24.717 13469 13469 I wrap.sh :   24966558  GrBufferAllocPool::createBlock(unsigned long)                                     ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:362:15
09-11 00:47:24.717 13469 13469 I wrap.sh :   24965a38  GrBufferAllocPool::makeSpace(unsigned long, unsigned long, sk_sp<GrBuffer const>*, unsigned long*)  ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:229:16
09-11 00:47:24.717 13469 13469 I wrap.sh :   249681ac  GrIndexBufferAllocPool::makeSpace(int, sk_sp<GrBuffer const>*, int*)              ../../third_party/skia/src/gpu/ganesh/GrBufferAllocPool.cpp:496:28
09-11 00:47:24.717 13469 13469 I wrap.sh :   24b7cc60  (anonymous namespace)::MeshOp::onPrepareDraws(GrMeshDrawTarget*)                  ../../third_party/skia/src/gpu/ganesh/ops/DrawMeshOp.cpp:1094:27
09-11 00:47:24.718 13469 13469 I wrap.sh :   24bcba98  GrOp::prepare(GrOpFlushState*)                                                    ../../third_party/skia/src/gpu/ganesh/ops/GrOp.h:187:15
09-11 00:47:24.718 13469 13469 I wrap.sh :   24bcafe0  skgpu::ganesh::OpsTask::onPrepare(GrOpFlushState*)                                ../../third_party/skia/src/gpu/ganesh/ops/OpsTask.cpp:531:27
09-11 00:47:24.718 13469 13469 I wrap.sh :   249f40c8  GrRenderTask::prepare(GrOpFlushState*)                                            ../../third_party/skia/src/gpu/ganesh/GrRenderTask.cpp:111:11
09-11 00:47:24.718 13469 13469 I wrap.sh :   2499ac58  GrDrawingManager::executeRenderTasks(GrOpFlushState*)                             ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:260:21
09-11 00:47:24.718 13469 13469 I wrap.sh :   24998d98  GrDrawingManager::flush(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:203:34
09-11 00:47:24.718 13469 13469 I wrap.sh :   2499c8e4  GrDrawingManager::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDrawingManager.cpp:530:27
09-11 00:47:24.718 13469 13469 I wrap.sh :   2498afb0  GrDirectContextPriv::flushSurfaces(SkSpan<GrSurfaceProxy*>, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.cpp:92:47
09-11 00:47:24.719 13469 13469 I wrap.sh :   v------>  GrDirectContextPriv::flushSurface(GrSurfaceProxy*, SkSurfaces::BackendSurfaceAccess, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContextPriv.h:106:22
09-11 00:47:24.719 13469 13469 I wrap.sh :   24983fc0  GrDirectContext::flush(SkSurface*, GrFlushInfo const&, skgpu::MutableTextureState const*)  ../../third_party/skia/src/gpu/ganesh/GrDirectContext.cpp:516:25
09-11 00:47:24.719 13469 13469 I wrap.sh :   24c22444  skgpu::ganesh::Flush(SkSurface*)                                                  ../../third_party/skia/src/gpu/ganesh/surface/SkSurface_Ganesh.cpp:782:45
09-11 00:47:24.719 13469 13469 I wrap.sh :   2a1cfaac  gpu::SharedContextState::FlushWriteAccess(gpu::SkiaImageRepresentation::ScopedWriteAccess*)  ../../gpu/command_buffer/service/shared_context_state.cc:798:9
09-11 00:47:24.719 13469 13469 I wrap.sh :   2a184c54  gpu::raster::RasterDecoderImpl::DoEndRasterCHROMIUM()                             ../../gpu/command_buffer/service/raster_decoder.cc:3128:30
09-11 00:47:24.719 13469 13469 I wrap.sh :   2a17f3c8  gpu::raster::RasterDecoderImpl::HandleEndRasterCHROMIUM(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/raster_decoder_autogen.h:162:3
09-11 00:47:24.719 13469 13469 I wrap.sh :   2a18e488  gpu::error::Error gpu::raster::RasterDecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/raster_decoder.cc:1510:18
09-11 00:47:24.720 13469 13469 I wrap.sh :   2829ff1c  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:231:35
09-11 00:47:24.720 13469 13469 I wrap.sh :   2a4673e0  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:503:22
09-11 00:47:24.720 13469 13469 I wrap.sh :   2a4662a4  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&)  ../../gpu/ipc/service/command_buffer_stub.cc:154:7
09-11 00:47:24.720 13469 13469 I wrap.sh :   2a47ecac  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long)  ../../gpu/ipc/service/gpu_channel.cc:932:13
09-11 00:47:24.720 13469 13469 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:47:24.720 13469 13469 I wrap.sh :   2a48bf84  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, void, 0ul, 1ul, 2ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&)  ../../base/functional/bind_internal.h:954:5
09-11 00:47:24.720 13469 13469 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, 0ul, 1ul, 2ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul, 2ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:47:24.720 13469 13469 I wrap.sh :   2a48bd68  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, unsigned long&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, unsigned long>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:47:24.720 13469 13469 I wrap.sh :   138d1804  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:156:12
09-11 00:47:24.720 13469 13469 I wrap.sh :   282cf2b8  gpu::SchedulerDfs::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler_dfs.cc:600:24
09-11 00:47:24.720 13469 13469 I wrap.sh :   282cd2ac  gpu::SchedulerDfs::RunNextTask()                                                  ../../gpu/command_buffer/service/scheduler_dfs.cc:524:3
09-11 00:47:24.720 13469 13469 I wrap.sh :   v------>  void base::internal::DecayedFunctorTraits<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>::Invoke<void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*>(void (gpu::SchedulerDfs::*)(), gpu::SchedulerDfs*&&)  ../../base/functional/bind_internal.h:738:12
09-11 00:47:24.720 13469 13469 I wrap.sh :   v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, void, 0ul>::MakeItSo<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:930:12
09-11 00:47:24.720 13469 13469 I wrap.sh :   v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<void (gpu::SchedulerDfs::*)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(void (gpu::SchedulerDfs::*&&)(), std::__Cr::tuple<base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1067:14
09-11 00:47:24.720 13469 13469 I wrap.sh :   282d0ad4  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::SchedulerDfs::*&&)(), gpu::SchedulerDfs*>, base::internal::BindState<true, true, false, void (gpu::SchedulerDfs::*)(), base::internal::UnretainedWrapper<gpu::SchedulerDfs, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:980:12
09-11 00:47:24.720 13469 13469 I wrap.sh : : 
09-11 00:47:24.720 13469 13469 I wrap.sh : Thread T16 (CrGpuMain) created by T0 (ileged_process3) here:
I 00:47:30.459  279.528s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpbit4673t --quiet /tmp/tmp47bc51fp
09-11 00:47:24.749 13469 13469 I wrap.sh : : 
09-11 00:47:24.749 13469 13469 I wrap.sh : SUMMARY: AddressSanitizer: heap-buffer-overflow (/data/app/~~KPyAmZWcrOc5MMNAXCzsqg==/org.chromium.chrome-S467huOY7bZcvacNu-lOrA==/lib/arm64/libchrome.so+0x24b7d1c8) (BuildId: 6ea1b6ebac3bf624) 
09-11 00:47:24.751 13469 13469 I wrap.sh : Shadow bytes around the buggy address:
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c780: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
09-11 00:47:24.751 13469 13469 I wrap.sh : =>0x00702510c800: 00 00 00 00[fa]fa fa fa fa fa fa fa fa fa fa fa
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c900: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510c980: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510ca00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:47:24.751 13469 13469 I wrap.sh :   0x00702510ca80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
09-11 00:47:24.751 13469 13469 I wrap.sh : Shadow byte legend (one shadow byte represents 8 application bytes):
09-11 00:47:24.751 13469 13469 I wrap.sh :   Addressable:           00
09-11 00:47:24.751 13469 13469 I wrap.sh :   Partially addressable: 01 02 03 04 05 06 07 
09-11 00:47:24.751 13469 13469 I wrap.sh :   Heap left redzone:       fa
09-11 00:47:24.751 13469 13469 I wrap.sh :   Freed heap region:       fd
09-11 00:47:24.751 13469 13469 I wrap.sh :   Stack left redzone:      f1
09-11 00:47:24.751 13469 13469 I wrap.sh :   Stack mid redzone:       f2
09-11 00:47:24.751 13469 13469 I wrap.sh :   Stack right redzone:     f3
09-11 00:47:24.751 13469 13469 I wrap.sh :   Stack after return:      f5
09-11 00:47:24.751 13469 13469 I wrap.sh :   Stack use after scope:   f8
09-11 00:47:24.751 13469 13469 I wrap.sh :   Global redzone:          f9
09-11 00:47:24.751 13469 13469 I wrap.sh :   Global init order:       f6
09-11 00:47:24.751 13469 13469 I wrap.sh :   Poisoned by user:        f7
09-11 00:47:24.751 13469 13469 I wrap.sh :   Container overflow:      fc
09-11 00:47:24.751 13469 13469 I wrap.sh :   Array cookie:            ac
09-11 00:47:24.751 13469 13469 I wrap.sh :   Intra object redzone:    bb
09-11 00:47:24.751 13469 13469 I wrap.sh :   ASan internal:           fe
09-11 00:47:24.751 13469 13469 I wrap.sh :   Left alloca redzone:     ca
09-11 00:47:24.751 13469 13469 I wrap.sh :   Right alloca redzone:    cb
09-11 00:47:24.752 13469 13469 I wrap.sh : : 
09-11 00:47:24.752 13469 13469 I wrap.sh : ==13470==ADDITIONAL INFO
09-11 00:47:24.752 13469 13469 I wrap.sh : : 
09-11 00:47:24.752 13469 13469 I wrap.sh : ==13470==Note: Please include this section with the ASan report.
09-11 00:47:24.752 13469 13469 I wrap.sh : Task trace:
I 00:47:30.511  279.580s Main  Running: /home/hyhy100/chromium/src/third_party/android_platform/development/scripts/stack.py --output-directory /home/hyhy100/chromium/src/out/android-arm64-static --apks-directory /tmp/tmpbit4673t --quiet /tmp/tmpt4n08d7a
09-11 00:47:24.752 13469 13469 I wrap.sh : 
09-11 00:47:24.752 13469 13469 I wrap.sh : Stack Trace:
09-11 00:47:24.752 13469 13469 I wrap.sh :   RELADDR   FUNCTION                                                                          FILE:LINE
09-11 00:47:24.752 13469 13469 I wrap.sh :   282cd620  gpu::SchedulerDfs::RunNextTask()                                                  ../../gpu/command_buffer/service/scheduler_dfs.cc:540:27
09-11 00:47:24.752 13469 13469 I wrap.sh :   282c8268  gpu::SchedulerDfs::TryScheduleSequence(gpu::SchedulerDfs::Sequence*)              ../../gpu/command_buffer/service/scheduler_dfs.cc:342:11
09-11 00:47:24.752 13469 13469 I wrap.sh :   23a43134  mojo::SimpleWatcher::Context::Notify(unsigned int, MojoHandleSignalsState, unsigned int)  ../../mojo/public/cpp/system/simple_watcher.cc:102:13
09-11 00:47:24.752 13469 13469 I wrap.sh : : 
09-11 00:47:24.752 13469 13469 I wrap.sh : : 
09-11 00:47:24.752 13469 13469 I wrap.sh : Command line: ` --type=gpu-process --enable-crash-reporter=,unknown --no-subproc-heap-profiling --gpu-preferences=UAAAAAAAAAAgAIAMAAAAAAAAAAAAAAAAAABgAAIAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAAAAAAAAAAEAAAAAAAAAAIAAAAAAAAAAgAAAAAAAAA --shared-files --metrics-shmem-handle=5,i,12911573890589611707,13663576127610292598,262144 --field-trial-handle=3,i,3921320852403805935,13091221255287897095,262144 --variations-seed-version --host-package-name=org.chromium.chrome --package-name=org.chromium.chrome --host-package-label=Chromium --host-version-code=661700004 --package-version-name=129.0.6617.0 --mojo-platform-channel-handle=binder:0 --enable-dom-distiller`
09-11 00:47:24.752 13469 13469 I wrap.sh : : 
09-11 00:47:24.752 13469 13469 I wrap.sh : : 
09-11 00:47:24.752 13469 13469 I wrap.sh : ==13470==END OF ADDITIONAL INFO
09-11 00:47:24.752 13469 13469 I wrap.sh : ==13470==ABORTING

```

### ap...@google.com (2024-09-11)

Project: skia
Branch: chrome/m126

commit 8618b9f741cef97ba244b4ec1a5e1a8aec97895b
Author: Michael Ludwig <michaelludwig@google.com>
Date:   Mon Aug 19 10:12:20 2024

    [M126-LTS][ganesh] Fix MeshOp index combination logic
    
    Check total index count in onCombineIfPossible.
    
    Bug: b/360265320
    Change-Id: I02f04593b60dcd2470580110d0a555ed4bf47280
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/890322
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>
    (cherry picked from commit fdc8c2d593f7dc95b3a98216ec6a4ffa23489516)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/894464
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>

M       src/gpu/ganesh/ops/DrawMeshOp.cpp

https://skia-review.googlesource.com/894464


### sp...@google.com (2024-09-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
Additional $10,000 reward based on a baseline demonstration of memory corruption in the Android GPU, following the initial $15,000 reward for high-quality report of GPU memory corruption 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-11)

Thank you for the follow-up and additional information. We've reassessed this issue based on the new information and demonstration of this issue on Android with specific stack trace to extend an additional $10,000 reward for baseline demonstration of memory corruption in the Android GPU, following up from the original reward for high-quality report of GPU memory corruption.

### ap...@google.com (2024-09-16)

Project: skia
Branch: chrome/m120

commit dd3abf64d02f683d30e78b5235e5c3e60e100135
Author: Michael Ludwig <michaelludwig@google.com>
Date:   Mon Aug 19 10:12:20 2024

    [M120-LTS][ganesh] Fix MeshOp index combination logic
    
    Check total index count in onCombineIfPossible.
    
    Bug: b/360265320
    Change-Id: I02f04593b60dcd2470580110d0a555ed4bf47280
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/890322
    Commit-Queue: Michael Ludwig <michaelludwig@google.com>
    (cherry picked from commit fdc8c2d593f7dc95b3a98216ec6a4ffa23489516)
    Reviewed-on: https://skia-review.googlesource.com/c/skia/+/894465
    Reviewed-by: Michael Ludwig <michaelludwig@google.com>

M       src/gpu/ganesh/ops/DrawMeshOp.cpp

https://skia-review.googlesource.com/894465


### pe...@google.com (2024-11-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/360265320)*
