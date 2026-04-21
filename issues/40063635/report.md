# Security: UAF in MLGraphXnnpack::BuildOnBackgroundThread

| Field | Value |
|-------|-------|
| **Issue ID** | [40063635](https://issues.chromium.org/issues/40063635) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebML |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | qj...@chromium.org |
| **Created** | 2023-03-17 |
| **Bounty** | $10,000.00 |

## Description

UAF in MLGraphXnnpack::BuildOnBackgroundThread

#Reproduce
Apply rca.diff for easy reproduce
chrome --js-flags="-expose-gc --allow-natives-syntax" --no-sandbox --enable-blink-test-features poc.html

NOTE:
Recent windows version of Chromium could not be compiled successfully (gclient sync failed), I did not locally compile and test whether the issue can be reproduced.

#Type of crash
render tab

#Analysis
Same as 1299743 root cause(https://bugs.chromium.org/p/chromium/issues/detail?id=1299743)
1. MLGraphXnnpack::BuildAsyncImpl can called from worker thread
2. BuildAsyncImpl will post BuildOnBackgroundThread to the thread pool for execution, where the parameters are wrapped in WrapCrossThreadPersistent[2]
3. When worker thread get terminal, BuildOnBackgroundThread will access freed object cause UAF[3]

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc;drc=c91306793e6bc6889ac28e1a98176c004f3558fc;l=1195
[2]
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc;drc=c91306793e6bc6889ac28e1a98176c004f3558fc;l=1219
[3]
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;drc=ddf482c0cf47fc8e47e5cfc5c112e2313e066cb8;l=13

#bisect:
https://chromium-review.googlesource.com/c/chromium/src/+/3995467


## Attachments

- [ml.html](attachments/ml.html) (text/plain, 914 B)
- [asan.txt](attachments/asan.txt) (text/plain, 11.1 KB)
- [busy_wait.diff](attachments/busy_wait.diff) (text/plain, 983 B)

## Timeline

### [Deleted User] (2023-03-17)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-03-17)

[Comment Deleted]

### m....@gmail.com (2023-03-17)

=================================================================
==14424==ERROR: AddressSanitizer: use-after-poison on address 0x7eb700342bac at pc 0x7ffb6a3228b5 bp 0x00b88a7fdbe0 sp 0x00b88a7fdc28
READ of size 4 at 0x7eb700342bac thread T4
==14424==*** WARNING: Failed to initialize DbgHelp!              ***
==14424==*** Most likely this means that the app is already      ***
==14424==*** using DbgHelp, possibly with incompatible flags.    ***
==14424==*** Due to technical reasons, symbolization might crash ***
==14424==*** or produce wrong results.                           ***
    #0 0x7ffb6a3228b4 in blink::MLGraphXnnpack::CreateXnnSubgraphAndRuntime D:\chromium\src\third_party\blink\renderer\modules\ml\webnn\ml_graph_xnnpack.cc:1173
    #1 0x7ffb6a31faa6 in blink::MLGraphXnnpack::BuildOnBackgroundThread D:\chromium\src\third_party\blink\renderer\modules\ml\webnn\ml_graph_xnnpack.cc:1095
    #2 0x7ffb6a32c9bd in base::internal::FunctorTraits<void (*)(cppgc::internal::BasicCrossThreadPersistent<blink::MLGraphXnnpack,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::HeapVector<std::Cr::pair<WTF::String,cppgc::internal::BasicMember<blink::MLOperand,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer> >,0>,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::HeapVector<cppgc::internal::BasicMember<const blink::MLOperator,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>,0>,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::ScriptPromiseResolver,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, scoped_refptr<base::SequencedTaskRunner>),void>::Invoke<void (*)(cppgc::internal::BasicCrossThreadPersistent<blink::MLGraphXnnpack,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::HeapVector<std::Cr::pair<WTF::String,cppgc::internal::BasicMember<blink::MLOperand,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer> >,0>,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink: D:\chromium\src\base\functional\bind_internal.h:654
    #3 0x7ffb6a32c6d6 in base::internal::Invoker<base::internal::BindState<void (*)(cppgc::internal::BasicCrossThreadPersistent<blink::MLGraphXnnpack,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::HeapVector<std::Cr::pair<WTF::String,cppgc::internal::BasicMember<blink::MLOperand,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer> >,0>,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::HeapVector<cppgc::internal::BasicMember<const blink::MLOperator,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer>,0>,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, cppgc::internal::BasicCrossThreadPersistent<blink::ScriptPromiseResolver,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>, scoped_refptr<base::SequencedTaskRunner>),cppgc::internal::BasicCrossThreadPersistent<blink::MLGraphXnnpack,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicCrossThreadPersistent<blink::HeapVector<std::Cr::pair<WTF::String,cppgc::internal::BasicMember<blink::MLOperand,cppgc::internal::StrongMemberTag,cppgc::internal::DijkstraWriteBarrierPolicy,cppgc::internal::DisabledCheckingPolicy,cppgc::internal::CompressedPointer> >,0>,cppgc::internal::StrongCrossThreadPersistentPolicy,cppgc::internal::IgnoreLocationPolicy,cppgc::internal::DisabledCheckingPolicy>,cppgc::internal::BasicCrossThreadPersistent<blink::Heap D:\chromium\src\base\functional\bind_internal.h:989
    #4 0x7ffc01b357b7 in base::TaskAnnotator::RunTaskImpl D:\chromium\src\base\task\common\task_annotator.cc:165
    #5 0x7ffc01bf1609 in base::internal::TaskTracker::RunTaskImpl D:\chromium\src\base\task\thread_pool\task_tracker.cc:649
    #6 0x7ffc01bf1409 in base::internal::TaskTracker::RunContinueOnShutdown D:\chromium\src\base\task\thread_pool\task_tracker.cc:626
    #7 0x7ffc01bf0907 in base::internal::TaskTracker::RunTask D:\chromium\src\base\task\thread_pool\task_tracker.cc:491
    #8 0x7ffc01bef9fb in base::internal::TaskTracker::RunAndPopNextTask D:\chromium\src\base\task\thread_pool\task_tracker.cc:406
    #9 0x7ffc01c1363f in base::internal::WorkerThread::RunWorker D:\chromium\src\base\task\thread_pool\worker_thread.cc:480
    #10 0x7ffc01c1280f in base::internal::WorkerThread::RunPooledWorker D:\chromium\src\base\task\thread_pool\worker_thread.cc:356
    #11 0x7ffc01d3b051 in base::`anonymous namespace'::ThreadFunc D:\chromium\src\base\threading\platform_thread_win.cc:134
    #12 0x7ffc0045b6f3 in _asan_default_suppressions__dll+0x13a3 (D:\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004b6f3)
    #13 0x7ffc52f87613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)
    #14 0x7ffc531a26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

Address 0x7eb700342bac is a wild pointer inside of access range of size 0x000000000004.
SUMMARY: AddressSanitizer: use-after-poison D:\chromium\src\third_party\blink\renderer\modules\ml\webnn\ml_graph_xnnpack.cc:1173 in blink::MLGraphXnnpack::CreateXnnSubgraphAndRuntime
Shadow bytes around the buggy address:
  0x7eb700342900: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342980: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342a00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342a80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342b00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x7eb700342b80: 00 00 00 00 00[00]00 00 00 00 00 00 00 00 00 00
  0x7eb700342c00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342c80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342d00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342d80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x7eb700342e00: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
Thread T4 created by T0 here:

#0 0x7ffc0045ce52 in _asan_wrap_CreateThread+0x62 (D:\chromium\src\out\asan\clang_rt.asan_dynamic-x86_64.dll+0x18004ce52)
    #1 0x7ffc01d39f38 in base::`anonymous namespace'::CreateThreadInternal D:\chromium\src\base\threading\platform_thread_win.cc:199
    #2 0x7ffc01c10b0c in base::internal::WorkerThread::Start D:\chromium\src\base\task\thread_pool\worker_thread.cc:193
    #3 0x7ffc01c04805 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl::<lambda_2>::operator() D:\chromium\src\base\task\thread_pool\thread_group_impl.cc:179
    #4 0x7ffc01c041c3 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::WorkerContainer::ForEachWorker<`lambda at ../../base/task/thread_pool/thread_group_impl.cc:178:37'> D:\chromium\src\base\task\thread_pool\thread_group_impl.cc:146
    #5 0x7ffc01c03904 in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::FlushImpl D:\chromium\src\base\task\thread_pool\thread_group_impl.cc:178
    #6 0x7ffc01bf760e in base::internal::ThreadGroupImpl::ScopedCommandsExecutor::~ScopedCommandsExecutor D:\chromium\src\base\task\thread_pool\thread_group_impl.cc:102
    #7 0x7ffc01bf72be in base::internal::ThreadGroupImpl::Start D:\chromium\src\base\task\thread_pool\thread_group_impl.cc:408
    #8 0x7ffc01c09718 in base::internal::ThreadPoolImpl::Start D:\chromium\src\base\task\thread_pool\thread_pool_impl.cc:194
    #9 0x7ffb99ba954d in content::ChildProcess::ChildProcess D:\chromium\src\content\child\child_process.cc:120
    #10 0x7ffb9d5713d8 in content::RenderProcess::RenderProcess D:\chromium\src\content\renderer\render_process.cc:18
    #11 0x7ffb9d571604 in content::RenderProcessImpl::RenderProcessImpl D:\chromium\src\content\renderer\render_process_impl.cc:99
    #12 0x7ffb9d571b19 in content::RenderProcessImpl::Create D:\chromium\src\content\renderer\render_process_impl.cc:283    #13 0x7ffb9d59b968 in content::RendererMain D:\chromium\src\content\renderer\renderer_main.cc:278
    #14 0x7ffb9db2c544 in content::RunOtherNamedProcessTypeMain D:\chromium\src\content\app\content_main_runner_impl.cc:761
    #15 0x7ffb9db2ef06 in content::ContentMainRunnerImpl::Run D:\chromium\src\content\app\content_main_runner_impl.cc:1135
    #16 0x7ffb9db29968 in content::RunContentProcess D:\chromium\src\content\app\content_main.cc:335
    #17 0x7ffb9db2a82a in content::ContentMain D:\chromium\src\content\app\content_main.cc:363
    #18 0x7ffbd43216ae in ChromeMain D:\chromium\src\chrome\app\chrome_main.cc:190
    #19 0x7ff657b25e3a in MainDllLoader::Launch D:\chromium\src\chrome\app\main_dll_loader_win.cc:166
    #20 0x7ff657b22a92 in main D:\chromium\src\chrome\app\chrome_exe_main_win.cc:391
    #21 0x7ff657dc679b in __scrt_common_main_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe_common.inl:288    #22 0x7ffc52f87613 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017613)
    #23 0x7ffc531a26a0 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x1800526a0)

### m....@gmail.com (2023-03-17)

It can be easily reproduced by associating only one CPU core to chromium.

### cl...@chromium.org (2023-03-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6133776250503168.

### m....@gmail.com (2023-03-20)

You can specify only one CPU core for CF to test

### ts...@chromium.org (2023-03-20)

Retrying with one CPU core.

### ts...@chromium.org (2023-03-20)

Apparently, there is a mutli-core flag but not a single-core flag.

### ts...@chromium.org (2023-03-20)

Assigning per https://crbug.com/1425922 - probably both should be looked at together?


[Monorail components: Blink>Internals>Modularization]

### qj...@chromium.org (2023-03-21)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Internals>Modularization Blink>WebML]

### [Deleted User] (2023-03-21)

The assigned owner "ningxin.hu@intel.com" is not able to receive e-mails, please re-triage.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qj...@chromium.org (2023-03-22)

[Empty comment from Monorail migration]

### ni...@intel.com (2023-03-22)

Thanks reporting and the analysis of this issue. I think we hit the first caveat of `CrossThreadPersistent ` [1] that

// Caveats:
// - Does not protect the heap owning an object from terminating. E.g., posting
//   a task with a CrossThreadPersistent for `this` will result in a
//   use-after-free in case the heap owning `this` is terminated before the task
//   is invoked.

I think a quick fix is to only expose async graph build() [2] and compute() [3] API to main thread (window). This would prevent JS code from using the async API in worker thread that causes this issue.  As far as I know, most WebNN developers either use async API in main thread or use sync API in worker thread. I am not aware anyone is using async API in worker. So, I suppose the impact would be minimum.

Later, if web developers still need async API in worker, we may fix it by referring to the solution for 1299743 [4]. The longer term solution may create a graph build info object that contains all info of operands and operators and transfer its ownership to worker pool thread for XNNPACK subgraph creation. In this way, the worker pool thread won't need to refer to the GC objects allocated on worker's heap.

WDYT, @qjw@chromium.org?

[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;l=20
[2]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/webnn/ml_graph_builder.idl;l=124
[3]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/ml/ml_context.idl;l=27
[4]: https://chromium-review.googlesource.com/c/chromium/src/+/3498864

### qj...@chromium.org (2023-03-23)

Do we have guarantee that this kind of issue won't happen on window?

My read of https://crbug.com/1299743 is this is because worker thread is destroyed before thread poll task starts running? What's preventing this from main thread (i.e. do we have guarantee that tasks are destroyed before main thread heap destroys)?

How complex would the long term solution be? If it's not too much work, I think we should do the long term fix. Otherwise I'm okay with the short-term fix you proposed then do a follow-up ASAP.

Also, based on the comment, seems this API is prone to misuse, we probably should reconsider the implementation and explore options to avoid using this.

+danakj (who triaged the root cause issue) for thoughts. Is stopping the method being called in Worker context sufficient to fix this?

### ni...@intel.com (2023-03-24)

I observed a similar usage of `AsyncAudioDecoder::DecodeAsync()` [1] that wraps `DOMArrayBuffer` by `CrossThreadPersistent` and posts it to worker pool thread for accessing. `AsyncAudioDecoder::DecodeAsync()` checks itself must be called on main thread.


[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/async_audio_decoder.h;l=67;bpv=1;bpt=1

### ni...@intel.com (2023-03-24)

> Also, based on the comment, seems this API is prone to misuse, we probably should reconsider the implementation and explore options to avoid using this.

Agreed. According to the comment of `CrossThreadPersistent` [1], we may want to use `CrossThreadHandle` [2] instead. I'll investigate and update later.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;l=16
[2]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_handle.h;l=49

### am...@chromium.org (2023-03-24)

before M110, so setting FoundIn-110 as it is currently the oldest active release channel; SI-None due to this being specific to blink test features 

### am...@chromium.org (2023-03-24)

Hi qjw@, since this bug cannot be assigned to ningxin.hu due to email bounce-backs, so ownership is rejected by the bot, is it okay if we assign this to you? 
Security bugs cannot go without owners so it's putting red in our triage dashboard. Please feel free to reassign to someone who can accept ownership if there is someone this can be assigned to. Thanks! 

### qj...@chromium.org (2023-03-27)

I can take the owner while Ningxin (who is the correct owner if not for the email bounce check) is working on a fix.

I'm not sure how the email bounce stuff could be fixed (this has caused some nuance that we worked around in the past).

### ni...@intel.com (2023-03-27)

Thanks Jiewei! I am checking around on my side about the email bounce issue. Before that fixed, I'll check this issue daily to ensure I won't miss anything.

### ni...@intel.com (2023-03-27)

I can't reproduce this issue locally. It might be because my machine has too many cores.

@m.cooolie@gmail.com, I can't find `rca.diff` in the attachments. Did I miss anything?

On my side, I made a small patch that busy-wait for 10ms in the beginning of `MLGraphXnnpack::BuildOnBackgroundThread()`. It can reproduce this issue for me. After the busy-wait, the accessing of `graph->xnn_context_`  causes UAF issue.

```
diff --git a/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc b/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
index 856fa5f3b28df..c7cc6d09351ab 100644
--- a/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
+++ b/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
@@ -1210,6 +1210,10 @@ void MLGraphXnnpack::BuildOnBackgroundThread(
         toposorted_operators,
     CrossThreadPersistent<ScriptPromiseResolver> resolver,
     scoped_refptr<base::SequencedTaskRunner> resolver_task_runner) {
+  // Busy wait for 10ms to tigger UAF issue.
+  const base::TimeTicks end_time = base::TimeTicks::Now() + base::Milliseconds(10);
+  while (base::TimeTicks::Now() < end_time) {};
+
   DCHECK(!IsMainThread());
   DCHECK(!graph->xnn_context_);
```

Please take a look and let me know whether this reproducing method works. Thanks!

### m....@gmail.com (2023-03-27)

Thank you for your feedback, because the method provided by https://bugs.chromium.org/p/chromium/issues/detail?id=1425922 can be reproduced stably locally without modifying the code, so it is not provided

### m....@gmail.com (2023-03-27)

Thank you for your feedback, because the method provided by https://bugs.chromium.org/p/chromium/issues/detail?id=1425922 can be reproduced stably locally without modifying the code, so it is not provided

### ni...@intel.com (2023-03-30)

Thanks, I can reproduce without busy_wait.diff on a machine with less cores.

### ni...@intel.com (2023-03-30)

The long-term fix is ready for review: https://chromium-review.googlesource.com/c/chromium/src/+/4373880

I verified locally that the UAF issue disappeared after applying the fix. 

### gi...@appspot.gserviceaccount.com (2023-04-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6

commit 7131bbb91d0bbcd502b53add8a8c715f2b9dffc6
Author: Ningxin Hu <ningxin.hu@intel.com>
Date: Wed Apr 05 00:31:54 2023

WebNN: Disable async build and compute methods for dedicated worker

This CL disables async `MLGraphBuilder.build()` and
`MLContext.compute()` for dedicated worker context, because the current
implementation is not safe to be called in a Web worker.

The existing `MLGraphXnnpack::BuildAsyncImpl()` and
`MLGraphXnnpack::ComputeAsyncImpl()` send the objects wrapped by
`CrossThreadPersistent` [1] to worker pool thread for processing.
However, `CrossThreadPersistent` doesn't protect the heap owning an
object from terminating. This would cause UAF (use-after-free) issue,
when the calling Web worker thread terminates, e.g. user code calls
`worker.terminate()`, `MLGraphXnnpack::BuildOnBackgroundThread()` or
`MLGraphXnnpack::ComputeOnBackgroundThread()` running worker pool thread
may access these freed objects.

The longer-term solution is left as TODOs. It may refer to the similar
fix of `FileSystemAccessRegularFileDelegate` [2] that transfers the
ownership of objects instead of wrapping them in
`CrossThreadPersistent`.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;drc=ddf482c0cf47fc8e47e5cfc5c112e2313e066cb8;l=13
[2]: https://bugs.chromium.org/p/chromium/issues/detail?id=1299743

Bug: 1425370,1425922
Change-Id: I294ab87859cc0954ae4f97e759e5111cef537a92
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4360360
Commit-Queue: ningxin hu <ningxin.hu@intel.com>
Reviewed-by: Jiewei Qian <qjw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1126346}

[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/pooling.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/softmax.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/leaky_relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/reshape.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/pooling.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/clamp.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/conv2d.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/renderer/modules/ml/webnn/ml_graph_builder.idl
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/leaky_relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/webexposed/global-interface-listing-dedicated-worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/relu.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/pad.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/hard_swish.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/softmax.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/pad.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/transpose.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/gemm.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/elementwise_binary.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/concat.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/reshape.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/clamp.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/conv2d.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/elementwise_binary.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/concat.https.any.worker-expected.txt
[add] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/sigmoid.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/win/external/wpt/webnn/idlharness.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/idlharness.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/sigmoid.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/transpose.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/renderer/modules/ml/ml_context.idl
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/hard_swish.https.any.worker-expected.txt
[modify] https://crrev.com/7131bbb91d0bbcd502b53add8a8c715f2b9dffc6/third_party/blink/web_tests/platform/mac/external/wpt/webnn/gemm.https.any.worker-expected.txt


### gi...@appspot.gserviceaccount.com (2023-04-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9ba5635929fe308bac22f1216a163c320a333939

commit 9ba5635929fe308bac22f1216a163c320a333939
Author: Ningxin Hu <ningxin.hu@intel.com>
Date: Thu Apr 13 08:20:06 2023

WebNN: Fix UAF issue in MLGraphXnnpack::BuildOnBackgroundThread()

The existing `MLGraphXnnpack::BuildAsyncImpl()` sends the GC objects
wrapped by `CrossThreadPersistent` [1] to worker pool thread for
processing. However, `CrossThreadPersistent` doesn't protect the heap
owning an object from terminating. This would cause UAF (use-after-free)
issue, when the calling Web worker thread terminates, e.g. user code
calls `worker.terminate()`, `MLGraphXnnpack::BuildOnBackgroundThread()`
running worker pool thread may access these freed objects.

This CL fixes this issue by wrapping the GC objects in
`CrossThreadHandle` [2] instead, passing them forward to and only
accessing them in the thread owning the heap. This CL implements
`MLGraphXnnpack::BuildAsyncImpl()` in a sequence of three steps. First,
it posts a task to a background thread that gets an instance of
`SharedXnnpackContext`, because XNNPACK library initialization may be
time-consuming. Then it runs a task in the thread owning the heap and
creates the XNNPACK Subgraph by traversing the GC objects of an MLGraph.
Last, it posts another task to the background thread that creates an
XNNPACK Runtime object with the created Subgraph, because it may also be
an expensive operation.


[1]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_persistent.h;l=16
[2]: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/heap/cross_thread_handle.h;l=49

Bug: 1425370
Change-Id: I903e9e3468761e8cecca79ae10a0cab08b310a62
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4373880
Commit-Queue: ningxin hu <ningxin.hu@intel.com>
Reviewed-by: Jiewei Qian <qjw@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1129732}

[modify] https://crrev.com/9ba5635929fe308bac22f1216a163c320a333939/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.cc
[modify] https://crrev.com/9ba5635929fe308bac22f1216a163c320a333939/third_party/blink/renderer/modules/ml/webnn/ml_graph_xnnpack.h


### am...@chromium.org (2023-04-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-04-18)

Marking this bug as fixed based on CL and https://crbug.com/chromium/1425370#c25 

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-27)

Congratulations! The VRP Panel has decided to award you $10,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2023-04-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-25)

This issue was migrated from crbug.com/chromium/1425370?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063635)*
