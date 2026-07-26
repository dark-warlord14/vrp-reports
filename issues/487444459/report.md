# OOB Write in CalculateNPOTTwiddleSparsePageMap3D cause android chrome gpu crash

| Field | Value |
|-------|-------|
| **Issue ID** | [487444459](https://issues.chromium.org/issues/487444459) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Internals>GPU>ANGLE |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ge...@google.com |
| **Created** | 2026-02-25 |
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

```
005a2b10    int64_t CalculateNPOTTwiddleSparsePageMap3D(int32_t arg1, int32_t arg2, uint32_t arg3, uint32_t arg4, uint32_t arg5, int32_t arg6, int32_t arg7, 
005a2b10      int32_t arg8, int32_t arg9, int32_t arg10, int32_t arg11, int32_t arg12, int32_t arg13, char arg14, int32_t* arg15, int64_t arg16, 
005a2b10      int32_t* arg17)

005a2b34        int128_t v0
005a2b34        v0.d = arg10
005a2b3c        int128_t v1
005a2b3c        v1.q = -1
005a2b3c        v1:8.q = -1
005a2b40        int64_t v2
005a2b40        v2.d = 1
005a2b40        v2:4.d = 1
005a2b4c        v0:4.d = arg11
005a2b60        uint32_t var_68 = arg5
005a2b68        int128_t v0_1 = v0 + sx.o(-1)
005a2b74        v1.d = v0_1.d u>> 1
005a2b74        v1:4.d = v0_1:4.d u>> 1
005a2b78        int32_t x8_2 = (arg9 - 1) | (arg9 - 1) u>> 1
005a2b7c        int128_t v0_2 = vorr_s8(v1, v0_1)
005a2b80        int32_t x8_3 = x8_2 | x8_2 u>> 2
005a2b84        v1.d = v0_2.d u>> 2
005a2b84        v1:4.d = v0_2:4.d u>> 2
005a2b88        int32_t x8_4 = x8_3 | x8_3 u>> 4
005a2b8c        int128_t v0_3 = vorr_s8(v1, v0_2)
005a2b90        v1.d = v0_3.d u>> 4
005a2b90        v1:4.d = v0_3:4.d u>> 4
005a2b94        int32_t x8_5 = x8_4 | x8_4 u>> 8
005a2b98        int128_t v0_4 = vorr_s8(v1, v0_3)
005a2ba0        v1.d = v0_4.d u>> 8
005a2ba0        v1:4.d = v0_4:4.d u>> 8
005a2ba8        int128_t v0_5 = vorr_s8(v1, v0_4)
005a2bb0        v1.d = v0_5.d u>> 0x10
005a2bb0        v1:4.d = v0_5:4.d u>> 0x10
005a2bb8        uint32_t x8_8 = arg1 u/ arg2
005a2bc0        int64_t v0_7 = vorr_s8(v1, v0_5) + v2
005a2bc4        uint32_t x28 = v0_7.d
005a2bc8        uint32_t x20 = v0_7:4.d
005a2bd8        int32_t x12 =
005a2bd8            (arg1 + ((x8_5 | x8_5 u>> 0x10) + 1) * arg2 * x28 * x20 - 1) & neg.d(arg1)
005a2be0        uint64_t x11 = zx.q(x12 u/ arg1)
005a2be0        
005a2bec        if ((zx.d(arg14) & 1) != 0 && arg1 u<= x12)
005a2bfc            unimplemented  {mov z0.b, #0}
005a2c00            unimplemented  {whilelo p0.b, xzr, x10}
005a2c00            
005a2c10            do
005a2c04                unimplemented  {st1b {z0.b}, p0, [x21, x9]}
005a2c08                unimplemented  {addvl x9, x9, #0x1}
005a2c0c                unimplemented  {whilelo p0.b, x9, x10}
005a2c10            while (x11.d - 1 s< 0)
005a2c10        
005a2c14        int64_t result = 0
005a2c24        uint64_t var_a8_1
005a2c24        int32_t var_90_1
005a2c24        int32_t var_8c_1
005a2c24        int32_t var_80_1
005a2c24        int32_t x8_9
005a2c24        int32_t x22_1
005a2c24        
005a2c24        if (x8_8 == 0x10)
005a2c7c            x8_9 = 2
005a2c88        label_5a2c88:
005a2c88            var_a8_1 = x11
005a2c8c            x22_1 = 4
005a2c90            var_90_1 = x12
005a2c90            var_8c_1 = x8_9
005a2c94            var_80_1 = x8_9
005a2c98            goto label_5a2cd8
005a2c98        
005a2c2c        if (x8_8 == 0x40)
005a2c84            x8_9 = 4
005a2c84            goto label_5a2c88
005a2c84        
005a2c34        if (x8_8 == 0x20)
005a2c3c            var_90_1 = x12
005a2c40            var_a8_1 = x11
005a2c44            x22_1 = 4
005a2c48            var_80_1 = 4
005a2c50            var_8c_1 = 2
005a2c54            goto label_5a2cd8
005a2c54        
005a2c5c        if (x8_8 == 4)
005a2ca0            var_90_1 = x12
005a2ca4            var_a8_1 = x11
005a2ca8            var_80_1 = 2
005a2cb0            var_8c_1 = 1
005a2cb4        label_5a2cb4:
005a2cb4            x22_1 = 2
005a2cd8        label_5a2cd8:
005a2cd8            
005a2cd8            if (var_68 u< arg8)
005a2d94                uint32_t x9_14
005a2d94                
005a2d94                do
005a2cf8                    uint32_t x25_1 = arg4
005a2cf8                    
005a2d00                    if (arg4 u< arg7)
005a2d78                        do
005a2d10                            if (arg3 u< arg6)
005a2d14                                uint32_t x26_1 = arg3
005a2d14                                
005a2d68                                do
005a2d38                                    int32_t x8_18 = SparsePageTwiddle3D.__un...7502316943677858827314526628860272693(
005a2d38                                        (x8_5 | x8_5 u>> 0x10) + 1, x28, x20, x26_1, x25_1, 
005a2d38                                        var_68) * arg2
005a2d44                                    *(arg16 + zx.q((x8_18 + arg12) u/ arg1)) = 1
005a2d44                                    
005a2d48                                    if (arg13 != 0)
005a2d58                                        *(arg16
005a2d58                                            + zx.q((arg12 + arg13 - 1 + x8_18) u/ arg1)) = 1
005a2d58                                    
005a2d60                                    x26_1 += x22_1
005a2d68                                while (x26_1 u< arg6)
005a2d68                            
005a2d70                            x25_1 += var_80_1
005a2d78                        while (x25_1 u< arg7)
005a2d78                    
005a2d84                    x9_14 = var_68 + var_8c_1
005a2d90                    var_68 = x9_14
005a2d94                while (x9_14 u< arg8)
005a2d94            
005a2da0            int32_t x8_26
005a2da0            int32_t x10_2
005a2da0            
005a2da0            if (arg1 u<= var_90_1)
005a2db4                int64_t x9_15 = 0
005a2db8                x8_26 = 0
005a2dbc                x10_2 = 0
005a2dbc                
005a2de0                do
005a2dc8                    uint32_t x12_2 = zx.d(*(arg16 + zx.q(arg12 u/ arg1 + x9_15.d)))
005a2dd0                    x10_2 += x12_2
005a2dd0                    
005a2dd4                    if (x12_2 != 0)
005a2dd4                        x8_26 = x9_15.d
005a2dd4                    
005a2dd8                    x9_15 += 1
005a2de0                while (x9_15 u< var_a8_1)
005a2da0            else
005a2da4                x10_2 = 0
005a2da8                x8_26 = 0
005a2da8            
005a2de8            result = 1
005a2dec            *arg15 = x10_2
005a2df0            *arg17 = x8_26
005a2c5c        else if (x8_8 == 8)
005a2c6c            var_a8_1 = x11
005a2c70            var_90_1 = x12
005a2c70            var_8c_1 = 2
005a2c74            var_80_1 = 2
005a2c78            goto label_5a2cb4
005a2c78        
005a2e10        return result


```

##RCA##

The vulnerability exists within CalculateNPOTTwiddleSparsePageMap3D due to an insecure 32-bit integer multiplication when calculating the total virtual memory page count.Specifically, at address 0x005a2bd8, the driver computes the total texture size using the rounded-up Power-of-Two (POT) dimensions:TotalSize = ui32PotWidth \* ui32PotHeight \* ui32PotDepth \* ui32BytesPerBlockWhen provided with dimensions like 600x600x600 (rounded to 1024), the product $1024 \times 1024 \times 1024 \times 4$ results in $2^{32}$, which overflows to $0$ in a 32-bit unsigned integer context. This causes ui32VMPageCount (register x11) to be calculated as 0.Subsequently, the loop at 0x005a2d44 performs memory writes to the pbOutUsedPageMap buffer (register arg16). Since the buffer was under-allocated based on the overflowed page count, this leads to an out-of-bounds write of the value 0x01 across the heap, as the loop bounds are still controlled by the original, non-overflowed dimensions.

VERSION
Chrome Version: [145.0.7632.109] + [stable, beta, or dev]

Operating System: [google/frankel/frankel:16/BP4A.260205.001/14624666:user/release-keys]

REPRODUCTION CASE

1.open poc.html

2.crash

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION

Type of crash: [GPU]

Crash State:

```

02-25 13:16:47.192 30757 30757 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
02-25 13:16:47.192 30757 30757 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/BP4A.260205.001/14624666:user/release-keys'
02-25 13:16:47.192 30757 30757 F DEBUG   : Kernel Release: '6.6.98-android15-8-g4b48560cd07d-ab14239520-4k'
02-25 13:16:47.192 30757 30757 F DEBUG   : Revision: 'MP1.0'
02-25 13:16:47.192 30757 30757 F DEBUG   : ABI: 'arm64'
02-25 13:16:47.192 30757 30757 F DEBUG   : Timestamp: 2026-02-25 13:16:47.055299991+0800
02-25 13:16:47.192 30757 30757 F DEBUG   : Process uptime: 11s
02-25 13:16:47.192 30757 30757 F DEBUG   : Executable: /system/bin/app_process64
02-25 13:16:47.192 30757 30757 F DEBUG   : Cmdline: org.chromium.chrome:privileged_process4
02-25 13:16:47.192 30757 30757 F DEBUG   : pid: 30702, tid: 30719, name: CrGpuMain  >>> org.chromium.chrome:privileged_process4 <<<
02-25 13:16:47.192 30757 30757 F DEBUG   : uid: 10327
02-25 13:16:47.192 30757 30757 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
02-25 13:16:47.192 30757 30757 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
02-25 13:16:47.192 30757 30757 F DEBUG   : esr: 0000000092000047 (Data Abort Exception 0x24)
02-25 13:16:47.192 30757 30757 F DEBUG   : signal 11 (SIGSEGV), code 2 (SEGV_ACCERR), fault addr 0x0000007994f3f8f0 (write)
02-25 13:16:47.192 30757 30757 F DEBUG   :     x0  0000000000200000  x1  0000000000000100  x2  0000000000000100  x3  0000000000000000
02-25 13:16:47.192 30757 30757 F DEBUG   :     x4  0000000000000000  x5  0000000000000000  x6  0000000000000096  x7  0000000000000096
02-25 13:16:47.192 30757 30757 F DEBUG   :     x8  0000000020000000  x9  0000000000020000  x10 0000000000000000  x11 0000000000000000
02-25 13:16:47.192 30757 30757 F DEBUG   :     x12 0000000000000000  x13 0000000000000001  x14 0000000000000010  x15 0000000000000008
02-25 13:16:47.192 30757 30757 F DEBUG   :     x16 0000007aebf911a0  x17 0000007aebf19b90  x18 0000007792d34000  x19 0000000000001000
02-25 13:16:47.192 30757 30757 F DEBUG   :     x20 0000000000000100  x21 0100007994f1f8f0  x22 0000000000000004  x23 0000000000000000
02-25 13:16:47.192 30757 30757 F DEBUG   :     x24 0000000000000000  x25 0000000000000000  x26 0000000000000080  x27 0000000000000001
02-25 13:16:47.192 30757 30757 F DEBUG   :     x28 0000000000000100  x29 0000007793b155d0
02-25 13:16:47.192 30757 30757 F DEBUG   :     lr  00000077e2fbed34  sp  0000007793b15580  pc  00000077e2fbed44  pst 0000000080001000
02-25 13:16:47.192 30757 30757 F DEBUG   :     esr 0000000092000047
02-25 13:16:47.192 30757 30757 F DEBUG   : 40 total frames
02-25 13:16:47.192 30757 30757 F DEBUG   : backtrace:
02-25 13:16:47.192 30757 30757 F DEBUG   :       #00 pc 00000000001a2d44  /vendor/lib64/egl/libGLESv2_powervr.so (CalculateNPOTTwiddleSparsePageMap3D+564) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #01 pc 00000000000d4758  /vendor/lib64/egl/libGLESv2_powervr.so (GetTwiddledMiptreeSparsePageMap+1784) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #02 pc 0000000000080d04  /vendor/lib64/egl/libGLESv2_powervr.so (CreateTextureMemory+1604) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #03 pc 00000000000b946c  /vendor/lib64/egl/libGLESv2_powervr.so (TextureMakeResident+284) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #04 pc 00000000000b9270  /vendor/lib64/egl/libGLESv2_powervr.so (MakeTexStorageResident+624) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #05 pc 00000000000cf1d0  /vendor/lib64/egl/libGLESv2_powervr.so (TexStorage3D+960) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #06 pc 00000000000cedb4  /vendor/lib64/egl/libGLESv2_powervr.so (glTexStorage3D+84) (BuildId: 5c09bdbf5bedc8055689e500629872cc)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #07 pc 0000000003422628  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #08 pc 00000000033560bc  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #09 pc 00000000032dd04c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #10 pc 0000000008f16010  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #11 pc 0000000008f0375c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #12 pc 0000000003c808a8  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #13 pc 0000000008fc440c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #14 pc 0000000008fc4150  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #15 pc 0000000008fc99e0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #16 pc 0000000008fcc608  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #17 pc 000000000384e7a0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #18 pc 0000000003c85bd0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #19 pc 0000000003c853d0  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #20 pc 0000000006668868  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #21 pc 0000000006682978  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #22 pc 0000000006682594  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #23 pc 000000000661ef8c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #24 pc 0000000006682f90  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #25 pc 0000000006649c9c  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #26 pc 000000000bf74a80  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #27 pc 00000000065fa400  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #28 pc 00000000065fb264  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #29 pc 00000000065f8e20  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #30 pc 00000000065f9d94  /data/app/~~1kKbzw01xOz6SGcOfBHcEg==/org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==/lib/arm64/libchrome.so (BuildId: e80387ba88bb64b6c4f83760097f3d5247fcfdba)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #31 pc 00000000002c2300  /apex/com.android.art/lib64/libart.so (art_quick_generic_jni_trampoline+144) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #32 pc 00000000015107a0  /data/dalvik-cache/arm64/data@app@~~1kKbzw01xOz6SGcOfBHcEg==@org.chromium.chrome-txCbTxo6OoHX2I2sgIwOrA==@base.apk@classes.dex (nf1.run+2048)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #33 pc 000000000031d5f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #34 pc 00000000002aaf94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #35 pc 00000000002709b0  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-25 13:16:47.192 30757 30757 F DEBUG   :       #36 pc 00000000004bdfc8  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-25 13:16:47.193 30757 30757 F DEBUG   :       #37 pc 00000000004bdb18  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: 61c7a211c01ef3c0068b4fbe31051050)
02-25 13:16:47.193 30757 30757 F DEBUG   :       #38 pc 000000000008a314  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
02-25 13:16:47.193 30757 30757 F DEBUG   :       #39 pc 000000000007b1f4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)


```

Suggest patch

Add a validation check in the ANGLE entry point for glTexStorage3D.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.5 KB)
- [crash.mp4](attachments/crash.mp4) (video/mp4, 1.4 MB)
- [poc.html](attachments/poc_73991256.html) (text/html, 6.5 KB)

