# Security: UAF IN video_capture::VideoSourceImpl::OnClientDisconnected() services/video_capture/video_source_impl.cc:88:14

| Field | Value |
|-------|-------|
| **Issue ID** | [40061705](https://issues.chromium.org/issues/40061705) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Media>CameraCapture |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | zh...@intel.com |
| **Created** | 2022-11-11 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF IN video\_capture::VideoSourceImpl::OnClientDisconnected() services/video\_capture/video\_source\_impl.cc:88:14

**VERSION**

Reproduce  

The problem was found by my fuzzer running on CF(CC Security team for access permission <https://clusterfuzz.com/testcase-detail/5927304757968896>)  

It cannot be reproduced stably, CF may not automatically report.

RCA

1. VideoSourceImpl owns device\_ through a raw\_ptr, but doesn't properly observe its lifetime
2. If device\_ is freed it will cause VideoSourceImpl to trigger a security issue when accessed
3. device\_ may get freed when OnClientDisconnected get call[1]

```
void VideoSourceImpl::OnClientDisconnected() {  
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);  
  
  // Stop |device_| when lose connection with VideoSourceImpl client.  
  if (device_)  
    device_->StopInProcess();					<<\*\*\*[1]\*\*\*  
  
  if (receivers_.empty()) {  
    // Note: Invoking this callback may synchronously trigger the destruction of  
    // |this|, so no more member access should be done after it.  
    on_last_binding_closed_cb_.Run();  
  }  
}  

```
# ASAN

==751187==ERROR: AddressSanitizer: SEGV on unknown address (pc 0x55abd3c8ecd2 bp 0x7ffe3f6598b0 sp 0x7ffe3f659840 T0)  

==751187==The signal is caused by a READ memory access.  

==751187==Hint: this fault was caused by a dereference of a high value address (see register values below). Disassemble the provided pc to learn which register was used.  

SCARINESS: 20 (wild-addr-read)  

#0 0x55abd3c8ecd2 in video\_capture::VideoSourceImpl::OnClientDisconnected() services/video\_capture/video\_source\_impl.cc:88:14  

#1 0x55abd3c91a6f in Invoke<void (video\_capture::VideoSourceImpl::\*)(), video\_capture::VideoSourceImpl \*> base/functional/bind\_internal.h:646:12  

#2 0x55abd3c91a6f in MakeItSo<void (video\_capture::VideoSourceImpl::\*const &)(), const std::Cr::tuple<base::internal::UnretainedWrapper<video\_capture::VideoSourceImpl, base::RawPtrBanDanglingIfSupported> > &> base/functional/bind\_internal.h:825:12  

#3 0x55abd3c91a6f in RunImpl<void (video\_capture::VideoSourceImpl::\*const &)(), const std::Cr::tuple<base::internal::UnretainedWrapper<video\_capture::VideoSourceImpl, base::RawPtrBanDanglingIfSupported> > &, 0UL> base/functional/bind\_internal.h:919:12  

#4 0x55abd3c91a6f in base::internal::Invoker<base::internal::BindState<void (video\_capture::VideoSourceImpl::\*)(), base::internal::UnretainedWrapper<video\_capture::VideoSourceImpl, base::RawPtrBanDanglingIfSupported>>, void ()>::Run(base::internal::BindStateBase\*) base/functional/bind\_internal.h:883:12  

#5 0x55abda717bee in Run base/functional/callback.h:309:12  

#6 0x55abda717bee in mojo::ReceiverSetState::OnDisconnect(unsigned long, unsigned int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&) mojo/public/cpp/bindings/receiver\_set.cc:168:25  

#7 0x55abda7191a6 in Invoke<void (mojo::ReceiverSetState::Entry::\*)(unsigned int, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &), mojo::ReceiverSetState::Entry \*, unsigned int, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &> base/functional/bind\_internal.h:646:12  

#8 0x55abda7191a6 in MakeItSo<void (mojo::ReceiverSetState::Entry::\*const &)(unsigned int, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::ReceiverSetState::Entry, base::RawPtrBanDanglingIfSupported> > &, unsigned int, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &> base/functional/bind\_internal.h:825:12  

#9 0x55abda7191a6 in RunImpl<void (mojo::ReceiverSetState::Entry::\*const &)(unsigned int, const std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char> > &), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::ReceiverSetState::Entry, base::RawPtrBanDanglingIfSupported> > &, 0UL> base/functional/bind\_internal.h:919:12  

#10 0x55abda7191a6 in base::internal::Invoker<base::internal::BindState<void (mojo::ReceiverSetState::Entry::\*)(unsigned int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&), base::internal::UnretainedWrapper<mojo::ReceiverSetState::Entry, base::RawPtrBanDanglingIfSupported>>, void (unsigned int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&)>::Run(base::internal::BindStateBase\*, unsigned int, std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&) base/functional/bind\_internal.h:883:12  

#11 0x55abda6dc933 in Run base/functional/callback.h:174:12  

#12 0x55abda6dc933 in mojo::InterfaceEndpointClient::NotifyError(absl::optional[mojo::DisconnectReason](javascript:void(0);) const&) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:736:45  

#13 0x55abda6fd607 in mojo::internal::MultiplexRouter::ProcessNotifyErrorTask(mojo::internal::MultiplexRouter::Task\*, mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:1016:13  

#14 0x55abda6f562a in mojo::internal::MultiplexRouter::ProcessTasks(mojo::internal::MultiplexRouter::ClientCallBehavior, base::SequencedTaskRunner\*) mojo/public/cpp/bindings/lib/multiplex\_router.cc:929:15  

#15 0x55abda6f1682 in mojo::internal::MultiplexRouter::OnPipeConnectionError(bool) mojo/public/cpp/bindings/lib/multiplex\_router.cc:839:3  

#16 0x55abda702c21 in Invoke<void (mojo::internal::MultiplexRouter::\*)(bool), mojo::internal::MultiplexRouter \*, bool> base/functional/bind\_internal.h:646:12  

#17 0x55abda702c21 in MakeItSo<void (mojo::internal::MultiplexRouter::\*)(bool), std::Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::RawPtrBanDanglingIfSupported>, bool> > base/functional/bind\_internal.h:825:12  

#18 0x55abda702c21 in RunImpl<void (mojo::internal::MultiplexRouter::\*)(bool), std::Cr::tuple<base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::RawPtrBanDanglingIfSupported>, bool>, 0UL, 1UL> base/functional/bind\_internal.h:919:12  

#19 0x55abda702c21 in base::internal::Invoker<base::internal::BindState<void (mojo::internal::MultiplexRouter::\*)(bool), base::internal::UnretainedWrapper<mojo::internal::MultiplexRouter, base::RawPtrBanDanglingIfSupported>, bool>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:870:12  

#20 0x55abda6ceca2 in Run base/functional/callback.h:174:12  

#21 0x55abda6ceca2 in mojo::Connector::HandleError(bool, bool) mojo/public/cpp/bindings/lib/connector.cc:688:44  

#22 0x55abda6d31f3 in Invoke<void (mojo::Connector::\*)(unsigned int), mojo::Connector \*, unsigned int> base/functional/bind\_internal.h:646:12  

#23 0x55abda6d31f3 in MakeItSo<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::RawPtrBanDanglingIfSupported> > &, unsigned int> base/functional/bind\_internal.h:825:12  

#24 0x55abda6d31f3 in RunImpl<void (mojo::Connector::\*const &)(unsigned int), const std::Cr::tuple<base::internal::UnretainedWrapper<mojo::Connector, base::RawPtrBanDanglingIfSupported> > &, 0UL> base/functional/bind\_internal.h:919:12  

#25 0x55abda6d31f3 in base::internal::Invoker<base::internal::BindState<void (mojo::Connector::\*)(unsigned int), base::internal::UnretainedWrapper<mojo::Connector, base::RawPtrBanDanglingIfSupported>>, void (unsigned int)>::Run(base::internal::BindStateBase\*, unsigned int) base/functional/bind\_internal.h:883:12  

#26 0x55abcde528bf in Run base/functional/callback.h:309:12  

#27 0x55abcde528bf in mojo::SimpleWatcher::DiscardReadyState(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.h:192:14  

#28 0x55abcde52aa5 in Invoke<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind\_internal.h:536:12  

#29 0x55abcde52aa5 in MakeItSo<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, unsigned int, const mojo::HandleSignalsState &> base/functional/bind\_internal.h:825:12  

#30 0x55abcde52aa5 in RunImpl<void (\*const &)(const base::RepeatingCallback<void (unsigned int)> &, unsigned int, const mojo::HandleSignalsState &), const std::Cr::tuple<base::RepeatingCallback<void (unsigned int)> > &, 0UL> base/functional/bind\_internal.h:919:12  

#31 0x55abcde52aa5 in base::internal::Invoker<base::internal::BindState<void (\*)(base::RepeatingCallback<void (unsigned int)> const&, unsigned int, mojo::HandleSignalsState const&), base::RepeatingCallback<void (unsigned int)>>, void (unsigned int, mojo::HandleSignalsState const&)>::Run(base::internal::BindStateBase\*, unsigned int, mojo::HandleSignalsState const&) base/functional/bind\_internal.h:883:12  

#32 0x55abda74a8d6 in Run base/functional/callback.h:309:12  

#33 0x55abda74a8d6 in mojo::SimpleWatcher::OnHandleReady(int, unsigned int, mojo::HandleSignalsState const&) mojo/public/cpp/system/simple\_watcher.cc:278:14  

#34 0x55abda74b96c in Invoke<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> base/functional/bind\_internal.h:646:12  

#35 0x55abda74b96c in MakeItSo<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState> > base/functional/bind\_internal.h:847:5  

#36 0x55abda74b96c in RunImpl<void (mojo::SimpleWatcher::\*)(int, unsigned int, const mojo::HandleSignalsState &), std::Cr::tuple<base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, 0UL, 1UL, 2UL, 3UL> base/functional/bind\_internal.h:919:12  

#37 0x55abda74b96c in base::internal::Invoker<base::internal::BindState<void (mojo::SimpleWatcher::\*)(int, unsigned int, mojo::HandleSignalsState const&), base::WeakPtr[mojo::SimpleWatcher](javascript:void(0);), int, unsigned int, mojo::HandleSignalsState>, void ()>::RunOnce(base::internal::BindStateBase\*) base/functional/bind\_internal.h:870:12  

#38 0x55abd9c08519 in Run base/functional/callback.h:174:12  

#39 0x55abd9c08519 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/task/common/task\_annotator.cc:154:32  

#40 0x55abd9c4e92c in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:450:11)> base/task/common/task\_annotator.h:84:5  

#41 0x55abd9c4e92c in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:448:23  

#42 0x55abd9c4d8da in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:299:30  

#43 0x55abd9c4fd94 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0  

#44 0x55abd9b08853 in base::MessagePumpDefault::Run(base::MessagePump::Delegate\*) base/message\_loop/message\_pump\_default.cc:40:55  

#45 0x55abd9c508cd in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:608:12  

#46 0x55abd9b94fee in base::RunLoop::Run(base::Location const&) base/run\_loop.cc:141:14  

#47 0x55abd5a468e9 in content::UtilityMain(content::MainFunctionParams) content/utility/utility\_main.cc:305:12  

#48 0x55abd897cc77 in content::RunOtherNamedProcessTypeMain(std::Cr::basic\_string<char, std::Cr::char\_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate\*) content/app/content\_main\_runner\_impl.cc:733:14  

#49 0x55abd897f02d in content::ContentMainRunnerImpl::Run() content/app/content\_main\_runner\_impl.cc:1085:10  

#50 0x55abd897790d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content/app/content\_main.cc:342:36  

#51 0x55abd8977f19 in content::ContentMain(content::ContentMainParams) content/app/content\_main.cc:370:10  

#52 0x55abc97a5ead in ChromeMain chrome/app/chrome\_main.cc:174:12  

#53 0x7f175741a082 in \_\_libc\_start\_main /build/glibc-SzIz7B/glibc-2.31/csu/libc-start.c:308:16  

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (/mnt/scratch0/clusterfuzz/bot/builds/chromium-browser-asan\_linux-release\_4392242b7f59878a2775b4607420a2b37e17ff13/revisions/asan-linux-release-1069727/chrome+0x16449cd2) (BuildId: a8e638f7e6b3a020)  

==751187==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 11.8 KB)

## Timeline

### m....@gmail.com (2022-11-11)

#Bitset
Introduce by this CL
https://chromium-review.googlesource.com/c/chromium/src/+/3975332

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-11)

