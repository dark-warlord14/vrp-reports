# Heap-buffer-overflow in av_freep

| Field | Value |
|-------|-------|
| **Issue ID** | [40054538](https://issues.chromium.org/issues/40054538) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ch...@gmail.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2012-03-06 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Opening attached gen.ogv file with chrome causes a heap buffer overflow.

**VERSION**  

Chrome Version: [ 19.0.1061.0 (125083)] + [dev]  

Operating System: [Ubuntu 10.04 64 bit]

**REPRODUCTION CASE**

1. Open attached gen.ogv file with chrome.
2. Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]  

Asan output:

==30509== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f81d1460ea0 at pc 0x7f81d6ed26a4 bp 0x7f81d0438db0 sp 0x7f81d0438da8  

READ of size 8 at 0x7f81d1460ea0 thread T4  

#0 0x7f81d6ed26a4 in av\_freep /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/ffmpeg/libavutil/mem.c:181  

#1 0x7f81d6eafcc0 in avformat\_close\_input /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/ffmpeg/libavformat/utils.c:2750  

0x7f81d1460ea0 is located 20 bytes to the right of 12-byte region [0x7f81d1460e80,0x7f81d1460e8c)  

allocated by thread T4 here:  

#0 0x7f81ec59ecdc in posix\_memalign ??:0  

#1 0x7f81d6ed24ac in av\_malloc /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/ffmpeg/libavutil/mem.c:94  

#2 0x7f81d6ed26bc in av\_mallocz /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/ffmpeg/libavutil/mem.c:186  

Thread T4 created by T0 here:  

#0 0x7f81ec59cbf3 in pthread\_create ??:0  

#1 0x7f81e6453669 in \_ZN4base12\_GLOBAL\_\_N\_112CreateThreadEmbPNS\_14PlatformThread8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:124  

#2 0x7f81e645356a in \_ZN4base14PlatformThread6CreateEmPNS0\_8DelegateEPm /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/platform\_thread\_posix.cc:228  

#3 0x7f81e645d0e5 in \_ZN4base6Thread16StartWithOptionsERKNS0\_7OptionsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:72  

#4 0x7f81e645ce8b in \_ZN4base6Thread5StartEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/threading/thread.cc:61  

#5 0x7f81ebb5c506 in \_ZN5media18MessageLoopFactory9GetThreadERKSs /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/media/base/message\_loop\_factory.cc:45  

#6 0x7f81ebb5c349 in \_ZNK4base6Thread12message\_loopEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/threading/thread.h:113  

#7 0x7f81ea866bd7 in \_ZN12webkit\_media18WebMediaPlayerImplC2EPN6WebKit8WebFrameEPNS1\_20WebMediaPlayerClientEN4base7WeakPtrINS\_22WebMediaPlayerDelegateEEEPN5media16FilterCollectionEPNS1\_22WebAudioSourceProviderEPNSA\_18MessageLoopFactoryEPNS\_17MediaStreamClientEPNSA\_8MediaLogE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/webkit/media/webmediaplayer\_impl.cc:129  

#8 0x7f81eb2e6dc4 in ~WeakPtr /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/memory/weak\_ptr.h:161  

#9 0x7f81e7e4e3b9 in createWebMediaPlayer /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebKit/chromium/src/WebMediaPlayerClientImpl.cpp:63  

#10 0x7f81e8865d6a in \_ZN7WebCore11MediaPlayer23loadWithNextMediaEngineEPNS\_18MediaPlayerFactoryE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:399  

#11 0x7f81e8864d07 in \_ZN7WebCore11MediaPlayer4loadERKNS\_4KURLERKNS\_11ContentTypeE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/platform/graphics/MediaPlayer.cpp:357  

#12 0x7f81e855d22c in \_ZN7WebCore16HTMLMediaElement12loadResourceERKNS\_4KURLERNS\_11ContentTypeE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:936  

#13 0x7f81e855bebe in ~RefPtr /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/JavaScriptCore/wtf/RefPtr.h:58  

#14 0x7f81e8549c11 in \_ZN7WebCore16HTMLMediaElement14loadTimerFiredEPNS\_5TimerIS0\_EE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/html/HTMLMediaElement.cpp:569  

#15 0x7f81e87da3e8 in \_ZN7WebCore12ThreadTimers24sharedTimerFiredInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/platform/ThreadTimers.cpp:118  

#16 0x7f81e63e3846 in \_ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272  

#17 0x7f81e63e40a8 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:470  

#18 0x7f81e63e5399 in \_ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:660  

#19 0x7f81e63ef8b7 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_default.cc:28  

#20 0x7f81e63e240e in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:418  

#21 0x7f81e63e05ff in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:745  

#22 0x7f81eb33c4ac in \_Z12RendererMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/renderer/renderer\_main.cc:241  

#23 0x7f81e633a213 in RunZygote /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main\_runner.cc:234  

#24 0x7f81e63387ca in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:35  

#25 0x7f81e4a89677 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#26 0x7f81e4a895cb in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

#27 0x7f81ddf08c4d in \_\_libc\_start\_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258  

==30509== ABORTING  

Stats: 35M malloced (31M for red zones) by 39744 calls  

Stats: 0M realloced by 247 calls  

Stats: 33M freed by 25718 calls  

Stats: 0M really freed by 0 calls  