## Timeline

### ha...@gmail.com (2026-02-25)

```
004bf6d0    int64_t Get3DMipMapOffsetInBytes(void* arg1, int32_t arg2)

004bf6e8        uint64_t x8_4
004bf6e8        int32_t x10_1
004bf6e8        int128_t v0
004bf6e8        
004bf6e8        if ((zx.d(*(arg1 + 0x240)) & 4) != 0)
004bf794            int32_t x19_1 = *(arg1 + 0x250)
004bf7a4            int16_t var_4_1 = 0
004bf7ac            int32_t var_8 = 0
004bf7ac            
004bf7b4            if ((IMGPixFmtsGetBlockSizeInfo(x19_1, &var_8) & 1) == 0)
004bf80c                PVRSRVDebugPrintf(2, &.str.1.llvm.11755986911736274898, 0x73d, 
004bf80c                    "%s: IMGPixFmtsGetBlockSizeInfo failed", "Get3DMipMapOffsetInBytes")
004bf810                return 0
004bf810            
004bf7d0            v0.d = float.s(zx.d(var_4_1.b))
004bf7dc            x10_1 = 1
004bf7e0            v0:4.d = zx.d(var_4_1:1.b)
004bf7e4            x8_4 = zx.q(*(mulu.dp.d(x19_1, 0x24) + 0x4364ea))
004bf6e8        else
004bf6fc            v0.d = 4
004bf6fc            v0:4.d = 4
004bf704            x10_1 = 4
004bf70c            x8_4 = zx.q(*(mulu.dp.d(*(arg1 + 0x250), 0x24) + 0x4364ea)) << 6
004bf70c        
004bf710        int64_t x9_1 = 0
004bf710        
004bf714        if (arg2 != 0)
004bf724            unimplemented  {ptrue p0.s, vl2}
004bf728            int128_t v2
004bf728            v2.q = *(arg1 + 0x244)
004bf744            int128_t v1_1
004bf744            v1_1.d = 2
004bf744            v1_1:4.d = 2
004bf748            uint32_t x11_4 =
004bf748                (x10_1 + *(arg1 + 0x24c) - 1) u>> _CountLeadingZeros(__rbit(x10_1))
004bf750            unimplemented  {udivr z0.s, p0/m, z0.s, z2.s}
004bf77c            int32_t i
004bf77c            
004bf77c            do
004bf754                int32_t x12_2 = v0:4.d
004bf758                uint64_t x13_1 = zx.q(v0.d)
004bf760                unimplemented  {umax v0.2s, v0.2s, v1.2s}
004bf764                v0.d u>>= 1
004bf764                v0:4.d u>>= 1
004bf768                uint64_t x12_3 = mulu.dp.d(x12_2, x11_4)
004bf76c                uint32_t x11_5
004bf76c                
004bf76c                x11_5 = x11_4 u> 2 ? x11_4 : 2
004bf76c                
004bf770                x11_4 = x11_5 u>> 1
004bf774                i = arg2
004bf774                arg2 -= 1
004bf778                x9_1 += x12_3 * x13_1
004bf77c            while (i != 1)
004bf77c        
004bf780        return x9_1 * x8_4


```

