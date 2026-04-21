# Heap Buffer Overflow in AudioWorkletProcessor::ClonePortTopology

| Field | Value |
|-------|-------|
| **Issue ID** | [40062369](https://issues.chromium.org/issues/40062369) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | em...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2022-12-24 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

tested chrome version:  

Chromium 111.0.5497.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1086812.zip)  

Chromium 110.0.5478.4  

os version:  

22.04  

repro steps:  

(1) python3 -m http.server 8000 --dir=|Directory path for containing the crash.html file.|  

(2) ./chrome --disable-gesture-requirement-for-media-playback --user-data-dir=/tmp/xx --autoplay-policy=no-user-gesture-required --incognito <http://localhost:8000/crash.html>  

(3)The crash results may some noisy, such as null-dereference crash or fatal check errors. In this case, manually refreshing the browser several times should trigger heap buffer overflow.

# **Problem Description:** The asan report may also mix with heap buffer overflow and other crash information, such as null-dereference crash or fatal check errors. It seems that this issue may be triggered by other threads crashing beforehand. I am not sure if this is an asan false positive or a valid security issue.

==2623679==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6250002460f0 at pc 0x564584bba186 bp 0x7f983df4b8b0 sp 0x7f983df4b8a8  

WRITE of size 16 at 0x6250002460f0 thread T24 (AudioOutputDevi)  

[2623679:2623696:1224/110302.011992:FATAL:v8\_initializer.cc(727)] V8 error: Cannot exit non-entered context (v8::Context::Exit()).  

#0 0x56457ee5d9b7 in backtrace /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/../sanitizer\_common/sanitizer\_common\_interceptors.inc:4434:13  

#1 0x56459097ae4c in base::debug::CollectStackTrace(void\*\*, unsigned long) ./../../base/debug/stack\_trace\_posix.cc:894:7  

#2 0x5645906bf312 in StackTrace ./../../base/debug/stack\_trace.cc:221:12  

#3 0x5645906bf312 in base::debug::StackTrace::StackTrace() ./../../base/debug/stack\_trace.cc:218:28  

#4 0x564590712ca2 in logging::LogMessage::~LogMessage() ./../../base/logging.cc:718:29  

#5 0x56459d93f675 in blink::ReportV8FatalError(char const\*, char const\*) ./../../third\_party/blink/renderer/bindings/core/v8/v8\_initializer.cc:727:3  

#6 0x56458455d49f in ReportApiFailure ./../../v8/src/api/api.cc:320:5  

...  

#0 0x564584bba185 in v8::internal::HandleScope::ZapRange(unsigned long\*, unsigned long\*) ./../../v8/src/handles/handles.cc:185:8  

#1 0x564584c80f55 in CloseScope ./../../v8/src/handles/handles-inl.h:132:3  

#2 0x564584c80f55 in v8::internal::Handle[v8::internal::JSArray](javascript:void(0);) v8::internal::HandleScope::CloseAndEscape[v8::internal::JSArray](javascript:void(0);)(v8::internal::Handle[v8::internal::JSArray](javascript:void(0);)) ./../../v8/src/handles/handles-inl.h:150:3  

#3 0x564584c80916 in v8::internal::Factory::NewJSArray(v8::internal::ElementsKind, int, int, v8::internal::ArrayStorageAllocationMode, v8::internal::AllocationType) ./../../v8/src/heap/factory.cc:2808:22  

#4 0x5645845daa4b in NewJSArray ./../../v8/src/heap/factory.h:596:12  

#5 0x5645845daa4b in v8::Array::New(v8::Isolate\*, int) ./../../v8/src/api/api.cc:7664:53  

#6 0x5645a7db4350 in blink::AudioWorkletProcessor::ClonePortTopology(v8::Isolate\*, v8::Local[v8::Context](javascript:void(0);), WTF::Vector<scoped\_refptr[blink::AudioBus](javascript:void(0);), 0u, WTF::PartitionAllocator> const&, v8::TracedReference[v8::Array](javascript:void(0);)&, blink::HeapVector<blink::HeapVector<v8::TracedReference[v8::ArrayBuffer](javascript:void(0);), 0u>, 0u>&) ./../../third\_party/blink/renderer/modules/webaudio/audio\_worklet\_processor.cc:280:7  

