# Heap-use-after-free in SubresourceLoader::didFinishLoading

| Field | Value |
|-------|-------|
| **Issue ID** | [40052378](https://issues.chromium.org/issues/40052378) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2011-12-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Below mentioned reproduction case causes chrome to display sad tab due to a use after free.

**VERSION**  

Chrome Version: [18.0.978.0 (Developer Build 115243 Linux)]  

Operating System: [Ubuntu 10.04 64 bit]

Does NOT reproduce on chrome stable version 16.0.912.63.

**REPRODUCTION CASE**

1. Download and copy attached print.html and test.html files to same folder.
2. Host them on local web server.
3. Open chrome browser and open print.html.
4. Chrome will display print dialog.
5. Click on Cancel button.
6. Click on web page which will cause it to reload.
7. Chrome will display print dialog.
8. Click on Cancel button again.
9. Chrome will display sad tab.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [tab]

This is what Asan has to say.

==14076== ERROR: AddressSanitizer heap-use-after-free on address 0x7ff0210ca8a0 at pc 0x7ff037731a68 bp 0x7fff19eed890 sp 0x7fff19eed888  

READ of size 8 at 0x7ff0210ca8a0 thread T0  

#0 0x7ff037731a68 in basic\_string /usr/lib/gcc/x86\_64-linux-gnu/4.4/../../../../include/c++/4.4/bits/basic\_string.h:254  

#1 0x7ff034d3a27f in \_ZN18ResourceDispatcher18OnReceivedResponseEiRKN7content20ResourceResponseHeadE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/resource\_dispatcher.cc:371  

#2 0x7ff034d39526 in ~ResourceResponseHead /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./content/public/common/resource\_response.h:23  

#3 0x7ff034d379e0 in \_ZN18ResourceDispatcher17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/resource\_dispatcher.cc:326  

#4 0x7ff034c43d6a in \_ZN11ChildThread17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/child\_thread.cc:172  

#5 0x7ff034d93a5a in \_ZN3IPC12ChannelProxy7Context17OnDispatchMessageERKNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_proxy.cc:263  

#6 0x7ff0336084a3 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:503  

#7 0x7ff033614037 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_default.cc:28  

#8 0x7ff0336067ee in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:451  

#9 0x7ff033604a0f in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:765  

#10 0x7ff038274f79 in \_Z12RendererMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/renderer/renderer\_main.cc:241  

#11 0x7ff03355e688 in RunZygote /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:233  

#12 0x7ff03355dae2 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:455  

#13 0x7ff031daf6c7 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#14 0x7ff031daf5c6 in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

0x7ff0210ca8a0 is located 32 bytes inside of 80-byte region [0x7ff0210ca880,0x7ff0210ca8d0)  

freed by thread T0 here:  

#0 0x7ff038e63ab4 in \_ZdlPv ??:0  

#1 0x7ff037732d0c in \_ZN11webkit\_glue16WebURLLoaderImplD0Ev /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/webkit/glue/weburlloader\_impl.cc:701  

#2 0x7ff03609a252 in \_ZN7WebCore17SubresourceLoader16didFinishLoadingEd /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:261  

#3 0x7ff036099100 in \_ZN7WebCore17SubresourceLoader18didReceiveResponseERKNS\_16ResourceResponseE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/WebCore/loader/SubresourceLoader.cpp:164  

#4 0x7ff03773104e in \_ZN11webkit\_glue16WebURLLoaderImpl7Context18OnReceivedResponseERKNS\_20ResourceResponseInfoE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/webkit/glue/weburlloader\_impl.cc:551  

#5 0x7ff034d3a27f in \_ZN18ResourceDispatcher18OnReceivedResponseEiRKN7content20ResourceResponseHeadE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/resource\_dispatcher.cc:371  

#6 0x7ff034d39526 in ~ResourceResponseHead /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./content/public/common/resource\_response.h:23  

#7 0x7ff034d379e0 in \_ZN18ResourceDispatcher17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/resource\_dispatcher.cc:326  

#8 0x7ff034c43d6a in \_ZN11ChildThread17OnMessageReceivedERKN3IPC7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/common/child\_thread.cc:172  

#9 0x7ff034d93a5a in \_ZN3IPC12ChannelProxy7Context17OnDispatchMessageERKNS\_7MessageE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/ipc/ipc\_channel\_proxy.cc:263  

#10 0x7ff0336084a3 in \_ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:503  

#11 0x7ff033614037 in \_ZN4base18MessagePumpDefault3RunEPNS\_11MessagePump8DelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_pump\_default.cc:28  

#12 0x7ff0336067ee in \_ZN11MessageLoop11RunInternalEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:451  

#13 0x7ff033604a0f in ~AutoRunState /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message\_loop.cc:765  

#14 0x7ff038274f79 in \_Z12RendererMainRKN7content18MainFunctionParamsE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/renderer/renderer\_main.cc:241  

#15 0x7ff03355e688 in RunZygote /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:233  

#16 0x7ff03355dae2 in \_ZN7content11ContentMainEiPPKcPNS\_19ContentMainDelegateE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/content/app/content\_main.cc:455  

#17 0x7ff031daf6c7 in ChromeMain /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_main.cc:32  

#18 0x7ff031daf5c6 in main /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/chrome/app/chrome\_exe\_main\_gtk.cc:18  

previously allocated by thread T0 here:  

#0 0x7ff038e638b4 in \_Znwm ??:0  

#1 0x7ff037732b01 in \_ZN11webkit\_glue16WebURLLoaderImplC2EPNS\_25WebKitPlatformSupportImplE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/webkit/glue/weburlloader\_impl.cc:698  

#2 0x7ff034ecd9fd in PassRefPtr /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/third\_party/WebKit/Source/JavaScriptCore/wtf/PassRefPtr.h:90  

==14076== ABORTING  

Stats: 10M malloced (10M for red zones) by 30013 calls  

Stats: 0M realloced by 304 calls  

Stats: 8M freed by 16169 calls  

Stats: 0M really freed by 0 calls  

Stats: 56M (14345 full pages) mmaped in 14 calls  

mmaps by size class: 8:32766; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:64; 17:32; 18:16; 20:4; 22:1;  

mallocs by size class: 8:26083; 9:1721; 10:1465; 11:447; 12:88; 13:66; 14:99; 15:13; 16:16; 17:11; 18:2; 20:1; 22:1;  

frees by size class: 8:13120; 9:1242; 10:1285; 11:311; 12:51; 13:47; 14:83; 15:9; 16:9; 17:8; 18:2; 20:1; 22:1;  

rfrees by size class:  

Stats: malloc large: 15 small slow: 121  

Shadow byte and word:  

0x1ffe04219514: fd  

0x1ffe04219510: fd fd fd fd fd fd fd fd  

More shadow bytes:  

0x1ffe042194f0: fd fd fd fd fd fd fd fd  

0x1ffe042194f8: fd fd fd fd fd fd fd fd  

0x1ffe04219500: fa fa fa fa fa fa fa fa  

0x1ffe04219508: fa fa fa fa fa fa fa fa  

=>0x1ffe04219510: fd fd fd fd fd fd fd fd  

0x1ffe04219518: fd fd fd fd fd fd fd fd  

0x1ffe04219520: fa fa fa fa fa fa fa fa  

0x1ffe04219528: fa fa fa fa fa fa fa fa  

0x1ffe04219530: fd fd fd fd fd fd fd fd

## Attachments

- [test.html](attachments/test.html) (application/x-empty; charset=binary, 0 B)
- [print.html](attachments/print.html) (text/html; charset=us-ascii, 171 B)

## Timeline

### pa...@chromium.org (2011-12-27)

Does not repro in 16 beta, but does in ToT. Does not repro on Mac, either beta or ToT.

### in...@chromium.org (2011-12-27)

It might affect the upcoming m17 beta, keeping m17 for now.

### in...@chromium.org (2011-12-31)

The crash stack speaks on some issue with subresource loader (recent regression). Can you please see if any of the recent changes could be causing this ?

### in...@chromium.org (2011-12-31)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-03)

Nate, James, this might be similar to http://trac.webkit.org/changeset/101543 ?

### si...@chromium.org (2012-01-04)

FYI, Valgrind offers a better stack trace. Notably, it points to an actual line of code.

It is a similar signature to the other bug. Namely, the object that's running code is deleted.

I'll dig into it more tomorrow.

==22313== Invalid read of size 8
==22313==    at 0x81CEB2C: webkit_glue::WebURLLoaderImpl::Context::OnReceivedResponse(webkit_glue::ResourceResponseInfo const&) (weburlloader_impl.cc:555)
==22313==    by 0x7EBB169: ResourceDispatcher::OnReceivedResponse(int, content::ResourceResponseHead const&) (resource_dispatcher.cc:370)
==22313==    by 0x7EBEE8C: void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&), int, content::ResourceResponseHead>(ResourceDispatcher
*, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&), Tuple2<int, content::ResourceResponseHead> const&) (tuple.h:554)
==22313==    by 0x7EBDFAB: bool ResourceMsg_ReceivedResponse::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&)>(IPC::Message
 const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&)) (resource_messages.h:131)
