# Negative-size-param in opj_t2_decode_packets

| Field | Value |
|-------|-------|
| **Issue ID** | [40080432](https://issues.chromium.org/issues/40080432) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Plugins>PDF |
| **Reporter** | cl...@gmail.com |
| **Assignee** | bo...@foxitsoftware.com |
| **Created** | 2014-09-11 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The following testcase crashes the 32 bit asan build of pdfium\_test (64 bit isn't affected).

The vulnerable code in t2.c:  

/\* Check if the cblk->data have allocated enough memory \*/  

if ((l\_cblk->data\_current\_size + l\_seg->newlen) > l\_cblk->data\_max\_size) {  

OPJ\_BYTE\* new\_cblk\_data = (OPJ\_BYTE\*) opj\_realloc(l\_cblk->data, l\_cblk->data\_current\_size + l\_seg->newlen);  

if(! new\_cblk\_data) {  

opj\_free(l\_cblk->data);  

l\_cblk->data\_max\_size = 0;  

/\* opj\_event\_msg(p\_manager, EVT\_ERROR, "Not enough memory to realloc code block cata!\n"); \*/  

return OPJ\_FALSE;  

}  

l\_cblk->data\_max\_size = l\_cblk->data\_current\_size + l\_seg->newlen;  

l\_cblk->data = new\_cblk\_data;  

}

```
                            memcpy(l_cblk->data + l_cblk->data_current_size, l_current_data, l_seg->newlen);  

```

This is likely due to an integer overflow in the check:  

(l\_cblk->data\_current\_size + l\_seg->newlen)

For large newlen the code will fail to allocate enough memory.

In 64-Bit build we get the following error:  

read: segment too long (1034683436) with max (2723) for codeblock 0 (p=0, b=0, r=4, c=0)

From the corresponding code here:  

if (l\_current\_data + l\_seg->newlen > p\_src\_data + p\_max\_length) {  

fprintf(stderr, "read: segment too long (%d) with max (%d) for codeblock %d (p=%d, b=%d, r=%d, c=%d)\n",  

l\_seg->newlen, p\_max\_length, cblkno, p\_pi->precno, bandno, p\_pi->resno, p\_pi->compno);  

return OPJ\_FALSE;

```
                            }  

```

In 32-bit builds this check fails as well.

ASAN output:

# ASAN:SIGSEGV

==12896==ERROR: AddressSanitizer: SEGV on unknown address 0x262783d3 (pc 0x08552637 sp 0xffa4ab60 bp 0xffa4acf8 T0)  

#0 0x8552636 in opj\_t2\_read\_packet\_data /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/t2.c:1170:0 #1 0x8552636 in opj\_t2\_decode\_packet /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/t2.c:525:0 #2 0x8552636 in opj\_t2\_decode\_packets /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/t2.c:399:0  

#3 0x84e2f71 in opj\_tcd\_t2\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1487:0 #4 0x84e2f71 in opj\_tcd\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/tcd.c:1230:0  

#5 0x84aea61 in opj\_j2k\_decode\_tile /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7661:0  

#6 0x84c256d in opj\_j2k\_decode\_tiles /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9177:0  

#7 0x84b41a7 in opj\_j2k\_exec /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:7048:0 #8 0x84b41a7 in opj\_j2k\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/j2k.c:9368:0  

#9 0x8371c26 in opj\_jp2\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/jp2.c:1332:0  

#10 0x836d2c1 in opj\_decode /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/fx\_libopenjpeg/src/../libopenjpeg20/openjpeg.c:413:0  

#11 0x836477b in CJPX\_Decoder::Init(unsigned char const\*, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:624:0  

#12 0x8365cbf in CCodec\_JpxModule::CreateDecoder(unsigned char const\*, unsigned int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fxcodec/codec/fx\_codec\_jpx\_opj.cpp:764:0  

#13 0x82bdcad in CPDF\_DIBSource::LoadJpxBitmap() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:643:0  

#14 0x82b9182 in CPDF\_DIBSource::CreateDecoder() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:599:0  

#15 0x82b4daf in CPDF\_DIBSource::StartLoadDIBSource(CPDF\_Document\*, CPDF\_Stream const\*, int, CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:335:0  

#16 0x82a20d5 in CPDF\_ImageCache::StartGetCachedBitmap(CPDF\_Dictionary\*, CPDF\_Dictionary\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:310:0  

#17 0x82a1cc8 in CPDF\_PageRenderCache::StartGetCachedBitmap(CPDF\_Stream\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_cache.cpp:131:0  

#18 0x82c6e45 in CPDF\_ProgressiveImageLoaderHandle::Start(CPDF\_ImageLoader\*, CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1489:0  

#19 0x82c7d67 in CPDF\_ImageLoader::StartLoadImage(CPDF\_ImageObject const\*, CPDF\_PageRenderCache\*, void\*&, int, unsigned int, int, CPDF\_RenderStatus\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_loadimage.cpp:1549:0  

#20 0x82a7f2d in CPDF\_ImageRenderer::StartLoadDIBSource() /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:371:0  

#21 0x82a3b9d in CPDF\_ImageRenderer::Start(CPDF\_RenderStatus\*, CPDF\_PageObject const\*, CFX\_Matrix const\*, int, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render\_image.cpp:525:0  

#22 0x8292901 in CPDF\_RenderStatus::ContinueSingleObject(CPDF\_PageObject const\*, CFX\_Matrix const\*, IFX\_Pause\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:350:0  

#23 0x829e7c4 in CPDF\_ProgressiveRenderer::Continue(IFX\_Pause\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1175:0  

#24 0x829d0cc in CPDF\_ProgressiveRenderer::Start(CPDF\_RenderContext\*, CFX\_RenderDevice\*, CPDF\_RenderOptions const\*, IFX\_Pause\*, int) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/core/src/fpdfapi/fpdf\_render/fpdf\_render.cpp:1114:0  

#25 0x80d9107 in FPDF\_RenderPage\_Retail(CRenderContext\*, void\*, int, int, int, int, int, int, int, IFSDK\_PAUSE\_Adapter\*) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:0  

#26 0x80d94f1 in FPDF\_RenderPageBitmap /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/fpdfsdk/src/fpdfview.cpp:574:0  

#27 0x80d5865 in RenderPdf(char const\*, char const\*, unsigned int, OutputFormat) /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:324:0  

#28 0x80d642f in main /home/bobthebuilder/chromium/src/out/Release/../../third\_party/pdfium/samples/pdfium\_test.cc:406:0  

#29 0xf7218a82 in \_\_libc\_start\_main ??:?  

#30 0x80d473d in \_start ??:0:0

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV ??:0 ??  

==12896==ABORTING  

**VERSION**  

Chrome Version: Trunk, 32-bit build

**REPRODUCTION CASE**  

Attached in repro.pdf

## Attachments

- [repro.pdf](attachments/repro.pdf) (application/pdf, 13.2 KB)

## Timeline

### ts...@chromium.org (2014-09-11)

Sorry, someone else beat you to it :(. 

### cl...@gmail.com (2014-09-11)

Aw ;( Could you please cc me into 407964? Thanks

### ts...@chromium.org (2014-09-11)

Done.

### cl...@gmail.com (2014-09-11)

Thanks!

Please see comment https://code.google.com/p/chromium/issues/detail?id=407964#c16 on why I think both issues are distinct.

### in...@chromium.org (2014-09-11)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-11)

[Empty comment from Monorail migration]

### ts...@chromium.org (2014-09-12)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-09-12)

I will take a look.

### cl...@chromium.org (2014-09-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-12)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6599271311736832

### cl...@chromium.org (2014-09-12)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=6215163695857664

### cl...@chromium.org (2014-09-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6215163695857664

Uploader: inferno@chromium.org
Job Type: Linux_asan_chrome_v8_arm

Crash Type: Negative-size-param
Crash Address: 
Crash State:
  opj_t2_decode_packets
  opj_tcd_decode_tile
  opj_j2k_decode_tile
  

Minimized Testcase (13.24 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95TYNtzxfr-Vo_IKpGMZ042ZrfJ0l9z7XtsNfSInq7WfNsrhAw1_-yV4zYGAkv-e31Zq6uPZIzan6aHRsZSFJdRN6NbrVnYV2CEWKCamcd0f2_X3F-v_VlzfOpFBRu_12IY0KfPQTnrkb6Ais0aGHKJonOgtA



### in...@chromium.org (2014-09-12)

Kostya, i didn't know Negative-size-param existed, so added a signature now. Is there any list of all the crash types, so that i can recheck if we are not missing anything.

### cl...@gmail.com (2014-09-12)

I never saw this before, what does the asan output look like?

### in...@chromium.org (2014-09-12)

=================================================================
==26189==ERROR: AddressSanitizer: negative-size-param: (size=1034683436)
    #0 0xe5d7c651 in __asan_memcpy
    #1 0xdbbe4802 in opj_t2_read_packet_data src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/t2.c:1170:33
    #2 0xdbbe0d9a in opj_t2_decode_packet src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/t2.c:525:23
    #3 0xdbbe063e in opj_t2_decode_packets src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/t2.c:399:39
    #4 0xdbb7d10f in opj_tcd_t2_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/tcd.c:1487:15
    #5 0xdbb7cf0e in opj_tcd_decode_tile src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/tcd.c:1230:15
    #6 0xdbb46765 in opj_j2k_decode_tile src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:7661:15
    #7 0xdbb5a157 in opj_j2k_decode_tiles src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:9177:23
    #8 0xdbb426a9 in opj_j2k_exec src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:7048:41
    #9 0xdbb4c40b in opj_j2k_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:9368:15
    #10 0xdba3e0a4 in opj_jp2_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/jp2.c:1332:8
    #11 0xdba396d3 in opj_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/openjpeg.c:413:10
    #12 0xdba3134c in CJPX_Decoder::Init(unsigned char const*, int) src/third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:624:15
    #13 0xdba32e46 in CCodec_JpxModule::CreateDecoder(unsigned char const*, unsigned int, int) src/third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:764:10
    #14 0xdb9bcb41 in CPDF_DIBSource::LoadJpxBitmap() src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:643:21
    #15 0xdb9b841e in CPDF_DIBSource::CreateDecoder() src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:599:9
    #16 0xdb9b4a21 in CPDF_DIBSource::StartLoadDIBSource(CPDF_Document*, CPDF_Stream const*, int, CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:335:15
    #17 0xdb9a5613 in CPDF_ImageCache::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:310:15
    #18 0xdb9a527d in CPDF_PageRenderCache::StartGetCachedBitmap(CPDF_Stream*, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:131:15
    #19 0xdb9c502b in CPDF_ProgressiveImageLoaderHandle::Start(CPDF_ImageLoader*, CPDF_ImageObject const*, CPDF_PageRenderCache*, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1489:15
    #20 0xdb9c5d53 in CPDF_ImageLoader::StartLoadImage(CPDF_ImageObject const*, CPDF_PageRenderCache*, void*&, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1549:19
    #21 0xdb9aaccc in CPDF_ImageRenderer::StartLoadDIBSource() src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_image.cpp:371:9
    #22 0xdb9a6f80 in CPDF_ImageRenderer::Start(CPDF_RenderStatus*, CPDF_PageObject const*, CFX_Matrix const*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_image.cpp:525:9
    #23 0xdb99b076 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject const*, CFX_Matrix const*, IFX_Pause*) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:350:14
    #24 0xdb9a2228 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:1175:21
    #25 0xdb9a1558 in CPDF_ProgressiveRenderer::Start(CPDF_RenderContext*, CFX_RenderDevice*, CPDF_RenderOptions const*, IFX_Pause*, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:1114:5
    #26 0xdb81da6b in FPDF_RenderPage_Retail(CRenderContext*, void*, int, int, int, int, int, int, int, IFSDK_PAUSE_Adapter*) src/third_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2
    #27 0xdb827bf0 in FPDF_RenderPageBitmap_Start src/third_party/pdfium/fpdfsdk/src/fpdf_progressive.cpp:52:2
    #28 0xdb7a654b in chrome_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData*) src/pdf/pdfium/pdfium_engine.cc:2398:10
    #29 0xdb7a51b8 in chrome_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*) src/pdf/pdfium/pdfium_engine.cc:729:11
    #30 0xdb74e4be in chrome_pdf::Instance::OnPaint(std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> > const&, std::__1::vector<PaintManager::ReadyRect, std::__1::allocator<PaintManager::ReadyRect> >*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*) src/pdf/instance.cc:804:7
    #31 0xdb750d61 in non-virtual thunk to chrome_pdf::Instance::OnPaint(std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> > const&, std::__1::vector<PaintManager::ReadyRect, std::__1::allocator<PaintManager::ReadyRect> >*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*) src/pdf/instance.cc:874:1
    #32 0xdb79104d in PaintManager::DoPaint() src/pdf/paint_manager.cc:201:3
    #33 0xdb793a2b in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::*)(int)>::operator()(PaintManager*, int) src/ppapi/utility/completion_callback_factory.h:605:9
    #34 0xdb7937f4 in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::*)(int)> >::Thunk(void*, int) src/ppapi/utility/completion_callback_factory.h:582:7
    #35 0xed250ccf in PP_RunCompletionCallback(PP_CompletionCallback*, int) src/ppapi/c/pp_completion_callback.h:240:3
    #36 0xed250be3 in void ppapi::CallWhileUnlocked<void, PP_CompletionCallback*, int, PP_CompletionCallback*, int>(void (*)(PP_CompletionCallback*, int), PP_CompletionCallback* const&, int const&) src/ppapi/shared_impl/proxy_lock.h:134:10
    #37 0xed250003 in ppapi::TrackedCallback::Run(int) src/ppapi/shared_impl/tracked_callback.cc:148:5
    #38 0xf0d95fc5 in ppapi::proxy::Graphics2DResource::OnPluginMsgFlushACK(ppapi::proxy::ResourceMessageReplyParams const&) src/ppapi/proxy/graphics_2d_resource.cc:147:3
    #39 0xf0d97a63 in base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>::Run(ppapi::proxy::Graphics2DResource*, ppapi::proxy::ResourceMessageReplyParams const&) src/base/bind_internal.h:190:12
    #40 0xf0d97927 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>, void (ppapi::proxy::Graphics2DResource* const&, ppapi::proxy::ResourceMessageReplyParams const&)>::MakeItSo(base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>, ppapi::proxy::Graphics2DResource* const&, ppapi::proxy::ResourceMessageReplyParams const&) src/base/bind_internal.h:898:5
    #41 0xf0d977ea in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>, void (ppapi::proxy::Graphics2DResource*, ppapi::proxy::ResourceMessageReplyParams const&), void (ppapi::proxy::Graphics2DResource*)>, void (ppapi::proxy::Graphics2DResource*, ppapi::proxy::ResourceMessageReplyParams const&)>::Run(base::internal::BindStateBase*, ppapi::proxy::ResourceMessageReplyParams const&) src/base/bind_internal.h:1219:12
    #42 0xf0ca7233 in base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>::Run(ppapi::proxy::ResourceMessageReplyParams const&) const src/base/callback.h:441:12
    #43 0xf0d96e73 in void ppapi::proxy::DispatchResourceReplyOrDefaultParams<PpapiPluginMsg_Graphics2D_FlushAck, void (base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>::*)(ppapi::proxy::ResourceMessageReplyParams const&) const>(base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>*, void (base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>::*)(ppapi::proxy::ResourceMessageReplyParams const&) const, ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) src/ppapi/proxy/dispatch_reply_message.h:129:3
    #44 0xf0d96c7b in ppapi::proxy::PluginResourceCallback<PpapiPluginMsg_Graphics2D_FlushAck, base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)> >::Run(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) src/ppapi/proxy/plugin_resource_callback.h:39:5
    #45 0xf0dd3c76 in ppapi::proxy::PluginResource::OnReplyReceived(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) src/ppapi/proxy/plugin_resource.cc:54:5
    #46 0xf1185d43 in content::PepperInProcessRouter::OnPluginMsgReceived(IPC::Message const&) src/content/renderer/pepper/pepper_in_process_router.cc:99:5
    #47 0xf1186768 in content::PepperInProcessRouter::DispatchPluginMsg(IPC::Message*) src/content/renderer/pepper/pepper_in_process_router.cc:164:18
    #48 0xf11872eb in base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>::Run(content::PepperInProcessRouter*, IPC::Message* const&) src/base/bind_internal.h:190:12
    #49 0xf118707f in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>, void (base::WeakPtr<content::PepperInProcessRouter> const&, IPC::Message*)>::MakeItSo(base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>, base::WeakPtr<content::PepperInProcessRouter> const&, IPC::Message*) src/base/bind_internal.h:909:5
    #50 0xf1186e78 in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>, void (content::PepperInProcessRouter*, IPC::Message*), void (base::WeakPtr<content::PepperInProcessRouter>, base::internal::OwnedWrapper<IPC::Message>)>, void (content::PepperInProcessRouter*, IPC::Message*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1248:12
    #51 0xe5e9cf22 in base::Callback<void ()>::Run() const src/base/callback.h:401:12
    #52 0xe73b437b in base::debug::TaskAnnotator::RunTask(char const*, char const*, base::PendingTask const&) src/base/debug/task_annotator.cc:62:3
    #53 0xe72ce72b in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:446:3
    #54 0xe72cefb7 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:456:5
    #55 0xe72cf649 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:565:13
    #56 0xe72dba64 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:32:21
    #57 0xe72cdf1e in base::MessageLoop::RunHandler() src/base/message_loop/message_loop.cc:415:3
    #58 0xe73115f4 in base::RunLoop::Run() src/base/run_loop.cc:49:3
    #59 0xe72cd0d6 in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:308:3
    #60 0xf102cf3c in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:230:7
    #61 0xe720b04e in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:344:14
    #62 0xe720c119 in content::RunNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:428:12
    #63 0xe720dd99 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:767:12
    #64 0xe720a39f in content::ContentMain(content::ContentMainParams const&) src/content/app/content_main.cc:19:15
    #65 0xe5db6b8b in ChromeMain src/chrome/app/chrome_main.cc:57:12
    #66 0xe3876904 in libc.so.6
0xd269b672 is located 1394 bytes inside of 4117-byte region [0xd269b100,0xd269c115)
allocated by thread T0 (chrome) here:
    #0 0xe5d97a11 in realloc
    #1 0xdbb45f38 in opj_j2k_read_sod src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:4338:40
    #2 0xdbb4452d in opj_j2k_read_tile_header src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:7551:31
    #3 0xdbb5a00e in opj_j2k_decode_tiles src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:9149:23
    #4 0xdbb426a9 in opj_j2k_exec src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:7048:41
    #5 0xdbb4c40b in opj_j2k_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/j2k.c:9368:15
    #6 0xdba3e0a4 in opj_jp2_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/jp2.c:1332:8
    #7 0xdba396d3 in opj_decode src/third_party/pdfium/core/src/fxcodec/fx_libopenjpeg/libopenjpeg20/openjpeg.c:413:10
    #8 0xdba3134c in CJPX_Decoder::Init(unsigned char const*, int) src/third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:624:15
    #9 0xdba32e46 in CCodec_JpxModule::CreateDecoder(unsigned char const*, unsigned int, int) src/third_party/pdfium/core/src/fxcodec/codec/fx_codec_jpx_opj.cpp:764:10
    #10 0xdb9bcb41 in CPDF_DIBSource::LoadJpxBitmap() src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:643:21
    #11 0xdb9b841e in CPDF_DIBSource::CreateDecoder() src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:599:9
    #12 0xdb9b4a21 in CPDF_DIBSource::StartLoadDIBSource(CPDF_Document*, CPDF_Stream const*, int, CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:335:15
    #13 0xdb9a5613 in CPDF_ImageCache::StartGetCachedBitmap(CPDF_Dictionary*, CPDF_Dictionary*, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:310:15
    #14 0xdb9a527d in CPDF_PageRenderCache::StartGetCachedBitmap(CPDF_Stream*, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_cache.cpp:131:15
    #15 0xdb9c502b in CPDF_ProgressiveImageLoaderHandle::Start(CPDF_ImageLoader*, CPDF_ImageObject const*, CPDF_PageRenderCache*, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1489:15
    #16 0xdb9c5d53 in CPDF_ImageLoader::StartLoadImage(CPDF_ImageObject const*, CPDF_PageRenderCache*, void*&, int, unsigned int, int, CPDF_RenderStatus*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_loadimage.cpp:1549:19
    #17 0xdb9aaccc in CPDF_ImageRenderer::StartLoadDIBSource() src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_image.cpp:371:9
    #18 0xdb9a6f80 in CPDF_ImageRenderer::Start(CPDF_RenderStatus*, CPDF_PageObject const*, CFX_Matrix const*, int, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render_image.cpp:525:9
    #19 0xdb99b076 in CPDF_RenderStatus::ContinueSingleObject(CPDF_PageObject const*, CFX_Matrix const*, IFX_Pause*) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:350:14
    #20 0xdb9a2228 in CPDF_ProgressiveRenderer::Continue(IFX_Pause*) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:1175:21
    #21 0xdb9a1558 in CPDF_ProgressiveRenderer::Start(CPDF_RenderContext*, CFX_RenderDevice*, CPDF_RenderOptions const*, IFX_Pause*, int) src/third_party/pdfium/core/src/fpdfapi/fpdf_render/fpdf_render.cpp:1114:5
    #22 0xdb81da6b in FPDF_RenderPage_Retail(CRenderContext*, void*, int, int, int, int, int, int, int, IFSDK_PAUSE_Adapter*) src/third_party/pdfium/fpdfsdk/src/fpdfview.cpp:772:2
    #23 0xdb827bf0 in FPDF_RenderPageBitmap_Start src/third_party/pdfium/fpdfsdk/src/fpdf_progressive.cpp:52:2
    #24 0xdb7a654b in chrome_pdf::PDFiumEngine::ContinuePaint(int, pp::ImageData*) src/pdf/pdfium/pdfium_engine.cc:2398:10
    #25 0xdb7a51b8 in chrome_pdf::PDFiumEngine::Paint(pp::Rect const&, pp::ImageData*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*) src/pdf/pdfium/pdfium_engine.cc:729:11
    #26 0xdb74e4be in chrome_pdf::Instance::OnPaint(std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> > const&, std::__1::vector<PaintManager::ReadyRect, std::__1::allocator<PaintManager::ReadyRect> >*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*) src/pdf/instance.cc:804:7
    #27 0xdb750d61 in non-virtual thunk to chrome_pdf::Instance::OnPaint(std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> > const&, std::__1::vector<PaintManager::ReadyRect, std::__1::allocator<PaintManager::ReadyRect> >*, std::__1::vector<pp::Rect, std::__1::allocator<pp::Rect> >*) src/pdf/instance.cc:874:1
    #28 0xdb79104d in PaintManager::DoPaint() src/pdf/paint_manager.cc:201:3
    #29 0xdb793a2b in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::*)(int)>::operator()(PaintManager*, int) src/ppapi/utility/completion_callback_factory.h:605:9
    #30 0xdb7937f4 in pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::CallbackData<pp::CompletionCallbackFactory<PaintManager, pp::ThreadSafeThreadTraits>::Dispatcher0<void (PaintManager::*)(int)> >::Thunk(void*, int) src/ppapi/utility/completion_callback_factory.h:582:7
    #31 0xed250ccf in PP_RunCompletionCallback(PP_CompletionCallback*, int) src/ppapi/c/pp_completion_callback.h:240:3
    #32 0xed250be3 in void ppapi::CallWhileUnlocked<void, PP_CompletionCallback*, int, PP_CompletionCallback*, int>(void (*)(PP_CompletionCallback*, int), PP_CompletionCallback* const&, int const&) src/ppapi/shared_impl/proxy_lock.h:134:10
    #33 0xed250003 in ppapi::TrackedCallback::Run(int) src/ppapi/shared_impl/tracked_callback.cc:148:5
    #34 0xf0d95fc5 in ppapi::proxy::Graphics2DResource::OnPluginMsgFlushACK(ppapi::proxy::ResourceMessageReplyParams const&) src/ppapi/proxy/graphics_2d_resource.cc:147:3
    #35 0xf0d97a63 in base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>::Run(ppapi::proxy::Graphics2DResource*, ppapi::proxy::ResourceMessageReplyParams const&) src/base/bind_internal.h:190:12
    #36 0xf0d97927 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>, void (ppapi::proxy::Graphics2DResource* const&, ppapi::proxy::ResourceMessageReplyParams const&)>::MakeItSo(base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>, ppapi::proxy::Graphics2DResource* const&, ppapi::proxy::ResourceMessageReplyParams const&) src/base/bind_internal.h:898:5
    #37 0xf0d977ea in base::internal::Invoker<1, base::internal::BindState<base::internal::RunnableAdapter<void (ppapi::proxy::Graphics2DResource::*)(ppapi::proxy::ResourceMessageReplyParams const&)>, void (ppapi::proxy::Graphics2DResource*, ppapi::proxy::ResourceMessageReplyParams const&), void (ppapi::proxy::Graphics2DResource*)>, void (ppapi::proxy::Graphics2DResource*, ppapi::proxy::ResourceMessageReplyParams const&)>::Run(base::internal::BindStateBase*, ppapi::proxy::ResourceMessageReplyParams const&) src/base/bind_internal.h:1219:12
    #38 0xf0ca7233 in base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>::Run(ppapi::proxy::ResourceMessageReplyParams const&) const src/base/callback.h:441:12
    #39 0xf0d96e73 in void ppapi::proxy::DispatchResourceReplyOrDefaultParams<PpapiPluginMsg_Graphics2D_FlushAck, void (base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>::*)(ppapi::proxy::ResourceMessageReplyParams const&) const>(base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>*, void (base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)>::*)(ppapi::proxy::ResourceMessageReplyParams const&) const, ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) src/ppapi/proxy/dispatch_reply_message.h:129:3
    #40 0xf0d96c7b in ppapi::proxy::PluginResourceCallback<PpapiPluginMsg_Graphics2D_FlushAck, base::Callback<void (ppapi::proxy::ResourceMessageReplyParams const&)> >::Run(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) src/ppapi/proxy/plugin_resource_callback.h:39:5
    #41 0xf0dd3c76 in ppapi::proxy::PluginResource::OnReplyReceived(ppapi::proxy::ResourceMessageReplyParams const&, IPC::Message const&) src/ppapi/proxy/plugin_resource.cc:54:5
    #42 0xf1185d43 in content::PepperInProcessRouter::OnPluginMsgReceived(IPC::Message const&) src/content/renderer/pepper/pepper_in_process_router.cc:99:5
    #43 0xf1186768 in content::PepperInProcessRouter::DispatchPluginMsg(IPC::Message*) src/content/renderer/pepper/pepper_in_process_router.cc:164:18
    #44 0xf11872eb in base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>::Run(content::PepperInProcessRouter*, IPC::Message* const&) src/base/bind_internal.h:190:12
    #45 0xf118707f in base::internal::InvokeHelper<true, void, base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>, void (base::WeakPtr<content::PepperInProcessRouter> const&, IPC::Message*)>::MakeItSo(base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>, base::WeakPtr<content::PepperInProcessRouter> const&, IPC::Message*) src/base/bind_internal.h:909:5
    #46 0xf1186e78 in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (content::PepperInProcessRouter::*)(IPC::Message*)>, void (content::PepperInProcessRouter*, IPC::Message*), void (base::WeakPtr<content::PepperInProcessRouter>, base::internal::OwnedWrapper<IPC::Message>)>, void (content::PepperInProcessRouter*, IPC::Message*)>::Run(base::internal::BindStateBase*) src/base/bind_internal.h:1248:12
    #47 0xe5e9cf22 in base::Callback<void ()>::Run() const src/base/callback.h:401:12
    #48 0xe73b437b in base::debug::TaskAnnotator::RunTask(char const*, char const*, base::PendingTask const&) src/base/debug/task_annotator.cc:62:3
    #49 0xe72ce72b in base::MessageLoop::RunTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:446:3
    #50 0xe72cefb7 in base::MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) src/base/message_loop/message_loop.cc:456:5
    #51 0xe72cf649 in base::MessageLoop::DoWork() src/base/message_loop/message_loop.cc:565:13
    #52 0xe72dba64 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) src/base/message_loop/message_pump_default.cc:32:21
    #53 0xe72cdf1e in base::MessageLoop::RunHandler() src/base/message_loop/message_loop.cc:415:3
    #54 0xe73115f4 in base::RunLoop::Run() src/base/run_loop.cc:49:3
    #55 0xe72cd0d6 in base::MessageLoop::Run() src/base/message_loop/message_loop.cc:308:3
    #56 0xf102cf3c in content::RendererMain(content::MainFunctionParams const&) src/content/renderer/renderer_main.cc:230:7
    #57 0xe720b04e in content::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:344:14
    #58 0xe720c119 in content::RunNamedProcessTypeMain(std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) src/content/app/content_main_runner.cc:428:12
    #59 0xe720dd99 in content::ContentMainRunnerImpl::Run() src/content/app/content_main_runner.cc:767:12
    #60 0xe720a39f in content::ContentMain(content::ContentMainParams const&) src/content/app/content_main.cc:19:15
    #61 0xe5db6b8b in ChromeMain src/chrome/app/chrome_main.cc:57:12
    #62 0xe3876904 in libc.so.6

SUMMARY: AddressSanitizer: negative-size-param ??:0 ??
==26189==ABORTING

### in...@chromium.org (2014-09-12)

ok generalizing and handing unknown signatures using https://github.com/llvm-mirror/compiler-rt/blob/master/lib/asan/asan_report.cc

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-16)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-09-17)

+cc Libopenjpeg devs.

Antonin, Mathieu - can you please take a look at these libopenjpeg high severity security vulnerabilities asap. Feel free to port them to libopenjpeg bug tracker provided you can restrict view them [should not be open to public].

### cl...@chromium.org (2014-09-19)

bo_xu@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-09-19)

+cc m.darbois

Bo, Jun, what is the easy way to extract the image bits from pdf. Can you please attach them to these 11 bugs.

### an...@gmail.com (2014-09-22)

This has been fixed by https://code.google.com/p/openjpeg/source/detail?r=2883 (19/09/2014).

OpenJPEG still fails to decode the image but at least it does so gracefully.

$ opj_decompress.exe -i ~/data/opj/issues/issue390/0.jp2 -o ~/data/opj/issues/issue390/0.png

[INFO] Start to read j2k main header (123).
[INFO] Main header has been correctly decoded.
[INFO] No decoded area parameters, set the decoded area to the whole image
[INFO] Header of tile 0 / 3 has been read.
read: segment too long (1034683436) with max (186) for codeblock 0 (p=0, b=0, r=4, c=0)
[ERROR] Failed to decode.
[ERROR] Failed to decode tile 1/4
[ERROR] Failed to decode the codestream in the JP2 file
ERROR -> opj_decompress: failed to decode image!

Note that Kakadu decodes sth ugly and issues a warning.

### in...@chromium.org (2014-09-22)

Bo, can you please uptake the openjpeg patch in pdfium.

Antonin, does this path fix any other bugs that we cced you on. is this for just this bug only ?

### bo...@foxitsoftware.com (2014-09-22)

I will put the fix into pdfium. Probably I should add antonin as a reviewer?

### in...@chromium.org (2014-09-22)

Sure that is fine.

### an...@gmail.com (2014-09-22)

@inferno: OpenJPEG r2883 added a lot of memory allocation checks.
issue407964 and issue413447 might have been solved as well but this need to be confirmed.
Other issues have been reproduced on latest openjpeg revision by Matthieu Darbois.

### bo...@foxitsoftware.com (2014-09-22)

@inferno, can you rerun this one again? I cannot reproduce it now. BTW, what is Linux_asan_chrome_v8_arm? 

### bo...@foxitsoftware.com (2014-09-22)

@antonin, I cannot see your email, can you add yourself as reviewer for the CL: https://codereview.chromium.org/589243004/

### in...@chromium.org (2014-09-22)

Clicked redo on report. Linux_asan_chrome_v8_arm  is 32-bit asan running on 64-bit machines. use builds from http://commondatastorage.googleapis.com/chromium-browser-asan/index.html?prefix=linux-release-v8-arm/. also, it needs specific asan_options - [Environment] ASAN_OPTIONS = alloc_dealloc_mismatch=0:strict_memcmp=0:redzone=128:malloc_context_size=128:handle_segv=1:symbolize=false:check_malloc_usable_size=0:fast_unwind_on_fatal=1:allocator_may_return_null=1:detect_stack_use_after_return=1:max_uar_stack_size_log=17

### bo...@foxitsoftware.com (2014-09-23)

@antonin, I added changes in r2883 but it still crashes in same location.

### bo...@foxitsoftware.com (2014-09-24)

@antonin, what is your email address? I'd like to add you to the code review for patches in pdfium, thanks!

### bo...@foxitsoftware.com (2014-09-24)

@antonin, also can you try the fix using pdfium_test? It's still crashing with ASan.

### an...@gmail.com (2014-09-25)

@bo_xu, i'm now able to see the review but not edit it (login failed). Anyway, I'm not sure to be the right guy to do that as I already validated this patch for openjpeg library, so I do not have any comment to do. If pdfium_test is still crashing, you should maybe upgrade to the latest version of OpenJPEG (2.1), a lot of bugs have been fixed in this version. You could even go up to 2883 as a few bugfixes have been added since 2.1. 

### ts...@chromium.org (2014-09-26)

@palmer - Now may be a good time to investigate mirroring the repository on pdfium.googlecode.com so that we can more easily roll between versions. Thoughts?

### bo...@foxitsoftware.com (2014-09-26)

@tsepez and palmer, what do you think to update openjpeg to the latest version?

### pa...@chromium.org (2014-09-26)

tsepez: You mean mirroring the OpenJPEG repository?

bo_xu: Yes, we should always track the latest stable version of all our dependencies.

### ts...@chromium.org (2014-09-26)

@palmer - Yes, and pull in a specific version via DEPS rather than merging into pdfium tree itself.

### bo...@foxitsoftware.com (2014-09-26)

@tsepez, currently the openjpeg code we used diverges from the openjpeg repository. Before pdfium open source, we had to fix dozens of security crashes in openjpeg. So upgrading to the latest version is a bit tricky and may introduce regression. It may require very careful merge.

### ma...@gmail.com (2014-09-26)

@bo_xu openjpeg 1.5.2 contains a lot of bug fixes which were initially reported as CVE, they have all been integrated in 2.1.0.

In any case we (=openjpeg team) are interested in any corrupted jp2 that may trigger stack smashing and such in our code base. Do you still have the test suite which triggered corruption in openjpeg ?

### bo...@foxitsoftware.com (2014-09-26)

@mathieu, I tried update openjpeg to r2883 and tested all the 11 openjpeg related issues. On 9 issues that I can reproduce, with the update, they can still reproduce.

I have upload the CL to https://codereview.chromium.org/589243004/, can you try it in pdfium (run pdfium_test --ppm test.pdf) build with ASan?

### cl...@chromium.org (2014-09-29)

[Empty comment from Monorail migration]

### bo...@foxitsoftware.com (2014-10-03)

Fixed in https://pdfium.googlesource.com/pdfium/+/e93d5341d87c54713a9632c8823288fa901a3b78

### cl...@chromium.org (2014-10-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-10-30)

merge approved for m39 branch 2171.  please ensure merge occurs in advance of nov 3, please email me with any issues.

### bo...@foxitsoftware.com (2014-10-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-03)

Dev/Bug owner, please merge to M-39 branch 2171 asap. We need all these security fixes to go into the first stable.

### in...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the report! It qualified for a $1000 reward.

### ti...@google.com (2014-12-08)

Payment in progress

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-01-09)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/413375?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080432)*
