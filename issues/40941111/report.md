# Security: WebAudio UAF caused by setSinkId

| Field | Value |
|-------|-------|
| **Issue ID** | [40941111](https://issues.chromium.org/issues/40941111) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | su...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2023-11-09 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

This is another triggering way for <https://crbug.com/chromium/1497859>. <https://crbug.com/chromium/1497859> just patched `RealtimeAudioDestinationHandler::SetChannelCount`, but there is a same problem in `RealtimeAudioDestinationHandler::SetSinkDescriptor`.

```
void RealtimeAudioDestinationHandler::SetSinkDescriptor(  
    const WebAudioSinkDescriptor& sink_descriptor,  
    media::OutputDeviceStatusCB callback) {  
  TRACE_EVENT1("webaudio", "RealtimeAudioDestinationHandler::SetSinkDescriptor",  
               "sink information (when descriptor change requested)",  
               audio_utilities::GetSinkInfoForTracing(  
                  sink_descriptor, latency_hint_, MaxChannelCount(),  
                  sample_rate_.has_value() ? sample_rate_.value() : -1,  
                  GetCallbackBufferSize()));  
  DCHECK(IsMainThread());  
  
  // Create a pending AudioDestination to replace the current one.  
  scoped_refptr<AudioDestination> pending_platform_destination =  
      AudioDestination::Create(  
          \*this, sink_descriptor, ChannelCount(), latency_hint_, sample_rate_,  
          Context()->GetDeferredTaskHandler().RenderQuantumFrames());  
  
  // With this pending AudioDestination, create and initialize an underlying  
  // sink in order to query the device status. If the status is OK, then replace  
  // the `platform_destination_` with the pending_platform_destination.  
  media::OutputDeviceStatus status =  
      pending_platform_destination->CreateSinkAndGetDeviceStatus();  
  if (status == media::OutputDeviceStatus::OUTPUT_DEVICE_STATUS_OK) {               <= destination recreation  
    StopPlatformDestination();  
    platform_destination_ = pending_platform_destination;  
    sink_descriptor_ = sink_descriptor;  
    StartPlatformDestination();  
  }  
  
  std::move(callback).Run(status);  
}  

```

**VERSION**  

Chrome Version: 119.0.6045.124 stable  

Operating System: Windows 11

**REPRODUCTION CASE**

run chrome with "--use-fake-ui-for-media-stream"

see crash.html

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State:

```
(2754.2410): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
chrome!std::__Cr::__cxx_atomic_fetch_sub [inlined in chrome!scoped_refptr<blink::AudioBus>::operator=+0x2d]:  
00007ffd`87e506ad f0ff0f          lock dec dword ptr [rdi] ds:00007ffd`8508bcc0=28ec8348  
0:015> k  
 # Child-SP          RetAddr               Call Site  
00 (Inline Function) --------`--------     chrome!std::__Cr::__cxx_atomic_fetch_sub [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__atomic\cxx_atomic_impl.h @ 462]   
01 (Inline Function) --------`--------     chrome!std::__Cr::__atomic_base<int,1>::fetch_sub [C:\b\s\w\ir\cache\builder\src\third_party\libc++\src\include\__atomic\atomic_base.h @ 171]   
02 (Inline Function) --------`--------     chrome!base::AtomicRefCount::Decrement [C:\b\s\w\ir\cache\builder\src\base\atomic_ref_count.h @ 43]   
03 (Inline Function) --------`--------     chrome!base::subtle::RefCountedThreadSafeBase::ReleaseImpl [C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 236]   
04 (Inline Function) --------`--------     chrome!base::subtle::RefCountedThreadSafeBase::Release [C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 184]   
05 (Inline Function) --------`--------     chrome!base::RefCountedThreadSafe<blink::AudioBus,WTF::DefaultThreadSafeRefCountedTraits<blink::AudioBus> >::Release [C:\b\s\w\ir\cache\builder\src\base\memory\ref_counted.h @ 415]   
06 (Inline Function) --------`--------     chrome!scoped_refptr<blink::AudioBus>::Release [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 382]   
07 (Inline Function) --------`--------     chrome!scoped_refptr<blink::AudioBus>::~scoped_refptr+0x5 [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 280]   
08 (Inline Function) --------`--------     chrome!scoped_refptr<blink::AudioBus>::operator=+0xb [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 306]   
09 00000078`0a5feb60 00007ffd`87e50640     chrome!scoped_refptr<blink::AudioBus>::operator=+0x2d [C:\b\s\w\ir\cache\builder\src\base\memory\scoped_refptr.h @ 300]   
0a 00000078`0a5feba0 00007ffd`884c4ea2     chrome!blink::AudioNodeOutput::Pull+0x40 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_output.cc @ 134]   
0b 00000078`0a5febe0 00007ffd`7d501523     chrome!blink::AudioNodeInput::SumAllConnections+0x42 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc @ 135]   
0c 00000078`0a5fec30 00007ffd`87e4fe35     chrome!blink::AudioNodeInput::Pull+0x73 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc @ 162]   
0d 00000078`0a5fec60 00007ffd`81097a26     chrome!blink::AudioHandler::PullInputs+0x65 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_handler.cc @ 386]   
0e 00000078`0a5fecd0 00007ffd`87e50657     chrome!blink::AudioHandler::ProcessIfNecessary+0x116 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_handler.cc @ 334]   
0f 00000078`0a5fedf0 00007ffd`884c4ea2     chrome!blink::AudioNodeOutput::Pull+0x57 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_output.cc @ 135]   
10 00000078`0a5fee30 00007ffd`7d501523     chrome!blink::AudioNodeInput::SumAllConnections+0x42 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc @ 135]   
11 00000078`0a5fee80 00007ffd`7d500fe6     chrome!blink::AudioNodeInput::Pull+0x73 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\audio_node_input.cc @ 162]   
12 00000078`0a5feeb0 00007ffd`885050b3     chrome!blink::RealtimeAudioDestinationHandler::Render+0x106 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\webaudio\realtime_audio_destination_handler.cc @ 225]   
13 00000078`0a5fefd0 00007ffd`83181566     chrome!blink::AudioDestination::ProvideResamplerInput+0x33 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc @ 547]   
14 00000078`0a5ff000 00007ffd`83181566     chrome!base::RepeatingCallback<void (int, media::AudioBus \*)>::Run+0x36 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 336]   
15 00000078`0a5ff030 00007ffd`83181566     chrome!base::RepeatingCallback<void (int, media::AudioBus \*)>::Run+0x36 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 336]   
16 00000078`0a5ff060 00007ffd`83194744     chrome!base::RepeatingCallback<void (int, media::AudioBus \*)>::Run+0x36 [C:\b\s\w\ir\cache\builder\src\base\functional\callback.h @ 336]   
17 00000078`0a5ff090 00007ffd`8318ea75     chrome!media::SincResampler::Resample+0xd4 [C:\b\s\w\ir\cache\builder\src\media\base\sinc_resampler.cc @ 283]   
18 00000078`0a5ff1c0 00007ffd`7dd8e5a6     chrome!media::MultiChannelResampler::Resample+0xe5 [C:\b\s\w\ir\cache\builder\src\media\base\multi_channel_resampler.cc @ 68]   
19 00000078`0a5ff220 00007ffd`7dd8daae     chrome!blink::AudioDestination::RequestRender+0x326 [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc @ 528]   
1a 00000078`0a5ff350 00007ffd`7f5b111a     chrome!blink::AudioDestination::Render+0x18e [C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\audio\audio_destination.cc @ 206]   
1b 00000078`0a5ff4b0 00007ffd`7de8a42b     chrome!content::RendererWebAudioDeviceImpl::Render+0x5a [C:\b\s\w\ir\cache\builder\src\content\renderer\media\renderer_webaudiodevice_impl.cc @ 286]   
1c 00000078`0a5ff530 00007ffd`7db005a2     chrome!media::SilentSinkSuspender::Render+0x9b [C:\b\s\w\ir\cache\builder\src\media\base\silent_sink_suspender.cc @ 86]   
1d 00000078`0a5ff5f0 00007ffd`7d80886d     chrome!media::AudioOutputDeviceThreadCallback::Process+0xd2 [C:\b\s\w\ir\cache\builder\src\media\audio\audio_output_device_thread_callback.cc @ 96]   
1e 00000078`0a5ff6f0 00007ffd`7d7604cc     chrome!media::AudioDeviceThread::ThreadMain+0xbd [C:\b\s\w\ir\cache\builder\src\media\audio\audio_device_thread.cc @ 110]   
1f 00000078`0a5ff790 00007ffd`e34a257d     chrome!base::`anonymous namespace'::ThreadFunc+0x11c [C:\b\s\w\ir\cache\builder\src\base\threading\platform_thread_win.cc @ 126]   
20 00000078`0a5ff820 00007ffd`e46aaa78     KERNEL32!BaseThreadInitThunk+0x1d  
21 00000078`0a5ff850 00000000`00000000     ntdll!RtlUserThreadStart+0x28  

```

