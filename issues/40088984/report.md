# Security: PDFium Out-Of-Bounds Read in CJPX_Decoder::Decode

| Field | Value |
|-------|-------|
| **Issue ID** | [40088984](https://issues.chromium.org/issues/40088984) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | rh...@chromium.org |
| **Created** | 2017-09-12 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS

ASAN Log, I'll post the details later.

==14613==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60200000ea71 at pc 0x0000009ab948 bp 0x7fffb29d2e40 sp 0x7fffb29d2e38
READ of size 1 at 0x60200000ea71 thread T0
    #0 0x9ab947 in CJPX_Decoder::Decode(unsigned char*, int, std::vector<unsigned char, std::allocator<unsigned char> > const&) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fxcodec/codec/fx_codec_jpx_opj.cpp:561:34
    #1 0x7a7a87 in CPDF_DIBSource::LoadJpxBitmap() /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_dibsource.cpp:689:8
    #2 0x79df2f in CPDF_DIBSource::CreateDecoder() /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_dibsource.cpp:511:5
    #3 0x7a2530 in CPDF_DIBSource::StartLoadDIBSource(CPDF_Document*, CPDF_Stream const*, bool, CPDF_Dictionary*, CPDF_Dictionary*, bool, unsigned int, bool) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_dibsource.cpp:289:13
    #4 0x89ebd7 in CPDF_ImageCacheEntry::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, bool, unsigned int, bool, CPDF_RenderStatus*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_imagecacheentry.cpp:71:13
    #5 0x7be8e4 in CPDF_PageRenderCache::StartGetCachedBitmap(CFX_RetainPtr<CPDF_Image> const&, bool, unsigned int, bool, CPDF_RenderStatus*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_pagerendercache.cpp:97:13
    #6 0x8bf32e in CPDF_ImageLoader::Start(CPDF_ImageObject const*, CPDF_PageRenderCache*, bool, unsigned int, bool, CPDF_RenderStatus*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_imageloader.cpp:34:11
    #7 0x8ac560 in CPDF_ImageRenderer::StartLoadDIBSource() /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_imagerenderer.cpp:62:7
    #8 0x8ac560 in CPDF_ImageRenderer::Start(CPDF_RenderStatus*, CPDF_ImageObject*, CFX_Matrix const*, bool, int) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_imagerenderer.cpp:181
    #9 0x7cd66c in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject*, CFX_Matrix const*, IFX_PauseIndicator*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_renderstatus.cpp:1132:8
    #10 0x7c2ee9 in CPDF_ProgressiveRenderer::Continue(IFX_PauseIndicator*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_progressiverenderer.cpp:93:13
    #11 0x7c1f94 in CPDF_ProgressiveRenderer::Start(IFX_PauseIndicator*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_progressiverenderer.cpp:44:3
    #12 0x532d1e in (anonymous namespace)::RenderPageImpl(CPDF_PageRenderContext*, CPDF_Page*, CFX_Matrix const&, FX_RECT const&, int, bool, IFSDK_PAUSE_Adapter*) /home/worker/Desktop/repo/pdfium/out/Release/../../fpdfsdk/fpdfview.cpp:128:3
    #13 0x5321dd in FPDF_RenderPage_Retail(CPDF_PageRenderContext*, void*, int, int, int, int, int, int, bool, IFSDK_PAUSE_Adapter*) /home/worker/Desktop/repo/pdfium/out/Release/../../fpdfsdk/fpdfview.cpp:1248:3
    #14 0x5209b5 in FPDF_RenderPageBitmap_Start /home/worker/Desktop/repo/pdfium/out/Release/../../fpdfsdk/fpdf_progressive.cpp:60:3
    #15 0x4f94c7 in (anonymous namespace)::RenderPage(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, void*, void*, (anonymous namespace)::FPDF_FORMFILLINFO_PDFiumTest*, int, (anonymous namespace)::Options const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /home/worker/Desktop/repo/pdfium/out/Release/../../samples/pdfium_test.cc:1273:16
    #16 0x4f94c7 in (anonymous namespace)::RenderPdf(std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, char const*, unsigned long, (anonymous namespace)::Options const&, std::__cxx11::basic_string<char, std::char_traits<char>, std::allocator<char> > const&) /home/worker/Desktop/repo/pdfium/out/Release/../../samples/pdfium_test.cc:1469
    #17 0x4f25d9 in main /home/worker/Desktop/repo/pdfium/out/Release/../../samples/pdfium_test.cc:1630:5
    #18 0x7f395a28282f in __libc_start_main /build/glibc-bfm8X4/glibc-2.23/csu/../csu/libc-start.c:291
    #19 0x41c978 in _start (/home/worker/Desktop/repo/pdfium/out/Release/pdfium_test+0x41c978)

0x60200000ea71 is located 0 bytes to the right of 1-byte region [0x60200000ea70,0x60200000ea71)
allocated by thread T0 here:
    #0 0x4eb0f0 in operator new(unsigned long) (/home/worker/Desktop/repo/pdfium/out/Release/pdfium_test+0x4eb0f0)
    #1 0x7a75c0 in __gnu_cxx::new_allocator<unsigned char>::allocate(unsigned long, void const*) /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/ext/new_allocator.h:104:27
    #2 0x7a75c0 in std::allocator_traits<std::allocator<unsigned char> >::allocate(std::allocator<unsigned char>&, unsigned long) /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/alloc_traits.h:491
    #3 0x7a75c0 in std::_Vector_base<unsigned char, std::allocator<unsigned char> >::_M_allocate(unsigned long) /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/stl_vector.h:170
    #4 0x7a75c0 in std::_Vector_base<unsigned char, std::allocator<unsigned char> >::_M_create_storage(unsigned long) /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/stl_vector.h:185
    #5 0x7a75c0 in std::_Vector_base<unsigned char, std::allocator<unsigned char> >::_Vector_base(unsigned long, std::allocator<unsigned char> const&) /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/stl_vector.h:136
    #6 0x7a75c0 in std::vector<unsigned char, std::allocator<unsigned char> >::vector(unsigned long, std::allocator<unsigned char> const&) /usr/bin/../lib/gcc/x86_64-linux-gnu/5.4.0/../../../../include/c++/5.4.0/bits/stl_vector.h:278
    #7 0x7a75c0 in CPDF_DIBSource::LoadJpxBitmap() /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_dibsource.cpp:682
    #8 0x79df2f in CPDF_DIBSource::CreateDecoder() /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_dibsource.cpp:511:5
    #9 0x7a2530 in CPDF_DIBSource::StartLoadDIBSource(CPDF_Document*, CPDF_Stream const*, bool, CPDF_Dictionary*, CPDF_Dictionary*, bool, unsigned int, bool) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_dibsource.cpp:289:13
    #10 0x89ebd7 in CPDF_ImageCacheEntry::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, bool, unsigned int, bool, CPDF_RenderStatus*) /home/worker/Desktop/repo/pdfium/out/Release/../../core/fpdfapi/render/cpdf_imagecacheentry.cpp:71:13

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/worker/Desktop/repo/pdfium/out/Release/../../core/fxcodec/codec/fx_codec_jpx_opj.cpp:561:34 in CJPX_Decoder::Decode(unsigned char*, int, std::vector<unsigned char, std::allocator<unsigned char> > const&)
Shadow bytes around the buggy address:
  0x0c047fff9cf0: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c047fff9d00: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c047fff9d10: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c047fff9d20: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c047fff9d30: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
=>0x0c047fff9d40: fa fa fd fa fa fa fd fa fa fa fd fd fa fa[01]fa
  0x0c047fff9d50: fa fa 00 fa fa fa fd fd fa fa fd fa fa fa fd fa
  0x0c047fff9d60: fa fa 00 04 fa fa 00 04 fa fa 00 00 fa fa 00 00
  0x0c047fff9d70: fa fa 00 00 fa fa 00 00 fa fa 00 00 fa fa 00 00
  0x0c047fff9d80: fa fa fd fd fa fa 00 00 fa fa fd fd fa fa fd fa
  0x0c047fff9d90: fa fa 01 fa fa fa 00 fa fa fa 00 00 fa fa 00 fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Heap right redzone:      fb
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack partial redzone:   f4
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
==14613==ABORTING

VERSION
Chrome Version: [x.x.x.x] + [stable, beta, or dev]
Operating System: [Please indicate OS, version, and service pack level]

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached
HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE
make the file as small as possible and remove any content not required to
demonstrate the bug.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace, registers, exception record]
Client ID (if relevant): [see link above]


