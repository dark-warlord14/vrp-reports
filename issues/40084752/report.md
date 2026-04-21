# Security: heap-buffer-overflow in opj_tcd_init_tile

| Field | Value |
|-------|-------|
| **Issue ID** | [40084752](https://issues.chromium.org/issues/40084752) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | [Deleted User] |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-07-04 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

A heap buffer overflow vulnerability is present in the jpeg2000.

## File libopenjpeg20/tcd.c, line 787:

```
	l_level_no = l_tilec->numresolutions - 1;  
	...  
		l_res->x0 = opj_int_ceildivpow2(l_tilec->x0, (OPJ_INT32)l_level_no);  
		l_res->y0 = opj_int_ceildivpow2(l_tilec->y0, (OPJ_INT32)l_level_no);  
		l_res->x1 = opj_int_ceildivpow2(l_tilec->x1, (OPJ_INT32)l_level_no);  
		l_res->y1 = opj_int_ceildivpow2(l_tilec->y1, (OPJ_INT32)l_level_no);  
		...  
		l_pdx = l_tccp->prcw[resno];  
		l_pdy = l_tccp->prch[resno];  
		...  
		l_tl_prc_x_start = opj_int_floordivpow2(l_res->x0, (OPJ_INT32)l_pdx) << l_pdx;  
		l_tl_prc_y_start = opj_int_floordivpow2(l_res->y0, (OPJ_INT32)l_pdy) << l_pdy;  
		l_br_prc_x_end = opj_int_ceildivpow2(l_res->x1, (OPJ_INT32)l_pdx) << l_pdx;  
		l_br_prc_y_end = opj_int_ceildivpow2(l_res->y1, (OPJ_INT32)l_pdy) << l_pdy;  
		...  
		l_res->pw = (l_res->x0 == l_res->x1) ? 0 : (OPJ_UINT32)((l_br_prc_x_end - l_tl_prc_x_start) >> l_pdx);  
		l_res->ph = (l_res->y0 == l_res->y1) ? 0 : (OPJ_UINT32)((l_br_prc_y_end - l_tl_prc_y_start) >> l_pdy);  
		...  
		l_nb_precincts = l_res->pw \* l_res->ph;  
		l_nb_precinct_size = l_nb_precincts \* (OPJ_UINT32)sizeof(opj_tcd_precinct_t);  

```

---

In my testcase, I used an image with a l\_level\_no == 1, l\_res->x1 == 0x446C, l\_res->y1 == 0x446C, l\_pdx == 0.  

sizeof(opj\_tcd\_precinct\_t) different between 32bit and 64bit.

The result of the multiplication can overflow.

On x86, poc\_32bit.pdf => ((0x50F6 >> 1) \* (0x50F6 >> 1) \* 0x28) == 0xABBE8  

On x64, poc\_64bit.pdf => ((0x446C >> 1) \* (0x446C >> 1) \* 0x38) == 0x5BDE0

## File libopenjpeg20/tcd.c, line 881:

## l\_band->precincts = (opj\_tcd\_precinct\_t \*) opj\_malloc( /\*3 \* \*/ l\_nb\_precinct\_size);

opj\_malloc call will allocate a buffer too small.

**VERSION**  

Chrome Version: 51.0.2704.106  

latest pdfium\_test

**REPRODUCTION CASE**  

Attached as poc\_32bit.pdf, poc\_64bit.pdf

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

# /pdfium/out/asan$ ./pdfium\_test poc\_64bit.pdf Rendering PDF file poc\_64bit.pdf.

==18756==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x7fe8c99875e0 at pc 0x0000007a7569 bp 0x7fff71569250 sp 0x7fff71569248  

READ of size 8 at 0x7fe8c99875e0 thread T0  

#0 0x7a7568 in opj\_tcd\_init\_tile (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x7a7568)  

#1 0x7a8ca3 in opj\_tcd\_init\_decode\_tile (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x7a8ca3)  

#2 0x6f8945 in opj\_j2k\_read\_tile\_header (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x6f8945)  

#3 0x72aa4d in opj\_j2k\_decode\_tiles (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x72aa4d)  

#4 0x6f3b2d in opj\_j2k\_exec (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x6f3b2d)  

#5 0x706c1e in opj\_j2k\_decode (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x706c1e)  

#6 0x73f08e in opj\_jp2\_decode (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x73f08e)  

#7 0x75bd06 in opj\_decode (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x75bd06)  

#8 0x316946e in CJPX\_Decoder::Init(unsigned char const\*, unsigned int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x316946e)  

#9 0x316cfb3 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, CPDF\_ColorSpace\*) out/asan/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:887:10  

#10 0x2f037d9 in CPDF\_DIBSource::LoadJpxBitmap() out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:634:24  

#11 0x2ef8749 in CPDF\_DIBSource::CreateDecoder() out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:593:5  

#12 0x2efe4d2 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:311:13  

#13 0x2ed2ea8 in CPDF\_ImageCacheEntry::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2ed2ea8)  

#14 0x2ed2884 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:13  

#15 0x2f12128 in CPDF\_ImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2f12128)  

#16 0x2f132a9 in CPDF\_ImageLoader::Start(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, CPDF\_ImageLoaderHandle\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2f132a9)  

#17 0x2ee23e3 in CPDF\_ImageRenderer::StartLoadDIBSource() (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2ee23e3)  

#18 0x2eda910 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2eda910)  

#19 0x2eb4f23 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:284:10  

#20 0x2ec13da in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1026:13  

#21 0x2ebfafa in CPDF\_ProgressiveRenderer::Start(IFX\_Pause\*) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2ebfafa)  

#22 0x2c85cfe in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2c85cfe)  

#23 0x2c848f0 in FPDF\_RenderPageBitmap out/asan/../../fpdfsdk/fpdfview.cpp:622:3  

#24 0x4fa9ab in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\* const&, void\* const&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) out/asan/../../samples/pdfium\_test.cc:552:5  

#25 0x4fd063 in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x4fd063)  

#26 0x4ffa5d in main out/asan/../../samples/pdfium\_test.cc:878:5  

#27 0x7fe917fa5f44 (/lib/x86\_64-linux-gnu/libc.so.6+0x21f44)

0x7fe8c99875e0 is located 0 bytes to the right of 376288-byte region [0x7fe8c992b800,0x7fe8c99875e0)  

allocated by thread T0 here:  

#0 0x4b772b in \_\_interceptor\_malloc (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x4b772b)  

#1 0x7a6657 in opj\_tcd\_init\_tile (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x7a6657)  

#2 0x7a8ca3 in opj\_tcd\_init\_decode\_tile (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x7a8ca3)  

#3 0x6f8945 in opj\_j2k\_read\_tile\_header (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x6f8945)  

#4 0x72aa4d in opj\_j2k\_decode\_tiles (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x72aa4d)  

#5 0x6f3b2d in opj\_j2k\_exec (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x6f3b2d)  

#6 0x706c1e in opj\_j2k\_decode (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x706c1e)  

#7 0x73f08e in opj\_jp2\_decode (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x73f08e)  

#8 0x75bd06 in opj\_decode (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x75bd06)  

#9 0x316946e in CJPX\_Decoder::Init(unsigned char const\*, unsigned int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x316946e)  

#10 0x316cfb3 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, CPDF\_ColorSpace\*) out/asan/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:887:10  

#11 0x2f037d9 in CPDF\_DIBSource::LoadJpxBitmap() out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:634:24  

#12 0x2ef8749 in CPDF\_DIBSource::CreateDecoder() out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:593:5  

#13 0x2efe4d2 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:311:13  

#14 0x2ed2ea8 in CPDF\_ImageCacheEntry::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2ed2ea8)  

#15 0x2ed2884 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:13  

#16 0x2f12128 in CPDF\_ImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2f12128)  

#17 0x2f132a9 in CPDF\_ImageLoader::Start(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, CPDF\_ImageLoaderHandle\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2f132a9)  

#18 0x2ee23e3 in CPDF\_ImageRenderer::StartLoadDIBSource() (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2ee23e3)  

#19 0x2eda910 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2eda910)  

#20 0x2eb4f23 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:284:10  

#21 0x2ec13da in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1026:13  

#22 0x2ebfafa in CPDF\_ProgressiveRenderer::Start(IFX\_Pause\*) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2ebfafa)  

#23 0x2c85cfe in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x2c85cfe)  

#24 0x2c848f0 in FPDF\_RenderPageBitmap out/asan/../../fpdfsdk/fpdfview.cpp:622:3  

#25 0x4fa9ab in RenderPage(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, void\* const&, void\* const&, int, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) out/asan/../../samples/pdfium\_test.cc:552:5  

#26 0x4fd063 in RenderPdf(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, char const\*, unsigned long, Options const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&) (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x4fd063)  

#27 0x4ffa5d in main out/asan/../../samples/pdfium\_test.cc:878:5  

#28 0x7fe917fa5f44 (/lib/x86\_64-linux-gnu/libc.so.6+0x21f44)

SUMMARY: AddressSanitizer: heap-buffer-overflow (/pdfium/repo/pdfium/out/asan/pdfium\_test+0x7a7568) in opj\_tcd\_init\_tile  

Shadow bytes around the buggy address:  

0x0ffd99328e60: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffd99328e70: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffd99328e80: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffd99328e90: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0ffd99328ea0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x0ffd99328eb0: 00 00 00 00 00 00 00 00 00 00 00 00[fa]fa fa fa  

0x0ffd99328ec0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ffd99328ed0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ffd99328ee0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ffd99328ef0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0ffd99328f00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==18756==ABORTING

## Attachments

- [poc_32bit.pdf](attachments/poc_32bit.pdf) (application/pdf, 2.3 KB)
- [poc_64bit.pdf](attachments/poc_64bit.pdf) (application/pdf, 2.3 KB)
- [poc_64bit_write.pdf](attachments/poc_64bit_write.pdf) (application/pdf, 2.3 KB)
- [ASAN.txt](attachments/ASAN.txt) (text/plain, 13.9 KB)

## Timeline

### pa...@chromium.org (2016-07-04)

thestig, can you please triage this one? Thanks!

[Monorail components: Blink>Image Internals>Plugins>PDF]

### cl...@chromium.org (2016-07-04)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5910862410022912

### pa...@chromium.org (2016-07-04)

[Empty comment from Monorail migration]

### [Deleted User] (2016-07-06)

I modified a size of image and then it caused an out of bound write.
Please check new attached file.


poc_64bit_write.pdf => ((0x7754 >> 1) * (0x75B0 >> 1) * 0x38) == 0x300000080

0x80 mod sizeof(opj_tcd_precinct) = 0x10

----------------------------------------
typedef struct opj_tcd_precinct {
	OPJ_INT32 x0, y0, x1, y1;
	OPJ_UINT32 cw, ch;           <-- offset 0x10 is here.
	union{
		opj_tcd_cblk_enc_t* enc;
		opj_tcd_cblk_dec_t* dec;
		void*               blocks;
	} cblks;
	OPJ_UINT32 block_size;
	opj_tgt_tree_t *incltree;
	opj_tgt_tree_t *imsbtree;
} opj_tcd_precinct_t;
----------------------------------------

File libopenjpeg20/tcd.c, line 932:
----------------------------------------
	l_current_precinct->cw = (OPJ_UINT32)((brcblkxend - tlcblkxstart) >> cblkwidthexpn);  <-- out of bound write
	l_current_precinct->ch = (OPJ_UINT32)((brcblkyend - tlcblkystart) >> cblkheightexpn);
----------------------------------------			



### th...@chromium.org (2016-07-06)

ochang: Do you have time to take a look?

### cl...@chromium.org (2016-07-06)

ClusterFuzz has detected this testcase as flaky and is unable to reproduce it in the original crash revision. Skipping fixed testing check and marking it as potentially fixed.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5910862410022912

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Sanitizer CHECK failure
Crash Address: 
Crash State:
  "((0)) != (0)" (0x0, 0x0)
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95fjwHL7PQC84fVs1gHVtKuJC5J2zR0ncvHSglkhpnREIPKhSjaZ63_EGN_8jxskMWWuPrTSqGZXvdlceKO-5Iw4nybcPdfUxCV6tWoFD42AIXva9uSEPV5lkgjZQ-mws6gkcfhsYuyyd4wC0v4rJQ5u4CZZQ?testcase_id=5910862410022912


See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-06)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5674864879075328

