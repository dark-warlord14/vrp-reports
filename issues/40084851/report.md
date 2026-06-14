# Security: heap-buffer-overflow in opj_v4dwt_interleave_h

| Field | Value |
|-------|-------|
| **Issue ID** | [40084851](https://issues.chromium.org/issues/40084851) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | [Deleted User] |
| **Assignee** | mo...@google.com |
| **Created** | 2016-07-14 |
| **Bounty** | $3,500.00 |

## Description

**VULNERABILITY DETAILS**

A heap buffer overflow vulnerability is present in the openjpeg.

This issue only affected 32-bit version of pdfium.

And can't be used with ASAN. because this vulnerability is using 3GB of memory.

When used with ASAN, It fails because it uses too much memory.

## File libopenjpeg20/dwt.c, line 841:

OPJ\_BOOL opj\_dwt\_decode\_real(opj\_tcd\_tilecomp\_t\* restrict tilec, OPJ\_UINT32 numres)  

{  

opj\_v4dwt\_t h;  

opj\_v4dwt\_t v;

```
opj_tcd_resolution_t\* res = tilec->resolutions;  

OPJ_UINT32 rw = (OPJ_UINT32)(res->x1 - res->x0);	/\* width of the resolution level computed \*/  
OPJ_UINT32 rh = (OPJ_UINT32)(res->y1 - res->y0);	/\* height of the resolution level computed \*/  

OPJ_UINT32 w = (OPJ_UINT32)(tilec->x1 - tilec->x0);  

h.wavelet = (opj_v4_t\*) opj_aligned_malloc((opj_dwt_max_resolution(res, numres)+5) \* sizeof(opj_v4_t));  

```

---

In my testcase, `opj_dwt_max_resolution(res, numres)` will return 0xFFFFFFB.

And `sizeof(obj_v4_t)` is 0x10.

Therefore, (0xFFFFFFB+5)\*0x10 will integer overflow.

opj\_aligned\_malloc will allocate memory with size 0.

The 64-bit version of pdfium is calculated correctly as 0x100000000.

This vulnerability cause an out of bounds write.

## File libopenjpeg20/dwt.c, line 624:

static void opj\_v4dwt\_interleave\_h(opj\_v4dwt\_t\* restrict w, OPJ\_FLOAT32\* restrict a, OPJ\_INT32 x, OPJ\_INT32 size){  

OPJ\_FLOAT32\* restrict bi = (OPJ\_FLOAT32\*) (w->wavelet + w->cas);  

OPJ\_INT32 count = w->sn;  

OPJ\_INT32 i, k;

```
for(k = 0; k < 2; ++k){  
	if ( count + 3 \* x < size && ((size_t) a & 0x0f) == 0 && ((size_t) bi & 0x0f) == 0 && (x & 0x0f) == 0 ) {  
		/\* Fast code path \*/  
		for(i = 0; i < count; ++i){  
			OPJ_INT32 j = i;  
			bi[i\*8    ] = a[j];    <--- out of bound write  
			j += x;  
			bi[i\*8 + 1] = a[j];  
			j += x;  
			bi[i\*8 + 2] = a[j];  
			j += x;  
			bi[i\*8 + 3] = a[j];  
		}  
	}  

```

---

**VERSION**  

Chrome Version: 51.0.2704.106 Stable x86  

Operating System: Windows 10 x64

**REPRODUCTION CASE**  

Attached as poc.pdf

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

(129c.1a8): Access violation - code c0000005 (first chance)  

First chance exceptions are reported before any exception handling.  

This exception may be expected and handled.  

No .natvis files found at C:\Program Files (x86)\Windows Kits\10\Debuggers\x86\Visualizers.  

eax=00000000 ebx=07fffffe ecx=5a705008 edx=7fffb020 esi=0ffffffb edi=0ffffffb  

eip=6acfac05 esp=0028c2cc ebp=0028c2f4 iopl=0 nv up ei ng nz ac po cy  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010293  

chrome\_child!opj\_v4dwt\_interleave\_h+0xc1:  

6acfac05 8941f8 mov dword ptr [ecx-8],eax ds:002b:5a705000=????????  

0:000> u  

chrome\_child!opj\_v4dwt\_interleave\_h+0xc1 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\dwt.c @ 647]:  

6acfac05 8941f8 mov dword ptr [ecx-8],eax  

6acfac08 8b45f8 mov eax,dword ptr [ebp-8]  

6acfac0b 03c7 add eax,edi  

6acfac0d 3bc6 cmp eax,esi  

6acfac0f 7d25 jge chrome\_child!opj\_v4dwt\_interleave\_h+0xf2 (6acfac36)  

6acfac11 8b45f4 mov eax,dword ptr [ebp-0Ch]  

6acfac14 8b00 mov eax,dword ptr [eax]  

6acfac16 8941fc mov dword ptr [ecx-4],eax  

0:000> dd ecx-8  

5a705000 ???????? ???????? ???????? ????????  

5a705010 ???????? ???????? ???????? ????????  

5a705020 ???????? ???????? ???????? ????????  

5a705030 ???????? ???????? ???????? ????????  

5a705040 ???????? ???????? ???????? ????????  

5a705050 ???????? ???????? ???????? ????????  

5a705060 ???????? ???????? ???????? ????????  

5a705070 ???????? ???????? ???????? ????????  

0:000> dd ecx-16  

5a704ff2 00385975 50005975 a0005a70 ????????  

5a705002 ???????? ???????? ???????? ????????  

5a705012 ???????? ???????? ???????? ????????  

5a705022 ???????? ???????? ???????? ????????  

5a705032 ???????? ???????? ???????? ????????  

5a705042 ???????? ???????? ???????? ????????  

5a705052 ???????? ???????? ???????? ????????  

5a705062 ???????? ???????? ???????? ????????  

0:000> lmvm chrome\_child  

Browse full module list  

start end module name  

69270000 6bfcd000 chrome\_child (private pdb symbols) c:\symbols\chrome\_child.dll.pdb\6D0E46FFC0C040548A49826AD955CA2C1\chrome\_child.dll.pdb  

Loaded symbol image file: C:\Program Files (x86)\Google\Chrome\Application\51.0.2704.106\chrome\_child.dll  

Image path: C:\Program Files (x86)\Google\Chrome\Application\51.0.2704.106\chrome\_child.dll  

Image name: chrome\_child.dll  

Browse all global symbols functions data  

Timestamp: Thu Jun 23 11:30:07 2016 (576B49AF)  

CheckSum: 02BDCB6D  

ImageSize: 02D5D000  

File version: 51.0.2704.106  

Product version: 51.0.2704.106  

File flags: 0 (Mask 17)  

File OS: 4 Unknown Win32  

File type: 1.0 App  

File date: 00000000.00000000  

Translations: 0409.04b0  

CompanyName: Google Inc.  

ProductName: Google Chrome  

InternalName: chrome\_dll  

OriginalFilename: chrome.dll  

ProductVersion: 51.0.2704.106  

FileVersion: 51.0.2704.106  

FileDescription: Google Chrome  

LegalCopyright: Copyright 2015 Google Inc. All rights reserved.

0:000> kb

# ChildEBP RetAddr Args to Child

00 0028c2f4 6acfa4c3 0028c328 7fffb020 0ffffffb chrome\_child!opj\_v4dwt\_interleave\_h+0xc1 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\dwt.c @ 647]  

01 0028c368 6acf8f7c 009d8628 00000001 0a769570 chrome\_child!opj\_dwt\_decode\_real+0x1a5 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\dwt.c @ 896]  

