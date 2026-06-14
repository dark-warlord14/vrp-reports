# Crash in blink::WaveShaperDSPKernel::WaveShaperCurveValues

| Field | Value |
|-------|-------|
| **Issue ID** | [40052178](https://issues.chromium.org/issues/40052178) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | rt...@chromium.org |
| **Created** | 2020-05-02 |
| **Bounty** | $3,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5676738657452032

Fuzzer: attekett_webaudio_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x632e00118800
Crash State:
  blink::WaveShaperDSPKernel::WaveShaperCurveValues
  blink::WaveShaperDSPKernel::Process
  blink::WaveShaperProcessor::Process
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=764264:764275

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5676738657452032

Issue filed automatically.

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5676738657452032 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2020-05-02)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>WebAudio]

### cl...@chromium.org (2020-05-02)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/d0332aa7414acb1c14794f76a5310ac8cdc9af52 (Vectorize WaveShaper interpolator).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### [Deleted User] (2020-05-02)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-02)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2020-05-04)

Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns.

### rt...@chromium.org (2020-05-05)

Unable to reproduce this on my linux box.  And the using the clusterfuzz reproduce tool fails because I can't authenticate (Oauth client disabled).  (Feedback filed).

I'm guessing, based on the line number that i1[3] is out-of-bounds.  

### am...@google.com (2020-05-05)

Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns.

### rt...@chromium.org (2020-05-05)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-05-06)

[Empty comment from Monorail migration]

### am...@google.com (2020-05-07)

Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns.

### am...@google.com (2020-05-07)

A prior comment / related label was applied to this bug: "Please ignore, no action required - we are testing automation around potential SLOs for release blockers.  Email me with any concerns."

This wording was poor - the *comment and the label RB-SLO-<Fix|Comment>* should be ignored, but this bug is still considered a release blocker that should be fixed as quickly as possible.  *Please do not ignore this bug* and continue to work on it as a top priority.

I apologize for any confusion this may have caused, and the new comment applied to bugs by this automation that is being tested will be more clear: "Please ignore this comment and the new label, and continue to work on this release blocking bug urgently - we are testing automation around potential SLOs for release blockers.  Email me with any concerns."

### at...@gmail.com (2020-05-08)

Did you manage to reproduce this issue?

I see it also on my fuzzing cluster with different fingerprints, but I haven't been able to reliably reproduce it.

If you managed to reproduce it reliably, what was needed for it?

FWIW, few fingerprints I have:

==19686==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602e000023e0 at pc 0x55f5b80ae233 bp 0x7ffa7a4afef0 sp 0x7ffa7a4afee8
READ of size 4 at 0x602e000023e0 thread T30 (AudioOutputDevi)
    #0 0x55f5b80ae232 in blink::WaveShaperDSPKernel::WaveShaperCurveValues(float*, float const*, unsigned int, float const*, int) const third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:178:19
    #1 0x55f5b80ad55f in ProcessCurve third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:238:3
    #2 0x55f5b80ad55f in ProcessCurve2x third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:252:3
    #3 0x55f5b80ad55f in blink::WaveShaperDSPKernel::Process(float const*, float*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:69:7
    #4 0x55f5b80acc3b in blink::WaveShaperProcessor::Process(blink::AudioBus const*, blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_processor.cc:109:20
    #5 0x55f5b80962e8 in blink::AudioBasicProcessorHandler::Process(unsigned int) third_party/blink/renderer/modules/webaudio/audio_basic_processor_handler.cc:85:18
.
.
.

=================================================================
==27626==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x621e00006100 at pc 0x55dac1f03233 bp 0x7fd7cb3dbef0 sp 0x7fd7cb3dbee8
READ of size 4 at 0x621e00006100 thread T57 (AudioOutputDevi)
    #0 0x55dac1f03232 in blink::WaveShaperDSPKernel::WaveShaperCurveValues(float*, float const*, unsigned int, float const*, int) const third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:178:19
    #1 0x55dac1f027be in ProcessCurve third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:238:3
    #2 0x55dac1f027be in blink::WaveShaperDSPKernel::ProcessCurve4x(float const*, float*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:269:3
    #3 0x55dac1f01c3b in blink::WaveShaperProcessor::Process(blink::AudioBus const*, blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_processor.cc:109:20
    #4 0x55dac1eeb2e8 in blink::AudioBasicProcessorHandler::Process(unsigned int) third_party/blink/renderer/modules/webaudio/audio_basic_processor_handler.cc:85:18
