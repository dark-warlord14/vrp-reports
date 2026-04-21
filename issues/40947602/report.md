# Security: Heap-use-after-free WRITE 16 · cppgc::internal::PersistentRegionBase::ClearAllUsedNodes

| Field | Value |
|-------|-------|
| **Issue ID** | [40947602](https://issues.chromium.org/issues/40947602) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebGPU |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | en...@chromium.org |
| **Created** | 2023-12-01 |
| **Bounty** | $10,000.00 |

## Description

Heap-use-after-free WRITE 16 · cppgc::internal::PersistentRegionBase::ClearAllUsedNodes

**REPRODUCTION CASE**  

Found by myfuzzer run on CF(<https://clusterfuzz.com/testcase-detail/5340201361014784>)  

But it cannot be reproduced stably, I manually provide analysis and report

#RCA  

The GPU::RequestAdapterImpl function uses WTF::BindOnce to create an OnceCallback object.  

By reading the code of WTF::BindOnce, it can be found that it cannot be used across threads.  

However, if we call requestAdapter in the Worker thread, it will result in the object being used across threads.

Through the ASAN (AddressSanitizer) log, it can be observed that the object is created in the Worker thread but released in the main thread, ultimately leading to a Use-After-Free (UAF) issue in the Worker thread.

I am still analyzing the issue to understand the root cause of the problem.

<https://chromium.googlesource.com/chromium/src/+/40f98c8a9f0272b524bc833ddb39268420505a96/third_party/blink/renderer/modules/webgpu/gpu.cc#303>

```
void GPU::RequestAdapterImpl(ScriptState\* script_state,  
                             const GPURequestAdapterOptions\* options,  
                             ScriptPromiseResolver\* resolver) {  
  ExecutionContext\* execution_context = ExecutionContext::From(script_state);  
---CUT---  
    CreateWebGPUGraphicsContext3DProviderAsync(  
        execution_context->Url(),  
        execution_context->GetTaskRunner(TaskType::kWebGPU),  
        WTF::BindOnce(  
            [](GPU\* gpu, ExecutionContext\* execution_context,  
               std::unique_ptr<WebGraphicsContext3DProvider> context_provider) {  
              const KURL& url = execution_context->Url();  
              context_provider =  
                  CheckContextProvider(url, std::move(context_provider));  
              if (context_provider) {  
                context_provider->WebGPUInterface()  
                    ->SetWebGPUExecutionContextToken(  
                        GetExecutionContextToken(execution_context));  
                // Make a new DawnControlClientHolder with the context provider  
                // we just made and set the lost context callback  
                gpu->dawn_control_client_ = DawnControlClientHolder::Create(  
                    std::move(context_provider),  
                    execution_context->GetTaskRunner(TaskType::kWebGPU));  
              }  
              WTF::Vector<base::OnceCallback<void()>> callbacks =  
                  std::move(gpu->dawn_control_client_initialized_callbacks_);  
              for (auto& callback : callbacks) {  
                std::move(callback).Run();  
              }  
            },  
            WrapPersistent(this), WrapPersistent(execution_context)));  
    return;  
  }  

```

<https://chromium.googlesource.com/chromium/src/+/40f98c8a9f0272b524bc833ddb39268420505a96/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc#57>

```
void CreateWebGPUGraphicsContextOnMainThreadAsync(  
    KURL url,  
    scoped_refptr<base::SingleThreadTaskRunner> task_runner,  
    CrossThreadOnceFunction<void(std::unique_ptr<WebGraphicsContext3DProvider>)>  
        callback) {  
  DCHECK(IsMainThread());  
  PostCrossThreadTask(  
      \*task_runner, FROM_HERE,  
      CrossThreadBindOnce(  
          std::move(callback),  
          Platform::Current()->CreateWebGPUGraphicsContext3DProvider(url)));  
}  

```

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 29.2 KB)
- [1.html](attachments/1.html) (text/plain, 1.3 KB)
- [dcheck.txt](attachments/dcheck.txt) (text/plain, 12.5 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 4.1 KB)

## Timeline

### [Deleted User] (2023-12-01)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-12-01)

Bisect
Introduce by this CL
https://chromium-review.googlesource.com/c/chromium/src/+/3874500

### sr...@google.com (2023-12-01)

m.cooolie@ can you recheck the bisect? The linked CL was reverted in https://chromium-review.googlesource.com/c/chromium/src/+/3961194

[Monorail components: Blink>WebGPU]

### sr...@google.com (2023-12-01)

Could it be the reland in https://chromium-review.googlesource.com/c/chromium/src/+/3974333 ?

### m....@gmail.com (2023-12-01)

yes reland by https://chromium-review.googlesource.com/c/chromium/src/+/3974333

### [Deleted User] (2023-12-01)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2023-12-01)

Thanks! Assigning to the CL owner and cc'ing reviewers.
I didn't reproduce this issue since we have an ASAN report in clusterfuzz and a bisect from the reporter.

### sr...@google.com (2023-12-01)

[Empty comment from Monorail migration]

### sr...@google.com (2023-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-01)

[Empty comment from Monorail migration]

### cw...@chromium.org (2023-12-01)

Tentatively assigning to Austin as he looked at this in details with Takahiro.

### [Deleted User] (2023-12-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cw...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### cw...@chromium.org (2023-12-01)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-12-03)

The reason for task freed in the main thread is that GuardedTaskPoster::PostTask calls TryBeginOperation to determine whether to proceed with the PostTask[2].
When the state is kShuttingDown, it causes GuardedTaskPoster::PostTask to return directly, resulting in the task being freed in the main thread.

NOTE:
When is_debug=true, BindOnce[1] adds thread consistency checks, using the provided sample(1.html) can reliably trigger DCHECK(see in dcheck.txt)."

```
1. 
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/wtf/functional.h;drc=8e78783dc1f7007bad46d657c9f332614e240fd8;l=372
#if DCHECK_IS_ON()
  using WrapperType =
      ThreadCheckingCallbackWrapper<base::OnceCallback<UnboundRunType>>;
  cb = base::BindOnce(&WrapperType::Run,
                      std::make_unique<WrapperType>(std::move(cb)));
#endif

2. 
https://source.chromium.org/chromium/chromium/src/+/main:base/task/sequence_manager/task_queue_impl.cc;drc=8e78783dc1f7007bad46d657c9f332614e240fd8;bpv=1;bpt=1;l=64?q=task_queue_impl.cc:75&ss=chromium%2Fchromium%2Fsrc&gsn=PostTask&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Dc%252B%252B%3Fpath%3Dbase%2Ftask%2Fsequence_manager%2Ftask_queue_impl.cc%23BYVPNw8VPfNAcFDhQMIYmllp8G-cCxLPHflKQ1BXIsA
bool TaskQueueImpl::GuardedTaskPoster::PostTask(PostedTask task) {
  // Do not process new PostTasks while we are handling a PostTask (tracing
  // has to do this) as it can lead to a deadlock and defer it instead.
  ScopedDeferTaskPosting disallow_task_posting;

  auto token = operations_controller_.TryBeginOperation();
  if (!token)
    return false;

  outer_->PostTask(std::move(task));
  return true;
}

OperationsController::OperationToken OperationsController::TryBeginOperation() {
---CUT---
  switch (ExtractState(prev_value)) {
    case State::kRejectingOperations:
      return OperationToken(nullptr);
    case State::kAcceptingOperations:
      return OperationToken(this);
    case State::kShuttingDown:
      DecrementBy(1);
      return OperationToken(nullptr);
  }
}
```

### m....@gmail.com (2023-12-03)

My proposed fix is to use CrossThreadBindOnce instead of BindOnce to ensure cross-thread safety.

```
diff --git a/third_party/blink/renderer/modules/webgpu/gpu.cc b/third_party/blink/renderer/modules/webgpu/gpu.cc
index 1031539c83961..2eb1ccdb244b4 100644
--- a/third_party/blink/renderer/modules/webgpu/gpu.cc
+++ b/third_party/blink/renderer/modules/webgpu/gpu.cc
@@ -44,6 +44,8 @@
 #include "third_party/blink/renderer/platform/instrumentation/use_counter.h"
 #include "third_party/blink/renderer/platform/privacy_budget/identifiability_digest_helpers.h"
 #include "third_party/blink/renderer/platform/weborigin/kurl.h"
+#include "third_party/blink/renderer/platform/wtf/cross_thread_functional.h"
+
 
 namespace blink {
 
@@ -300,7 +302,7 @@ void GPU::RequestAdapterImpl(ScriptState* script_state,
     CreateWebGPUGraphicsContext3DProviderAsync(
         execution_context->Url(),
         execution_context->GetTaskRunner(TaskType::kWebGPU),
-        WTF::BindOnce(
+        WTF::CrossThreadBindOnce(
             [](GPU* gpu, ExecutionContext* execution_context,
                std::unique_ptr<WebGraphicsContext3DProvider> context_provider) {
               const KURL& url = execution_context->Url();
@@ -324,7 +326,7 @@ void GPU::RequestAdapterImpl(ScriptState* script_state,
                 std::move(callback).Run();
               }
             },
-            WrapPersistent(this), WrapPersistent(execution_context)));
+            WrapCrossThreadWeakPersistent(this),  WrapCrossThreadWeakPersistent(execution_context)));
     return;
   }
 
diff --git a/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc b/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
index e1665fa565a65..ec159f1b10509 100644
--- a/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
+++ b/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
@@ -92,11 +92,11 @@ CreateOffscreenGraphicsContext3DProvider(
 void CreateWebGPUGraphicsContext3DProviderAsync(
     const KURL& url,
     scoped_refptr<base::SingleThreadTaskRunner> current_thread_task_runner,
-    base::OnceCallback<void(std::unique_ptr<WebGraphicsContext3DProvider>)>
+    CrossThreadOnceFunction<void(std::unique_ptr<WebGraphicsContext3DProvider>)>
         callback) {
   if (IsMainThread()) {
     Platform::Current()->CreateWebGPUGraphicsContext3DProviderAsync(
-        url, std::move(callback));
+        url, ConvertToBaseOnceCallback(std::move(callback)));
   } else {
     // Posts a task to the main thread to create context provider
     // because the current RendererBlinkPlatformImpl and viz::Gpu
@@ -112,7 +112,7 @@ void CreateWebGPUGraphicsContext3DProviderAsync(
         FROM_HERE,
         CrossThreadBindOnce(&CreateWebGPUGraphicsContextOnMainThreadAsync, url,
                             current_thread_task_runner,
-                            CrossThreadBindOnce(std::move(callback))));
+                            std::move(callback)));
   }
 }
 
diff --git a/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h b/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h
index 8fcab24bfec2c..79f91994ef90a 100644
--- a/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h
+++ b/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h
@@ -10,7 +10,7 @@
 #include "third_party/blink/public/platform/web_graphics_context_3d_provider.h"
 #include "third_party/blink/renderer/platform/platform_export.h"
 #include "third_party/blink/renderer/platform/weborigin/kurl.h"
-
+#include "third_party/blink/renderer/platform/wtf/cross_thread_functional.h"
 namespace blink {
 
 // Synchronously creates a WebGraphicsContext3DProvider on any thread.
@@ -42,7 +42,7 @@ CreateWebGPUGraphicsContext3DProvider(const KURL& url);
 PLATFORM_EXPORT void CreateWebGPUGraphicsContext3DProviderAsync(
     const KURL& url,
     scoped_refptr<base::SingleThreadTaskRunner> current_thread_task_runner,
-    base::OnceCallback<void(std::unique_ptr<WebGraphicsContext3DProvider>)>
+    CrossThreadOnceFunction<void(std::unique_ptr<WebGraphicsContext3DProvider>)>
         callback);
 
 }  // namespace blink

```

### [Deleted User] (2023-12-06)

[Empty comment from Monorail migration]

### cw...@chromium.org (2023-12-11)

Austin, Takahiro in the original CL there was some concern about using CrossThreadBindOnce. Do you remember them? Are they still current?

### gi...@appspot.gserviceaccount.com (2023-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4

commit 542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4
Author: Austin Eng <enga@chromium.org>
Date: Wed Dec 13 21:13:45 2023

Use cross thread handles to bind args for async webgpu context creation

Fixed: 1506923
Change-Id: I174703cbd993471e3afb39c0cfa4cce2770755f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5113019
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Reviewed-by: Stephen White <senorblanco@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1237179}

