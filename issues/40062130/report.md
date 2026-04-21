# Security: UAF in MojoQueryQuotaIpcz

| Field | Value |
|-------|-------|
| **Issue ID** | [40062130](https://issues.chromium.org/issues/40062130) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Mojo |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ss...@gmail.com |
| **Assignee** | ro...@google.com |
| **Created** | 2022-12-08 |
| **Bounty** | $30,000.00 |

## Description

**VULNERABILITY DETAILS**  

An IPC Endpoint is wrapped as `MojoHandle` while passing to Mojo `Connector` from the low-level Mojo Core. In Mojo Core, the `MojoHandle` is a counter number used to fetch the `Dispatcher` from a global map.

Things get more interesting when the low-level Mojo Core is switched to Ipcz. The IPC Endpoints in Ipcz are managed by `Portal` and the `MojoHandle` wraps the raw pointer of `Portal` with a [forced cast](https://source.chromium.org/chromium/chromium/src/+/main:third_party/ipcz/src/ipcz/api_object.h;drc=da5cd04508573976a35a81780ef12f57bfc9bee9;l=46).

The `MojoHandle` may be wrapped and passed to `Connector` as [message\_pipe\_](https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/bindings/connector.h;drc=d387f092f963cdceb9568d3a589686f7cf0e5986;l=303) and the `message_pipe_` is passed to [quota\_checker\_](https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/bindings/lib/connector.cc;drc=fcc13b7aa51f368288cef07876d95567a0e16125;l=406) but never got cleared :)

In `Connector::HandleError`, the `message_pipe_.reset` is invoked synchronously(which may free the `Portal`) if `force_pipe_reset` is true and the destruction of `InterfaceEndpointClient` is deferred if `force_async_handler` is true. The call to `MultiplexRouter::RaiseErrorInNonTestingMode` in `MultiplexRouter::ProcessIncomingMessage`(e.g. Validation error while accepting Mojo Call) will hit this situation.

Thus a UAF may occur if we still use the `message_pipe_` in `quota_checker_` before the destruction of InterfaceEndpointClient.

One example is an asynchronous Mojo Call expect the response and the response is deferred. The POC use [Annotate.AnnotateImage](https://source.chromium.org/chromium/chromium/src/+/main:services/image_annotation/public/mojom/image_annotation.mojom;drc=098756533733ea50b2dcb1c40d9a9e18d49febbe;l=66), the response callback is deferred when [ImageProcessor.GetJpgImageData](https://source.chromium.org/chromium/chromium/src/+/main:services/image_annotation/public/mojom/image_annotation.mojom;drc=098756533733ea50b2dcb1c40d9a9e18d49febbe;l=13) is responded from the Renderer.

The issue is introduced in 2019 when the `MojoRecordUnreadMessageCount` landed but only result in UAF when Ipcz is introduced.

**VERSION**  

Operating System: Ubuntu 22.04  

Commit Id: [dev] 4f40d66e66edb1c1c7dd00d83e09ff7ab89081cf

**REPRODUCTION CASE**  

To reproduce:  

1. A http server with `poc.html` and `mojo js bindings`  

2. ./chrome --enable-blink-features=MojoJS --enable-features=MojoIpcz,"MojoRecordUnreadMessageCount<Study" --force-fieldtrials=Study/Group1 --force-fieldtrial-params=Study.Group1:SampleRate/1 <http://localhost/index.html>

The creation of `quota_checker_` need `MojoRecordUnreadMessageCount` to be enabled.

The field trial parameters are set for a more stable reproduction. Without the parameter, we could spray more IPC connection for a stable reproduction since the sample rate is 1% by default.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see `asan.log`

**CREDIT INFORMATION**  

Reporter credit: avaue at S.S.L.

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 40.5 KB)
- [poc.html](attachments/poc.html) (text/plain, 1.1 KB)
- [fix.diff](attachments/fix.diff) (text/plain, 1.2 KB)

## Timeline

### [Deleted User] (2022-12-08)

[Empty comment from Monorail migration]

### ss...@gmail.com (2022-12-08)

The fix should clear the `message_pipe_` passed to `quota_checker_` in [Connector::CancelWait](https://source.chromium.org/chromium/chromium/src/+/main:mojo/public/cpp/bindings/lib/connector.cc;drc=fcc13b7aa51f368288cef07876d95567a0e16125;l=650).

See the attachment `fix.diff` above.

### cl...@chromium.org (2022-12-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5339964167618560.

### ad...@google.com (2022-12-09)

 With main version f8f598a80cb94aade1a73bcc94f0503eab859143, position 1080860, using the following gn args and ninja command:

is_component_build = false
is_asan = true
use_goma = true
use_libfuzzer = true
is_debug = false
symbol_level = 2
dcheck_always_on = true
enable_ipc_fuzzer = true

autoninja -C out/ASAN/ services/image_annotation/public/mojom:mojom_js chrome mojo/public/js:bindings

I get:

$ out/ASAN/chrome --enable-blink-features=MojoJS --enable-features=MojoIpcz,"MojoRecordUnreadMessageCount<Study" --force-fieldtrials=Study/Group1 --force-fieldtrial-params=Study.Group1:SampleRate/1 http://localhost:8000/poc.html
[22447:22475:1209/154713.884948:FATAL:message_quota_checker.cc(158)] Check failed: MOJO_RESULT_OK == rv (0 vs. 12)
    #0 0x55f55d3b89b7 in __interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4434
    #1 0x55f55d3b89b7 in __interceptor_crypt /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:10194
    #2 0x55f57466223a in base::debug::CollectStackTrace(void**, unsigned long) ./../../base/debug/stack_trace_posix.cc:894
    #3 0x55f5742d45cd in StackTrace ./../../base/debug/stack_trace.cc:221
    #4 0x55f5742d45cd in StackTrace ./../../base/debug/stack_trace.cc:218
    #5 0x55f57433781d in ~LogMessage ./../../base/logging.cc:718
    #6 0x55f57433a1e8 in ~LogMessage ./../../base/logging.cc:712
    #7 0x55f57530bad7 in mojo::internal::MessageQuotaChecker::SetMessagePipe(mojo::MessagePipeHandle) ./../../mojo/public/cpp/bindings/lib/message_quota_checker.cc:158
    #8 0x55f5752db857 in mojo::Connector::SetMessageQuotaChecker(scoped_refptr<mojo::internal::MessageQuotaChecker>) ./../../mojo/public/cpp/bindings/lib/connector.cc:406
    #9 0x55f57530ea8f in MultiplexRouter ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:394
    #10 0x55f57530dd8d in scoped_refptr<mojo::internal::MultiplexRouter> base::MakeRefCounted<mojo::internal::MultiplexRouter, base::PassKey<mojo::internal::MultiplexRouter>, mojo::ScopedHandleBase<mojo::MessagePipeHandle>, mojo::internal::MultiplexRouter::Config&, bool&, scoped_refptr<base::SequencedTaskRunner>&, char const*&>(base::PassKey<mojo::internal::MultiplexRouter>&&, mojo::ScopedHandleBase<mojo::MessagePipeHandle>&&, mojo::internal::MultiplexRouter::Config&, bool&, scoped_refptr<base::SequencedTaskRunner>&, char const*&) ./../../base/memory/scoped_refptr.h:154
    #11 0x55f57530dd8d in mojo::internal::MultiplexRouter::Create(mojo::ScopedHandleBase<mojo::MessagePipeHandle>, mojo::internal::MultiplexRouter::Config, bool, scoped_refptr<base::SequencedTaskRunner>, char const*) ./../../mojo/public/cpp/bindings/lib/multiplex_router.cc:350
    #12 0x55f57530911b in mojo::internal::InterfacePtrStateBase::InitializeEndpointClient(bool, bool, bool, std::Cr::unique_ptr<mojo::MessageReceiver, std::Cr::default_delete<mojo::MessageReceiver> >, char const*, unsigned int (*(*)(mojo::Message&))(), char const* (*)(mojo::Message&)) ./../../mojo/public/cpp/bindings/lib/interface_ptr_state.cc:104
    #13 0x55f56c346e68 in mojo::internal::InterfacePtrState<memory_instrumentation::mojom::ClientProcess>::ConfigureProxyIfNecessary() ./../../mojo/public/cpp/bindings/lib/interface_ptr_state.h:266
    #14 0x55f56c346a16 in mojo::internal::InterfacePtrState<memory_instrumentation::mojom::ClientProcess>::instance() ./../../mojo/public/cpp/bindings/lib/interface_ptr_state.h:144
    #15 0x55f56c346a16 in mojo::Remote<memory_instrumentation::mojom::ClientProcess>::Bind(mojo::PendingRemote<memory_instrumentation::mojom::ClientProcess>, scoped_refptr<base::SequencedTaskRunner>) ./../../mojo/public/cpp/bindings/remote.h:289
    #16 0x55f56c33a2a8 in Remote ./../../mojo/public/cpp/bindings/remote.h:81
    #17 0x55f56c33a2a8 in Remote ./../../mojo/public/cpp/bindings/remote.h:73
    #18 0x55f56c33a2a8 in memory_instrumentation::CoordinatorImpl::RegisterClientProcess(mojo::PendingReceiver<memory_instrumentation::mojom::Coordinator>, mojo::PendingRemote<memory_instrumentation::mojom::ClientProcess>, memory_instrumentation::mojom::ProcessType, int, absl::optional<std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char> > > const&) ./../../services/resource_coordinator/memory_instrumentation/coordinator_impl.cc:110
    #19 0x55f56b6a46c8 in content::InitializeBrowserMemoryInstrumentationClient() ./../../content/browser/tracing/memory_instrumentation_util.cc:27
    #20 0x55f5603fe8da in void base::internal::FunctorTraits<void (*)(), void>::Invoke<void (*)()>(void (*&&)()) ./../../base/functional/bind_internal.h:561
    #21 0x55f5603fe8da in void base::internal::InvokeHelper<false, void>::MakeItSo<void (*)(), std::Cr::tuple<>>(void (*&&)(), std::Cr::tuple<>&&) ./../../base/functional/bind_internal.h:850
    #22 0x55f5603fe8da in void base::internal::Invoker<base::internal::BindState<void (*)()>, void ()>::RunImpl<void (*)(), std::Cr::tuple<>>(void (*&&)(), std::Cr::tuple<>&&, std::Cr::integer_sequence<unsigned long>) ./../../base/functional/bind_internal.h:944
    #23 0x55f5603fe8da in base::internal::Invoker<base::internal::BindState<void (*)()>, void ()>::RunOnce(base::internal::BindStateBase*) ./../../base/functional/bind_internal.h:895
    #24 0x55f5744d0bdc in base::OnceCallback<void ()>::Run() && ./../../base/functional/callback.h:152
    #25 0x55f5744d0bdc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task_annotator.cc:156
    #26 0x55f57455ce72 in void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_0>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_0&&) ./../../base/task/common/task_annotator.h:85
    #27 0x55f57455ce72 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:472
    #28 0x55f57455abe2 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:323
    #29 0x55f57455ed6f in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:?
    #30 0x55f574362d85 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) ./../../base/message_loop/message_pump_default.cc:48
    #31 0x55f5745600ae in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:632
    #32 0x55f5744304da in base::RunLoop::Run(base::Location const&) ./../../base/run_loop.cc:141
    #33 0x55f5745f91e6 in base::Thread::Run(base::RunLoop*) ./../../base/threading/thread.cc:344
    #34 0x55f5745f9af4 in base::Thread::ThreadMain() ./../../base/threading/thread.cc:414
    #35 0x55f5746b5f97 in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:103
    #36 0x7fbe04e8784a in start_thread ./nptl/pthread_create.c:442
    #37 0x7fbe04f0b0ac in clone3 ./misc/../sysdeps/unix/sysv/linux/x86_64/clone3.S:81
Task trace:
    #0 0x55f56b6a476f in content::InitializeBrowserMemoryInstrumentationClient() ./../../content/browser/tracing/memory_instrumentation_util.cc:19
Crash keys:
  "num-experiments" = "0"
  "switch-5" = "http://localhost:8000/poc.html"
  "switch-4" = "--force-fieldtrial-params=Study.Group1:SampleRate/1"
  "switch-3" = "--force-fieldtrials=Study/Group1"
  "switch-2" = "--enable-features=MojoIpcz,MojoRecordUnreadMessageCount<Study"
  "switch-1" = "--enable-blink-features=MojoJS"
  "num-switches" = "5"
  "osarch" = "x86_64"
  "pid" = "22447"
  "ptype" = "browser"

[1209/154713.903134:ERROR:file_io_posix.cc(144)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_cur_freq: No such file or directory (2)
[1209/154713.903261:ERROR:file_io_posix.cc(144)] open /sys/devices/system/cpu/cpu0/cpufreq/scaling_max_freq: No such file or directory (2)
Trace/breakpoint trap



### ad...@google.com (2022-12-09)

Forcing dcheck_always_on to false in the gn args I instead sometimes get:

[87733:87733:1209/160021.728588:ERROR:validation_errors.cc(106)] Invalid message: VALIDATION_ERROR_UNEXPECTED_INVALID_HANDLE (invalid field 3)
[87733:87733:1209/160021.728659:ERROR:render_process_host_impl.cc(5229)] Terminating render process for bad Mojo message: Received bad user message: Validation failed for image_annotation.mojom.Annotator [VALIDATION_ERROR_UNEXPECTED_INVALID_HANDLE (invalid field 3)]
[87733:87733:1209/160021.728721:ERROR:bad_message.cc(29)] Terminating renderer for bad IPC message, reason 123

but sometimes I get a UaF as described.

I assume this could allow browser process memory corruption driven from a compromised renderer, so rating as High severity. Given that the reporter says ipcz is at a 1% experiment, I assume this does impact real users.

[Monorail components: Internals>Mojo]

### ad...@google.com (2022-12-09)

Reproduced with 109 as well. But, for some reason I can't reproduce this with 108 (27d3765d341b09369006d030f83f582a29eb57ae) - maybe that's because the ipcz field trials don't apply back in 108? So, setting FoundIn-109.

### [Deleted User] (2022-12-09)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-09)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2022-12-09)

This can only occur if the "MojoRecordUnreadMessageCount" study is also active, which is never active in production (there's no Finch for it and no intent to spin one up). We can probably remove the whole feature.

### gi...@appspot.gserviceaccount.com (2022-12-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7308d4b6162df4e03024e74590f1100308b70309

commit 7308d4b6162df4e03024e74590f1100308b70309
Author: Ken Rockot <rockot@google.com>
Date: Tue Dec 13 06:35:56 2022

Mojo: Remove MessageQuotaChecker

This is effectively dead code, enabled only by feature flags which must
be manually enabled and which were added for investigations that are
no longer being done. The feature flags are also removed.

Fixed: 1399511
Change-Id: I3e6462c728c1ee39848670a2bff4f29be61f1865
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4093879
Reviewed-by: Oksana Zhuravlova <oksamyt@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Commit-Queue: Ken Rockot <rockot@google.com>
Reviewed-by: Zhenyao Mo <zmo@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1082320}

[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_factory.cc
[delete] https://crrev.com/6fa0640287a27a1911d4eb319b676ab10414082f/mojo/public/cpp/bindings/tests/message_quota_checker_unittest.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_factory.h
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/gpu/ipc/client/gpu_channel_host.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/mojo/public/cpp/bindings/lib/connector.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_mojo.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_proxy.h
[delete] https://crrev.com/6fa0640287a27a1911d4eb319b676ab10414082f/mojo/public/cpp/bindings/lib/message_quota_checker.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/mojo/public/cpp/bindings/BUILD.gn
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_proxy.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_common.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_channel_mojo.h
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_mojo_bootstrap.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/mojo/public/cpp/bindings/lib/multiplex_router.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/content/common/child_process_host_impl.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/mojo/public/cpp/bindings/connector.h
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_test_base.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_mojo_bootstrap.h
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/ipc/ipc_mojo_bootstrap_unittest.cc
[modify] https://crrev.com/7308d4b6162df4e03024e74590f1100308b70309/mojo/public/cpp/bindings/tests/BUILD.gn
[delete] https://crrev.com/6fa0640287a27a1911d4eb319b676ab10414082f/mojo/public/cpp/bindings/lib/message_quota_checker.h


### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-13)

Requesting merge to beta M109 because latest trunk commit (1082320) appears to be after beta branch point (1070088).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-14)

Merge review required: M109 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-19)

Based on https://crbug.com/chromium/1399511#c10 "This can only occur if the "MojoRecordUnreadMessageCount" study is also active, which is never active in production (there's no Finch for it and no intent to spin one up)." updating this as SI-None this does not appear to impact production, thus no merge is required here. (RIP all the repro work adetaylor@ put in above 🫡 ) 

### [Deleted User] (2022-12-19)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-04)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-04)

Congratulations, S.S.L. Team! The VRP Panel has decided to award you $30,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### am...@google.com (2023-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1399511?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### dx...@google.com (2025-10-27)

Project: chromium/src  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7082508>

Remove MojoRecordUnreadMessageCount base::Feature entry

---


Expand for full commit details
```
     
    This entry is leftover from the code deletion in 
    https://crrev.com/1082320. With this entry gone, 
    mojo/public/cpp/bindings/features.* are empty and can be deleted as 
    well. 
     
    Bug: 40062130 
    Change-Id: I8d5d62d8dc16c249b655b42c3bc6edd168b7817a 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7082508 
    Reviewed-by: Andrea Orru <andreaorru@chromium.org> 
    Auto-Submit: Lei Zhang <thestig@chromium.org> 
    Reviewed-by: Nate Fischer <ntfschr@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1536117}

```

---

Files:

- M `android_webview/browser/aw_field_trials.cc`
- M `ipc/ipc_channel_unittest.cc`
- M `ipc/ipc_mojo_bootstrap.cc`
- M `mojo/golden/generated/c++/basic_struct.test-mojom.cc.golden`
- M `mojo/golden/generated/c++/basic_union.test-mojom.cc.golden`
- M `mojo/golden/generated/c++/interface.test-mojom.cc.golden`
- M `mojo/golden/generated/c++/optional_primitives.test-mojom.cc.golden`
- M `mojo/golden/generated/c++/results.test-mojom.cc.golden`
- M `mojo/golden/generated/c++/typemap.test-mojom.cc.golden`
- M `mojo/public/cpp/bindings/BUILD.gn`
- D `mojo/public/cpp/bindings/features.cc`
- D `mojo/public/cpp/bindings/features.h`
- M `mojo/public/cpp/bindings/lib/multiplex_router.cc`
- M `mojo/public/cpp/bindings/tests/associated_interface_unittest.cc`
- M `mojo/public/tools/bindings/generators/cpp_templates/module.cc.tmpl`

---

Hash: [31418085d7b889004bbf011226e91061de5d9a43](https://chromiumdash.appspot.com/commit/31418085d7b889004bbf011226e91061de5d9a43)  

Date: Mon Oct 27 18:27:42 2025


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062130)*
