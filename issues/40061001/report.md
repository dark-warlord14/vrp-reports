# Security: heap-use-after-free in GrClientMappedBufferManager::owningDirectContext

| Field | Value |
|-------|-------|
| **Issue ID** | [40061001](https://issues.chromium.org/issues/40061001) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Internals>GPU, Internals>Skia |
| **Platforms** | Linux, Mac, Windows |
| **CVE IDs** | CVE-2022-3445 |
| **Reporter** | et...@gmail.com |
| **Assignee** | eg...@google.com |
| **Created** | 2022-09-16 |
| **Bounty** | $15,000.00 |

## Description

**REPRODUCTION CASE**  

The problem was found by my fuzzer, you can download asan linux chromium from here and run poc.html:  

<https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1040186.zip?generation=1661691896532624&alt=media>

But it cannot be reproduced stably, after manual analysis, the root cause of the vulnerability is clearly understood.

**VULNERABILITY DETAILS**

## Root Cause

I analyzed the cause of this vulnerability, which I think is this:  

The key to this problem is the callback triggered when the GPU is in the VK\_ERROR\_DEVICE\_LOST state.

1. The asyncReadPixels function will take out the GrClientMappedBufferManager pointer[0] saved in the GrDirectContext\* dContext, and use this pointer to create a finishContext and a finishCallback, and encapsulate them into a GrFlushInfo[1] for subsequent use, which will be saved at the end into SkTArray.  
   
   So when finishCallback is executed, it will use finishContext as parameter, \*\*finishContext has a reference to GrClientMappedBufferManager in GrDirectContext\*\*

```
void SurfaceContext::asyncReadPixels(GrDirectContext\* dContext,  
                                     const SkIRect& rect,  
                                     SkColorType colorType,  
                                     ReadPixelsCallback callback,  
                                     ReadPixelsContext callbackContext) {  
    auto mappedBufferManager = dContext->priv().clientMappedBufferManager(); //---->[0]  
    ...  
    struct FinishContext {  
        ReadPixelsCallback\* fClientCallback;  
        ReadPixelsContext fClientContext;  
        SkISize fSize;  
        SkColorType fColorType;  
        size_t fBufferAlignment;  
        GrClientMappedBufferManager\* fMappedBufferManager;  
        PixelTransferResult fTransferResult;  
    };  
    // Assumption is that the caller would like to flush. We could take a parameter or require an  
    // explicit flush from the caller. We'd have to have a way to defer attaching the finish  
    // callback to GrGpu until after the next flush that flushes our op list, though.  
    auto\* finishContext = new FinishContext{callback,  
                                            callbackContext,  
                                            rect.size(),  
                                            colorType,  
                                            this->caps()->transferBufferRowBytesAlignment(),  
                                            mappedBufferManager, //----->[1]  
                                            std::move(transferResult)};  
    auto finishCallback = [](GrGpuFinishedContext c) {  
        const auto\* context = reinterpret_cast<const FinishContext\*>(c);  
        auto manager = context->fMappedBufferManager;  
        auto result = std::make_unique<AsyncReadResult>(manager->owningDirectContext());  
        size_t rowBytes =  
                SkAlignTo(context->fSize.width() \* SkColorTypeBytesPerPixel(context->fColorType),  
                          context->fBufferAlignment);  
        if (!result->addTransferResult(context->fTransferResult, context->fSize, rowBytes,  
                                       manager)) {  
            result.reset();  
        }  
        (\*context->fClientCallback)(context->fClientContext, std::move(result));  
        delete context;  
    };  
    GrFlushInfo flushInfo;  
    flushInfo.fFinishedContext = finishContext;//---->[1]  
    flushInfo.fFinishedProc = finishCallback; //----->[1]  
  
    dContext->priv().flushSurface(this->asSurfaceProxy(),  
                                  SkSurface::BackendSurfaceAccess::kNoAccess,  
                                  flushInfo);  
}  

```

2. SkiaOutputSurfaceImpl::FlushGpuTasks->viz::SkiaOutputSurfaceImplOnGpu::SwapBuffers->...GrVkGpu::submitCommandBuffer->GrVkResourceProvider::checkCommandBuffers[2] to enter the GrDirectContext's free process, if we are in GPU hung VK\_ERROR\_DEVICE\_LOST state, here will abandon the vk context and unref all the fActiveCommandPools and reset the array. (refer to comments and source code)

```
void GrVkResourceProvider::checkCommandBuffers() {  
    // When resetting a command buffer it can trigger client provided procs (e.g. release or  
    // finished) to be called. During these calls the client could trigger us to abandon the vk  
    // context, e.g. if we are in a DEVICE_LOST state. When we abandon the vk context we will  
    // unref all the fActiveCommandPools and reset the array. Since this can happen in the middle  
    // of the loop here, we need to additionally check that fActiveCommandPools still has pools on  
    // each iteration.  
    //  
    // TODO: We really need to have a more robust way to protect us from client proc calls that  
    // happen in the middle of us doing work. This may be just one of many potential pitfalls that  
    // could happen from the client triggering GrDirectContext changes during a proc call.  
    for (int i = fActiveCommandPools.count() - 1; fActiveCommandPools.count() && i >= 0; --i) {  
        GrVkCommandPool\* pool = fActiveCommandPools[i];  
        if (!pool->isOpen()) {  
            GrVkPrimaryCommandBuffer\* buffer = pool->getPrimaryCommandBuffer();  
            if (buffer->finished(fGpu)) {  
                fActiveCommandPools.removeShuffle(i);  
                SkASSERT(pool->unique());  
                pool->reset(fGpu); //--------->[2]  
                // After resetting the pool (specifically releasing the pool's resources) we may  
                // have called a client callback proc which may have disconnected the GrVkGpu. In  
                // that case we do not want to push the pool back onto the cache, but instead just  
                // drop the pool.  
                if (fGpu->disconnected()) {  
                    pool->unref();  
                    return;  
                }  
                fAvailableCommandPools.push_back(pool);  
            }  
        }  
    }  
}  

```

3. When reset SkTArray, it will pop out all elements[3] in turn, and execute the fReleaseProc callback [4] in its saved RefCntedCallback in sequence, here it will execute CleanupAfterSkiaFlush and the closure callback finishCallback in sequence.

```
void reset() {  
    this->pop_back_n(fCount);  
    fReserved = false;  
}  
  
...  
  
void pop_back_n(int n) {  
    SkASSERT(n >= 0);  
    SkASSERT(this->count() >= n);  
    fCount -= n;  
    for (int i = 0; i < n; ++i) {  
        fItemArray[fCount + i].~T(); //---->[3]  
    }  
    this->checkRealloc(0, kShrinking);  
}  
  
...  
  
~RefCntedCallback() {  
    if (fReleaseProc) {  
        SkASSERT(!fResultReleaseProc);  
        fReleaseProc(fReleaseCtx); //---->[4]  
    } else {  
        SkASSERT(fResultReleaseProc);  
        fResultReleaseProc(fReleaseCtx, fResult);  
    }  
}  

```

4. CleanupAfterSkiaFlush will call ProcessCleanupTasks and finally execute to GrDirectContext::abandoned, \*\*If we are currently in GPU hung VK\_ERROR\_DEVICE\_LOST state\*\*, it will call abandonContext[5] to release fMappedBufferManager[6] saved in GrDirectContext, but there is still a reference to the finishContext saved by the closure callback finishCallback.

```
bool GrDirectContext::abandoned() {  
    if (INHERITED::abandoned()) {  
        return true;  
    }  
  
    if (fGpu && fGpu->isDeviceLost()) {  
        this->abandonContext();//----->[5]  
        return true;  
    }  
    return false;  
}  

```
```
void GrDirectContext::abandonContext() {  
    ...  
    // Must be after GrResourceCache::abandonAll().  
    fMappedBufferManager.reset(); //----->[6]  
  
    if (fSmallPathAtlasMgr) {  
        fSmallPathAtlasMgr->reset();  
    }  
    fAtlasManager->freeAll();  
}  

```

5. When the closure callback finishCallback created in asyncReadPixels is executed, it will use the freed fMappedBufferManager, causing UAF[7].

```
void SurfaceContext::asyncReadPixels(GrDirectContext\* dContext,  
                                     const SkIRect& rect,  
                                     SkColorType colorType,  
                                     ReadPixelsCallback callback,  
                                     ReadPixelsContext callbackContext) {  
    ...  
    auto finishCallback = [](GrGpuFinishedContext c) {  
        const auto\* context = reinterpret_cast<const FinishContext\*>(c);  
        auto manager = context->fMappedBufferManager;//----->[7]  
        auto result = std::make_unique<AsyncReadResult>(manager->owningDirectContext());//----->[7]  
        size_t rowBytes =  
                SkAlignTo(context->fSize.width() \* SkColorTypeBytesPerPixel(context->fColorType),  
                          context->fBufferAlignment);  
        if (!result->addTransferResult(context->fTransferResult, context->fSize, rowBytes,  
                                       manager)) {  
            result.reset();  
        }  
        (\*context->fClientCallback)(context->fClientContext, std::move(result));  
        delete context;  
    };  
    ...  
}  

```

[0] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/SurfaceContext.cpp;l=732;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=SurfaceContext::asyncReadPixels&ss=chromium%2Fchromium%2Fsrc>

[1] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/SurfaceContext.cpp;l=759;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=SurfaceContext::asyncReadPixels&ss=chromium%2Fchromium%2Fsrc>

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/SurfaceContext.cpp;l=787;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=SurfaceContext::asyncReadPixels&ss=chromium%2Fchromium%2Fsrc>

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/SurfaceContext.cpp;l=788;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=SurfaceContext::asyncReadPixels&ss=chromium%2Fchromium%2Fsrc>

[2] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/vk/GrVkResourceProvider.cpp;l=443;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=GrVkResourceProvider::checkCommandBuffers&ss=chromium%2Fchromium%2Fsrc>

[3] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/include/private/SkTArray.h;l=313;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=pop_back_n&ss=chromium%2Fchromium%2Fsrc>

[4] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/RefCntedCallback.h;l=41;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=RefCntedCallback&ss=chromium%2Fchromium%2Fsrc>

[5] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/GrDirectContext.cpp;l=162;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=GrDirectContext::abandoned&ss=chromium%2Fchromium%2Fsrc>

[6] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/GrDirectContext.cpp;l=138;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=GrDirectContext::abandoned&ss=chromium%2Fchromium%2Fsrc>

[7] <https://source.chromium.org/chromium/chromium/src/+/main:third_party/skia/src/gpu/ganesh/SurfaceContext.cpp;l=775;drc=f616c54d73c8eea9db5f7e567611711897651b66;bpv=1;bpt=1?q=SurfaceContext::asyncReadPixels&ss=chromium%2Fchromium%2FsrcSteps> to reproduce the problem:

## Other

From the above analysis, it can be seen that the reproduce condition of this vulnerability needs to be able to call asyncReadPixels at the same time when the GPU is hung, thereby creating a closure callback.

Therefore, when the vk context and its own GrClientMappedBufferManager are released, the reference to the GrClientMappedBufferManager is still stored in the callback, causing UAF.

This is the root cause of the unstable reproduction of this bug, I'm not familiar with GPU code, I hope experienced developers can help me fix this bug.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: gpu  

Crash State: see asan log

**CREDIT INFORMATION**  

Reporter credit: Nan Wang (@eternalsakura13) and Yong Liu of 360 Vulnerability Research Institute

## Attachments

- [poc_c56eaf2e4a5a1ff62c74236d538bd093.zip](attachments/poc_c56eaf2e4a5a1ff62c74236d538bd093.zip) (application/octet-stream, 461.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 24.6 KB)
- [fuzz_run_log.txt](attachments/fuzz_run_log.txt) (text/plain, 53.4 KB)

## Timeline

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-09-16)