==22313==    by 0x7EBBFA8: ResourceDispatcher::DispatchMessage(IPC::Message const&) (resource_dispatcher.cc:553)
==22313==    by 0x7EBAEC8: ResourceDispatcher::OnMessageReceived(IPC::Message const&) (resource_dispatcher.cc:326)
==22313==    by 0x7D7C099: ChildThread::OnMessageReceived(IPC::Message const&) (child_thread.cc:172)
==22313==    by 0x41D70F3: IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) (ipc_channel_proxy.cc:257)
==22313==    by 0x41DA62E: base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run(IPC::ChannelProxy::Context*, IPC::Message const&) (bind_internal.h:188)
==22313==    by 0x41DA1F6: base::internal::InvokeHelper<false, void, base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy::Context* c
onst&, IPC::Message const&)>::MakeItSo(base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, IPC::ChannelProxy::Context* const&, IPC::Message const&) (bind_in
ternal.h:896)
==22313==    by 0x41D9B9C: base::internal::Invoker<2, base::internal::BindState<base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>, void (IPC::ChannelProxy:
:Context*, IPC::Message const&), void (IPC::ChannelProxy::Context*, IPC::Message)>, void (IPC::ChannelProxy::Context*, IPC::Message const&)>::Run(base::internal::BindStateBase*) (bind_internal.h:1
254)
==22313==    by 0x4F40B76: base::Callback<void ()>::Run() const (callback.h:276)
==22313==    by 0x4F7DAEA: MessageLoop::RunTask(base::PendingTask const&) (message_loop.cc:520)
==22313==    by 0x4F7DC04: MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) (message_loop.cc:532)
==22313==    by 0x4F7E426: MessageLoop::DoWork() (message_loop.cc:722)
==22313==    by 0x4F86CBF: base::MessagePumpDefault::Run(base::MessagePump::Delegate*) (message_pump_default.cc:28)
==22313==    by 0x4F7D742: MessageLoop::RunInternal() (message_loop.cc:479)
==22313==    by 0x4F7D5F5: MessageLoop::RunHandler() (message_loop.cc:452)
==22313==    by 0x4F7CF2A: MessageLoop::Run() (message_loop.cc:362)
==22313==    by 0x8007180: RendererMain(content::MainFunctionParams const&) (renderer_main.cc:241)
==22313==    by 0x7A66C47: (anonymous namespace)::RunZygote(content::MainFunctionParams const&, content::ContentMainDelegate*) (content_main.cc:233)
==22313==    by 0x7A66E1C: (anonymous namespace)::RunNamedProcessTypeMain(std::string const&, content::MainFunctionParams const&, content::ContentMainDelegate*) (content_main.cc:271)
==22313==    by 0x7A673B1: content::ContentMain(int, char const**, content::ContentMainDelegate*) (content_main.cc:455)
==22313==    by 0x4E534C: ChromeMain (chrome_main.cc:32)
==22313==    by 0x4E530B: main (chrome_exe_main_gtk.cc:18)
==22313==  Address 0x1f207cf0 is 48 bytes inside a block of size 96 free'd
==22313==    at 0x4C2848E: operator delete(void*) (vg_replace_malloc.c:1083)
==22313==    by 0x81D0034: webkit_glue::WebURLLoaderImpl::Context::~Context() (weburlloader_impl.cc:292)
==22313==    by 0x81D0547: base::RefCounted<webkit_glue::WebURLLoaderImpl::Context>::Release() const (ref_counted.h:95)
==22313==    by 0x81D05B0: scoped_refptr<webkit_glue::WebURLLoaderImpl::Context>::~scoped_refptr() (ref_counted.h:241)
==22313==    by 0x81CF8B9: webkit_glue::WebURLLoaderImpl::~WebURLLoaderImpl() (weburlloader_impl.cc:703)
==22313==    by 0xAF093DB: void WTF::deleteOwnedPtr<WebKit::WebURLLoader>(WebKit::WebURLLoader*) (OwnPtrCommon.h:53)
==22313==    by 0xAF08E60: WTF::OwnPtr<WebKit::WebURLLoader>::~OwnPtr() (OwnPtr.h:55)
==22313==    by 0xAF08C53: WebCore::ResourceHandleInternal::~ResourceHandleInternal() (ResourceHandleInternal.h:48)
==22313==    by 0xAF0945E: void WTF::deleteOwnedPtr<WebCore::ResourceHandleInternal>(WebCore::ResourceHandleInternal*) (OwnPtrCommon.h:53)
==22313==    by 0xAF09092: WTF::OwnPtr<WebCore::ResourceHandleInternal>::~OwnPtr() (OwnPtr.h:55)
==22313==    by 0xAF08724: WebCore::ResourceHandle::~ResourceHandle() (ResourceHandle.cpp:244)
==22313==    by 0xAF08E43: WTF::RefCounted<WebCore::ResourceHandle>::deref() (RefCounted.h:183)
==22313==    by 0xAF094CF: void WTF::derefIfNotNull<WebCore::ResourceHandle>(WebCore::ResourceHandle*) (PassRefPtr.h:52)
==22313==    by 0xBFA8E1B: WTF::RefPtr<WebCore::ResourceHandle>::operator=(WebCore::ResourceHandle*) (RefPtr.h:135)
==22313==    by 0xBFA6CCE: WebCore::ResourceLoader::releaseResources() (ResourceLoader.cpp:100)
==22313==    by 0xBFAC342: WebCore::SubresourceLoader::releaseResources() (SubresourceLoader.cpp:309)
==22313==    by 0xBFA7D78: WebCore::ResourceLoader::didFinishLoading(double) (ResourceLoader.cpp:313)
==22313==    by 0xBFABE8C: WebCore::SubresourceLoader::didFinishLoading(double) (SubresourceLoader.cpp:261)
==22313==    by 0xBFAB58D: WebCore::SubresourceLoader::didReceiveResponse(WebCore::ResourceResponse const&) (SubresourceLoader.cpp:164)
==22313==    by 0xBFA8430: WebCore::ResourceLoader::didReceiveResponse(WebCore::ResourceHandle*, WebCore::ResourceResponse const&) (ResourceLoader.cpp:435)
==22313==    by 0xAF07E3D: WebCore::ResourceHandleInternal::didReceiveResponse(WebKit::WebURLLoader*, WebKit::WebURLResponse const&) (ResourceHandle.cpp:121)
==22313==    by 0x81CEB24: webkit_glue::WebURLLoaderImpl::Context::OnReceivedResponse(webkit_glue::ResourceResponseInfo const&) (weburlloader_impl.cc:551)
==22313==    by 0x7EBB169: ResourceDispatcher::OnReceivedResponse(int, content::ResourceResponseHead const&) (resource_dispatcher.cc:370)
==22313==    by 0x7EBEE8C: void DispatchToMethod<ResourceDispatcher, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&), int, content::ResourceResponseHead>(ResourceDispatcher
*, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&), Tuple2<int, content::ResourceResponseHead> const&) (tuple.h:554)
==22313==    by 0x7EBDFAB: bool ResourceMsg_ReceivedResponse::Dispatch<ResourceDispatcher, ResourceDispatcher, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&)>(IPC::Message
 const*, ResourceDispatcher*, ResourceDispatcher*, void (ResourceDispatcher::*)(int, content::ResourceResponseHead const&)) (resource_messages.h:131)