#7 0x5645a7db31c0 in blink::AudioWorkletProcessor::Process(WTF::Vector<scoped\_refptr[blink::AudioBus](javascript:void(0);), 0u, WTF::PartitionAllocator> const&, WTF::Vector<scoped\_refptr[blink::AudioBus](javascript:void(0);), 0u, WTF::PartitionAllocator>&, WTF::HashMap<WTF::String, std::Cr::unique\_ptr<blink::AudioArray<float>, std::Cr::default\_delete<blink::AudioArray<float>>>, WTF::DefaultHash[WTF::String](javascript:void(0);), WTF::HashTraits[WTF::String](javascript:void(0);), WTF::HashTraits<std::Cr::unique\_ptr<blink::AudioArray<float>, std::Cr::default\_delete<blink::AudioArray<float>>>>, WTF::PartitionAllocator> const&) ./../../third\_party/blink/renderer/modules/webaudio/audio\_worklet\_processor.cc:66:9  

#8 0x5645a7dc707a in blink::AudioWorkletHandler::Process(unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_worklet\_handler.cc:141:22  

#9 0x5645a7d7e32e in blink::AudioHandler::ProcessIfNecessary(unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/audio\_handler.cc:346:7  

#10 0x5645a7d6f080 in blink::DeferredTaskHandler::ProcessAutomaticPullNodes(unsigned int) ./../../third\_party/blink/renderer/modules/webaudio/deferred\_task\_handler.cc:187:41  

#11 0x5645a7e9be1f in blink::RealtimeAudioDestinationHandler::Render(blink::AudioBus\*, unsigned int, blink::AudioIOPosition const&, blink::AudioCallbackMetric const&) ./../../third\_party/blink/renderer/modules/webaudio/realtime\_audio\_destination\_handler.cc:229:37  

#12 0x5645a7ea1572 in blink::AudioDestination::RequestRender(unsigned long, unsigned long, double, double) ./../../third\_party/blink/renderer/platform/audio/audio\_destination.cc:308:17  

#13 0x5645a7ea086d in blink::AudioDestination::Render(blink::WebVector<float\*> const&, unsigned int, double, double) ./../../third\_party/blink/renderer/platform/audio/audio\_destination.cc:248:5  

#14 0x5645a865dc20 in content::RendererWebAudioDeviceImpl::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus\*) ./../../content/renderer/media/renderer\_webaudiodevice\_impl.cc:277:21  

#15 0x564581e0b94a in media::SilentSinkSuspender::Render(base::TimeDelta, base::TimeTicks, media::AudioGlitchInfo const&, media::AudioBus\*) ./../../media/base/silent\_sink\_suspender.cc:83:14  

#16 0x564581ce9135 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) ./../../media/audio/audio\_ou

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 43.8 KB)
- [repro.mov](attachments/repro.mov) (video/quicktime, 3.4 MB)

## Timeline

### [Deleted User] (2022-12-24)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-12-24)

Sorry, I missed a flag. In order to reproduce the results stably, you need to add an additional '--no-sandbox' startup flag.

### xi...@chromium.org (2022-12-26)

Thanks for the report. I tried several times but still not able to reproduce. I already applied the following flags as you suggested:
--disable-gesture-requirement-for-media-playback --autoplay-policy=no-user-gesture-required --no-sandbox

Reporter, I noticed that the main() function in crash.html calls itself recursively. Note that DoS attack is not considered as security bugs[1]. Do you have a PoC that doesn't require recursion to trigger this error? Otherwise, I don't think it is a security bug. Keeping it as security bug for now just in case.

+hongchan@, it seems that you have investigated https://crbug.com/1305340. Could you take a look at this crash to see if it is a duplicate? Thanks!

[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/faq.md#are-denial-of-service-issues-considered-security-bugs

[Monorail components: Blink>WebAudio]

### xi...@chromium.org (2022-12-26)

In addition, while trying to reproduce, my console is flooded with warnings like this:

...
[72583:72745:1226/000045.725657:WARNING:push_pull_fifo.cc(237)] PushPullFIFO::PullAndUpdateEarmarkunderflow while pulling (underflowCount=70, availableFrames=2, requestedFrames=441, fifoLength=12288)
[72583:72745:1226/000045.734053:WARNING:push_pull_fifo.cc(237)] PushPullFIFO::PullAndUpdateEarmarkunderflow while pulling (underflowCount=71, availableFrames=2, requestedFrames=441, fifoLength=12288)
...


### [Deleted User] (2022-12-26)

[Empty comment from Monorail migration]

### em...@gmail.com (2022-12-26)

I have not yet reproduced without using recursive call, but I don't think there is much of a relation between recursive call and DOS in this case. I have uploaded a video of the reproduction here, hoping it can help you.

### [Deleted User] (2022-12-26)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-26)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-07)

hongchan: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ho...@chromium.org (2023-01-10)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-01-10)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-01-10)

I see a crash from ASAN, but different location:

[1443997:1444192:0110/212921.976501:FATAL:audio_worklet_processor.cc(48)] Check failed: global_scope_->IsContextThread().

Also the provided repro case is very flaky and I can't reproduce the issue consistently. This will be difficult to fix/verify.



