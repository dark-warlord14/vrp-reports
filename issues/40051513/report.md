# Use-after-poison in WebGLRenderingContextBase

| Field | Value |
|-------|-------|
| **Issue ID** | [40051513](https://issues.chromium.org/issues/40051513) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebGL, Blink>Workers |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | da...@davidmanouchehri.com |
| **Assignee** | sh...@google.com |
| **Created** | 2020-02-13 |
| **Bounty** | $8,500.00 |

## Description

**VULNERABILITY DETAILS**  

Inside WebGLRenderingContextBase::PrintWarningToConsole, we can end up in a state where a garbage collected context is used.

We can trigger this edge case through the following steps:

1. Create an iframe and append it to our document to get a new ExecutionContext
2. Create a AudioWorklet within our new iframe's ExecutionContext
3. Remove the iframe's ExecutionContext, which calls ContextLifecycleObserver::ContextDestroyed
4. Force a WebGL console error message, which will attempt to use the context that was uninitialized

void WebGLRenderingContextBase::PrintWarningToConsole(const String& message) {  

blink::ExecutionContext\* context = Host()->GetTopExecutionContext();  

if (context) { // <------------------ UAP, does not check if the context has been destroyed  

context->AddConsoleMessage(  

ConsoleMessage::Create(mojom::ConsoleMessageSource::kRendering,  

mojom::ConsoleMessageLevel::kWarning, message));  

}  

}

Note: I'm simply using AudioWorklets because I'm already familiar with them, I don't think there's a bug here in WebAudio. I would expect other Worklet interfaces to be able to trigger the same bug.

**VERSION**  

Tested on 79.0.3945.130 + stable and 82.0.4057.0 + canary  

Operating System: Any

**REPRODUCTION CASE**  

Put audio.html, audio.js, and processor.js in the same folder, then serve that folder over HTTPS. Open <https://localhost:44444/audio.html> (replace with applicable port/host) in Chrome.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: Tab/renderer  

Crash State:  

[0212/191530.862516:ERROR:buffer\_manager.cc(817)] [.WebGL-0x61b000063580]GL ERROR :GL\_INVALID\_VALUE : glMapBufferRange: bound to target 0x8892 : offset/size out of range  

Received signal 11 SEGV\_MAPERR 000000000048  

#0 0x5576b998632b in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4107:13  

#1 0x5576c4159e89 in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:840:39  

#2 0x5576c3f1b0c3 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack\_trace.cc:206:12  

#3 0x5576c3f1b0c3 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:203:28  

#4 0x5576c4158aba in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo\_t\*, void\*) ./../../base/debug/stack\_trace\_posix.cc:345:3  

#5 0x7f2d9b55a890 in \_\_funlockfile ??:?  

#6 0x7f2d9b55a890 in ?? ??:0  

#7 0x5576d235f4a6 in blink::WorkerThread::GetWorkerReportingProxy() const ./../../third\_party/blink/renderer/core/workers/worker\_thread.h:0:12  

#8 0x5576d235f4a6 in blink::WorkletGlobalScope::AddConsoleMessageImpl(blink::ConsoleMessage\*, bool) ./../../third\_party/blink/renderer/core/workers/worklet\_global\_scope.cc:149:19  

#9 0x5576d397d93d in blink::ExecutionContext::AddConsoleMessage(blink::ConsoleMessage\*, bool) ./../../third\_party/blink/renderer/core/execution\_context/execution\_context.h:231:5  

#10 0x5576d397d93d in blink::WebGLRenderingContextBase::PrintWarningToConsole(WTF::String const&) ./../../third\_party/blink/renderer/modules/webgl/webgl\_rendering\_context\_base.cc:7609:14  

#11 0x5576d397d93d in blink::WebGLRenderingContextBase::PrintGLErrorToConsole(WTF::String const&) ./../../third\_party/blink/renderer/modules/webgl/webgl\_rendering\_context\_base.cc:7596:3  

#12 0x5576d397a2ca in blink::WebGLRenderingContextBase::OnErrorMessage(char const\*, int) ./../../third\_party/blink/renderer/modules/webgl/webgl\_rendering\_context\_base.cc:1434:5  

#13 0x5576c7622fda in base::RepeatingCallback<void (char const\*, int)>::Run(char const\*, int) const & ./../../base/callback.h:132:12  

#14 0x5576c7622fda in gpu::gles2::GLES2Implementation::SendErrorMessage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >, int) ./../../gpu/command\_buffer/client/gles2\_implementation.cc:414:27  

#15 0x5576c7622c09 in gpu::gles2::GLES2Implementation::OnGpuControlErrorMessage(char const\*, int) ./../../gpu/command\_buffer/client/gles2\_implementation.cc:373:3  

#16 0x5576bb5de455 in void base::DispatchToMethodImpl<gpu::CommandBufferProxyImpl\*, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&), std::\_\_1::tuple<GPUCommandBufferConsoleMessage>, 0ul>(gpu::CommandBufferProxyImpl\* const&, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&), std::\_\_1::tuple<GPUCommandBufferConsoleMessage>&&, std::\_\_1::integer\_sequence<unsigned long, 0ul>) ./../../base/tuple.h:52:3  

#17 0x5576bb5de455 in void base::DispatchToMethod<gpu::CommandBufferProxyImpl\*, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&), std::\_\_1::tuple<GPUCommandBufferConsoleMessage> >(gpu::CommandBufferProxyImpl\* const&, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&), std::\_\_1::tuple<GPUCommandBufferConsoleMessage>&&) ./../../base/tuple.h:60:3  

#18 0x5576bb5de455 in void IPC::DispatchToMethod<gpu::CommandBufferProxyImpl, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&), void, std::\_\_1::tuple<GPUCommandBufferConsoleMessage> >(gpu::CommandBufferProxyImpl\*, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&), void\*, std::\_\_1::tuple<GPUCommandBufferConsoleMessage>&&) ./../../ipc/ipc\_message\_templates.h:51:3  

#19 0x5576bb5de455 in bool IPC::MessageT<GpuCommandBufferMsg\_ConsoleMsg\_Meta, std::\_\_1::tuple<GPUCommandBufferConsoleMessage>, void>::Dispatch<gpu::CommandBufferProxyImpl, gpu::CommandBufferProxyImpl, void, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&)>(IPC::Message const\*, gpu::CommandBufferProxyImpl\*, gpu::CommandBufferProxyImpl\*, void\*, void (gpu::CommandBufferProxyImpl::\*)(GPUCommandBufferConsoleMessage const&)) ./../../ipc/ipc\_message\_templates.h:146:7  

#20 0x5576bb5dd645 in gpu::CommandBufferProxyImpl::OnMessageReceived(IPC::Message const&) ./../../gpu/ipc/client/command\_buffer\_proxy\_impl.cc:144:5  

#21 0x5576c4029773 in base::OnceCallback<void ()>::Run() && ./../../base/callback.h:98:12  

#22 0x5576c4029773 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) ./../../base/task/common/task\_annotator.cc:142:33  

#23 0x5576c4062619 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*, bool\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:365:23  

#24 0x5576c4061f9a in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoSomeWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:219:7  

#25 0x5576c3f6ac4e in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_default.cc:39:55  

#26 0x5576c4064403 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:463:12  

#27 0x5576c4064403 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#28 0x5576c3fd8c7b in base::RunLoop::Run() ./../../base/run\_loop.cc:124:14  

#29 0x5576c21e4f32 in blink::scheduler::WorkerThread::SimpleThreadImpl::Run() ./../../third\_party/blink/renderer/platform/scheduler/worker/worker\_thread.cc:169:14  

#30 0x5576c4191632 in base::(anonymous namespace)::ThreadFunc(void\*) ./../../base/threading/platform\_thread\_posix.cc:81:13  

#31 0x7f2d9b54f6db in start\_thread ??:0:0  

#32 0x7f2d93d6188f in clone ??:0:0  

r8: 7fffffffffffffff r9: 00007f2d77e39864 r10: 00007f2d79146f50 r11: 00000fd7ad71c3e2  

r12: 00007ecb2a861a98 r13: 00000fd96550c3db r14: 00007ecb2a861ed8 r15: 00007eb96b921ec8  

di: 0000000000000048 si: 00007eb96b921ec8 bp: 00007f2d79147090 bx: 00007f2d791470a0  

dx: 0000000000000000 ax: 0000000000000009 cx: 00005576d639e660 sp: 00007f2d79147050  

ip: 00005576d235f4a6 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004  

trp: 000000000000000e msk: 0000000000000000 cr2: 0000000000000048  

[end of stack trace]

**CREDIT INFORMATION**  

Reporter credit: David Manouchehri

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### da...@davidmanouchehri.com (2020-02-13)

The primitive gained is the same as https://bugs.chromium.org/p/chromium/issues/detail?id=1048473.

I'm going to take a stab at patching this one myself. =) 

### da...@davidmanouchehri.com (2020-02-13)

[Comment Deleted]

### da...@davidmanouchehri.com (2020-02-13)

I've patched the vulnerability for ya, no longer crashes on the UAP. https://chromium-review.googlesource.com/c/chromium/src/+/2053167


### da...@davidmanouchehri.com (2020-02-13)

Could @shrekshao be added to this ticket? I believe he's looked at similar bugs before.

### rs...@chromium.org (2020-02-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebGL]

### cl...@chromium.org (2020-02-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5644307466878976.

### cl...@chromium.org (2020-02-13)

ClusterFuzz testcase 5644307466878976 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-02-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5644307466878976

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000048
Crash State:
  blink::WorkletGlobalScope::AddConsoleMessageImpl
  blink::WebGLRenderingContextBase::PrintWarningToConsole
  blink::WebGLRenderingContextBase::PrintGLErrorToConsole
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=741099

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5644307466878976

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5644307466878976 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

### da...@davidmanouchehri.com (2020-02-13)

I rebased my CL and confirmed that the UAP does not occur locally anymore. Not sure what ClusterFuzz is up to.

### rs...@chromium.org (2020-02-17)

[Empty comment from Monorail migration]

### rs...@chromium.org (2020-02-17)

shrekshao: Could you look at this? This seems related to https://crbug.com/chromium/1008300, and it looks like it may be a worker race condition triggering whether or not it will be a NULL deref or something else. I'm tentatively targeting it Medium, but it may be a high if it ends up as a UAP?

I can reproduce it as a crash on HEAD, kicked off clusterfuzz again. 

[Monorail components: Blink>Workers]

### [Deleted User] (2020-02-17)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-17)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2020-02-18)

Detailed Report: https://clusterfuzz.com/testcase?key=5644307466878976

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000048
Crash State:
  blink::WorkletGlobalScope::AddConsoleMessageImpl
  blink::WebGLRenderingContextBase::PrintWarningToConsole
  blink::WebGLRenderingContextBase::PrintGLErrorToConsole
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=668438:668440

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5644307466878976

Additional requirements: Requires HTTP

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5644307466878976 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### da...@davidmanouchehri.com (2020-02-18)

Could you try applying my patch? It's pretty simple and should solve the problem. https://chromium-review.googlesource.com/c/chromium/src/+/2053167

### [Deleted User] (2020-02-18)

[Empty comment from Monorail migration]

### sh...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### sh...@google.com (2020-02-18)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/54454ec7fbcbd043f7eafea03049e53ccec5e04f

commit 54454ec7fbcbd043f7eafea03049e53ccec5e04f
Author: David Manouchehri <david@davidmanouchehri.com>
Date: Wed Feb 19 00:29:19 2020

Verify if the context is still available.

Bug: 1051748
Change-Id: I6bbef3ef50930048984593270fbe39a59a6d61f3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2053167
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Auto-Submit: David Manouchehri <david@davidmanouchehri.com>
Cr-Commit-Position: refs/heads/master@{#742401}

[modify] https://crrev.com/54454ec7fbcbd043f7eafea03049e53ccec5e04f/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### [Deleted User] (2020-02-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kb...@chromium.org (2020-02-19)

We believe this is fixed with the above CL.


### da...@davidmanouchehri.com (2020-02-19)

I think this should have the Security_Impact-Stable label added back, not sure why ClusterFuzz removed it.

### kb...@chromium.org (2020-02-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-02-20)

ClusterFuzz testcase 5644307466878976 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=742396:742403

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-02-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-24)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-24)