==22313==    by 0x7EBBFA8: ResourceDispatcher::DispatchMessage(IPC::Message const&) (resource_dispatcher.cc:553)
==22313==    by 0x7EBAEC8: ResourceDispatcher::OnMessageReceived(IPC::Message const&) (resource_dispatcher.cc:326)
==22313==    by 0x7D7C099: ChildThread::OnMessageReceived(IPC::Message const&) (child_thread.cc:172)
==22313==    by 0x41D70F3: IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) (ipc_channel_proxy.cc:257)
==22313==    by 0x41DA62E: base::internal::RunnableAdapter<void (IPC::ChannelProxy::Context::*)(IPC::Message const&)>::Run(IPC::ChannelProxy::Context*, IPC::Message const&) (bind_internal.h:188)
==

### ja...@chromium.org (2012-01-04)

This is a regression from http://trac.webkit.org/changeset/102602.

### in...@chromium.org (2012-01-04)

Thank you Sir!! Adjusting flags and assignment!

### ch...@gmail.com (2012-01-19)

This reproduction case does not crash now.
Chrome version:18.0.1012.0 (Developer Build 118088 Linux)


### ja...@chromium.org (2012-01-19)

Sorry for not commenting here. This should be fixed as of http://trac.webkit.org/changeset/105226