Please do not dup this issue to https://bugs.chromium.org/p/chromium/issues/detail?id=1358016
1358016 is a little confusing, I reopened a new issue here, please dup it to this issue.

### ts...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL Internals>GPU]

### ts...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-16)

[Empty comment from Monorail migration]

[Monorail components: Internals>Skia]

### [Deleted User] (2022-09-16)

[Empty comment from Monorail migration]

### ts...@chromium.org (2022-09-16)

Pinged hcm offline in search of an owner.

### et...@gmail.com (2022-09-17)

Re https://crbug.com/chromium/1364604#c8:
hi, @tsepez, since the owner of the original bug report seems to be offline, can you help me find a more appropriate owner to fix this issue?


### hc...@google.com (2022-09-17)

thanks for the ping- Greg is our GPU lead and one of our Vk experts- hopefully he can help with analysis or getting another GPU eng on it

### hc...@google.com (2022-09-17)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2022-09-23)

any update?

### gi...@appspot.gserviceaccount.com (2022-09-23)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/ecd08a9d2dc7840618f38eec183ed915bf616a6c

commit ecd08a9d2dc7840618f38eec183ed915bf616a6c
Author: Greg Daniel <egdaniel@google.com>
Date: Fri Sep 23 15:23:47 2022

Fix GrDirectContext::fClinetMappedBuffer access in abandoned callbacks.

