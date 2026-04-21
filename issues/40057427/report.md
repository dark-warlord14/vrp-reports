# Security: WebAudio oob read in AudioDelayDSPKernel::ProcessKRate

| Field | Value |
|-------|-------|
| **Issue ID** | [40057427](https://issues.chromium.org/issues/40057427) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | su...@gmail.com |
| **Assignee** | ho...@chromium.org |
| **Created** | 2021-09-28 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86\_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/95.0.4628.3 Safari/537.36

**VULNERABILITY DETAILS**  

In `AudioDelayDSPKernel::ProcessKRate`, if delay\_time is `nan`, the `nan` will be propagated to `read_position`.  

After that `read_position` will be casted to int type and the value will be assigned to `read_index1`. The int value  

converted by nan is very large and definitely exceeds the buffer\_length. So `read_pointer` will point to an inaccessible  

memory and the program will crash on memcpy.

```
void AudioDelayDSPKernel::ProcessKRate(const float\* source,  
                                       float\* destination,  
                                       uint32_t frames_to_process) {  
  int buffer_length = buffer_.size();  
  float\* buffer = buffer_.Data();  
  
  // ...  
  
  float sample_rate = SampleRate();  
  double max_time = MaxDelayTime();  
  
  // ...  
  
  double delay_time = DelayTime(sample_rate);  
  // Make sure the delay time is in a valid range.  
  delay_time = clampTo(delay_time, 0.0, max_time);  
  double desired_delay_frames = delay_time \* sample_rate;  
  int w_index = write_index_;  
  double read_position = w_index + buffer_length - desired_delay_frames; // <<<<<<<<<< read_position = nan;  
  
  if (read_position >= buffer_length)  
    read_position -= buffer_length;  
  
  // Linearly interpolate in-between delay times.  |read_index1| and  
  // |read_index2| are the indices of the frames to be used for  
  // interpolation.  
  int read_index1 = static_cast<int>(read_position); // <<<<<<<<<< covert nan to a large in value  
    
  // ...  
  
  // Now copy out the samples from the buffer, starting at the read pointer,  
  // carefully handling wrapping of the read pointer.  
  float\* read_pointer = &buffer[read_index1]; // <<<<<<<<<< get an invalid pointer  
  
  uint32_t remainder = static_cast<uint32_t>(buffer_end - read_pointer);  
  memcpy(sample1, read_pointer, // <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<   crash here!!!  
         sizeof(\*sample1) \* std::min(frames_to_process, remainder));  
  // ...  

```

**VERSION**  

Chrome Version: 95.0.4628.3(dev)  

Operating System: Linux, Windows

**REPRODUCTION CASE**

1. Build release chromium without dcheck (Chromium 95.0.4628.3 is\_debug=false dcheck\_always\_on=false).
2. Serve crash.html from a server: python3 -m http.server 8605.
3. Run ./chrome <http://localhost:8605/crash.html>

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 2.0 KB)
- [crash_sym.log](attachments/crash_sym.log) (text/plain, 7.0 KB)
- [crash.html](attachments/crash.html) (text/plain, 1.4 KB)
- [audio_sample_smallest.mp3](attachments/audio_sample_smallest.mp3) (application/octet-stream, 477 B)

## Timeline

### [Deleted User] (2021-09-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-09-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>WebAudio]

### rs...@chromium.org (2021-09-29)

hongchan: Could you take a look at this? Assuming I've not botched anything, this does appear to be legitimate. In a DCHECK-enabled build, this triggers at https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/vector_math.cc;l=129-136;drc=4cd749d0d82138ff31ed3a2bc5d925bb6d83fe16

I _not_ reproduced this on all platforms, but given the shared code, setting it conservatively here.

### [Deleted User] (2021-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### su...@gmail.com (2021-09-30)

You should reproduce this on the version without DCHECK, both ASAN and Release are ok. 

And here is a patch that works, hope this will help you.

diff --git a/third_party/blink/renderer/modules/webaudio/audio_param.cc b/third_party/blink/renderer/modules/webaudio/audio_param.cc
index 671a079fcb069..4e3f4a78d839b 100644
--- a/third_party/blink/renderer/modules/webaudio/audio_param.cc
+++ b/third_party/blink/renderer/modules/webaudio/audio_param.cc
@@ -372,6 +372,7 @@ void AudioParamHandler::CalculateFinalValues(float* values,
     vector_math::Vclip(values, 1, &min_value, &max_value, values, 1,
                        number_of_values);
   }