### cl...@chromium.org (2016-07-06)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5674864879075328

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x610000007800
Crash State:
  opj_tcd_init_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856

Minimized Testcase (2.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gM-CjflTe2gRXtyxTlvZhNFNE6j4XrzOsXQe9_8LaTlIucnEvoK2B_wZ9bvhSinmvZRPmJ_zEVKr08__Uwg4b3r4wOgao1B7Kk9UKMMQv6Aap6OZTaX2yJ48R5Ch60U9anei1LGPSGlHBmlWXl7-ImIynKA?testcase_id=5674864879075328

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### oc...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-07-06)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Image]

### bu...@chromium.org (2016-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/95adc31201fd4d1f3b9ec96a62993e64d3273ed9

commit 95adc31201fd4d1f3b9ec96a62993e64d3273ed9
Author: ochang <ochang@chromium.org>
Date: Thu Jul 07 02:47:54 2016

Roll PDFium cfb31d6..2f6d148

https://pdfium.googlesource.com/pdfium.git/+log/cfb31d6..2f6d148

BUG=625541,625823

Review-Url: https://codereview.chromium.org/2128163002
Cr-Commit-Position: refs/heads/master@{#404047}

[modify] https://crrev.com/95adc31201fd4d1f3b9ec96a62993e64d3273ed9/DEPS


### cl...@chromium.org (2016-07-07)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5674864879075328

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x610000007800
Crash State:
  opj_tcd_init_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856

Minimized Testcase (2.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gM-CjflTe2gRXtyxTlvZhNFNE6j4XrzOsXQe9_8LaTlIucnEvoK2B_wZ9bvhSinmvZRPmJ_zEVKr08__Uwg4b3r4wOgao1B7Kk9UKMMQv6Aap6OZTaX2yJ48R5Ch60U9anei1LGPSGlHBmlWXl7-ImIynKA?testcase_id=5674864879075328

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### cl...@chromium.org (2016-07-07)

ClusterFuzz has detected this issue as fixed in range 403906:404161.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5674864879075328

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x610000007800
Crash State:
  opj_tcd_init_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=403906:404161

Minimized Testcase (2.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gM-CjflTe2gRXtyxTlvZhNFNE6j4XrzOsXQe9_8LaTlIucnEvoK2B_wZ9bvhSinmvZRPmJ_zEVKr08__Uwg4b3r4wOgao1B7Kk9UKMMQv6Aap6OZTaX2yJ48R5Ch60U9anei1LGPSGlHBmlWXl7-ImIynKA?testcase_id=5674864879075328

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-07-07)

ClusterFuzz testcase is verified as fixed, closing issue.

If this is incorrect, please add ClusterFuzz-Wrong label and re-open the issue.

### cl...@chromium.org (2016-07-07)

ClusterFuzz has detected this issue as fixed in range 403906:404161.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5674864879075328

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x610000007800
Crash State:
  opj_tcd_init_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=403906:404161

Minimized Testcase (2.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gM-CjflTe2gRXtyxTlvZhNFNE6j4XrzOsXQe9_8LaTlIucnEvoK2B_wZ9bvhSinmvZRPmJ_zEVKr08__Uwg4b3r4wOgao1B7Kk9UKMMQv6Aap6OZTaX2yJ48R5Ch60U9anei1LGPSGlHBmlWXl7-ImIynKA?testcase_id=5674864879075328

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### oc...@chromium.org (2016-07-07)

Requesting merges.

### sh...@chromium.org (2016-07-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-07-08)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5674864879075328

Job Type: linux_asan_pdfium
Platform Id: linux

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0x610000007800
Crash State:
  opj_tcd_init_tile
  opj_j2k_read_tile_header
  opj_j2k_decode_tiles
  
Recommended Security Severity: High

Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=299683:299856
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_pdfium&range=403906:404161

Minimized Testcase (2.30 Kb): https://cluster-fuzz.appspot.com/download/AMIfv94gM-CjflTe2gRXtyxTlvZhNFNE6j4XrzOsXQe9_8LaTlIucnEvoK2B_wZ9bvhSinmvZRPmJ_zEVKr08__Uwg4b3r4wOgao1B7Kk9UKMMQv6Aap6OZTaX2yJ48R5Ch60U9anei1LGPSGlHBmlWXl7-ImIynKA?testcase_id=5674864879075328

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-07-14)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

### oc...@chromium.org (2016-07-15)

Yes, it's safe to merge.

### go...@chromium.org (2016-07-15)

Thank you ochang@.

awhalley@, should we take this merge in for M52 and M53? Please note that fixed is verified by ClusterFuzz and baked in canary but not in dev.

### aw...@chromium.org (2016-07-15)

Yep, we should take this for both.

### go...@chromium.org (2016-07-15)

Ok, approving merge to M52 branch 2743 and M53 branch 2785. Please merge ASAP. Thank you.

### bu...@chromium.org (2016-07-15)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/461182bf88597975d2aa8c5b64aaed4e90137956

commit 461182bf88597975d2aa8c5b64aaed4e90137956
Author: Oliver Chang <ochang@google.com>
Date: Fri Jul 15 16:32:20 2016


### oc...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

Congratulations! Our panel has awarded $3,000 for this bug!  A member of our finance team will be in touch in the next few weeks.

(Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.)

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-04)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/625541?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084752)*
