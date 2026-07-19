# OOB write in PDFium TIFF decoder via lossless JPEG data precision mismatch

| Field | Value |
|-------|-------|
| **Issue ID** | [496907110](https://issues.chromium.org/issues/496907110) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | PDFium |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | th...@chromium.org |
| **Created** | 2026-03-27 |
| **Bounty** | $50,000.00 |

## Description

## Summary

A heap buffer overflow write exists in PDFium's TIFF image decoder when processing a TIFF file that uses JPEG compression with a lossless JPEG codestream (SOF3) whose data precision is less than 8 bits. The bundled libtiff calculates the strip buffer size based on the TIFF BitsPerSample tag (e.g. 2 bits per sample), while the bundled libjpeg-turbo, which has lossless JPEG support enabled in Chromium, outputs decoded samples at 8 bits each. This mismatch causes libjpeg-turbo to write 4x more data than the allocated buffer can hold, producing an attacker-controlled heap overflow in the renderer process. The bug affects all platforms and is reachable through XFA PDF forms when the PdfXfaSupport feature is enabled. No user interaction beyond opening a PDF is required.

## Bisect

Introducing Commit: `4aa3b725c` (PDFium)

- Date: 2025-10-23
- Author: Lei Zhang
- Review: Upgrade libtiff from 4.7.0 to 4.7.1

## Root Cause

PDFium's bundled libtiff validates JPEG data precision in `JPEGPreDecode` by comparing only the JPEG header's `data_precision` against the TIFF tag `td_bitspersample`:

```
// third_party/pdfium/third_party/libtiff/tif_jpeg.c
if (sp->cinfo.d.data_precision != td->td_bitspersample)
{
    TIFFErrorExtR(tif, module, "Improper JPEG data precision");
    return (0);
}

```

This check passes when both values are 2, but it does not verify that the precision equals `BITS_IN_JSAMPLE` (8), which is the output sample width of libjpeg-turbo. The upstream libtiff fix `0f726d9` adds exactly this check, but the PDFium copy has not incorporated it.

Separately, Chromium's bundled libjpeg-turbo 3.1.0 defines `D_LOSSLESS_SUPPORTED` in `jmorecfg.h`, enabling the lossless JPEG decoding path. This path accepts `data_precision` values from 2 through 16 in `jdinput.c`:

```
// third_party/libjpeg_turbo/src/jdinput.c
#ifdef D_LOSSLESS_SUPPORTED
  if (cinfo->master->lossless) {
    if (cinfo->data_precision < 2 || cinfo->data_precision > 16)
      ERREXIT1(cinfo, JERR_BAD_PRECISION, cinfo->data_precision);
  } else

```

The post-processing controller in `jdpostct.c` also accepts precision 2 through 8 when `BITS_IN_JSAMPLE == 8`:

```
// third_party/libjpeg_turbo/src/jdpostct.c
#if BITS_IN_JSAMPLE == 8
    if (cinfo->data_precision > BITS_IN_JSAMPLE || cinfo->data_precision < 2)
#endif
      ERREXIT1(cinfo, JERR_BAD_PRECISION, cinfo->data_precision);

```

A precision of 2 passes all of these checks. The lossless decoder then writes one `JSAMPLE` (8-bit `unsigned char`) per output sample through `null_convert` in `jdcolor.c`. Meanwhile, libtiff computes the strip buffer size via `TIFFScanlineSize(tif)`, which packs samples at 2 bits each. For a 64-pixel wide, single-component image, the scanline buffer is `ceil(64 * 2 / 8) = 16` bytes, but libjpeg-turbo writes `64 * 1 = 64` bytes per row. When `JPEGDecode` advances the buffer pointer by `sp->bytesperline` (16 bytes) after the first row and calls `jpeg_read_scanlines` again, the second row's 64-byte write extends 48 bytes past the end of the 64-byte strip buffer.

## Exploitability

The overflow size is directly controlled by the attacker through the TIFF image dimensions and the JPEG data precision value. For a width of W pixels and a precision of P bits, each scanline overflows by `W - ceil(W * P / 8)` bytes. Lowering the precision increases the ratio; at precision 2, the overflow is 75% of the image width per row, and additional rows multiply the total. The written bytes are the decoded lossless JPEG sample values, which the attacker encodes into the Huffman stream and therefore fully controls. Combined with the ability to choose arbitrary image dimensions to target specific heap bucket sizes, this gives an attacker a controlled, variable-length heap write primitive in the renderer process.

## Reproduce

Tested on Chromium commit `46afa4acada327a9d297f780fc811554a9eecf99` on macOS arm64 and Ubuntu 22.04. The bug is platform-independent. No source modifications are required.

Check out the commit and configure an ASAN build:

```
is_asan = true
is_debug = false
dcheck_always_on = false

```

Then build:

```
autoninja -C out/asan chrome

```

Generate the malicious PDF using the attached Python script, or use the `poc.pdf` directly, then open it in Chrome with XFA support enabled:

```
python3 gen_poc.py

out/asan/Chromium.app/Contents/MacOS/Chromium --user-data-dir=./userdata --enable-features=PdfXfaSupport poc.pdf

```

The renderer process will abort with `ERROR: AddressSanitizer: heap-buffer-overflow`, WRITE of size 1, in `null_convert` (jdcolor.c). The full ASAN trace is in `asan.txt`.

### ASAN output

```
=================================================================
==34815==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x6070001174a0 at pc 0x00035de48638 bp 0x00016b0ec230 sp 0x00016b0ec228
WRITE of size 1 at 0x6070001174a0 thread T0
==34815==WARNING: invalid path to external symbolizer!
==34815==WARNING: Failed to use and restart external symbolizer!
    #0 0x00035de48634 in null_convert+0xfd8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7759.0/Chromium Framework:arm64+0x13d78634)
    #1 0x00035ddbd638 in sep_upsample+0x300 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7759.0/Chromium Framework:arm64+0x13ced638)
    #2 0x00035de5aa7c in process_data_simple_main+0x138 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7759.0/Chromium Framework:arm64+0x13d8aa7c)
    #3 0x00035ddb8d20 in chromium_jpeg_read_scanlines+0x324 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7759.0/Chromium Framework:arm64+0x13ce8d20)
    #4 0x00035b3375f0 in TIFFjpeg_read_scanlines+0x34 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7759.0/Chromium Framework:arm64+0x112675f0)
    #5 0x00035b332fac in JPEGDecode+0x1f8 (/Users/test/Desktop/src/chromium/src/out/asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7759.0/Chromium Framework:arm64+0x11262fac)
......

```

The complete untruncated log is in the attached `asan.txt`.

## References

- [tif\_jpeg.c JPEGPreDecode precision check](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/third_party/libtiff/tif_jpeg.c;l=1290)
- [jmorecfg.h D\_LOSSLESS\_SUPPORTED](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libjpeg_turbo/src/jmorecfg.h;l=262)
- [jdinput.c lossless precision acceptance](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libjpeg_turbo/src/jdinput.c;l=62)
- [jdpostct.c post-controller precision check](https://source.chromium.org/chromium/chromium/src/+/main:third_party/libjpeg_turbo/src/jdpostct.c;l=270)
- [tiff\_decoder.cpp CTiffContext::Decode](https://source.chromium.org/chromium/chromium/src/+/main:third_party/pdfium/core/fxcodec/tiff/tiff_decoder.cpp;l=269)
- [Upstream libtiff fix 0f726d9](https://gitlab.com/libtiff/libtiff/-/commit/0f726d9)

## Credit

Please use 86ac1f1587b71893ed2ad792cd7dde32 as the credit for this vulnerability. Thank you.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 27.7 KB)
- [gen_poc.py](attachments/gen_poc.py) (text/x-python, 8.1 KB)
- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.2 KB)
- [asan.txt](attachments/asan_74863468.txt) (text/plain, 28.0 KB)
- [exploit.pdf](attachments/exploit.pdf) (application/pdf, 5.1 KB)
- [gen_exploit_pdf.py](attachments/gen_exploit_pdf.py) (text/x-python, 8.7 KB)
- [exploit_writeup.md](attachments/exploit_writeup.md) (text/markdown, 8.2 KB)
- [exp_gdb.png](attachments/exp_gdb.png) (image/png, 1.5 MB)
- [exp.png](attachments/exp.png) (image/png, 181.1 KB)

## Timeline

### hc...@google.com (2026-03-27)

Reproed on linux, 148.0.7743.0 (Developer Build) (64-bit)

asan attached.

### th...@chromium.org (2026-03-27)

Note that the TIFF decoder requires XFA support, which is not enabled by default.

### dx...@google.com (2026-03-27)

Project: pdfium  

Branch:  main  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/145550>

Patch an overflow in libtiff

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://gitlab.com/libtiff/libtiff/-/commit/0f726d9 
     
    Bug: 496907110 
    Change-Id: Ic8665879ebdd4445f473e9a1e156cfc42c294d51 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145550 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org>

```

---

Files:

- A `third_party/libtiff/0034-tiff-jpeg-overflow.patch`
- M `third_party/libtiff/README.pdfium`
- M `third_party/libtiff/tif_jpeg.c`

---

Hash: ca8a943c247c208fd7a9cd21b4de049f22b93070  

Date: Fri Mar 27 21:52:16 2026


---

### dx...@google.com (2026-03-28)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/7709460>

Roll PDFium from b067c3092ba7 to ca8a943c247c (2 revisions)

---


Expand for full commit details
```
     
    https://pdfium.googlesource.com/pdfium.git/+log/b067c3092ba7..ca8a943c247c 
     
    2026-03-27 thestig@chromium.org Patch an overflow in libtiff 
    2026-03-27 aryankrishnan4b@gmail.com Replace render caps with individual boolean functions 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/pdfium-autoroll 
    Please CC akall@google.com,dhoss@chromium.org,thestig@chromium.org on the revert to ensure that a human 
    is aware of the problem. 
     
    To file a bug in PDFium: https://bugs.chromium.org/p/pdfium/issues/entry 
    To file a bug in Chromium: https://bugs.chromium.org/p/chromium/issues/entry 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:496907110 
    Tbr: akall@google.com 
    Change-Id: I8c6d08da4ef5e5443d9028fa33573a0f0d579d3b 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7709460 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1606628}

```

---

Files:

- M `DEPS`
- M `third_party/pdfium`

---

Hash: [054cc4bd35521e8598346d241c05bb3afab816c8](https://chromiumdash.appspot.com/commit/054cc4bd35521e8598346d241c05bb3afab816c8)  

Date: Sat Mar 28 05:33:28 2026


---

### ch...@google.com (2026-03-28)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-28)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### se...@gmail.com (2026-04-02)

**For Chrome VRP, this is the exploit that hijacks RIP for this vulnerability:**

# Exploit

This exploit demonstrates a heap buffer overflow in PDFium's TIFF decoder within the renderer process that achieves fully controlled instruction pointer hijack from a crafted PDF file, without modifying any Chromium or PDFium source code. The exploit constructs a deterministic heap layout through a two-image XFA PDF that manipulates PartitionAlloc's LIFO freelist ordering within PDFium's isolated partition, positions the TIFF strip buffer at a lower address than the TIFF `struct tiff` in the same bucket-1536 SlotSpan, and uses the lossless JPEG precision mismatch overflow to write attacker-controlled bytes into the TIFF struct's `tif_postdecode` function pointer. The controlled write is demonstrated by the crash showing `Received signal 11 SEGV_MAPERR 414141414141` on stderr, and the GDB register dump confirming `rip = 0x414141414141` (the attacker's chosen call target).

## Vulnerability

PDFium's bundled libtiff calculates the strip buffer size based on the TIFF `BitsPerSample` tag (e.g. 2 bits per sample), while the bundled libjpeg-turbo outputs decoded samples at 8 bits each (one `JSAMPLE` per sample). For `BitsPerSample=2`, libjpeg-turbo writes 4x more data than the allocated buffer can hold. The overflow content is fully attacker-controlled through the Huffman-coded entropy stream in the lossless JPEG codestream.

Despite the declared precision of 2, the output bytes are not limited to the range [0, 3]. The lossless decoder computes `(prediction + difference) & 0xFFFF` and casts directly to `unsigned char` without precision-based masking, giving the attacker full byte-level control (0x00–0xFF) over every overflow byte.

## Target Object

The `struct tiff` (sizeof=1368) is defined in `third_party/pdfium/third_party/libtiff/tiffiop.h` and contains codec method function pointers. The exploit targets `tif_postdecode` at offset `0x4c8`, which is called immediately after each strip decode completes:

```
// third_party/pdfium/third_party/libtiff/tif_read.c
if ((*tif->tif_decodestrip)(tif, *buf, this_stripsize, plane) <= 0)
    return ((tmsize_t)(-1));
(*tif->tif_postdecode)(tif, *buf, this_stripsize);  // ← hijack target

```

The compiler emits `call *0x4c8(%rbx)` for this dispatch. `tif_decodestrip` (offset `0x3e8`) is already mid-execution when the overflow occurs, so corrupting it is harmless. No other `tif` struct field is read between `tif_decodestrip`'s return and the `tif_postdecode` call.

## Allocator Geometry

PDFium creates its own isolated PartitionAlloc partition via `GetGeneralPartitionAllocator()` in `fx_memory_pa.cpp`. The exploit operates entirely within this partition.

Both the TIFF struct and the strip buffer land in PartitionAlloc bucket 1536. The TIFF struct allocation is 1379 bytes (`sizeof(TIFF) + strlen(name) + 1`); the strip buffer allocation is 1516 bytes (1500 data + 16-byte `_TIFFmallocExt` cumulated-tracking header). Bucket boundaries at this size range are 1024, 1280, 1536, 1792; both 1379 and 1516 round up to bucket 1536.

A critical asymmetry in `_TIFFmallocExt` determines the relative addressing: when called with `tif=NULL` (TIFF struct allocation in `TIFFClientOpen`), it returns the raw `_TIFFmalloc(s)` pointer with no header; when called with `tif≠NULL` (strip buffer), it prepends a 16-byte size-tracking header and returns `ptr + 16`. Therefore `tif − buf = 1536 − 16 = 1520` (0x5F0).

## LIFO Freelist Manipulation

The exploit uses a two-image XFA PDF to reorder the LIFO freelist so that the strip buffer ends up at a lower address than the TIFF struct.

**Image A** (setup) is a small JPEG-compressed TIFF whose compressed JPEG data is padded with a COM marker to 1400 bytes, placing the rawdata buffer in bucket 1536 alongside the TIFF struct, JPEGState, and strip buffer — four objects in one SlotSpan. These four objects are allocated sequentially (TIFF struct, JPEGState, rawdata, strip buffer) but freed in a different order: strip buffer first (by `gtStripContig`), then JPEGState (by `TIFFFreeDirectory` → `(*tif->tif_cleanup)(tif)` → `JPEGCleanup`), then rawdata (by `TIFFCleanup` → `_TIFFfreeExt(tif, tif->tif_rawdata)`), then TIFF struct last (by `TIFFCleanup` → `_TIFFfreeExt(NULL, tif)`). This asymmetry between allocation and free order shuffles the LIFO freelist.

**Image B** (exploit) is a 3000×2 pixel TIFF with `BitsPerSample=2` and JPEG data sized to fall outside bucket 1536. Image B allocates only three objects in bucket 1536 (TIFF struct, JPEGState, strip buffer), drawing from the shuffled freelist left by Image A.

The crash confirms the result: `SEGV_MAPERR 414141414141` at the `call *0x4c8(%rbx)` instruction proves that the strip buffer's forward overflow reached and overwrote `tif_postdecode` inside the TIFF struct — meaning the strip buffer was placed at a lower address.

## Overflow Into TIFF Struct

The distance from `buf` to `tif_postdecode` is `1520 + 0x4c8 = 2744` bytes. In overflow-relative terms (from the first byte past `strip_size`):

```
overflow_offset = 2744 − 1500 = 1244

```

The exploit fills the overflow region with `0x41` and places the canonical address `0x0000414141414141` (little-endian: `41 41 41 41 41 41 00 00`) at overflow offset 1244, overwriting `tif_postdecode`.

## Instruction Pointer Hijack

After the decode, `call *0x4c8(%rbx)` loads `0x0000414141414141` from the corrupted `tif_postdecode` and transfers control there. Chrome's stderr reports:

```
Received signal 11 SEGV_MAPERR 414141414141

```

GDB attached via `--renderer-cmd-prefix` shows the full state:

```
Thread 1 "chrome" received signal SIGSEGV, Segmentation fault.
0x0000414141414141 in ?? ()
rip            0x414141414141      0x414141414141
rax            0x1                 1
rbx            0x3bd8006a4c00      65798905940992
rdi            0x3bd8006a4c00      65798905940992
rsi            0x3bd8006a4610      65798905939472
rdx            0x5dc               1500
#0  0x0000414141414141 in ?? ()
#1  0x000055555f819190 in _TIFFReadEncodedStripAndAllocBuffer ()
#2  0x000055555f7ff9b8 in gtStripContig ()
#3  0x000055555f7fedfe in TIFFReadRGBAImageOriented ()
#4  0x000055555f781422 in CTiffContext::Decode(fxcrt::RetainPtr<CFX_DIBitmap>) ()
#5  0x000055555f77c658 in fxcodec::ProgressiveDecoder::ContinueDecode() ()

```

- **RIP** = `0x414141414141`, the attacker's chosen value
- **RBX/RDI** = `tif` pointer (the corrupted TIFF struct)
- **RSI** = `buf` pointer (the strip buffer); `rdi − rsi = 0x5F0 = 1520` ✓
- **RDX** = `0x5dc` (1500) = `stripsize`
- **RAX** = `0x1` = return value of `tif_decodestrip` (success)
- Frame #1 = `_TIFFReadEncodedStripAndAllocBuffer`, the return address pushed by `call *0x4c8(%rbx)`

The value `0x0000414141414141` is a proof-of-concept sentinel. An attacker with knowledge of the process address layout can replace it with the address of `system()` and place a command string at `tif + 0x00`, achieving arbitrary command execution through `system(rdi)` where `rdi = tif`.

## Reproduce

The exploit was developed and verified against the following Chromium revision, build configuration, and operating system.

Chromium commit: `46afa4acada327a9d297f780fc811554a9eecf99`

Operating system: `Ubuntu 22.04 (x86_64)`

Build configuration (`out/release/args.gn`):

```
is_asan = false
is_debug = false
dcheck_always_on = false

```

Build with:

```
autoninja -C out/release chrome

```

Generate the exploit PDF or use the `exploit.pdf` I uploaded and launch Chrome with XFA support enabled:

```
cd /path/to/chromium/src

python3 gen_exploit_pdf.py              # generates exploit.pdf

out/release/chrome --no-sandbox \
      --enable-features=PdfXfaSupport \
      --user-data-dir=./userdata exploit.pdf

```

The expected output on stderr:

```
Received signal 11 SEGV_MAPERR 414141414141

```

To verify the exact RIP value, attach GDB to the renderer:

```
out/release/chrome --no-sandbox \
    --enable-features=PdfXfaSupport \
    --renderer-cmd-prefix='gdb -ex "handle SIGSEGV stop nopass" -ex "handle SIGTERM nostop noprint" -ex run -ex "info reg rip rax rbx rdi rsi rdx" -ex "bt 6" --args' \
    --user-data-dir=./userdata exploit.pdf

```

The crash is deterministic and reproduces on every run. The entire exploit chain — from LIFO freelist manipulation through heap overflow to instruction pointer control — executes from a single crafted PDF file without requiring any source code modifications.

### ch...@google.com (2026-04-07)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-07)

Requesting merge to M146 because latest trunk commit (1606628) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1606628) appears to be after M147 branch point (1596535).

### ch...@google.com (2026-04-07)

**M146** merge request created. **Please update [crbug/500245949](https://crbug.com/500245949) to have this merge reviewed.**

### ch...@google.com (2026-04-07)

**M147** merge request created. **Please update [crbug/500246916](https://crbug.com/500246916) to have this merge reviewed.**

### dx...@google.com (2026-04-09)

2 changes merged

---

Project: pdfium  

Branch:  chromium/7680  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/145971>

M146: Patch an overflow in libtiff

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://gitlab.com/libtiff/libtiff/-/commit/0f726d9 
     
    Bug: 496907110 
    Fixed: 500245949 
    Change-Id: Ic8665879ebdd4445f473e9a1e156cfc42c294d51 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145550 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    (cherry picked from commit ca8a943c247c208fd7a9cd21b4de049f22b93070) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145971 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- A `third_party/libtiff/0034-tiff-jpeg-overflow.patch`
- M `third_party/libtiff/README.pdfium`
- M `third_party/libtiff/tif_jpeg.c`

---

Hash: 95f1333b0de63c2c3adb65755f55bfb72241d945  

Date: Thu Apr 9 16:50:50 2026


---


---

Project: pdfium  

Branch:  chromium/7727  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/145972>

M147: Patch an overflow in libtiff

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://gitlab.com/libtiff/libtiff/-/commit/0f726d9 
     
    Bug: 496907110 
    Fixed: 500246916 
    Change-Id: Ic8665879ebdd4445f473e9a1e156cfc42c294d51 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145550 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    (cherry picked from commit ca8a943c247c208fd7a9cd21b4de049f22b93070) 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145972 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com>

```

---

Files:

- A `third_party/libtiff/0034-tiff-jpeg-overflow.patch`
- M `third_party/libtiff/README.pdfium`
- M `third_party/libtiff/tif_jpeg.c`

---

Hash: da11aad230aa1ba37f923d3b82c29638beaa9a71  

Date: Thu Apr 9 16:50:56 2026


---

### pe...@google.com (2026-04-09)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### th...@chromium.org (2026-04-09)

1. Was this issue a regression for the milestone it was found in?

Not a regression. Newly found security issue.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No.

### sp...@google.com (2026-04-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $50000.00 for this report.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2026-05-14)

Project: pdfium  

Branch:  chromium/7559  

Author:  Lei Zhang [thestig@chromium.org](mailto:thestig@chromium.org)  

Link:    <https://pdfium-review.googlesource.com/147650>

[M144-LTS] Patch an overflow in libtiff

---


Expand for full commit details
```
     
    Apply fix [1] from upstream, which is not in the most recent versioned 
    release. 
     
    [1] https://gitlab.com/libtiff/libtiff/-/commit/0f726d9 
     
    Bug: 496907110 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/145550 
    Reviewed-by: Andy Phan <andyphan@chromium.org> 
    Commit-Queue: Lei Zhang <thestig@chromium.org> 
    (cherry picked from commit ca8a943c247c208fd7a9cd21b4de049f22b93070) 
     
    Change-Id: I5fd7a5fd9b7b0a6696f199ae2ea731065dd74864 
    Reviewed-on: https://pdfium-review.googlesource.com/c/pdfium/+/147650 
    Reviewed-by: Lei Zhang <thestig@chromium.org>

```

---

Files:

- A `third_party/libtiff/0034-tiff-jpeg-overflow.patch`
- M `third_party/libtiff/README.pdfium`
- M `third_party/libtiff/tif_jpeg.c`

---

Hash: f376eb162cbd3b41648be83cf2209728be682a4a  

Date: Thu May 14 18:34:01 2026


---

### pe...@google.com (2026-05-14)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### ch...@google.com (2026-07-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496907110)*
