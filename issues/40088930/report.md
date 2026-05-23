# PDFium TIFF Image Flate Decoder Code Execution Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [40088930](https://issues.chromium.org/issues/40088930) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | th...@chromium.org |
| **Created** | 2017-09-05 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/602.1.50 (KHTML, like Gecko) Version/10.0 Safari/602.1.50

Steps to reproduce the problem:
1. 
2. 
3. 

What is the expected behavior?

What went wrong?
review attached advisory

Did this work before? N/A 

Chrome version: <Copy from: 'about:version'>  Channel: n/a
OS Version: OS X 10.12
Flash Version: 

n/a

## Attachments

- [TALOS-2017-0432 - Google PDFium TIFF Image Flate Decoder Code Execution Vulnerability.txt](attachments/TALOS-2017-0432 - Google PDFium TIFF Image Flate Decoder Code Execution Vulnerability.txt) (text/plain, 17.1 KB)
- [google pdfium trigger.pdf](attachments/google pdfium trigger.pdf) (application/pdf, 324 B)

## Timeline

### el...@chromium.org (2017-09-05)

2017-MM-DD (published patch date)
TALOS-2017-0432
CVE-2017-XXXX 


Google PDFium TIFF Image Flate Decoder Code Execution Vulnerability


### Summary

An off-by-one read/write on the heap vulnerability exists in the TIFF image decoder functionality of Pdfium as used by Google Chrome up to and including 60.0.3112.101. A specially crafted PDF file can trigger an off-by-one read and write on the heap resulting in memory corruption and a possible information leak and potential code execution. The victim needs to open a malicious PDF in the browser in order to trigger this vulnerability. 


### Tested Versions

Google Chrome 60.0.3112.101


### Product URLs