Thanks for report. Surprised device_ is not null? it is a wild pointer here? Perhaps just nulling it would help?

I'm adding the relevant teams and will also work on a repro, although CF seems to have already reproduced.

[Monorail components: Internals>Media>CameraCapture]

### [Deleted User] (2022-11-11)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-11)

also, no free stack from asan. that's odd. Do you know what is freeing the device_?

this service seems to run unsandboxed on multiple platforms https://source.chromium.org/chromium/chromium/src/+/main:services/video_capture/public/mojom/video_capture_service.mojom;l=32

so this might be a critical, but the flakiness and lack of consistent reproducibility just bumps it down to High in my view.

### wf...@chromium.org (2022-11-11)

Assigning an owner.

### m....@gmail.com (2022-11-12)

I think the root cause of the issue is incorrect use of raw_ptr( assign raw_ptr<T> memory directly)[1].

https://source.chromium.org/chromium/chromium/src/+/main:services/video_capture/video_source_impl.cc;drc=5a691c7c1c46421b2fa7ff3cd3b5f79470ed3808;l=124
```
void VideoSourceImpl::OnCreateDeviceResponse(
    std::unique_ptr<ScopedCaptureTrace> scoped_trace,
    DeviceInProcessInfo info) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(sequence_checker_);

  if (info.result_code == media::VideoCaptureError::kNone) {
    if (scoped_trace)
      scoped_trace->AddStep("StartDevice");

    // Device was created successfully.
    device_ = info.device;<<***1***
```