[modify] https://crrev.com/542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h
[modify] https://crrev.com/542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
[modify] https://crrev.com/542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4/third_party/blink/renderer/modules/webgpu/gpu.cc


### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-14)

Requesting merge to stable M120 because latest trunk commit (1237179) appears to be after stable branch point (1217362).

Requesting merge to beta M121 because latest trunk commit (1237179) appears to be after beta branch point (1233107).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-14)

Merge review required: M121 is already shipping to beta.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-14)

Merge review required: M120 is already shipping to stable.

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### en...@chromium.org (2023-12-15)

M121:

1. Yes, it is a security issue
2. https://chromium-review.googlesource.com/c/chromium/src/+/5125833
3. Yes
4. No
5. N/A
6. No


M120:
I'm not sure.
Guidelines say "important security issues (medium severity or higher) requested by the security team", so I'd like feedback from the security team.

### am...@chromium.org (2023-12-15)

Thanks for your work on this and answering the merge questionnaire, enga@. 
https://crrev.com/c/5125833 approved for merge to M121 and M120, because this is a UAF in the GPU process, which is sufficiently serious and warrants backmerge to Stable. 
Please merge this fix to M121 Beta / branch 6167 and M120 Stable / branch 6099 at your earliest convenience and before the EOD 27 December so this fix can be included in the next M120 Stable security and M121 Beta update the first week of January 2024, since we are currently in release freeze. 