.
.
.

=================================================================
==3047==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x617e0000ec80 at pc 0x55d36bfd921f bp 0x7f576f4cc4b0 sp 0x7f576f4cc4a8
READ of size 4 at 0x617e0000ec80 thread T39 (AudioOutputDevi)
    #0 0x55d36bfd921e in blink::WaveShaperDSPKernel::WaveShaperCurveValues(float*, float const*, unsigned int, float const*, int) const third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:176:15
    #1 0x55d36bfd7c3b in blink::WaveShaperProcessor::Process(blink::AudioBus const*, blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_processor.cc:109:20
    #2 0x55d36bfc12e8 in blink::AudioBasicProcessorHandler::Process(unsigned int) third_party/blink/renderer/modules/webaudio/audio_basic_processor_handler.cc:85:18
.
.
.

=================================================================
==100==ERROR: AddressSanitizer: SEGV on unknown address 0x602e000bb210 (pc 0x559721284c7e bp 0x7f057c64ee10 sp 0x7f057c64dc60 T101)
==100==The signal is caused by a READ memory access.
    #0 0x559721284c7e in blink::WaveShaperDSPKernel::WaveShaperCurveValues(float*, float const*, unsigned int, float const*, int) const third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:178:19
    #1 0x55972128455f in ProcessCurve third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:238:3
    #2 0x55972128455f in ProcessCurve2x third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:252:3
    #3 0x55972128455f in blink::WaveShaperDSPKernel::Process(float const*, float*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc:69:7
    #4 0x559721283c3b in blink::WaveShaperProcessor::Process(blink::AudioBus const*, blink::AudioBus*, unsigned int) third_party/blink/renderer/modules/webaudio/wave_shaper_processor.cc:109:20
    #5 0x55972126d2e8 in blink::AudioBasicProcessorHandler::Process(unsigned int) third_party/blink/renderer/modules/webaudio/audio_basic_processor_handler.cc:85:18
.
.
.

### rt...@chromium.org (2020-05-08)

No, I haven't been able to reproduce this locally.

But all the reports point to the lines v[k+n] = curve_data(i1[n]).

I think these are all caused by i1[n] being 0x8000000.

I have a CL up for this, but I'm waiting for the reviewer to finish.  I can't test it myself, so I'm hoping clusterfuzz will be able to check the issue to see if it's fixed.


### am...@google.com (2020-05-08)

Please ignore this comment and the new label, and continue to work on this blocking bug urgently - we are testing automation around potential SLOs for release blockers.  Email me with any concerns.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0cf9bfc48ad1cc20c0bd67699871ca3f44c42362

commit 0cf9bfc48ad1cc20c0bd67699871ca3f44c42362
Author: Raymond Toy <rtoy@chromium.org>
Date: Fri May 08 17:57:20 2020

Fix loop and indexing for WaveShaper curve computation

First, there's one error in the loop in WaveShaperCurveValues.  If
frames_to_process were, say, 7, then the main loop would get executed
for k = 0 and 4.  However, in the second loop we would process 4
samples at a time, but there are only 3 left, so we'd potentially read
past the end of an array and also write past the end of an array.
Change the loop so that this won't happen.

Second, there might be a case where the indices (index1) are
out-of-bound.  Clamp these, as we do for index2.

This is a tentative fix for the bug.  I can't reproduce this myself.

Bug: 1077491
Change-Id: I90275e9f920c61591c299fbf1fb9c2eed1bf6b16
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2181755
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#766895}

[modify] https://crrev.com/0cf9bfc48ad1cc20c0bd67699871ca3f44c42362/third_party/blink/renderer/modules/webaudio/wave_shaper_dsp_kernel.cc


### cl...@chromium.org (2020-05-09)

ClusterFuzz testcase 5676738657452032 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=766894:766895

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-05-09)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-14)

Congrats! The Panel decided to award $2,000  + $1,000 fuzzing bonus for this report. 


### na...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### at...@gmail.com (2020-05-16)

Just a note. I'm going to donate this reward to charity, so please do not process it normally.

### [Deleted User] (2020-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1077491?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052178)*
