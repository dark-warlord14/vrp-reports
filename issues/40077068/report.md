# Heap-use-after-free in WebCore::AudioNodeOutput::pull

| Field | Value |
|-------|-------|
| **Issue ID** | [40077068](https://issues.chromium.org/issues/40077068) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-03-01 |
| **Bounty** | $3,133.00 |

## Description


Tested on:

OS: Ubuntu 12.04
Chromium: ASAN 27.0.1427.0 (Developer Build 185590)

Repro-file:

<script>
var Context0= new webkitAudioContext()
var Analyser0=Context0.createAnalyser();
var WaveShaper0=Context0.createWaveShaper();
var Convolver3=Context0.createConvolver();
Analyser0.connect(WaveShaper0);

WaveShaper0.connect(Context0.destination);
Convolver3.connect(Analyser0);

setInterval(function(){
Analyser0.disconnect();
},4)
setTimeout(function(){location.reload()},1000)
</script>


ASAN-report:

==21345== ERROR: AddressSanitizer: heap-use-after-free on address 0x600c00047cc8 at pc 0x7f8b8a72c3fe bp 0x7f8b54cea280 sp 0x7f8b54cea278
READ of size 8 at 0x600c00047cc8 thread T13 (AudioOutputDevi)
    #0 0x7f8b8a72c3fd in WebCore::AudioNodeOutput::pull(WebCore::AudioBus*, unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/Vector.h:547:0
    #1 0x7f8b8a726dc6 in WebCore::AudioNode::processIfNecessary(unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioNode.cpp:300:0
    #2 0x7f8b8b09baec in WebCore::AudioContext::processAutomaticPullNodes(unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioContext.cpp:932:0
    #3 0x7f8b8b4879f1 in WebCore::AudioDestinationNode::render(WebCore::AudioBus*, WebCore::AudioBus*, unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioDestinationNode.cpp:86:0
    #4 0x7f8b8d8af7b2 in WebCore::AudioPullFIFO::consume(WebCore::AudioBus*, unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/platform/audio/AudioPullFIFO.cpp:65:0
.
.
.
freed by thread T13 (AudioOutputDevi) here:
    #0 0x7f8b8716d482 in operator delete(void*) ??:0
    #1 0x7f8b8a72bf03 in WebCore::AudioNodeOutput::updateNumberOfChannels() /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/OwnPtrCommon.h:63:0
    #2 0x7f8b8b480a86 in WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput(WebCore::AudioNodeInput*) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioBasicProcessorNode.cpp:124:0
    #3 0x7f8b8a734474 in WebCore::AudioSummingJunction::updateRenderingState() /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioSummingJunction.cpp:74:0
    #4 0x7f8b8b099f6b in WebCore::AudioContext::handleDirtyAudioSummingJunctions() /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioContext.cpp:874:0
.
.
.


## Attachments

- [chrome-heap-use-after-free-WebCoreAudioNodeOutputpull10.html](attachments/chrome-heap-use-after-free-WebCoreAudioNodeOutputpull10.html) (text/html; charset=us-ascii, 23.6 KB)

## Timeline

### in...@chromium.org (2013-03-04)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-04)

ClusterFuzz report pending, will be at https://cluster-fuzz.appspot.com/testcase?key=169025003

antonm seems to own most of WebCore::AudioNodeOutput::pull.

According to ClusterFuzz, this is a very recent (Canary/27) regression.

### pa...@google.com (2013-03-04)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=169025003

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60180015ba88
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioNode::processIfNecessary
  - free stack -
  WebCore::AudioNodeOutput::updateNumberOfChannels
  WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput
  

Minimized Testcase (0.38 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95lhWl9_BW1AbcZMe8Dgb4VNN6rWpGPUZqq9wGmf6Obh6Dc_i7vaolKVxdUNpohxWZLviPqld_pHM79dUXWn0CB5jnEIbKULtlmTjxcKv4K2SQjctXYRQiy3IS2luznASDy6L8On85Brn0DgnZC8kuHeyb8TVD_YAjQLeSj1jkqlXRNAyQ
<script>
var Context0= new webkitAudioContext()
var Analyser0=Context0.createAnalyser();
var WaveShaper0=Context0.createWaveShaper();
var Convolver3=Context0.createConvolver();
Analyser0.connect(WaveShaper0);

WaveShaper0.connect(Context0.destination);
Convolver3.connect(Analyser0);

setInterval(function(){
Analyser0.disconnect();
},4)
setTimeout(function(){location.reload()},1000)
</script>

### pa...@chromium.org (2013-03-04)

Upstreamed: https://bugs.webkit.org/show_bug.cgi?id=111362

### [Deleted User] (2013-03-05)

+xingnan
could you grant the access of this issue to xingnan? thanks 



### in...@chromium.org (2013-03-05)

done!

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-03-15)

ClusterFuzz has detected this issue as fixed in range 187778:187880.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=169025003

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60180015ba88
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioNode::processIfNecessary
  - free stack -
  WebCore::AudioNodeOutput::updateNumberOfChannels
  WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=184931:185533
Fixed: https://cluster-fuzz.appspot.com/revisions?range=187778:187880

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95lhWl9_BW1AbcZMe8Dgb4VNN6rWpGPUZqq9wGmf6Obh6Dc_i7vaolKVxdUNpohxWZLviPqld_pHM79dUXWn0CB5jnEIbKULtlmTjxcKv4K2SQjctXYRQiy3IS2luznASDy6L8On85Brn0DgnZC8kuHeyb8TVD_YAjQLeSj1jkqlXRNAyQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### [Deleted User] (2013-03-16)

Could you authorize me to access the report? Thanks.

### in...@chromium.org (2013-03-16)

sorry Xingnan, ClusterFuzz access is restricted to chromium members only. The report does not contain any other information other than what is in the bug. I have clicked redo on the report to recheck whether the bug is really fixed or not. Does anything in this range https://cluster-fuzz.appspot.com/revisions?range=187778:187880 trigger any bells/whistles ?

### [Deleted User] (2013-03-18)

I also cannot reproduce the bug, but I am curious about that I could not find any related fix in range=187778:187880.
Chris, any comments?

### at...@gmail.com (2013-03-18)

Here is second un-minimized repro-file that still reproduces on my system with: 

Ubuntu 12.04
Chromium 27.0.1444.0 (Developer Build 188694)

ASAN-report snippet:
==19777== ERROR: AddressSanitizer: heap-use-after-free on address 0x600c000458c8 at pc 0x7f2baab47d4e bp 0x7f2b7473d0a0 sp 0x7f2b7473d098
READ of size 8 at 0x600c000458c8 thread T8 (AudioOutputDevi)
    #0 0x7f2baab47d4d in WebCore::AudioNodeOutput::pull(WebCore::AudioBus*, unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WTF/wtf/Vector.h:547:0
    #1 0x7f2baab43846 in WebCore::AudioNode::processIfNecessary(unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioNode.cpp:300:0
    #2 0x7f2baab3a0dc in WebCore::AudioContext::processAutomaticPullNodes(unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioContext.cpp:932:0
    #3 0x7f2baaf58601 in WebCore::AudioDestinationNode::render(WebCore::AudioBus*, WebCore::AudioBus*, unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/Modules/webaudio/AudioDestinationNode.cpp:86:0
    #4 0x7f2bad54cc22 in WebCore::AudioPullFIFO::consume(WebCore::AudioBus*, unsigned long) /home/attekett/chrome/src/out/Release/../../third_party/WebKit/Source/WebCore/platform/audio/AudioPullFIFO.cpp:65:0
.
.
.


### [Deleted User] (2013-03-20)

It can be reproduced now, and updated the fix in https://bugs.webkit.org/show_bug.cgi?id=111362

### [Deleted User] (2013-03-21)

Bulk Edit

### [Deleted User] (2013-03-21)

Bulk edit

### cl...@chromium.org (2013-03-24)

ClusterFuzz has detected this issue as fixed in range 187778:187881.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=169025003

Uploader: palmer@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x60180015ba88
Crash State:
  - crash stack -
  WebCore::AudioNodeOutput::pull
  WebCore::AudioNode::processIfNecessary
  - free stack -
  WebCore::AudioNodeOutput::updateNumberOfChannels
  WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=184931:185533
Fixed: https://cluster-fuzz.appspot.com/revisions?range=187778:187881

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95lhWl9_BW1AbcZMe8Dgb4VNN6rWpGPUZqq9wGmf6Obh6Dc_i7vaolKVxdUNpohxWZLviPqld_pHM79dUXWn0CB5jnEIbKULtlmTjxcKv4K2SQjctXYRQiy3IS2luznASDy6L8On85Brn0DgnZC8kuHeyb8TVD_YAjQLeSj1jkqlXRNAyQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### [Deleted User] (2013-04-16)

James, do you plan to contribute to Blink? If not we will need to find new owners for these security bugs.

Thanks!

### [Deleted User] (2013-04-17)

cdn, 

xingnan has a patch under review for this issue. https://codereview.chromium.org/14042005/ 



### in...@chromium.org (2013-04-17)

Chris (crogers@), please help to review 14042005. It has potential to resolve most of the webaudio issues and then we can easily dupe them out.

### cr...@google.com (2013-04-17)

We're working on it

### bu...@chromium.org (2013-04-24)

------------------------------------------------------------------------
r149041 | crogers@google.com | 2013-04-24T21:27:42.793760Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/OfflineAudioDestinationNode.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/chromium/support/WebAudioBus.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/HRTFElevation.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioBus.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/OfflineAudioDestinationNode.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioResampler.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioBus.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioResampler.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNodeInput.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNodeOutput.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/Reverb.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioBuffer.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/Platform/chromium/public/WebAudioBus.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNodeInput.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/modules/webaudio/AudioNodeOutput.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/AudioFileReader.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/Reverb.h?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/MultiChannelResampler.cpp?r1=149041&r2=149040&pathrev=149041
   M http://src.chromium.org/viewvc/blink/trunk/Source/core/platform/audio/chromium/AudioBusChromium.cpp?r1=149041&r2=149040&pathrev=149041

Heap-use-after-free in WebCore::AudioNodeOutput::pull

BUG=179522

Review URL: https://codereview.chromium.org/14042005
------------------------------------------------------------------------

### in...@chromium.org (2013-04-25)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-05-06)

@attekett: this reward covers all the recently fixed webaudio bugs (179522, 180172, 188092, 219285, 222292)
Although some of the test cases in the end turned out to be technical "duplicates" (fixed by generic patch r149041), we're rewarding $3133.7 for your excellent help thus far in beating webaudio into better shape!

### sc...@gmail.com (2013-05-06)

M27 is https://src.chromium.org/viewvc/blink?view=rev&revision=149786

### bu...@chromium.org (2013-05-06)

------------------------------------------------------------------------
r149786 | cevans@chromium.org | 2013-05-06T20:10:11.575774Z

Changed paths:
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/AudioResampler.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/Reverb.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/Platform/chromium/public/WebAudioBus.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/AudioFileReader.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/Reverb.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/OfflineAudioDestinationNode.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/MultiChannelResampler.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/chromium/AudioBusChromium.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/OfflineAudioDestinationNode.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/chromium/support/WebAudioBus.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/AudioNodeInput.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/AudioNodeOutput.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/HRTFElevation.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/AudioBus.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/AudioResampler.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/AudioBuffer.cpp?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/AudioNodeInput.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/Modules/webaudio/AudioNodeOutput.h?r1=149786&r2=149785&pathrev=149786
   M http://src.chromium.org/viewvc/blink/branches/chromium/1453/Source/WebCore/platform/audio/AudioBus.h?r1=149786&r2=149785&pathrev=149786

Merge Blink r149041 to M27

BUG=179522
TBR=crogers@google.com

Review URL: https://codereview.chromium.org/14957010
------------------------------------------------------------------------

### sc...@gmail.com (2013-05-17)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-05-28)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/179522?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/180172, crbug.com/chromium/222292, crbug.com/chromium/265131]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40077068)*