Bug: chromium:1364604
Change-Id: I1ca44cab1c762e7f94ac94be94991ec94a7497be
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/583963
Commit-Queue: Greg Daniel <egdaniel@google.com>
Reviewed-by: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/ecd08a9d2dc7840618f38eec183ed915bf616a6c/tests/GrFinishedFlushTest.cpp
[modify] https://crrev.com/ecd08a9d2dc7840618f38eec183ed915bf616a6c/src/gpu/ganesh/GrDirectContext.cpp
[modify] https://crrev.com/ecd08a9d2dc7840618f38eec183ed915bf616a6c/src/gpu/ganesh/GrFinishCallbacks.cpp


### gi...@appspot.gserviceaccount.com (2022-09-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/51474d0bdf88af205e598800e514386dcbdda28c

commit 51474d0bdf88af205e598800e514386dcbdda28c
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date: Sat Sep 24 00:11:40 2022

Roll Skia from ce98326ffda6 to 2daeb66a76f4 (15 revisions)

https://skia.googlesource.com/skia.git/+log/ce98326ffda6..2daeb66a76f4

2022-09-23 jcgregorio@google.com AMD Linux machines upgraded to 11.5.
2022-09-23 egdaniel@google.com Fix jio bot after abandoned finish proc change.
2022-09-23 jvanverth@google.com [metal] Copy shader string into NSString to avoid invalid access.
2022-09-23 herb@google.com Remove unused API calls
2022-09-23 johnstiles@google.com Add Nanobench stat for binary size consumed by modules.
2022-09-23 kjlubick@google.com Fix skcms version
2022-09-23 brianosman@google.com Use default args to remove some gradient factories
2022-09-23 johnstiles@google.com Improve error reporting for duplicate-definition functions.
2022-09-23 kjlubick@google.com Update WASM GM tests to use different constructor
2022-09-23 johnstiles@google.com Honor operator precedence in Expression::description.
2022-09-23 kjlubick@google.com Use different procs for CPU/Ganesh/Graphite tests
2022-09-23 egdaniel@google.com Fix GrDirectContext::fClinetMappedBuffer access in abandoned callbacks.
2022-09-23 herb@google.com Reduce work a-like calls in SkTDArray
2022-09-23 herb@google.com Remove redundant setReserve call
2022-09-23 brianosman@google.com Skip RP stack_rewind test on HWASAN bot

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/skia-autoroll
Please CC jvanverth@google.com on the revert to ensure that a human
is aware of the problem.

