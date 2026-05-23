# Security: Heap Buffer Overflow in opj_j2k_read_SQcd_SQcc

| Field | Value |
|-------|-------|
| **Issue ID** | [40084556](https://issues.chromium.org/issues/40084556) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | st...@gmail.com |
| **Assignee** | oc...@chromium.org |
| **Created** | 2016-06-12 |
| **Bounty** | $3,500.00 |

## Description

Security: PDFium: Heap Buffer Overflow in opj\_j2k\_read\_SQcd\_SQcc

**VULNERABILITY DETAILS**  

This heap-buffer-overflow vulnerability was caused by the malformed jpeg2000 image file embedded in the PDF document.  

The latest stable version of Chrome (51.0.2704.84 m) is vulnerable to this issue.

---

## AddressSanitizer Information

==4050==ERROR: AddressSanitizer: heap-buffer-overflow on address 0xb6103668 at pc 0x0870a663 bp 0xbfd642b8 sp 0xbfd642b0  

WRITE of size 4 at 0xb6103668 thread T0  

#0 0x870a662 in opj\_j2k\_read\_SQcd\_SQcc out/Release/../../third\_party/libopenjpeg20/j2k.c:9027:9  

#1 0x8700ae0 in opj\_j2k\_read\_qcd out/Release/../../third\_party/libopenjpeg20/j2k.c:2803:15  

#2 0x870c988 in opj\_j2k\_read\_header\_procedure out/Release/../../third\_party/libopenjpeg20/j2k.c:7217:26  

#3 0x86d940f in opj\_j2k\_exec out/Release/../../third\_party/libopenjpeg20/j2k.c:7290:43  

#4 0x86d940f in opj\_j2k\_read\_header out/Release/../../third\_party/libopenjpeg20/j2k.c:6768  

#5 0x8716371 in opj\_jp2\_read\_header out/Release/../../third\_party/libopenjpeg20/jp2.c:2653:9  

#6 0x86cc3bf in opj\_read\_header out/Release/../../third\_party/libopenjpeg20/openjpeg.c:391:10  

#7 0x8549539 in CJPX\_Decoder::Init(unsigned char const\*, unsigned int) out/Release/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:751:8  

#8 0x854bcb9 in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, CPDF\_ColorSpace\*) out/Release/../../core/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:887:10  

#9 0x83fc272 in CPDF\_DIBSource::LoadJpxBitmap() out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:634:24  

#10 0x83f2a1e in CPDF\_DIBSource::CreateDecoder() out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:593:5  

#11 0x83f72e1 in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:311:13  

#12 0x83d984d in CPDF\_ImageCacheEntry::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:274:25  

#13 0x83d984d in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:124  

#14 0x84078a4 in CPDF\_ImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1502:11  

#15 0x840887a in CPDF\_ImageLoader::Start(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, CPDF\_ImageLoaderHandle\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1563:10  

#16 0x83e4409 in CPDF\_ImageRenderer::StartLoadDIBSource() out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:351:7  

#17 0x83df008 in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:496:7  

#18 0x83c3e8b in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:284:10  

#19 0x83cfcec in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:1038:13  

#20 0x83ced7a in CPDF\_ProgressiveRenderer::Start(IFX\_Pause\*) out/Release/../../core/fpdfapi/fpdf\_render/fpdf\_render.cpp:999:3  

#21 0x815b491 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) out/Release/../../fpdfsdk/fpdfview.cpp:870:3  

#22 0x815ab11 in FPDF\_RenderPageBitmap out/Release/../../fpdfsdk/fpdfview.cpp:606:3  

#23 0x813f069 in RenderPage(std::string const&, void\* const&, void\* const&, int, Options const&, std::string const&) out/Release/../../samples/pdfium\_test.cc:514:5  

#24 0x8140cfb in RenderPdf(std::string const&, char const\*, unsigned int, Options const&, std::string const&) out/Release/../../samples/pdfium\_test.cc:694:9  

#25 0x8142d13 in main out/Release/../../samples/pdfium\_test.cc:835:5  

#26 0xb7496a82 in \_*libc\_start\_main /build/eglibc-617sU*/eglibc-2.19/csu/libc-start.c:287  

#27 0x807e5c3 in \_start (out/Release/pdfium\_test+0x807e5c3)

0xb6103668 is located 8 bytes to the left of 1-byte region [0xb6103670,0xb6103671)  

allocated by thread T0 here:  

#0 0x81163ff in calloc (out/Release/pdfium\_test+0x81163ff)  

#1 0x870228a in opj\_j2k\_read\_siz out/Release/../../third\_party/libopenjpeg20/j2k.c:2095:46  

#2 0x870c988 in opj\_j2k\_read\_header\_procedure out/Release/../../third\_party/libopenjpeg20/j2k.c:7217:26  

#3 0x86d940f in opj\_j2k\_exec out/Release/../../third\_party/libopenjpeg20/j2k.c:7290:43  

#4 0x86d940f in opj\_j2k\_read\_header out/Release/../../third\_party/libopenjpeg20/j2k.c:6768

SUMMARY: AddressSanitizer: heap-buffer-overflow out/Release/../../third\_party/libopenjpeg20/j2k.c:9027 opj\_j2k\_read\_SQcd\_SQcc  

Shadow bytes around the buggy address:  

0x36c20670: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x36c20680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x36c20690: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x36c206a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x36c206b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x36c206c0: fa fa fa fa fa fa 01 fa fa fa 01 fa fa[fa]01 fa  

0x36c206d0: fa fa 01 fa fa fa 04 fa fa fa 00 04 fa fa 00 04  

0x36c206e0: fa fa 00 04 fa fa 00 04 fa fa 00 fa fa fa fd fa  

0x36c206f0: fa fa 00 fa fa fa 04 fa fa fa 04 fa fa fa fd fa  

0x36c20700: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x36c20710: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

==4050==ABORTING

---

## Exception Information

(1d28.22c0): Access violation - code c0000005 (!!! second chance !!!)  

eax=00000000 ebx=003cd474 ecx=0973dff8 edx=003cd44b esi=09b2bc19 edi=09b26f28  

eip=0141a744 esp=003cd438 ebp=003cd444 iopl=0 nv up ei pl zr na pe nc  

cs=0023 ss=002b ds=002b es=002b fs=0053 gs=002b efl=00010246  

pdfium\_test!opj\_j2k\_read\_SQcd\_SQcc+0x74:  

0141a744 894118 mov dword ptr [ecx+18h],eax ds:002b:0973e010=????????

---

## Heap Information

0:000> !heap -p -a ecx  

address 0973dff8 found in  

\_DPH\_HEAP\_ROOT @ 171000  

in busy allocation ( DPH\_HEAP\_BLOCK: UserAddr UserSize - VirtAddr VirtSize)  

95f3ed4: 973dff8 1 - 973d000 2000  

10778e89 verifier!AVrfDebugPageHeapAllocate+0x00000229  

77621d4e ntdll!RtlDebugAllocateHeap+0x00000030  

775db586 ntdll!RtlpAllocateHeap+0x000000c4  

77583541 ntdll!RtlAllocateHeap+0x0000023a  

016c446c pdfium\_test!\_calloc\_base+0x00000047 [d:\th\minkernel\crts\ucrt\src\appcrt\heap\calloc\_base.cpp @ 33]  

01415edb pdfium\_test!opj\_j2k\_read\_siz+0x0000041b [third\_party\libopenjpeg20\j2k.c @ 2244]  

0141ac21 pdfium\_test!opj\_j2k\_read\_header\_procedure+0x000001d1 [third\_party\libopenjpeg20\j2k.c @ 7217]  

0141dd66 pdfium\_test!opj\_jp2\_exec+0x00000036 [third\_party\libopenjpeg20\jp2.c @ 2247]  

0141a9ff pdfium\_test!opj\_j2k\_read\_header+0x0000007f [third\_party\libopenjpeg20\j2k.c @ 6768]  

0141e18f pdfium\_test!opj\_jp2\_read\_header+0x0000005f [third\_party\libopenjpeg20\jp2.c @ 2653]  

0141580a pdfium\_test!opj\_read\_header+0x0000003a [third\_party\libopenjpeg20\openjpeg.c @ 391]  

013d747b pdfium\_test!CJPX\_Decoder::Init+0x0000013b [core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp @ 751]  

013d6e80 pdfium\_test!CCodec\_JpxModule::CreateDecoder+0x00000040 [core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp @ 887]  

013c4fb7 pdfium\_test!CPDF\_DIBSource::LoadJpxBitmap+0x00000067 [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 634]  

013c36ac pdfium\_test!CPDF\_DIBSource::CreateDecoder+0x0000023c [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 594]  

013c5bed pdfium\_test!CPDF\_DIBSource::StartLoadDIBSource+0x0000017d [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 311]  

013a1d57 pdfium\_test!CPDF\_ImageCacheEntry::StartGetCachedBitmap+0x00000067 [core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 277]  

013a1e5f pdfium\_test!CPDF\_PageRenderCache::StartGetCachedBitmap+0x000000cf [core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 124]  

013c59d4 pdfium\_test!CPDF\_ImageLoaderHandle::Start+0x00000044 [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1502]  

013c597d pdfium\_test!CPDF\_ImageLoader::Start+0x0000005d [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1563]  

013a8b40 pdfium\_test!CPDF\_ImageRenderer::StartLoadDIBSource+0x00000070 [core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 351]  

013a85c6 pdfium\_test!CPDF\_ImageRenderer::Start+0x00000076 [core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 496]  

0138c253 pdfium\_test!CPDF\_RenderStatus::ContinueSingleObject+0x000000c3 [core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 284]  

0138c064 pdfium\_test!CPDF\_ProgressiveRenderer::Continue+0x00000294 [core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 1038]  

0135ca2c pdfium\_test!FPDF\_RenderPage\_Retail+0x000001fc [fpdfsdk\fpdfview.cpp @ 871]  

0135d67f pdfium\_test!FPDF\_RenderPageBitmap+0x000000bf [fpdfsdk\fpdfview.cpp @ 609]  

01355689 pdfium\_test!RenderPage+0x000001b9 [samples\pdfium\_test.cc @ 516]  

01355b02 pdfium\_test!RenderPdf+0x00000302 [samples\pdfium\_test.cc @ 694]  

0135bb22 pdfium\_test!main+0x00000432 [samples\pdfium\_test.cc @ 836]  

016a8749 pdfium\_test!\_\_scrt\_common\_main\_seh+0x000000ff [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 264]  

7528338a kernel32!BaseThreadInitThunk+0x0000000e  

77589a02 ntdll!\_\_RtlUserThreadStart+0x00000070

---

## Overflow Information

static OPJ\_BOOL opj\_j2k\_read\_SQcd\_SQcc(opj\_j2k\_t \*p\_j2k,  

OPJ\_UINT32 p\_comp\_no,  

OPJ\_BYTE\* p\_header\_data,  

OPJ\_UINT32 \* p\_header\_size,  

opj\_event\_mgr\_t \* p\_manager  

)  

{  

/\* loop\*/  

OPJ\_UINT32 l\_band\_no;  

opj\_cp\_t \*l\_cp = 00;  

opj\_tcp\_t \*l\_tcp = 00;  

opj\_tccp\_t \*l\_tccp = 00;  

OPJ\_BYTE \* l\_current\_ptr = 00;  

OPJ\_UINT32 l\_tmp, l\_num\_band;

```
    /\* preconditions\*/  
    assert(p_j2k != 00);  
    assert(p_manager != 00);  
    assert(p_header_data != 00);  

    l_cp = &(p_j2k->m_cp);  
    /\* come from tile part header or main header ?\*/  
    l_tcp = (p_j2k->m_specific_param.m_decoder.m_state == J2K_STATE_TPH) ? /\*FIXME J2K_DEC_STATE_TPH\*/  
                            &l_cp->tcps[p_j2k->m_current_tile_number] :  
                            p_j2k->m_specific_param.m_decoder.m_default_tcp;  

    /\* precondition again\*/  
    assert(p_comp_no <  p_j2k->m_private_image->numcomps);  

    l_tccp = &l_tcp->tccps[p_comp_no];  
    l_current_ptr = p_header_data;  

    if (\*p_header_size < 1) {  
            opj_event_msg(p_manager, EVT_ERROR, "Error reading SQcd or SQcc element\n");  
            return OPJ_FALSE;  
    }  
    \*p_header_size -= 1;  

    opj_read_bytes(l_current_ptr, &l_tmp ,1);                       /\* Sqcx \*/  
    ++l_current_ptr;  

    l_tccp->qntsty = l_tmp & 0x1f;               // <------------------------------------------------ Heap Buffer Overflow!!!  
    l_tccp->numgbits = l_tmp >> 5;  
    if (l_tccp->qntsty == J2K_CCP_QNTSTY_SIQNT) {  
    l_num_band = 1;  
    }  

```

0:000> dv  

p\_j2k = <value unavailable>  

p\_comp\_no = <value unavailable>  

p\_header\_data = 0x09b2bc18 "@???"  

p\_header\_size = 0x003cd474  

p\_manager = 0x09b22fd4  

l\_tccp = 0x0973dff8 ; <----------------------------- Heap Buffer  

l\_tmp = 0x40  

l\_tcp = <value unavailable>  

l\_current\_ptr = 0x09b2bc19 "???"  

l\_num\_band = <value unavailable>  

l\_band\_no = <value unavailable>

---

## Stacktrace Information

0:000> k  

ChildEBP RetAddr  

003cd444 014163a9 pdfium\_test!opj\_j2k\_read\_SQcd\_SQcc+0x74 [third\_party\libopenjpeg20\j2k.c @ 9027]  

003cd464 0141ac21 pdfium\_test!opj\_j2k\_read\_qcd+0x19 [third\_party\libopenjpeg20\j2k.c @ 2803]  

003cd498 0141dd66 pdfium\_test!opj\_j2k\_read\_header\_procedure+0x1d1 [third\_party\libopenjpeg20\j2k.c @ 7217]  

003cd4b8 0141a9ff pdfium\_test!opj\_jp2\_exec+0x36 [third\_party\libopenjpeg20\jp2.c @ 2247]  

003cd4d8 0141e18f pdfium\_test!opj\_j2k\_read\_header+0x7f [third\_party\libopenjpeg20\j2k.c @ 6768]  

003cd4fc 0141580a pdfium\_test!opj\_jp2\_read\_header+0x5f [third\_party\libopenjpeg20\jp2.c @ 2653]  

003cd514 013d747b pdfium\_test!opj\_read\_header+0x3a [third\_party\libopenjpeg20\openjpeg.c @ 391]  

003cf57c 013d6e80 pdfium\_test!CJPX\_Decoder::Init+0x13b [core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp @ 751]  

003cf590 013c4fb7 pdfium\_test!CCodec\_JpxModule::CreateDecoder+0x40 [core\fxcodec\codec\fx\_codec\_jpx\_opj.cpp @ 887]  

003cf5d4 013c36ac pdfium\_test!CPDF\_DIBSource::LoadJpxBitmap+0x67 [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 634]  

003cf604 013c5bed pdfium\_test!CPDF\_DIBSource::CreateDecoder+0x23c [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 594]  

003cf628 013a1d57 pdfium\_test!CPDF\_DIBSource::StartLoadDIBSource+0x17d [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 311]  

003cf654 013a1e5f pdfium\_test!CPDF\_ImageCacheEntry::StartGetCachedBitmap+0x67 [core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 277]  

003cf688 013c59d4 pdfium\_test!CPDF\_PageRenderCache::StartGetCachedBitmap+0xcf [core\fpdfapi\fpdf\_render\fpdf\_render\_cache.cpp @ 124]  

003cf6b8 013c597d pdfium\_test!CPDF\_ImageLoaderHandle::Start+0x44 [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1502]  

003cf6e8 013a8b40 pdfium\_test!CPDF\_ImageLoader::Start+0x5d [core\fpdfapi\fpdf\_render\fpdf\_render\_loadimage.cpp @ 1563]  

003cf740 013a85c6 pdfium\_test!CPDF\_ImageRenderer::StartLoadDIBSource+0x70 [core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 351]  

003cf750 0138c253 pdfium\_test!CPDF\_ImageRenderer::Start+0x76 [core\fpdfapi\fpdf\_render\fpdf\_render\_image.cpp @ 496]  

003cf778 0138c064 pdfium\_test!CPDF\_RenderStatus::ContinueSingleObject+0xc3 [core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 284]  

003cf7cc 0135ca2c pdfium\_test!CPDF\_ProgressiveRenderer::Continue+0x294 [core\fpdfapi\fpdf\_render\fpdf\_render.cpp @ 1038]  

003cf808 0135d67f pdfium\_test!FPDF\_RenderPage\_Retail+0x1fc [fpdfsdk\fpdfview.cpp @ 871]  

003cf848 01355689 pdfium\_test!FPDF\_RenderPageBitmap+0xbf [fpdfsdk\fpdfview.cpp @ 609]  

003cf968 01355b02 pdfium\_test!RenderPage+0x1b9 [samples\pdfium\_test.cc @ 516]  

003cfa84 0135bb22 pdfium\_test!RenderPdf+0x302 [samples\pdfium\_test.cc @ 694]  

003cfbc0 016a8749 pdfium\_test!main+0x432 [samples\pdfium\_test.cc @ 836]  

(Inline) -------- pdfium\_test!invoke\_main+0x1d [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 74]  

003cfc0c 7528338a pdfium\_test!\_\_scrt\_common\_main\_seh+0xff [f:\dd\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 264]  

003cfc18 77589a02 kernel32!BaseThreadInitThunk+0xe  

003cfc58 775899d5 ntdll!\_\_RtlUserThreadStart+0x70  

003cfc70 00000000 ntdll!\_RtlUserThreadStart+0x1b

**VERSION**  

Chrome Version: [51.0.2704.84 m] + [Stable]  

Operating System: [Windows 7 SP1]

**REPRODUCTION CASE**  

Both the the malformed jpeg2000 image file, and the proof-of-concept PDF file were attached.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

## Attachments

- [poc.pdf](attachments/poc.pdf) (application/pdf, 1.1 KB)
- [poc.jp2](attachments/poc.jp2) (application/octet-stream, 159 B)
- [0016-read_SQcd_SQcc_overflow.patch](attachments/0016-read_SQcd_SQcc_overflow.patch) (application/octet-stream, 1.3 KB)

## Timeline

### st...@gmail.com (2016-06-12)

[Comment Deleted]

### st...@gmail.com (2016-06-12)

It seems the COD (0xFF52) component always comes before the QCD (0xFF5C) component. But this condition cannot be guaranteed. 

If the jpeg2000 image doesn't contain a COD component, as described in this issue, your check in function opj_j2k_read_SPCod_SPCoc will be bypassed.

Or if the QCD component comes before the COD component, your check will be bypassed too.

### st...@gmail.com (2016-06-13)

[Comment Deleted]

### st...@gmail.com (2016-06-13)

A simple patch for this issue.

### cl...@chromium.org (2016-06-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5685692965584896

### st...@gmail.com (2016-06-14)

Oh, why it takes so long to run ClusterFuzz? Can any one help me cc a PDFium member?

### cl...@chromium.org (2016-06-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5221940801568768

### es...@chromium.org (2016-06-15)

ochang, do you think you could please take a look at this? Also, I'm not sure why ClusterFuzz is taking so long to analyze and not setting labels.

[Monorail components: Internals>Plugins>PDF]

### es...@chromium.org (2016-06-15)

[Empty comment from Monorail migration]

### es...@chromium.org (2016-06-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-15)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-15)

[Empty comment from Monorail migration]

### oc...@chromium.org (2016-06-16)

stackexploit, feel free to upload a CL to codereview.chromium.org with your patch.

### st...@gmail.com (2016-06-16)

hi ochang, I've already submitted my patch to codereview.chromium.org, please take a look at it.
https://codereview.chromium.org/2071773002/

my first submission :)

### st...@gmail.com (2016-06-16)

oh, I forgot to update the README.pdfium file in libopenjpeg20 :(

### st...@gmail.com (2016-06-17)

The README.pdfium file has been updated.

### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium.git/+/338a6b75994eb148d429b7abccfffaf7ae9f9b55

commit 338a6b75994eb148d429b7abccfffaf7ae9f9b55
Author: stackexploit <stackexploit@gmail.com>
Date: Mon Jun 20 18:23:46 2016

openjpeg: Prevent a buffer overflow in opj_j2k_read_SQcd_SQcc.

BUG=chromium:619405

R=ochang@chromium.org

Review-Url: https://codereview.chromium.org/2071773002

[add] https://crrev.com/338a6b75994eb148d429b7abccfffaf7ae9f9b55/third_party/libopenjpeg20/0016-read_SQcd_SQcc_overflow.patch
[modify] https://crrev.com/338a6b75994eb148d429b7abccfffaf7ae9f9b55/third_party/libopenjpeg20/README.pdfium
[modify] https://crrev.com/338a6b75994eb148d429b7abccfffaf7ae9f9b55/third_party/libopenjpeg20/j2k.c


### bu...@chromium.org (2016-06-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f7014ec458435b22a73f4a085e50764444351ee9

commit f7014ec458435b22a73f4a085e50764444351ee9
Author: ochang <ochang@chromium.org>
Date: Mon Jun 20 22:18:54 2016

Roll PDFium 2fad11a..df6ec80

https://pdfium.googlesource.com/pdfium.git/+log/2fad11a..df6ec80

BUG=612918,619405,621094
TBR=thestig@chromium.org

Review-Url: https://codereview.chromium.org/2078383003
Cr-Commit-Position: refs/heads/master@{#400811}

[modify] https://crrev.com/f7014ec458435b22a73f4a085e50764444351ee9/DEPS


### oc...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-22)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@google.com (2016-06-22)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### ti...@google.com (2016-06-22)

[Automated comment] DEPS changes referenced in bugdroid comments, needs manual review.

### sh...@chromium.org (2016-06-22)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-06-22)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this applicable to all OS or any specific OS?

### oc...@chromium.org (2016-06-22)

This is applicable to all OSes. It's safe to merge.

### go...@chromium.org (2016-06-23)

Approving merge to M52 branch 2743 based on https://crbug.com/chromium/619405#c25. Please merge ASAP. Thank you.

awhalley@ as FYI

### bu...@chromium.org (2016-06-24)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=89063

------------------------------------------------------------------
r89063 | ochang@google.com | 2016-06-24T03:05:00.069831Z

-----------------------------------------------------------------

### oc...@chromium.org (2016-06-24)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

Congratulations!  $3,500 for this one (including $500 for the patch).

### st...@gmail.com (2016-07-14)

Thanks! Please use 'Ke Liu of Tencent's Xuanwu LAB' as the credit information when you're ready to release a newer version of Chrome.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-07-22)

M51 is done, removing merge request.

### aw...@chromium.org (2016-07-29)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-02)

[Empty comment from Monorail migration]

### st...@gmail.com (2016-08-23)

Hi, I'm going to write an essay about this issue and share it publicly.
Can you tell me when it is OK to do this please?

### aw...@chromium.org (2016-08-24)

Hi Ke. Thanks for checking!  Yes, you may publicly talk about this issue.

### sh...@chromium.org (2016-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/619405?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/620191]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084556)*
