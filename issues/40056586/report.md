# Security: heap-use-after-free in the PaymentCredential in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40056586](https://issues.chromium.org/issues/40056586) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2021-07-19 |
| **Bounty** | $20,000.00 |

## Description

**VULNERABILITY DETAILS**  

heap-use-after-free in the PaymentCredential in the browser process which will excape the sandbox.

**VERSION**  

Chrome Version: [94.0.4581.0] + [dev] (asan-win32-release\_x64-902937)  

Operating System: Windows 10

**REPRODUCTION CASE**

Put the confirm.html & confirm.js in the webserver.  

Then run the command:  

C:\chromium\_version\asan-win32-release\_x64-902937>chrome.exe --user-data-dir=c:/tmp/no1 --enable-experimental-web-platform-features <https://test.com/confirm.html>

Don't need click any button.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

# C:\chromium\_version\asan-win32-release\_x64-902866>chrome.exe --user-data-dir=c:/tmp/what --enable-experimental-web-platform-features <https://test.com/trial/confirm.html> [9760:9320:0718/231716.989:ERROR:device\_event\_log\_impl.cc(214)] [23:17:16.987] Bluetooth: bluetooth\_adapter\_winrt.cc:1073 Getting Default Adapter failed.

==9760==ERROR: AddressSanitizer: heap-use-after-free on address 0x122017f320f8 at pc 0x7ffa8c0cefb4 bp 0x00fc067fde20 sp 0x00fc067fde68  

READ of size 8 at 0x122017f320f8 thread T0  

==9760==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffa8c0cefb3 in scoped\_refptr<const base::internal::WeakReference::Flag>::operator= C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:250  

#1 0x7ffa8c0ff036 in base::internal::WeakPtrBase::reset C:\b\s\w\ir\cache\builder\src\base\memory\weak\_ptr.h:161  

#2 0x7ffaa4da954f in payments::PaymentCredentialEnrollmentController::CloseDialog C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_controller.cc:77  

#3 0x7ffaa326b338 in payments::PaymentCredential::Reset C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:324  

#4 0x7ffaa326ae71 in payments::PaymentCredential::~PaymentCredential C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:48  

#5 0x7ffaa326eb79 in payments::PaymentCredential::~PaymentCredential C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:47  

#6 0x7ffa90937106 in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::RenderFrameHost \*),content::RenderFrameHostImpl \*&> C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:1476  

#7 0x7ffa909602c7 in content::WebContentsImpl::DidStartNavigation C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:5250  

#8 0x7ffa90499f42 in content::NavigationRequest::StartNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:2022  

#9 0x7ffa9049efc0 in content::NavigationRequest::BeginNavigationImpl C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:1758  

#10 0x7ffa9049dcd7 in content::NavigationRequest::BeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:1585  

#11 0x7ffa904e8dae in content::Navigator::OnBeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:921  

#12 0x7ffa905463d9 in content::RenderFrameHostImpl::BeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:6647  

#13 0x7ffa8ed2fdcb in content::mojom::FrameHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.cc:5164  

#14 0x7ffa96839b11 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:898  

#15 0x7ffa98ffd489 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#16 0x7ffa9683d39c in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:655  

#17 0x7ffa9709126a in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:981  

#18 0x7ffa9708b161 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#19 0x7ffa964eb6ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#20 0x7ffa98eba492 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#21 0x7ffa98eb9af2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#22 0x7ffa965958a6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#23 0x7ffa96593a18 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#24 0x7ffa98ebb97e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#25 0x7ffa9646d9c3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#26 0x7ffa8faa9627 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:987  

#27 0x7ffa8faae9a1 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152  

#28 0x7ffa8faa2c52 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:47  

#29 0x7ffa922f5558 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:595  

#30 0x7ffa922f7ff6 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1086  

#31 0x7ffa922f7152 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:953  

#32 0x7ffa922f441e in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:386  

#33 0x7ffa922f4a1f in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:412  

#34 0x7ffa8bd6145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:151  

#35 0x7ff677415b74 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#36 0x7ff677412be8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#37 0x7ff67780158f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#38 0x7ffb24e57033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#39 0x7ffb25102650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x122017f320f8 is located 184 bytes inside of 200-byte region [0x122017f32040,0x122017f32108)  