### en...@chromium.org (2023-12-15)

No, this is a UAF in the Renderer process

### en...@chromium.org (2023-12-15)

Adding back Merge-Review-120 to clarify whether we should merge to Stable since this is in the renderer process.

### am...@chromium.org (2023-12-18)

Oh right that's clear as day and not sure how I missed that in my earlier check. But yes, renderer memory corruption is still high severity and sufficiently warrants backmerge. 

### gi...@appspot.gserviceaccount.com (2023-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/50a1bddfca85046282797f0361c35c92f9eacf6a

commit 50a1bddfca85046282797f0361c35c92f9eacf6a
Author: Austin Eng <enga@chromium.org>
Date: Tue Dec 19 17:25:51 2023

Use cross thread handles to bind args for async webgpu context creation

(cherry picked from commit 542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4)

Fixed: 1506923
Change-Id: I174703cbd993471e3afb39c0cfa4cce2770755f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5113019
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Reviewed-by: Stephen White <senorblanco@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1237179}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5133239
Cr-Commit-Position: refs/branch-heads/6099@{#1551}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/50a1bddfca85046282797f0361c35c92f9eacf6a/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h
[modify] https://crrev.com/50a1bddfca85046282797f0361c35c92f9eacf6a/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
[modify] https://crrev.com/50a1bddfca85046282797f0361c35c92f9eacf6a/third_party/blink/renderer/modules/webgpu/gpu.cc


### [Deleted User] (2023-12-19)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-12-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c1c8264e475f79375dee3d18814268c25482fb81

commit c1c8264e475f79375dee3d18814268c25482fb81
Author: Austin Eng <enga@chromium.org>
Date: Tue Dec 19 19:12:23 2023

Use cross thread handles to bind args for async webgpu context creation

(cherry picked from commit 542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4)

Fixed: 1506923
Change-Id: I174703cbd993471e3afb39c0cfa4cce2770755f7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5113019
Reviewed-by: Corentin Wallez <cwallez@chromium.org>
Commit-Queue: Austin Eng <enga@chromium.org>
Reviewed-by: Stephen White <senorblanco@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1237179}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5125833
Auto-Submit: Austin Eng <enga@chromium.org>
Commit-Queue: Stephen White <senorblanco@chromium.org>
Cr-Commit-Position: refs/branch-heads/6167@{#499}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/c1c8264e475f79375dee3d18814268c25482fb81/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h
[modify] https://crrev.com/c1c8264e475f79375dee3d18814268c25482fb81/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
[modify] https://crrev.com/c1c8264e475f79375dee3d18814268c25482fb81/third_party/blink/renderer/modules/webgpu/gpu.cc


### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Congratulations! The Chrome VRP Panel has decided to award you $10,000 for this high quality report of memory corruption in the renderer process + bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! Happy New Year! 

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-04)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-16)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-16)