### em...@gmail.com (2023-01-11)

I have tried on other pc and it is not repro stable with the above flags. I added --no-sandbox and it can now be more stably reproduced on other pc as well.
You can try adding the --no-sandbox flag and see if it can repro.
tested version:
Chromium 111.0.5523.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1091147.zip)
launch command:
./crhome --disable-gesture-requirement-for-media-playback  --user-data-dir=/tmp/xx --autoplay-policy=no-user-gesture-required --incognito http://localhost:8000/crash.html --no-sandbox

### ho...@chromium.org (2023-01-12)

I am actively working on this problem, but I was able to reproduce heap-buffer-overflow only once so far. (Yes. I am using --no-sandbox option)

However, I think I understood why this problem is happening - hopefully I can produce a fix in a couple of days.

### ho...@chromium.org (2023-01-13)

Here's my analysis:


# Repro case

async function main() {
    context = new AudioContext();
     let node;
     await context.audioWorklet.addModule(url);
     node = new AudioWorkletNode(context, "processor");
     await context.resume();                                                        
     main()
     context.suspend();
     context.resume();
 }
 main();


# Analysis

The problem is the robustness of context.resume() operation. In Chromium WebAudio, the context state switching from "running" to "suspended" is immediate, but the opposite is not the case; resuming a suspended context is not synchronous since it activates the underlying audio infrastructure. So there's a slight chance of "limbo state" where the platform sink (destination) is running, but the resolution of AudioContext.resume() promise has not happened yet.

This is usually not a problem, but the thread switching caused by AudioWorklet.addModule() cause invalid thread access. The AudioWorkletGlobalScope should only be accessed from the AudioWorklet thread, but the limbo state makes it possible for non-AudioWorklet thread to execute the code in AudioWorkletProcessor and AudioWorkletGlobalScope. Various problems can be triggered by this and heap-buffer-overflow is just one of them. However, when DCHECK() is enabled the crash can be reproduced consistently at AudioWorkletProcessor::ClonePortTopology() because it is the first operation that allocates memory from the Worklet/Worker space. When that code is executed from non-Worklet thread, DCHECK(global_scope_->IsContextThread()) fails.

The recursion in the above repro make it easier to crash ASAN by rapidly switching the context status.


# Resolution

1) Short-term: BaseAudioContext::NotifyWorkletIsReady() method should handle the suspended case properly so the "limbo state" won't propagate to the platform destination level. POC CL: http://crrev.com/c/4150813

2) Long-term: The state switching/resolution logic should be revised so the limbo state doesn't happen. This will require a non-trivial refactoring.

### gi...@appspot.gserviceaccount.com (2023-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b1535a240f0a7697417f5dc5218ff9929fa1d7fe

commit b1535a240f0a7697417f5dc5218ff9929fa1d7fe
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Jan 25 20:31:15 2023

Handle a transitory state of context/destination correctly for AudioWorklet operation

When the context resumes from a suspended state, it is possible for
the internal (destination) and the external (context) state to be
different in a rare case. This allows the non-worklet thread to
touch the worklet-related objects, which can causes invalid access
to the V8-managed memory space.

This CL adds a check; if the context state is suspended it swaps
the task runner right away without waiting until a resume() promise
is resolved.

Bug: 1403515
Test: The provided repro case doesn't crash ASAN anymore.
Change-Id: Ic2ea7b0337c444b7dc7d9d8b7195ed3e9ac3955f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4150813
Reviewed-by: Michael Wilson <mjwilson@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1096948}

[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/modules/webaudio/audio_destination_handler.h
[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/modules/webaudio/base_audio_context.cc
[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.h
[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc
[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/platform/audio/audio_destination.cc
[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/platform/audio/audio_destination.h
[modify] https://crrev.com/b1535a240f0a7697417f5dc5218ff9929fa1d7fe/third_party/blink/renderer/modules/webaudio/offline_audio_destination_handler.h


### ho...@chromium.org (2023-01-31)

emilykim8708@ I locally tested the patch in https://crbug.com/chromium/1403515#c16 and the repro case doesn't crash the ASAN anymore. The patch is available on 111.0.5561.0 and later.

Please feel free to reopen the issue if the problem persists.

### em...@gmail.com (2023-02-01)

hongchan@
confirmed.
The issue did not reproduce again.
tested version:
-   Chromium 112.0.5572.0(gs://chromium-browser-asan/linux-release/asan-linux-release-1099531.zip)
-   Chromium 111.0.5545.6(custom asan build with patch)

### ho...@chromium.org (2023-02-01)

Thank you for a quick response! Changing the status to Verified.

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-10)

Really sweeping them up this week! Congratulations on yet another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- great work! 

### am...@google.com (2023-02-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-10)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1403515?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062369)*