## Attachments

- deleted (application/octet-stream, 0 B)
- [OOB-Write.txt](attachments/OOB-Write.txt) (text/plain, 4.6 KB)

## Timeline

### st...@gmail.com (2017-09-12)

In function CPDF_DIBSource::LoadJpxBitmap, the value of |components| was read from the |ihdr| box of the JP2 image file. Here the value was 1.

```
631  void CPDF_DIBSource::LoadJpxBitmap() {

639    uint32_t width = 0;
640    uint32_t height = 0;
641    uint32_t components = 0;
642    pJpxModule->GetImageInfo(context->decoder(), &width, &height, &components);

681    m_pCachedBitmap->Clear(0xFFFFFFFF);
682    std::vector<uint8_t> output_offsets(components);
```

The content of the |ihdr| box.

struct ihdr_box {
    uint32 size;        // 00 00 00 16
    uint32 flag;        // 69 68 64 72
    uint32 height;      // 00 00 01 D8
    uint32 width;       // 00 00 02 DF
    uint16 NC;          // 00 01, --> number of components
    uint8  BPC;         // 07
    uint8  C;           // 07
    uint8  Unk;         // 01
    uint8  IPR;         // 00
}

In this case, a vector with 1 element was created:
std::vector<uint8_t> output_offsets(components)

