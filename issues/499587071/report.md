# Chromium crashes during xdg-desktop-portal screencast on Wayland KDE (Slack screen share)

| Field | Value |
|-------|-------|
| **Issue ID** | [499587071](https://issues.chromium.org/issues/499587071) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>ScreenCapture |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 146.0.7680.177 (Official Build) Arch Linux (64-bit)  |
| **Reporter** | bo...@gmail.com |
| **Assignee** | gr...@gmail.com |
| **Created** | 2026-04-05 |
| **Bounty** | $4,000.00 |

## Description

# Steps to reproduce the problem

1. Navigate to slack.com
2. Join a huddle & share screen
3. xdg-desktop-portal popup opens, choose one of the screens to share
4. Confirm in slack you want to share that screen
5. Repeat the above 1-10 times: The crash does not happen every time
6. See the shared screen rendered once in slack before chromium freezes then crashes

# Problem Description

Chromium sometimes crashes when sharing a screen via xdg-desktop-portal in slack.

# Additional Comments

Crash happens in Chromium & Google Chrome

# Summary

Chromium crashes during xdg-desktop-portal screencast on Wayland KDE (Slack screen share)

# Custom Questions

#### Crashed report ID:

1d90fc35909c51b9

#### How much crashed?

The whole browser

#### Is it a problem with a plugin?

No - It's the browser itself

# Additional Data

Category: Crashes   

Chrome Channel: Stable   

Regression: N/A   

Has Chrome Feedback with description matching the bug title: <https://listnr.corp.google.com/product/237/reports?searchText=Chromium%20crashes%20during%20xdg-desktop-portal%20screencast%20on%20Wayland%20KDE%20(Slack%20screen%20share)&filter=0&dateRange=30>

## Attachments

- chrome_debug.log (text/plain, 2.3 MB)
- about-gpu-2026-04-05T17-49-42-838Z.txt (text/plain, 39.0 KB)
- [499587071-M146.webm](attachments/499587071-M146.webm) (video/webm, 22.5 MB)
- [Screencast_20260406_201722.webm](attachments/Screencast_20260406_201722.webm) (video/webm, 3.2 MB)
- [chrome-version.txt](attachments/chrome-version.txt) (text/plain, 35.6 KB)
- [chrome-crash-dbus2.log](attachments/chrome-crash-dbus2.log) (text/plain, 384.8 KB)
- [repro.html](attachments/repro.html) (text/html, 4.1 KB)
- [core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000.zst](attachments/core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000.zst) (application/octet-stream, 17.5 MB)
- [asan.log](attachments/asan.log) (text/plain, 24.1 KB)
- [repro-asan.html](attachments/repro-asan.html) (text/html, 2.9 KB)

## Timeline

### bo...@gmail.com (2026-04-05)

redacted

### bo...@gmail.com (2026-04-06)

redacted

### de...@google.com (2026-04-06)

Tested the issue on Chrome version #146.0.7680.177 using Linux Ubuntu as per comment#1

Steps to reproduce:
===============
1. Launched Chrome and navigated to slack.com
2. Joined a huddle and initiated a screen share
3. When the xdg-desktop-portal popup appeared, selected a screen and confirmed the share 
4. Repeated the process approximately 10 times
Observed able to share the screen every time and no freeze/unresponsiveness or crash seen

Requesting alcooper@ for further inputs on this issue.

Attaching screencast for reference.

Reporter@: Could you please review the above observations and let us know if we missed anything, please share a screencast of the issue for further triaging the issue.

Note: Requesting you to copy-paste the entire content of chrome://version/?show-variations-cmd details to a .txt file format and attach it.
Thanks..!!

### bo...@gmail.com (2026-04-06)

> Requesting you to copy-paste the entire content of chrome://version/?show-variations-cmd details to a .txt file format and attach it.

Attached as chrome-version.txt

Please also see the attached video for a similar reproduction. Crash ID: 396b85d2a212843d

I am running Arch Linux with KDE, which might be relevant. Ubuntu may be using a different xdg-desktop-portal but I'm not certain. The crash appears to be related to the dbus traffic with xdg-desktop-portal.

Please try sharing the 'Entire Screen' instead of just a single tab.

### pe...@google.com (2026-04-06)

Thank you for providing more feedback. Adding the requester to the CC list.

### sx...@google.com (2026-04-06)

Crash 396b85d2a212843d (go/crash/396b85d2a212843d) doesn't provide much meaningful information, but I noticed there are some other crashers in the user's chrome://crashes - does disabling audio sharing change the crash behavior by any chance? (Seeing something suspicious in the other ones)

### sx...@google.com (2026-04-06)

Here are the other crashes:

- <http://crash/browse?q=reportid=%275a95babe7ba38192%27>
- <http://crash/browse?q=reportid=%2721342d82969ff2c1%27>
- <http://crash/browse?q=reportid=%27daef684b7a4dd58b%27>
- <http://crash/browse?q=reportid=%27c3d0187951e73192%27>
- <http://crash/browse?q=reportid=%279578277d8c38f958%27>

### bo...@gmail.com (2026-04-06)

> does disabling audio sharing change the crash behavior by any chance?

Could you clarify how I can test this?

I am not sharing a tab, which has the "Also share tab audio" option. Instead I am sharing the "Entire Screen", then I see the "Share screen with Google Chrome" xdg-desktop-portal window where I choose a monitor. There does not appear to be an option to share my audio. See: https://issues.chromium.org/499587071#attachment75225211

I've tried revoking microphone permission to slack, but the crash still occurs (b428ce32ac6ca691, dd2a362e218a1a49).

### bo...@gmail.com (2026-04-06)

Please also see https://issues.chromium.org/issues/499572780 which is related

### sx...@google.com (2026-04-06)

My bad, completely forgot that system audio sharing isn't implemented on Linux. I saw Pipewire in the stack from the majority of your crashers, hence the question.

### sx...@google.com (2026-04-06)

Thanks for connecting the dots, give us some time to take a look.

### gr...@gmail.com (2026-04-07)

Hi, I'm unable to reproduce it, but that might be given a different xdg-desktop-portal version (on Fedora 44). I don't have access to <https://issues.chromium.org/issues/499572780> or to any backtrace.

Can you run `dbus-monitor --session` in a terminal and try to reproduce the issue and attach the output here? That might have some useful information, but still without a backtrace or reproducer on my side I can only guess.

### bo...@gmail.com (2026-04-07)

I do believe the issue is related to the xdg-desktop-portal backend version.

I've attached a chrome-crash-dbus2.log. Google Chrome Crash ID: d8512fcad2751821

I can reproduce the same crash in Chromium, and have attached more details to https://issues.chromium.org/issues/499572780

Now that this issue is marked as Vulnerability and has Limited visibility I will copy the details here:

-------------------------

VULNERABILITY DETAILS

Use-after-free in webrtc::SharedScreenCastStreamPrivate::StartScreenCastStream()
on Wayland (xdg-desktop-portal ScreenCast). getDisplayMedia({audio: true}) creates
5 BaseCapturerPipeWire instances on 5 separate NativeDesktopMediaList::Worker
threads sharing a ref-counted SharedScreenCastStream (RefCountedNonVirtual, not
thread-safe). When one worker destroys its capturer, the shared stream's private_
is freed. Another capturer's valid D-Bus callback then calls StartScreenCastStream()
on the freed object. The freed memory is reused for web-content-controlled
JavaScript strings, giving the attacker control over a vtable write in the
browser process.

Related (reported by me before I realized the security impact): https://issues.chromium.org/issues/499587071

VERSION
Chrome Version: Chromium 146.0.7680.177 Arch Linux & Google Chrome 146.0.7680.177
Operating System: Arch Linux x86_64, kernel 6.19.11-zen1-1-zen, KDE Plasma 6.6.3
KWin Wayland, xdg-desktop-portal 1.20.3, xdg-desktop-portal-kde 6.6.3,
PipeWire 1.6.2, Mesa 26.0.4

REPRODUCTION CASE

Attached files:
- repro.html: calls getDisplayMedia({audio:true, video:{frameRate:{max:15}}})
  with WebRTC peer connections and browser-process heap pressure

Steps:
1. chromium repro.html   (on Wayland with xdg-desktop-portal)
2. Click "Start", grant mic permission, select a screen in the portal dialog
3. Repeatedly select screen in portal dialog
4. Browser process crashes (SIGSEGV)

Please note: Slack Huddle screen sharing appears to trigger this bug in the wild, there:

1. Start a huddle
2. Share screen
3. May need to repeat ~5 times
4. Browser process crashes (SIGSEGV)

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser
Crash State:

Symbolized stack trace (consistent across 10+ reproductions):

  #0 webrtc::SharedScreenCastStreamPrivate::StartScreenCastStream(
       unsigned int, int, unsigned int, unsigned int, bool,
       webrtc::DesktopCapturer::Callback*)
  #1 webrtc::BaseCapturerPipeWire::OnScreenCastRequestResult(
       webrtc::xdg_portal::RequestResponse, unsigned int, int)
  #2 webrtc::ScreenCastPortal::OnPortalDone(
       webrtc::xdg_portal::RequestResponse)
  #3 webrtc::ScreenCastPortal::OnOpenPipeWireRemoteRequested(
       _GDBusProxy*, _GAsyncResult*, void*)
  #4 g_task_return_now (libgio, gtask.c:1363)
  #5 g_task_return (libgio, gtask.c:1432)
  #6 reply_cb (libgio, gdbusproxy.c:2557)
  ...
  #16 g_main_context_iteration (libglib)
  #17 base::MessagePumpGlib::Run(base::MessagePump::Delegate*)
  #18 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run
  #19 base::RunLoop::Run
  #20 content::BrowserMainLoop::RunMainMessageLoop()

