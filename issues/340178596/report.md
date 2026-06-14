# heap-use-after-free on AudioManagerMac

| Field | Value |
|-------|-------|
| **Issue ID** | [340178596](https://issues.chromium.org/issues/340178596) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ol...@chromium.org |
| **Created** | 2024-05-13 |
| **Bounty** | $2,000.00 |

## Description

VULNERABILITY DETAILS

The specific vulnerability is the same as https://issues.chromium.org/issues/40065022,
AudioManagerMac::HandleDeviceChanges bind as unretaied, so there may be UAF during competition. Because the calling paths are different, ASAN is still reproducing, but the vulnerability is exactly the same as 40065022. You can see the obvious problem directly in the code.

AudioOutputStream* AudioManagerMac::MakeLowLatencyOutputStream(
    const AudioParameters& params,
    const std::string& device_id,
    const LogCallback& log_callback) {
  DCHECK(GetTaskRunner()->BelongsToCurrentThread());
  bool device_listener_first_init = false;
  // Lazily create the audio device listener on the first stream creation,
  // even if getting an audio device fails. Otherwise, if we have 0 audio
  // devices, the listener will never be initialized, and new valid devices
  // will never be detected.
  if (!output_device_listener_) {
    // NOTE: Use base::BindPostTaskToCurrentDefault() to ensure the callback is
    // always PostTask'd even if OSX calls us on the right thread.  Some
    // CoreAudio drivers will fire the callbacks during stream creation, leading
    // to re-entrancy issues otherwise.  See http://crbug.com/349604
    output_device_listener_ = AudioDeviceListenerMac::Create(
        base::BindPostTaskToCurrentDefault(base::BindRepeating(
            &AudioManagerMac::HandleDeviceChanges, base::Unretained(this))), //[0]
        /*monitor_sample_rate_changes=*/
        base::FeatureList::IsEnabled(kMonitorOutputSampleRateChangesMac),
        /*monitor_default_input=*/false,
        /*monitor_addition_removal=*/false,
        /*monitor_sources=*/false);
    device_listener_first_init = true;
  }

  AudioDeviceID device = GetAudioDeviceIdByUId(false, device_id);
  if (device == kAudioObjectUnknown) {
    DLOG(ERROR) << "Failed to open output device: " << device_id;
    return NULL;
  }

  // Only set the device and sample rate if we just initialized the device
  // listener.
  if (device_listener_first_init) {
    // Only set the current output device for the default device.
    if (AudioDeviceDescription::IsDefaultDevice(device_id)) {
      current_output_device_ = device;
    }
    // Just use the current sample rate since we don't allow non-native sample
    // rates on OSX.
    current_sample_rate_ = params.sample_rate();
  }

  AUHALStream* stream = new AUHALStream(this, params, device, log_callback);
  output_streams_.insert(stream);
  return stream;
}

fix
see issue 40065022



## Timeline

### ad...@google.com (2024-05-13)

Yep, I can't see any reason why this same issue wouldn't occur here. Rating the same severity and FoundIn.

### ha...@gmail.com (2024-05-14)

Yes, this vulnerability is obvious. The steps to reproduce are the same as 40065022, but I am missing a speaker, so I cannot give the ASAN.

### pe...@google.com (2024-05-14)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-14)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-15)

Project: chromium/src
Branch: main

commit 6d95935f83b1296e45c7f4cc2b64108a81865601
Author: Olga Sharonova <olka@chromium.org>
Date:   Wed May 15 14:59:21 2024

    Use weak_ptr<AudioManagerMac> to configure AudioDeviceListenerMac
    
    See the bug and https://g-issues.chromium.org/issues/40065022#comment33
    
    Bug: 340178596,40065022
    Change-Id: I02402519d4f73d035cd3b7a0f3f04ce353f755fd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5538281
    Reviewed-by: Fredrik Hernqvist <fhernqvist@google.com>
    Commit-Queue: Fredrik Hernqvist <fhernqvist@google.com>
    Auto-Submit: Olga Sharonova <olka@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1301300}

M       media/audio/mac/audio_manager_mac.cc

https://chromium-review.googlesource.com/5538281


### pe...@google.com (2024-05-20)

Merge review required: M126 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

### pe...@google.com (2024-05-20)

Merge review required: M125 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

### ol...@google.com (2024-05-20)

I'm not sure re: cherry-picking to M125. It's a shutdown crash of the audio process, which would happen only on the whole browser shutdown, as far as I can see.

### ol...@google.com (2024-05-20)

M126:

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?
   A security issue.
2. What changes specifically would you like to merge? Please link to Gerrit.
   <https://chromium-review.googlesource.com/c/chromium/src/+/5538281>
3. Have the changes been released and tested on canary?
   Yes
4. Is this a new feature?
   no

### ol...@google.com (2024-05-20)

M125:

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

An audio process (sandboxed) crash on the browser shutdown.
"important security issues (medium severity or higher) requested by the security team."

2. What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.googlesource.com/c/chromium/src/+/5538281>

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature?

No

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team?

No

### am...@chromium.org (2024-05-21)

M126 Beta merges approved for <https://chromium-review.googlesource.com/c/chromium/src/+/5538281>
Please merge this fix at soonest to branch 6478 (M126) by EOD today so this fix can be included in tomorrow's M126 Beta update.

I saw renderer UAF and the bot had updated this as merge review for M125, and went into approval autopilot, but seeing as how this is mitigated by requiring shutdown and reviewing the context of the previous variant of this issue, I agree this probably doesn't warrant merging to Stable, which is already mid-lifecycle.

### ap...@google.com (2024-05-22)

Project: chromium/src
Branch: refs/branch-heads/6478

commit f9ea2265267c653ce0c789662b527b17af022eac
Author: Olga Sharonova <olka@chromium.org>
Date:   Wed May 22 12:57:51 2024

    [M126] Use weak_ptr<AudioManagerMac> to configure AudioDeviceListenerMac
    
    See the bug and https://g-issues.chromium.org/issues/40065022#comment33
    
    (cherry picked from commit 6d95935f83b1296e45c7f4cc2b64108a81865601)
    
    Bug: 340178596,40065022
    Change-Id: I02402519d4f73d035cd3b7a0f3f04ce353f755fd
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5538281
    Reviewed-by: Fredrik Hernqvist <fhernqvist@google.com>
    Commit-Queue: Fredrik Hernqvist <fhernqvist@google.com>
    Auto-Submit: Olga Sharonova <olka@chromium.org>
    Cr-Original-Commit-Position: refs/heads/main@{#1301300}
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5554599
    Commit-Queue: Olga Sharonova <olka@chromium.org>
    Cr-Commit-Position: refs/branch-heads/6478@{#423}
    Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

M       media/audio/mac/audio_manager_mac.cc

https://chromium-review.googlesource.com/5554599


### ol...@google.com (2024-05-22)

(Could not make it yesterday - was approved way outside of my working hours.)

### sp...@google.com (2024-06-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of highly mitigated bug in a non-sandboxed process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-27)

Thank you for your efforts and reporting this issue to us! 

### pe...@google.com (2024-08-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/340178596)*