--------------------------------------------------------------

In function CJPX_Decoder::Decode, the value of |m_Image->numcomps| will be updated in function opj_decode. Here the value was updated in function opj_jp2_apply_pclr, we can see that the value was read from the |pclr| box.

```
1022  static OPJ_BOOL opj_jp2_apply_pclr(opj_image_t *image,
1023                                     opj_jp2_color_t *color,
1024                                     opj_event_mgr_t * p_manager)
1025  {

1035      channel_size = color->jp2_pclr->channel_size;
1036      channel_sign = color->jp2_pclr->channel_sign;
1037      entries = color->jp2_pclr->entries;
1038      cmap = color->jp2_pclr->cmap;
1039      nr_channels = color->jp2_pclr->nr_channels;

1147      image->comps = new_comps;
1148      image->numcomps = nr_channels;
1149  
1150      opj_jp2_free_pclr(color);
1151  
1152      return OPJ_TRUE;
1153  }/* apply_pclr() */
```

The content of the |pclr| box.

struct ihdr_box {
    uint32 size;        // 00 00 03 0E
    uint32 flag;        // 70 63 6C 72
    uint16 NE;          // 01 00
    uint8  NPC;         // 03, --> number of components
    // ......
}

Now, let's return to function CJPX_Decoder::Decode. OOB read can be triggered since the value of |m_Image->numcomps| was 3 but the size of |offsets| was 1.

```
506  bool CJPX_Decoder::Decode(uint8_t* dest_buf,
507                            int pitch,
508                            const std::vector<uint8_t>& offsets) {

525      if (!(opj_decode(m_Codec, m_Stream, m_Image) &&
526            opj_end_decompress(m_Codec, m_Stream))) {
527        opj_image_destroy(m_Image);
528        m_Image = nullptr;
529        return false;
530      }

558    std::vector<uint8_t*> channel_bufs(m_Image->numcomps);
559    std::vector<int> adjust_comps(m_Image->numcomps);
560    for (uint32_t i = 0; i < m_Image->numcomps; i++) {
561      channel_bufs[i] = dest_buf + offsets[i];           // --> OOB Read!!!
562      adjust_comps[i] = m_Image->comps[i].prec - 8;
563      if (i > 0) {
564        if (m_Image->comps[i].dx != m_Image->comps[i - 1].dx ||
565            m_Image->comps[i].dy != m_Image->comps[i - 1].dy ||
566            m_Image->comps[i].prec != m_Image->comps[i - 1].prec) {
567          return false;
568        }
569      }
570    }
```

### st...@gmail.com (2017-09-12)

GDB stacktrace.