Registers at crash:
  rbx = freed SharedScreenCastStreamPrivate (memory reused for UTF-16 JS strings)
  r14 = 0x46005400280020 (UTF-16LE " (TF" from JS string at offset 0xc0 of object)
  rax = vtable pointer (valid code address)

Crashing instruction:
  mov    0xc0(%rbx),%r14   ; load pointer from freed object → garbage
  test   %r14,%r14          ; null check passes (garbage is non-null)
  je     skip
  lea    vtable,%rax
  mov    %rax,(%r14)        ; write vtable to attacker-influenced address → SEGV

Analysis:
- getDisplayMedia({audio:true}) creates 5 BaseCapturerPipeWire instances on
  5 worker threads (confirmed via LD_PRELOAD thread ID logging)
- All share SharedScreenCastStream via DesktopCaptureOptions (ref-counted with
  non-thread-safe RefCountedNonVirtual)
- The callback is NOT stale: g_cancellable_is_cancelled() returns false
  (confirmed via LD_PRELOAD diagnostic instrumentation)
- The freed memory is reused for web-content-controlled JavaScript strings,
  giving attacker control over the pointer at offset 0xc0 which receives a
  vtable write — a potential code execution primitive in the browser process

Suggested fix (mitigation): add null guards on private_ in
SharedScreenCastStream methods (patch attached as fix-screencast-crash.patch).
Root-cause fix: SharedScreenCastStream uses RefCountedNonVirtual which is not
thread-safe, but is shared across 5 worker threads. Either make the refcounting
atomic or ensure single-threaded ownership.

