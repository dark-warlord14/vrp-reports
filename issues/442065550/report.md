# libusc UAF via WebGPU shaders at MergeConsecutiveBarriersBP

| Field | Value |
|-------|-------|
| **Issue ID** | [442065550](https://issues.chromium.org/issues/442065550) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Dawn>Tint |
| **Platforms** | Android |
| **Reporter** | a7...@gmail.com |
| **Assignee** | jr...@google.com |
| **Created** | 2025-08-30 |
| **Bounty** | $25,000.00 |

## Description

##### VULNERABILITY DETAILS

Chrome on Android translates WebGPU shaders to SPIR-V. On Pixel 10 devices, these SPIR-V shaders are eventually passed to the vendor-specific libraries libufwriter.so and libusc.so for optimization and native code generation. This bug report is about a WebGPU shader that crashes com.android.chrome on an MTE-enable device. MTE detects a UAF in `MergeConsecutiveBarriersBP`.

#### VERSION

Device: Pixel 10 Pro   

Android build number: BD3A.250721.001   

Chromium: 139.0.7258.158

#### REPRODUCER

There are 2 ways to reproduce the issue, within Chrome and a standalone reproducer. The problematic shader itself is not particularly complex:

```
@compute @workgroup_size(16, 16, 1)
fn main() {
    storageBarrier();
    storageBarrier();
}

```
##### REPRODUCTION CASE (Chromium)

Enable MTE on the device and for Chrome (as described here: <https://googleprojectzero.blogspot.com/2023/11/first-handset-with-mte-on-market.html>). Then open the attached HTML, you should get the following message in your adb logs:

```
08-30 19:53:13.711 11118 11118 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
08-30 19:53:13.711 11118 11118 F DEBUG   : Build fingerprint: 'google/blazer/blazer:16/BD3A.250721.001/13808258:user/release-keys'
08-30 19:53:13.711 11118 11118 F DEBUG   : Kernel Release: '6.6.82-android15-8-gd4aed7ed470e-ab13759939-4k'
08-30 19:53:13.711 11118 11118 F DEBUG   : Revision: 'MP1.0'
08-30 19:53:13.711 11118 11118 F DEBUG   : ABI: 'arm64'
08-30 19:53:13.711 11118 11118 F DEBUG   : Timestamp: 2025-08-30 19:53:13.601761139+0200
08-30 19:53:13.711 11118 11118 F DEBUG   : Process uptime: 36s
08-30 19:53:13.711 11118 11118 F DEBUG   : Executable: /system/bin/app_process64
08-30 19:53:13.711 11118 11118 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
08-30 19:53:13.711 11118 11118 F DEBUG   : pid: 10923, tid: 10944, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
08-30 19:53:13.711 11118 11118 F DEBUG   : uid: 10225
08-30 19:53:13.711 11118 11118 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
08-30 19:53:13.711 11118 11118 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
08-30 19:53:13.711 11118 11118 F DEBUG   : esr: 0000000092000011 (Data Abort Exception 0x24)
08-30 19:53:13.711 11118 11118 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000006ffb8c0828 (read)
08-30 19:53:13.711 11118 11118 F DEBUG   :     x0  00000071687bdf04  x1  0000006e2bb17d84  x2  0500006ffb8c0710  x3  0000006e2bb17d48
08-30 19:53:13.711 11118 11118 F DEBUG   :     x4  0000006e2bb17d88  x5  0000000000000170  x6  0000000000000001  x7  0a00006f0b8e66b8
08-30 19:53:13.711 11118 11118 F DEBUG   :     x8  0000000000000060  x9  0a00006ffb8b4da0  x10 00000000000001c0  x11 0100006ffb8c0880
08-30 19:53:13.711 11118 11118 F DEBUG   :     x12 000000000000003f  x13 00000000ff3b5930  x14 090000705b8c9f00  x15 000000000000003f
08-30 19:53:13.711 11118 11118 F DEBUG   :     x16 00000071687b0158  x17 00000071687372f0  x18 0000006e2a234000  x19 0a00006f0b8e4980
08-30 19:53:13.711 11118 11118 F DEBUG   :     x20 0000006e2bb17f0c  x21 0500006ffb8c0720  x22 0500006ffb8d29a0  x23 0a00006ffb8b4da0
08-30 19:53:13.711 11118 11118 F DEBUG   :     x24 0000000000000001  x25 0000000000000018  x26 0f00006ffb8a64e0  x27 030000702b8cc110
08-30 19:53:13.711 11118 11118 F DEBUG   :     x28 0a00006f0b8e64e8  x29 0000006e2bb17e10
08-30 19:53:13.711 11118 11118 F DEBUG   :     lr  0015ae6e7a1577bc  sp  0000006e2bb17e10  pc  0000006e7a1577dc  pst 0000000060001000
08-30 19:53:13.711 11118 11118 F DEBUG   :     esr 0000000092000011
08-30 19:53:13.711 11118 11118 F DEBUG   : 40 total frames
08-30 19:53:13.711 11118 11118 F DEBUG   : backtrace:
08-30 19:53:13.711 11118 11118 F DEBUG   :       #00 pc 00000000000e07dc  /vendor/lib64/libusc.so (MergeConsecutiveBarriersBP+172) (BuildId: d02d10daa1af7a5b6b41431bd228dafd)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #01 pc 0000000000163c4c  /vendor/lib64/libusc.so (DoOnCfgBasicBlocks+172) (BuildId: d02d10daa1af7a5b6b41431bd228dafd)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #02 pc 0000000000163d18  /vendor/lib64/libusc.so (DoOnAllBasicBlocks+88) (BuildId: d02d10daa1af7a5b6b41431bd228dafd)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #03 pc 00000000000e071c  /vendor/lib64/libusc.so (MergeConsecutiveBarriers+60) (BuildId: d02d10daa1af7a5b6b41431bd228dafd)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #04 pc 00000000000662d4  /vendor/lib64/libusc.so (PVRUniFlexCompileToHw+4884) (BuildId: d02d10daa1af7a5b6b41431bd228dafd)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #05 pc 00000000000aa250  /vendor/lib64/hw/vulkan.powervr.so (IMG_vkCreateComputePipelines+1024) (BuildId: 6da1e8d2c4cb26e4cd69d13e854ee8c3)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #06 pc 00000000027ecebc  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #07 pc 000000000700b918  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #08 pc 0000000002786c60  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #09 pc 0000000002786a48  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #10 pc 0000000008487a24  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #11 pc 000000000848d2cc  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #12 pc 0000000008556644  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochr
ome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #13 pc 0000000008556750  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #14 pc 00000000085541cc  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #15 pc 0000000006a77778  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #16 pc 0000000006a7694c  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #17 pc 0000000006a76630  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #18 pc 0000000006a76520  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #19 pc 0000000006a7646c  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #20 pc 0000000006aa9fbc  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #21 pc 0000000006db7e78  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #22 pc 000000000550a46c  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #23 pc 00000000054d6e14  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #24 pc 00000000054d6890  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #25 pc 0000000006d167e4  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #26 pc 000000000551a734  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #27 pc 0000000005491fc0  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #28 pc 00000000054c7a8c  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #29 pc 0000000005530720  /data/app/~~C1FpiXhvItaUisPzXWxM6w==/com.google.android.trichromelibrary_725815833-lPcSLodmsRFmpN3W7uHHzA==/base.apk!libmonochrome_64.so (offset 0x8dc000) (Java_J_N_IZ+296) (BuildId: 1486a57a4ba7b56144721fcd544c8b14f165e53b)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #30 pc 00000000002e1460  /system/framework/arm64/boot.oat (art_jni_trampoline+112) (BuildId: 43c19f4791b03b034c6738462e3654bda9ffc2c4)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #31 pc 0000000000689588  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: d57befa204d91d200485ace46c3b8814)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #32 pc 00000000000e2906  /data/app/~~vQJpNviU_xKKUAYTT3SOvQ==/com.android.chrome-bp-o8wmwxdWv5y425joZtQ==/base.apk (offset 0x145000) (If0.run+646)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #33 pc 00000000000a94f0  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: 43c19f4791b03b034c6738462e3654bda9ffc2c4)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #34 pc 0000000000328194  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: d57befa204d91d200485ace46c3b8814)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #35 pc 00000000002d9348  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+216) (BuildId: d57befa204d91d200485ace46c3b8814)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #36 pc 0000000000421028  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+932) (BuildId: d57befa204d91d200485ace46c3b8814)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #37 pc 0000000000420c74  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: d57befa204d91d200485ace46c3b8814)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #38 pc 00000000000875d4  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 4a26e04ea2224937eb165e0d5fee74ad)
08-30 19:53:13.711 11118 11118 F DEBUG   :       #39 pc 0000000000079e54  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 4a26e04ea2224937eb165e0d5fee74ad)
08-30 19:53:13.711 11118 11118 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```
##### REPRODUCTION CASE (Standalone)

- Compile the attached standalone.cpp via: `~/android-ndk-r27/toolchains/llvm/prebuilt/linux-x86_64/bin/x86_64-linux-android35-clang++ --target=aarch64-linux-android35 -lvulkan standalone.cpp -o reproducer`
- Push the resulting binary and comp.spv onto the device.
- Enable MTE sync for the reproducer: `adb shell setprop arm64.memtag.process.reproducer sync`
- Run the reproducer via `./reproducer comp.spv`

## Attachments

- [comp.spv](attachments/comp.spv) (application/octet-stream, 280 B)
- [a.html](attachments/a.html) (text/html, 2.7 KB)
- [standalone.cpp](attachments/standalone.cpp) (text/x-c++src, 7.6 KB)

## Timeline

### li...@chromium.org (2025-09-02)

I don't have an MTE device to reproduce. Reporter, is it possible for you to upload a screen recording of the crash, and also is it possible for you to get a more symbolized stack trace?

### a7...@gmail.com (2025-09-02)

Within libusc.so symbols are not going to get any better as it is a closed-source lib. So far the stack trace of my custom build looks pretty identical, but I'm working on it. I found a security contact at Imagination and also reported the issue there, I'll keep you posted if the vendor provides any information.

### pe...@google.com (2025-09-02)

Thank you for providing more feedback. Adding the requester to the CC list.

### el...@chromium.org (2025-09-02)

Thanks for reporting this to Imagination. I also don't have an MTE device to repro this with, and given (as you say) that the bug is in a closed-source component we don't own I am not sure what else we might do here. I'm going to move this into the Dawn component for someone to investigate whether we can mitigate this ourselves, but it may be ExternalDependency.

### el...@chromium.org (2025-09-02)

Marked FoundIn-139,140,141 (although it probably affects any version on a device with a vulnerable libusc), OS-Android, Pri-1 Sev-1 due to unsandboxed code execution.

### ds...@chromium.org (2025-09-02)

Looking at the issue, I don't think there is anything specific we can do at this point. Need to wait for feedback from the vendor.

### ch...@google.com (2025-09-03)

Setting milestone because of s0/s1 severity.

### a7...@gmail.com (2025-09-10)

I haven't heard anything at all from the vendor, not even a confirmation email that an issue was filed. If anyone has a direct contact feel free to reach out to them.

### jr...@google.com (2025-09-10)

We have raised the issue with the vendor and they have reproduced on their side.

We are now waiting on a fix and a security impact assessment.

### ch...@google.com (2025-10-09)

jrprice: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### jr...@google.com (2025-10-09)

See internal bug [b/442637050](https://issues.chromium.org/issues/442637050) which is pending Android security review.

### an...@chromium.org (2025-10-30)

[security shepherd] Hi jrprice@, looks like [b/442637050](https://issues.chromium.org/issues/442637050) has been fixed. Can you comment on the next steps? Thanks!

### ch...@google.com (2025-10-30)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2025-11-04)

jrprice: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-19)

jrprice: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ri...@google.com (2025-11-24)

[Secondary Shepherd] Seems like the repro case is fixed from [b/442637050#comment13](https://issues.chromium.org/issues/442637050#comment13). Marking this as fixed. Feel free to re-open if necessary.

### ch...@google.com (2025-11-24)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dn...@google.com (2025-11-26)

Fixed by a driver update in Pixel 10. See [b/442637050](https://issues.chromium.org/issues/442637050)

### ch...@google.com (2025-11-27)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M142. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M143. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142, 143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Sandbox escape / Memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-03-05)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Sandbox escape / Memory corruption in a non-sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/442065550)*
