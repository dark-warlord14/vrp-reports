# Security: UAF in webrtc::SctpDataChannel::SetState

| Field | Value |
|-------|-------|
| **Issue ID** | [40066280](https://issues.chromium.org/issues/40066280) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebRTC>DataChannel |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2023-06-23 |
| **Bounty** | $7,000.00 |

## Description

VULNERABILITY DETAILS
## Bisect
todo

## RCA
This is a race condition vulnerability, as indicated by ASAN LOG. The functions create/free and use are executed in two different threads, T0 and T20, respectively. T20 is an network thread created by T0 using blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory.

allocate: when chrome needs to create a new RTCDataChannel, it will execute the path [1][2] in order, and at [2] it creates RTCDataChannel::oberserver_, which is a reference-counted object.
```
RTCDataChannel* RTCPeerConnection::createDataChannel(
    ScriptState* script_state,
    String label,
    const RTCDataChannelInit* data_channel_dict,
    ExceptionState& exception_state) {
  ...

  rtc::scoped_refptr<webrtc::DataChannelInterface> webrtc_channel = // <--------------- [6]
      peer_handler_->CreateDataChannel(label, init);
  ...
  auto* channel = MakeGarbageCollected<RTCDataChannel>(     // <----------- [1]
      GetExecutionContext(), std::move(webrtc_channel), peer_handler_.get());

  return channel;
}

RTCDataChannel::RTCDataChannel(
    ExecutionContext* context,
    rtc::scoped_refptr<webrtc::DataChannelInterface> channel,
    RTCPeerConnectionHandler* peer_connection_handler)
    : ActiveScriptWrappable<RTCDataChannel>({}),
      ExecutionContextLifecycleObserver(context),
      scheduled_event_timer_(context->GetTaskRunner(TaskType::kNetworking),
                             this,
                             &RTCDataChannel::ScheduledEventTimerFired),
      observer_(base::MakeRefCounted<Observer>(                   // <--------------- [2]
          context->GetTaskRunner(TaskType::kNetworking),
          this,
          channel)),
      signaling_thread_(peer_connection_handler->signaling_thread()) {
  DCHECK(peer_connection_handler);

  // Register observer and get state update to make up for state change updates
  // that might have been missed between creating the webrtc::DataChannel object
  // on the signaling thread and RTCDataChannel construction posted on the main
  // thread. Done in a single synchronous call to the signaling thread to ensure
  // channel state consistency.
  // TODO(tommi): Check it this^ is still possible.
  channel->RegisterObserver(observer_.get());          // <----------------------- [5]
  if (channel->state() != state_) {
    observer_->OnStateChange();
  }

  IncrementCounters(*channel.get());
}
```

free: When the iframe is destroyed, RTCDataChannel::ContextDestroyed is called following the path [3][4] to reduce the reference count of the observer and cause the observer to be released.
```
void RTCDataChannel::ContextDestroyed() {
  Dispose();         // <---------- [3]
  stopped_ = true;
  state_ = webrtc::DataChannelInterface::kClosed;
  feature_handle_for_scheduler_.reset();
}
void RTCDataChannel::Dispose() {
  if (stopped_)
    return;

  // Clears the weak persistent reference to this on-heap object.
  observer_->Unregister();  
  observer_ = nullptr; // <-------- [4]
}
```

use: Although RTCDataChannel::observer_ uses reference counting to ensure that it will only be released when no object holds or uses it. However, in RTCDataChannel::RTCDataChannel [5] the original pointer to observer_, which is protected by reference counting, is registered to a DataChannelInterface object.
This DataChannelInterface object will hold the original pointer to observer_. Then if the DataChannelInterface has a longer lifecycle than the RTCDataChannel, this may result in a UAF for the observer.
The DataChannelInterface object is created at RTCPeerConnection::createDataChannel [6] and saved in the DataChannelController at [7].

```
RTCErrorOr<rtc::scoped_refptr<SctpDataChannel>>
DataChannelController::CreateDataChannel(const std::string& label,
                                         InternalDataChannelInit& config) {
  ...

  rtc::scoped_refptr<SctpDataChannel> channel = SctpDataChannel::Create(
      weak_factory_.GetWeakPtr(), label, data_channel_transport_ != nullptr,
      config, signaling_thread(), network_thread());
  RTC_DCHECK(channel);
  sctp_data_channels_n_.push_back(channel); // <-------------- [7]

  // If we have an id already, notify the transport.
  if (sid.HasValue())
    AddSctpDataStream(sid);

  return channel;
}
```

From the asan log, we can see that when the observer is destructured, there are also callbacks from [8] that will be sent to the network thread, thus using the observer and triggering the UAF.

```
void SdpOfferAnswerHandler::DestroyDataChannelTransport(RTCError error) {
  RTC_DCHECK_RUN_ON(signaling_thread());
  context_->network_thread()->BlockingCall( // <-------------- [8]
      [&, data_channel_controller = data_channel_controller()] {
        RTC_DCHECK_RUN_ON(context_->network_thread());
        pc_->TeardownDataChannelTransport_n(error);
      });
  pc_->ResetSctpDataInfo();
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;l=2039;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=289;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=510;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[4] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=668;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[5] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=302;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[6] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;l=2032;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[7] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/data_channel_controller.cc;l=296;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[8] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/sdp_offer_answer.cc;l=5169;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758

VERSION
Chrome Version:
Fuzz Test chrome commit hash 
```
commit c3b22ba646219765aaefb47d06a0398a14f507fc (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Jun 22 03:07:16 2023 +0000

    Roll Chrome Mac Arm PGO Profile

    Roll Chrome Mac Arm PGO profile from chrome-mac-arm-main-1687370140-da3ac341ee8c5099ac5106f1df07f83ee9525ced.profdata to chrome-mac-arm-main-1687377583-074b74b65b16ebdd0f90799803942b6baec87837.profdata

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pgo-mac-arm-chromium
    Please CC chrome-brapp-engprod@google.com,pgo-profile-sheriffs@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Chromium main branch: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chrome.try:mac-chrome
    Tbr: pgo-profile-sheriffs@google.com
    Change-Id: I03b7da87bc6dfafede7dd4573fe3276134d2faff
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4634530
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
```
Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction and only needs to destroy iframe to cause a use-after-free in the render process. This is likely an exploitable vulnerability.
I am unable to provide a minimized poc at this time. However, I have provided the root cause analysis and ASAN log to assist with the vulnerability fix.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: render
Crash State: see asan log

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 27.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.0 KB)
- [asan.log](attachments/asan.log) (text/plain, 27.0 KB)
- [patch.diff](attachments/patch.diff) (text/plain, 4.2 KB)

## Timeline

### [Deleted User] (2023-06-23)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-06-23)

This vulnerability was discovered by my fuzzer. Since it is a race condition vulnerability, it cannot be reproduced stably. It will be updated after I find root cause.

### ki...@gmail.com (2023-06-23)

Title: heap-use-after-free on webrtc::SctpDataChannel::SetState

VULNERABILITY DETAILS
## Bisect
todo

## RCA
This is a race condition vulnerability, as indicated by ASAN LOG. The functions create/free and use are executed in two different threads, T0 and T20, respectively. T20 is an network thread created by T0 using blink::PeerConnectionDependencyFactory::CreatePeerConnectionFactory.

allocate: when chrome needs to create a new RTCDataChannel, it will execute the path [1][2] in order, and at [2] it creates RTCDataChannel::oberserver_, which is a reference-counted object.
```
RTCDataChannel* RTCPeerConnection::createDataChannel(
    ScriptState* script_state,
    String label,
    const RTCDataChannelInit* data_channel_dict,
    ExceptionState& exception_state) {
  ...

  rtc::scoped_refptr<webrtc::DataChannelInterface> webrtc_channel = // <--------------- [6]
      peer_handler_->CreateDataChannel(label, init);
  ...
  auto* channel = MakeGarbageCollected<RTCDataChannel>(     // <----------- [1]
      GetExecutionContext(), std::move(webrtc_channel), peer_handler_.get());

  return channel;
}

RTCDataChannel::RTCDataChannel(
    ExecutionContext* context,
    rtc::scoped_refptr<webrtc::DataChannelInterface> channel,
    RTCPeerConnectionHandler* peer_connection_handler)
    : ActiveScriptWrappable<RTCDataChannel>({}),
      ExecutionContextLifecycleObserver(context),
      scheduled_event_timer_(context->GetTaskRunner(TaskType::kNetworking),
                             this,
                             &RTCDataChannel::ScheduledEventTimerFired),
      observer_(base::MakeRefCounted<Observer>(                   // <--------------- [2]
          context->GetTaskRunner(TaskType::kNetworking),
          this,
          channel)),
      signaling_thread_(peer_connection_handler->signaling_thread()) {
  DCHECK(peer_connection_handler);

  // Register observer and get state update to make up for state change updates
  // that might have been missed between creating the webrtc::DataChannel object
  // on the signaling thread and RTCDataChannel construction posted on the main
  // thread. Done in a single synchronous call to the signaling thread to ensure
  // channel state consistency.
  // TODO(tommi): Check it this^ is still possible.
  channel->RegisterObserver(observer_.get());          // <----------------------- [5]
  if (channel->state() != state_) {
    observer_->OnStateChange();
  }

  IncrementCounters(*channel.get());
}
```

free: When the iframe is destroyed, RTCDataChannel::ContextDestroyed is called following the path [3][4] to reduce the reference count of the observer and cause the observer to be released.
```
void RTCDataChannel::ContextDestroyed() {
  Dispose();         // <---------- [3]
  stopped_ = true;
  state_ = webrtc::DataChannelInterface::kClosed;
  feature_handle_for_scheduler_.reset();
}
void RTCDataChannel::Dispose() {
  if (stopped_)
    return;

  // Clears the weak persistent reference to this on-heap object.
  observer_->Unregister();  
  observer_ = nullptr; // <-------- [4]
}
```

use: Although RTCDataChannel::observer_ uses reference counting to ensure that it will only be released when no object holds or uses it. However, in RTCDataChannel::RTCDataChannel [5] the original pointer to observer_, which is protected by reference counting, is registered to a DataChannelInterface object.
This DataChannelInterface object will hold the original pointer to observer_. Then if the DataChannelInterface has a longer lifecycle than the RTCDataChannel, this may result in a UAF for the observer.
The DataChannelInterface object is created at RTCPeerConnection::createDataChannel [6] and saved in the DataChannelController at [7].

```
RTCErrorOr<rtc::scoped_refptr<SctpDataChannel>>
DataChannelController::CreateDataChannel(const std::string& label,
                                         InternalDataChannelInit& config) {
  ...

  rtc::scoped_refptr<SctpDataChannel> channel = SctpDataChannel::Create(
      weak_factory_.GetWeakPtr(), label, data_channel_transport_ != nullptr,
      config, signaling_thread(), network_thread());
  RTC_DCHECK(channel);
  sctp_data_channels_n_.push_back(channel); // <-------------- [7]

  // If we have an id already, notify the transport.
  if (sid.HasValue())
    AddSctpDataStream(sid);

  return channel;
}
```

From the asan log, we can see that when the observer is destructured, there are also callbacks from [8] that will be sent to the network thread, thus using the observer and triggering the UAF.

```
void SdpOfferAnswerHandler::DestroyDataChannelTransport(RTCError error) {
  RTC_DCHECK_RUN_ON(signaling_thread());
  context_->network_thread()->BlockingCall( // <-------------- [8]
      [&, data_channel_controller = data_channel_controller()] {
        RTC_DCHECK_RUN_ON(context_->network_thread());
        pc_->TeardownDataChannelTransport_n(error);
      });
  pc_->ResetSctpDataInfo();
}
```

[1] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;l=2039;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[2] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=289;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[3] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=510;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[4] https://source.chromium.org/chromium/chromium/src/+/refs/heads/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=668;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[5] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc;l=302;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[6] https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/peerconnection/rtc_peer_connection.cc;l=2032;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[7] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/data_channel_controller.cc;l=296;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758
[8] https://source.chromium.org/chromium/chromium/src/+/main:third_party/webrtc/pc/sdp_offer_answer.cc;l=5169;drc=afec9eaf1d11cc77e8e06f06cb026fadf0dbf758

VERSION
Chrome Version:
Fuzz Test chrome commit hash 
```
commit c3b22ba646219765aaefb47d06a0398a14f507fc (HEAD -> main, origin/main, origin/HEAD)
Author: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
Date:   Thu Jun 22 03:07:16 2023 +0000

    Roll Chrome Mac Arm PGO Profile

    Roll Chrome Mac Arm PGO profile from chrome-mac-arm-main-1687370140-da3ac341ee8c5099ac5106f1df07f83ee9525ced.profdata to chrome-mac-arm-main-1687377583-074b74b65b16ebdd0f90799803942b6baec87837.profdata

    If this roll has caused a breakage, revert this CL and stop the roller
    using the controls here:
    https://autoroll.skia.org/r/pgo-mac-arm-chromium
    Please CC chrome-brapp-engprod@google.com,pgo-profile-sheriffs@google.com on the revert to ensure that a human
    is aware of the problem.

    To file a bug in Chromium main branch: https://bugs.chromium.org/p/chromium/issues/entry

    To report a problem with the AutoRoller itself, please file a bug:
    https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

    Documentation for the AutoRoller is here:
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

    Cq-Include-Trybots: luci.chrome.try:mac-chrome
    Tbr: pgo-profile-sheriffs@google.com
    Change-Id: I03b7da87bc6dfafede7dd4573fe3276134d2faff
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4634530
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com>
```
Operating System: Windows


REPRODUCTION CASE
The vulnerability was triggered by my fuzzer, it does not require any interaction and only needs to destroy iframe to cause a use-after-free in the render process. This is likely an exploitable vulnerability.
I am unable to provide a minimized poc at this time. However, I have provided the root cause analysis and ASAN log to assist with the vulnerability fix.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: render
Crash State: see asan log

### ah...@google.com (2023-06-23)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebRTC>DataChannel]

### ah...@google.com (2023-06-23)

Hello kipreyxx@gmail.com,

Thanks for the report. Since we have no way of reproducing this on our end, could you please provide the earliest version you encountered the issue?

Thanks,

### ah...@google.com (2023-06-23)

Setting severity high as per severity guidelines regarding renderer process memory corruption.


### [Deleted User] (2023-06-23)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ah...@google.com (2023-06-23)

Hello @tommi@chromium.org
Could you please take a look and point me in the right direction if this is not on your end?
Thanks in advance,

### [Deleted User] (2023-06-23)

[Empty comment from Monorail migration]

### to...@chromium.org (2023-06-26)

orphis - could you take a look?

Looking at the code, I wonder if `blink_channel_` is being set to nullptr too early and that operation needs to be moved such that it happens _after_ `webrtc_channel_` has been cleared?

```
void RTCDataChannel::Observer::Unregister() {
  DCHECK(main_thread_->BelongsToCurrentThread());
  blink_channel_ = nullptr;
  if (webrtc_channel_.get()) {
    webrtc_channel_->UnregisterObserver();
    // Now that we're guaranteed to not get further OnStateChange callbacks,
    // it's safe to release our reference to the channel.
    webrtc_channel_ = nullptr;
  }
}
```

The call to `UnregisterObserver()` should execute synchronously and clear the observer pointer on the network thread, so from that pov I think that Unregister() is doing the right thing.

One btw comment on the design of the RTCDataChannel code is that the observer class seems to own the reference to the data channel, which again holds on to a pointer to the observer. That seems to be a circular dependency to me and makes it more difficult to reason about the logic (i.e. it's unclear that freeing the observer, indirectly releases a reference to the channel).
I don't think we should do something about it now but mentioning in case there's other work going on which we could consider if we could clarify this relationship.

### es...@chromium.org (2023-06-29)

Tentatively setting FoundIn-116 assuming this was introduced in https://chromium.googlesource.com/chromium/src/+/c3b22ba646219765aaefb47d06a0398a14f507fc as identified by the reporter. Please update this label if the bug existed before then. Thanks!

### [Deleted User] (2023-06-29)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-06-29)

Is anyone fixing this bug, thanks

### or...@chromium.org (2023-06-29)

Hi,

I tried to stresstest an ASAN build creating and destroying data channels and I haven't been able to reproduce the issue.
Could you please share a reproducible case or better detailed instructions explaining what your fuzzer is doing?

### or...@chromium.org (2023-06-29)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-06-29)

Hello, I am currently on vacation and will try to reproduce it again next week. Before that, could you please help investigate the lifecycle according to the ASAN log?

### to...@chromium.org (2023-06-30)

Thanks for the report @kipreyxx.

Do you have any local modifications?

The reason I ask is because while the statement "if the DataChannelInterface has a longer lifecycle than the RTCDataChannel, this may result in a UAF for the observer" is true, this is how the observer pointer is freed (Unregister() is called from Dispose() before setting observer_ to nullptr):

```
void RTCDataChannel::Observer::Unregister() {
  DCHECK(main_thread_->BelongsToCurrentThread());
  blink_channel_ = nullptr;
  if (webrtc_channel_.get()) {
    webrtc_channel_->UnregisterObserver();
    // Now that we're guaranteed to not get further OnStateChange callbacks,
    // it's safe to release our reference to the channel.
    webrtc_channel_ = nullptr;
  }
}
```

The implementation of UnregisterObserver() in webrtc will then effectively do this (simplified for brevity):

    network_thread_->BlockingCall([&]() {
      RTC_DCHECK_RUN_ON(network_thread_);
      observer_ = nullptr;
    });

This should ensure that the observer pointer on the network thread is set to nullptr and any pending calls that might dereference the observer pointer, have been flushed before returning back to the `main_thread_`.

### to...@chromium.org (2023-06-30)

Adding pkasting and handellm in case this might have something to do with thread_wrapper.cc changes and if there's a possibility that the UnregisterObserver() task never runs.

### ki...@gmail.com (2023-06-30)

re https://crbug.com/chromium/1457421#c17:
I used some simple modifications to avoid authorization and file selection popups during fuzzing. But I don't think it has anything to do with this vulnerability of webrtc, the attachment is patch.diff.

run cmd:
D:\project\chromium\src\out\asan-release\chrome.exe --user-data-dir=D:\project\outdir\instances\browser-17\userdata --enable-features=BrowsingTopics,Fledge,Parakeet,FencedFramesAPIChanges,PrivacySandboxAdsAPIs,AbortSignalAny,DisableVoiceMatch,ReduceToolbarUpdatesForSameDocNavigations,PerformanceControlsBatterySaverOptOutSurvey,UserMediaScreenCapturing,WebViewSurfaceControl,EnableLazyLoginWebUILoading,ArcvmSwapoutKeyboardShortcut,IPH_BadgedReadingList,ServiceWorkerStorageControlOnThreadPool --enable-blink-features=TopicsAPI,SharedStorageAPI,WebGLDraftExtensions,WebGLDeveloperExtensions,ExtraWebGLVideoTextureMetadata,WebGPU,FencedFramesDefaultMode,FencedFramesAPIChanges,LCPMouseoverHeuristics,VideoFullscreenOrientationLock,WebHIDOnServiceWorkers,NetInfoConstantType,RemotePlaybackBackend,ExtraWebGLVideoTextureMetadata,AutoplayIgnoresWebAudio,StylusHandwriting --no-sandbox --js-flags=--expose_gc --allow-natives-syntax --no-first-run --disable-in-process-stack-traces --enable-experimental-extension-apis --enable-experimental-web-platform-features --disable-translate --disable-breakpad --no-user-gesture-required --disable-gesture-requirement-for-media-playback --use-file-for-fake-audio-capture=test.wav --use-file-for-fake-video-capture=test.mjpeg --use-fake-device-for-media-stream --use-fake-ui-for-media-stream --enable-blink-test-features --allow-file-access-from-files --allow-natives-syntax --window-size=1024,768 --enable-logging=stderr --no-zygote --disable-gpu-sandbox --no-default-browser-check --disable-extensions --autoplay-policy=no-user-gesture-required --disable-kill-after-bad-ipc --deny-permission-prompts --ignore-certificate-errors-spki-list=BSQJ0jkQ7wwhR7KvPZ+DSNk2XTZ/MS6xCbo9qu++VdQ= --origin-to-force-quic-on=127.0.0.1:9002 http://127.0.0.1:8888/instance-17\fuzz-6-23_3-27-8-322945-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-34-44-128576-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-35-41-731991-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-38-15-200727-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-38-47-564803-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-39-20-280523-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-39-3-811561-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-40-0-540740-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-40-37-159882-testcase.html http://127.0.0.1:8888/instance-17\fuzz-6-23_3-40-47-625028-testcase.html

### ki...@gmail.com (2023-06-30)

Please let me know if you find anything.
I'll be back from vacation next week and try to reproduce it with the fuzzer again.

### [Deleted User] (2023-06-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-07-03)

Tentative fix: https://chromium-review.googlesource.com/c/chromium/src/+/4663082
@kipreyxx - could you try that out with your setup too?

### gi...@appspot.gserviceaccount.com (2023-07-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/08d5ad011f53a1995bfccef6728bfa62541f7608

commit 08d5ad011f53a1995bfccef6728bfa62541f7608
Author: Tommi <tommi@chromium.org>
Date: Mon Jul 03 21:04:47 2023

Make RTCDataChannel's channel and observer pointers const.

This allows channel properties to be queried while the RTCDataChannel
instance exists and avoids potential null deref after entering the
kClosed state.

Bug: 1456567, 1457421
Change-Id: I4747f9c00804b35711667d7320ec6188f20910c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4663082
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1165406}

[modify] https://crrev.com/08d5ad011f53a1995bfccef6728bfa62541f7608/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
[modify] https://crrev.com/08d5ad011f53a1995bfccef6728bfa62541f7608/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc


### ki...@gmail.com (2023-07-05)

After extensive testing, I think this vulnerability has been fixed by this patch. I will update this issue again if it is not completely fixed. And for now, please mark it as fixed and thank you for your kind efforts @tommi !


To VRP: While I noticed a null pointer dereference bug (https://crbug.com/chromium/1456567) is related with the same patch, this bug is not a security issue. And the asan log in my report identifies it as a UAF issue, which may not be able to be triggered by clusterfuzz because of the long time that has passed,  so this report should not be duplicated.

### to...@chromium.org (2023-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-05)

Merge approved: your change passed merge requirements and is auto-approved for M116. Please go ahead and merge the CL to branch 5845 (refs/branch-heads/5845) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), eakpobaro (iOS), obenedict (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-05)

Merge review required: M115 has already been cut for stable release.

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
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b0397356186229e3aab75991d48ef632bfe276af

commit b0397356186229e3aab75991d48ef632bfe276af
Author: Tommi <tommi@chromium.org>
Date: Wed Jul 05 10:55:53 2023

[M116] Make RTCDataChannel's channel and observer pointers const.

This allows channel properties to be queried while the RTCDataChannel
instance exists and avoids potential null deref after entering the
kClosed state.

(cherry picked from commit 08d5ad011f53a1995bfccef6728bfa62541f7608)

Bug: 1456567, 1457421
Change-Id: I4747f9c00804b35711667d7320ec6188f20910c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4663082
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1165406}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4665530
Cr-Commit-Position: refs/branch-heads/5845@{#300}
Cr-Branched-From: 5a5dff63a4a4c63b9b18589819bebb2566c85443-refs/heads/main@{#1160321}

[modify] https://crrev.com/b0397356186229e3aab75991d48ef632bfe276af/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
[modify] https://crrev.com/b0397356186229e3aab75991d48ef632bfe276af/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc


### [Deleted User] (2023-07-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-10)

There was no bisect provided and it appears this issue goes back to beyond 116 for some time, updating FoundIn and other labels accordingly 
This fix also needs to be merged back to M114 since M114 will become Extended Stable support when 115 is promoted to Stable next week. 

Merges approved to M115 and M114, please merge this fix to branches 5790 and 5735 respectively at your earliest convenience 

 

### am...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2023-07-10)

Replying to https://crbug.com/chromium/1457421#c34:

1. No. This part of the code hasn't changed for a while from what I can tell.
2. No (to the best of my knowledge).

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a43b34dfc661b96f44d9e02528d62c0d711b9dc6

commit a43b34dfc661b96f44d9e02528d62c0d711b9dc6
Author: Tommi <tommi@chromium.org>
Date: Mon Jul 10 19:53:21 2023

[M114] Make RTCDataChannel's channel and observer pointers const.

This allows channel properties to be queried while the RTCDataChannel
instance exists and avoids potential null deref after entering the
kClosed state.

(cherry picked from commit 08d5ad011f53a1995bfccef6728bfa62541f7608)

Bug: 1456567, 1457421
Change-Id: I4747f9c00804b35711667d7320ec6188f20910c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4663082
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1165406}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4675624
Reviewed-by: Mirko Bonadei <mbonadei@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1447}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/a43b34dfc661b96f44d9e02528d62c0d711b9dc6/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
[modify] https://crrev.com/a43b34dfc661b96f44d9e02528d62c0d711b9dc6/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc


### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/19e3023eaf832c29eb984c0fdc7cc7d2d9120270

commit 19e3023eaf832c29eb984c0fdc7cc7d2d9120270
Author: Tommi <tommi@chromium.org>
Date: Mon Jul 10 20:20:29 2023

[M115] Make RTCDataChannel's channel and observer pointers const.

This allows channel properties to be queried while the RTCDataChannel
instance exists and avoids potential null deref after entering the
kClosed state.

(cherry picked from commit 08d5ad011f53a1995bfccef6728bfa62541f7608)

Bug: 1456567, 1457421
Change-Id: I4747f9c00804b35711667d7320ec6188f20910c4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4663082
Commit-Queue: Tomas Gunnarsson <tommi@chromium.org>
Reviewed-by: Elad Alon <eladalon@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1165406}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4675730
Reviewed-by: Mirko Bonadei <mbonadei@chromium.org>
Cr-Commit-Position: refs/branch-heads/5790@{#1553}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/19e3023eaf832c29eb984c0fdc7cc7d2d9120270/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.h
[modify] https://crrev.com/19e3023eaf832c29eb984c0fdc7cc7d2d9120270/third_party/blink/renderer/modules/peerconnection/rtc_data_channel.cc


### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-13)

[Description Changed]

### am...@chromium.org (2023-07-13)

Congratulations @Kipreyyy! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### vo...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-07-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-07-18)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-27)

Already merged to M114.

### am...@google.com (2023-08-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1457421?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066280)*
