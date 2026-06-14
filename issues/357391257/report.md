# memory corruption in blink::Delay::ProcessARateScalar

| Field | Value |
|-------|-------|
| **Issue ID** | [357391257](https://issues.chromium.org/issues/357391257) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | em...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2024-08-05 |
| **Bounty** | $7,000.00 |

## Description

tested OS:
ubuntu 22.04 and MacOS
tested chrome version:
    Chromium 129.0.6630.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1335746.zip)
    stable & canary & dev

Repro Steps:
    -  Open browser.
         ~/asan-linux-release/chrome  --incognito --user-data-dir=/tmp/xx2 http://localhost:8880
    -  Manually click on crash.html in the browser's list immediately reproduces the issue. 
Note:
    - Manually clicking on crash.html in the browser's list immediately reproduces the issue. However, directly passing crash.html as a command line argument in the terminal does not reproduce the issue as consistently. Therefore, I'm not entirely sure if CF can reproduce this issue. If CF cannot reproduce it, you can try manually.

    - This issue is similar to https://issues.chromium.org/issues/40945677. In the PoC code, I only added one line of code to trigger this issue:

    - delay.delayTime.setValueAtTime(5, ctx.currentTime);
    On Linux, it's a non-ASan instrumented crash, but on macOS, it reproduces a stack-use-after-return or UAF.

## Attachments

- [crash.html](attachments/crash.html) (text/html, 662 B)
- [SEGV_MAPERR_linux.log](attachments/SEGV_MAPERR_linux.log) (text/plain, 9.4 KB)
- [stack-use-after-return-macos.log](attachments/stack-use-after-return-macos.log) (text/plain, 22.4 KB)

## Timeline

### kr...@google.com (2024-08-05)