(gdb) bt
#0  0x00007ffff7316428 in __GI_raise (sig=sig@entry=6) at ../sysdeps/unix/sysv/linux/raise.c:54
#1  0x00007ffff731802a in __GI_abort () at abort.c:89
#2  0x0000000000422c9a in (anonymous namespace)::(anonymous namespace)::PartitionCookieCheckValue
#3  0x0000000000422b1b in (anonymous namespace)::(anonymous namespace)::PartitionFreeWithPage 
#4  0x000000000043f152 in (anonymous namespace)::(anonymous namespace)::PartitionFree
#5  0x000000000043f0f0 in FX_Free (ptr=0xf5fa6c58010) at ../../core/fxcrt/fx_memory.h:116
#6  0x000000000043fc89 in FxFreeDeleter::operator()
#7  0x00000000008a6f91 in (anonymous namespace)::(anonymous namespace)::unique_ptr<unsigned char, FxFreeDeleter>::reset
#8  (anonymous namespace)::(anonymous namespace)::unique_ptr<unsigned char, FxFreeDeleter>::~unique_ptr
#9  CFX_MaybeOwned<unsigned char, FxFreeDeleter>::~CFX_MaybeOwned
#10 0x000000000089e381 in CFX_DIBitmap::~CFX_DIBitmap
#11 0x000000000089e3b9 in CFX_DIBitmap::~CFX_DIBitmap
#12 0x0000000000428f28 in CFX_Retainable::Release
#13 0x000000000042bb1c in ReleaseDeleter<CFX_DIBitmap>::operator()
#14 0x0000000000617f9c in (anonymous namespace)::(anonymous namespace)::unique_ptr<CFX_DIBitmap, ReleaseDeleter<CFX_DIBitmap> >::reset
#15 CFX_RetainPtr<CFX_DIBitmap>::Reset
#16 0x000000000060e8d9 in CPDF_DIBSource::~CPDF_DIBSource
#17 0x000000000060ebf9 in CPDF_DIBSource::~CPDF_DIBSource
#18 0x0000000000428f28 in CFX_Retainable::Release
#19 0x000000000044531c in ReleaseDeleter<CFX_DIBSource>::operator()
#20 0x00000000005679dc in (anonymous namespace)::(anonymous namespace)::unique_ptr<CFX_DIBSource, ReleaseDeleter<CFX_DIBSource> >::reset
#21 CFX_RetainPtr<CFX_DIBSource>::Reset
#22 0x0000000000699858 in CPDF_ImageCacheEntry::ContinueGetCachedBitmap
#23 0x00000000006996a5 in CPDF_ImageCacheEntry::StartGetCachedBitmap
#24 0x0000000000620574 in CPDF_PageRenderCache::StartGetCachedBitmap
#25 0x00000000006aaf9c in CPDF_ImageLoader::Start
#26 0x000000000069a09e in CPDF_ImageRenderer::StartLoadDIBSource
#27 0x000000000069cc8b in CPDF_ImageRenderer::Start
#28 0x000000000062cbda in CPDF_RenderStatus::ContinueSingleObject
#29 0x00000000006270e5 in CPDF_ProgressiveRenderer::Continue
#30 0x0000000000626620 in CPDF_ProgressiveRenderer::Start
#31 0x000000000044dc20 in (anonymous namespace)::RenderPageImpl
#32 0x000000000044c3bf in FPDF_RenderPage_Retail
#33 0x000000000042b2ff in FPDF_RenderPageBitmap_Start
#34 0x000000000040eb4b in (anonymous namespace)::RenderPage
#35 0x000000000040b6c3 in (anonymous namespace)::RenderPdf
#36 0x00000000004065cf in main (argc=2, argv=0x7fffffffde18)

### st...@gmail.com (2017-09-12)

Although the root cause was Out-Of-Bounds Read, it may lead to Out-Of-Bounds Write circumstance if we audit the code in function CJPX_Decoder::Decode carefully. This can be verified by the stacktrace information posted in #2

### st...@gmail.com (2017-09-12)

The stacktrace in #3 shows that the cookies were corrupted.

ALWAYS_INLINE void PartitionCookieCheckValue(void* ptr) {
#if DCHECK_IS_ON()
  unsigned char* cookie_ptr = reinterpret_cast<unsigned char*>(ptr);
  for (size_t i = 0; i < kCookieSize; ++i, ++cookie_ptr)
    DCHECK(*cookie_ptr == kCookieValue[i]);
#endif
}

### st...@gmail.com (2017-09-12)

5 0 obj
<<
    /BitsPerComponent 8
    /ColorSpace /DeviceGray    % DeviceGray -> m_pColorSpace->CountComponents() = 1
    /Filter [ /JPXDecode ]
    /Height 472
    /Length 143021
    /Subtype /Image
    /Type /XObject
    /Width 735
>>

In the pdf file we set /ColorSpace to /DeviceGray, which will set the value of m_pColorSpace->m_nComponents to 1. As a result, the ``if`` statement at line 648 will be bypassed.

