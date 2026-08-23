# memory corruption in qualcomm gpu lead sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [507508103](https://issues.chromium.org/issues/507508103) |
| **Status** | New |
| **Severity** | S4-Minimal |
| **Priority** | P0 |
| **Component** | Blink>WebGL |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | kb...@google.com |
| **Created** | 2026-04-29 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

This vulnerability ultimately caused a crash in glInvalidateFramebuffer.

VERSION
Chrome Version: [147.0.7727.111] + [stable]

Operating System: [samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCSABZD1\_CHCABZD1:user/release-keys ]

REPRODUCTION CASE

1.luach chrome on S25

2.open poc.html

3.logcat | grep DEBU

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: [GPU]

```
04-29 08:53:38.572 19717 19717 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
04-29 08:53:38.572 19717 19717 F DEBUG   : Build fingerprint: 'samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCSABZD1_CHCABZD1:user/release-keys'
04-29 08:53:38.572 19717 19717 F DEBUG   : Revision: '11'
04-29 08:53:38.572 19717 19717 F DEBUG   : ABI: 'arm64'
04-29 08:53:38.572 19717 19717 F DEBUG   : Processor: '4'
04-29 08:53:38.572 19717 19717 F DEBUG   : Timestamp: 2026-04-29 08:53:38.445931008+0900
04-29 08:53:38.572 19717 19717 F DEBUG   : Process uptime: 11s
04-29 08:53:38.572 19717 19717 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
04-29 08:53:38.572 19717 19717 F DEBUG   : pid: 19431, tid: 19457, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
04-29 08:53:38.572 19717 19717 F DEBUG   : uid: 10398
04-29 08:53:38.572 19717 19717 F DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
04-29 08:53:38.572 19717 19717 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
04-29 08:53:38.572 19717 19717 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x00da000000008199
04-29 08:53:38.572 19717 19717 F DEBUG   :     x0  b400007515af8ae0  x1  b4000074c5b700b0  x2  0000000000000002  x3  0000000000000000
04-29 08:53:38.572 19717 19717 F DEBUG   :     x4  0000000000000002  x5  0000007414395a50  x6  0000000000000000  x7  0000000000000000
04-29 08:53:38.572 19717 19717 F DEBUG   :     x8  b4000074d5b03fd0  x9  8761fa37f6e82302  x10 0000000000000002  x11 0000000000000000
04-29 08:53:38.572 19717 19717 F DEBUG   :     x12 0000000000000400  x13 fffffffffdffffff  x14 00000074147b1a00  x15 0000000000000000
04-29 08:53:38.573 19717 19717 F DEBUG   :     x16 0000000000000017  x17 000000000000483f  x18 000000741701c000  x19 b400007515af8ae0
04-29 08:53:38.573 19717 19717 F DEBUG   :     x20 b400007575b96160  x21 a6da000000008101  x22 fffffffffdffffff  x23 0000000000000000
04-29 08:53:38.573 19717 19717 F DEBUG   :     x24 0000006e004b0380  x25 0000000000000001  x26 0000000000000000  x27 0000000000000000
04-29 08:53:38.573 19717 19717 F DEBUG   :     x28 000000000000821a  x29 00000074186e1870
04-29 08:53:38.573 19717 19717 F DEBUG   :     lr  0072c4f414395a9c  sp  00000074186e1870  pc  0000007414395af8  pst 0000000000001000
04-29 08:53:38.573 19717 19717 F DEBUG   : 31 total frames
04-29 08:53:38.573 19717 19717 F DEBUG   : backtrace:
04-29 08:53:38.573 19717 19717 F DEBUG   :       #00 pc 0000000000185af8  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!15308ad94fb9d06ecc441bc7d751ce!e4a2ccdb56!+56) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #01 pc 0000000000185a98  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!00392d1e72e084bd76e3a9667b1d57!e4a2ccdb56!+72) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #02 pc 000000000020cd48  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!3a076a0f5bf41e4bcac9395c0e1375!e4a2ccdb56!+648) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #03 pc 00000000090151a8  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #04 pc 0000000008ffcab8  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #05 pc 00000000090141c8  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #06 pc 00000000072d4f58  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #07 pc 00000000072d4468  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #08 pc 00000000072d4194  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #09 pc 00000000072d403c  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #10 pc 00000000072d3fac  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #11 pc 0000000007309f58  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #12 pc 00000000076dec98  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #13 pc 0000000005ed7474  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #14 pc 0000000005e5b244  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #15 pc 0000000005e5adac  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #16 pc 000000000767d4d8  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #17 pc 0000000005ef9164  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #18 pc 0000000005e35060  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #19 pc 0000000005e3144c  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #20 pc 0000000005e311b8  /data/app/~~jc6tK6agABvdATeOmce48Q==/com.google.android.trichromelibrary_772711133-oHunpAMWjmcv7EV5TiVMeg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 61365ef44cd4d1d3897904e966c0abdf0b41035b)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #21 pc 00000000002d7d90  /system/framework/arm64/boot.oat (art_jni_trampoline+112) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #22 pc 0000000000689408  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #23 pc 00000000000e1346  /data/app/~~NZPtaYUqIYoCKjhy8J1FXw==/com.android.chrome-DV-Die4gK059hfQy4GokQQ==/base.apk (offset 0x20b000) (oq3.run+574)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #24 pc 00000000000a9500  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #25 pc 0000000000317194  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #26 pc 0000000000302838  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+216) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #27 pc 00000000004c8298  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+932) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #28 pc 00000000004c7ee4  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #29 pc 0000000000082740  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*)+184) (BuildId: 61a049a7ad18156ebc52d8d483539df9)
04-29 08:53:38.573 19717 19717 F DEBUG   :       #30 pc 0000000000074b98  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 61a049a7ad18156ebc52d8d483539df9)
04-29 09:02:43.375 21600 21600 I QCCEventLogger: Logging from Module qti.qcc.system, eventId QCCAppStart, type DEBUG, payloadSize 21

```

