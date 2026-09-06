# Chrome sandbox escape via libGLES_mali.so exploited in the wild

| Field | Value |
|-------|-------|
| **Issue ID** | [492218546](https://issues.chromium.org/issues/492218546) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Android, Linux, ChromeOS |
| **Reporter** | he...@google.com |
| **Assignee** | ge...@chromium.org |
| **Created** | 2026-03-13 |
| **Bounty** | $25,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

This vulnerability is at <https://issues.chromium.org/issues/427162086>. The patch doesn't seem to have fixed it properly; it can be bypassed. My guess is that the patch that fixes PauseTransformFeedback, ResumeTransformFeedback, and bypasses geoff is likely related to this vulnerability.

PoC reproduce environment

chrome stable 146.0.7680.115

Android 16pixel 9 pro XL build/CP1A.260305.018

trigger from pixel 9 use mali.html

```
03-13 13:03:10.355 28101 28101 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
03-13 13:03:10.355 28101 28101 F DEBUG   : Build fingerprint: 'google/komodo/komodo:16/CP1A.260305.018/14887507:user/release-keys'
03-13 13:03:10.355 28101 28101 F DEBUG   : Kernel Release: '6.1.145-android14-11-gfa1d6308d1fe-ab14691759'
03-13 13:03:10.355 28101 28101 F DEBUG   : Revision: 'MP1.0'
03-13 13:03:10.355 28101 28101 F DEBUG   : ABI: 'arm64'
03-13 13:03:10.355 28101 28101 F DEBUG   : Timestamp: 2026-03-13 13:03:10.216034468+0800
03-13 13:03:10.355 28101 28101 F DEBUG   : Process uptime: 11s
03-13 13:03:10.355 28101 28101 F DEBUG   : Executable: /system/bin/app_process64
03-13 13:03:10.355 28101 28101 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
03-13 13:03:10.355 28101 28101 F DEBUG   : pid: 27923, tid: 27939, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
03-13 13:03:10.355 28101 28101 F DEBUG   : uid: 10217
03-13 13:03:10.355 28101 28101 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
03-13 13:03:10.355 28101 28101 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
03-13 13:03:10.355 28101 28101 F DEBUG   : esr: 000000008a000000 (PC Alignment Exception 0x22)
03-13 13:03:10.355 28101 28101 F DEBUG   : signal 7 (SIGBUS), code 1 (BUS_ADRALN), fault addr 0x002e00640069006f (read)
03-13 13:03:10.355 28101 28101 F DEBUG   :     x0  00000073cf2894f0  x1  0000000000000000  x2  0000000000000000  x3  0b0000738f4234a8
03-13 13:03:10.355 28101 28101 F DEBUG   :     x4  000000760ee6b050  x5  0000000000000001  x6  0000000000000000  x7  00000072d0a704cc
03-13 13:03:10.355 28101 28101 F DEBUG   :     x8  0000000000000000  x9  0000000000000001  x10 0000000000000000  x11 0000000000000002
03-13 13:03:10.355 28101 28101 F DEBUG   :     x12 0040000000000000  x13 0000000000000001  x14 00000000ffffffff  x15 0000000000000000
03-13 13:03:10.355 28101 28101 F DEBUG   :     x16 002e00640069006f  x17 0000007644a9e360  x18 00000072cf1c8000  x19 00000072c93a5200
03-13 13:03:10.355 28101 28101 F DEBUG   :     x20 000000760ee6b050  x21 00000072c93bd7d0  x22 00000072c93bd8f8  x23 000000760ee6b068
03-13 13:03:10.355 28101 28101 F DEBUG   :     x24 0000000000000000  x25 0000000000000001  x26 000000760ee6b070  x27 0000000000000010
03-13 13:03:10.355 28101 28101 F DEBUG   :     x28 0000000000000008  x29 0000000000000001
03-13 13:03:10.355 28101 28101 F DEBUG   :     lr  000000731dc7dc08  sp  00000072d0a703e0  pc  002e00640069006f  pst 0000000060001400
03-13 13:03:10.355 28101 28101 F DEBUG   :     esr 000000008a000000  vg  0000000000000002
03-13 13:03:10.355 28101 28101 F DEBUG   : 31 total frames
03-13 13:03:10.355 28101 28101 F DEBUG   : backtrace:
03-13 13:03:10.355 28101 28101 F DEBUG   :       #00 pc 000000640069006f  <unknown>
03-13 13:03:10.355 28101 28101 F DEBUG   :       #01 pc 0000000000a08c04  /vendor/lib64/egl/libGLES_mali.so (gles_drawp_handle_dependencies(gles_context*, gles_draw_call*, glescore_submission*)+308) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #02 pc 0000000000a0a678  /vendor/lib64/egl/libGLES_mali.so (gles_drawp_draw_common+1208) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #03 pc 00000000009a20a4  /vendor/lib64/egl/libGLES_mali.so (glDrawArrays+100) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #04 pc 0000000008eabd0c  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #05 pc 0000000008ecaf78  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #06 pc 00000000075be358  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #07 pc 00000000075bd864  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #08 pc 00000000075bd590  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #09 pc 00000000075bd438  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #10 pc 00000000075bd3a8  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #11 pc 00000000072bf5a4  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #12 pc 00000000076e38c8  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #13 pc 0000000005c7d130  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #14 pc 0000000005c54730  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #15 pc 0000000005c54298  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #16 pc 00000000075f2148  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #17 pc 0000000005d0e694  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #18 pc 0000000005c2eadc  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #19 pc 0000000005c3d888  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #20 pc 0000000005c3d5f4  /data/app/~~EkdXpIl488J9cq_XIDSqbQ==/com.google.android.trichromelibrary_768011533-44In0660L55Eqt7SaVvR9w==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 7b80773ca0f2b9243c829f960c001c2e510eea1c)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #21 pc 0000000000d54ed0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #22 pc 00000000006683e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #23 pc 00000000000dec8c  /data/app/~~rY5l9jUqVFcAUi22_c4ffQ==/com.android.chrome-JS_o-aFnvk0GgsHqVndwdA==/base.apk (offset 0x1fc000) (no3.run+564)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #24 pc 00000000003215f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #25 pc 00000000002aaf94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #26 pc 00000000002708ec  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #27 pc 00000000004bdfe0  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #28 pc 00000000004bdb30  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #29 pc 000000000008a714  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 85b03e7fa9ea7fb50d6ced4f441df0ae)
03-13 13:03:10.355 28101 28101 F DEBUG   :       #30 pc 000000000007b3b4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 85b03e7fa9ea7fb50d6ced4f441df0ae)

```

Exploit reproduce environment

1.local test
build with mali\_exp.ccp

2.adb shell and logcat -s LOG

```
--------- beginning of main

 LOG     : uid=2000(shell) gid=2000(shell) groups=2000(shell),1004(input),1007(log),1011(adb),1015(sdcard_rw),1028(sdcard_r),1078(ext_data_rw),1079(ext_obb_rw),3001(net_bt_admin),3002(net_bt),3003(inet),3006(net_bw_stats),3009(readproc),3011(uhid),3012(readtracefs) context=u:r:shell:s0

```

from chromium

chromium version 147.0.7721.0

Oneplus Ace5 coloros 16.0.3

apply code like this <https://issues.chromium.org/issues/427162086>

build chromium with patch renderer code

run exp\_mali.html

adb shell and logcat -s LOG

--------- beginning of main

LOG : uid=10396(u0\_a396) gid=10396(u0\_a396) groups=10396(u0\_a396),3002(net\_bt),3003(inet),9997(everybody),20396(u0\_a396\_cache),50396(all\_a396) context=u:r:untrusted\_app:s0:c140,c257,c512,c768

## Attachments

- [mali.html](attachments/mali.html) (text/html, 6.8 KB)
- [mali_exp.cpp](attachments/mali_exp.cpp) (text/x-c++src, 4.1 KB)
- [mali_exp.h](attachments/mali_exp.h) (text/x-chdr, 4.5 KB)
- [exp_mali.html](attachments/exp_mali.html) (text/html, 201 B)
- exploit.mp4 (video/mp4, 874.8 KB)
- [about-gpu-2026-03-14T00-10-44-477Z.txt.phps](attachments/about-gpu-2026-03-14T00-10-44-477Z.txt.phps) (application/x-httpd-php-source, 56.4 KB)
- exp.mp4 (video/mp4, 4.1 MB)
- [exploit.diff](attachments/exploit.diff) (text/x-diff, 5.6 KB)

## Timeline

### ha...@gmail.com (2026-03-13)

I will delete this video after the VRP evaluation, as it contains some of my private information.

### ha...@gmail.com (2026-03-13)

If you need the control 0x41414141 poc, please let me know. acknowledgement: happy2me

### kb...@chromium.org (2026-03-13)

Submitter: could you please go to `about:gpu` on your ARM phone, click "Download Report to File" and upload the file as an attachment here? I want to see whether the passthrough command decoder and ANGLE are in use and whether the fix for [Issue 427162086](https://issues.chromium.org/issues/427162086) might need to be redone for those code paths.

### dc...@chromium.org (2026-03-13)

Is this issue specific to Android? The other issue was marked as Linux and ChromeOS as well.

### ha...@gmail.com (2026-03-14)

I've uploaded it. No matter what configuration I change, stable seems to trigger automatically.Is the tag wrong? I've only found issues with Mali so far.

### ch...@google.com (2026-03-14)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-14)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### kb...@chromium.org (2026-03-16)

Thanks for the `about:gpu` report. In that browser, ANGLE and the passthrough command decoder are in use.

I misread the fixes for [Issue 427162086](https://issues.chromium.org/issues/427162086); both the validating command decoder and ANGLE+the passthrough command decoder were fixed. Given this I'm not 100% sure how the previous fix is being bypassed. Hoping Geoff and perhaps Vasiliy (CC'd) can test locally.

### ha...@gmail.com (2026-03-17)

The key code is `PauseTransformFeedback` and `ResumeTransformFeedback`.

### bl...@chromium.org (2026-03-23)

FYI: Geoff and I chatted about this offline. He has this issue on his radar but is currently flooded by urgent security vulnerabilities, so won't be able to get to this immediately.

### ha...@gmail.com (2026-03-23)

Yes, but I think this has a higher priority because it may have already been used in the wild.

### ge...@chromium.org (2026-03-23)

Some notes:

Both ANGLE and the validating command decoder track the total number of vertices written to the transform feedback buffer. ANGLE tracks the max vertices possible to draw and [updates it on start/resume](https://source.chromium.org/chromium/chromium/src/+/main:third_party/angle/src/libANGLE/TransformFeedback.cpp;l=237;drc=23c1350a5eb632830a9ece307987fdd6816893f1). The validating decoder checks every draw call if the [new vertex count will overflow](https://source.chromium.org/chromium/chromium/src/+/main:gpu/command_buffer/service/transform_feedback_manager.cc;l=104;drc=23c1350a5eb632830a9ece307987fdd6816893f1).

This bug seems more complicated, the repro case is a lot of buffer switches, pauses and resumes over multiple frames.

I will need a few days to find a device that can repro.

### ha...@gmail.com (2026-03-23)

The best solution would be to have ARM fix it, but they seem unwilling to do so.

### ha...@gmail.com (2026-04-03)

Hi Geoff,have you thought of a solution to this vulnerability?

### ha...@gmail.com (2026-04-08)

This is a complete video I recorded two weeks ago, but I forgot to upload it. The previous video was probably too simple.

### ge...@chromium.org (2026-04-15)

ARM has confirmed that this will be fixed in r56 of their driver.

The Pixel9 which reproduced this still gets regular security updates.

### ha...@gmail.com (2026-05-07)

Hi,Geoff

Is there a fix for this at the Chrome level?

### ch...@google.com (2026-05-13)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ha...@gmail.com (2026-05-20)

Provide Symbolizing stack

```
Symbolizing stack using ABI=arm64
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x74ec658f68 in tid 11282 (CrGpuMain), pid 11266 (ileged_process0)
Build fingerprint: 'google/komodo/komodo:16/CP1A.260405.005/15001963:user/release-keys'
Revision: 'MP1.0'
pid: 11266, tid: 11282, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x00000074ec658f68 (read)

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  0000000001c2d2c4  cobj_instance_get_import_handles+4) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d  /vendor/lib64/egl/libGLES_mali.so
  0000000000a08c04  gles_drawp_handle_dependencies(gles_context*, gles_draw_call*, glescore_submission*)+308) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d  /vendor/lib64/egl/libGLES_mali.so
  0000000000a0a678  gles_drawp_draw_common+1208) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d   /vendor/lib64/egl/libGLES_mali.so
  00000000009a20a4  glDrawArrays+100) (BuildId: 7881438741eeeb5f10dc4d10ccb2f1f88d94c26d              /vendor/lib64/egl/libGLES_mali.so
  00000000030fb9fc  rx::ContextGL::drawArrays(gl::Context const*, gl::PrimitiveMode, int, int)        ../../third_party/angle/src/libANGLE/renderer/gl/ContextGL.cpp:356:31
  v------>  gl::Context::drawArrays(gl::PrimitiveMode, int, int)                              ../../third_party/angle/src/libANGLE/Context.inl.h:168:40
  0000000007a63d74  GL_DrawArrays                                                                     ../../third_party/angle/src/libGLESv2/entry_points_gles_2_0_autogen.cpp:1819:22
  00000000090328e8  gpu::gles2::GLES2DecoderPassthroughImpl::DoDrawArrays(unsigned int, int, int)     ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:1159:10
  0000000009027a04  gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:742:20
  0000000003cf4f44  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:267:35
  00000000090e9c68  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/command_buffer_stub.cc:149:0
  v------>  base::ObserverList<gpu::CommandBufferStub::DestructionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>::Iter<true>::clamped_max_index() const  ../../base/observer_list.h:271:14
  v------>  base::ObserverList<gpu::CommandBufferStub::DestructionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>::Iter<true>::is_end() const  ../../base/observer_list.h:274:54
  v------>  base::ObserverList<gpu::CommandBufferStub::DestructionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>::Iter<true>::operator==(base::ObserverList<gpu::CommandBufferStub::DestructionObserver, false, (base::ObserverListReentrancyPolicy)1, base::internal::UncheckedObserverAdapter<(partition_alloc::internal::RawPtrTraits)0, false>>::Iter<true> const&) const  ../../base/observer_list.h:221:15
  00000000090e99ac  gpu::CommandBufferStub::Destroy()                                                 ../../gpu/ipc/service/command_buffer_stub.cc:338:23
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::__base_destruct_at_end(gpu::SyncToken*)  gen/third_party/libc++/src/include/__vector/vector.h:0:5
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::clear()  gen/third_party/libc++/src/include/__vector/vector.h:549:5
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::__destroy_vector::operator()()  gen/third_party/libc++/src/include/__vector/vector.h:248:16
  v------>  std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>::~vector()  gen/third_party/libc++/src/include/__vector/vector.h:259:67
  v------>  gpu::Scheduler::Task* std::__Cr::construct_at<gpu::Scheduler::Task, base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>, gpu::Scheduler::Task*>(gpu::Scheduler::Task*, base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)  gen/third_party/libc++/src/include/__memory/construct_at.h:37:3
  v------>  gpu::Scheduler::Task* std::__Cr::__construct_at<gpu::Scheduler::Task, base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>, gpu::Scheduler::Task*>(gpu::Scheduler::Task*, base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)  gen/third_party/libc++/src/include/__memory/construct_at.h:45:10
  v------>  void std::__Cr::allocator_traits<std::__Cr::allocator<gpu::Scheduler::Task>>::construct<gpu::Scheduler::Task, base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>, 0>(std::__Cr::allocator<gpu::Scheduler::Task>&, gpu::Scheduler::Task*, base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)  gen/third_party/libc++/src/include/__memory/allocator_traits.h:302:5
  v------>  void std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::__emplace_back_assume_capacity<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)  gen/third_party/libc++/src/include/__vector/vector.h:480:5
  v------>  gpu::Scheduler::Task& std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::emplace_back<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)::'lambda'()::operator()() const  gen/third_party/libc++/src/include/__vector/vector.h:1145:9
  v------>  void std::__Cr::__if_likely_else<gpu::Scheduler::Task& std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::emplace_back<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)::'lambda'(), gpu::Scheduler::Task& std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::emplace_back<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)::'lambda0'()>(bool, gpu::Scheduler::Task& std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::emplace_back<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)::'lambda'(), gpu::Scheduler::Task& std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::emplace_back<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)::'lambda0'())  gen/third_party/libc++/src/include/__vector/vector.h:1126:7
  v------>  gpu::Scheduler::Task& std::__Cr::vector<gpu::Scheduler::Task, std::__Cr::allocator<gpu::Scheduler::Task>>::emplace_back<base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>>(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>&, base::OnceCallback<void ()>&&, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>>&&)  gen/third_party/libc++/src/include/__vector/vector.h:1142:3
  00000000090ef37c  gpu::GpuChannelMessageFilter::FlushDeferredRequests(std::__Cr::vector<mojo::StructPtr<gpu::mojom::DeferredRequest>, std::__Cr::allocator<mojo::StructPtr<gpu::mojom::DeferredRequest>>>, unsigned int)  ../../gpu/ipc/service/gpu_channel.cc:411:11
  00000000090f1e3c  gpu::GpuChannel::GetMemoryUsage() const                                           ../../gpu/ipc/service/gpu_channel.cc:1117:0
  v------>  base::OnceCallback<void (media::DemuxerStream*)>::Run(media::DemuxerStream*) &&   ../../base/functional/callback.h:155:12
  v------>  void base::internal::DecayedFunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*&&>::Invoke<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*>(base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&)  ../../base/functional/bind_internal.h:815:49
  v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, void, 0ul>::MakeItSo<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:932:12
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (media::DemuxerStream*)>, base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1069:14
  0000000003645628  base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (BrowserWindowInterface*)>&&, base::raw_ptr<BrowserWindowInterface, (partition_alloc::internal::RawPtrTraits)1>&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (BrowserWindowInterface*)>, base::internal::UnretainedWrapper<BrowserWindowInterface, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)1>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  0000000003cfa258  gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler.cc:707:29
  0000000003cf9a58  gpu::Scheduler::RunNextTask()                                                     ../../gpu/command_buffer/service/scheduler.cc:625:3
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  00000000067bd134  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:229:34
  v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:112:5
  00000000067d7468  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
  00000000067d7084  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
  0000000006773600  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:42:55
  00000000067d7a80  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
  000000000679e608  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:135:14
  v------>  content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0::operator()(mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>) const  ../../content/gpu/gpu_child_thread.cc:276:35
  v------>  void base::internal::DecayedFunctorTraits<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>&&>::Invoke<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>(content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0&&, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>&&)  ../../base/functional/bind_internal.h:658:12
  v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0&&, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>&&>, void, 0ul>::MakeItSo<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0, std::__Cr::tuple<mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>>(content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0&&, std::__Cr::tuple<mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>&&)  ../../base/functional/bind_internal.h:932:12
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0&&, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>&&>, base::internal::BindState<false, false, false, content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>, void ()>::RunImpl<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0, std::__Cr::tuple<mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>, 0ul>(content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0&&, std::__Cr::tuple<mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1069:14
  000000000c1193d8  base::internal::Invoker<base::internal::FunctorTraits<content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0&&, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>&&>, base::internal::BindState<false, false, false, content::GpuChildThread::CreateAndroidOverlay(scoped_refptr<base::SingleThreadTaskRunner>, base::UnguessableToken const&, media::AndroidOverlayConfig)::$_0, mojo::PendingReceiver<media::mojom::AndroidOverlayProvider>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
  000000000674eca0  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:762:14
  000000000674fb40  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1152:10
  000000000674d6b4  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:358:36
  000000000674e628  content::StartContentMain(bool)                                                   ../../content/app/android/content_main_android.cc:54:10
  0000000000d5364c  art_jni_trampoline+108                                                            /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  0000000000668468  nterp_helper+152) (BuildId: 7087b2f2160bfbf3335d54ba9779e325                      /apex/com.android.art/lib64/libart.so
  000000000028ea5e  offset 0x1eff000) (yh1.run+570                                                    /data/app/~~fcwjjNufI2Ac7HDiD94CoQ==/org.chromium.chrome-WgFrL03y443EE9jXjmbP-Q==/base.apk/libmonochrome.so
  00000000003215f0  java.lang.Thread.run+64                                                           /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  00000000002aad94  art_quick_invoke_stub+612) (BuildId: 7087b2f2160bfbf3335d54ba9779e325             /apex/com.android.art/lib64/libart.so
  00000000002707ac  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 7087b2f2160bfbf3335d54ba9779e325  /apex/com.android.art/lib64/libart.so
  00000000004bdc28  art::Thread::CreateCallback(void*)+1184) (BuildId: 7087b2f2160bfbf3335d54ba9779e325  /apex/com.android.art/lib64/libart.so
  00000000004bd778  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 7087b2f2160bfbf3335d54ba9779e325  /apex/com.android.art/lib64/libart.so
  000000000008a714  __pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: a246e817808ed398a3423870bfeba4a6  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000007b3b4  __start_thread+68) (BuildId: a246e817808ed398a3423870bfeba4a6                     /apex/com.android.runtime/lib64/bionic/libc.so


```

### dx...@google.com (2026-05-27)

Project: angle/angle  

Branch:  main  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7864196>

Validate that TF buffers cannot be modified when TF is unbound.

---


Expand for full commit details
```
     
    The buffer transform feedback conflict validation would only track 
    buffers that are bound to the current transform feedback object. Since 
    it is possible to pause transform feedback and unbind it, the buffers 
    could be modified when in this state. 
     
    Add additional tracking for when the buffer is attached to an active 
    transform feedback. 
     
    Apply this validation to hardened contexts as well as WebGL since it is 
    undefined behaviour in the GL spec to use a buffer for transform 
    feedback and other usages simultaneously. 
     
    Fixed: chromium:492218546 
    Fixed: chromium:513925114 
    Change-Id: I45b99ce847d74946870ba35fc9a17294e3386523 
    Reviewed-on: https://chromium-review.googlesource.com/c/angle/angle/+/7864196 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org>

```

---

Files:

- M `src/libANGLE/Buffer.cpp`
- M `src/libANGLE/Buffer.h`
- M `src/libANGLE/TransformFeedback.cpp`
- M `src/libANGLE/VertexArray.cpp`
- M `src/libANGLE/validationES.cpp`
- M `src/libANGLE/validationES2.cpp`
- M `src/libANGLE/validationES3.cpp`
- M `src/tests/gl_tests/TransformFeedbackTest.cpp`
- M `src/tests/gl_tests/WebGLCompatibilityTest.cpp`

---

Hash: [ee21230bc87855404b87b97b738091cd04b0d3f3](https://chromiumdash.appspot.com/commit/ee21230bc87855404b87b97b738091cd04b0d3f3)  

Date: Wed May 20 15:46:30 2026


---

### ch...@google.com (2026-05-28)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-28)

**M148** merge request created. **Please update [crbug/517405606](https://crbug.com/517405606) to have this merge reviewed.**

### ch...@google.com (2026-05-28)

**M149** merge request created. **Please update [crbug/517405678](https://crbug.com/517405678) to have this merge reviewed.**

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Baseline. Sandbox escape / Memory corruption / RCE in a non-sandboxed process.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2026-06-05)

Hello, is the bounty amount correct? My RCE video showed,and it should be $250000.00 for this issue?

### aj...@google.com (2026-06-05)

Panel: see comment 26

### aj...@google.com (2026-06-05)

reporter: could you briefly explain exactly which files include demonstration of the exploit and what the exploit demonstrates (rip control, controlled write, code execution) and which devices are necessary to demonstrate it?

### ha...@gmail.com (2026-06-05)

Panel: exploit.diff and mali\_exp.h demonstrate an exploit in Chrome's GPU process. They primarily demonstrate code execution, specifically executing the `id` command. This vulnerability can directly control the RIP/PC. The device used in the demonstration is a OnePlus Ace5 with ColorOS 16.0.3. The demonstration video is exploit.mp4.You can see the video.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $225000.00 for this report.

Rationale for this decision:
Well done!


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2026-07-01)

What's wrong?I cant still reproduce it with mali.html.There may be other triggering paths; when will the Pixel 9 patch rollout?

### ch...@google.com (2026-09-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. Sandbox escape / Memory corruption / RCE in a non-sandboxed process.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492218546)*
