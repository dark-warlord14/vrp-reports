# Security: heap-buffer-overflow in opj_tcd_code_block_dec_allocate

| Field | Value |
|-------|-------|
| **Issue ID** | [40084863](https://issues.chromium.org/issues/40084863) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | [Deleted User] |
| **Assignee** | mo...@google.com |
| **Created** | 2016-07-16 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**

A heap buffer overflow vulnerability is present in the openjpeg.

## File libopenjpeg20/tcd.c, line 842:

## 689 OPJ\_UINT32 l\_nb\_code\_blocks\_size; ... 842 l\_nb\_code\_blocks = l\_current\_precinct->cw \* l\_current\_precinct->ch; 843 844 l\_nb\_code\_blocks\_size = l\_nb\_code\_blocks \* (OPJ\_UINT32)sizeof\_block; 845 846 if (! l\_current\_precinct->cblks.blocks) { 847 l\_current\_precinct->cblks.blocks = opj\_malloc(l\_nb\_code\_blocks\_size);

In my testcase, I used an image with a l\_current\_precinct->cw == 0x2000, l\_current\_precinct->ch == 0x2000, sizeof\_block == 0x40.

Therefore, 0x2000\*0x2000\*0x40 will integer overflow.

opj\_malloc will allocate memory with size 0.

**VERSION**  

latest pdfium\_test  

Ubuntu 16.04 x64

**REPRODUCTION CASE**  

Attached as poc.pdf

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** /pdfium/pdfium/out/asan$ ./pdfium\_test ./poc.pdf Rendering PDF file ./poc.pdf.

==4828==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000dc90 at pc 0x000000702fa4 bp 0x7ffe108f38a0 sp 0x7ffe108f3898  

READ of size 8 at 0x60200000dc90 thread T0  

#0 0x702fa3 in opj\_tcd\_code\_block\_dec\_allocate ./out/asan/../../third\_party/libopenjpeg20/tcd.c:1111  

#1 0x6fa487 in opj\_tcd\_init\_tile ./out/asan/../../third\_party/libopenjpeg20/tcd.c:1024  

#2 0x6fa963 in opj\_tcd\_init\_decode\_tile ./out/asan/../../third\_party/libopenjpeg20/tcd.c:1056  

#3 0x64a3b5 in opj\_j2k\_read\_tile\_header ./out/asan/../../third\_party/libopenjpeg20/j2k.c:8020  

#4 0x67c55d in opj\_j2k\_decode\_tiles ./out/asan/../../third\_party/libopenjpeg20/j2k.c:9582  

#5 0x64559d in opj\_j2k\_exec ./out/asan/../../third\_party/libopenjpeg20/j2k.c:7290 (discriminator 1)  

#6 0x65868e in opj\_j2k\_decode ./out/asan/../../third\_party/libopenjpeg20/j2k.c:9810  

#7 0x690b9e in opj\_jp2\_decode ./out/asan/../../third\_party/libopenjpeg20/jp2.c:1488  

#8 0x6ad856 in opj\_decode ./out/asan/../../third\_party/libopenjpeg20/openjpeg.c:412  

#9 0x2986c7e in \_ZN12CJPX\_Decoder4InitEPKhj ./out/asan/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764  

#10 0x298a7c3 in \_ZN16CCodec\_JpxModule13CreateDecoderEPKhjP15CPDF\_ColorSpace ./out/asan/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:887 (discriminator 4)  

#11 0x2712799 in \_ZN14CPDF\_DIBSource13LoadJpxBitmapEv ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:634 (discriminator 1)  

#12 0x2707709 in \_ZN14CPDF\_DIBSource13CreateDecoderEv ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:593  

#13 0x270d492 in \_ZN14CPDF\_DIBSource18StartLoadDIBSourceEP13CPDF\_DocumentPK11CPDF\_StreamiP15CPDF\_DictionaryS6\_iji ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:311  

#14 0x26e10b8 in \_ZN20CPDF\_ImageCacheEntry20StartGetCachedBitmapEP15CPDF\_DictionaryS1\_ijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:282  

#15 0x26e0a94 in \_ZN20CPDF\_PageRenderCache20StartGetCachedBitmapEP11CPDF\_StreamijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131  

#16 0x27210e8 in \_ZN22CPDF\_ImageLoaderHandle5StartEP16CPDF\_ImageLoaderPK16CPDF\_ImageObjectP20CPDF\_PageRenderCacheijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1502 (discriminator 1)  

#17 0x27223ee in \_ZN16CPDF\_ImageLoader5StartEPK16CPDF\_ImageObjectP20CPDF\_PageRenderCachePNSt3\_\_110unique\_ptrI22CPDF\_ImageLoaderHandleNS5\_14default\_deleteIS7\_EEEEijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1565  

#18 0x26f1053 in \_ZN18CPDF\_ImageRenderer18StartLoadDIBSourceEv ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:360  

#19 0x26e8b40 in \_ZN18CPDF\_ImageRenderer5StartEP17CPDF\_RenderStatusPK15CPDF\_PageObjectPK10CFX\_Matrixii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:507  

#20 0x26c3133 in \_ZN17CPDF\_RenderStatus20ContinueSingleObjectEPK15CPDF\_PageObjectPK10CFX\_MatrixP9IFX\_Pause ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:297 (discriminator 1)  

#21 0x26cf72a in \_ZN24CPDF\_ProgressiveRenderer8ContinueEP9IFX\_Pause ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1057 (discriminator 1)  

#22 0x26cde4a in \_ZN24CPDF\_ProgressiveRenderer5StartEP9IFX\_Pause ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1018  

#23 0x247fe65 in \_Z22FPDF\_RenderPage\_RetailP14CRenderContextPviiiiiiiP19IFSDK\_PAUSE\_Adapter ./out/asan/../../fpdfsdk/fpdfview.cpp:885  

#24 0x247ec70 in FPDF\_RenderPageBitmap ./out/asan/../../fpdfsdk/fpdfview.cpp:621  

#25 0x50663b in *Z10RenderPageRKNSt3\_\_112basic\_stringIcNS\_11char\_traitsIcEENS\_9allocatorIcEEEERKPvSA\_iRK7OptionsS7* ./out/asan/../../samples/pdfium\_test.cc:551  

#26 0x508f7c in *Z9RenderPdfRKNSt3\_\_112basic\_stringIcNS\_11char\_traitsIcEENS\_9allocatorIcEEEEPKcmRK7OptionsS7* ./out/asan/../../samples/pdfium\_test.cc:735  

#27 0x50bd49 in main ./out/asan/../../samples/pdfium\_test.cc:875 (discriminator 1)  

#28 0x7f29895c082f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

0x60200000dc91 is located 0 bytes to the right of 1-byte region [0x60200000dc90,0x60200000dc91)  

allocated by thread T0 here:  

#0 0x4c105c in \_\_interceptor\_malloc ??:?  

#1 0x6f9248 in opj\_tcd\_init\_tile ./out/asan/../../third\_party/libopenjpeg20/tcd.c:947  

#2 0x6fa963 in opj\_tcd\_init\_decode\_tile ./out/asan/../../third\_party/libopenjpeg20/tcd.c:1056  

#3 0x64a3b5 in opj\_j2k\_read\_tile\_header ./out/asan/../../third\_party/libopenjpeg20/j2k.c:8020  

#4 0x67c55d in opj\_j2k\_decode\_tiles ./out/asan/../../third\_party/libopenjpeg20/j2k.c:9582  

#5 0x64559d in opj\_j2k\_exec ./out/asan/../../third\_party/libopenjpeg20/j2k.c:7290 (discriminator 1)  

#6 0x65868e in opj\_j2k\_decode ./out/asan/../../third\_party/libopenjpeg20/j2k.c:9810  

#7 0x690b9e in opj\_jp2\_decode ./out/asan/../../third\_party/libopenjpeg20/jp2.c:1488  

#8 0x6ad856 in opj\_decode ./out/asan/../../third\_party/libopenjpeg20/openjpeg.c:412  

#9 0x2986c7e in \_ZN12CJPX\_Decoder4InitEPKhj ./out/asan/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764  

#10 0x298a7c3 in \_ZN16CCodec\_JpxModule13CreateDecoderEPKhjP15CPDF\_ColorSpace ./out/asan/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:887 (discriminator 4)  

#11 0x2712799 in \_ZN14CPDF\_DIBSource13LoadJpxBitmapEv ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:634 (discriminator 1)  

#12 0x2707709 in \_ZN14CPDF\_DIBSource13CreateDecoderEv ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:593  

#13 0x270d492 in \_ZN14CPDF\_DIBSource18StartLoadDIBSourceEP13CPDF\_DocumentPK11CPDF\_StreamiP15CPDF\_DictionaryS6\_iji ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:311  

#14 0x26e10b8 in \_ZN20CPDF\_ImageCacheEntry20StartGetCachedBitmapEP15CPDF\_DictionaryS1\_ijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:282  

#15 0x26e0a94 in \_ZN20CPDF\_PageRenderCache20StartGetCachedBitmapEP11CPDF\_StreamijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131  

#16 0x27210e8 in \_ZN22CPDF\_ImageLoaderHandle5StartEP16CPDF\_ImageLoaderPK16CPDF\_ImageObjectP20CPDF\_PageRenderCacheijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1502 (discriminator 1)  

#17 0x27223ee in \_ZN16CPDF\_ImageLoader5StartEPK16CPDF\_ImageObjectP20CPDF\_PageRenderCachePNSt3\_\_110unique\_ptrI22CPDF\_ImageLoaderHandleNS5\_14default\_deleteIS7\_EEEEijiP17CPDF\_RenderStatusii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1565  

#18 0x26f1053 in \_ZN18CPDF\_ImageRenderer18StartLoadDIBSourceEv ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:360  

#19 0x26e8b40 in \_ZN18CPDF\_ImageRenderer5StartEP17CPDF\_RenderStatusPK15CPDF\_PageObjectPK10CFX\_Matrixii ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:507  

#20 0x26c3133 in \_ZN17CPDF\_RenderStatus20ContinueSingleObjectEPK15CPDF\_PageObjectPK10CFX\_MatrixP9IFX\_Pause ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:297 (discriminator 1)  

#21 0x26cf72a in \_ZN24CPDF\_ProgressiveRenderer8ContinueEP9IFX\_Pause ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1057 (discriminator 1)  

#22 0x26cde4a in \_ZN24CPDF\_ProgressiveRenderer5StartEP9IFX\_Pause ./out/asan/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1018  

#23 0x247fe65 in \_Z22FPDF\_RenderPage\_RetailP14CRenderContextPviiiiiiiP19IFSDK\_PAUSE\_Adapter ./out/asan/../../fpdfsdk/fpdfview.cpp:885  

#24 0x247ec70 in FPDF\_RenderPageBitmap ./out/asan/../../fpdfsdk/fpdfview.cpp:621  

#25 0x50663b in *Z10RenderPageRKNSt3\_\_112basic\_stringIcNS\_11char\_traitsIcEENS\_9allocatorIcEEEERKPvSA\_iRK7OptionsS7* ./out/asan/../../samples/pdfium\_test.cc:551  

#26 0x508f7c in *Z9RenderPdfRKNSt3\_\_112basic\_stringIcNS\_11char\_traitsIcEENS\_9allocatorIcEEEEPKcmRK7OptionsS7* ./out/asan/../../samples/pdfium\_test.cc:735  

#27 0x50bd49 in main ./out/asan/../../samples/pdfium\_test.cc:875 (discriminator 1)  

#28 0x7f29895c082f in \_\_libc\_start\_main /build/glibc-GKVZIf/glibc-2.23/csu/../csu/libc-start.c:291

SUMMARY: AddressSanitizer: heap-buffer-overflow (/dd/pdfium/pdfium/out/asan/pdfium\_test+0x702fa3)  

Shadow bytes around the buggy address:  

0x0c047fff9b40: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9b50: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9b60: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9b70: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c047fff9b80: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c047fff9b90: fa fa[01]fa fa fa 00 fa fa fa 00 04 fa fa 03 fa  

0x0c047fff9ba0: fa fa 03 fa fa fa 00 04 fa fa 00 04 fa fa 00 00  

0x0c047fff9bb0: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00  

0x0c047fff9bc0: fa fa fd fd fa fa 00 00 fa fa 00 00 fa fa 04 fa  

0x0c047fff9bd0: fa fa 04 fa fa fa fd fa fa fa 01 fa fa fa 00 fa  

0x0c047fff9be0: fa fa 00 00 fa fa 00 00 fa fa fd fa fa fa fd fa  

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

==4828==ABORTING

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 2.3 KB)