You can also compile a standalone `poc.c` version separately, which makes it easier to determine the cause. Qualcomm Developer allows you to enable MTE locally and fully reconstruct the vulnerability.

CREDIT INFORMATION

Reporter credit: [Anymous]

## Attachments

- [poc.html](attachments/poc.html) (text/html, 9.4 KB)
- [poc.c](attachments/poc.c) (text/x-csrc, 1.8 KB)
- [poc_oob_pc.c](attachments/poc_oob_pc.c) (text/x-csrc, 8.0 KB)

## Timeline

### ka...@google.com (2026-04-30)

S0. Likely will be ExternalDependency unless there's a way for us to protect against it.

### kb...@google.com (2026-04-30)

Submitter, what is being claimed here? Is the address of the crash controllable? Is a write occurring and is that what is provoking the crash?

### kb...@google.com (2026-05-01)

The C and the HTML/WebGL POCs are very different. The C POC creates an obviously incomplete framebuffer and calls `glInvalidateFramebuffer` against it. It would be simple to guard against that. The HTML / WebGL POC contains a bunch of different call sequences and they all seem to create valid framebuffers. We don't have this hardware in house to reproduce on. Submitter, can you please minimize the WebGL POC more?

Mukesh, can you please investigate this from Qualcomm's side?

This seems potentially related and/or the same underlying bug as [Issue 493747593](https://issues.chromium.org/issues/493747593).

Marking ExternalDependency because the Chrome Graphics team won't be able to postulate a workaround without more information from Qualcomm.

### wf...@chromium.org (2026-05-01)

are you sure this is not a null ptr deref? the addr 0x00da000000008199 seems like a PAC masked addr and would in fact be (in or close to) the null page once unmasked...? Have we been able to symbolize this code to check if it's just a null deref?

### ha...@gmail.com (2026-05-01)

re [comment#5](https://issues.chromium.org/issues/507508103#comment5)
This is of course not a null pointer. A null pointer does not have such a tag.

re [comment#3](https://issues.chromium.org/issues/507508103#comment3)
Because the initial performance of this vulnerability is OOB read, pure HTML cannot crash. This must be the case. If MTE is enabled, HTML converted directly from C language can be reproduced, but Samsung does not seem to have MTE enabled. This vulnerability can control PC registers in depth, but it is only available in C language, so I did not provide it. I cannot use html to achieve that purpose.

### kb...@google.com (2026-05-01)

[#comment6](https://issues.chromium.org/issues/507508103#comment6) are you saying that MTE can't be enabled for Chrome's GPU process on this Samsung device, and that's why the HTML POC can't reproduce the problem?

Again, the HTML and C POCs are radically different. The C POC sets up an incomplete framebuffer, with a depth/stencil attachment that's not a depth-renderable format (`GL_RGBA8` rather than something like `GL_DEPTH24_STENCIL8` or `GL_DEPTH32F_STENCIL8`), and then calls `glInvalidateFramebuffer`. It would be trivial to guard against this in Chrome's validating command decoder and ANGLE but I'm not sure that's the biggest problem here.

Can any of the sequence of calls in the HTML POC, if converted to C, provoke a similar crash? I want to know if this can be provoked with a complete framebuffer, and if so, what is the minimal sequence of OpenGL ES API calls that does so. Thanks.

### ha...@gmail.com (2026-05-01)

Yes, it's impossible to trigger a crash with the minimum proof-of-concept (PoC). I don't know why, but individual crashes in C and HTML are the same.

### ha...@gmail.com (2026-05-01)

It would be much easier if you had Qualcomm equipment.

### wf...@chromium.org (2026-05-01)

re: [comment#6](https://issues.chromium.org/issues/507508103#comment6) are you sure it's not a wild array access to a null array - because with TBI on the PAC signature would be da00? This would most certainly be non exploitable then.

Are you able to identify which bit of code is actually triggering this - does anyone have symbols.

### ha...@gmail.com (2026-05-01)

This is what I tested using the native version. Do you still think it's a null pointer exception?

```
05-01 09:36:07.817  9886  9886 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
05-01 09:36:07.817  9886  9886 F DEBUG   : Build fingerprint: 'samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCSABZD1_CHCABZD1:user/release-keys'
05-01 09:36:07.817  9886  9886 F DEBUG   : Revision: '11'
05-01 09:36:07.817  9886  9886 F DEBUG   : ABI: 'arm64'
05-01 09:36:07.817  9886  9886 F DEBUG   : Processor: '1'
05-01 09:36:07.817  9886  9886 F DEBUG   : Timestamp: 2026-05-01 09:36:07.778508017+0800
05-01 09:36:07.817  9886  9886 F DEBUG   : Process uptime: 1s
05-01 09:36:07.817  9886  9886 F DEBUG   : Cmdline: ./poc
05-01 09:36:07.817  9886  9886 F DEBUG   : pid: 9883, tid: 9883, name: poc  >>> ./poc <<<
05-01 09:36:07.817  9886  9886 F DEBUG   : uid: 2000
05-01 09:36:07.817  9886  9886 F DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
05-01 09:36:07.817  9886  9886 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
05-01 09:36:07.817  9886  9886 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0xdeadbeefcafebab0
05-01 09:36:07.817  9886  9886 F DEBUG   :     x0  0000007c77cb6000  x1  0000000000040000  x2  b400007b62712650  x3  7fbc380036004f3f
05-01 09:36:07.817  9886  9886 F DEBUG   :     x4  0000000000000002  x5  00000079dbbd2fe8  x6  000000000000000a  x7  00000000d50324dd
05-01 09:36:07.817  9886  9886 F DEBUG   :     x8  0000000000000000  x9  0000000000000001  x10 00000079dbbd2f80  x11 0000007c77cb6000
05-01 09:36:07.817  9886  9886 F DEBUG   :     x12 0000000000000000  x13 0000000077557bec  x14 0000000000000000  x15 b400007be2737030
05-01 09:36:07.817  9886  9886 F DEBUG   :     x16 00000079dbbd2f80  x17 deadbeefcafebab0  x18 0000007c78c24000  x19 0000000000000001
05-01 09:36:07.817  9886  9886 F DEBUG   :     x20 00000079dbbd2f80  x21 00000079dbbd2f88  x22 b400007b427168e0  x23 b400007b427168e0
05-01 09:36:07.817  9886  9886 F DEBUG   :     x24 b400007b427168e0  x25 0000000000000000  x26 0000000000000000  x27 0000000000000000
05-01 09:36:07.817  9886  9886 F DEBUG   :     x28 0000000000000000  x29 0000007ff14a90d0
05-01 09:36:07.818  9886  9886 F DEBUG   :     lr  00000079db7b66f0  sp  0000007ff14a9080  pc  deadbeefcafebab0  pst 0000000020001400
05-01 09:36:07.818  9886  9886 F DEBUG   : 8 total frames
05-01 09:36:07.818  9886  9886 F DEBUG   : backtrace:
05-01 09:36:07.818  9886  9886 F DEBUG   :   NOTE: Function names and BuildId information is missing for some frames due
05-01 09:36:07.818  9886  9886 F DEBUG   :   NOTE: to unreadable libraries. For unwinds of apps, only shared libraries
05-01 09:36:07.818  9886  9886 F DEBUG   :   NOTE: found under the lib/ directory are readable.
05-01 09:36:07.818  9886  9886 F DEBUG   :   NOTE: On this device, run setenforce 0 to make the libraries readable.
05-01 09:36:07.818  9886  9886 F DEBUG   :   NOTE: Unreadable libraries:
05-01 09:36:07.818  9886  9886 F DEBUG   :   NOTE:   /data/local/tmp/poc
05-01 09:36:07.818  9886  9886 F DEBUG   :       #00 pc ffffffefcafebab0  <unknown>
05-01 09:36:07.818  9886  9886 F DEBUG   :       #01 pc 00000000001866ec  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!5468ec4faecdff9ca829d2b26980a8!e4a2ccdb56!+1372) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
05-01 09:36:07.818  9886  9886 F DEBUG   :       #02 pc 0000000000185d18  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!2770da8d0aa620c0ea715c1866c504!e4a2ccdb56!+88) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
05-01 09:36:07.818  9886  9886 F DEBUG   :       #03 pc 0000000000185b24  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!15308ad94fb9d06ecc441bc7d751ce!e4a2ccdb56!+100) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
05-01 09:36:07.818  9886  9886 F DEBUG   :       #04 pc 0000000000185a98  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!00392d1e72e084bd76e3a9667b1d57!e4a2ccdb56!+72) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
05-01 09:36:07.818  9886  9886 F DEBUG   :       #05 pc 000000000020cd48  /vendor/lib64/egl/libGLESv2_adreno.so (!!!0000!3a076a0f5bf41e4bcac9395c0e1375!e4a2ccdb56!+648) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766)
05-01 09:36:07.818  9886  9886 F DEBUG   :       #06 pc 00000000000056dc  /data/local/tmp/poc
05-01 09:36:07.818  9886  9886 F DEBUG   :       #07 pc 000000000006a714  /apex/com.android.runtime/lib64/bionic/libc.so (__libc_init+124) (BuildId: 61a049a7ad18156ebc52d8d483539df9)

```

### ch...@google.com (2026-05-01)

Setting milestone because of s0/s1 severity.

### kb...@google.com (2026-05-08)

Qualcomm indicates the fix for this bug is in driver versions >= 881. Preparing Chrome-side workarounds now.

### dx...@google.com (2026-05-11)

Project: chromium/src  

Branch:  main  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7832911>

Add glInvalidateFramebuffer workaround for incomplete FBOs.

---


Expand for full commit details
```
     
    If the framebuffer isn't complete, skip the call to 
    glInvalidateFramebuffer or glDiscardFrameBufferEXT. Apply this 
    workaround to Qualcomm drivers less than version 881. 
     
    Add a unit test verifying the API call is skipped in these situations. 
     
    Co-authored with jetski-cli. 
     
    Bug: 507508103 
    Change-Id: Id030cdf666fc3e83743782c29975988514f516ae 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7832911 
    Auto-Submit: Kenneth Russell <kbr@chromium.org> 
    Reviewed-by: Loko Kung <lokokung@google.com> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1628708}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_unittest_framebuffers.cc`
- A `gpu/command_buffer/tests/gl_invalidate_framebuffer_unittest.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [825a2a4d6c24dd7eb8fc8d628538d73cc6486ae5](https://chromiumdash.appspot.com/commit/825a2a4d6c24dd7eb8fc8d628538d73cc6486ae5)  

Date: Mon May 11 18:37:53 2026


---

### dx...@google.com (2026-05-12)

Project: angle/angle  

Branch:  main  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7834009>

GL: Add glInvalidateFramebuffer workaround for incomplete FBOs.

---


Expand for full commit details
```
     
    If the FBO is incomplete, skip the glInvalidateFramebuffer or 
    glDiscardFramebufferEXT calls. Apply this workaround to Qualcomm 
    drivers earlier than version 881. 
     
    Incorporate unit test from the bug report. 
     
    Co-authored with jetski-cli. 
     
    Bug: chromium:507508103 
    Change-Id: I8f3910b2d5cf4ae41dbe44d2550bc2cad021fea5 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7834009 
    Commit-Queue: Kenneth Russell <kbr@chromium.org> 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/libANGLE/renderer/gl/FramebufferGL.cpp`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [4a6d53434044d4d955731bed2a085155260c5911](https://chromiumdash.appspot.com/commit/4a6d53434044d4d955731bed2a085155260c5911)  

Date: Sat May 9 01:12:55 2026


---

### dx...@google.com (2026-05-12)

Project: chromium/src  

Branch:  main  

Author:  [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com) [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7839298>

Roll ANGLE from 9ba6c809fd46 to 4a6d53434044 (5 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/angle/angle.git/+log/9ba6c809fd46..4a6d53434044 
     
    2026-05-12 kbr@chromium.org GL: Add glInvalidateFramebuffer workaround for incomplete FBOs. 
    2026-05-12 syoussefi@chromium.org Vulkan: Update ImageViewHelper before creating views 
    2026-05-12 syoussefi@chromium.org Vulkan: Don't use mImage for sRGB view update 
    2026-05-12 zork@google.com Vulkan: Fix out-of-bounds read in divisor emulation 
    2026-05-12 syoussefi@chromium.org Roll cherry-picked fixes to VMA 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/angle-chromium-autoroll 
    Please CC abdolrashidi@google.com,angle-team@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in ANGLE: https://bugs.chromium.org/p/angleproject/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Cq-Include-Trybots: luci.chromium.try:android_optional_gpu_tests_rel;luci.chromium.try:linux_optional_gpu_tests_rel;luci.chromium.try:mac_optional_gpu_tests_rel;luci.chromium.try:gpu-fyi-cq-mac-arm64;luci.chromium.try:win_optional_gpu_tests_rel;luci.chromium.try:linux-swangle-try-x64;luci.chromium.try:win-swangle-try-x86 
    Bug: chromium:498372331,chromium:506414791,chromium:507508103 
    Tbr: abdolrashidi@google.com 
    Test: Test: angle_end2end_tests --gtest_filter=InstancingTestES3.IncompleteStrideForLastVertex* 
    Change-Id: I00512e7fa82e8e410a4248a479b20daf8cb9860c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7839298 
    Commit-Queue: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Bot-Commit: chromium-autoroll@skia-public.iam.gserviceaccount.com <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1629045}

```

---

Files:

- M `DEPS`
- M `third_party/angle`

---

Hash: [3af4993c85821e8918f8737b6ab74c1d00bdd2de](https://chromiumdash.appspot.com/commit/3af4993c85821e8918f8737b6ab74c1d00bdd2de)  

Date: Tue May 12 04:28:21 2026


---

### kb...@google.com (2026-05-15)

Submitter: would you please help me verify the workarounds that have been added? It should no longer be able to trigger this crash from the web, either through the validating or passthrough command decoders, nor through a native GLES app linked against ANGLE.

### ch...@google.com (2026-05-15)

**M148** merge request created. **Please update [crbug/513686250](https://crbug.com/513686250) to have this merge reviewed.**

### ch...@google.com (2026-05-15)

**M149** merge request created. **Please update [crbug/513686465](https://crbug.com/513686465) to have this merge reviewed.**

### ha...@gmail.com (2026-05-15)

Sure, have you released a Chrome version of merge? I can download it to verify it.

### kb...@google.com (2026-05-16)

The last of these patches landed in Chrome Canary 150.0.7837.0 (see [this link](https://chromiumdash.appspot.com/commit/3af4993c85821e8918f8737b6ab74c1d00bdd2de)). Current Canary on the Play Store is 150.0.7842.0, so it contains all of them. It's necessary to go to about:flags, change the Passthrough command decoder setting to both "Enabled" and "Disabled", and test both configurations. Thanks.

### ha...@gmail.com (2026-05-16)

This vulnerability appears to be impossible to reproduce.

### kb...@google.com (2026-05-18)

Thank you for confirming.

### dx...@google.com (2026-05-19)

Project: angle/angle  

Branch:  chromium/7827  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7858795>

[M149] GL: Add glInvalidateFramebuffer workaround for...

---


Expand for full commit details
```
     
    ...incomplete FBOs. 
     
    If the FBO is incomplete, skip the glInvalidateFramebuffer or 
    glDiscardFramebufferEXT calls. Apply this workaround to Qualcomm 
    drivers earlier than version 881. 
     
    Incorporate unit test from the bug report. 
     
    Co-authored with jetski-cli. 
     
    Bug: chromium:507508103 
    Fixed: chromium:513686465 
    Change-Id: Icfed56cc597d1eeb1d00f036baab3dc10ed86102 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7858795 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/libANGLE/renderer/gl/FramebufferGL.cpp`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [9e9e80c74cd0dc2ab3bdca38c2145d021451185b](https://chromiumdash.appspot.com/commit/9e9e80c74cd0dc2ab3bdca38c2145d021451185b)  

Date: Sat May 9 01:12:55 2026


---

### dx...@google.com (2026-05-19)

Project: angle/angle  

Branch:  chromium/7778  

Author:  Ken Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7858112>

[M148] GL: Add glInvalidateFramebuffer workaround for...

---


Expand for full commit details
```
     
    ...incomplete FBOs. 
     
    If the FBO is incomplete, skip the glInvalidateFramebuffer or 
    glDiscardFramebufferEXT calls. Apply this workaround to Qualcomm 
    drivers earlier than version 881. 
     
    Incorporate unit test from the bug report. 
     
    Co-authored with jetski-cli. 
     
    Bug: chromium:507508103 
    Fixed: chromium:513686250 
    Change-Id: I257e2700a86d810e4b4bf68b5c1852cb11d222f8 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7858112 
    Reviewed-by: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `include/platform/autogen/FeaturesGL_autogen.h`
- M `include/platform/gl_features.json`
- M `src/libANGLE/renderer/gl/FramebufferGL.cpp`
- M `src/libANGLE/renderer/gl/renderergl_utils.cpp`
- M `src/tests/gl_tests/FramebufferTest.cpp`
- M `util/autogen/angle_features_autogen.cpp`
- M `util/autogen/angle_features_autogen.h`

---

Hash: [64f92abb05021617ce379b392cf66f69fbbe9a5c](https://chromiumdash.appspot.com/commit/64f92abb05021617ce379b392cf66f69fbbe9a5c)  

Date: Sat May 9 01:12:55 2026


---

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7858113>

[M149] Add glInvalidateFramebuffer workaround for incomplete FBOs.

---


Expand for full commit details
```
     
    If the framebuffer isn't complete, skip the call to 
    glInvalidateFramebuffer or glDiscardFrameBufferEXT. Apply this 
    workaround to Qualcomm drivers less than version 881. 
     
    Add a unit test verifying the API call is skipped in these situations. 
     
    Co-authored with jetski-cli. 
     
    Bug: 507508103 
    Change-Id: I300178ceafa6d22c18a8c0186cda72ad9a571a3d 
    Fixed: 513686465 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7858113 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1187} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_unittest_framebuffers.cc`
- A `gpu/command_buffer/tests/gl_invalidate_framebuffer_unittest.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [2b895b9a0ff5076c1a5334caf18647321828383d](https://chromiumdash.appspot.com/commit/2b895b9a0ff5076c1a5334caf18647321828383d)  

Date: Tue May 19 20:06:55 2026


---

### dx...@google.com (2026-05-19)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Kenneth Russell [kbr@chromium.org](mailto:kbr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7858599>

[M148] Add glInvalidateFramebuffer workaround for incomplete FBOs.

---


Expand for full commit details
```
     
    If the framebuffer isn't complete, skip the call to 
    glInvalidateFramebuffer or glDiscardFrameBufferEXT. Apply this 
    workaround to Qualcomm drivers less than version 881. 
     
    Add a unit test verifying the API call is skipped in these situations. 
     
    Co-authored with jetski-cli. 
     
    Bug: 507508103 
    Change-Id: I1adb110f8dc7d61847d1f705228b44eeb18836da 
    Fixed: 513686250 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7858599 
    Reviewed-by: Geoff Lang <geofflang@chromium.org> 
    Reviewed-by: Zhenyao Mo <zmo@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3259} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `gpu/BUILD.gn`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_unittest_framebuffers.cc`
- A `gpu/command_buffer/tests/gl_invalidate_framebuffer_unittest.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [2f7ce8903b7b81d5ce0253149ff5462204d54392](https://chromiumdash.appspot.com/commit/2f7ce8903b7b81d5ce0253149ff5462204d54392)  

Date: Tue May 19 21:15:33 2026


---

### sp...@google.com (2026-05-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Below baseline. Memory Corruption / RCE in a highly privileged process (e.g. GPU or network)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2026-05-19)

Hello, this suddenly becomes "below baseline," which is completely inaccurate. My report clearly conforms to the baseline; you can't do this.

### ha...@gmail.com (2026-05-19)

<https://issues.chromium.org/issues/485945891>
<https://issues.chromium.org/issues/495475001>
Aren't all my vulnerability submissions of the same format and quality?

### kb...@google.com (2026-05-19)

Submitter: please hold off on further comments. I'll discuss this with a representative of the VRP panel tomorrow.

### ha...@gmail.com (2026-05-20)

Based on previous reports, I'm adding a symbolic stack.Thanks

```
  Symbolizing stack using ABI: arm64
  Build fingerprint: 'samsung/pa1qzcx/pa1q:16/BP2A.250605.031.A3/S9310ZCSABZD1_CHCABZD1:user/release-keys'
  Revision: '11'
  pid: 22627, tid: 22654, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
  signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x000b000000010199

  Stack Trace:
    RELADDR   FUNCTION                                                                          FILE:LINE
    0000000000185af8  !!!0000!15308ad94fb9d06ecc441bc7d751ce!e4a2ccdb56!+56) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766  /vendor/lib64/egl/libGLESv2_adreno.so
    0000000000185a98  !!!0000!00392d1e72e084bd76e3a9667b1d57!e4a2ccdb56!+72) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766  /vendor/lib64/egl/libGLESv2_adreno.so
    000000000020cd48  !!!0000!3a076a0f5bf41e4bcac9395c0e1375!e4a2ccdb56!+648) (BuildId: 02d4e5bda5f7509bf3ae03a0a2d87766  /vendor/lib64/egl/libGLESv2_adreno.so
    000000000900baf8  gpu::gles2::GLES2DecoderImpl::InvalidateFramebufferImpl(unsigned int, int, unsigned int const volatile*, int, int, int, int, char const*, gpu::gles2::GLES2DecoderImpl::FramebufferOperation)
  ../../gpu/command_buffer/service/gles2_cmd_decoder.cc:0:16
    v------>  gpu::gles2::GLES2DecoderImpl::DoInvalidateFramebuffer(unsigned int, int, unsigned int const volatile*)  ../../gpu/command_buffer/service/gles2_cmd_decoder.cc:5661:3
    0000000008ff2520  gpu::gles2::GLES2DecoderImpl::HandleInvalidateFramebufferImmediate(unsigned int, void const volatile*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_autogen.h:2249:3
    000000000900a10c  gpu::error::Error gpu::gles2::GLES2DecoderImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/gles2_cmd_decoder.cc:4763:18
    0000000003cf4f44  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:267:35
    00000000090ea084  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:504:22
    00000000090e9dc8  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/command_buffer_stub.cc:173:7
    00000000090ef798  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/gpu_channel.cc:833:13
    v------>  void base::internal::DecayedFunctorTraits<...>::Invoke<...>(...)  ../../base/functional/bind_internal.h:740:12
    v------>  void base::internal::InvokeHelper<true, ...>::MakeItSo<...>(...)  ../../base/functional/bind_internal.h:956:5
    v------>  void base::internal::Invoker<...>::RunImpl<...>(...)  ../../base/functional/bind_internal.h:1069:14
    00000000090f2258  base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)  ../../base/functional/bind_internal.h:982:12
    v------>  base::OnceCallback<void (media::DemuxerStream*)>::Run(media::DemuxerStream*) &&   ../../base/functional/callback.h:155:12
    v------>  void base::internal::DecayedFunctorTraits<...>::Invoke<...>(...)  ../../base/functional/bind_internal.h:815:49
    v------>  void base::internal::InvokeHelper<false, ...>::MakeItSo<...>(...)  ../../base/functional/bind_internal.h:932:12
    v------>  void base::internal::Invoker<...>::RunImpl<...>(...)  ../../base/functional/bind_internal.h:1069:14
    0000000003645628  base::internal::Invoker<...>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
    v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
    0000000003cfa258  gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler.cc:707:29
    0000000003cf9a58  gpu::Scheduler::RunNextTask()                                                     ../../gpu/command_buffer/service/scheduler.cc:625:3
    v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
    00000000067bd134  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:229:34
    v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&,
  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:112:5
    00000000067d7468  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
    00000000067d7084  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
    0000000006773600  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:42:55
    00000000067d7a80  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
    000000000679e608  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:135:14
    000000000c119b24  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:479:14
    000000000674eca0  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)
  ../../content/app/content_main_runner_impl.cc:762:14
    000000000674fb40  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1152:10
    000000000674d6b4  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:358:36
    000000000674e628  content::StartContentMain(bool)                                                   ../../content/app/android/content_main_android.cc:54:10
    00000000002d66bc  art_jni_trampoline+108) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5        /system/framework/arm64/boot.oat
    0000000000689408  nterp_helper+152) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390                      /apex/com.android.art/lib64/libart.so
    000000000028ea5e  offset 0x1eff000) (yh1.run+570                                                    /data/app/~~6rGUIcosSJnaWu7ohK3n5A==/org.chromium.chrome-YoEOtPSTEngWDwEKrgsROw==/base.apk/libmonochrome.so
    00000000000a9500  java.lang.Thread.run+64) (BuildId: 1dfca4cf5b8b42c8355c90c8df5ea0c828c6d4b5       /system/framework/arm64/boot.oat
    0000000000317194  art_quick_invoke_stub+612) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390             /apex/com.android.art/lib64/libart.so
    0000000000302838  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+216) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390  /apex/com.android.art/lib64/libart.so
    00000000004c8298  art::Thread::CreateCallback(void*)+932) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390  /apex/com.android.art/lib64/libart.so
    00000000004c7ee4  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: eb4ec0f1d1c7267591d83fa87cb36390  /apex/com.android.art/lib64/libart.so
    0000000000082740  __pthread_start(void*)+184) (BuildId: 61a049a7ad18156ebc52d8d483539df9            /apex/com.android.runtime/lib64/bionic/libc.so
    0000000000074b98  __start_thread+68) (BuildId: 61a049a7ad18156ebc52d8d483539df9                     /apex/com.android.runtime/lib64/bionic/libc.so


```

### jd...@google.com (2026-05-26)

deleted

### aj...@google.com (2026-06-03)

The panel has reassessed this issue and declines to update the reward in this case - a clear email update was sent to reporters outlining our requirements for reports to include fully symbolized stacks when they were reported, and to include all necessary information in the initially submitted report.

### ch...@google.com (2026-07-31)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ch...@google.com (2026-08-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507508103)*
