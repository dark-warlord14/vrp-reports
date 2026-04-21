# Security: UAF in guest_view::GuestViewManager::EmbedderProcessDestroyed(browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40065124](https://issues.chromium.org/issues/40065124) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Apps>BrowserTag |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2023-05-31 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in guest\_view::GuestViewManager::EmbedderProcessDestroyed when destroy the webview app.

**VERSION**  

Chromium 116.0.5805.0 (Developer Build) (64-bit)  

Revision 7e43ded13451eef1b12f8df95432f93ce9230cc3-refs/heads/main@{#1151488}  

OS Windows 10 Version 22H2 (Build 19045.2965)

**REPRODUCTION CASE**

1. put background.js/index.html/manifest.json/script.js into the extension\_dir
2. put poc.html/testharness.js/urltestdata.json into webserver dir and run the command: python3 -m http.server 8000
3. run the command in the terminal :  
   
   chrome.exe --user-data-dir=tmp --load-extension=extension\_dir
4. press Ctrl+C in the terminal to trigger the UAF.(Some other way will also trigger the UAF )

I have reproduced this issue in Windows/Linux/ChromiumOS.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

=================================================================  

==14048==ERROR: AddressSanitizer: heap-use-after-free on address 0x1173e0150c98 at pc 0x7ffeca7d4d4d bp 0x00535bbfe1c0 sp 0x00535bbfe208  

READ of size 8 at 0x1173e0150c98 thread T0  

==14048==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffeca7d4d4c in std::\_\_Cr::\_\_tree\_iterator<std::\_\_Cr::\_\_value\_type<void \*,perfetto::base::UnixTaskRunner::WatchTask>,std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<void \*,perfetto::base::UnixTaskRunner::WatchTask>,void \*> \*,long long>::operator++ C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:866  

#1 0x7ffeca7d4e43 in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::chrono::duration<long long,std::\_\_Cr::ratio<1,1000> >,std::\_\_Cr::function<void ()> >,std::\_\_Cr::\_\_map\_value\_compare<std::\_\_Cr::chrono::duration<long long,std::\_\_Cr::ratio<1,1000> >,std::\_\_Cr::\_\_value\_type<std::\_\_Cr::chrono::duration<long long,std::\_\_Cr::ratio<1,1000> >,std::\_\_Cr::function<void ()> >,std::\_\_Cr::less<std::\_\_Cr::chrono::duration<long long,std::\_\_Cr::ratio<1,1000> > >,1>,std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<std::\_\_Cr::chrono::duration<long long,std::\_\_Cr::ratio<1,1000> >,std::\_\_Cr::function<void ()> > > >::\_\_remove\_node\_pointer C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2257  

#2 0x7ffedaa7a6db in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > >,std::\_\_Cr::\_\_map\_value\_compare<int,std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > >,std::\_\_Cr::less<int>,1>,std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > > > >::\_\_erase\_multi<int> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2467  

#3 0x7ffedaa75b8f in guest\_view::GuestViewManager::EmbedderProcessDestroyed C:\b\s\w\ir\cache\builder\src\components\guest\_view\browser\guest\_view\_manager.cc:356  

#4 0x7ffed33decf5 in content::RenderProcessHostImpl::ProcessDied C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:5003  

#5 0x7ffed33de25d in content::RenderProcessHostImpl::FastShutdownIfPossible C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:3834  

#6 0x7ffed80f5b9c in browser\_shutdown::OnShutdownStarting C:\b\s\w\ir\cache\builder\src\chrome\browser\lifetime\browser\_shutdown.cc:169  

#7 0x7ffedb58971a in chrome::SessionEnding C:\b\s\w\ir\cache\builder\src\chrome\browser\lifetime\application\_lifetime\_desktop.cc:228  

#8 0x7ffed6a3f352 in base::internal::Invoker<base::internal::BindState<void (\*)(unsigned long),unsigned long>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#9 0x7ffed82d1aa6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#10 0x7ffedb8f3f82 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#11 0x7ffedb8f2cff in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#12 0x7ffed820ef40 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:211  

#13 0x7ffed820c9c6 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:77  

#14 0x7ffedb8f666f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#15 0x7ffed833c2d7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#16 0x7ffed228a48b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#17 0x7ffed2291697 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#18 0x7ffed2282102 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:34  

#19 0x7ffed6a39785 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:707  

#20 0x7ffed6a3d841 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1284  

#21 0x7ffed6a3cf8b in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1138  

#22 0x7ffed6a3787f in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#23 0x7ffed6a38589 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#24 0x7ffeca74171d in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#25 0x7ff6381563e4 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#26 0x7ff638152bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#27 0x7ff63858204b in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#28 0x7fffa0d37613 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017613)  

#29 0x7fffa10026a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x1173e0150c98 is located 8 bytes inside of 48-byte region [0x1173e0150c90,0x1173e0150cc0)  

freed by thread T0 here:  

#0 0x7ff63820f23d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffedaa73259 in std::\_\_Cr::multimap<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> >,std::\_\_Cr::less<int>,std::\_\_Cr::allocator<std::\_\_Cr::pair<const int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > > > >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\map:2080  

#2 0x7ffedaa730b4 in guest\_view::GuestViewManager::TransferOwnership C:\b\s\w\ir\cache\builder\src\components\guest\_view\browser\guest\_view\_manager.cc:193  

#3 0x7ffedaa87408 in guest\_view::`anonymous namespace'::DestroyGuestIfUnattached C:\b\s\w\ir\cache\builder\src\components\guest\_view\browser\guest\_view\_base.cc:37  

#4 0x7ffed3859eac in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)()> C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:1549  

#5 0x7ffed385783f in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:1183  

#6 0x7ffed38d5aa5 in content::WebContentsImpl::~WebContentsImpl C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:1075  

#7 0x7ffed51f8514 in extensions::WebViewGuest::~WebViewGuest C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:808  

#8 0x7ffed5200f1d in extensions::WebViewGuest::~WebViewGuest C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:798  

#9 0x7ffedaa7a6ec in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > >,std::\_\_Cr::\_\_map\_value\_compare<int,std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > >,std::\_\_Cr::less<int>,1>,std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > > > >::\_\_erase\_multi<int> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2467  

#10 0x7ffedaa75b8f in guest\_view::GuestViewManager::EmbedderProcessDestroyed C:\b\s\w\ir\cache\builder\src\components\guest\_view\browser\guest\_view\_manager.cc:356  

#11 0x7ffed33decf5 in content::RenderProcessHostImpl::ProcessDied C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:5003  

#12 0x7ffed33de25d in content::RenderProcessHostImpl::FastShutdownIfPossible C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:3834  

#13 0x7ffed80f5b9c in browser\_shutdown::OnShutdownStarting C:\b\s\w\ir\cache\builder\src\chrome\browser\lifetime\browser\_shutdown.cc:169  

#14 0x7ffedb58971a in chrome::SessionEnding C:\b\s\w\ir\cache\builder\src\chrome\browser\lifetime\application\_lifetime\_desktop.cc:228  

#15 0x7ffed6a3f352 in base::internal::Invoker<base::internal::BindState<void (\*)(unsigned long),unsigned long>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#16 0x7ffed82d1aa6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#17 0x7ffedb8f3f82 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#18 0x7ffedb8f2cff in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#19 0x7ffed820ef40 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:211  

#20 0x7ffed820c9c6 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:77  

#21 0x7ffedb8f666f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#22 0x7ffed833c2d7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#23 0x7ffed228a48b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#24 0x7ffed2291697 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#25 0x7ffed2282102 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:34  

#26 0x7ffed6a39785 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:707  

#27 0x7ffed6a3d841 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1284

previously allocated by thread T0 here:  

#0 0x7ff63820f33d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffeedecbfde in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffedaa7944d in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > >,std::\_\_Cr::\_\_map\_value\_compare<int,std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > >,std::\_\_Cr::less<int>,1>,std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > > > >::\_\_emplace\_multi<std::\_\_Cr::pair<const int,std::\_\_Cr::unique\_ptr<guest\_view::GuestViewBase,std::\_\_Cr::default\_delete<guest\_view::GuestViewBase> > > > C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2192  

#3 0x7ffedaa7354f in guest\_view::GuestViewManager::ManageOwnership C:\b\s\w\ir\cache\builder\src\components\guest\_view\browser\guest\_view\_manager.cc:210  

#4 0x7ffed51f60f9 in extensions::WebViewGuest::RequestNewWindowPermission C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:1603  

#5 0x7ffed51ff415 in extensions::WebViewGuest::AddNewContents C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:1393  

#6 0x7ffed3885ac4 in content::WebContentsImpl::ShowCreatedWindow C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:4384  

#7 0x7ffed32cf2b2 in content::RenderFrameHostImpl::ShowCreatedWindow C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:5768  

#8 0x7ffecdd17ded in blink::mojom::LocalMainFrameHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\frame\frame.mojom.cc:19406  

#9 0x7ffed3347518 in blink::mojom::LocalMainFrameHostStub<mojo::RawPtrImplRefTraits[blink::mojom::LocalMainFrameHost](javascript:void(0);) >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\frame\frame.mojom.h:1995  

#10 0x7ffed8a3b44f in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:970  

#11 0x7ffedbde334f in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#12 0x7ffed8a40f51 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:701  

#13 0x7ffed8e74406 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1069  

#14 0x7ffed8e6b241 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#15 0x7ffed82d1aa6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#16 0x7ffedb8f3f82 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#17 0x7ffedb8f2cff in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#18 0x7ffed820ef40 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:211  

#19 0x7ffed820c9c6 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:77  

#20 0x7ffedb8f666f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#21 0x7ffed833c2d7 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#22 0x7ffed228a48b in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#23 0x7ffed2291697 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#24 0x7ffed2282102 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:34  

#25 0x7ffed6a39785 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:707  

#26 0x7ffed6a3d841 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1284  

#27 0x7ffed6a3cf8b in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1138

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:866 in std::\_\_Cr::\_\_tree\_iterator<std::\_\_Cr::\_\_value\_type<void \*,perfetto::base::UnixTaskRunner::WatchTask>,std::\_\_Cr::\_\_tree\_node<std::\_\_Cr::\_\_value\_type<void \*,perfetto::base::UnixTaskRunner::WatchTask>,void \*> \*,long long>::operator++  

Shadow bytes around the buggy address:  

0x1173e0150a00: f7 fa fd fd fd fd fd fd f7 fa 00 00 00 00 00 fa  

0x1173e0150a80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fa  

0x1173e0150b00: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa  

0x1173e0150b80: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa  

0x1173e0150c00: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fa  

=>0x1173e0150c80: f7 fa fd[fd]fd fd fd fd f7 fa fd fd fd fd fd fa  

0x1173e0150d00: f7 fa fd fd fd fd fd fa f7 fa fd fd fd fd fd fd  

0x1173e0150d80: f7 fa 00 00 00 00 00 00 f7 fa fd fd fd fd fd fd  

0x1173e0150e00: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

0x1173e0150e80: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

0x1173e0150f00: f7 fa fd fd fd fd fd fd f7 fa fd fd fd fd fd fd  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

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

==14048==ADDITIONAL INFO

==14048==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffed6a3f00f in content::`anonymous namespace'::BrowserConsoleControlHandler C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:496

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==14048==END OF ADDITIONAL INFO  

==14048==ABORTING

## Attachments

- [background.js](attachments/background.js) (text/plain, 72 B)
- [index.html](attachments/index.html) (text/plain, 73 B)
- [script.js](attachments/script.js) (text/plain, 290 B)
- [manifest.json](attachments/manifest.json) (text/plain, 181 B)
- [poc.html](attachments/poc.html) (text/plain, 2.1 KB)
- [testharness.js](attachments/testharness.js) (text/plain, 180.4 KB)
- [urltestdata.json](attachments/urltestdata.json) (text/plain, 196.3 KB)

## Timeline

### [Deleted User] (2023-05-31)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2023-05-31)

I reproduce this issue with the official asan build: asan-win32-release_x64-1151488.zip

### ct...@chromium.org (2023-06-01)

mcnee@ could you look into this report or help re-assign? Thanks!

Note: I used a disposable VM to reproduce this as the files are very large and I was not able to determine that they are safe to run.

Reporter: Would you be able to provide a minimized proof-of-concept for this? It seems likely that this could be triggered without needing the very large test harness and data files, which would make it easier for us to quickly audit the provided code and determine that it's safe to run.

I was able to reproduce this on Linux ASAN release r1151488 with the directions above. (r1151488 is fairly close to current Canary M116.)

Testing on other channels:
- r1135585 (close to current Stable M114) can't reproduce
- r1148132 (close to current Beta M115) can't reproduce

Setting some security labels: Security_Severity-High (UAF in browser process, but requires a malicious Chrome App), FoundIn-116

[Monorail components: Platform>Apps>BrowserTag]

### [Deleted User] (2023-06-01)

[Empty comment from Monorail migration]

### 0x...@gmail.com (2023-06-02)

Hi, you can get the testharness.js, urltestdata.json from the chromium source code.
chromium/src/third_party/blink/web_tests/external/wpt/resources/testharness.js
chromium/src/third_party/blink/web_tests/external/wpt/url/resources/urltestdata.json

### [Deleted User] (2023-06-02)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-06-02)

I'm able to repro.

I was able to reduce this down to the following in the embedder:
let webview = new WebView();                                                               
webview.src = /* page that just calls window.open */;                                                 
document.body.appendChild(webview);                                                                                                                  
while (true) {}

Then once the second guest (from the window.open) is created, kill the embedder.

Since the while loop is blocking the embedder process, it can't complete the attachment process, so the first guest is still owned by GuestViewManager::owned_guests_ along with the second guest.

When we destroy the embedder process, we erase all guests in owned_guests_ for that process. But since the second guest has an opener relationship with the first, when we destroy the first guest, we also destroy the second, recursively calling erase on owned_guests_. The UAF itself occurs in the implementation of std::multimap::erase, so doing that is evidently unsafe.

### mc...@chromium.org (2023-06-05)

Re https://crbug.com/chromium/1450397#c3: The affected code has been present since M108. I think it would be prudent to assume other branches are affected.

### [Deleted User] (2023-06-05)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-06-05)

CL: https://chromium-review.googlesource.com/c/chromium/src/+/4589949

### gi...@appspot.gserviceaccount.com (2023-06-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6345e7871e8197af92f9c6158b06c6e197f87945

commit 6345e7871e8197af92f9c6158b06c6e197f87945
Author: Kevin McNee <mcnee@chromium.org>
Date: Mon Jun 05 19:22:43 2023

Don't recursively destroy guests when clearing unattached guests

When an embedder process is destroyed, we also destroy any unattached
guests associated with that process. This is currently done with a
single call to `owned_guests_.erase`. However, it's possible that two
unattached guests could have an opener relationship, which causes the
destruction of the opener guest to also destroy the other guest, during
the call to `erase`, which is unsafe.

We now separate the steps of erasing `owned_guests_` and destroying the
guests, to avoid this recursive guest destruction.

This also fixes the WaitForNumGuestsCreated test method to not
return prematurely.

Bug: 1450397
Change-Id: Ifef5ec9ff3a1e6952ff56ec279e29e8522625ac0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4589949
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1153396}

[modify] https://crrev.com/6345e7871e8197af92f9c6158b06c6e197f87945/components/guest_view/browser/guest_view_manager.cc
[add] https://crrev.com/6345e7871e8197af92f9c6158b06c6e197f87945/chrome/test/data/extensions/platform_apps/web_view/newwindow/guest_opener_open_on_load.html
[modify] https://crrev.com/6345e7871e8197af92f9c6158b06c6e197f87945/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/6345e7871e8197af92f9c6158b06c6e197f87945/components/guest_view/browser/test_guest_view_manager.h
[modify] https://crrev.com/6345e7871e8197af92f9c6158b06c6e197f87945/chrome/test/data/extensions/platform_apps/web_view/newwindow/embedder.js
[modify] https://crrev.com/6345e7871e8197af92f9c6158b06c6e197f87945/components/guest_view/browser/test_guest_view_manager.cc


### mc...@chromium.org (2023-06-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-06)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-06-12)

I'm not sure why sheriffbot hasn't requested merges. I assume we'd at least want to merge to M115.

### [Deleted User] (2023-06-12)

Merge review required: M115 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-06-12)

1. This fixes a security issue (UAF).
2. https://chromium-review.googlesource.com/c/chromium/src/+/4589949
3. The fix has been released on canary. I tested on ToT.
4. No.
5. N/A.
6. No. This is now covered by automated tests.

### am...@chromium.org (2023-06-12)

Thanks for requesting merge here, Kevin! 
I there were issues with some merge requests and <110 FoundIn labels recently that has been should have been fixed, looks like the SI- label is correct, but the original M-116 and Target-116 labels caused some issues with sheriffbot being able to do it's job well here. 

You're correct, we'd at least want to get this in 115 as well as backmerged to 114/Stable. 

Merges approved for M115 and M114
Please merge this fix to M115/ branch 5790 at soonest so this fix can be included in next M115/Beta. 
Please also merge this fix to M114/branch 5735 at your earliest convenience so this fix can be included in the next M114/Stable. 

### mc...@chromium.org (2023-06-13)

pbommana@ has a cherry pick for M115 here: https://chromium-review.googlesource.com/c/chromium/src/+/4610070
I have a cherry pick for M114 here: https://chromium-review.googlesource.com/c/chromium/src/+/4611152

The M114 one had merge conflicts in test code.

### gi...@appspot.gserviceaccount.com (2023-06-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bef3eb90215470d092425787037dc63f440e4f78

commit bef3eb90215470d092425787037dc63f440e4f78
Author: Kevin McNee <mcnee@chromium.org>
Date: Tue Jun 13 19:34:03 2023

Don't recursively destroy guests when clearing unattached guests

When an embedder process is destroyed, we also destroy any unattached
guests associated with that process. This is currently done with a
single call to `owned_guests_.erase`. However, it's possible that two
unattached guests could have an opener relationship, which causes the
destruction of the opener guest to also destroy the other guest, during
the call to `erase`, which is unsafe.

We now separate the steps of erasing `owned_guests_` and destroying the
guests, to avoid this recursive guest destruction.

This also fixes the WaitForNumGuestsCreated test method to not
return prematurely.

(cherry picked from commit 6345e7871e8197af92f9c6158b06c6e197f87945)

Bug: 1450397
Change-Id: Ifef5ec9ff3a1e6952ff56ec279e29e8522625ac0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4589949
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1153396}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4610070
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Reviewed-by: Kevin McNee <mcnee@chromium.org>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5790@{#706}
Cr-Branched-From: 1d71a337b1f6e707a13ae074dca1e2c34905eb9f-refs/heads/main@{#1148114}

[modify] https://crrev.com/bef3eb90215470d092425787037dc63f440e4f78/components/guest_view/browser/guest_view_manager.cc
[add] https://crrev.com/bef3eb90215470d092425787037dc63f440e4f78/chrome/test/data/extensions/platform_apps/web_view/newwindow/guest_opener_open_on_load.html
[modify] https://crrev.com/bef3eb90215470d092425787037dc63f440e4f78/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/bef3eb90215470d092425787037dc63f440e4f78/components/guest_view/browser/test_guest_view_manager.h
[modify] https://crrev.com/bef3eb90215470d092425787037dc63f440e4f78/chrome/test/data/extensions/platform_apps/web_view/newwindow/embedder.js
[modify] https://crrev.com/bef3eb90215470d092425787037dc63f440e4f78/components/guest_view/browser/test_guest_view_manager.cc


### [Deleted User] (2023-06-13)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-06-13)

Re c#22: A merge is already in progress for M114.
https://chromium-review.googlesource.com/c/chromium/src/+/4611152

### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/85beff6fd3026c3f13ef85d19100e6c34c77b77a

commit 85beff6fd3026c3f13ef85d19100e6c34c77b77a
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed Jun 14 01:10:19 2023

M114: Don't recursively destroy guests when clearing unattached guests

Don't recursively destroy guests when clearing unattached guests

When an embedder process is destroyed, we also destroy any unattached
guests associated with that process. This is currently done with a
single call to `owned_guests_.erase`. However, it's possible that two
unattached guests could have an opener relationship, which causes the
destruction of the opener guest to also destroy the other guest, during
the call to `erase`, which is unsafe.

We now separate the steps of erasing `owned_guests_` and destroying the
guests, to avoid this recursive guest destruction.

This also fixes the WaitForNumGuestsCreated test method to not
return prematurely.

(cherry picked from commit 6345e7871e8197af92f9c6158b06c6e197f87945)

Bug: 1450397
Change-Id: Ifef5ec9ff3a1e6952ff56ec279e29e8522625ac0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4589949
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1153396}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4611152
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1292}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/85beff6fd3026c3f13ef85d19100e6c34c77b77a/components/guest_view/browser/guest_view_manager.cc
[add] https://crrev.com/85beff6fd3026c3f13ef85d19100e6c34c77b77a/chrome/test/data/extensions/platform_apps/web_view/newwindow/guest_opener_open_on_load.html
[modify] https://crrev.com/85beff6fd3026c3f13ef85d19100e6c34c77b77a/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/85beff6fd3026c3f13ef85d19100e6c34c77b77a/components/guest_view/browser/test_guest_view_manager.h
[modify] https://crrev.com/85beff6fd3026c3f13ef85d19100e6c34c77b77a/chrome/test/data/extensions/platform_apps/web_view/newwindow/embedder.js
[modify] https://crrev.com/85beff6fd3026c3f13ef85d19100e6c34c77b77a/components/guest_view/browser/test_guest_view_manager.cc


### rz...@google.com (2023-06-15)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-16)

Congratulations! The VRP Panel has decided to award you $5,000 for this mildly mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-17)

[Empty comment from Monorail migration]

### rz...@google.com (2023-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-06-20)

1. Just https://crrev.com/c/4614596
2. Low, just a few simple conflicts
3. 114, 115, 116
4. Yes

### gm...@google.com (2023-06-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-26)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### pg...@google.com (2023-06-26)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/88f1a27eb64e561a5aa8cc570a288f2ae730a546

commit 88f1a27eb64e561a5aa8cc570a288f2ae730a546
Author: Kevin McNee <mcnee@chromium.org>
Date: Mon Jul 10 15:31:23 2023

[M108-LTS] Don't recursively destroy guests when clearing unattached guests

M108 merge issues:
    components/guest_view/browser/test_guest_view_manager.h:
    Conflicting declarations around the removed line.

  chrome/browser/apps/guest_view/web_view_browsertest.cc:
    Conflicting declarion of ContextMenuInspectElement test.

When an embedder process is destroyed, we also destroy any unattached
guests associated with that process. This is currently done with a
single call to `owned_guests_.erase`. However, it's possible that two
unattached guests could have an opener relationship, which causes the
destruction of the opener guest to also destroy the other guest, during
the call to `erase`, which is unsafe.

We now separate the steps of erasing `owned_guests_` and destroying the
guests, to avoid this recursive guest destruction.

This also fixes the WaitForNumGuestsCreated test method to not
return prematurely.

(cherry picked from commit 6345e7871e8197af92f9c6158b06c6e197f87945)

Bug: 1450397
Change-Id: Ifef5ec9ff3a1e6952ff56ec279e29e8522625ac0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4589949
Commit-Queue: Kevin McNee <mcnee@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1153396}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4614596
Reviewed-by: Simon Hangl <simonha@google.com>
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1490}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/88f1a27eb64e561a5aa8cc570a288f2ae730a546/components/guest_view/browser/guest_view_manager.cc
[add] https://crrev.com/88f1a27eb64e561a5aa8cc570a288f2ae730a546/chrome/test/data/extensions/platform_apps/web_view/newwindow/guest_opener_open_on_load.html
[modify] https://crrev.com/88f1a27eb64e561a5aa8cc570a288f2ae730a546/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/88f1a27eb64e561a5aa8cc570a288f2ae730a546/components/guest_view/browser/test_guest_view_manager.h
[modify] https://crrev.com/88f1a27eb64e561a5aa8cc570a288f2ae730a546/chrome/test/data/extensions/platform_apps/web_view/newwindow/embedder.js
[modify] https://crrev.com/88f1a27eb64e561a5aa8cc570a288f2ae730a546/components/guest_view/browser/test_guest_view_manager.cc


### rz...@google.com (2023-07-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@gmail.com (2023-10-05)

[Comment Deleted]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1450397?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065124)*