The vulnerability resides in Get3DMipMapOffsetInBytes, which calculates the total storage required for a 3D texture mip-chain. The logic fails to use 64-bit safe-math when multiplying the three dimensions with the texel byte size.Specifically, at 0x004bf780, the total accumulated volume x9\_1 ($W \times H \times D$) is multiplied by the bytes-per-pixel value x8\_4. For a 1024x1024x1024 texture with a 4-byte format, the calculation $2^{30} \times 4$ results in an integer wrap-around to 0.This "zero-size" result is returned to the memory management layer, leading to a massive heap buffer under-allocation. Any subsequent operation attempting to access the texture data results in a heap out-of-bounds write.

### ha...@gmail.com (2026-02-25)

Because of the out-of-bounds write, other values ​​were corrupted, and the value of x0 can be seen.

```
02-25 14:28:38.256 14293 14293 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
02-25 14:28:38.257 14293 14293 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/BP4A.260205.001/14624666:user/release-keys'
02-25 14:28:38.257 14293 14293 F DEBUG   : Kernel Release: '6.6.98-android15-8-g4b48560cd07d-ab14239520-4k'
02-25 14:28:38.257 14293 14293 F DEBUG   : Revision: 'MP1.0'
02-25 14:28:38.257 14293 14293 F DEBUG   : ABI: 'arm64'
02-25 14:28:38.257 14293 14293 F DEBUG   : Timestamp: 2026-02-25 14:28:38.161910650+0800
02-25 14:28:38.257 14293 14293 F DEBUG   : Process uptime: 19s
02-25 14:28:38.257 14293 14293 F DEBUG   : Executable: /system/bin/app_process64
02-25 14:28:38.257 14293 14293 F DEBUG   : Cmdline: org.chromium.chrome:privileged_process0
02-25 14:28:38.257 14293 14293 F DEBUG   : pid: 14064, tid: 14086, name: vkmem_free  >>> org.chromium.chrome:privileged_process0 <<<
02-25 14:28:38.257 14293 14293 F DEBUG   : uid: 10329
02-25 14:28:38.257 14293 14293 F DEBUG   : tagged_addr_ctrl: 0000000000000001 (PR_TAGGED_ADDR_ENABLE)
02-25 14:28:38.257 14293 14293 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
02-25 14:28:38.257 14293 14293 F DEBUG   : esr: 0000000092000004 (Data Abort Exception 0x24)
02-25 14:28:38.257 14293 14293 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0000010108a20101 (read)
02-25 14:28:38.257 14293 14293 F DEBUG   :     x0  b400010108a20101  x1  000000757a0ecf84  x2  00000076489b2750  x3  000000757a0ecf88
02-25 14:28:38.257 14293 14293 F DEBUG   :     x4  0000000000000050  x5  0000000000000050  x6  0000000000000004  x7  0000000000000001
02-25 14:28:38.257 14293 14293 F DEBUG   :     x8  0000000000000000  x9  0000000000000001  x10 0000000000000002  x11 0000000000050005
02-25 14:28:38.257 14293 14293 F DEBUG   :     x12 ffffff80ffffffd0  x13 0000000000003ca8  x14 0000000000000018  x15 0000000000000000
02-25 14:28:38.257 14293 14293 F DEBUG   :     x16 000000755bf17560  x17 000000788094e520  x18 0000007503518000  x19 b400010108a20101
02-25 14:28:38.257 14293 14293 F DEBUG   :     x20 b4000077189ae470  x21 000000000000007e  x22 0000000000000001  x23 0000000000001bd0
02-25 14:28:38.257 14293 14293 F DEBUG   :     x24 0000000000001b78  x25 000000757a0ed090  x26 0000000000000000  x27 0000000000000008
02-25 14:28:38.257 14293 14293 F DEBUG   :     x28 0000007579ff5000  x29 000000757a0ecfc0
02-25 14:28:38.257 14293 14293 F DEBUG   :     lr  000000755beca678  sp  000000757a0ecfc0  pc  000000788094e524  pst 0000000080001000
02-25 14:28:38.257 14293 14293 F DEBUG   :     esr 0000000092000004
02-25 14:28:38.257 14293 14293 F DEBUG   : 9 total frames
02-25 14:28:38.257 14293 14293 F DEBUG   : backtrace:
02-25 14:28:38.257 14293 14293 F DEBUG   :       #00 pc 000000000008c524  /apex/com.android.runtime/lib64/bionic/libc.so (pthread_mutex_destroy+4) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #01 pc 0000000000034674  /vendor/lib64/libsrv_um.so (OSMutexDestroy+20) (BuildId: 630e8f7d21a97710c03a3833dca0ccb5)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #02 pc 000000000003c754  /vendor/lib64/libsrv_um.so (DevmemMemDescRelease+260) (BuildId: 630e8f7d21a97710c03a3833dca0ccb5)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #03 pc 000000000005e29c  /vendor/lib64/libsrv_um.so (RGXRenderTargetFreeRGXResources+124) (BuildId: 630e8f7d21a97710c03a3833dca0ccb5)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #04 pc 000000000005d1a4  /vendor/lib64/libsrv_um.so (RGXRemoveRenderTarget+196) (BuildId: 630e8f7d21a97710c03a3833dca0ccb5)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #05 pc 0000000000076cb4  /vendor/lib64/hw/vulkan.powervr.so (RenderTargetDestroy(_DEVICE const*, _RENDER_TARGET*) (.__uniq.307328593831598131656896110154879408869.llvm.17948168011611327450)+84) (BuildId: f9a2f7010ecca73dc53632e214b31300)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #06 pc 0000000000076e00  /vendor/lib64/hw/vulkan.powervr.so (FbFreeWorkerThread+96) (BuildId: f9a2f7010ecca73dc53632e214b31300)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #07 pc 000000000008a314  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)
02-25 14:28:38.257 14293 14293 F DEBUG   :       #08 pc 000000000007b1f4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37)

```