To file a bug in Skia: https://bugs.chromium.org/p/skia/issues/entry
To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux-blink-rel;luci.chromium.try:linux-chromeos-compile-dbg;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:win_optional_gpu_tests_rel
Cq-Do-Not-Cancel-Tryjobs: true
Bug: chromium:1364604
Tbr: jvanverth@google.com
Change-Id: I1c7ba64566c7cd1d45b0fe42ea70f255bb59481f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3916870
Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/heads/main@{#1050875}

[modify] https://crrev.com/51474d0bdf88af205e598800e514386dcbdda28c/DEPS


### et...@gmail.com (2022-09-27)

Can you mark it as Fixed(in order to enter the reward process)? thanks :)

### eg...@google.com (2022-09-27)

Since I wasn't able to repro the exact failure, but made a guess about the crash, can we have the original reporter test on the latest ToT chrome to see if the issue is fixed in their test?

### et...@gmail.com (2022-09-27)

I'm the original reporter of this bug, and I can no longer reproduce the bug in my weekend fuzz test run, so I think the problem should have been solved, thanks for your help. :)

### eg...@google.com (2022-09-27)

Thanks for verifying.

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

Requesting merge to extended stable M104 because latest trunk commit (1050875) appears to be after extended stable branch point (1012729).

Requesting merge to stable M105 because latest trunk commit (1050875) appears to be after stable branch point (1027018).

Requesting merge to beta M106 because latest trunk commit (1050875) appears to be after beta branch point (1036826).

Requesting merge to dev M107 because latest trunk commit (1050875) appears to be after dev branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-27)

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-27)

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-27)

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-03)