hongchan can you take a look as it looks very similar to [b/40945677](https://issues.chromium.org/issues/40945677)? Setting found-in as 126 as in extended stable, but it has probably been around for a long time.

### pe...@google.com (2024-08-06)

Setting milestone because of s0/s1 severity.

### ho...@chromium.org (2024-08-06)

The stack trace:

```
Received signal 11 SEGV_MAPERR 7feec3e0d800
    #0 0x558206747c16 in ___interceptor_backtrace /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/../sanitizer_common/sanitizer_common_interceptors.inc:4369:13
    #1 0x55821e9475d8 in base::debug::CollectStackTrace(base::span<void const*, 18446744073709551615ul, void const**>) ./../../base/debug/stack_trace_posix.cc:1044:7
    #2 0x55821e8ff9f9 in base::debug::StackTrace::StackTrace(unsigned long) ./../../base/debug/stack_trace.cc:245:20
    #3 0x55821e9468c6 in base::debug::(anonymous namespace)::StackDumpSignalHandler(int, siginfo_t*, void*) ./../../base/debug/stack_trace_posix.cc:463:3
    #4 0x7feb52c591a0 in __GI___sigaction :?
    #5 0x558233d9a6b5 in blink::Delay::ProcessARateVector(float*, unsigned int) const ./../../third_party/blink/renderer/platform/audio/cpu/x86/delay_sse2.cc:0:0
    #6 0x558233d992b0 in blink::Delay::ProcessARate(float const*, float*, unsigned int) ./../../third_party/blink/renderer/platform/audio/delay.cc:202:7
    #7 0x558233f2fcba in blink::DelayHandler::Process(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/delay_handler.cc:73:24
    #8 0x558233decf3b in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_handler.cc:0:21
    #9 0x558233e26c65 in blink::AudioNodeOutput::Pull(blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_output.cc:134:13
    #10 0x558233e22491 in blink::AudioNodeInput::SumAllConnections(scoped_refptr<blink::AudioBus>, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_input.cc:132:40
    #11 0x558233e22d02 in blink::AudioNodeInput::Pull(blink::AudioBus*, unsigned int) ./../../third_party/blink/renderer/modules/webaudio/audio_node_input.cc:162:3
    #12 0x558233fb495c in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&, base::TimeDelta, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc:241:18
    #13 0x558233fc2b4e in PullFromCallback ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:594:14
    #14 0x558233fc2b4e in blink::AudioDestination::ProvideResamplerInput(int, blink::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:582:3
    #15 0x558233fc649f in Invoke<void (blink::AudioDestination::*)(int, blink::AudioBus *), blink::AudioDestination *, int, blink::AudioBus *> ./../../base/functional/bind_internal.h:738:12
    #16 0x558233fc649f in MakeItSo<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, int, blink::AudioBus *> ./../../base/functional/bind_internal.h:930:12
    #17 0x558233fc649f in RunImpl<void (blink::AudioDestination::*const &)(int, blink::AudioBus *), const std::__Cr::tuple<WTF::CrossThreadUnretainedWrapper<blink::AudioDestination> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #18 0x558233fc649f in base::internal::Invoker<base::internal::FunctorTraits<void (blink::AudioDestination::* const&)(int, blink::AudioBus*), blink::AudioDestination*>, base::internal::BindState<true, true, false, void (blink::AudioDestination::*)(int, blink::AudioBus*), WTF::CrossThreadUnretainedWrapper<blink::AudioDestination>>, void (int, blink::AudioBus*)>::Run(base::internal::BindStateBase*, int, blink::AudioBus*) ./../../base/functional/bind_internal.h:987:12
    #19 0x558233f568f0 in base::RepeatingCallback<void (int, blink::AudioBus*)>::Run(int, blink::AudioBus*) const & ./../../base/functional/callback.h:344:12
    #20 0x558233f55c20 in Run ./../../third_party/blink/renderer/platform/wtf/functional.h:305:22
    #21 0x558233f55c20 in blink::MediaMultiChannelResampler::ProvideResamplerInput(int, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/media_multi_channel_resampler.cc:59:12
    #22 0x558233f56587 in Invoke<void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus *), blink::MediaMultiChannelResampler *, int, media::AudioBus *> ./../../base/functional/bind_internal.h:738:12
    #23 0x558233f56587 in MakeItSo<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, int, media::AudioBus *> ./../../base/functional/bind_internal.h:930:12
    #24 0x558233f56587 in RunImpl<void (blink::MediaMultiChannelResampler::*const &)(int, media::AudioBus *), const std::__Cr::tuple<base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0> > &, 0UL> ./../../base/functional/bind_internal.h:1067:14
    #25 0x558233f56587 in base::internal::Invoker<base::internal::FunctorTraits<void (blink::MediaMultiChannelResampler::* const&)(int, media::AudioBus*), blink::MediaMultiChannelResampler*>, base::internal::BindState<true, true, false, void (blink::MediaMultiChannelResampler::*)(int, media::AudioBus*), base::internal::UnretainedWrapper<blink::MediaMultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void (int, media::AudioBus*)>::Run(base::internal::BindStateBase*, int, media::AudioBus*) ./../../base/functional/bind_internal.h:987:12
    #26 0x55820a111830 in base::RepeatingCallback<void (int, media::AudioBus*)>::Run(int, media::AudioBus*) const & ./../../base/functional/callback.h:344:12
    #27 0x55820a1a080f in media::MultiChannelResampler::ProvideInput(int, int, float*) ./../../media/base/multi_channel_resampler.cc:98:14
    #28 0x55820a1a290e in Invoke<void (media::MultiChannelResampler::*)(int, int, float *), media::MultiChannelResampler *, const int &, int, float *> ./../../base/functional/bind_internal.h:738:12
    #29 0x55820a1a290e in MakeItSo<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, int, float *> ./../../base/functional/bind_internal.h:930:12
    #30 0x55820a1a290e in RunImpl<void (media::MultiChannelResampler::*const &)(int, int, float *), const std::__Cr::tuple<base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int> &, 0UL, 1UL> ./../../base/functional/bind_internal.h:1067:14
    #31 0x55820a1a290e in base::internal::Invoker<base::internal::FunctorTraits<void (media::MultiChannelResampler::* const&)(int, int, float*), media::MultiChannelResampler*, int const&>, base::internal::BindState<true, true, false, void (media::MultiChannelResampler::*)(int, int, float*), base::internal::UnretainedWrapper<media::MultiChannelResampler, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>, int>, void (int, float*)>::Run(base::internal::BindStateBase*, int, float*) ./../../base/functional/bind_internal.h:987:12
    #32 0x55820a203a50 in base::RepeatingCallback<void (int, float*)>::Run(int, float*) const & ./../../base/functional/callback.h:344:12
    #33 0x55820a203439 in media::SincResampler::Resample(int, float*) ./../../media/base/sinc_resampler.cc:348:14
    #34 0x55820a1a10c7 in media::MultiChannelResampler::Resample(int, media::AudioBus*) ./../../media/base/multi_channel_resampler.cc:82:23
    #35 0x558233fbce48 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:558:19
    #36 0x558233fbb13d in blink::AudioDestination::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../third_party/blink/renderer/platform/audio/audio_destination.cc:216:7
    #37 0x558238b3e77a in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../content/renderer/media/renderer_webaudiodevice_impl.cc:312:27
    #38 0x55820a1faf18 in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus*) ./../../media/base/silent_sink_suspender.cc:83:14
    #39 0x55820a068ada in media::AudioOutputDeviceThreadCallback::Process(unsigned int) ./../../media/audio/audio_output_device_thread_callback.cc:96:21
    #40 0x55820a0321f2 in media::AudioDeviceThread::ThreadMain() ./../../media/audio/audio_device_thread.cc:100:18
    #41 0x55821e8e196a in base::(anonymous namespace)::ThreadFunc(void*) ./../../base/threading/platform_thread_posix.cc:101:13
    #42 0x55820679cbd7 in asan_thread_start(void*) _asan_rtl_:28
    #43 0x7feb52ca539c in start_thread ./nptl/pthread_create.c:444:8
    #44 0x7feb52d26490 in __clone ./misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:100:0
  r8: 0000000000000000  r9: 0000000000000000 r10: 00000000000bb880 r11: 0000000000000000
 r12: 00007feac4801800 r13: 0000516000060980 r14: 000000000000001f r15: 0000516000060380
  di: 0000516000060980  si: 00000a2c80004130  bp: 00007feac5ffa6f0  bx: 00005080000a41bc
  dx: 0000000000000000  ax: 0000516000060380  cx: 00007feec3e0d800  sp: 00007feac5ffa6b0
  ip: 0000558233d9a6b5 efl: 0000000000010246 cgf: 002b000000000033 erf: 0000000000000004
 trp: 000000000000000e msk: 0000000000000000 cr2: 00007feec3e0d800
[end of stack trace]
../../sandbox/linux/seccomp-bpf-helpers/sigsys_handlers.cc:**CRASHING**:seccomp-bpf failure in syscall nr=0x25 arg1=0x5 arg2=0x7feac5ff9d70 arg3=0x0 arg4=0x8


```

SEGV\_MAPERR is happening at:

```
  unsigned frames_processed;
  std::tie(frames_processed, write_index_) =
      ProcessARateVector(destination, frames_to_process); <== HERE

```

### ho...@chromium.org (2024-08-12)

The CL is now under the review:
<https://crrev.com/c/5767447>

### ho...@chromium.org (2024-08-21)

The CL is approved, and the team is working to land it.

### ap...@google.com (2024-08-21)

Project: chromium/src
Branch: main

commit ec85a32bb5d736637c934088c14b2b6a42457467
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Wed Aug 21 22:11:47 2024

    Protect automation_rate_ from non-deterministic change
    
    This CL fixes non-deterministic (racy) data change on
    AudioParamHandler::automation_rate_. It also revises incorrect logic
    in the DelayHandler's process function; the process function
    needs to process all the channels in the delay kernel in the same
    rate. However, the previous code allowed the automation rate to
    change any time even in the middle of processing.
    
    This fix is locally confirmed with the provided repro case,
    and also a test was added to verify other related API surfaces.
    
    Bug: 357391257
    Change-Id: I7ce953837edd818e435e3a1b917f6b3c6147d95b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767447
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1345091}