Reading raw_ptr.md you can see that this usage is explicitly forbidden because it will result in undefined behavior
https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md#extra-pointer-rules
```
Don’t initialize or assign raw_ptr<T> memory directly (e.g. reinterpret_cast<ClassWithRawPtr*>(buffer) or memcpy(reinterpret_cast<void*>(&obj_with_raw_ptr), buffer).
```


### [Deleted User] (2022-11-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@intel.com (2022-11-14)

I cannot repro this issue on my side, is this happened in case both DeviceFactory and VideoSourceImpl are used as mojo interface in renderer process?

### m....@gmail.com (2022-11-14)

In utility process
    #47 0x55abd5a468e9 in content::UtilityMain(content::MainFunctionParams) content/utility/utility_main.cc:305:12
    #48 0x55abd897cc77 in content::RunOtherNamedProcessTypeMain(std::Cr::basic_string<char, std::Cr::char_traits<char>, std::Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:733:14
    #49 0x55abd897f02d in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1085:10
    #50 0x55abd897790d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:342:36
    #51 0x55abd8977f19 in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:370:10
    #52 0x55abc97a5ead in ChromeMain chrome/app/chrome_main.cc:174:12

### zh...@intel.com (2022-11-14)

Hi m.cooolie@, I uploaded a patch trying fix this at https://chromium-review.googlesource.com/c/chromium/src/+/4025329, is it convenient for you to test it?