```
631  void CPDF_DIBSource::LoadJpxBitmap() {
632    CCodec_JpxModule* pJpxModule = CPDF_ModuleMgr::Get()->GetJpxModule();
633    auto context = pdfium::MakeUnique<JpxBitMapContext>(pJpxModule);
634    context->set_decoder(pJpxModule->CreateDecoder(
635        m_pStreamAcc->GetData(), m_pStreamAcc->GetSize(), m_pColorSpace));
636    if (!context->decoder())
637      return;
638  
639    uint32_t width = 0;
640    uint32_t height = 0;
641    uint32_t components = 0;
642    pJpxModule->GetImageInfo(context->decoder(), &width, &height, &components);
643    if (static_cast<int>(width) < m_Width || static_cast<int>(height) < m_Height)
644      return;
645  
646    bool bSwapRGB = false;
647    if (m_pColorSpace) {
648      if (components != m_pColorSpace->CountComponents())    // --> bypass
649        return;
650  
```

If we set /ColorSpace to /DeviceRGB or /DeviceCMYK, the crash will not be reproducible since ``components != m_pColorSpace->CountComponents()``.

### el...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

[Monorail components: Internals>Plugins>PDF]

### th...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-09-12)

This is recent. From https://pdfium-review.googlesource.com/13550

### me...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### me...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### th...@chromium.org (2017-09-12)

[Empty comment from Monorail migration]

### st...@gmail.com (2017-09-13)

[Comment Deleted]

### st...@gmail.com (2017-09-13)

As described in https://crbug.com/chromium/764177#c2,#3,#4, this issue could lead to Out-Of-Bounds Write circumstances. And we can verify it by debugging the pdfium_test.exe process. The following log demonstrates that the memory behind the |dest_buf| was corrupted in function CJPX_Decoder::Decode.


bool CJPX_Decoder::Decode(uint8_t* dest_buf, int pitch, const std::vector<uint8_t>& offsets)

==============================
Windbg Debugging Log
==============================
0:000> bp pdfium_test_exe!CJPX_Decoder::Decode
0:000> g
Breakpoint 0 hit


0:000> p
0:000> p
0:000> p
0:000> p
0:000> p
eax=07e92fd8 ebx=07e1cf80 ecx=000002e0 edx=000001d8 esi=07e22fa8 edi=00d56ffc
eip=010a5e09 esp=001be050 ebp=001be0d4 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
pdfium_test_exe!CJPX_Decoder::Decode+0x4b:
010a5e09 83be4020000000  cmp     dword ptr [esi+2040h],0 ds:002b:07e24fe8=00000000


0:000> dd ebp+8 L4
001be0dc  25c58010 000002e0 001be11c 001be144


0:000> db 25c58010
25c58010  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58020  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58030  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58040  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58050  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58060  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58070  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25c58080  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................


0:000> db 25c58010+0x54d04-10
25cacd04  ff ff ff ff ff ff ff ff-ff ff ff ff 00 00 00 00  ................
25cacd14  de ad be ef ca fe d0 0d-13 37 f0 05 ba 11 ab 1e  .........7......
25cacd24  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd34  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd44  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd54  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd64  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd74  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................


0:000> ba w4 25cacd14


0:000> dv
           this = 0x07e22fa8
        offsets = 0x07e92fd8


0:000> db 0x07e92fd8
07e92fd8  00 00 00 00 00 00 00 00-df 02 00 00 d8 01 00 00  ................
07e92fe8  01 00 00 00 00 00 00 00-c8 4f e9 07 00 00 00 00  .........O......
07e92ff8  00 00 00 00 01 00 00 00-?? ?? ?? ?? ?? ?? ?? ??  ........????????


0:000> g
Breakpoint 1 hit
eax=000005c4 ebx=07e22fa8 ecx=25cac750 edx=000000ff esi=000001ec edi=000000ff
eip=010a6621 esp=001be050 ebp=001be0d4 iopl=0         nv up ei pl zr na pe nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000246
pdfium_test_exe!CJPX_Decoder::Decode+0x863:
010a6621 46              inc     esi


0:000> db 25cacd14
25cacd14  ff ad be ef ca fe d0 0d-13 37 f0 05 ba 11 ab 1e  .........7......
25cacd24  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd34  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd44  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd54  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd64  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd74  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................
25cacd84  00 00 00 00 00 00 00 00-00 00 00 00 00 00 00 00  ................


0:000> bc *