M       third_party/blink/renderer/modules/webaudio/audio_param_handler.h
M       third_party/blink/renderer/modules/webaudio/delay_handler.cc
A       third_party/blink/web_tests/webaudio/AudioParam/audioparam-rate-change-357391257.html

https://chromium-review.googlesource.com/5767447


### ho...@chromium.org (2024-08-22)

Now the patch is included in 130.0.6671.0.

We believe the issue has been resolved. We would greatly appreciate verification from the reporter.

### em...@gmail.com (2024-08-22)

I tested this CL over a week ago, and I can confirm that the issue has been resolved.
Tested on: Ubuntu and macOS.

### ho...@chromium.org (2024-08-22)

Thank you very much for the confirmation!

### pe...@google.com (2024-08-23)

Requesting merge to stable (M128) because latest trunk commit (1345091) appears to be after stable branch point (1331488).
Requesting merge to beta (M129) because latest trunk commit (1345091) appears to be after beta branch point (1343869).
Merge review required: M128 is already shipping to stable.

**Merge approved:** your change passed merge requirements and is auto-approved for M129. Please go ahead and merge the CL to branch 6668 (refs/branch-heads/6668) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [128, 129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ho...@chromium.org (2024-08-23)

1. <https://chromium-review.googlesource.com/5767447>
2. Yes
3. No
4. No
5. No
6. Done

### ho...@chromium.org (2024-08-23)

Merge M129 (6668) is completed: <https://crrev.com/c/5809298>.

### ap...@google.com (2024-08-23)

Project: chromium/src
Branch: refs/branch-heads/6668

commit 8669b50ce1c002cc5e9f039b8cb94857f68a1414
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Fri Aug 23 18:02:20 2024

    Protect automation_rate_ from non-deterministic change
    
    This CL fixes non-deterministic (racy) data change on
    AudioParamHandler::automation_rate_. It also revises incorrect logic
    in the DelayHandler's process function; the process function
    needs to process all the channels in the delay kernel in the same
    rate. However, the previous code allowed the automation rate to
    change any time even in the middle of processing.
    
    This fix is locally confirmed with the provided repro case,
    and also a test was added to verify other related API surfaces.
    
    (cherry picked from commit ec85a32bb5d736637c934088c14b2b6a42457467)
    
    Bug: 357391257
    Change-Id: I7ce953837edd818e435e3a1b917f6b3c6147d95b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767447
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1345091}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5809298
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6668@{#216}
    Cr-Branched-From: 05bc664984ca075216b7f2198c88b9725bfa1b9b-refs/heads/main@{#1343869}

M       third_party/blink/renderer/modules/webaudio/audio_param_handler.h
M       third_party/blink/renderer/modules/webaudio/delay_handler.cc
A       third_party/blink/web_tests/webaudio/AudioParam/audioparam-rate-change-357391257.html

https://chromium-review.googlesource.com/5809298


### pe...@google.com (2024-08-23)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@chromium.org (2024-08-28)

<https://crrev.com/c/5767447> approved for merge to M128; please merge this fix to branch 6613 by EOD Thursday, 29 August so this fix can be included in the next M128 Stable update -- thanks!

### ho...@chromium.org (2024-08-28)

Merge M128 (6613) is in-flight: <https://crrev.com/c/5824779>

### ap...@google.com (2024-08-28)

Project: chromium/src
Branch: refs/branch-heads/6613

commit 5aeecd43d0baa3b40d9c967c498f53e62202cfcc
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Wed Aug 28 22:16:32 2024

    Protect automation_rate_ from non-deterministic change
    
    This CL fixes non-deterministic (racy) data change on
    AudioParamHandler::automation_rate_. It also revises incorrect logic
    in the DelayHandler's process function; the process function
    needs to process all the channels in the delay kernel in the same
    rate. However, the previous code allowed the automation rate to
    change any time even in the middle of processing.
    
    This fix is locally confirmed with the provided repro case,
    and also a test was added to verify other related API surfaces.
    
    (cherry picked from commit ec85a32bb5d736637c934088c14b2b6a42457467)
    
    Bug: 357391257
    Change-Id: I7ce953837edd818e435e3a1b917f6b3c6147d95b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767447
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1345091}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5824779
    Auto-Submit: Hongchan Choi <hongchan@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6613@{#1437}
    Cr-Branched-From: 03c1799e6f9c7239802827eab5e935b9e14fceae-refs/heads/main@{#1331488}

M       third_party/blink/renderer/modules/webaudio/audio_param_handler.h
M       third_party/blink/renderer/modules/webaudio/delay_handler.cc
A       third_party/blink/web_tests/webaudio/AudioParam/audioparam-rate-change-357391257.html

https://chromium-review.googlesource.com/5824779


### sp...@google.com (2024-08-28)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
baseline report of memory corruption in a sandboxed process / renderer


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-29)

Congratulations Cassidy Kim! Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-09-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2024-09-13)

1. Just https://crrev.com/c/5853171
2. Low, no conflicts
3. 120
4. Yes

### pe...@google.com (2024-09-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-09-13)

1. <https://crrev.com/c/5854511>
2. Low, no conflicts
3. 128, 129
4. Yes

### ap...@google.com (2024-09-16)

Project: chromium/src
Branch: refs/branch-heads/6099

commit 4cb5d5ed55ba5517ba880f212eafb8b77e84057e
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Mon Sep 16 19:42:13 2024

    [M120-LTS] Protect automation_rate_ from non-deterministic change
    
    This CL fixes non-deterministic (racy) data change on
    AudioParamHandler::automation_rate_. It also revises incorrect logic
    in the DelayHandler's process function; the process function
    needs to process all the channels in the delay kernel in the same
    rate. However, the previous code allowed the automation rate to
    change any time even in the middle of processing.
    
    This fix is locally confirmed with the provided repro case,
    and also a test was added to verify other related API surfaces.
    
    (cherry picked from commit ec85a32bb5d736637c934088c14b2b6a42457467)
    
    Bug: 357391257
    Change-Id: I7ce953837edd818e435e3a1b917f6b3c6147d95b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767447
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1345091}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5853171
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Artem Sumaneev <asumaneev@google.com>
    Commit-Queue: Michael Wilson <mjwilson@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6099@{#2081}
    Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

M       third_party/blink/renderer/modules/webaudio/audio_param_handler.h
M       third_party/blink/renderer/modules/webaudio/delay_handler.cc
A       third_party/blink/web_tests/webaudio/AudioParam/audioparam-rate-change-357391257.html

https://chromium-review.googlesource.com/5853171


### ap...@google.com (2024-09-17)

Project: chromium/src
Branch: refs/branch-heads/6478

commit 35497f6aaf45b4e2fa5641261dbb402e98238e60
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Tue Sep 17 17:04:42 2024

    [M126-LTS] Protect automation_rate_ from non-deterministic change
    
    This CL fixes non-deterministic (racy) data change on
    AudioParamHandler::automation_rate_. It also revises incorrect logic
    in the DelayHandler's process function; the process function
    needs to process all the channels in the delay kernel in the same
    rate. However, the previous code allowed the automation rate to
    change any time even in the middle of processing.
    
    This fix is locally confirmed with the provided repro case,
    and also a test was added to verify other related API surfaces.
    
    (cherry picked from commit ec85a32bb5d736637c934088c14b2b6a42457467)
    
    Bug: 357391257
    Change-Id: I7ce953837edd818e435e3a1b917f6b3c6147d95b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767447
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1345091}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5854511
    Reviewed-by: Giovanni Pezzino <giovax@google.com>
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Commit-Position: refs/branch-heads/6478@{#1962}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/webaudio/audio_param_handler.h
M       third_party/blink/renderer/modules/webaudio/delay_handler.cc
A       third_party/blink/web_tests/webaudio/AudioParam/audioparam-rate-change-357391257.html

https://chromium-review.googlesource.com/5854511


### ap...@google.com (2024-09-18)

Project: chromium/src
Branch: refs/branch-heads/6478_182

commit 0bbd2f1fdbaf38ce3d9225a84607cbae3b170cc3
Author: Hongchan Choi <hongchan@chromium.org>
Date:   Wed Sep 18 04:21:46 2024

    [CfM-M126] Protect automation_rate_ from non-deterministic change
    
    This CL fixes non-deterministic (racy) data change on
    AudioParamHandler::automation_rate_. It also revises incorrect logic
    in the DelayHandler's process function; the process function
    needs to process all the channels in the delay kernel in the same
    rate. However, the previous code allowed the automation rate to
    change any time even in the middle of processing.
    
    This fix is locally confirmed with the provided repro case,
    and also a test was added to verify other related API surfaces.
    
    (cherry picked from commit ec85a32bb5d736637c934088c14b2b6a42457467)
    
    (cherry picked from commit 35497f6aaf45b4e2fa5641261dbb402e98238e60)
    
    Bug: 357391257
    Change-Id: I7ce953837edd818e435e3a1b917f6b3c6147d95b
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5767447
    Commit-Queue: Hongchan Choi <hongchan@chromium.org>
    Cr-Original-Original-Commit-Position: refs/heads/main@{#1345091}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5854511
    Reviewed-by: Giovanni Pezzino <giovax@google.com>
    Reviewed-by: Hongchan Choi <hongchan@chromium.org>
    Reviewed-by: Michael Wilson <mjwilson@chromium.org>
    Commit-Queue: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com>
    Cr-Original-Commit-Position: refs/branch-heads/6478@{#1962}
    Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5871312
    Commit-Queue: Pablo Ceballos <pceballos@chromium.org>
    Owners-Override: Pablo Ceballos <pceballos@chromium.org>
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
    Cr-Commit-Position: refs/branch-heads/6478_182@{#78}
    Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       third_party/blink/renderer/modules/webaudio/audio_param_handler.h
M       third_party/blink/renderer/modules/webaudio/delay_handler.cc
A       third_party/blink/web_tests/webaudio/AudioParam/audioparam-rate-change-357391257.html

https://chromium-review.googlesource.com/5871312


### pe...@google.com (2024-11-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/357391257)*