+  HandleNaNValues(values, number_of_values, DefaultValue());
 }

 void AudioParamHandler::CalculateTimelineValues(float* values,

### ho...@chromium.org (2021-09-30)

[Empty comment from Monorail migration]

### ho...@chromium.org (2021-09-30)

From the repro case:

delay_node.delayTime.exponentialRampToValueAtTime(2, 32768);
delay_node.delayTime.cancelAndHoldAtTime(4);

This happens before the delay node makes a connection to the destination. Somehow these two lines are causing NaN somehow even without any active connections. Thus the logic in this comment is not true:
(https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_param.cc;l=361)

// AudioParams by themselves don't produce NaN because of the finite min
// and max values.  But an input to an AudioParam could have NaNs.

I'll test if the fix https://crbug.com/chromium/1253746#c6 makes sense from the audio processing performance POV.

### ho...@chromium.org (2021-09-30)

This DCHECK should not be triggered in any case, and I locally confirmed this is consistently reproducible:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/platform/audio/vector_math.cc;l=133?q=vector_math.cc

This means that the fix proposed in https://crbug.com/chromium/1253746#c6 is not really effective. Technically, NaN should not exist in the array.  I moved HandleNaNValues() function around the vector_math::Vclip() call, but still getting the same error. I suspect that HandleNaNValues() function is broken, but this needs more investigation to confirm.


### su...@gmail.com (2021-10-01)

[Comment Deleted]

### ho...@chromium.org (2021-10-04)

The crash is coming from the overlap of the automation period:

delay_node.delayTime.exponentialRampToValueAtTime(2, 4.1);
delay_node.delayTime.cancelAndHoldAtTime(4);

This is good enough to cause a crash.

Investigating further...

### ho...@chromium.org (2021-10-04)

Also I was suspicious about making a connection in onaudioprocess event, but that's not relevant to the crash.

### ho...@chromium.org (2021-10-04)

I have reduced the range of the offending code to L1045-1102 of this file:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_param_timeline.cc

A function invoked within this range is somehow cause NaN value(s) in the resulting array.

### ho...@chromium.org (2021-10-04)

I was able to pinpoint the root cause to this function:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/webaudio/audio_param_timeline.cc;l=1521

Will take a look why we're getting NaN from this.

### gi...@appspot.gserviceaccount.com (2021-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4e2dcd84dc33f29b032b52e053726ab49e4d0b4d

commit 4e2dcd84dc33f29b032b52e053726ab49e4d0b4d
Author: Hongchan Choi <hongchan@chromium.org>
Date: Wed Oct 06 15:16:37 2021

Use zero when the starting value of exponential ramp is zero

The calculation of an exponential curve is done by the specification:
https://webaudio.github.io/web-audio-api/#dom-audioparam-exponentialramptovalueattime

However, it missed a case where V0 (value1) is zero where it causes
a NaN.

Bug: 1253746,1240610
Test: third_party/blink/web_tests/webaudio/AudioParam/exponential-ramp-crash-1253746.html
Change-Id: Ib4a95f9298b4300705eda6a2eea64169de7cb002
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3205982
Reviewed-by: Ryan Sleevi <rsleevi@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/heads/main@{#928673}

[add] https://crrev.com/4e2dcd84dc33f29b032b52e053726ab49e4d0b4d/third_party/blink/web_tests/webaudio/AudioParam/exponential-ramp-crash-1253746.html
[modify] https://crrev.com/4e2dcd84dc33f29b032b52e053726ab49e4d0b4d/third_party/blink/renderer/modules/webaudio/audio_param_timeline.cc


### ho...@chromium.org (2021-10-07)

The latest Canary contains the fix in https://crbug.com/chromium/1253746#c15.

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-07)

Requesting merge to beta M95 because latest trunk commit (928673) appears to be after beta branch point (920003).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-07)

Merge review required: M95 is already shipping to beta.

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
Owners: benmason (Android), harrysouders (iOS), None (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2021-10-08)

hongchan@ please reply to questions posted in https://crbug.com/chromium/1253746#c20

### ho...@chromium.org (2021-10-08)