Requesting merge to beta M81 because latest trunk commit (742401) appears to be after beta branch point (737173).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-02-24)

This bug requires manual review: M81's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2020-02-25)

+adetaylor@(Security TPM) for inputs.

shrekshao@google.com please provide the details w.r.t questions posted in https://crbug.com/chromium/1051748#c28 which would help us in approval process.

### sh...@google.com (2020-02-25)

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
The CL is landed on Feb 19 2020. which is within four weeks of beta rollout.
This is a minor tweak.
The bug is not release blocking though. Target-81 label is added by sheriff
2. Links to the CLs you are requesting to merge.
Commit: https://chromium.googlesource.com/chromium/src/+/54454ec7fbcbd043f7eafea03049e53ccec5e04f
Reviewed on: https://chromium-review.googlesource.com/c/chromium/src/+/2053167
3. Has the change landed and been verified on master/ToT?
Yes
4. Why are these changes required in this milestone after branch?
It's a defect that could lead to a tab/renderer crash. The fix is verified by clusterfuzz
5. Is this a new feature?
No
6. If it is a new feature, is it behind a flag using finch?
N/A

### ad...@chromium.org (2020-02-25)

Yes, please merge to M81 (branch: 4044).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-02-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8a429ea726a967e02c5a57c2bf6819c3c39e1c24