02 0028c388 6acf8ed7 009f4d14 009f32b0 0099a5c0 chrome\_child!opj\_tcd\_dwt\_decode+0x53 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\tcd.c @ 1635]  

03 0028c39c 6acf2cd5 000035b8 00a13010 000043c8 chrome\_child!opj\_tcd\_decode\_tile+0x7b [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\tcd.c @ 1317]  

04 0028c3cc 6acf2e5d 0099a5c0 00000000 e68b2020 chrome\_child!opj\_j2k\_decode\_tile+0x5e [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c @ 8069]  

05 0028c420 6acf3509 0099a5c0 00993018 009960fc chrome\_child!opj\_j2k\_decode\_tiles+0x8e [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c @ 9608]  

06 0028c440 6acf29b1 0099a5c0 00a0a138 00993018 chrome\_child!opj\_j2k\_exec+0x32 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c @ 7290]  

07 0028c474 6acf6a80 0099a5c0 00993018 009a13d0 chrome\_child!opj\_j2k\_decode+0x4e [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\j2k.c @ 9808]  

08 0028c494 6acefb06 0098d660 00993018 009a13d0 chrome\_child!opj\_jp2\_decode+0x24 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\jp2.c @ 1487]  

09 0028c4ac 6acc65bb 009960d0 00993018 009a13d0 chrome\_child!opj\_decode+0x26 [c:\b\build\slave\win\build\src\third\_party\pdfium\third\_party\libopenjpeg20\openjpeg.c @ 412]  