1. This is security problem.
2. https://chromium-review.googlesource.com/c/chromium/src/+/3205982
3. M94 crashes with the repro in https://crbug.com/chromium/1253746#c3, and Canary does not crash.
4. No.
5. N/A
6. This is a crash on the stable channel. Yes, the verification from the test team would be helpful.

### am...@chromium.org (2021-10-11)

approving for merge to M95; as long as there are no stability concerns, please go ahead and merge to branch 4638 as soon as possible so this can be included in the M95 stable cut tomorrow

### gi...@appspot.gserviceaccount.com (2021-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c69dddfe1cdede662f2b1a2d5a3c1613029a3e98

commit c69dddfe1cdede662f2b1a2d5a3c1613029a3e98
Author: Hongchan Choi <hongchan@chromium.org>
Date: Mon Oct 11 23:53:51 2021

Use zero when the starting value of exponential ramp is zero

The calculation of an exponential curve is done by the specification:
https://webaudio.github.io/web-audio-api/#dom-audioparam-exponentialramptovalueattime

However, it missed a case where V0 (value1) is zero where it causes
a NaN.

(cherry picked from commit 4e2dcd84dc33f29b032b52e053726ab49e4d0b4d)

Bug: 1253746,1240610
Test: third_party/blink/web_tests/webaudio/AudioParam/exponential-ramp-crash-1253746.html
Change-Id: Ib4a95f9298b4300705eda6a2eea64169de7cb002
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3205982
Reviewed-by: Ryan Sleevi <rsleevi@chromium.org>
Reviewed-by: Chrome Cunningham <chcunningham@chromium.org>
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#928673}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3218139
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Cr-Commit-Position: refs/branch-heads/4638@{#766}
Cr-Branched-From: 159257cab5585bc8421abf347984bb32fdfe9eb9-refs/heads/main@{#920003}

[add] https://crrev.com/c69dddfe1cdede662f2b1a2d5a3c1613029a3e98/third_party/blink/web_tests/webaudio/AudioParam/exponential-ramp-crash-1253746.html
[modify] https://crrev.com/c69dddfe1cdede662f2b1a2d5a3c1613029a3e98/third_party/blink/renderer/modules/webaudio/audio_param_timeline.cc


### am...@chromium.org (2021-10-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-10-19)

hello reporter, can you please let us know the information you would like used to acknowledge you for this issue in our release notes? Thank you.

### am...@google.com (2021-10-19)

[Empty comment from Monorail migration]

### su...@gmail.com (2021-10-19)

ok, here is the information.
sunburst@Ant Security Light-Year Lab

### am...@google.com (2021-10-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-20)

Congratulations, sunburst! The VRP Panel has decided to award you $2000 for this report. A member of our finance team will be in touch soon to arrange payment. Thank you for reporting this issue to us! 

### rz...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-21)

[Empty comment from Monorail migration]

### gi...@google.com (2021-10-25)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-10-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2a8c262b443a7086299b1deaa44d0ed058a280a8

commit 2a8c262b443a7086299b1deaa44d0ed058a280a8
Author: Hongchan Choi <hongchan@chromium.org>
Date: Tue Oct 26 13:41:34 2021

[M90-LTS] Use zero when the starting value of exponential ramp is zero

The calculation of an exponential curve is done by the specification:
https://webaudio.github.io/web-audio-api/#dom-audioparam-exponentialramptovalueattime

However, it missed a case where V0 (value1) is zero where it causes
a NaN.

(cherry picked from commit 4e2dcd84dc33f29b032b52e053726ab49e4d0b4d)

Bug: 1253746,1240610
Test: third_party/blink/web_tests/webaudio/AudioParam/exponential-ramp-crash-1253746.html
Change-Id: Ib4a95f9298b4300705eda6a2eea64169de7cb002
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3205982
Commit-Queue: Hongchan Choi <hongchan@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#928673}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3234533
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1645}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[add] https://crrev.com/2a8c262b443a7086299b1deaa44d0ed058a280a8/third_party/blink/web_tests/webaudio/AudioParam/exponential-ramp-crash-1253746.html
[modify] https://crrev.com/2a8c262b443a7086299b1deaa44d0ed058a280a8/third_party/blink/renderer/modules/webaudio/audio_param_timeline.cc


### rz...@google.com (2021-10-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1253746?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057427)*
