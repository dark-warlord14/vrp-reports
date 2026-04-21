# Web Audio DelayNode of an OfflineAudioContext adds one sample to the delay.

| Field | Value |
|-------|-------|
| **Issue ID** | [40053188](https://issues.chromium.org/issues/40053188) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>WebAudio |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2020-08-28 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36

Steps to reproduce the problem:
1.Open the dev tools console.
2.Run the following code:

```js
const ctx = new OfflineAudioContext({ sampleRate: 44100, length: 5 });
const osc = new ConstantSourceNode(ctx);
const gain = ctx.createDelay();
gain.delayTime.value = 3 / ctx.sampleRate;
osc.connect(gain).connect(ctx.destination);
osc.start();
ctx.startRendering()
    .then((audioBuffer) => console.log(Array.from(audioBuffer.getChannelData(0))))
```

What is the expected behavior?
The code above should log [0,0,0,1,1].

What went wrong?
The code above logs [0,0,0,0,1].

Did this work before? Yes v84

Does this work in other browsers? Yes

Chrome version: 85.0.4183.83  Channel: stable
OS Version: OS X 10.14.6
Flash Version: 

The DelayNode does still work as expected with the realtime AudioContext.

## Timeline

### rt...@chromium.org (2020-08-28)

I confirmed this.

Thanks Christoph!

### rt...@chromium.org (2020-08-28)

The issue appears to be in WrapPositionVector that doesn't seem to be wrapping the values correctly.  Some prints show that mm_cmplt_ps isn't producing the results I was expecting.

More investigation needed.

### rt...@chromium.org (2020-08-28)

I believe there's also a security issue here where we read past the end of an array.

When the position is 8320 and the buffer length is 8320, we were supposed to wrap the position back to the beginning of the buffer.  But a logic error prevented that so we would read from element 8320, which is one past the end of the buffer.

### rt...@chromium.org (2020-08-28)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-08-31)

chrisguttandin@

Thanks so much for finding this. Can I ask how you find this problem? We would like to find out how we can prevent this.

> The DelayNode does still work as expected with the realtime AudioContext.

This is a bit surprising to me. The DelayNode doesn't differentiate the context type. Also this wouldn't be a Mac-only problem.

> I believe there's also a security issue here where we read past the end of an array.

Then is this P1? Do we need to talk to the security team?

### rt...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-08-31)

[Empty comment from Monorail migration]

### ho...@chromium.org (2020-08-31)

chrisguttandin@

> The DelayNode does still work as expected with the realtime AudioContext.

I asked this question in https://crbug.com/chromium/1123023#c5, but can you confirm this? We don't think you would have a different result on the realtime context. Also this should not be platform-specific because it applies for both SSE2 and NEON.



### ch...@gmail.com (2020-08-31)

The tests that I run on the realtime context work by setting up a ScriptProcessorNode which has two inputs. It expects to receive three impulses on one of the channels. Theses impulses are expected to come in with a pre-defined delay to make sure the buffering of the ScriptProcessorNode did not change during the tests. The ScriptProcessorNode will record what it receives on the other channel during the second impulse. Each test gets repeated two times to make sure the result is consistent.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4113a81fe771768a2fff238c7d647022c555c749

commit 4113a81fe771768a2fff238c7d647022c555c749
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Aug 31 22:45:28 2020

Fix incorrect delay of DelayNode

WrapPositionVector was not wrapping the position around when it equaled
the end of the buffer.  This caused an extra zero value to be output
in this case.

Examination of WrapIndexVector also indicates a related logic error
because there's no >= intrinsic, so we used < but got the logic wrong.

The NEON version appears to be correct, so just added additional
comments to match the SSE2 version.

Added one test to make sure the delay is correct (based on the bug
report).

Bug: 1123023
Test: the-delaynode-interface/delay-test.html
Change-Id: Ibcb09573c53d62e926a332307d07601110b91aa3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2382656
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/heads/master@{#803289}

[modify] https://crrev.com/4113a81fe771768a2fff238c7d647022c555c749/third_party/blink/renderer/platform/audio/cpu/arm/audio_delay_dsp_kernel_neon.cc
[modify] https://crrev.com/4113a81fe771768a2fff238c7d647022c555c749/third_party/blink/renderer/platform/audio/cpu/x86/audio_delay_dsp_kernel_sse2.cc
[add] https://crrev.com/4113a81fe771768a2fff238c7d647022c555c749/third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-delaynode-interface/delay-test.html


### rt...@chromium.org (2020-08-31)

I think this depends a lot on where the delay node internal buffer indices are at when the realtime context gets the signals.

Christoph pointed out and I confirmed that even with an offline context, doing osc.start(1/ctx.sampleRate) has a delay of 3 samples, which is correct.  This is mostly by accident because the delay node buffer pointers are just right and the extra delay just makes things work out.  When the fix is applied, starting the source at n/ctx.sampleRate does in fact have a delay of n + 3 frames, as expected.

### rt...@chromium.org (2020-09-02)

I think I know why the realtime context may not show the extra delay.  When the context is running, the indices for the delay buffer are constantly being updated. So unless you set up everything before the delay node has processed the very first buffer, the indices will have changed such that the failed wrapping may not occur.

### rt...@chromium.org (2020-09-02)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-02)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-09-08)

The CL in c#10 fixes a case where we read past the end of an array.

Should this be merged to M86? According to omahaproxy, M87 has this fix.

### [Deleted User] (2020-09-08)

This bug requires manual review: M86's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### wf...@chromium.org (2020-09-08)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-08)

Hi rtoy@, first we should get the Security_Impact label right. In https://crbug.com/chromium/1123023#c7 you've stated that the oldest affected build is M87, perhaps inadvertently especially since the original reporter says it affects M85. Could you confirm that, as far as you understand it, this _does_ affect M85+? If so we'll set Security_Impact-Stable.

Sheriffbot would then normally request a merge to M86, and a little later, will request merge to M85. Please comment on any stability implications of doing this merge.

### rt...@chromium.org (2020-09-08)

I confirmed that with M85, the bug exists.  The output is 0,0,0,1 when it should be 0,0,1.

### ad...@google.com (2020-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-09-11)

Approving merge to M86, branch 4240, assuming this is looking good in Canary.

### rt...@chromium.org (2020-09-14)

AFAIK, there weren't any crashes caused by this and I uploaded this test to clusterfuzz and wasn't able to reproduce any issues.



### pb...@google.com (2020-09-14)

Please merge your change to M86 branch 4240 ASAP so we can take it in for this week beta release. Thank you.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4306f6b5ae1c9e1304673f601fe97564658ce9c0

commit 4306f6b5ae1c9e1304673f601fe97564658ce9c0
Author: Raymond Toy <rtoy@chromium.org>
Date: Mon Sep 14 17:55:21 2020

Fix incorrect delay of DelayNode

WrapPositionVector was not wrapping the position around when it equaled
the end of the buffer.  This caused an extra zero value to be output
in this case.

Examination of WrapIndexVector also indicates a related logic error
because there's no >= intrinsic, so we used < but got the logic wrong.

The NEON version appears to be correct, so just added additional
comments to match the SSE2 version.

Added one test to make sure the delay is correct (based on the bug
report).

(cherry picked from commit 4113a81fe771768a2fff238c7d647022c555c749)

Bug: 1123023
Test: the-delaynode-interface/delay-test.html
Change-Id: Ibcb09573c53d62e926a332307d07601110b91aa3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2382656
Reviewed-by: Dale Curtis <dalecurtis@chromium.org>
Reviewed-by: Hongchan Choi <hongchan@chromium.org>
Commit-Queue: Raymond Toy <rtoy@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#803289}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2410440
Reviewed-by: Raymond Toy <rtoy@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#670}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/4306f6b5ae1c9e1304673f601fe97564658ce9c0/third_party/blink/renderer/platform/audio/cpu/arm/audio_delay_dsp_kernel_neon.cc
[modify] https://crrev.com/4306f6b5ae1c9e1304673f601fe97564658ce9c0/third_party/blink/renderer/platform/audio/cpu/x86/audio_delay_dsp_kernel_sse2.cc
[add] https://crrev.com/4306f6b5ae1c9e1304673f601fe97564658ce9c0/third_party/blink/web_tests/external/wpt/webaudio/the-audio-api/the-delaynode-interface/delay-test.html


### ad...@google.com (2020-09-14)

[Empty comment from Monorail migration]

### rt...@chromium.org (2020-09-14)

It's landed now, per c#26.

### ad...@google.com (2020-09-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-09-16)

chrisguttandin@gmail.com thank you for reporting this. As this turned out to have security implications, our VRP panel has decided to award $3,000 for the report. Someone from our finance team will get in touch. You'll also be credited in the Chrome release notes - how would you like to be credited?

### ch...@gmail.com (2020-09-17)

Thanks @adetaylor, that's very welcome. I'll take it as a contribution to finance my open-source work which also caused me to find this bug.

You can credit me by my full name. It's Christoph Guttandin. Thanks.

### ad...@chromium.org (2020-09-17)

Will do, thank you!

### ad...@google.com (2020-09-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-12-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1123023?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053188)*