This issue was migrated from crbug.com/chromium/1506923?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



### rz...@google.com (2024-02-13)

1. <https://crrev.com/c/5201365>
2. Low, just a simple conflict and
3. 120, 121
4. Yes, but we need to check with the author if the CL still fixes the issue, had to change a call because its async version doesn't exist in 114: <https://crrev.com/c/5201365/3..4/third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc>

### na...@google.com (2024-02-27)

Approving merge for LTS-114

### ap...@google.com (2024-02-28)

Project: chromium/src
Branch: refs/branch-heads/5735

commit 2a5b082d539917957ef8f51596568206aa625298
Author: Zakhar Voit <voit@google.com>
Date:   Wed Feb 28 16:54:12 2024

    [M114-LTS] Use cross thread handles to bind args for async webgpu context creation
    
    M114 merge issues:
      third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc:
        Conflicting CreateWebGPUGraphicsContext3DProvider calls
    
    (cherry picked from commit 542b278a0c1de7202f4bf5e3e5cbdc2dd6c337d4)
    
    Fixed: 1506923
    Change-Id: I86e7c9901b5cb5b0b1223ceb6300fd231f6ec5cf
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5331672
    Commit-Queue: Austin Eng <enga@chromium.org>
    Reviewed-by: Austin Eng <enga@chromium.org>
    Owners-Override: Mohamed Omar <mohamedaomar@google.com>
    Auto-Submit: Zakhar Voit <voit@google.com>
    Cr-Commit-Position: refs/branch-heads/5735@{#1705}
    Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

M       third_party/blink/renderer/modules/webgpu/gpu.cc
M       third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.cc
M       third_party/blink/renderer/platform/graphics/web_graphics_context_3d_provider_util.h

https://chromium-review.googlesource.com/5331672


### pe...@google.com (2024-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40947602)*