### m....@gmail.com (2022-11-14)

I can't reproduce it locally, but the patch LGTM.

### gi...@appspot.gserviceaccount.com (2022-11-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/02cdf461547f293914584f7c08eb342730f0e6ed

commit 02cdf461547f293914584f7c08eb342730f0e6ed
Author: Zhaoliang Ma <zhaoliang.ma@intel.com>
Date: Tue Nov 15 01:29:27 2022

services/video_capture: Stop Device from DeviceFactory to avoid UaF

Device should call Stop() when VideoSource remote is discarded with active PushSubscription, this CL doing this by calling DeviceFactory for safety.

Bug: 1383442, 1360658
Change-Id: If4817ee2a87c9e9c327b9921479bd7f38b7f50d4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025329
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Zhaoliang Ma <zhaoliang.ma@intel.com>
Cr-Commit-Position: refs/heads/main@{#1071375}

[modify] https://crrev.com/02cdf461547f293914584f7c08eb342730f0e6ed/services/video_capture/video_source_impl.h
[modify] https://crrev.com/02cdf461547f293914584f7c08eb342730f0e6ed/services/video_capture/video_source_impl.cc


### [Deleted User] (2022-11-28)

zhaoliang.ma: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zh...@intel.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

Requesting merge to dev M109 because latest trunk commit (1071375) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-29)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-11-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/161ba1e2eeb5fee307cfcb556c1a182220838591