**CREDIT INFORMATION**

Reporter credit: Huang Xilin of Ant Group Light-Year Security Lab

## Attachments

- [crash.html](attachments/crash.html) (text/plain, 1.3 KB)

## Timeline

### [Deleted User] (2023-11-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-09)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5992117118107648.

### su...@gmail.com (2023-11-10)

This issue was introduced in https://chromium.googlesource.com/chromium/src/+/751b533743c567cc069f12da53e4470f51008e7a

### cl...@chromium.org (2023-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>WebAudio]

### cl...@chromium.org (2023-11-10)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/0b49ac93c05ff8c9d64c75d0123a7c0e901788ed (Reject pending setSinkId requests with valid ExceptionContext).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2023-11-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5992117118107648

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free WRITE 1
Crash Address: 0x50f00005dd90
Crash State:
  blink::AudioNodeOutput::Pull
  blink::AudioNodeInput::SumAllConnections
  blink::AudioNodeInput::Pull
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1094658:1094695

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5992117118107648

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### al...@chromium.org (2023-11-10)

[Empty comment from Monorail migration]

### ho...@chromium.org (2023-11-10)

It's UAF, so let's treat it as P1.

### gi...@appspot.gserviceaccount.com (2023-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0f9bb9a1083865d4e51059e588f27f729ab32753