[https://pdfium.googlesource.com](https://pdfium.googlesource.com)


### CVSSv3 Score

7.5 - CVSS:3.0/AV:N/AC:H/PR:N/UI:R/S:U/C:H/I:H/A:H


### CWE

CWE-193: Off-by-one Error


### Details

Pdfium is an open source PDF renderer developed by Google and used extensively in the Chrome browser, online services as well as other standalone applications. This bug was triaged on the latest git version as well as the latest chromium address sanitizer build available (asan-linux-release-498039). 

A heap-buffer overflow is present in the code responsible for decoding a compressed TIFF image stream. While parsing pixel data of the flate decoded image stream, the function TIFF_PredictLine is reached:

  void TIFF_PredictLine(uint8_t* dest_buf,
                       uint32_t row_size,
                       int BitsPerComponent,
                       int Colors,
                       int Columns) {
  ...

   int BytesPerPixel = BitsPerComponent * Colors / 8;
   if (BitsPerComponent == 16) {
     for (uint32_t i = BytesPerPixel; i < row_size; i += 2) {
       uint16_t pixel =
           (dest_buf[i - BytesPerPixel] << 8) | dest_buf[i - BytesPerPixel + 1];
       pixel += (dest_buf[i] << 8) | dest_buf[i + 1];
       dest_buf[i] = pixel >> 8;
       dest_buf[i + 1] = (uint8_t)pixel;
     }
  ...

   }
  }

In the above code, during the for loop, 4 bytes will always be read from `dest_buffer` even if the length of the buffer is less than that. This can potentially lead to an off-by-one read on the heap, followed immediately by an off-by-one write. 
In order to reach the buggy code and trigger the vulnerable state, a couple of conditions need to be satisfied. In the previous function , `TIFF_Predictor`, we see: 

  bool TIFF_Predictor(uint8_t*& data_buf,
                      uint32_t& data_size,
                      int Colors,
                      int BitsPerComponent,
                      int Columns) {
    int row_size = (Colors * BitsPerComponent * Columns + 7) / 8;                         [1]
    if (row_size == 0)
      return false;
    const int row_count = (data_size + row_size - 1) / row_size;
    const int last_row_size = data_size % row_size;                                        [2]
    for (int row = 0; row < row_count; row++) {
      uint8_t* scan_line = data_buf + row * row_size;
      if ((row + 1) * row_size > (int)data_size) {
        row_size = last_row_size;                                                        [3]
      }
      TIFF_PredictLine(scan_line, row_size, BitsPerComponent, Colors, Columns);        [4]
    }
    return true;
  }

At [1], `row_size` is calculated and is a multiple of 8. At [2], the data size of the last row is calculated, as input data might not have a multiple of `row_size` bytes available. When the last row is being used (if the next row would end up outside the data size) `row_size` is set to `last_row_size` at [3]. At [4], vulnerable function `TIFF_PredictLine` is called with the calculated row_size. If we line up the buffer sizes and `last_row_size` properly, this can result in last_row_size being 3, where `Tiff_PredictLine` actually reads/writes 4 bytes from the data buffer , leading to off-by-one read/write. 

A sample PDF to trigger this bug is:

  %PDF-1.6
                     
  47 0 obj
  <</DecodeParms
          <<        /Columns 2
          /Colors 1
                  /BitsPerComponent 16
                  /Predictor 2>>
          /Filter/FlateDecode
          /W[0 0 0]>>
  stream
  ...
  endstream
  endobj
  startxref 30
  %%EOF

The content of the stream above just needs to satisfy one condition and that is that it must decode to a length that would result in 3 in the calculation at [2] in the previously mentioned code. The lowest length that satisfies these and some of the previously mentioned conditions is 23. The values of `Columns`, `Colors` and uncompressed stream lengths can be adjusted to control the sizes of the buffers, number of loops and bytes accessed and all ultimately get passed to their corresponding values to the functions that we mentioned.

Depending on the underlying allocator and other variables, abusing this bug for information leaks or memory overwrite might or might not be possible, but it could potentially be combined with other vulnerabilities to cause further memory corruption. 


### Crash Information 

Address Sanitizer output from latest build at the time (`asan-linux-release-498039`)

  Rendering PDF file poc_test.pdf.
  =================================================================
  ==67198==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x603000003177 at pc 0x0000025b0826 bp 0x7fffffffcf70 sp 0x7fffffffcf68
  READ of size 1 at 0x603000003177 thread T0
      #0 0x25b0825 in _ZN12_GLOBAL__N_116TIFF_PredictLineEPhjiii ./out/Release/../../third_party/pdfium/core/fxcodec/codec/fx_codec_flate.cpp:478
      #1 0x25b0825 in ?? ??:0
      #2 0x25b2646 in TIFF_Predictor ./out/Release/../../third_party/pdfium/core/fxcodec/codec/fx_codec_flate.cpp:504
      #3 0x25b2646 in FlateOrLZWDecode ./out/Release/../../third_party/pdfium/core/fxcodec/codec/fx_codec_flate.cpp:805
      #4 0x25b2646 in ?? ??:0
      #5 0x2423440 in _Z24FPDFAPI_FlateOrLZWDecodebPKhjP15CPDF_DictionaryjPPhPj ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/fpdf_parser_decode.cpp:319
      #6 0x2423440 in ?? ??:0
      #7 0x24240a9 in _Z14PDF_DataDecodePKhjPK15CPDF_DictionaryjbPPhPjP14CFX_ByteStringPPS1_ crtstuff.c:?
      #8 0x24240a9 in ?? ??:0
      #9 0x2412602 in _ZN14CPDF_StreamAcc11LoadAllDataEbjb ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_stream_acc.cpp:45
      #10 0x2412602 in ?? ??:0
      #11 0x23faa1b in _ZN11CPDF_Parser14LoadCrossRefV5EPlb ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:1085
      #12 0x23faa1b in ?? ??:0
      #13 0x23ed71a in _ZN11CPDF_Parser17LoadAllCrossRefV5El ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:645
      #14 0x23ed71a in ?? ??:0
      #15 0x23eaf90 in _ZN11CPDF_Parser18StartParseInternalEP13CPDF_Document ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:248
      #16 0x23eaf90 in ?? ??:0
      #17 0x20f747b in _ZN12_GLOBAL__N_116LoadDocumentImplERK13CFX_RetainPtrI22IFX_SeekableReadStreamEPKc ./out/Release/../../third_party/pdfium/fpdfsdk/fpdfview.cpp:288
      #18 0x20f747b in ?? ??:0
      #19 0x20f7734 in FPDF_LoadCustomDocument ./out/Release/../../third_party/pdfium/fpdfsdk/fpdfview.cpp:629
      #20 0x20f7734 in ?? ??:0
      #21 0x4f64b0 in _ZN12_GLOBAL__N_19RenderPdfERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEPKcmRKNS_7OptionsES8_ ./out/Release/../../third_party/pdfium/samples/pdfium_test.cc:1406
      #22 0x4f64b0 in ?? ??:0
      #23 0x4f3b7f in main ./out/Release/../../third_party/pdfium/samples/pdfium_test.cc:1624
      #24 0x4f3b7f in ?? ??:0
      #25 0x7ffff624e82f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291
      #26 0x7ffff624e82f in ?? ??:0


  0x603000003177 is located 0 bytes to the right of 23-byte region [0x603000003160,0x603000003177)
  allocated by thread T0 here:
      #0 0x4c48e3 in __interceptor_malloc ??:?
      #1 0x4c48e3 in ?? ??:0
      #2 0x25b2106 in PartitionAllocGenericFlags ./out/Release/../../third_party/pdfium/third_party/base/allocator/partition_allocator/partition_alloc.h:787
      #3 0x25b2106 in FX_SafeAlloc ./out/Release/../../third_party/pdfium/core/fxcrt/fx_memory.h:46
      #4 0x25b2106 in FX_AllocOrDie ./out/Release/../../third_party/pdfium/core/fxcrt/fx_memory.h:67
      #5 0x25b2106 in FlateUncompress ./out/Release/../../third_party/pdfium/core/fxcodec/codec/fx_codec_flate.cpp:556
      #6 0x25b2106 in FlateOrLZWDecode ./out/Release/../../third_party/pdfium/core/fxcodec/codec/fx_codec_flate.cpp:794
      #7 0x25b2106 in ?? ??:0
      #8 0x2423440 in _Z24FPDFAPI_FlateOrLZWDecodebPKhjP15CPDF_DictionaryjPPhPj ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/fpdf_parser_decode.cpp:319
      #9 0x2423440 in ?? ??:0
      #10 0x24240a9 in _Z14PDF_DataDecodePKhjPK15CPDF_DictionaryjbPPhPjP14CFX_ByteStringPPS1_ crtstuff.c:?
      #11 0x24240a9 in ?? ??:0
      #12 0x2412602 in _ZN14CPDF_StreamAcc11LoadAllDataEbjb ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_stream_acc.cpp:45
      #13 0x2412602 in ?? ??:0
      #14 0x23faa1b in _ZN11CPDF_Parser14LoadCrossRefV5EPlb ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:1085
      #15 0x23faa1b in ?? ??:0
      #16 0x23ed71a in _ZN11CPDF_Parser17LoadAllCrossRefV5El ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:645
      #17 0x23ed71a in ?? ??:0
      #18 0x23eaf90 in _ZN11CPDF_Parser18StartParseInternalEP13CPDF_Document ./out/Release/../../third_party/pdfium/core/fpdfapi/parser/cpdf_parser.cpp:248
      #19 0x23eaf90 in ?? ??:0
      #20 0x20f747b in _ZN12_GLOBAL__N_116LoadDocumentImplERK13CFX_RetainPtrI22IFX_SeekableReadStreamEPKc ./out/Release/../../third_party/pdfium/fpdfsdk/fpdfview.cpp:288
      #21 0x20f747b in ?? ??:0
      #22 0x20f7734 in FPDF_LoadCustomDocument ./out/Release/../../third_party/pdfium/fpdfsdk/fpdfview.cpp:629
      #23 0x20f7734 in ?? ??:0
      #24 0x4f64b0 in _ZN12_GLOBAL__N_19RenderPdfERKNSt3__112basic_stringIcNS0_11char_traitsIcEENS0_9allocatorIcEEEEPKcmRKNS_7OptionsES8_ ./out/Release/../../third_party/pdfium/samples/pdfium_test.cc:1406
      #25 0x4f64b0 in ?? ??:0
      #26 0x4f3b7f in main ./out/Release/../../third_party/pdfium/samples/pdfium_test.cc:1624
      #27 0x4f3b7f in ?? ??:0
      #28 0x7ffff624e82f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291
      #29 0x7ffff624e82f in ?? ??:0


  SUMMARY: AddressSanitizer: heap-buffer-overflow (/home/user/pdfium/repo/asan-linux-release-498039/pdfium_test+0x25b0825)
  Shadow bytes around the buggy address:
    0x0c067fff85d0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff85e0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff85f0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff8600: fa fa fd fd fd fd fa fa fd fd fd fd fa fa fd fd
    0x0c067fff8610: fd fd fa fa fd fd fd fa fa fa fd fd fd fa fa fa
  =>0x0c067fff8620: fd fd fd fa fa fa fd fd fd fa fa fa 00 00[07]fa
    0x0c067fff8630: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff8640: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff8650: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff8660: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
    0x0c067fff8670: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  Shadow byte legend (one shadow byte represents 8 application bytes):
    Addressable:           00
    Partially addressable: 01 02 03 04 05 06 07
    Heap left redzone:       fa
    Freed heap region:       fd
    Stack left redzone:      f1
    Stack mid redzone:       f2
    Stack right redzone:     f3
    Stack after return:      f5
    Stack use after scope:   f8
    Global redzone:          f9
    Global init order:       f6
    Poisoned by user:        f7
    Container overflow:      fc
    Array cookie:            ac
    Intra object redzone:    bb
    ASan internal:           fe
    Left alloca redzone:     ca
    Right alloca redzone:    cb
  ==67198==ABORTING


Official, latest version of Chrome on Windows crashes with the following when run with PageHeap enabled (output from BugId):

  BugId:            OOBW[0x1FB]+0~1#b6d7 c40.313 
  Location:         chrome.exe!verifier.dll!AVrfpDphCheckPageHeapBlock 
  Description:      Page heap detected heap corruption at 0x8EA7FFB; at the end of a 507/0x1FB bytes heap block at 0x8EA7E00. This appears to be a classic buffer-overrun vulnerability. The following byte values were written to the corrupted area: 22. 
  Version:          chrome.exe: 60.0.3112.113 (x86)
  verifier.dll: 6.1.7600.16385 (x86) 
  Security impact:  Potentially highly exploitable security issue. 
  Integrity level:  0x2000 (Medium Integrity; this process appears to not be sandboxed!) 
  Arguments:  ['--enable-experimental-accessibility-features', '--enable-experimental-canvas-features', '--enable-experimental-input-view-features', '--enable-experimental-web-platform-features', '--enable-logging=stderr', '--enable-usermedia-screen-capturing', '--enable-viewport', '--enable-webgl-draft-extensions', '--enable-webvr', '--expose-internals-for-testing', '--disable-popup-blocking', '--disable-prompt-on-repost', '--force-renderer-accessibility', '--javascript-harmony', '--js-flags="--expose-gc"', '--no-sandbox', 'c:\\Users\\ea\\Desktop\\poc.pdf'] 

  Stack:
  verifier.dll!VerifierStopMessage + 0x1F8 (this frame is irrelevant to this bug)
  2.verifier.dll!AVrfpDphReportCorruptedBlock + 0x1C2 (this frame is irrelevant to this bug)
  3.verifier.dll!AVrfpDphCheckPageHeapBlock + 0x161 (id: c40)
  4.verifier.dll!AVrfpDphFindBusyMemory + 0xDA (id: 313)
  5.verifier.dll!AVrfpDphFindBusyMemoryAndRemoveFromBusyList + 0x20
  6.ntdll.dll!RtlpDebugPageHeapFree + ? (the exact offset is not known)
  7.ntdll.dll!RtlDebugFreeHeap + 0x2F
  8.ntdll.dll!RtlpFreeHeap + 0x5D
  9.ntdll.dll!RtlFreeHeap + 0x142
  10.kernel32.dll!HeapFree + 0x14
  11.chrome_child.dll + 0x163239 (no function symbol available)
  12.chrome_child.dll + 0x1852FAA (no function symbol available)
  13.chrome_child.dll + 0x184DDD1 (no function symbol available)
  14.chrome_child.dll + 0x1846493 (no function symbol available)
  15.chrome_child.dll + 0x18488BD (no function symbol available)
  16.chrome_child.dll + 0x18485B5 (no function symbol available)
  17.chrome_child.dll + 0x1823308 (no function symbol available)
  18.chrome_child.dll + 0x18175AB (no function symbol available)
  19.chrome_child.dll + 0x181413D (no function symbol available)
  20.chrome_child.dll + 0x181468D (no function symbol available)
  21.chrome_child.dll + 0x181F15A (no function symbol available)
  22.chrome_child.dll + 0x181E1AF (no function symbol available)
  23.chrome_child.dll + 0x17CA70A (no function symbol available)
  24.chrome_child.dll + 0x1437254 (no function symbol available)
  25.chrome_child.dll + 0x143797E (no function symbol available)
  26.chrome_child.dll + 0x16729C1 (no function symbol available)

  Page heap output for heap block near 0x8EA7FFB
     address 08ea7e00 found in
     _DPH_HEAP_ROOT @ 4161000
     in busy allocation (  DPH_HEAP_BLOCK:         UserAddr         UserSize -         VirtAddr         VirtSize)
                                  8712000:          8ea7e00              1fb -          8ea7000             2000
     6ccf8e89 verifier!AVrfDebugPageHeapAllocate+0x00000229
     77876206 ntdll!RtlDebugAllocateHeap+0x00000030
     7783a127 ntdll!RtlpAllocateHeap+0x000000c4
     77805950 ntdll!RtlAllocateHeap+0x0000023a
     58de52c3 chrome_child!ovly_debug_event+0x0014dff3
     5a357dd2 chrome_child!IsSandboxedProcess+0x003fb31f
     5a3cf306 chrome_child!IsSandboxedProcess+0x00472853
     5a379bca chrome_child!IsSandboxedProcess+0x0041d117
     5a37a05d chrome_child!IsSandboxedProcess+0x0041d5aa
     5a38311c chrome_child!IsSandboxedProcess+0x00426669
     5a376b0e chrome_child!IsSandboxedProcess+0x0041a05b
     5a376493 chrome_child!IsSandboxedProcess+0x004199e0
     5a3788bd chrome_child!IsSandboxedProcess+0x0041be0a
     5a3785b5 chrome_child!IsSandboxedProcess+0x0041bb02
     5a353308 chrome_child!IsSandboxedProcess+0x003f6855
     5a3475ab chrome_child!IsSandboxedProcess+0x003eaaf8
     5a34413d chrome_child!IsSandboxedProcess+0x003e768a
     5a34468d chrome_child!IsSandboxedProcess+0x003e7bda
     5a34f15a chrome_child!IsSandboxedProcess+0x003f26a7
     5a34e1af chrome_child!IsSandboxedProcess+0x003f16fc
     5a2fa70a chrome_child!IsSandboxedProcess+0x0039dc57
     59f67254 chrome_child!IsSandboxedProcess+0x0000a7a1
     59f6797e chrome_child!IsSandboxedProcess+0x0000aecb
     5a1a29c1 chrome_child!IsSandboxedProcess+0x00245f0e
     5a1a2be2 chrome_child!IsSandboxedProcess+0x0024612f
     5a17e7ea chrome_child!IsSandboxedProcess+0x00221d37
     5a17e9fb chrome_child!IsSandboxedProcess+0x00221f48
     58c33f7e chrome_child+0x00103f7e
     58c31129 chrome_child+0x00101129
     58c33bc4 chrome_child+0x00103bc4
     58c996e8 chrome_child!ovly_debug_event+0x00002418
     58f54b95 chrome_child!ChromeMain+0x0000b501


### Credit 

Discovered by Aleksandar Nikolic of Cisco Talos.
http://talosintelligence.com/vulnerability-reports/


### Timeline


2017-09-05 - Vendor Disclosure
YYYY-MM-DD - Public Release


[Monorail components: Internals>Plugins>PDF]

### [Deleted User] (2017-09-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2017-09-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5924241940938752.

### ts...@chromium.org (2017-09-05)

[Empty comment from Monorail migration]

### ds...@chromium.org (2017-09-05)

npm@ more TIFF fun if you've got time, feel free to assign back if you don't.

### cl...@chromium.org (2017-09-05)

ClusterFuzz testcase 5924241940938752 is flaky and no longer crashes, so closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### th...@chromium.org (2017-09-05)

Repros with ASAN here.

### th...@chromium.org (2017-09-05)

Uploaded https://pdfium-review.googlesource.com/13212

### np...@chromium.org (2017-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-07)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-09-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-08)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/131c0eb2e34ece6ede6288842cb3004ec3c600d4

commit 131c0eb2e34ece6ede6288842cb3004ec3c600d4
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Sep 08 22:51:02 2017

Fix an off by 1 error in TIFF_PredictLine().

BUG=chromium:762106

Change-Id: I714d69320cc4fb81d535f811c18d4ef91fec44d3
Reviewed-on: https://pdfium-review.googlesource.com/13212
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>

[modify] https://crrev.com/131c0eb2e34ece6ede6288842cb3004ec3c600d4/core/fxcodec/codec/fx_codec_flate.cpp


### th...@chromium.org (2017-09-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/60ffdffea2683c732514874a7d3548d5acecf740

commit 60ffdffea2683c732514874a7d3548d5acecf740
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Sat Sep 09 00:31:42 2017

Roll src/third_party/pdfium/ ee1e75790..131c0eb2e (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/ee1e757902d0..131c0eb2e34e

$ git log ee1e75790..131c0eb2e --date=short --no-merges --format='%ad %ae %s'
2017-09-08 thestig Fix an off by 1 error in TIFF_PredictLine().

Created with:
  roll-dep src/third_party/pdfium
BUG=762106


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: I7d6bba2e7c2c73d247a9390597f2b09e397663e8
Reviewed-on: https://chromium-review.googlesource.com/658400
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#500756}
[modify] https://crrev.com/60ffdffea2683c732514874a7d3548d5acecf740/DEPS


### sh...@chromium.org (2017-09-09)

[Empty comment from Monorail migration]

### [Deleted User] (2017-09-11)

Is there a public disclosure release date scheduled since this issue is now fixed?


### aw...@google.com (2017-09-11)

regiwils@ - standard procedure is that the bug will be automatically opened to public view 14 weeks after the fix date.

This is very likely to be merged to M62, for a stable release in mid October (https://www.chromium.org/developers/calendar)

### sh...@chromium.org (2017-09-11)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Please contact the milestone owner if you have questions.
Owners: amineer@(Android), cmasso@(iOS), bhthompson@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2017-09-11)

Approving merge to M62, branch: 3202. 

### sh...@chromium.org (2017-09-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bu...@chromium.org (2017-09-15)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/fc556ac0c823bccffaff84fea7a118835f33147a

commit fc556ac0c823bccffaff84fea7a118835f33147a
Author: Lei Zhang <thestig@chromium.org>
Date: Fri Sep 15 21:37:14 2017

M62: Fix an off by 1 error in TIFF_PredictLine().

BUG=chromium:762106
TBR=tsepez@chromium.org

Change-Id: I714d69320cc4fb81d535f811c18d4ef91fec44d3
Reviewed-on: https://pdfium-review.googlesource.com/13212
Commit-Queue: Lei Zhang <thestig@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
(cherry picked from commit 131c0eb2e34ece6ede6288842cb3004ec3c600d4)
Reviewed-on: https://pdfium-review.googlesource.com/14190
Reviewed-by: Lei Zhang <thestig@chromium.org>

[modify] https://crrev.com/fc556ac0c823bccffaff84fea7a118835f33147a/core/fxcodec/codec/fx_codec_flate.cpp


### in...@chromium.org (2017-09-18)

We have made a bunch of changes on ClusterFuzz side, so resetting ClusterFuzz-Wrong label.

### aw...@chromium.org (2017-09-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-18)

Hi regiwils@ - the VRP panel has decided to award $2,000 for this report, and noted their thanks for the detailed bug explanation. A member of our finance team will be in touch to arrange payment.  Also, how would you like to be credited in release notes?  Thanks!

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2017-09-19)

Thanks for the update and acknowledgement! We would like credit to appear as "Discovered by Aleksandar Nikolic of Cisco Talos."


### aw...@google.com (2017-10-16)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-10-18)

[Empty comment from Monorail migration]

### [Deleted User] (2017-10-19)

Is this confirming public release?


### aw...@chromium.org (2017-10-19)

While this bug is still private (by default it will be made public 14 weeks after the fix landed), it has been included in our release notes: https://chromereleases.googleblog.com/2017/10/stable-channel-update-for-desktop.html

### sh...@chromium.org (2017-12-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/762106?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088930)*