freed by thread T0 here:  

#0 0x7ff6774b5f4b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffaa5e95108 in payments::PaymentCredentialEnrollmentBridgeDesktop::~PaymentCredentialEnrollmentBridgeDesktop C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_bridge\_desktop.cc:32  

#2 0x7ffaa4da9318 in payments::PaymentCredentialEnrollmentController::OnResponse C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_controller.cc:100  

#3 0x7ffaa6af701e in payments::PaymentCredentialEnrollmentDialogView::OnDialogClosed C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\payments\payment\_credential\_enrollment\_dialog\_view.cc:99  

#4 0x7ffa9bd8bb58 in views::DialogDelegate::WindowWillClose C:\b\s\w\ir\cache\builder\src\ui\views\window\dialog\_delegate.cc:228  

#5 0x7ffa9626f682 in views::WidgetDelegate::WindowWillClose C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget\_delegate.cc:215  

#6 0x7ffa9625eabe in views::Widget::CloseWithReason C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:674  

#7 0x7ffaa5e9508f in payments::PaymentCredentialEnrollmentBridgeDesktop::CloseDialog C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_bridge\_desktop.cc:87  

#8 0x7ffaa4da954f in payments::PaymentCredentialEnrollmentController::CloseDialog C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_controller.cc:77  

#9 0x7ffaa326b338 in payments::PaymentCredential::Reset C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:324  

#10 0x7ffaa326ae71 in payments::PaymentCredential::~PaymentCredential C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:48  

#11 0x7ffaa326eb79 in payments::PaymentCredential::~PaymentCredential C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:47  

#12 0x7ffa90937106 in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::RenderFrameHost \*),content::RenderFrameHostImpl \*&> C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:1476  

#13 0x7ffa909602c7 in content::WebContentsImpl::DidStartNavigation C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:5250  

#14 0x7ffa90499f42 in content::NavigationRequest::StartNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:2022  

#15 0x7ffa9049efc0 in content::NavigationRequest::BeginNavigationImpl C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:1758  

#16 0x7ffa9049dcd7 in content::NavigationRequest::BeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_request.cc:1585  

#17 0x7ffa904e8dae in content::Navigator::OnBeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:921  

#18 0x7ffa905463d9 in content::RenderFrameHostImpl::BeginNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:6647  

#19 0x7ffa8ed2fdcb in content::mojom::FrameHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\frame.mojom.cc:5164  

#20 0x7ffa96839b11 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:898  

#21 0x7ffa98ffd489 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#22 0x7ffa9683d39c in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:655  

#23 0x7ffa9709126a in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:981  

#24 0x7ffa9708b161 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#25 0x7ffa964eb6ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#26 0x7ffa98eba492 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#27 0x7ffa98eb9af2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260

previously allocated by thread T0 here:  

#0 0x7ff6774b604b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffaa88c7d6a in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffaa5e94526 in payments::PaymentCredentialEnrollmentBridge::Create C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_bridge\_desktop.cc:25  

#3 0x7ffaa4da8c74 in payments::PaymentCredentialEnrollmentController::ShowDialog C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential\_enrollment\_controller.cc:58  

#4 0x7ffaa326d20c in payments::PaymentCredential::DidDownloadIcon C:\b\s\w\ir\cache\builder\src\components\payments\content\payment\_credential.cc:251  

#5 0x7ffaa326f2db in base::internal::Invoker<base::internal::BindState<void (payments::PaymentCredential::\*)(std::\_\_1::u16string, int, int, const GURL &, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &),base::WeakPtr[payments::PaymentCredential](javascript:void(0);),std::\_\_1::u16string>,void (int, int, const GURL &, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#6 0x7ffa9095db93 in content::WebContentsImpl::OnDidDownloadImage C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:7910  