### aj...@google.com (2026-02-25)

Hello do you have a crash report id available?

### aj...@google.com (2026-02-25)

No crash for me on pixel 8a.

### ha...@gmail.com (2026-02-26)

Hello,this is the crash report, and you need to test it on a Pixel 10 or other phones with PowerVR GPUs.

### pe...@google.com (2026-02-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2026-02-26)

If you can crash chrome's gpu process you should be able to upload a crashdump and provide the crash report id - that will make it a lot easier for us to triage this! Otherwise all we have from you is an unsymbolized stacktrace.

### ha...@gmail.com (2026-02-26)

```
Symbolizing stack using ABI=arm64
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x75aa4715d0 in tid 8212 (CrGpuMain), pid 8196 (ileged_process0)
Build fingerprint: 'google/frankel/frankel:16/BP4A.260205.001/14624666:user/release-keys'
Revision: 'MP1.0'
pid: 8196, tid: 8212, name: CrGpuMain  >>> org.chromium.chrome:privileged_process0 <<<
signal 11 (SIGSEGV), code 9 (SEGV_MTESERR), fault addr 0x00000075aa4715d0 (write)

Stack Trace:
  RELADDR   FUNCTION                                                                          FILE:LINE
  00000000001a2d44  CalculateNPOTTwiddleSparsePageMap3D+564) (BuildId: 5c09bdbf5bedc8055689e500629872cc  /vendor/lib64/egl/libGLESv2_powervr.so
  00000000000d4758  GetTwiddledMiptreeSparsePageMap+1784) (BuildId: 5c09bdbf5bedc8055689e500629872cc  /vendor/lib64/egl/libGLESv2_powervr.so
  0000000000080d04  CreateTextureMemory+1604) (BuildId: 5c09bdbf5bedc8055689e500629872cc              /vendor/lib64/egl/libGLESv2_powervr.so
  00000000000b946c  TextureMakeResident+284) (BuildId: 5c09bdbf5bedc8055689e500629872cc               /vendor/lib64/egl/libGLESv2_powervr.so
  00000000000b9270  MakeTexStorageResident+624) (BuildId: 5c09bdbf5bedc8055689e500629872cc            /vendor/lib64/egl/libGLESv2_powervr.so
  00000000000cf1d0  TexStorage3D+960) (BuildId: 5c09bdbf5bedc8055689e500629872cc                      /vendor/lib64/egl/libGLESv2_powervr.so
  00000000000cedb4  glTexStorage3D+84) (BuildId: 5c09bdbf5bedc8055689e500629872cc                     /vendor/lib64/egl/libGLESv2_powervr.so
  00000000034490a8  rx::TextureGL::setStorage(gl::Context const*, gl::TextureType, unsigned long, unsigned int, angle::Extents<int> const&)  ../../third_party/angle/src/libANGLE/renderer/gl/TextureGL.cpp:1286:26
  000000000337c950  gl::Texture::setStorage(gl::Context*, gl::TextureType, int, unsigned int, angle::Extents<int> const&)  ../../third_party/angle/src/libANGLE/Texture.cpp:1777:25
  0000000003303608  gl::Context::texStorage3D(gl::TextureType, int, unsigned int, int, int, int)      ../../third_party/angle/src/libANGLE/Context.cpp:6754:32
  0000000008f5d050  gpu::gles2::GLES2DecoderPassthroughImpl::DoTexStorage3D(unsigned int, int, unsigned int, int, int, int)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough_doers.cc:3020:10
  0000000008f4a988  gpu::error::Error gpu::gles2::GLES2DecoderPassthroughImpl::DoCommandsImpl<false>(unsigned int, void const volatile*, int, int*)  ../../gpu/command_buffer/service/gles2_cmd_decoder_passthrough.cc:742:20
  0000000003caaeac  gpu::CommandBufferService::Flush(int, gpu::AsyncAPIInterface*)                    ../../gpu/command_buffer/service/command_buffer_service.cc:267:35
  v------>  std::__Cr::unique_ptr<gpu::CommandBufferService, std::__Cr::default_delete<gpu::CommandBufferService>>::operator->() const  gen/third_party/libc++/src/include/__memory/unique_ptr.h:265:101
  000000000900be5c  gpu::CommandBufferStub::OnAsyncFlush(int, unsigned int, std::__Cr::vector<gpu::SyncToken, std::__Cr::allocator<gpu::SyncToken>> const&)  ../../gpu/ipc/service/command_buffer_stub.cc:504:5
  v------>  std::__Cr::unique_ptr<gpu::mojom::AsyncFlushParams, std::__Cr::default_delete<gpu::mojom::AsyncFlushParams>>::operator*() const  gen/third_party/libc++/src/include/__memory/unique_ptr.h:263:13
  v------>  mojo::StructPtr<gpu::mojom::AsyncFlushParams>::operator*() const                  ../../mojo/public/cpp/bindings/struct_ptr.h:82:12
  000000000900bba0  gpu::CommandBufferStub::ExecuteDeferredRequest(gpu::mojom::DeferredCommandBufferRequestParams&, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/command_buffer_stub.cc:172:21
  v------>  std::__Cr::unique_ptr<gpu::mojom::DeferredCommandBufferRequestParams, std::__Cr::default_delete<gpu::mojom::DeferredCommandBufferRequestParams>>::operator*() const  gen/third_party/libc++/src/include/__memory/unique_ptr.h:263:13
  v------>  mojo::StructPtr<gpu::mojom::DeferredCommandBufferRequestParams>::operator*() const  ../../mojo/public/cpp/bindings/struct_ptr.h:82:12
  0000000009011570  gpu::GpuChannel::ExecuteDeferredRequest(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*)  ../../gpu/ipc/service/gpu_channel.cc:833:36
  v------>  void base::internal::DecayedFunctorTraits<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>::Invoke<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel> const&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:740:12
  v------>  void base::internal::InvokeHelper<true, base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, void, 0ul, 1ul>::MakeItSo<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, gpu::FenceSyncReleaseDelegate*>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:956:5
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunImpl<void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, 0ul, 1ul>(void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), std::__Cr::tuple<base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>&&, std::__Cr::integer_sequence<unsigned long, 0ul, 1ul>, gpu::FenceSyncReleaseDelegate*&&)  ../../base/functional/bind_internal.h:1069:14
  0000000009014030  base::internal::Invoker<base::internal::FunctorTraits<void (gpu::GpuChannel::*&&)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>&&, mojo::StructPtr<gpu::mojom::DeferredRequestParams>&&>, base::internal::BindState<true, true, false, void (gpu::GpuChannel::*)(mojo::StructPtr<gpu::mojom::DeferredRequestParams>, gpu::FenceSyncReleaseDelegate*), base::WeakPtr<gpu::GpuChannel>, mojo::StructPtr<gpu::mojom::DeferredRequestParams>>, void (gpu::FenceSyncReleaseDelegate*)>::RunOnce(base::internal::BindStateBase*, gpu::FenceSyncReleaseDelegate*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void (media::DemuxerStream*)>::Run(media::DemuxerStream*) &&   ../../base/functional/callback.h:155:12
  v------>  void base::internal::DecayedFunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*&&>::Invoke<base::OnceCallback<void (media::DemuxerStream*)>, media::DemuxerStream*>(base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&)  ../../base/functional/bind_internal.h:815:49
  v------>  void base::internal::InvokeHelper<false, base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, void, 0ul>::MakeItSo<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&)  ../../base/functional/bind_internal.h:932:12
  v------>  void base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (media::DemuxerStream*)>&&, media::DemuxerStream*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (media::DemuxerStream*)>, base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunImpl<base::OnceCallback<void (media::DemuxerStream*)>, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, 0ul>(base::OnceCallback<void (media::DemuxerStream*)>&&, std::__Cr::tuple<base::internal::UnretainedWrapper<media::DemuxerStream, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>&&, std::__Cr::integer_sequence<unsigned long, 0ul>)  ../../base/functional/bind_internal.h:1069:14
  0000000003880e88  base::internal::Invoker<base::internal::FunctorTraits<base::OnceCallback<void (void const*)>&&, collaboration::CollaborationController*&&>, base::internal::BindState<false, true, true, base::OnceCallback<void (void const*)>, base::internal::UnretainedWrapper<collaboration::CollaborationController, base::unretained_traits::MayNotDangle, (partition_alloc::internal::RawPtrTraits)0>>, void ()>::RunOnce(base::internal::BindStateBase*)  ../../base/functional/bind_internal.h:982:12
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  0000000003cb01bc  gpu::Scheduler::ExecuteSequence(base::IdType<gpu::SyncPointOrderData, unsigned int, 0u, 1u>)  ../../gpu/command_buffer/service/scheduler.cc:707:29
  0000000003caf9bc  gpu::Scheduler::RunNextTask()                                                     ../../gpu/command_buffer/service/scheduler.cc:625:3
  v------>  base::OnceCallback<void ()>::Run() &&                                             ../../base/functional/callback.h:155:12
  00000000066be220  base::TaskAnnotator::RunTaskImpl(base::PendingTask&)                              ../../base/task/common/task_annotator.cc:229:34
  v------>  void base::TaskAnnotator::RunTask<base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3>(perfetto::StaticString, base::PendingTask&, base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)::$_3&&)  ../../base/task/common/task_annotator.h:112:5
  00000000066d850c  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:475:23
  00000000066d8128  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()   ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:346:40
  0000000006674a64  base::MessagePumpDefault::Run(base::MessagePump::Delegate*)                       ../../base/message_loop/message_pump_default.cc:42:55
  00000000066d8b24  base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta)  ../../base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:650:12
  000000000669f6b8  base::RunLoop::Run(base::Location const&)                                         ../../base/run_loop.cc:135:14
  v------>  unsigned char std::__Cr::__cxx_atomic_load<unsigned char>(std::__Cr::__cxx_atomic_base_impl<unsigned char> const*, std::__Cr::memory_order)  gen/third_party/libc++/src/include/__atomic/support/c11.h:81:10
  v------>  std::__Cr::__atomic_base<unsigned char, false>::load(std::__Cr::memory_order) const  gen/third_party/libc++/src/include/__atomic/atomic.h:71:12
  v------>  void perfetto::DataSource<perfetto::internal::TrackEventDataSource, perfetto::internal::TrackEventDataSourceTraits>::CallIfEnabled<perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CategoryTracePointTraits, void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)>(unsigned long, content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int))::'lambda'(unsigned int)>(void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)>(unsigned long, content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int))::'lambda'(unsigned int), content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)::TracePointData)  ../../third_party/perfetto/include/perfetto/tracing/data_source.h:429:32
  v------>  void perfetto::internal::TrackEvent<&base::perfetto_track_event::internal::kCategoryRegistry>::CallIfCategoryEnabled<content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int)>(unsigned long, content::GpuMain(content::MainFunctionParams)::$_2::operator()() const::'lambda0'(unsigned int))  ../../third_party/perfetto/include/perfetto/tracing/internal/track_event_data_source.h:460:5
  v------>  content::GpuMain(content::MainFunctionParams)::$_2::operator()() const            ../../content/gpu/gpu_main.cc:478:5
  000000000bff93f0  content::GpuMain(content::MainFunctionParams)                                     ../../content/gpu/gpu_main.cc:478:5
  000000000664fe24  content::RunOtherNamedProcessTypeMain(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char>> const&, content::MainFunctionParams, content::ContentMainDelegate*)  ../../content/app/content_main_runner_impl.cc:762:14
  0000000006650cc4  content::ContentMainRunnerImpl::Run()                                             ../../content/app/content_main_runner_impl.cc:1152:10
  000000000664e838  content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*)  ../../content/app/content_main.cc:358:36
  000000000664f7ac  content::StartContentMain(bool)                                                   ../../content/app/android/content_main_android.cc:54:10
  00000000002c2300  art_quick_generic_jni_trampoline+144) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea  /apex/com.android.art/lib64/libart.so
  00000000006683e8  nterp_helper+152) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea                      /apex/com.android.art/lib64/libart.so
  0000000000289a3e  offset 0x1edb000) (lg1.run+570                                                    /data/app/~~KWO0JD6yPlW7SmjbtNZrAg==/org.chromium.chrome-2Z0tgytiLSC8EPEj3neBRw==/base.apk/libmonochrome.so
  000000000031d5f0  java.lang.Thread.run+64                                                           /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat
  00000000002aaf94  art_quick_invoke_stub+612) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea             /apex/com.android.art/lib64/libart.so
  00000000002708ec  art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea  /apex/com.android.art/lib64/libart.so
  00000000004bdfe0  art::Thread::CreateCallback(void*)+1184) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea  /apex/com.android.art/lib64/libart.so
  00000000004bdb30  art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea  /apex/com.android.art/lib64/libart.so
  000000000008a314  __pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37  /apex/com.android.runtime/lib64/bionic/libc.so
  000000000007b1f4  __start_thread+68) (BuildId: 5e0a77ba8573ea8c77efcf596e9edd37                     /apex/com.android.runtime/lib64/bionic/libc.so


```

