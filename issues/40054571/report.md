# Talos Security Advisory for Google Chrome browser (TALOS-2021-1235)

| Field | Value |
|-------|-------|
| **Issue ID** | [40054571](https://issues.chromium.org/issues/40054571) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | rt...@chromium.org |
| **Created** | 2021-01-25 |
| **Bounty** | $7,500.00 |

## Description

Google Chrome AudioDelayDSPKernel::ProcessKRate heap-based buffer overlow vulnerability

Summary

An exploitable heap-based buffer overflow vulnerability exists in Google Chromium browser at least in versions 89.0.4383.0 64-bit and 90.0.4390.0 64-bit. A specially crafted HTML web page can cause a heap-based Buffer Overflow condition, resulting in a remote code execution. The victim needs to visit malicious web site to trigger the vulnerability.

Tested Versions

Google Chrome ver 841401 ( 89.0.4383.0 64-bit) 
Google Chrome ver 844161 ( 90.0.4390.0 64-bit)

Product URLs

https://www.google.com/chrome/

CVSSv3 Score

8.8 - CVSS:3.0/AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H

CWE

CWE-122 - Heap-based Buffer Overflow

Details

Google Chrome is a cross-platform web browser, developed by Google.

To understand the vulnerability let us analyze some parts of the poc.html file and coresponding logged lines from the browser console:

 "Mutation nodes amount :  6"
 "[ 4:21:34 PM ] :: Connecting nodes"
 "[ 4:21:34 PM ] :: Nodes connected"
 "[ 4:21:34 PM ] :: MediaElementAudioSourceNode_handler"
 "[ 4:21:34 PM ] :: AudioContext_handler"
 "IIRFilterNode: state is bad, probably due to unstable filter."

 "[ 4:21:34 PM ] :: ScriptProcessorNode_oncomplete"
 "[ 4:21:34 PM ] :: Index : 1"
 "[ 4:21:34 PM ] :: Connect IIRFilterNode to DelayNode.delayTime"
As we can see, after an initialization phase of PoC setup, first events start to appear and being handle.
Crucial actions for our PoC take place inside the oncomplete event handler named ScriptProcessorNode_oncomplete of the ScriptProcessorNode node:

Line 42     var g_fuzzRandom_index = 0;
Line 43
Line 44     //events handlers
Line 45     function ScriptProcessorNode_oncomplete()
Line 46     {
Line 47         writeLog("ScriptProcessorNode_oncomplete");
Line 48         
Line 49         g_fuzzRandom_index++;
Line 50         writeLog("Index : " + g_fuzzRandom_index);
Line 51
Line 52
Line 53         if(g_fuzzRandom_index == 1)
Line 54         {    
Line 55             writeLog("Connect IIRFilterNode to DelayNode.delayTime");
Line 56             audioNodesObjects.mutation[4].obj.connect( audioNodesObjects.mutation[5].obj.delayTime );    
Line 57             return;
Line 58         }
During the first execution of ScriptProcessorNode_oncomplete event handler IIRFilterNode node is being connected to an AudioParam object. In our case it is a delayTime field of DelayNode object line 56.
That connection is required to trigger the vulnerability but tests have shown that beside IIRFilterNode a different type of AudioNode can be also use to obtain the same result.

When the ScriptProcessorNode_oncomplete handler is executed for a second time, the following lines will appear inside the log file:

 "[ 4:21:35 PM ] :: ScriptProcessorNode_oncomplete"
 "[ 4:21:35 PM ] :: Index : 2"
 "[ 4:21:35 PM ] :: Switch delayTime of DelayNode to k-rate"
and the corresponding code is executed :

Line 59 if(g_fuzzRandom_index == 2)
Line 60 {                       
Line 61     //DelayNode
Line 62     writeLog("Switch delayTime of DelayNode to k-rate");
Line 63     audioNodesObjects.mutation[5].obj.delayTime.automationRate = "k-rate";
Line 64     return;
Line 65 }
The crucial code is executed in line 63 where value of automationRate field is changed to k-rate from a-rate. 
More details about possible AutomationRate values are available here: https://www.w3.org/TR/webaudio/#dom-audioparam-automationrate
That switch during processing phase (we are inside oncomplete event handler) leads to the vulnerability inside blink::AudioDelayDSPKernel::ProcessKRate method located in file third_party\blink\renderer\platform\audio\audio_delay_dsp_kernel.cc.
As you might notice browsing code around blink::AudioDelayDSPKernel::ProcessKRate there is also method responsible of data procesing in case when automationRate field is set to a-rate and its called AudioDelayDSPKernel::ProcessARate.
As I mentioned before, it seems to runtime change from "a-rate" to "k-rate" during processing phase have lead to internal state confusion of the DelayNode object and finally to the vulnerability in :

audio_delay_dsp_kernel.cc

Line 276   // Now copy out the samples from the buffer, starting at the read pointer,
Line 277   // carefully handling wrapping of the read pointer.
Line 278   float* read_pointer = &buffer[read_index1];
Line 279  
Line 280   int remainder = buffer_end - read_pointer;
Line 281   memcpy(sample1, read_pointer,
Line 282          sizeof(*sample1) *
Line 283              std::min(static_cast<int>(frames_to_process), remainder));
There is no check whether buffer_end is smaller than read_pointer which in our case happens. Further in line 281 as a size parameter for memcpy the smaller value of frames_to_process and reminder is selected.
Because both variables are treated as a signed integer our remainder ends up beeing selected because its value is < 0. At the end its casted to size_t (unsigned value) what finally cause an attempt to copy a huge amount of memory.

Proper heap grooming can give an attacker full control of this heap overflow vulnerability and as a result could allow it to be turned into a arbitrary code execution.

Crash Information

=================================================================
==1076==ERROR: AddressSanitizer: negative-size-param: (size=-8589824196)
    #0 0x7ff74867402f in __asan_memcpy C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_interceptors_memintrinsics.cpp:22
    #1 0x7ffaf2dc9ab1 in blink::AudioDelayDSPKernel::ProcessKRate(float const *, float *, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_delay_dsp_kernel.cc:281:3
    #2 0x7ffaf2dcf38c in blink::AudioDSPKernelProcessor::Process(class blink::AudioBus const *, class blink::AudioBus *, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_dsp_kernel_processor.cc:85:20
    #3 0x7ffaf23dfbac in blink::AudioBasicProcessorHandler::Process(unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_basic_processor_handler.cc:85:18
    #4 0x7ffaf0be1e26 in blink::AudioHandler::ProcessIfNecessary(unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node.cc:368:7
    #5 0x7ffaf18a8f2c in blink::AudioNodeOutput::Pull(class blink::AudioBus *, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_output.cc:137:13
    #6 0x7ffaf18abfe6 in blink::AudioNodeInput::SumAllConnections(class scoped_refptr<class blink::AudioBus>, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc:128:40
    #7 0x7ffaf18ac278 in blink::AudioNodeInput::Pull(class blink::AudioBus *, unsigned int) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc:158:3
    #8 0x7ffaf1953707 in blink::RealtimeAudioDestinationHandler::Render(class blink::AudioBus *, unsigned int, struct blink::AudioIOPosition const &, struct blink::AudioCallbackMetric const &) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\realtime_audio_destination_node.cc:207:18
    #9 0x7ffaf23c15a7 in blink::AudioDestination::RequestRender(unsigned __int64, unsigned __int64, double, double, unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:251:17
    #10 0x7ffaf23c03f4 in blink::AudioDestination::Render(class blink::WebVector<float *> const &, unsigned __int64, double, double, unsigned __int64) C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc:194:5
    #11 0x7ffaedebee86 in content::RendererWebAudioDeviceImpl::Render(class base::TimeDelta, class base::TimeTicks, int, class media::AudioBus *) C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc:253:21
    #12 0x7ffada23aef4 in media::SilentSinkSuspender::Render(class base::TimeDelta, class base::TimeTicks, int, class media::AudioBus *) C:\b\s\w\ir\cache\builder\src\media\base\silent_sink_suspender.cc:84:14
    #13 0x7ffada171b16 in media::AudioOutputDeviceThreadCallback::Process(unsigned int) C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_device_thread_callback.cc:80:21
    #14 0x7ffada15810f in media::AudioDeviceThread::ThreadMain(void) C:\b\s\w\ir\cache\builder\src\media\audio\audio_device_thread.cc:95:18
    #15 0x7ffae1c7f18f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc:111:13
    #16 0x7ff74867e3a8 in __asan::AsanThread::ThreadStart(unsigned __int64, struct __sanitizer::atomic_uintptr_t *) C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_thread.cpp:273
    #17 0x7ffba61a7c23  (C:\WINDOWS\System32\KERNEL32.DLL+0x180017c23)
    #18 0x7ffba7ced4d0  (C:\WINDOWS\SYSTEM32\ntdll.dll+0x18006d4d0)
Credit

Discovered by Marcin 'Icewall' Noga of Cisco Talos.

https://talosintelligence.com/vulnerability_reports/


## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 27.0 KB)
- [TALOS-2021-1235 - Google_Chrome_AudioDelayDSPKernel::ProcessKRate_heap-based_buffer_overlow_vulnerability.txt](attachments/TALOS-2021-1235 - Google_Chrome_AudioDelayDSPKernel_ProcessKRate_heap-based_buffer_overlow_vulnerability.txt) (text/plain, 9.2 KB)
- [utilsAudio.js](attachments/utilsAudio.js) (text/plain, 1.5 KB)
- [README.md](attachments/README.md) (text/plain, 332 B)
- [random.js](attachments/random.js) (text/plain, 1.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 6.0 KB)
- [nodesDefinitions.js](attachments/nodesDefinitions.js) (text/plain, 3.6 KB)
- [demicmAudioShort.mp3](attachments/demicmAudioShort.mp3) (application/octet-stream, 22.4 KB)

## Timeline

### [Deleted User] (2021-01-25)

[Comment Deleted]

### [Deleted User] (2021-01-25)

Please add access to vulndiscovery@sourcefire.com 

### lg...@chromium.org (2021-01-26)

[Mac triage] changing label to Windows based on stack trace in c#0

### [Deleted User] (2021-01-26)

[Empty comment from Monorail migration]

### rt...@chromium.org (2021-01-26)

Where is the repro case?  That would be very helpful.

This code is used on all platforms so likely also affects all platforms (except iOS of course).

[Monorail components: Blink>WebAudio]

### vu...@sourcefire.com (2021-01-26)

poc file added

### rt...@chromium.org (2021-01-26)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-01-27)

Adding the contents of the zip file directly.

### cl...@chromium.org (2021-01-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5669169327833088.

### rt...@chromium.org (2021-01-28)

Thanks for the poc.  I can reproduce this on my linux box. Not sure why clusterfuzz can't reproduce this.

### rt...@chromium.org (2021-01-28)

Thanks for excellent analysis. The main thread changes the automation rate, but the audio thread could be in the middle of processing the AudioParam.  These need to be coordinated better.  I think the solution is that the main thread must wait until the audio thread is done processing before the rate is changed.

Implementing this now.

### rt...@chromium.org (2021-01-29)

Adding a bunch of prints and stuff shows that the real problem is that the delay time AudioParam is NaN.  Probably because the IIRFilter is possibly unstable.

I had a CL a while ago to make all AudioParams force NaN and infinity to the AudioParam.defaultValue.  That was rejected.  I'll have to try something else.

### rt...@chromium.org (2021-01-29)

I also see that the random coefficients used for the IIRFilter can cause a DCHECK failure estimating the roots.  I'll need to file a new issue on that.


### rt...@chromium.org (2021-01-29)

Oops.  I meant biquad not IIRFilter.

### rt...@chromium.org (2021-01-29)

Converting the NaN values in an AudioParam to the default value (as specified in https://webaudio.github.io/web-audio-api/#computation-of-value) fixes  this issue.  I can't get a crash anymore.

I still think your analysis does point to a problem, but without a repro case, it's hard to say and even harder to verify that it's fixed.

### cl...@chromium.org (2021-02-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6190435751231488.

### ts...@chromium.org (2021-02-05)

Updating a couple of labels.  Feel free to let me know if I've misjudged the situation. Thanks!

### [Deleted User] (2021-02-05)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ab1862017b5717271a28376659944dddc602195c

commit ab1862017b5717271a28376659944dddc602195c
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Feb 08 17:13:08 2021

Convert AudioParam NaN values to the default value

If any output value of an AudioParam (including the intrinsic values
and any inputs to the AudioParam), should be NaN, replace the NaN
value with the associated defaultValue.

This causes some slowdowns so SIMD/NEON code was added to mitigate the
degradation.  There is still some slowdown, but the worst case is now
about 7% slower on x86 and 10% on arm. Generally, the slowdown is less
than 2% and 5%, respectively.  (Perversely, some results got faster,
and the differences are statistically significant.)

Full details can be found at
https://docs.google.com/spreadsheets/d/1EhbLHm-9cUoEO5aj1vYemVBLQ3Dh4dCJPPLTfZPrZt4/edit?usp=sharing

Manually tested the test case from the bug and the issue no longer
occurs.

Bug: 1170531
Change-Id: I00d902b40a9ef9da990c6d68b664b1dcfc31b091
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2658724
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#851733}

[modify] https://crrev.com/ab1862017b5717271a28376659944dddc602195c/third_party/blink/renderer/modules/webaudio/audio_param.cc
[add] https://crrev.com/ab1862017b5717271a28376659944dddc602195c/third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-audioparam-interface/nan-param.html


### rt...@chromium.org (2021-02-09)

[Empty comment from Monorail migration]

### rt...@chromium.org (2021-02-09)

Fix has baked for a day so I think it's good to go.

### [Deleted User] (2021-02-09)

Requesting merge to stable M88 because latest trunk commit (851733) appears to be after stable branch point (827102).

Requesting merge to beta M89 because latest trunk commit (851733) appears to be after beta branch point (843830).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-09)

This bug requires manual review: M89's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-02-09)

Approving merge to M89, branch 4389.

### rt...@chromium.org (2021-02-09)

1. Does your merge fit within the Merge Decision Guidelines?
Yes.

2. Links to the CLs you are requesting to merge.
https://chromium-review.googlesource.com/c/chromium/src/+/2658724

3. Has the change landed and been verified on ToT?
Yes. Did a local build with ToT and retested.  Repro case no longer does.

4. Does this change need to be merged into other active release branches (M-1, M+1)?
Should merge to 89, possibly 88 as well.

5. Why are these changes required in this milestone after branch?
Security issue due to writing past the bounds of an array.  This is explained very well in c#0.

6. Is this a new feature?
No.



### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/eb0c0353bf245885797d8ce0d1b864d88a381fbb

commit eb0c0353bf245885797d8ce0d1b864d88a381fbb
Author: Raymond Toy <rtoy@chromium.org>
Date: Wed Feb 10 05:34:49 2021

Convert AudioParam NaN values to the default value

If any output value of an AudioParam (including the intrinsic values
and any inputs to the AudioParam), should be NaN, replace the NaN
value with the associated defaultValue.

This causes some slowdowns so SIMD/NEON code was added to mitigate the
degradation.  There is still some slowdown, but the worst case is now
about 7% slower on x86 and 10% on arm. Generally, the slowdown is less
than 2% and 5%, respectively.  (Perversely, some results got faster,
and the differences are statistically significant.)

Full details can be found at
https://docs.google.com/spreadsheets/d/1EhbLHm-9cUoEO5aj1vYemVBLQ3Dh4dCJPPLTfZPrZt4/edit?usp=sharing

Manually tested the test case from the bug and the issue no longer
occurs.

(cherry picked from commit ab1862017b5717271a28376659944dddc602195c)

Bug: 1170531
Change-Id: I00d902b40a9ef9da990c6d68b664b1dcfc31b091
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2658724
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#851733}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2686369
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4389@{#880}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/eb0c0353bf245885797d8ce0d1b864d88a381fbb/third_party/blink/renderer/modules/webaudio/audio_param.cc
[add] https://crrev.com/eb0c0353bf245885797d8ce0d1b864d88a381fbb/third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-audioparam-interface/nan-param.html


### [Deleted User] (2021-02-10)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-10)

[Empty comment from Monorail migration]

### ad...@chromium.org (2021-02-10)

I'm not going to approve merge to M88 just yet; I think new and exciting SIMD code probably requires a few more days' bake time before rolling out to stable. That probably means this will actually ship in the initial M89 release but we'll see how things go.

### am...@google.com (2021-02-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-18)

Congratulations, Cisco Talos team (especially Icewall)! The VRP Panel had decided to award y'all $7,500 for this report. Thanks for your submission and nice work!

### [Deleted User] (2021-02-18)

Thank you for the update and reward. What is the timeline for disclosure release?

### am...@google.com (2021-02-18)

Hi, regiwils@ - in most cases (unless there is a notable exception) we make the reports public 14 weeks after report status is updated to Fixed. 

### aw...@google.com (2021-02-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

Not merging to M88 - no further releases planned.

### as...@google.com (2021-03-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### gi...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### as...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3910c9f5cde621b957349209a80cc524dea74b71

commit 3910c9f5cde621b957349209a80cc524dea74b71
Author: Raymond Toy <rtoy@chromium.org>
Date: Tue Mar 02 15:15:29 2021

Convert AudioParam NaN values to the default value

If any output value of an AudioParam (including the intrinsic values
and any inputs to the AudioParam), should be NaN, replace the NaN
value with the associated defaultValue.

This causes some slowdowns so SIMD/NEON code was added to mitigate the
degradation.  There is still some slowdown, but the worst case is now
about 7% slower on x86 and 10% on arm. Generally, the slowdown is less
than 2% and 5%, respectively.  (Perversely, some results got faster,
and the differences are statistically significant.)

Full details can be found at
https://docs.google.com/spreadsheets/d/1EhbLHm-9cUoEO5aj1vYemVBLQ3Dh4dCJPPLTfZPrZt4/edit?usp=sharing

Manually tested the test case from the bug and the issue no longer
occurs.

(cherry picked from commit ab1862017b5717271a28376659944dddc602195c)

(cherry picked from commit eb0c0353bf245885797d8ce0d1b864d88a381fbb)

Bug: 1170531
Change-Id: I00d902b40a9ef9da990c6d68b664b1dcfc31b091
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2658724
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#851733}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2686369
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4389@{#880}
Cr-Original-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2727697
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1551}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/3910c9f5cde621b957349209a80cc524dea74b71/third_party/blink/renderer/modules/webaudio/audio_param.cc
[add] https://crrev.com/3910c9f5cde621b957349209a80cc524dea74b71/third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-audioparam-interface/nan-param.html


### as...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### vu...@sourcefire.com (2021-03-03)

Please update the credits on https://chromereleases.googleblog.com/ for this bug to be "Marcin 'Icewall' Noga of Cisco Talos" rather than Aleksandar Nikolic

### am...@google.com (2021-03-03)

vulndiscovery@ - sure thing! Apologies we didn't catch that in our updates process. It will be updated on the release notes blog later today. 

### vu...@sourcefire.com (2021-03-03)

Label: reward_to-manoga_at_cisco.com

### am...@google.com (2021-03-03)

Hello vulndiscovery@sourcefire folks, I see the reward-to label update from earlier today from y'all. Unfortunately, since the reward decision was made last week on this report, the payment process is already in progress and is associated with the regiwils@sourcefire account. Hopefully, there are no issues with transferring that reward internally on your side. 
In the future, to ensure payment to an individual researcher on your team, it would be best to report that bug from an individual email address that is aligned to or can be tied to that researcher on your team through our payment process. 
Please reach out with any questions or concerns. 

### vu...@sourcefire.com (2021-03-04)

Sadly we can't facilitate any transfers, there are tax implications to this especially since Marcin is in another country. We can't submit from individual email addresses, that would make it impossible for us to track any of this. Please reassign the bounty.

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-10)

vulndiscovery@ due to the details and complexities of the payment situation in our efforts to redirect the reward payment, I've sent a response off-bug via email. 

### vu...@sourcefire.com (2021-04-09)

What is the planned release date?

### am...@chromium.org (2021-04-09)

The patch was part of the M89 milestone release and the bug will be made public 14 weeks after fix (which was as of 9 February), which is around 18 May, if my math is correct. 

### [Deleted User] (2021-05-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1170531?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054571)*