commit 8a429ea726a967e02c5a57c2bf6819c3c39e1c24
Author: shrekshao <shrekshao@google.com>
Date: Wed Feb 26 02:27:24 2020

[M81 merge] Verify if the context is still available.

TBR=david@davidmanouchehri.com
(cherry picked from commit 54454ec7fbcbd043f7eafea03049e53ccec5e04f)

Bug: 1051748
Change-Id: I2806d3fcdcc54e7b9f3247893de49a5d88cb31b8
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Auto-Submit: David Manouchehri <david@davidmanouchehri.com>
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2073150
Commit-Queue: Shrek Shao <shrekshao@google.com>
Cr-Commit-Position: refs/branch-heads/4044@{#484}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/8a429ea726a967e02c5a57c2bf6819c3c39e1c24/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### na...@google.com (2020-02-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-02-27)

Congrats the Panel decided to award $7,500 for this report and an additional $1,000 patch bonus. Nice one! 

### na...@google.com (2020-03-03)

[Empty comment from Monorail migration]

### da...@davidmanouchehri.com (2020-03-05)

Now I regret not providing patches for my previous tickets. =P 

Could I have a CVE for this one too? =) 

### ad...@chromium.org (2020-03-05)

This will get a CVE when it's released and credited in the release notes. Thanks for the report!