0:000> gu
eax=07e22f01 ebx=07e1cf80 ecx=3f3323b0 edx=00411078 esi=000002e0 edi=00d56ffc
eip=010a67bc esp=001be0e8 ebp=001be0e8 iopl=0         nv up ei pl nz na po nc
cs=0023  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00000202
pdfium_test_exe!CCodec_JpxModule::Decode+0x14:
010a67bc 5d              pop     ebp


0:000> db 25cacd14
25cacd14  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd24  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd34  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd44  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd54  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd64  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd74  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................
25cacd84  ff ff ff ff ff ff ff ff-ff ff ff ff ff ff ff ff  ................

### st...@gmail.com (2017-09-13)

Not sure why my comments in #12 & #13 were deleted automatically. So I put my comment in the attachment.

The thing I can to point out is that this issue could lead to Out-Of-Bounds Write circumstances. I'm wondering if this issue deserves a Security_Severity-High label. Thank you.

### sh...@chromium.org (2017-09-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rh...@chromium.org (2017-09-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-14)

The following revision refers to this bug:
  https://pdfium.googlesource.com/pdfium/+/3ad06a513bc490065b860a543ffb43eb169769bd

commit 3ad06a513bc490065b860a543ffb43eb169769bd
Author: Ryan Harrison <rharrison@chromium.org>
Date: Thu Sep 14 15:44:21 2017

Revert moving JPX library decode from Init to Decode

Due to some of the size parameters for allocating space in Decode()
depending on the values produced by opj_decode(), this change was
causing misallocation of space, which in turn was causing illegal
reads/writes.

The issue with excessive memory usage that the original CL was trying
to change is less significant than the above mentioned problems, so
reverting this fix and looking for another solution to the
problem. This will re-open bugs https://crbug.com/754423 and
https://crbug.com/761005.

BUG=chromium:764177,chromium:754423,chromium:761005

Change-Id: I1cafac8a8117ec1e3bc32b31196bdec719d46477
Reviewed-on: https://pdfium-review.googlesource.com/13950
Commit-Queue: Ryan Harrison <rharrison@chromium.org>
Reviewed-by: Henrique Nakashima <hnakashima@chromium.org>

[modify] https://crrev.com/3ad06a513bc490065b860a543ffb43eb169769bd/core/fxcodec/codec/fx_codec_jpx_opj.cpp


### rh...@chromium.org (2017-09-14)

[Empty comment from Monorail migration]

### bu...@chromium.org (2017-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d9eaae6913711672807d9ca1b36eaf717dade779

commit d9eaae6913711672807d9ca1b36eaf717dade779
Author: pdfium-deps-roller@chromium.org <pdfium-deps-roller@chromium.org>
Date: Thu Sep 14 17:02:20 2017

Roll src/third_party/pdfium/ 038740c2f..3ad06a513 (1 commit)

https://pdfium.googlesource.com/pdfium.git/+log/038740c2fbd2..3ad06a513bc4

$ git log 038740c2f..3ad06a513 --date=short --no-merges --format='%ad %ae %s'
2017-09-14 rharrison Revert moving JPX library decode from Init to Decode

Created with:
  roll-dep src/third_party/pdfium
BUG=764177,754423,761005


Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+/master/autoroll/README.md

If the roll is causing failures, see:
http://www.chromium.org/developers/tree-sheriffs/sheriff-details-chromium#TOC-Failures-due-to-DEPS-rolls


TBR=dsinclair@chromium.org

Change-Id: If61754f47a2144bf9770b3ced03db0f92c4ef288
Reviewed-on: https://chromium-review.googlesource.com/667497
Reviewed-by: <pdfium-deps-roller@chromium.org>
Commit-Queue: <pdfium-deps-roller@chromium.org>
Cr-Commit-Position: refs/heads/master@{#501969}
[modify] https://crrev.com/d9eaae6913711672807d9ca1b36eaf717dade779/DEPS


### sh...@chromium.org (2017-09-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-18)

[Empty comment from Monorail migration]

### mb...@google.com (2017-09-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2017-09-22)

Groovy! The VRP panel decided to award $3,000 for this report.  Thanks!

### aw...@chromium.org (2017-09-22)

[Empty comment from Monorail migration]

### aw...@chromium.org (2017-11-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2017-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2018-03-27)

[Empty comment from Monorail migration]

### is...@google.com (2018-03-27)

This issue was migrated from crbug.com/chromium/764177?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40088984)*