0a 0028e518 6acc609b 00a0a7c8 0000457b 6b833968 chrome\_child!CJPX\_Decoder::Init+0x183 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp @ 757]  

0b 0028e530 6acac323 00a0a7c8 0000457b 009dc390 chrome\_child!CCodec\_JpxModule::CreateDecoder+0x35 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp @ 880]  

0c 0028e578 6acaad48 009f09a8 009f0980 009cddd8 chrome\_child!CPDF\_DIBSource::LoadJpxBitmap+0x60 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 637]  

0d 0028e5a4 6acacd92 009cdca0 009a1760 009cdc98 chrome\_child!CPDF\_DIBSource::CreateDecoder+0x209 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 594]  

0e 0028e5c8 6aca0de9 00996070 009cddd8 00000001 chrome\_child!CPDF\_DIBSource::StartLoadDIBSource+0x15f [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 312]  

0f 0028e5f4 6aca0e93 00000000 009da920 00000000 chrome\_child!CPDF\_ImageCacheEntry::StartGetCachedBitmap+0x60 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 286]  

10 0028e630 6acacba8 009cddd8 00000000 00000000 chrome\_child!CPDF\_PageRenderCache::StartGetCachedBitmap+0x80 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 125]  

11 0028e660 6acacb5f 009636b8 00992f28 009cdc98 chrome\_child!CPDF\_ImageLoaderHandle::Start+0x44 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1519]  

12 0028e690 6ac995fe 00992f28 009cdc98 009636f4 chrome\_child!CPDF\_ImageLoader::Start+0x51 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1580]  

13 0028e6e8 6ac990a4 00992f28 009a9df8 009cdea4 chrome\_child!CPDF\_ImageRenderer::StartLoadDIBSource+0x70 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 343]  

14 0028e6fc 6ac7b0d6 009a9df8 00992f28 009cdea4 chrome\_child!CPDF\_ImageRenderer::Start+0x6b [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 487]  

15 0028e724 6ac7af52 00992f28 009cdea4 0028e818 chrome\_child!CPDF\_RenderStatus::ContinueSingleObject+0x91 [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 330]  

16 0028e7a4 6ac57601 0028e818 009dce18 009f2710 chrome\_child!CPDF\_ProgressiveRenderer::Continue+0x1dd [c:\b\build\slave\win\build\src\third\_party\pdfium\core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 1103]  

17 0028e7e0 6ac597c0 009f2710 00975390 00000004 chrome\_child!FPDF\_RenderPage\_Retail+0x206 [c:\b\build\slave\win\build\src\third\_party\pdfium\fpdfsdk\fpdfview.cpp @ 936]  

18 0028e824 6a4386c7 009a1610 00975390 00000004 chrome\_child!FPDF\_RenderPageBitmap\_Start+0xc5 [c:\b\build\slave\win\build\src\third\_party\pdfium\fpdfsdk\fpdf\_progressive.cpp @ 64]  

19 0028e884 6a43c63e 0000002f 000003cb 009cde00 chrome\_child!chrome\_pdf::PDFiumEngine::ContinuePaint+0xed [c:\b\build\slave\win\build\src\pdf\pdfium\pdfium\_engine.cc @ 2719]  

1a 0028e918 6a442c4d 0028e9e4 009cca48 0028e944 chrome\_child!chrome\_pdf::PDFiumEngine::Paint+0x159 [c:\b\build\slave\win\build\src\pdf\pdfium\pdfium\_engine.cc @ 958]  

1b 0028ea18 6a447a33 0028ead0 0028ea4c 0028ea58 chrome\_child!chrome\_pdf::OutOfProcessInstance::OnPaint+0x187 [c:\b\build\slave\win\build\src\pdf\out\_of\_process\_instance.cc @ 720]  

...

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 18.3 KB)

## Timeline

### mb...@chromium.org (2016-07-14)

hong_zhang: Could you take a look at this?

### mb...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### sh...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-15)

[Empty comment from Monorail migration]

### [Deleted User] (2016-07-19)

* Fix Suggestion
I refer to #625541

