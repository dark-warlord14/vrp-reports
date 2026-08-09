# Chromium crashes during xdg-desktop-portal screencast on Wayland KDE (Slack screen share)

| Field | Value |
|-------|-------|
| **Issue ID** | [499572780](https://issues.chromium.org/issues/499572780) |
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

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

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

Client ID (if relevant): 5871494582033073428

Crash IDs: 1d90fc35909c51b9, 18b3f3c13ca6e7de

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Wouter Hünd

## Attachments

- [repro.html](attachments/repro.html) (text/html, 6.7 KB)
- [core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000.zst](attachments/core.chromium.1000.bd96f1fff7634c26a511dbe0327f3205.1683929.1775436052000000.zst) (application/octet-stream, 17.5 MB)
- [repro.html](attachments/repro_75185880.html) (text/html, 4.1 KB)
- [asan.log](attachments/asan.log) (text/plain, 24.1 KB)

## Timeline

### ma...@wouterh.nl (2026-04-06)

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

### ma...@wouterh.nl (2026-04-06)

Please note I've also reported this here using another google account before realizing the potential security implications: https://issues.chromium.org/issues/499587071 (see Comment #3)

### sx...@google.com (2026-04-06)

Can you take a quick look and see if this is valid? The crash doesn't trigger on my machine at least, will need to check on a different config later today.

### jo...@google.com (2026-04-07)

yeah I'll take a look.

### aj...@google.com (2026-04-09)

This report does not provide enough information for us to quickly understand and
reproduce a problem. It will be closed as Won't Fix. Once you have gathered the
required information please open a new issue with a brief description that
attaches all necessary pocs, traces and patches as individual files.

In particular:

- attach a complete symbolized trace as `asan.log` including all additional information

For more information see: <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting>

### ma...@wouterh.nl (2026-04-09)

I reported this over at https://issues.chromium.org/issues/499587071 before I realized the potential security implications, and it seems a developer has picked it up: https://issues.chromium.org/issues/499587071#comment16

Will attach asan.log there as well.

### ch...@google.com (2026-04-09)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-07-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/499572780)*
