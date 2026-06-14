# Heap-use-after-free in WebCore::MediaPlayer::sourceSetTimestampOffset [exploitable]

| Field | Value |
|-------|-------|
| **Issue ID** | [40076621](https://issues.chromium.org/issues/40076621) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink, Blink>WebRTC, Internals>Media>Source |
| **Reporter** | sc...@gmail.com |
| **Assignee** | ac...@chromium.org |
| **Created** | 2012-11-27 |
| **Bounty** | $7,331.00 |

## Description

We've received a privately disclosed exploit from Pinkie Pie, who has undertaken the "64-bit exploits" challenge as per http://blog.chromium.org/2012/08/chromium-vulnerability-rewards-program.html

I confirm exploitability on my Ubuntu 12.04 machine with a fresh profile in Chrome 23.0.1271.91 stable.

The code execution is achieved with a use-after-free due to object lifetime issues with the ownership of MediaPlayer.

I have attached a hand-minimized repro; you can see ASAN catch the problem by launching chrome with these flags against the local file:

./out/Debug/chrome ~/viduaf.html --disable-seccomp-filter-sandbox --disable-seccomp-sandbox --js-flags='--expose_gc' --allow-file-access-from-files

==23060== ERROR: AddressSanitizer: heap-use-after-free on address 0x7fc758fb0e98 at pc 0x7fc78350d95f bp 0x7fff8b35a410 sp 0x7fff8b35a408
READ of size 8 at 0x7fc758fb0e98 thread T0
    #0 0x7fc78350d95e in WTF::OwnPtr<WebCore::MediaPlayerPrivateInterface>::operator->() const out/Debug/../../third_party/WebKit/Source/WTF/wtf/OwnPtr.h:72
    #1 0x7fc7834fcf73 in WebCore::MediaPlayer::sourceSetTimestampOffset(WTF::String const&, double) out/Debug/../../third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:509
    #2 0x7fc775b219ae in WebCore::MediaSource::setTimestampOffset(WTF::String const&, double, int&) out/Debug/../../third_party/WebKit/Source/WebCore/Modules/mediasource/MediaSource.cpp:316
    #3 0x7fc775b3d762 in WebCore::SourceBuffer::setTimestampOffset(double, int&) out/Debug/../../third_party/WebKit/Source/WebCore/Modules/mediasource/SourceBuffer.cpp:74
    #4 0x7fc77e740ce1 in WebCore::SourceBufferV8Internal::timestampOffsetAttrSetter(v8::Local<v8::String>, v8::Local<v8::Value>, v8::AccessorInfo const&) out/Debug/gen/webcore/bindings/V8SourceBuffer.cpp:77
...0x7fc758fb0e98 is located 88 bytes inside of 280-byte region [0x7fc758fb0e40,0x7fc758fb0f58)
freed by thread T0 here:
    #0 0x7fc79263ee50 in __interceptor_free ??:0
    #1 0x7fc7884746cd in WTF::fastFree(void*) out/Debug/../../third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:331
    #2 0x7fc78350d051 in WebCore::MediaPlayer::operator delete(void*) out/Debug/../../third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.h:224
    #3 0x7fc7834f72e9 in ~MediaPlayer out/Debug/../../third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:353
    #4 0x7fc76fcb3b0c in void WTF::deleteOwnedPtr<WebCore::MediaPlayer>(WebCore::MediaPlayer*) out/Debug/../../third_party/WebKit/Source/WTF/wtf/OwnPtrCommon.h:60
    #5 0x7fc76fce8b4b in ~OwnPtr out/Debug/../../third_party/WebKit/Source/WTF/wtf/OwnPtr.h:63
    #6 0x7fc76fc4eee6 in ~OwnPtr out/Debug/../../third_party/WebKit/Source/WTF/wtf/OwnPtr.h:63
    #7 0x7fc76fbf7cbf in ~HTMLMediaElement out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:320
    #8 0x7fc78c09bbbe in WebCore::HTMLVideoElement::~HTMLVideoElement() out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.h:38
    #9 0x7fc78c099166 in WebCore::HTMLVideoElement::~HTMLVideoElement() out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.h:38
    #10 0x7fc78c09929f in WebCore::HTMLVideoElement::~HTMLVideoElement() out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.h:38
    #11 0x7fc77a446d99 in WebCore::Node::removedLastRef() out/Debug/../../third_party/WebKit/Source/WebCore/dom/Node.cpp:2825
...
previously allocated by thread T0 here:
    #0 0x7fc79263ef10 in __interceptor_malloc ??:0
    #1 0x7fc78847347b in WTF::fastMalloc(unsigned long) out/Debug/../../third_party/WebKit/Source/WTF/wtf/FastMalloc.cpp:269
    #2 0x7fc76fcfb415 in WebCore::MediaPlayer::operator new(unsigned long) out/Debug/../../third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.h:224
    #3 0x7fc76fc66f23 in WebCore::MediaPlayer::create(WebCore::MediaPlayerClient*) out/Debug/../../third_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.h:229
    #4 0x7fc76fc06051 in WebCore::HTMLMediaElement::createMediaPlayer() out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:4315
    #5 0x7fc76fc014d6 in WebCore::HTMLMediaElement::prepareForLoad() out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:730
    #6 0x7fc76fbfdb00 in WebCore::HTMLMediaElement::scheduleLoad(WebCore::HTMLMediaElement::LoadType) out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:590
    #7 0x7fc76fbfa766 in WebCore::HTMLMediaElement::parseAttribute(WebCore::QualifiedName const&, WTF::AtomicString const&) out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:372
    #8 0x7fc78c09479f in WebCore::HTMLVideoElement::parseAttribute(WebCore::QualifiedName const&, WTF::AtomicString const&) out/Debug/../../third_party/WebKit/Source/WebCore/html/HTMLVideoElement.cpp:124

## Attachments

- [viduaf.html](attachments/viduaf.html) (text/plain; charset=us-ascii, 394 B)

## Timeline

### sc...@gmail.com (2012-11-27)

I'm going to leave it for @acolwell / @scherkus / @inferno to debate and land the correct fix in the morning, but the patch below seems to do the unregistering of the MediaPlayer at the right time, and keeps ASAN happy.

It still needs someone familiar with the object lifetimes here to investigate further, though. For example, if there's a codepath where this assert...
    ASSERT(!m_mediaSource);  // HTMLMediaElement::loadResource()
... does not hold, then the MediaSource will get overwritten and the old one will not get the notification callback of the pending MediaPlayer destruction.

There may be other object lifetime issues; an expert should review this area thoroughly.


Index: HTMLMediaElement.cpp
===================================================================
--- HTMLMediaElement.cpp	(revision 135622)
+++ HTMLMediaElement.cpp	(working copy)
@@ -317,6 +317,8 @@
         m_mediaController->removeMediaElement(this);
 
     removeElementFromDocumentMap(this, document());
+    if (m_mediaSource)
+        m_mediaSource->setMediaPlayer(0);
 }
 
 void HTMLMediaElement::didMoveToNewDocument(Document* oldDocument)