commit 0f9bb9a1083865d4e51059e588f27f729ab32753
Author: Alvin Ji <alvinji@chromium.org>
Date: Fri Nov 10 22:36:52 2023

Check context status before creating new platform destination

RealtimeAudioDestinationHandler::SetSinkDescriptor creates new
destination platofrm without validating context status. This can
reactivate the audio rendering thread when AudioContext is already in
closed state.

Bug: 1500856
Change-Id: If1fd531324b56fcdc38d315fd84d4cec577a14bc
Test: Locally confirmed with ASAN
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5021160
Reviewed-by: Alvin Ji <alvinji@chromium.org>
Commit-Queue: Alvin Ji <alvinji@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1223168}

[modify] https://crrev.com/0f9bb9a1083865d4e51059e588f27f729ab32753/third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc


### al...@chromium.org (2023-11-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-11-11)

ClusterFuzz testcase 5992117118107648 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1223161:1223169

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-11)

Requesting merge to extended stable M118 because latest trunk commit (1223168) appears to be after extended stable branch point (1192594).

Requesting merge to stable M119 because latest trunk commit (1223168) appears to be after stable branch point (1204232).

Requesting merge to beta M120 because latest trunk commit (1223168) appears to be after beta branch point (1217362).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-11)

Merge review required: M120 is already shipping to beta.

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

### [Deleted User] (2023-11-11)

Merge review required: M119 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-11-11)

Merge review required: M118 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-11-13)

120 merge approved for https://crrev.com/c/5021160 -- please merge this fix to M120 / branch 6099 so this fix can be included in this week's 120 Beta update