### mm...@google.com (2020-03-10)

shrekshao@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-03-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-03-16)

[Comment Deleted]

### go...@chromium.org (2020-03-16)

Changing it back to Merge-Review-80 as we're hitting merge conflict. 

Taking adetaylor@'s input. Can we just skip for M80?

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/01360ded829865a6ffc3cf3c25b1f2a109fa87d7

commit 01360ded829865a6ffc3cf3c25b1f2a109fa87d7
Author: shrekshao <shrekshao@google.com>
Date: Mon Mar 16 18:25:33 2020

Verify if the context is still available.

Resolve conflict manually with git-drover

Bug: 1051748
Change-Id: I6bbef3ef50930048984593270fbe39a59a6d61f3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2053167
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Auto-Submit: David Manouchehri <david@davidmanouchehri.com>
Cr-Commit-Position: refs/heads/master@{#742401}
(cherry picked from commit 54454ec7fbcbd043f7eafea03049e53ccec5e04f)


TBR=kbr@chromium.org

Change-Id: I76fb4fea4a0f34b45ca425df353b36efe66f4708
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2104990
Reviewed-by: Shrek Shao <shrekshao@google.com>
Commit-Queue: Shrek Shao <shrekshao@google.com>
Cr-Commit-Position: refs/branch-heads/3987_137@{#14}
Cr-Branched-From: 55c16ce255e7a7feca588abeb4f082026b35e1ef-refs/branch-heads/3987@{#989}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/01360ded829865a6ffc3cf3c25b1f2a109fa87d7/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### go...@chromium.org (2020-03-17)

Approving merge to M80 branch 3987, please merge ASAP. Thank you.

### go...@chromium.org (2020-03-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7361a8e5073fdf9bf6b102991485efe59ce4bb23

commit 7361a8e5073fdf9bf6b102991485efe59ce4bb23
Author: shrekshao <shrekshao@google.com>
Date: Tue Mar 17 04:05:24 2020

[M80 merge] Verify if the context is still available.

Bug: 1051748
Change-Id: I6bbef3ef50930048984593270fbe39a59a6d61f3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2053167
Reviewed-by: Shrek Shao <shrekshao@google.com>
Reviewed-by: Kenneth Russell <kbr@chromium.org>
Commit-Queue: Kenneth Russell <kbr@chromium.org>
Auto-Submit: David Manouchehri <david@davidmanouchehri.com>
Cr-Commit-Position: refs/heads/master@{#742401}
(cherry picked from commit 54454ec7fbcbd043f7eafea03049e53ccec5e04f)


TBR=kbr@chromium.org

Change-Id: I34b3b6db1f1668012ab7cfd6c787b6a3ba5fec72
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2106751
Reviewed-by: Shrek Shao <shrekshao@google.com>
Commit-Queue: Shrek Shao <shrekshao@google.com>
Cr-Commit-Position: refs/branch-heads/3987@{#1014}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/7361a8e5073fdf9bf6b102991485efe59ce4bb23/third_party/blink/renderer/modules/webgl/webgl_rendering_context_base.cc


### ad...@google.com (2020-03-17)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-03-17)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-03-19)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1051748?no_tracker_redirect=1

[Multiple monorail components: Blink>WebGL, Blink>Workers]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051513)*