### pe...@google.com (2026-02-26)

Thank you for providing more feedback. Adding the requester to the CC list.

### aj...@google.com (2026-02-27)

[security triage] -> geofflang to pick someone to take a look. Setting Critical Sev as this is a web reachable crash in the android gpu process.

### ch...@google.com (2026-02-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-28)

Setting Priority to P0 to match Severity s0. To ensure SLOs are tracked correctly, priority must exceed severity.

### ha...@gmail.com (2026-03-01)

My tests showed that on a Moto G54 phone, the entire operating system could crash. Accessing the system directly through Chrome caused the operating system kernel to crash.

### ha...@gmail.com (2026-03-01)

This vulnerability should allow direct access from normal users to RCE to root, because without root access, I cannot see which address of the GPU page was overwritten.

### kb...@chromium.org (2026-03-03)

Filed internal [bug 489200502](https://issues.chromium.org/issues/489200502) about fixing this in Imagination's driver.

Extra validation in ANGLE which is triggered on problematic drivers could probably be added as a mitigation.

### ha...@gmail.com (2026-03-05)

Currently, the only setting is to control the fault addr to 0x0001010101010101; I don't know how to control the others.

```
03-05 16:10:34.776 31442 31442 F DEBUG   : *** *** *** *** *** *** *** *** *** *** *** *** *** *** *** ***
03-05 16:10:34.776 31442 31442 F DEBUG   : Build fingerprint: 'google/frankel/frankel:16/CP1A.260305.018/14887507:user/release-keys'
03-05 16:10:34.776 31442 31442 F DEBUG   : Kernel Release: '6.6.102-android15-8-g6eb5b2a8c46b-ab14739656-4k'
03-05 16:10:34.776 31442 31442 F DEBUG   : Revision: 'MP1.0'
03-05 16:10:34.776 31442 31442 F DEBUG   : ABI: 'arm64'
03-05 16:10:34.776 31442 31442 F DEBUG   : Timestamp: 2026-03-05 16:10:34.504335601+0800
03-05 16:10:34.776 31442 31442 F DEBUG   : Process uptime: 6s
03-05 16:10:34.776 31442 31442 F DEBUG   : Executable: /system/bin/app_process64
03-05 16:10:34.776 31442 31442 F DEBUG   : Cmdline: com.android.chrome:privileged_process0
03-05 16:10:34.776 31442 31442 F DEBUG   : pid: 31327, tid: 31354, name: CrGpuMain  >>> com.android.chrome:privileged_process0 <<<
03-05 16:10:34.776 31442 31442 F DEBUG   : uid: 10230
03-05 16:10:34.776 31442 31442 F DEBUG   : tagged_addr_ctrl: 000000000007fff1 (PR_TAGGED_ADDR_ENABLE, mask 0xfffe)
03-05 16:10:34.776 31442 31442 F DEBUG   : pac_enabled_keys: 000000000000000f (PR_PAC_APIAKEY, PR_PAC_APIBKEY, PR_PAC_APDAKEY, PR_PAC_APDBKEY)
03-05 16:10:34.776 31442 31442 F DEBUG   : esr: 0000000092000004 (Data Abort Exception 0x24)
03-05 16:10:34.776 31442 31442 F DEBUG   : signal 11 (SIGSEGV), code 1 (SEGV_MAPERR), fault addr 0x0001010101010101 (read)
03-05 16:10:34.776 31442 31442 F DEBUG   :     x0  0101010101010101  x1  0c000071f4d815b0  x2  0000000000000000  x3  000000de52217f4a
03-05 16:10:34.776 31442 31442 F DEBUG   :     x4  0000000000000009  x5  00000000004ca8c8  x6  0000000000000000  x7  00000080014e4000
03-05 16:10:34.776 31442 31442 F DEBUG   :     x8  0600007244e9fb30  x9  0d00007134d6b6d0  x10 0000000000000000  x11 0000006fc8d90880
03-05 16:10:34.776 31442 31442 F DEBUG   :     x12 0000000000000001  x13 0200006a0002cd80  x14 0000006f3455fa90  x15 0400006a000e1be4
03-05 16:10:34.776 31442 31442 F DEBUG   :     x16 000000701e3f4548  x17 00000073243590a0  x18 0000006fc7b28000  x19 0c000071f4d815b0
03-05 16:10:34.776 31442 31442 F DEBUG   :     x20 0000000000000009  x21 0000000000000000  x22 0600007244d75390  x23 0000000000000009
03-05 16:10:34.776 31442 31442 F DEBUG   :     x24 00000000000017f0  x25 0000000000000000  x26 0000006a0018b000  x27 0000006fc8d92240
03-05 16:10:34.776 31442 31442 F DEBUG   :     x28 0000000000000001  x29 0000006fc8d907b0
03-05 16:10:34.776 31442 31442 F DEBUG   :     lr  000000701e3aac34  sp  0000006fc8d907a0  pc  00000073243590a4  pst 0000000060001000
03-05 16:10:34.776 31442 31442 F DEBUG   :     esr 0000000092000004  vg  0000000000000002
03-05 16:10:34.776 31442 31442 F DEBUG   : 28 total frames
03-05 16:10:34.776 31442 31442 F DEBUG   : backtrace:
03-05 16:10:34.776 31442 31442 F DEBUG   :       #00 pc 000000000008c0a4  /apex/com.android.runtime/lib64/bionic/libc.so (pthread_mutex_lock+4) (BuildId: 8d65ea529c21c79c019713e50adb6675)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #01 pc 000000000003bc30  /vendor/lib64/libsrv_um.so (DevmemXUnmapVirtualRange+160) (BuildId: 7806edaa6a56e5e90e5131189ef8cb1e)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #02 pc 000000000016f35c  /vendor/lib64/hw/vulkan.powervr.so (IMG_vkDestroyBuffer+380) (BuildId: af33e0bbb85a052bfb98677c54834b2a)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #03 pc 0000000008293794  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #04 pc 0000000007684c64  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #05 pc 0000000007d3fdf0  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #06 pc 0000000007d40254  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #07 pc 00000000077685a8  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #08 pc 00000000058fc4bc  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #09 pc 0000000007596714  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #10 pc 0000000005a5b2ac  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #11 pc 00000000058e9f8c  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #12 pc 00000000058e9af4  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #13 pc 0000000007109794  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #14 pc 000000000588b024  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #15 pc 00000000059c2f6c  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #16 pc 00000000059a4cec  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #17 pc 00000000059a49fc  /data/app/~~fduaAbEHBWjj_O51z6-vew==/com.google.android.trichromelibrary_763212233-sSDXzfwWTdZmdXhezaZevg==/base.apk!libmonochrome_64.so (offset 0x930000) (BuildId: 10a0e7b86b2f415859e3d293b382d7c52ad28840)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #18 pc 0000000000d54ed0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (art_jni_trampoline+112)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #19 pc 00000000006683e8  /apex/com.android.art/lib64/libart.so (nterp_helper+152) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #20 pc 00000000000da42a  /data/app/~~yaDL9kQKvSfXAEnwvCssqw==/com.android.chrome-s_nSQQFkD0avdt1DDTtaUg==/base.apk (offset 0x1cd000) (jm3.run+562)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #21 pc 00000000003215f0  /data/misc/apexdata/com.android.art/dalvik-cache/arm64/boot.oat (java.lang.Thread.run+64)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #22 pc 00000000002aaf94  /apex/com.android.art/lib64/libart.so (art_quick_invoke_stub+612) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #23 pc 00000000002708ec  /apex/com.android.art/lib64/libart.so (art::ArtMethod::Invoke(art::Thread*, unsigned int*, unsigned int, art::JValue*, char const*)+220) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #24 pc 00000000004bdfe0  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallback(void*)+1184) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #25 pc 00000000004bdb30  /apex/com.android.art/lib64/libart.so (art::Thread::CreateCallbackWithUffdGc(void*)+8) (BuildId: a1fcb66a9fb3fa9071e8a42dcf9cd5ea)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #26 pc 000000000008a914  /apex/com.android.runtime/lib64/bionic/libc.so (__pthread_start(void*) (.__uniq.67847048707805468364044055584648682506)+180) (BuildId: 8d65ea529c21c79c019713e50adb6675)
03-05 16:10:34.776 31442 31442 F DEBUG   :       #27 pc 000000000007b5a4  /apex/com.android.runtime/lib64/bionic/libc.so (__start_thread+68) (BuildId: 8d65ea529c21c79c019713e50adb6675)

```

### ge...@google.com (2026-03-06)

This bug has been reproduced by the Pixel team and the vendor, the vendor is working on a fix and I will work around it at the ANGLE/Chrome level once I can see it.

### ge...@google.com (2026-03-12)

This has now been fixed upstream and should go out with the next update. Internal fix link: ag/38891116

### ch...@google.com (2026-03-28)

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M147. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### dr...@chromium.org (2026-04-01)

Given we're relying on upstream rollouts, removing merge requests.

### sp...@google.com (2026-04-02)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $32000.00 for this report.

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

### ch...@google.com (2026-07-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487444459)*