I'm not sure which branches (if any) need this merged.

### in...@chromium.org (2012-01-19)

This will go directly to Fixed, never affect m17, m18.

### in...@chromium.org (2012-01-19)

Nate says that the bugs affects m17.

http://trac.webkit.org/changeset/105173 was already merged to 963, so we just need to care about merging http://trac.webkit.org/changeset/105226 to m17 branch.

### sc...@gmail.com (2012-01-24)

@chamal.desilva: thanks for catching this regression! A $1000 Chromium Security Reward.

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### ch...@gmail.com (2012-01-24)

Thank you very much for the reward :)

### ts...@chromium.org (2012-01-24)

Merged into m17 at r105798.

### sc...@gmail.com (2012-01-31)

[Empty comment from Monorail migration]

### ch...@gmail.com (2012-02-03)

I received the money today. Thanks a lot :)

### [Deleted User] (2012-05-15)

Marking old security bugs Fixed..

### ch...@gmail.com (2012-06-05)

[Comment Deleted]

### ch...@gmail.com (2012-06-05)

This test case causes a browser crash now.

Chrome version: Version 21.0.1164.0 (140285) (With Asan)
OS : Ubuntu 11.04

Asan reports two errors.

1. A Null pointer error
2. AddressSanitizer crashed on unknown address 0xffffffff81b5b9e8 error.
   Does this type or error indicate a security risk?