There are no further planned releases of 104 or 105. 
Merge approved for 107/beta, please ensure there are no issues or concerns with merging to beta and merge to branch 5304 as soon as possible so this fix can be in tomorrow's beta release. 

Will need to revisit for merge to 106 on Wednesday as 106/stable promotion/rollout is ongoing. 

### pb...@google.com (2022-10-05)

[Bulk Edit] Merge approved for M107 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap.

Note : We are cutting M107 Beta RC today i.e., Oct-05th, Please cherry pick the changes  before 1PM PST or earlier.


### am...@chromium.org (2022-10-05)

106 merge approved, please merge this update to branch 5249 at your earliest convenience (NLT noon PST, Friday 7 October) so this fix can be included in the next week's Stable security refresh -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-10-05)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/299f1b4e596b8b945cd9059609df8e0489676ccf

commit 299f1b4e596b8b945cd9059609df8e0489676ccf
Author: Greg Daniel <egdaniel@google.com>
Date: Wed Oct 05 19:28:56 2022

[Cherry-pick] Fix GrDirectContext::fClinetMappedBuffer access in abandoned callbacks.

Bug: chromium:1364604
Change-Id: I1ca44cab1c762e7f94ac94be94991ec94a7497be
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/583963
Commit-Queue: Greg Daniel <egdaniel@google.com>
Reviewed-by: Brian Salomon <bsalomon@google.com>
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/588036
Auto-Submit: Greg Daniel <egdaniel@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/299f1b4e596b8b945cd9059609df8e0489676ccf/src/gpu/ganesh/GrDirectContext.cpp
[modify] https://crrev.com/299f1b4e596b8b945cd9059609df8e0489676ccf/src/gpu/ganesh/GrFinishCallbacks.cpp


### gi...@appspot.gserviceaccount.com (2022-10-05)

The following revision refers to this bug:
  https://skia.googlesource.com/skia/+/07a2ce61e31a5dfdc758e4ef1543fd3d0fa774d2

commit 07a2ce61e31a5dfdc758e4ef1543fd3d0fa774d2
Author: Greg Daniel <egdaniel@google.com>
Date: Wed Oct 05 19:28:56 2022

[Cherry-pick] Fix GrDirectContext::fClinetMappedBuffer access in abandoned callbacks.

Bug: chromium:1364604
Change-Id: I1ca44cab1c762e7f94ac94be94991ec94a7497be
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/583963
Commit-Queue: Greg Daniel <egdaniel@google.com>
Reviewed-by: Brian Salomon <bsalomon@google.com>
Reviewed-on: https://skia-review.googlesource.com/c/skia/+/587879
Auto-Submit: Greg Daniel <egdaniel@google.com>
Commit-Queue: Brian Salomon <bsalomon@google.com>

[modify] https://crrev.com/07a2ce61e31a5dfdc758e4ef1543fd3d0fa774d2/src/gpu/ganesh/GrDirectContext.cpp
[modify] https://crrev.com/07a2ce61e31a5dfdc758e4ef1543fd3d0fa774d2/src/gpu/ganesh/GrFinishCallbacks.cpp


### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations, Nan Wang and Yong Liu! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts in reporting this issue to us -- nice finding and great work! 

### et...@gmail.com (2022-10-07)

Thanks, I'll keep working on the GPU and try to find more interesting bugs. :)


### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### pb...@google.com (2022-10-10)

Based on offline chat with all required changes have been merged to M106 branch hence dropping Merge-Approved-106

### [Deleted User] (2022-10-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### eg...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### pb...@google.com (2022-10-10)

[Bulk Edit] Your change has been approved for M107 Branch, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M107 branch(go/chrome-branches).


### am...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-10-13)

re https://crbug.com/chromium/1364604#c40:
hi,  @amyressler
https://chromereleases.googleblog.com/2022/10/stable-channel-update-for-desktop_11.html
[$15000][1364604] High CVE-2022-3445: Use after free in Skia. Reported by Nan Wang (@eternalsakura13) and Yong Liu of 360 Vulnerability Research Institute on 2022-09-16

Maybe we need to add a CVE tag to this issue?


### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### mi...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1364604?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Internals>GPU, Internals>Skia]
[Monorail mergedwith: crbug.com/chromium/1358016, crbug.com/chromium/1373000]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061001)*