-------------------------

Attaching updated repro.html and core dump proving attacker control over the pointer value used in the vtable write.

The repro page fills freed memory with attacker-chosen character U+4141 via console.log IPC to the browser process. The
core dump shows:

#0 webrtc::SharedScreenCastStreamPrivate::StartScreenCastStream(+150)

r14 = 0x4141414141414141

This is the register used in the crashing instruction mov %rax,(%r14) - a vtable pointer write to an attacker-controlled
address. The attacker chose 0x4141 in JavaScript, and the browser process wrote to 0x4141414141414141.

The primitive is:
- WHAT is written: a known vtable pointer (in rax, a fixed code address loaded via lea)
- WHERE it is written: 0x4141414141414141 (attacker-controlled via JavaScript string content at offset 0xc0 of the freed
object)

After the vtable write, the code reads *(r14+0x20) — also within the attacker-controlled string data — and passes it to a
destructor call. An attacker who points r14 to a heap-sprayed region controls both the vtable write destination and the
subsequent virtual call target, which is a standard path to code execution.

This is a Linux/Wayland-only bug. The trigger requires only getDisplayMedia({audio: true}) with a single user gesture
(screen share permission grant). No extensions or special privileges needed.

To verify from the attached core dump:

zstd -d core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000.zst -o core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000

DEBUGINFOD_URLS="https://debuginfod.archlinux.org" gdb -batch \
  -ex "set debuginfod enabled on" \
  -ex "file /usr/lib/chromium/chromium" \
  -ex "core-file core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000" \
  -ex "bt 8" \
  -ex "info registers r14 rax rbx"


### fl...@google.com (2026-04-09)

[Security shepherd here]

I'm setting Found In on the basis of the reporter's version of Chrome, but grulja@, if you're unable to reproduce / don't see the same thing, please feel free to update that. Thanks.

### gr...@gmail.com (2026-04-09)

I'm unable to reproduce, because this is really specific and not easily reproducible, but same issue is reported against Firefox and I have a fix almost ready.

Btw. this has been an issue most likely from the beginning, definitely not something introduced recently.

### ch...@google.com (2026-04-09)

Setting milestone because of s2 severity.