#7 0x7ffa9099ed4e in base::internal::FunctorTraits<void (content::WebContentsImpl::\*)(base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), base::OnceCallback<void (int, int, const GURL &, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &)>, int, const GURL &, int, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &),void>::Invoke<void (content::WebContentsImpl::\*)(base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), base::OnceCallback<void (int, int, const GURL &, const std::vector<SkBitmap> &, const std::vector[gfx::Size](javascript:void(0);) &)>, int, const GURL &, int, const std::vector<SkBitmap> &, const std::vector[gfx::Size](javascript:void(0);) &),base::WeakPtr[content::WebContentsImpl](javascript:void(0);),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),base::OnceCallback<void (int, int, const GURL &, const std::vector<SkBitmap> &, const std::vector[gfx::Size](javascript:void(0);) &)>,int,GURL,int,const std::vector<SkBitmap> &,const std::vector[gfx::Size](javascript:void(0);) &> C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:509  

#8 0x7ffa9099f402 in base::internal::Invoker<base::internal::BindState<void (content::WebContentsImpl::\*)(base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);), base::OnceCallback<void (int, int, const GURL &, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &)>, int, const GURL &, int, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &),base::WeakPtr[content::WebContentsImpl](javascript:void(0);),base::WeakPtr[content::RenderFrameHostImpl](javascript:void(0);),base::OnceCallback<void (int, int, const GURL &, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &)>,int,GURL>,void (int, const std::\_\_1::vector<SkBitmap,std::\_\_1::allocator<SkBitmap> > &, const std::\_\_1::vector<gfx::Size,std::\_\_1::allocator[gfx::Size](javascript:void(0);) > &)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:690  

#9 0x7ffa8e95e13c in blink::mojom::ImageDownloader\_DownloadImage\_ForwardToCallback::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\image\_downloader\image\_downloader.mojom.cc:218  

#10 0x7ffa96839985 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:893  

#11 0x7ffa98ffd576 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#12 0x7ffa9683d39c in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:655  

#13 0x7ffa96851801 in mojo::internal::MultiplexRouter::ProcessIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1099  

#14 0x7ffa96850593 in mojo::internal::MultiplexRouter::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:719  

#15 0x7ffa98ffd576 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#16 0x7ffa968348d2 in mojo::Connector::DispatchMessageW C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:546  

#17 0x7ffa9683611f in mojo::Connector::ReadAllAvailableMessages C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\connector.cc:604  

#18 0x7ffa96886076 in mojo::SimpleWatcher::OnHandleReady C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#19 0x7ffa964eb6ba in base::TaskAnnotator::RunTask C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:178  

#20 0x7ffa98eba492 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:360  

#21 0x7ffa98eb9af2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:260  

#22 0x7ffa965958a6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#23 0x7ffa96593a18 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#24 0x7ffa98ebb97e in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:467  

#25 0x7ffa9646d9c3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#26 0x7ffa8faa9627 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:987  

#27 0x7ffa8faae9a1 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:152

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:250 in scoped\_refptr<const base::internal::WeakReference::Flag>::operator=  

Shadow bytes around the buggy address:  

0x04421ace63c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04421ace63d0: fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa  

0x04421ace63e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x04421ace63f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa  

0x04421ace6400: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

=>0x04421ace6410: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]  

0x04421ace6420: fd fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x04421ace6430: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x04421ace6440: 00 00 00 00 00 00 00 00 00 00 00 fa fa fa fa fa  

0x04421ace6450: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x04421ace6460: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

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

==9760==ABORTING

C:\chromium\_version\asan-win32-release\_x64-902866>

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 19.4 KB)
- [confirm.html](attachments/confirm.html) (text/plain, 1.6 KB)
- [confirm.js](attachments/confirm.js) (text/plain, 1.3 KB)
- [pay.gif](attachments/pay.gif) (image/gif, 7.7 MB)

## Timeline

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### jd...@chromium.org (2021-07-19)

1. I can't reproduce this easily because my Windows machine is having a rough day, evidently.
2. This PoC looks pretty basic. That suggests that this may be trunk churn. Does this reproduce in Beta or Stable?
3. I'm assuming the use of --enable-experimental-web-platform-features is required, and so this is Impact-None (and thus not rewardable). If it doesn't require that flag, please let me know and we'll update accordingly.

rouslan@: can you please take a look? Feel free to re-assign to a more appropriate person if needed. Thanks!

[Monorail components: Blink>Payments]

### jd...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-07-19)

jdeblasio@ - This feature is in origin trial from M91 to M94, so any website owner could enable it without the need for --enable-experimental-web-platform-features flag. I'm looking into this.

### jd...@chromium.org (2021-07-19)