Asan output

==2291== ERROR: AddressSanitizer crashed on unknown address 0x000000000000 (pc 0x7fddaf41c71e sp 0x7ffffcabf1c0 bp 0x7ffffcabf210 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7fddaf41c71e in IA__gtk_widget_get_toplevel /build/buildd/gtk+2.0-2.24.4/gtk/gtkwidget.c:8212
    #1 0x7fddb2d6d8a5 in ~Callback /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:282
    #2 0x7fddb2d749a3 in _ZN4base8internal15RunnableAdapterIPFvRK13scoped_refptrIN8printing19PrintJobWorkerOwnerEERKNS_8CallbackIFvvEEEEE3RunES7_SC_ /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/bind_internal.h:226
    #3 0x7fddb3309dc5 in _ZNK4base8CallbackIFvvEE3RunEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/./base/callback.h:272
    #4 0x7fddb330a50e in _ZN11MessageLoop21DeferOrRunPendingTaskERKN4base11PendingTaskE /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message_loop.cc:477
    #5 0x7fddb330ba80 in _ZN11MessageLoop6DoWorkEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message_loop.cc:654
    #6 0x7fddb33ba309 in _ZN4base15MessagePumpGlib14HandleDispatchEv /home/chamal/chrome/home/chrome-svn/tarball/chromium/src/base/message_pump_glib.cc:268
    #7 0x7fddaf84bbcd in g_main_dispatch /build/buildd/glib2.0-2.28.6/./glib/gmain.c:2440
Stats: 100M malloced (137M for red zones) by 417235 calls
Stats: 5M realloced by 16716 calls
Stats: 78M freed by 338698 calls
Stats: 0M really freed by 0 calls
Stats: 268M (68637 full pages) mmaped in 67 calls
  mmaps   by size class: 8:360426; 9:32764; 10:36855; 11:6141; 12:3072; 13:2048; 14:768; 15:256; 16:320; 17:64; 18:32; 19:8; 20:4; 21:4; 22:4;
  mallocs by size class: 8:349782; 9:23793; 10:33672; 11:4531; 12:2525; 13:1750; 14:637; 15:176; 16:288; 17:39; 18:24; 19:6; 20:4; 21:4; 22:4;
  frees   by size class: 8:280329; 9:19226; 10:32511; 11:3085; 12:1857; 13:673; 14:574; 15:128; 16:254; 17:27; 18:20; 19:6; 20:3; 21:2; 22:3;
  rfrees  by size class:
Stats: malloc large: 81 small slow: 1656
ASAN:SIGSEGV
==2312== ERROR: AddressSanitizer crashed on unknown address 0xffffffff81b5b9e8 (pc 0x7f6f8d830978 sp 0x7fff4af50070 bp 0x7f6f820128b2 T0)
AddressSanitizer can not provide additional info. ABORTING
    #0 0x7f6f8d830978 in XQueryExtension /build/buildd/libx11-1.4.2/build/src/../../src/QuExt.c:43
Stats: 49M malloced (43M for red zones) by 70102 calls
Stats: 0M realloced by 340 calls
Stats: 46M freed by 67529 calls
Stats: 0M really freed by 0 calls
Stats: 112M (28693 full pages) mmaped in 28 calls
  mmaps   by size class: 8:65532; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:1792; 15:128; 16:64; 17:32; 18:16; 19:64;
  mallocs by size class: 8:62242; 9:3038; 10:1078; 11:616; 12:687; 13:486; 14:1775; 15:57; 16:31; 17:18; 18:16; 19:58;
  frees   by size class: 8:60530; 9:2491; 10:1029; 11:490; 12:636; 13:421; 14:1767; 15:51; 16:27; 17:16; 18:15; 19:56;
  rfrees  by size class:
Stats: malloc large: 92 small slow: 466


### sc...@gmail.com (2012-06-05)

@chamal: thanks for re-checking this case.

It's probably best to open a brand new bug rather than tacking on details to a long-since-fixed issue. Would you mind doing that? (Chances are you're hitting a completely different issue).