### bo...@gmail.com (2026-04-09)

Attached asan.log for `python3 ./get_asan_chrome.py --version 146.0.7680.177`

### bo...@gmail.com (2026-04-09)

I see https://issues.chromium.org/issues/499572780 has been closed.

Apologies for reporting it here first. I did not realize the potential security implications when I reported it, and it feels inappropriate to open a new report now this one is appropriately marked & gaining traction. Hopefully this bug report is still eligible for the VRP :-)

### dx...@google.com (2026-04-16)

Project: src  

Branch:  main  

Author:  Jan Grulich [grulja@gmail.com](mailto:grulja@gmail.com)  

Link:    <https://webrtc-review.googlesource.com/463800>

Fix use-after-free in ScreenCast and Camera portal D-Bus callbacks

---


Expand for full commit details
```
     
    GDBus async callbacks fire on the GLib main thread with a raw pointer 
    to the portal object. When the portal is destroyed on another thread, 
    the callback accesses freed memory. 
     
    Introduce PortalGuard, a ref-counted mutex-protected wrapper that 
    outlives the portal. Callbacks lock the guard and check the portal 
    pointer before use. Stop() locks the same mutex to null the pointer, 
    blocking until any in-flight callback finishes. Utility functions 
    now take scoped_refptr<PortalGuard> and manage refs internally. 
     
    Bug: chromium:491979284 
    Bug: chromium:499587071 
    Change-Id: I80fe20c5c3b6509666554c7cc7454f09cab6c2e4 
    Reviewed-on: https://webrtc-review.googlesource.com/c/src/+/463800 
    Reviewed-by: Harald Alvestrand <hta@webrtc.org> 
    Commit-Queue: Jan Grulich <grulja@gmail.com> 
    Reviewed-by: Ilya Nikolaevskiy <ilnik@webrtc.org> 
    Reviewed-by: Andreas Pehrson <apehrson@mozilla.com> 
    Cr-Commit-Position: refs/heads/main@{#47444}

```

---

Files:

- M `modules/desktop_capture/linux/wayland/base_capturer_pipewire.cc`
- M `modules/desktop_capture/linux/wayland/screen_capture_portal_interface.cc`
- M `modules/desktop_capture/linux/wayland/screen_capture_portal_interface.h`
- M `modules/desktop_capture/linux/wayland/screencast_portal.cc`
- M `modules/desktop_capture/linux/wayland/screencast_portal.h`
- M `modules/portal/BUILD.gn`
- A `modules/portal/portal_guard.h`
- M `modules/portal/xdg_desktop_portal_utils.cc`
- M `modules/portal/xdg_desktop_portal_utils.h`
- M `modules/video_capture/linux/camera_portal.cc`

---

Hash: 9dde36ebf937da0ab92837932b253cc3d42c8dc2  

Date: Thu Apr 16 09:04:26 2026


---

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7768853>

Roll WebRTC from c0f60f349a19 to 9dde36ebf937 (5 revisions)

---


Expand for full commit details
```
     
    https://webrtc.googlesource.com/src.git/+log/c0f60f349a19..9dde36ebf937 
     
    2026-04-16 grulja@gmail.com Fix use-after-free in ScreenCast and Camera portal D-Bus callbacks 
    2026-04-16 tommi@webrtc.org Cache ICE credentials and remove signaling thread blocking calls 
    2026-04-16 tommi@webrtc.org DTLS role caching in JsepTransportController 
    2026-04-16 jakobi@webrtc.org Cleanup audio nack logic. 
    2026-04-16 chromium-webrtc-autoroll@webrtc-ci.iam.gserviceaccount.com Roll chromium_revision 420a8d9cea..9e7bbda03e (1615218:1615680) 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/webrtc-chromium-autoroll 
    Please CC webrtc-chromium-sheriffs-robots@google.com,webrtc-infra@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in WebRTC: https://bugs.chromium.org/p/webrtc/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:491979284,chromium:499587071 
    Tbr: webrtc-chromium-sheriffs-robots@google.com 
    Change-Id: I084602896df14039f0a1cd42e6c03a6ae5d240c7 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7768853 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1615812}

```

---

Files:

- M `DEPS`
- M `third_party/webrtc`

---

Hash: [70077633a0b15ab323417b025ec03a8c26ac6c25](https://chromiumdash.appspot.com/commit/70077633a0b15ab323417b025ec03a8c26ac6c25)  

Date: Thu Apr 16 14:02:15 2026


---

### sp...@google.com (2026-06-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
Mildly mitigated UAF.  


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499587071)*