File libopenjpeg20/dwt.c, line 841:
-----------------------------------------------------------------------------------------------
OPJ_BOOL opj_dwt_decode_real(opj_tcd_tilecomp_t* restrict tilec, OPJ_UINT32 numres)
{
	opj_v4dwt_t h;
	opj_v4dwt_t v;

	opj_tcd_resolution_t* res = tilec->resolutions;

	OPJ_UINT32 rw = (OPJ_UINT32)(res->x1 - res->x0);	/* width of the resolution level computed */
	OPJ_UINT32 rh = (OPJ_UINT32)(res->y1 - res->y0);	/* height of the resolution level computed */

	OPJ_UINT32 w = (OPJ_UINT32)(tilec->x1 - tilec->x0);

+	OPJ_UINT32 mr = opj_dwt_max_resolution(res, numres);
+	if ((mr + 5) <= mr) {
+		return OPJ_FALSE;
+	}
+	mr += 5;
+	if (((OPJ_UINT32)-1) / (OPJ_UINT32)sizeof(opj_v4_t) < mr) {
+		return OPJ_FALSE;
+	}
+
+	h.wavelet = (opj_v4_t*) opj_aligned_malloc(mr * sizeof(opj_v4_t));
-	h.wavelet = (opj_v4_t*) opj_aligned_malloc((opj_dwt_max_resolution(res, numres)+5) * sizeof(opj_v4_t));
-----------------------------------------------------------------------------------------------

You will be able to verify this patch with the 32bit version of pdfium_test(no ASAN, Please use windbg or gdb)

But on Ubuntu, Sometimes it fails. Because it uses too much memory.

I recommend that you test on Win64.


### sh...@chromium.org (2016-07-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-29)

hong_zhang: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ts...@chromium.org (2016-07-29)

@ochang, if you're up for it, I'm concerned that there's so much of this all over the place that we ought to add opj_alligned_malloc_2d() and _3d() using logic along the lines of FX_AllocOrDie2D() and ensure that we never do any multiplications inside a malloc() call.

### [Deleted User] (2016-07-30)

That's a good point!

There is similar issue at r554172

openjpeg has several dangerous routine.


File libopenjpeg20/dwt.c, line 578:
-----------------------------------------------------------------------------------------------
	h.mem_count = opj_dwt_max_resolution(tr, numres);
	h.mem = (OPJ_INT32*)opj_aligned_malloc(h.mem_count * sizeof(OPJ_INT32));
-----------------------------------------------------------------------------------------------

File libopenjpeg20/t1.c, line 1185:
-----------------------------------------------------------------------------------------------
	t1->flags_stride=w+2;
	flagssize=t1->flags_stride * (h+2);

	if(flagssize > t1->flagssize){
		opj_aligned_free(t1->flags);
		t1->flags = (opj_flag_t*) opj_aligned_malloc(flagssize * sizeof(opj_flag_t));
-----------------------------------------------------------------------------------------------

File libopenjpeg20/jp2.c, line 972:
-----------------------------------------------------------------------------------------------
	nr_channels = color->jp2_pclr->nr_channels;

	old_comps = image->comps;
	new_comps = (opj_image_comp_t*)
			opj_malloc(nr_channels * sizeof(opj_image_comp_t));
-----------------------------------------------------------------------------------------------


### [Deleted User] (2016-07-30)

typo.

See crbug.com/554172

### [Deleted User] (2016-08-05)

Review URL: https://codereview.chromium.org/2218783002

### th...@chromium.org (2016-08-05)

Usually one hits "Publish+Mail Comments" on the code review to generate an email.

### [Deleted User] (2016-08-05)

Done!

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

Same here - do we actually want to merge back to M53? M52?


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

Approving merge to M53 branch 2785 based on https://crbug.com/chromium/628304#c20. Please merge ASAP (latest by tomorrow, Tuesday 3:00 PM PT) so we can take it in for this week beta release.

### go...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-08-09)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/chrome/tools/buildspec/+/205c3faca7f4c678fddf6e3811ec6fe9b0fd7031

commit 205c3faca7f4c678fddf6e3811ec6fe9b0fd7031
Author: Oliver Chang <ochang@google.com>
Date: Tue Aug 09 16:01:16 2016


### aw...@chromium.org (2016-08-09)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-30)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-09-08)

Nice - $3,500 for this one.

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

This issue was migrated from crbug.com/chromium/628304?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084851)*