There is release freeze next week, and this week's Stable RC was cut on Friday, so I'll re-evaulate this fix for Stable and Extended Stable merge later this week (after Stable release) to be included in the next updates following next week's freeze 

### gi...@appspot.gserviceaccount.com (2023-11-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3f45b1af5e414fc01018584f7ed4ae642172aec0

commit 3f45b1af5e414fc01018584f7ed4ae642172aec0
Author: Alvin Ji <alvinji@chromium.org>
Date: Mon Nov 13 20:24:24 2023

Check context status before creating new platform destination

RealtimeAudioDestinationHandler::SetSinkDescriptor creates new
destination platofrm without validating context status. This can
reactivate the audio rendering thread when AudioContext is already in
closed state.

(cherry picked from commit 0f9bb9a1083865d4e51059e588f27f729ab32753)

Bug: 1500856
Change-Id: If1fd531324b56fcdc38d315fd84d4cec577a14bc
Test: Locally confirmed with ASAN
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5021160
Reviewed-by: Alvin Ji <alvinji@chromium.org>
Commit-Queue: Alvin Ji <alvinji@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1223168}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5026373
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#607}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/3f45b1af5e414fc01018584f7ed4ae642172aec0/third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc


### am...@google.com (2023-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-16)

Congratulations Huang Xilin on your nice follow-up to your Tianful Cup 2023 bug (and congratulations on that as well!) ! The Chrome VRP Panel has decided to award you $10,000 for this report. Thank you for your efforts and reporting this issue to us -- excellent work!

### am...@chromium.org (2023-11-16)

119 and 118 merges approved for https://crrev.com/c/5021160, please go ahead and merge this fix to M119/ branch 6045 and M118/ branch 5993 at your earliest convenience. Since release freeze beings tomorrow through next week, this fix will be included in the next M119 Stable and M118 Extended Stable security updates the following Tuesday. Thanks! 

### gi...@appspot.gserviceaccount.com (2023-11-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e0ade1941c6a07cf865c33678a056c6ce7f048a1

commit e0ade1941c6a07cf865c33678a056c6ce7f048a1
Author: Alvin Ji <alvinji@chromium.org>
Date: Thu Nov 16 23:20:11 2023

Check context status before creating new platform destination

RealtimeAudioDestinationHandler::SetSinkDescriptor creates new
destination platofrm without validating context status. This can
reactivate the audio rendering thread when AudioContext is already in
closed state.

(cherry picked from commit 0f9bb9a1083865d4e51059e588f27f729ab32753)

Bug: 1500856
Change-Id: If1fd531324b56fcdc38d315fd84d4cec577a14bc
Test: Locally confirmed with ASAN
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5021160
Reviewed-by: Alvin Ji <alvinji@chromium.org>
Commit-Queue: Alvin Ji <alvinji@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1223168}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5038792
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/6045@{#1382}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/e0ade1941c6a07cf865c33678a056c6ce7f048a1/third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc


### gi...@appspot.gserviceaccount.com (2023-11-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6dcaa80f5ebad73b773801845098b16cdadf9295

commit 6dcaa80f5ebad73b773801845098b16cdadf9295
Author: Alvin Ji <alvinji@chromium.org>
Date: Fri Nov 17 00:56:14 2023

Check context status before creating new platform destination

RealtimeAudioDestinationHandler::SetSinkDescriptor creates new
destination platofrm without validating context status. This can
reactivate the audio rendering thread when AudioContext is already in
closed state.

(cherry picked from commit 0f9bb9a1083865d4e51059e588f27f729ab32753)

Bug: 1500856
Change-Id: If1fd531324b56fcdc38d315fd84d4cec577a14bc
Test: Locally confirmed with ASAN
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5021160
Reviewed-by: Alvin Ji <alvinji@chromium.org>
Commit-Queue: Alvin Ji <alvinji@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1223168}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5037917
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/5993@{#1619}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/6dcaa80f5ebad73b773801845098b16cdadf9295/third_party/blink/renderer/modules/webaudio/realtime_audio_destination_handler.cc


### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1500856?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40941111)*