@@ -3752,6 +3754,8 @@
 void HTMLMediaElement::clearMediaPlayer(int flags)
 {
 #if !ENABLE(PLUGIN_PROXY_FOR_VIDEO)
+    if (m_mediaSource)
+        m_mediaSource->setMediaPlayer(0);
     m_player.clear();
 #endif
     stopPeriodicTimers();


### js...@chromium.org (2012-11-27)

[Empty comment from Monorail migration]

### ka...@google.com (2012-11-27)

marking as a blocker so i can track.

### ac...@chromium.org (2012-11-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-27)

CF Report coming in https://cluster-fuzz.appspot.com/testcase?key=143438494. But we already have the line numbers.

### in...@chromium.org (2012-11-27)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=143438494

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f394b0314d0
Crash State:
  - crash stack -
  WebCore::MediaPlayer::sourceSetTimestampOffset
  WebCore::MediaSource::setTimestampOffset
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=155400:155482

Minimized Testcase (0.32 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94W0CLcIFwelGUL5t905SNBkEGqXZsOEgzPck-jaqqhBv5n6RFNJ8p0F2HsJzeY2k-U8benveQ8GfZyalngZXKZLvRwkmLGUpn8_HAFczTf7-IiaP7wTVNY7O5KwloU-yGkfkm8ESz1oKpuiSrvejsS37I683PFaqzt0f0mOZLz0_q9Ntw
<video id="vid"><script>
function source_opened() {
  buffer = ms.addSourceBuffer('video/webm; codecs="vorbis,vp8"');
  vid.parentNode.removeChild(vid);
  gc();
  buffer.timestampOffset = 42;
}

ms = new WebKitMediaSource();
ms.addEventListener('webkitsourceopen', source_opened);
vid.src = window.URL.createObjectURL(ms);
</script>

### in...@chromium.org (2012-11-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-11-27)

http://trac.webkit.org/changeset/135906

### sc...@gmail.com (2012-11-27)

M23: http://trac.webkit.org/changeset/135931
M24: http://trac.webkit.org/changeset/135932

### cl...@chromium.org (2012-11-28)

ClusterFuzz has detected this issue as fixed in range 169616:169821.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=143438494

Uploader: inferno@chromium.org

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f394b0314d0
Crash State:
  - crash stack -
  WebCore::MediaPlayer::sourceSetTimestampOffset
  WebCore::MediaSource::setTimestampOffset
  - free stack -
  WebCore::HTMLMediaElement::~HTMLMediaElement
  WebCore::HTMLVideoElement::~HTMLVideoElement
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=155400:155482
Fixed: https://cluster-fuzz.appspot.com/revisions?range=169616:169821

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv94W0CLcIFwelGUL5t905SNBkEGqXZsOEgzPck-jaqqhBv5n6RFNJ8p0F2HsJzeY2k-U8benveQ8GfZyalngZXKZLvRwkmLGUpn8_HAFczTf7-IiaP7wTVNY7O5KwloU-yGkfkm8ESz1oKpuiSrvejsS37I683PFaqzt0f0mOZLz0_q9Ntw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-11-29)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-11)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-12-14)

Payment in system.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-05-24)

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

### sh...@chromium.org (2018-07-29)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-29)

This issue was migrated from crbug.com/chromium/162835?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>WebRTC, Internals>Media>Source]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40076621)*