commit 161ba1e2eeb5fee307cfcb556c1a182220838591
Author: Zhaoliang Ma <zhaoliang.ma@intel.com>
Date: Wed Nov 30 11:24:42 2022

[M109]services/video_capture: Stop Device from DeviceFactory to avoid UaF

Device should call Stop() when VideoSource remote is discarded with active PushSubscription, this CL doing this by calling DeviceFactory for safety.

(cherry picked from commit 02cdf461547f293914584f7c08eb342730f0e6ed)

Bug: 1383442, 1360658
Change-Id: If4817ee2a87c9e9c327b9921479bd7f38b7f50d4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4025329
Reviewed-by: Henrik Boström <hbos@chromium.org>
Commit-Queue: Zhaoliang Ma <zhaoliang.ma@intel.com>
Cr-Original-Commit-Position: refs/heads/main@{#1071375}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4064931
Commit-Queue: Henrik Boström <hbos@chromium.org>
Auto-Submit: Zhaoliang Ma <zhaoliang.ma@intel.com>
Cr-Commit-Position: refs/branch-heads/5414@{#307}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[modify] https://crrev.com/161ba1e2eeb5fee307cfcb556c1a182220838591/services/video_capture/video_source_impl.h
[modify] https://crrev.com/161ba1e2eeb5fee307cfcb556c1a182220838591/services/video_capture/video_source_impl.cc


### [Deleted User] (2022-11-30)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-11-30)

The device_->StopInProcess() call on VideoSourceImpl::OnClientDisconnected() isn't present in 102 and most of the rest of the changes aren't applicable

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $15,000 for this report + bisect bonus. Thank you for your efforts in discovering and reporting this issue to us -- great work! 

### m....@gmail.com (2022-12-09)

Thanks for reward, can I get extra fuzz bounty as issue was found by my fuzzer run on CF.

### am...@chromium.org (2022-12-09)

Hello, thanks for this question. Unfortunately, we cannot extend a fuzzer bonus for this report. The expectations around fuzzer bonuses is that the fuzzer and testcase being run on ClusterFuzz is able to automatically submit a report, including an automatic bisect, potential owner cc/ assignment, and identifying regression range (if applicable) - fairly automated triage, without human / manual intervention needed to submit the report and then to triage it.  

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-24)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-01-31)

@rzanoni, can you please evaluate for LTC-108?

### rz...@google.com (2023-02-01)

The device_->StopInProcess() call on VideoSourceImpl::OnClientDisconnected() isn't present in 108 and most of the rest of the changes aren't applicable

### rz...@google.com (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1383442?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061705)*
