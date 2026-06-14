# Heap-buffer-overflow in skia::BGRAConvolve2D

| Field | Value |
|-------|-------|
| **Issue ID** | [40060611](https://issues.chromium.org/issues/40060611) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals, Internals>Skia |
| **Reporter** | at...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2012-07-02 |
| **Bounty** | $1,000.00 |

## Description

repro-file as attachment.

Chrome version: ASAN Chromium 22.0.1192.0

==15000== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f0abb9d5980 at pc 0x7f0ae3c18420 bp 0x7fff49108270 sp 0x7fff49108268
READ of size 16 at 0x7f0abb9d5980 thread T0
    #0 0x7f0ae3c18420 in skia::BGRAConvolve2D(unsigned char const*, int, bool, skia::ConvolutionFilter1D const&, skia::ConvolutionFilter1D const&, int, unsigned char*, bool) ???:0
    #1 0x7f0ae3ba47b7 in skia::ImageOperations::ResizeBasic(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&) ???:0
    #2 0x7f0ae3ba50bd in skia::ImageOperations::Resize(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int) ???:0
    #3 0x7f0ae1bef307 in FaviconHandler::ResizeFaviconIfNeeded(gfx::Image const&) ???:0
    #4 0x7f0ae1beed0b in FaviconHandler::SetFavicon(GURL const&, GURL const&, gfx::Image const&, history::IconType) ???:0
    #5 0x7f0ae1bf237c in FaviconHandler::OnDidDownloadFavicon(int, GURL const&, bool, gfx::Image const&) ???:0
    #6 0x7f0ae1317b3b in FaviconTabHelper::OnDidDownloadFavicon(int, GURL const&, bool, SkBitmap const&) ???:0
    #7 0x7f0ae1317a03 in bool IconHostMsg_DidDownloadFavicon::Dispatch<FaviconTabHelper, FaviconTabHelper, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)>(IPC::Message const*, FaviconTabHelper*, FaviconTabHelper*, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)) ???:0
    #8 0x7f0ae13177fb in FaviconTabHelper::OnMessageReceived(IPC::Message const&) ???:0
.
.
.



## Attachments

- [cnode0002-crashed-sp.html](attachments/cnode0002-crashed-sp.html) (text/html; charset=utf-8, 6.1 KB)
- [crbug135432.html](attachments/crbug135432.html) (text/html; charset=us-ascii, 120 B)
- [valgrind.txt](attachments/valgrind.txt) (text/x-c; charset=us-ascii, 5.6 KB)

## Timeline

### gl...@chromium.org (2012-07-02)

https://crbug.com/chromium/123151 might be related.

### at...@gmail.com (2012-07-02)

Actually it seems that you don't need anything else than the following file-content 
to reproduce this.


<html>
<link rel="shortcut icon" href="data:image/gif;base64,R0lGODdhAQACAPABAAD/AP///ywAAAAAAQACAAACAkQKADs=">

</html>
.



### js...@chromium.org (2012-07-02)

Not sure about the relationship to https://crbug.com/chromium/123151, but cluster-fuzz confirms this is an old one: https://cluster-fuzz.appspot.com/testcase?key=70714139

### in...@chromium.org (2012-07-02)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=70714139

Uploader: jschuh@chromium.org

Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x7f0fae81b980
Crash State:
  - crash stack -
  skia::BGRAConvolve2D
  skia::ImageOperations::ResizeBasic
  skia::ImageOperations::Resize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=130029:130062

Minimized Testcase (0.10 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96r5l2Mf9aw0UyqHGhH6tw3zr2ZF2yLUPlTcyJxyXzwfcwAFVdJubiMoXCjv7iiQyu0P7QnUmjljFHqfQXpMscy2cUHMrIZK3ccYFCR0GgyLDlk8uT7u54cHEiIgWriodO625SUbDHtR0YA4rVjwwdXgH91KSi09_jPk3cTfhIOO7YD6JU

### [Deleted User] (2012-07-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-07-16)

Elliot, can you please help to take a look or help with an owner.

### in...@chromium.org (2012-07-16)

[Empty comment from Monorail migration]

### ep...@google.com (2012-07-19)

I can confirm that my local release build, running on my Linux desktop via NX, yields the following ASAN error when opening the attached sample (copied from https://crbug.com/chromium/135432#c2).

Chromium	22.0.1209.0 (Developer Build 146872)
OS	Linux
WebKit	537.1 (trunk/Source/WebCore/Configurations@122718)
JavaScript	V8 3.12.11
Flash	11.2 r202
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1209.0 Safari/537.1
Command Line	 out/Release/chrome --flag-switches-begin --flag-switches-end file:///home/epoger/bugs
Executable Path	/usr/local/google/home/epoger/src/chrome/asan-release/src/out/Release/chrome
Profile Path	/home/epoger/.config/chromium/Default

=================================================================
==22623== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7fd005206380 at pc 0x7fd04b0b6587 bp 0x7fffbb776910 sp 0x7fffbb776908
READ of size 16 at 0x7fd005206380 thread T0
    #0 0x7fd04b0b6587 in skia::(anonymous namespace)::ConvolveHorizontally_SSE2(unsigned char const*, skia::ConvolutionFilter1D const&, unsigned char*) skia/ext/convolver.cc:350
    #1 0x7fd04b0b47f8 in skia::BGRAConvolve2D(unsigned char const*, int, bool, skia::ConvolutionFilter1D const&, skia::ConvolutionFilter1D const&, int, unsigned char*, bool) skia/ext/convolver.cc:803
    #2 0x7fd04b04f0df in skia::ImageOperations::ResizeBasic(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&) skia/ext/image_operations.cc:532
    #3 0x7fd04b04df52 in skia::ImageOperations::Resize(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&) skia/ext/image_operations.cc:359
    #4 0x7fd04b04f6a7 in skia::ImageOperations::Resize(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int) skia/ext/image_operations.cc:545
    #5 0x7fd049892c49 in FaviconHandler::ResizeFaviconIfNeeded(gfx::Image const&) chrome/browser/favicon/favicon_handler.cc:535
    #6 0x7fd049892847 in FaviconHandler::SetFavicon(GURL const&, GURL const&, gfx::Image const&, history::IconType) chrome/browser/favicon/favicon_handler.cc:208
    #7 0x7fd04989431c in FaviconHandler::OnDidDownloadFavicon(int, GURL const&, bool, gfx::Image const&) chrome/browser/favicon/favicon_handler.cc:327
    #8 0x7fd049033a74 in FaviconTabHelper::OnDidDownloadFavicon(int, GURL const&, bool, SkBitmap const&) chrome/browser/favicon/favicon_tab_helper.cc:192
    #9 0x7fd04903398a in bool IconHostMsg_DidDownloadFavicon::Dispatch<FaviconTabHelper, FaviconTabHelper, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)>(IPC::Message const*, FaviconTabHelper*, FaviconTabHelper*, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)) ./chrome/common/icon_messages.h:41
    #10 0x7fd049033892 in FaviconTabHelper::OnMessageReceived(IPC::Message const&) chrome/browser/favicon/favicon_tab_helper.cc:180
    #11 0x7fd04da1f410 in WebContentsImpl::OnMessageReceived(IPC::Message const&) content/browser/web_contents/web_contents_impl.cc:609
    #12 0x7fd04da22f6d in non-virtual thunk to WebContentsImpl::OnMessageReceived(IPC::Message const&) ???:0
    #13 0x7fd04d9590cb in content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_view_host_impl.cc:851
    #14 0x7fd04d9614ad in non-virtual thunk to content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) ???:0
    #15 0x7fd04d9393c5 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:1014
    #16 0x7fd04d93a23d in non-virtual thunk to content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) ???:0
    #17 0x7fd04a047483 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:257
    #18 0x7fd04a04df68 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) ./base/bind_internal.h:899
    #19 0x7fd049f49e13 in MessageLoop::RunTask(base::PendingTask const&) base/message_loop.cc:457
    #20 0x7fd049f4a57d in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:468
    #21 0x7fd049f4a892 in MessageLoop::DoWork() base/message_loop.cc:644
    #22 0x7fd049ff1e56 in base::MessagePumpGlib::RunWithDispatcher(base::MessagePump::Delegate*, base::MessagePumpDispatcher*) base/message_pump_glib.cc:203
    #23 0x7fd049f4960c in MessageLoop::RunInternal() base/message_loop.cc:416
    #24 0x7fd049f83813 in base::RunLoop::Run() base/run_loop.cc:46
    #25 0x7fd04982c631 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome/browser/chrome_browser_main.cc:1962
    #26 0x7fd04d7ab612 in content::BrowserMainLoop::RunMainMessageLoopParts() content/browser/browser_main_loop.cc:455
    #27 0x7fd04d7ae28a in (anonymous namespace)::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner.cc:100
    #28 0x7fd04d7a90cf in BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:21
    #29 0x7fd049e2b88e in content::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner.cc:375
    #30 0x7fd049e2c5f0 in content::ContentMainRunnerImpl::Run() content/app/content_main_runner.cc:630
    #31 0x7fd049e2a57f in content::ContentMain(int, char const**, content::ContentMainDelegate*) content/app/content_main.cc:35
    #32 0x7fd048ab31f7 in ChromeMain chrome/app/chrome_main.cc:32
    #33 0x7fd048ab315b in main chrome/app/chrome_exe_main_gtk.cc:18
    #34 0x7fd041a8dc4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
0x7fd005206380 is located 0 bytes to the right of 8-byte region [0x7fd005206380,0x7fd005206388)
allocated by thread T0 here:
    #0 0x7fd04f250d52 in __interceptor_malloc ??:0
    #1 0x7fd04b054a7c in sk_malloc_flags(unsigned long, unsigned int) skia/ext/SkMemory_new_handler.cpp:59
    #2 0x7fd04af882fc in SkBitmap::HeapAllocator::allocPixelRef(SkBitmap*, SkColorTable*) third_party/skia/src/core/SkBitmap.cpp:451
    #3 0x7fd04af87f3c in SkBitmap::allocPixels(SkBitmap::Allocator*, SkColorTable*) third_party/skia/src/core/SkBitmap.cpp:383
    #4 0x7fd048bd11c1 in SkBitmap::allocPixels(SkColorTable*) third_party/skia/include/core/SkBitmap.h:286
    #5 0x7fd04ae877c7 in (anonymous namespace)::SkBitmap_Data::InitSkBitmapFromData(SkBitmap*, char const*, unsigned long) const content/public/common/common_param_traits.cc:39
    #6 0x7fd04ae87667 in IPC::ParamTraits<SkBitmap>::Read(IPC::Message const*, PickleIterator*, SkBitmap*) content/public/common/common_param_traits.cc:480
    #7 0x7fd04e550579 in bool IPC::ReadParam<SkBitmap>(IPC::Message const*, PickleIterator*, SkBitmap*) ./ipc/ipc_message_utils.h:174
    #8 0x7fd04e55bad0 in IPC::ParamTraits<Tuple4<int, GURL, bool, SkBitmap> >::Read(IPC::Message const*, PickleIterator*, Tuple4<int, GURL, bool, SkBitmap>*) ./ipc/ipc_message_utils.h:655
    #9 0x7fd04e55ba69 in bool IPC::ReadParam<Tuple4<int, GURL, bool, SkBitmap> >(IPC::Message const*, PickleIterator*, Tuple4<int, GURL, bool, SkBitmap>*) ./ipc/ipc_message_utils.h:174
    #10 0x7fd04e5427c1 in IPC::MessageSchema<Tuple4<int, GURL, bool, SkBitmap> >::Read(IPC::Message const*, Tuple4<int, GURL, bool, SkBitmap>*) ./ipc/ipc_message_utils_impl.h:22
    #11 0x7fd04e542739 in IconHostMsg_DidDownloadFavicon::Read(IPC::Message const*, Tuple4<int, GURL, bool, SkBitmap>*) ./chrome/common/icon_messages.h:41
    #12 0x7fd049033973 in bool IconHostMsg_DidDownloadFavicon::Dispatch<FaviconTabHelper, FaviconTabHelper, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)>(IPC::Message const*, FaviconTabHelper*, FaviconTabHelper*, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)) ./chrome/common/icon_messages.h:41
    #13 0x7fd049033892 in FaviconTabHelper::OnMessageReceived(IPC::Message const&) chrome/browser/favicon/favicon_tab_helper.cc:180
    #14 0x7fd04da1f410 in WebContentsImpl::OnMessageReceived(IPC::Message const&) content/browser/web_contents/web_contents_impl.cc:609
    #15 0x7fd04da22f6d in non-virtual thunk to WebContentsImpl::OnMessageReceived(IPC::Message const&) ???:0
    #16 0x7fd04d9590cb in content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_view_host_impl.cc:851
    #17 0x7fd04d9614ad in non-virtual thunk to content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) ???:0
    #18 0x7fd04d9393c5 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:1014
    #19 0x7fd04d93a23d in non-virtual thunk to content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) ???:0
    #20 0x7fd04a047483 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:257
    #21 0x7fd04a04df68 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) ./base/bind_internal.h:899
    #22 0x7fd049f49e13 in MessageLoop::RunTask(base::PendingTask const&) base/message_loop.cc:457
    #23 0x7fd049f4a57d in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:468
    #24 0x7fd049f4a892 in MessageLoop::DoWork() base/message_loop.cc:644
==22623== ABORTING
Stats: 47M malloced (76M for red zones) by 238159 calls
Stats: 2M realloced by 8758 calls
Stats: 37M freed by 165891 calls
Stats: 0M really freed by 0 calls
Stats: 160M (40978 full pages) mmaped in 40 calls
  mmaps   by size class: 8:229362; 9:16382; 10:16380; 11:4094; 12:2048; 13:1024; 14:768; 15:256; 16:256; 17:32; 18:16; 19:8; 20:4; 21:2;
  mallocs by size class: 8:208421; 9:10120; 10:13779; 11:2857; 12:1576; 13:483; 14:532; 15:117; 16:230; 17:22; 18:16; 19:2; 20:2; 21:2;
  frees   by size class: 8:141175; 9:7591; 10:12903; 11:2109; 12:1039; 13:281; 14:474; 15:90; 16:200; 17:13; 18:12; 19:2; 21:2;
  rfrees  by size class:
Stats: malloc large: 44 small slow: 984
Shadow byte and word:
  0x1ffa00a40c70: 0
  0x1ffa00a40c70: 00 fb fb fb fb fb fb fb
More shadow bytes:
  0x1ffa00a40c50: 00 00 00 00 00 00 00 00
  0x1ffa00a40c58: 00 00 00 00 00 00 00 07
  0x1ffa00a40c60: fa fa fa fa fa fa fa fa
  0x1ffa00a40c68: fa fa fa fa fa fa fa fa
=>0x1ffa00a40c70: 00 fb fb fb fb fb fb fb
  0x1ffa00a40c78: fb fb fb fb fb fb fb fb
  0x1ffa00a40c80: fa fa fa fa fa fa fa fa
  0x1ffa00a40c88: fa fa fa fa fa fa fa fa
  0x1ffa00a40c90: 00 00 00 00 00 00 00 00


### ep...@google.com (2012-07-19)

I also see it in this debug build on the same machine...

Chromium	22.0.1209.0 (Developer Build 146887)
OS	Linux
WebKit	537.1 (trunk/Source/WebCore/Configurations@121656)
JavaScript	V8 3.12.11
Flash	11.2 r202
User Agent	Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1209.0 Safari/537.1
Command Line	 out/Debug/chrome --single-process --flag-switches-begin --flag-switches-end
Executable Path	/usr/local/google/home/epoger/src/chrome/asan-debug/src/out/Debug/chrome
Profile Path	/home/epoger/.config/chromium/Default

=================================================================
==25336== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7ffc1a1ae180 at pc 0x7ffc4f5fd456 bp 0x7fff605f0e70 sp 0x7fff605f0e68
READ of size 16 at 0x7ffc1a1ae180 thread T0
    #0 0x7ffc4f5fd456 in skia::(anonymous namespace)::ConvolveHorizontally_SSE2(unsigned char const*, skia::ConvolutionFilter1D const&, unsigned char*) skia/ext/convolver.cc:323
    #1 0x7ffc4f5e0271 in skia::BGRAConvolve2D(unsigned char const*, int, bool, skia::ConvolutionFilter1D const&, skia::ConvolutionFilter1D const&, int, unsigned char*, bool) skia/ext/convolver.cc:805
    #2 0x7ffc4f275dd5 in skia::ImageOperations::ResizeBasic(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&) skia/ext/image_operations.cc:532
    #3 0x7ffc4f2701e4 in skia::ImageOperations::Resize(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int, SkIRect const&) skia/ext/image_operations.cc:359
    #4 0x7ffc4f279213 in skia::ImageOperations::Resize(SkBitmap const&, skia::ImageOperations::ResizeMethod, int, int) skia/ext/image_operations.cc:545
    #5 0x7ffc45e7ae4e in FaviconHandler::ResizeFaviconIfNeeded(gfx::Image const&) chrome/browser/favicon/favicon_handler.cc:535
    #6 0x7ffc45e7a26b in FaviconHandler::SetFavicon(GURL const&, GURL const&, gfx::Image const&, history::IconType) chrome/browser/favicon/favicon_handler.cc:206
    #7 0x7ffc45e7ee5e in FaviconHandler::OnDidDownloadFavicon(int, GURL const&, bool, gfx::Image const&) chrome/browser/favicon/favicon_handler.cc:327
    #8 0x7ffc433876bf in FaviconTabHelper::OnDidDownloadFavicon(int, GURL const&, bool, SkBitmap const&) chrome/browser/favicon/favicon_tab_helper.cc:192
    #9 0x7ffc43389c77 in void DispatchToMethod<FaviconTabHelper, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&), int, GURL, bool, SkBitmap>(FaviconTabHelper*, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&), Tuple4<int, GURL, bool, SkBitmap> const&) ./base/tuple.h:566
    #10 0x7ffc4338886a in bool IconHostMsg_DidDownloadFavicon::Dispatch<FaviconTabHelper, FaviconTabHelper, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)>(IPC::Message const*, FaviconTabHelper*, FaviconTabHelper*, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)) ./chrome/common/icon_messages.h:41
    #11 0x7ffc43386e81 in FaviconTabHelper::OnMessageReceived(IPC::Message const&) chrome/browser/favicon/favicon_tab_helper.cc:179
    #12 0x7ffc5dfb8a90 in WebContentsImpl::OnMessageReceived(IPC::Message const&) content/browser/web_contents/web_contents_impl.cc:609
    #13 0x7ffc5dfc4a4f in non-virtual thunk to WebContentsImpl::OnMessageReceived(IPC::Message const&) content/browser/web_contents/web_contents_impl.cc:2110
    #14 0x7ffc5dbab756 in content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_view_host_impl.cc:851
    #15 0x7ffc5dbc51af in non-virtual thunk to content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_view_host_impl.cc:1744
    #16 0x7ffc5db0d046 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:1014
    #17 0x7ffc5db0ed7f in non-virtual thunk to content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:1506
    #18 0x7ffc4850e424 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:260
    #19 0x7ffc48532a08 in base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run(IPC::ChannelProxy::Context*, IPC::Message const&) ./base/bind_internal.h:190
    #20 0x7ffc485325b2 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) ./base/bind_internal.h:899
    #21 0x7ffc485320dd in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context*, IPC::Message const&), void ()(IPC::ChannelProxy::Context*, IPC::Message)>, void ()(IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) ./base/bind_internal.h:1256
    #22 0x7ffc43005d25 in base::Callback<void ()()>::Run() const ./base/callback.h:388
    #23 0x7ffc47efe11f in MessageLoop::RunTask(base::PendingTask const&) base/message_loop.cc:457
    #24 0x7ffc47effa83 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) base/message_loop.cc:471
    #25 0x7ffc47f002a8 in MessageLoop::DoWork() base/message_loop.cc:644
    #26 0x7ffc4830ec3d in base::MessagePumpGlib::HandleDispatch() base/message_pump_glib.cc:268
    #27 0x7ffc4830b635 in (anonymous namespace)::WorkSourceDispatch(_GSource*, int (*)(void*), void*) base/message_pump_glib.cc:105
    #28 0x7ffc3d9e78c2 in g_main_dispatch /tmp/glib2.0.0xzuTt/glib2.0-2.24.1/glib/gmain.c:1960
0x7ffc1a1ae180 is located 0 bytes to the right of 8-byte region [0x7ffc1a1ae180,0x7ffc1a1ae188)
allocated by thread T0 here:
    #0 0x7ffc66945cb2 in __interceptor_malloc ??:0
    #1 0x7ffc4f2a0a1c in sk_malloc_flags(unsigned long, unsigned int) skia/ext/SkMemory_new_handler.cpp:59
    #2 0x7ffc4ece53d8 in SkBitmap::HeapAllocator::allocPixelRef(SkBitmap*, SkColorTable*) third_party/skia/src/core/SkBitmap.cpp:451
    #3 0x7ffc4ece4117 in SkBitmap::allocPixels(SkBitmap::Allocator*, SkColorTable*) third_party/skia/src/core/SkBitmap.cpp:383
    #4 0x7ffc41ceab42 in SkBitmap::allocPixels(SkColorTable*) third_party/skia/include/core/SkBitmap.h:286
    #5 0x7ffc4e61129d in (anonymous namespace)::SkBitmap_Data::InitSkBitmapFromData(SkBitmap*, char const*, unsigned long) const content/public/common/common_param_traits.cc:39
    #6 0x7ffc4e610b07 in IPC::ParamTraits<SkBitmap>::Read(IPC::Message const*, PickleIterator*, SkBitmap*) content/public/common/common_param_traits.cc:479
    #7 0x7ffc40fae231 in bool IPC::ReadParam<SkBitmap>(IPC::Message const*, PickleIterator*, SkBitmap*) ./ipc/ipc_message_utils.h:174
    #8 0x7ffc410fe90a in IPC::ParamTraits<Tuple4<int, GURL, bool, SkBitmap> >::Read(IPC::Message const*, PickleIterator*, Tuple4<int, GURL, bool, SkBitmap>*) ./ipc/ipc_message_utils.h:654
    #9 0x7ffc40fefaa1 in bool IPC::ReadParam<Tuple4<int, GURL, bool, SkBitmap> >(IPC::Message const*, PickleIterator*, Tuple4<int, GURL, bool, SkBitmap>*) ./ipc/ipc_message_utils.h:174
    #10 0x7ffc410300fc in IPC::MessageSchema<Tuple4<int, GURL, bool, SkBitmap> >::Read(IPC::Message const*, Tuple4<int, GURL, bool, SkBitmap>*) ./ipc/ipc_message_utils_impl.h:22
    #11 0x7ffc40f41e38 in IconHostMsg_DidDownloadFavicon::Read(IPC::Message const*, Tuple4<int, GURL, bool, SkBitmap>*) ./chrome/common/icon_messages.h:41
    #12 0x7ffc43388746 in bool IconHostMsg_DidDownloadFavicon::Dispatch<FaviconTabHelper, FaviconTabHelper, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)>(IPC::Message const*, FaviconTabHelper*, FaviconTabHelper*, void (FaviconTabHelper::*)(int, GURL const&, bool, SkBitmap const&)) ./chrome/common/icon_messages.h:41
    #13 0x7ffc43386e81 in FaviconTabHelper::OnMessageReceived(IPC::Message const&) chrome/browser/favicon/favicon_tab_helper.cc:179
    #14 0x7ffc5dfb8a90 in WebContentsImpl::OnMessageReceived(IPC::Message const&) content/browser/web_contents/web_contents_impl.cc:609
    #15 0x7ffc5dfc4a4f in non-virtual thunk to WebContentsImpl::OnMessageReceived(IPC::Message const&) content/browser/web_contents/web_contents_impl.cc:2110
    #16 0x7ffc5dbab756 in content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_view_host_impl.cc:851
    #17 0x7ffc5dbc51af in non-virtual thunk to content::RenderViewHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_view_host_impl.cc:1744
    #18 0x7ffc5db0d046 in content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:1014
    #19 0x7ffc5db0ed7f in non-virtual thunk to content::RenderProcessHostImpl::OnMessageReceived(IPC::Message const&) content/browser/renderer_host/render_process_host_impl.cc:1506
    #20 0x7ffc4850e424 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc/ipc_channel_proxy.cc:260
    #21 0x7ffc48532a08 in base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run(IPC::ChannelProxy::Context*, IPC::Message const&) ./base/bind_internal.h:190
    #22 0x7ffc485325b2 in base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context* const&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) ./base/bind_internal.h:899
    #23 0x7ffc485320dd in base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void ()(IPC::ChannelProxy::Context*, IPC::Message const&), void ()(IPC::ChannelProxy::Context*, IPC::Message)>, void ()(IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) ./base/bind_internal.h:1256
    #24 0x7ffc43005d25 in base::Callback<void ()()>::Run() const ./base/callback.h:388
==25336== ABORTING
Stats: 49M malloced (80M for red zones) by 256405 calls
Stats: 2M realloced by 8758 calls
Stats: 37M freed by 175056 calls
Stats: 0M really freed by 0 calls
Stats: 164M (42001 full pages) mmaped in 41 calls
  mmaps   by size class: 8:245745; 9:16382; 10:20475; 11:4094; 12:2048; 13:1024; 14:768; 15:128; 16:256; 17:32; 18:16; 19:8; 20:4; 21:2;
  mallocs by size class: 8:224845; 9:10689; 10:14698; 11:3103; 12:1550; 13:493; 14:664; 15:103; 16:221; 17:22; 18:11; 19:2; 20:2; 21:2;
  frees   by size class: 8:149072; 9:7901; 10:13703; 11:2235; 12:991; 13:276; 14:592; 15:76; 16:190; 17:9; 18:7; 19:2; 21:2;
  rfrees  by size class:
Stats: malloc large: 39 small slow: 1026
Shadow byte and word:
  0x1fff83435c30: 0
  0x1fff83435c30: 00 fb fb fb fb fb fb fb
More shadow bytes:
  0x1fff83435c10: 00 00 00 00 00 00 00 00
  0x1fff83435c18: 00 00 00 00 00 00 00 07
  0x1fff83435c20: fa fa fa fa fa fa fa fa
  0x1fff83435c28: fa fa fa fa fa fa fa fa
=>0x1fff83435c30: 00 fb fb fb fb fb fb fb
  0x1fff83435c38: fb fb fb fb fb fb fb fb
  0x1fff83435c40: fa fa fa fa fa fa fa fa
  0x1fff83435c48: fa fa fa fa fa fa fa fa
  0x1fff83435c50: 00 00 00 00 00 00 00 00


### ep...@google.com (2012-07-20)

I can also get this ASAN failure within the debugger.

It looks like the failure actually occurs at line 323 of skia/ext/convolver.cc:
__m128i src8 = _mm_loadu_si128(row_to_filter);

The debugger tells me that row_to_filter=0x7ffffffebfa0

Mike/Brian, does this mean anything to you?

### [Deleted User] (2012-07-20)

stephen, is that code you worked on?

### se...@chromium.org (2012-07-20)

No, this is Brett's Lanczos3 implementation IIRC.  I don't know if anyone's been working on it lately; will check SVN blame.

### se...@chromium.org (2012-07-20)

[Empty comment from Monorail migration]

### se...@chromium.org (2012-07-20)

It's also possible that the heap overflow is due to an inadequate buffer in the caller (seems to be favicon code?).

### in...@chromium.org (2012-08-01)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-02)

Please do read Mark's email titled "Code Yellow: Security Bug Backlog" on chrome-team mailing list.

### se...@chromium.org (2012-08-02)

I'll take this on.

### in...@chromium.org (2012-08-02)

Thanks Stephen.

### se...@chromium.org (2012-08-02)

Notes:  I've repro'ed this in a Debug build with an invalid read error in valgrind (the stacktrace is a bit different, probably due to lack of inlining in Debug).  Output is attached.

The bug seems to be in the SSE2 code.  If I comment out 

#define SIMD_SSE2 1

in convolver.h, the valgrind error goes away.

So it is probably related to http://code.google.com/p/chromium/issues/detail?id=123151 as glider suggested.

### se...@chromium.org (2012-08-02)

Unfortunately, I will be out of the office for a week, and I won't be able to work on this until I get back.

SecurityTeam:  If you need a quick fix, I would suggest disabling the SSE2 code in BGRAConvolve2D  (#define SIMD_SSE2 0 in convolver.h).

This will have some performance impact, but most of our image-resizing-sensitive codepaths have been tweaked to avoid using the Lanczos3 path anyway (they dial down to bilinear), so it shouldn't be a big hit.

### in...@chromium.org (2012-08-06)

Mike/Elliot/Tom, can one of you take this please. this is a high severity one and has higher priority than the other medium severity ones.

### to...@chromium.org (2012-08-06)

https://chromiumcodereview.appspot.com/10823186/ implements Steven's suggested quick fix to close the hole in M22; we'll then have breathing room to fix the high-performance version.

### in...@chromium.org (2012-08-06)

Sounds good, the high-performance version change can be tracked in a separate functional bug.

### in...@chromium.org (2012-08-06)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-08-07)

http://src.chromium.org/viewvc/chrome?view=rev&revision=150335

### ep...@google.com (2012-08-07)

I see that this is marked Merge-Approved... I think these are the remaining steps.  Right, inferno?

M21:

1. confirm that we can repro the bug in the most recent M21 build, i.e. http://master.chrome.corp.google.com/official_builds/21.0.1180.75/
2. merge http://crrev.com/150335 into M21
3. confirm that the bug is fixed in the next M21 build after that merge
4. change the label on this bug from Mstone-21 to Mstone-22

M22:

1. confirm that we can repro the bug in the then-most-recent M22 build in http://master.chrome.corp.google.com/official_builds/
2. merge http://crrev.com/150335 into M22
3. confirm that the bug is fixed in the next M22 build after that merge
4. mark the bug as Fixed

### in...@chromium.org (2012-08-07)

Yes lets do only the m22 part for now and keep in fixunreleased. we are unsure if we will merge this to stable, but easier to decide when we are closer to the merge window for 1st security patch m21.

### cl...@chromium.org (2012-08-07)

ClusterFuzz has detected this issue as fixed in range 150246:150269.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=70714139

Uploader: jschuh@chromium.org

Crash Type: Heap-buffer-overflow READ 16
Crash Address: 0x7f0fae81b980
Crash State:
  - crash stack -
  skia::BGRAConvolve2D
  skia::ImageOperations::ResizeBasic
  skia::ImageOperations::Resize
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=130029:130062
Fixed: https://cluster-fuzz.appspot.com/revisions?range=150246:150269

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv96r5l2Mf9aw0UyqHGhH6tw3zr2ZF2yLUPlTcyJxyXzwfcwAFVdJubiMoXCjv7iiQyu0P7QnUmjljFHqfQXpMscy2cUHMrIZK3ccYFCR0GgyLDlk8uT7u54cHEiIgWriodO625SUbDHtR0YA4rVjwwdXgH91KSi09_jPk3cTfhIOO7YD6JU

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### br...@chromium.org (2012-08-07)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-16)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-08-20)

Nice, buffer overflow.
$1000

### sc...@gmail.com (2012-09-05)

I merged the disable of SIMD SSE2 at r155005

### sc...@gmail.com (2012-09-12)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-14)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### se...@chromium.org (2013-03-08)

[Empty comment from Monorail migration]

### [Deleted User] (2013-03-08)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-14)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/135432?no_tracker_redirect=1

[Multiple monorail components: Internals, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060611)*