Stats: 100M (25619 full pages) mmaped in 25 calls  

mmaps by size class: 8:49149; 9:8191; 10:4095; 11:2047; 12:1024; 13:2560; 14:256; 15:128; 16:64; 17:32; 18:16; 19:16; 20:20; 22:1;  

mallocs by size class: 8:30805; 9:3680; 10:2107; 11:644; 12:160; 13:2078; 14:122; 15:42; 16:42; 17:24; 18:13; 19:9; 20:17; 22:1;  

frees by size class: 8:18320; 9:2749; 10:1843; 11:438; 12:103; 13:2043; 14:96; 15:38; 16:30; 17:18; 18:13; 19:9; 20:17; 22:1;  

rfrees by size class:  

Stats: malloc large: 64 small slow: 311  

Shadow byte and word:  

0x1ff03a28c1d4: fb  

0x1ff03a28c1d0: 00 04 fb fb fb fb fb fb  

More shadow bytes:  

0x1ff03a28c1b0: fd fd fd fd fd fd fd fd  

0x1ff03a28c1b8: fd fd fd fd fd fd fd fd  

0x1ff03a28c1c0: fa fa fa fa fa fa fa fa  

0x1ff03a28c1c8: fa fa fa fa fa fa fa fa  

=>0x1ff03a28c1d0: 00 04 fb fb fb fb fb fb  

0x1ff03a28c1d8: fb fb fb fb fb fb fb fb  

0x1ff03a28c1e0: fa fa fa fa fa fa fa fa  

0x1ff03a28c1e8: fa fa fa fa fa fa fa fa  

0x1ff03a28c1f0: 00 00 00 00 00 00 00 04

## Attachments

- [gen.ogv](attachments/gen.ogv) (application/ogg; charset=binary, 2.9 MB)

## Timeline

### sc...@gmail.com (2012-03-06)

Thank you Chamal. Any idea if this affects earlier versions?
Looks like a weird stack trace.

Andrew, Dale, are you aware of any recent regressions in video layer or ffmpeg?

### ch...@gmail.com (2012-03-06)

Does not reproduce in stable version 17.0.963.46.
I ll test with chrome beta versions and report shortly.

### ch...@gmail.com (2012-03-06)

Does not reproduce in Version 19.0.1055.1 dev either.

### sc...@gmail.com (2012-03-06)

Videostack guys -- looks like it's a pretty recent regression. Any chance one of you could dig into this whilst the regression is still fresh? Probably easier to fix now rather than a firedrill later.

### in...@chromium.org (2012-03-06)

ClusterFuzz regression range coming....

### in...@chromium.org (2012-03-06)

ptr looks bad when it enters av_freep, does not look good.

### in...@chromium.org (2012-03-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=24670833

Uploader: inferno@chromium.org

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x7fe3ddcfb2a0
Crash State:
  - crash stack -
  av_freep
  avformat_close_input
  posix_memalign
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=124482:124537

Minimized Testcase (2986.36 Kb): https://cluster-fuzz.appspot.com/download/AMIfv97HfQAUlb49WptGHy0PR3HJSMEagFAOb_vmBUTE3JJlHemT7L4U-HM_SjyeTCNLV_ABHZawBCN6zQ5XbWNXFiBa1NCpvu7pOxch3a8QWvoF1bISwKW9Oi1taVa_e_jbhPJEUGQI6ZoJBUv1sotTgDh7bv4c5Q

### in...@chromium.org (2012-03-06)

Looks to have regressed in ffmpeg roll http://src.chromium.org/viewvc/chrome?view=rev&revision=124501

### sc...@gmail.com (2012-03-06)

Sorry, Dale :-/
Can you dig into and deal with this one?

### da...@chromium.org (2012-03-06)

Yup, digging on this now.

### da...@chromium.org (2012-03-06)

[Empty comment from Monorail migration]

### da...@chromium.org (2012-03-06)

Fix: https://chromiumcodereview.appspot.com/9546027/

### sc...@gmail.com (2012-03-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-03-10)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=125969

------------------------------------------------------------------------
r125969 | dalecurtis@google.com | Fri Mar 09 17:12:21 PST 2012

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=125969&r2=125968&pathrev=125969
 M http://src.chromium.org/viewvc/chrome/trunk/src/media/ffmpeg/ffmpeg_regression_tests.cc?r1=125969&r2=125968&pathrev=125969

Roll ffmpeg DEPS. Add test cases for a couple issues.

ffmpeg_revision:
http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/ffmpeg/?view=log

ffmpeg_hash:
http://git.chromium.org/gitweb/?p=chromium/third_party/ffmpeg.git;a=commit;h=d70dcd6cce182fe5fe1ce47561e17890a1bae2b9

BUG=116927, 112976, 110839, 110838
TEST=Valgrind, ASAN.

Review URL: https://chromiumcodereview.appspot.com/9664026
------------------------------------------------------------------------

### da...@chromium.org (2012-03-10)

Should be fixed now.

### ke...@chromium.org (2012-03-12)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

Invalid free()s can be nasty, so $1000 reward! Thanks for catching the regression.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ch...@gmail.com (2012-03-15)

Thank you very much for the reward :)

### sc...@gmail.com (2012-03-27)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2013-01-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

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

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/116927?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054538)*