Thanks for the update. If that's the case, than this would be a web-accessible UaF in the browser process, which is severity-critical. Updating it as such.

### ad...@google.com (2021-07-19)

Yep. rouslan@ can we cancel the origin trial for a couple of weeks? Otherwise we'll need to let the release TPMs know that they'll need to recut the M92 release to include a fix for this and that will make them Sad.

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-07-19)

adetaylor@ - Out of curiosity, where is the "couple of weeks" timeline coming from?

### sm...@chromium.org (2021-07-19)

> Yep. rouslan@ can we cancel the origin trial for a couple of weeks? Otherwise we'll need to let the release TPMs know that they'll need to recut the M92 release to include a fix for this and that will make them Sad.

(Hi, Web Payments lead here :))

I would want to discuss this with the release TPMs (but let's make sure we can actually reproduce, and on M92, first). Turning down the origin trial for multiple weeks (I presume until the next stable refresh) would be invasive to our multiple partners who are using this Origin Trial, and I would want to make sure we balance that against the general pain of holding a release.

### ro...@chromium.org (2021-07-19)

So far https://rsolomakhin.github.io/pr/test2/confirm.html is not crashing my Chrome 91 stable. Is that because UAF is not user visible?

### ro...@chromium.org (2021-07-19)

(on Mac)

### sm...@chromium.org (2021-07-19)

> So far https://rsolomakhin.github.io/pr/test2/confirm.html is not crashing my Chrome 91 stable. Is that because UAF is not user visible?

Quite likely. You need to use an ASAN build to determine whether or not it reproduces. I think we have pre-built binaries available; https://commondatastorage.googleapis.com/chromium-browser-asan/index.html 

### ad...@google.com (2021-07-19)

> couple of weeks

Because we do a stable security refresh every two weeks, and so I expect we'd be able to roll the fix into the first M92 security refresh.



### go...@chromium.org (2021-07-19)

Applying "RBS" label for tracking this bug for future M92 refresh.

This  will need a Postmortem as Severity=Critical impacting Stable, correct +adetaylor@?

### sm...@chromium.org (2021-07-19)

We are still trying to reproduce, but we believe that this may have been introduced in https://crrev.com/0647faa3549084fd6235b77b6fde81621e7a7eb3 which landed in M93 and should not be in M92. *THIS IS NOT CONFIRMED YET*

### ro...@chromium.org (2021-07-19)

Confirmed that the ASAN build of Chrome 92.0.4515.0 does not have this issue, while Chrome 93.0.4573.0 does. More details here:

https://docs.google.com/document/d/1_an1Qt9vUjlFAGnKDNzT-OdLMRKdJ8v-9X1q7o3PP2k

Suspected CL landed in M93 - https://chromiumdash.appspot.com/commit/0647faa3549084fd6235b77b6fde81621e7a7eb3, which is currently in Dev. Removing M-92 and FoundIn-91 labels.

Please help to re-triage the security labels and confirm that there is no need for a postmortem.

### [Deleted User] (2021-07-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-19)

Great! The labels are duly adjusted.

### ro...@chromium.org (2021-07-19)

Is this Pri-1 in that case, @adetaylor? Is the severity set correctly?

### ad...@google.com (2021-07-19)

Yes. It remains Critical in terms of the consequences for users. Critical bugs are rare and they are all pri-0.

It's just that it currently only affects canary/dev users rather than stable users. It's also still a release blocker for M93 (of course). In fact, I _think_ Sheriffbot will label this ReleaseBlock-Beta tomorrow too - that's normal for Critical bugs. i.e. we won't be able to promote M93 to beta until this is fixed, so there remains significant urgency.

### ro...@chromium.org (2021-07-20)

Writing a browser test that reproduces this uaf.

### ro...@chromium.org (2021-07-20)

The patch at https://crrev.com/c/3042519 contains a new browser test case that reproduces the UAF under ASAN build.

### ro...@chromium.org (2021-07-20)

https://crrev.com/c/3042519 now has the fix and is out for review. The fix is preventing the UAF in the browser tests on my local ASAN build, but the bots on the code review website have not caught up yet.

### gi...@appspot.gserviceaccount.com (2021-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/60d431517f7a58c313b0de2567213df685fb60ae

commit 60d431517f7a58c313b0de2567213df685fb60ae
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Tue Jul 20 23:13:50 2021

[SPC] Correctly handle page closing during enrollment.

Before this patch, closing or reloading the page while the browser
enrollment dialog for SPC was opened would cause a use after free
condition in the UI controller, because the UI controller could cause
itself to be deleted in the middle of its own CloseDialog() method due
to re-entrancy.

This patch makes PaymentCredentialEnrollmentController::CloseDialog()
handle re-entry into itself safely.

After this patch, closing or reloading the page while the browser
enrollment dialog for SPC is opened will not cause a use after free
condition in the UI controller.

Bug: 1230530
Cq-Include-Trybots: luci.chromium.try:win-asan,mac_chromium_asan_rel_ng
Change-Id: I3d3c31b3ca8908d841633317976e9f04b2118bcb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3042519
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#903687}

[modify] https://crrev.com/60d431517f7a58c313b0de2567213df685fb60ae/chrome/browser/payments/secure_payment_confirmation_browsertest.cc
[modify] https://crrev.com/60d431517f7a58c313b0de2567213df685fb60ae/components/payments/content/payment_credential_enrollment_controller.cc


### ro...@chromium.org (2021-07-20)

[Empty comment from Monorail migration]

### ro...@chromium.org (2021-07-21)

Do I need to mark the bug fixed for the merge request to be visible to the approvers?

### ma...@chromium.org (2021-07-21)

+benmason@ for M93 merge review. Thank you.

### ad...@google.com (2021-07-21)

Re https://crbug.com/chromium/1230530#c28 yes please - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels

### ma...@chromium.org (2021-07-21)

Yes. I've just reread the discussion about it. The concensus is that we should mark fixed before requesting a merge, meaning that all issues have been cleared.

### ad...@chromium.org (2021-07-21)

Thanks, approving merge to M93, branch 4577.

### ro...@chromium.org (2021-07-21)

Thank you. Requesting @maxlg to review the merge patch in https://crrev.com/c/3044000.

### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/09982563b47ed3b42cc04628b9203d957009efd8

commit 09982563b47ed3b42cc04628b9203d957009efd8
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Wed Jul 21 16:55:38 2021

[Merge M93][SPC] Correctly handle page closing during enrollment.

Before this patch, closing or reloading the page while the browser
enrollment dialog for SPC was opened would cause a use after free
condition in the UI controller, because the UI controller could cause
itself to be deleted in the middle of its own CloseDialog() method due
to re-entrancy.

This patch makes PaymentCredentialEnrollmentController::CloseDialog()
handle re-entry into itself safely.

After this patch, closing or reloading the page while the browser
enrollment dialog for SPC is opened will not cause a use after free
condition in the UI controller.

(cherry picked from commit 60d431517f7a58c313b0de2567213df685fb60ae)

Bug: 1230530
Change-Id: I3d3c31b3ca8908d841633317976e9f04b2118bcb
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3042519
Reviewed-by: Liquan (Max) Gu <maxlg@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#903687}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3044000
Cr-Commit-Position: refs/branch-heads/4577@{#52}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/09982563b47ed3b42cc04628b9203d957009efd8/chrome/browser/payments/secure_payment_confirmation_browsertest.cc
[modify] https://crrev.com/09982563b47ed3b42cc04628b9203d957009efd8/components/payments/content/payment_credential_enrollment_controller.cc


### [Deleted User] (2021-07-21)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-07-28)

Congratulations! The VRP Panel has decided to award you $20,000 fro this report. Excellent work! 

### am...@google.com (2021-07-29)

[Empty comment from Monorail migration]

### ad...@google.com (2021-08-06)

rouslan@ as you might be aware, Critical security bugs are unusual, so we ask for a post-mortem on each such bug. Would you mind kicking one off? It would be interesting to know what we could have done better to avoid this (e.g. are there areas which should have fuzzing coverage? Could more code be sandboxed? Are there code patterns which should be made more robust to error? etc.)

### ro...@chromium.org (2021-08-06)

I will start the postmortem.

### vo...@google.com (2021-10-24)

Marking as not applicable for M90 LTS since the problem emerged in M93.

### [Deleted User] (2021-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1230530?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056586)*