### ch...@gmail.com (2012-06-05)

Sure i will open a new issue :)

### ch...@gmail.com (2012-06-05)

Reported issue http://code.google.com/p/chromium/issues/detail?id=131139 for issue mentioned in https://crbug.com/chromium/108544#c20.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/eda7fe8a65919d44f1fbabe23319ba66b97dd613

commit eda7fe8a65919d44f1fbabe23319ba66b97dd613
Author: Filip Filmar <fmil@google.com>
Date: Fri Sep 02 18:57:36 2022

[fuchsia2002aug] Make references to //third_party/icu relative

This allows the build of ICU to be placed in directories other
than //third_party/icu downstream.

The change does not make a difference in code bases that
continue to use //third_party/icu.

Bug: 108544
Change-Id: If702e4294aba6fcd45f8691a9b87cade5b4b33d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3871752
Reviewed-by: Frank Tang <ftang@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>

[modify] https://crrev.com/eda7fe8a65919d44f1fbabe23319ba66b97dd613/BUILD.gn


### gi...@appspot.gserviceaccount.com (2022-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/icu/+/eda7fe8a65919d44f1fbabe23319ba66b97dd613

commit eda7fe8a65919d44f1fbabe23319ba66b97dd613
Author: Filip Filmar <fmil@google.com>
Date: Fri Sep 02 18:57:36 2022

[fuchsia2002aug] Make references to //third_party/icu relative

This allows the build of ICU to be placed in directories other
than //third_party/icu downstream.

The change does not make a difference in code bases that
continue to use //third_party/icu.

Bug: 108544
Change-Id: If702e4294aba6fcd45f8691a9b87cade5b4b33d2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/icu/+/3871752
Reviewed-by: Frank Tang <ftang@chromium.org>
Reviewed-by: Jungshik Shin <jshin@chromium.org>

[modify] https://crrev.com/eda7fe8a65919d44f1fbabe23319ba66b97dd613/BUILD.gn


### is...@google.com (2022-09-07)

This issue was migrated from crbug.com/chromium/108544?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052378)*