## Timeline

### [Deleted User] (2016-07-16)

typo mistake.
`line 842` => `line 942`


File libopenjpeg20/tcd.c, line 942:
--------------------------------------------------------------------------------
689	OPJ_UINT32 l_nb_code_blocks_size;
	...
942		l_nb_code_blocks = l_current_precinct->cw * l_current_precinct->ch;
943		
944		l_nb_code_blocks_size = l_nb_code_blocks * (OPJ_UINT32)sizeof_block;
945		
946		if (! l_current_precinct->cblks.blocks) {
947			l_current_precinct->cblks.blocks = opj_malloc(l_nb_code_blocks_size);
--------------------------------------------------------------------------------



### ta...@google.com (2016-07-18)

Thank you gogil. I'm confirming this bug with clusterfuzz (https://cluster-fuzz.appspot.com/testcase?key=6379260017377280)

### cl...@chromium.org (2016-07-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=4658093640384512

### ta...@google.com (2016-07-18)

I can confirm the heap-buffer-overflow crash on ubuntu. hong_zhang@, this looks related to 628304. Can you take a look? Thanks!

[Monorail components: Infra>Client>Pdfium]

### mb...@chromium.org (2016-07-18)

[Empty comment from Monorail migration]

[Monorail components: -Infra>Client>Pdfium Internals>Plugins>PDF]

### [Deleted User] (2016-07-19)

* Fix Suggestion
I refer to #625541

File libopenjpeg20/tcd.c, line 939:
--------------------------------------------------------------------------------
		l_current_precinct->cw = (OPJ_UINT32)((brcblkxend - tlcblkxstart) >> cblkwidthexpn);
		l_current_precinct->ch = (OPJ_UINT32)((brcblkyend - tlcblkystart) >> cblkheightexpn);

+		if (l_current_precinct->cw && ((OPJ_UINT32)-1) / l_current_precinct->cw < l_current_precinct->ch) {
+			return OPJ_FALSE;
+		}
		l_nb_code_blocks = l_current_precinct->cw * l_current_precinct->ch;
		/*fprintf(stderr, "\t\t\t\t precinct_cw = %d x recinct_ch = %d\n",l_current_precinct->cw, l_current_precinct->ch);      */

+		if (((OPJ_UINT32)-1) / (OPJ_UINT32)sizeof_block < l_nb_code_blocks) {
+			return OPJ_FALSE;
+		}
		l_nb_code_blocks_size = l_nb_code_blocks * (OPJ_UINT32)sizeof_block;

		if (! l_current_precinct->cblks.blocks) {
			l_current_precinct->cblks.blocks = opj_malloc(l_nb_code_blocks_size);
--------------------------------------------------------------------------------


### sh...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-31)

hong_zhang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2016-08-04)

Review URL: https://codereview.chromium.org/2212973002

### th...@chromium.org (2016-08-04)

Thanks for the patch! I'll let ochang@ take care of it.

### bu...@chromium.org (2016-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2b7d329e0a69e97cd3dc2bf267fb96e40a7880a4

commit 2b7d329e0a69e97cd3dc2bf267fb96e40a7880a4
Author: thestig <thestig@chromium.org>
Date: Fri Aug 05 22:06:00 2016

Roll PDFium 32e693f..135b998

https://pdfium.googlesource.com/pdfium.git/+log/32e693f..135b998

BUG=628304,628890
TBR=tsepez@chromium.org

Review-Url: https://codereview.chromium.org/2223573002
Cr-Commit-Position: refs/heads/master@{#410182}

[modify] https://crrev.com/2b7d329e0a69e97cd3dc2bf267fb96e40a7880a4/DEPS


### th...@chromium.org (2016-08-05)

Do we actually want to merge back to M53? M52?

### sh...@chromium.org (2016-08-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-08-08)

[Empty comment from Monorail migration]

### di...@chromium.org (2016-08-08)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### go...@chromium.org (2016-08-08)

+awhalley@, is this good to take in for this week M53 Beta release?

### aw...@chromium.org (2016-08-09)

Yep, good for M53, along with the other bugs bugs that have a PDFium roll: 624514, 628304, 628890

### go...@chromium.org (2016-08-09)

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/628890#c19. Please merge ASAP (latest by tomorrow, Tuesday 3:00 PM PT) so we can take it in for this week beta release.

### aw...@chromium.org (2016-08-09)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/205c3faca7f4c678fddf6e3811ec6fe9b0fd7031

commit 205c3faca7f4c678fddf6e3811ec6fe9b0fd7031
Author: Oliver Chang <ochang@google.com>
Date: Tue Aug 09 16:01:16 2016


### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

Congrats, $3,500 for this report.  Cheers!

### aw...@chromium.org (2016-09-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-10-28)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-11-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/628890?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084863)*
