# Security: heap-use-after-free in the media::AudioManagerBase in the browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40057977](https://issues.chromium.org/issues/40057977) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ag...@chromium.org |
| **Created** | 2021-11-20 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

Heap-use-after-free(Windows) vulnerability in the MediaStreamDispatcherHost mojo interface

This poc can alse triger a container-overflow(Windows&&Linux) asan crash.

**VERSION**  

Chrome Version: Version 98.0.4719.0 (Developer Build) (64-bit)  

Operating System: [Windows && Linux]

**REPRODUCTION CASE**

Download the latest asan build from gs://chromium-browser-asan/win32-release\_x64/asan-win32-release\_x64-943819.zip

Cope the mojo js to the website && python -m http.server 80

Then run:  

asan-win32-release\_x64-943819>chrome.exe --user-data-dir=c:/tmp/asdf --enable-blink-features=MojoJS,MojoJSTest <http://localhost/poc.html>

This poc can be triggered stably in the latest dev version in the Windows&&Linux.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

UAF Asan log:

> chrome.exe --user-data-dir=c:/tmp/asdf --enable-blink-features=MojoJS,MojoJSTest <http://localhost/poc1.html>  
> 
> =================================================================  
> 
> ==1680==ERROR: AddressSanitizer: heap-use-after-free on address 0x1246c58bd400 at pc 0x7ffb1700117f bp 0x0067589fe530 sp 0x0067589fe578  
> 
> READ of size 8 at 0x1246c58bd400 thread T0  
> 
> ==1680==WARNING: Failed to use and restart external symbolizer!  
> 
> #0 0x7ffb1700117e in media::AudioManagerBase::`vcall'{168}'+0x3e (C:\chromium_version\asan-win32-release_x64-943819\chrome.dll+0x18240117e) #1 0x7ffb197c1969 in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(double),double> C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.h:1493 #2 0x7ffb197c1308 in content::WebContentsImpl::SendChangeLoadProgress C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:6425 #3 0x7ffb197cf959 in content::WebContentsImpl::DidChangeLoadProgress C:\b\s\w\ir\cache\builder\src\content\browser\web_contents\web_contents_impl.cc:7274 #4 0x7ffb17595f66 in blink::mojom::LocalFrameHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\public\mojom\frame\frame.mojom.cc:5480 #5 0x7ffb1fa60711 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:900 #6 0x7ffb223a0505 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:48 #7 0x7ffb1fa63f88 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657 #8 0x7ffb202eccb0 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1004  
> 
> #9 0x7ffb202e6a51 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  
> 
> #10 0x7ffb1f7122a4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  
> 
> #11 0x7ffb22259f85 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  
> 
> #12 0x7ffb22259658 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  
> 
> #13 0x7ffb1f7b81e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  
> 
> #14 0x7ffb1f7b6478 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  
> 
> #15 0x7ffb2225b655 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  
> 
> #16 0x7ffb1f6922f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  
> 
> #17 0x7ffb188b54b2 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1001  
> 
> #18 0x7ffb188ba861 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  
> 
> #19 0x7ffb188aef4a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  
> 
> #20 0x7ffb1b2f0b9b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  
> 
> #21 0x7ffb1b2f3c69 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1159  
> 
> #22 0x7ffb1b2f2d9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  
> 
> #23 0x7ffb1b2eef15 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  
> 
> #24 0x7ffb1b2effe2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  
> 
> #25 0x7ffb14c0148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  
> 
> #26 0x7ff6b1d35b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  
> 
> #27 0x7ff6b1d32c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  
> 
> #28 0x7ff6b2132dff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  
> 
> #29 0x7ffbc7b97033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  
> 
> #30 0x7ffbc81c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x1246c58bd400 is located 0 bytes inside of 24-byte region [0x1246c58bd400,0x1246c58bd418)  

freed by thread T11 here:  

#0 0x7ff6b1de247b in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffb19216600 in base::OnceCallback<void (std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) >)>::Run C:\b\s\w\ir\cache\builder\src\base\callback.h:143  

#2 0x7ffb19216078 in base::internal::ReplyAdapter<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) >,std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) > > C:\b\s\w\ir\cache\builder\src\base\task\post\_task\_and\_reply\_with\_result\_internal.h:30  

#3 0x7ffb192163dc in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) > ()>, std::\_\_1::unique\_ptr<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) >,std::\_\_1::default\_delete<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) > > > \*),base::OnceCallback<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) > ()>,base::internal::UnretainedWrapper<std::\_\_1::unique\_ptr<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) >,std::\_\_1::default\_delete<std::\_\_1::unique\_ptr<content::MediaStreamWebContentsObserver,std::\_\_1::default\_delete[content::MediaStreamWebContentsObserver](javascript:void(0);) > > > > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#4 0x7ffb222546cb in base::`anonymous namespace'::PostTaskAndReplyRelay::RunReply C:\b\s\w\ir\cache\builder\src\base\threading\post_task_and_reply_impl.cc:118 #5 0x7ffb22254923 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #6 0x7ffb1f7122a4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task_annotator.cc:135 #7 0x7ffb22259f85 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:356 #8 0x7ffb22259658 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:261 #9 0x7ffb1f7bc004 in base::MessagePumpForIO::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:720 #10 0x7ffb1f7b6478 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc:78 #11 0x7ffb2225b655 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc:468 #12 0x7ffb1f6922f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run_loop.cc:140 #13 0x7ffb1f7582b9 in base::Thread::Run C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:334 #14 0x7ffb188bdb57 in content::BrowserProcessIOThread::IOThreadRun C:\b\s\w\ir\cache\builder\src\content\browser\browser_process_io_thread.cc:133 #15 0x7ffb1f7587d0 in base::Thread::ThreadMain C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:405 #16 0x7ffb1f7d979f in base::`anonymous namespace'::ThreadFunc C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:121  

#17 0x7ff6b1deda23 in \_\_asan::AsanThread::ThreadStart C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_thread.cpp:278  

#18 0x7ffbc7b97033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#19 0x7ffbc81c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

previously allocated by thread T0 here:  

#0 0x7ff6b1de257b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffb320d39fe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffb192109d7 in content::`anonymous namespace'::StartObservingWebContents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\media\media_stream_dispatcher_host.cc:57 #3 0x7ffb19215cce in base::internal::Invoker<base::internal::BindState<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > (\*)(int, int, base::RepeatingCallback<void ()>),int,int,base::RepeatingCallback<void ()> >,std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #4 0x7ffb19216215 in base::internal::ReturnAsParamAdapter<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > C:\b\s\w\ir\cache\builder\src\base\task\post_task_and_reply_with_result_internal.h:22 #5 0x7ffb192163dc in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>, std::__1::unique_ptr<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> >,std::__1::default_delete<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > > \*),base::OnceCallback<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>,base::internal::UnretainedWrapper<std::__1::unique_ptr<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> >,std::__1::default_delete<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > > > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #6 0x7ffb222540df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#7 0x7ffb22254923 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#8 0x7ffb1f7122a4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#9 0x7ffb22259f85 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#10 0x7ffb22259658 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#11 0x7ffb1f7b81e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#12 0x7ffb1f7b6478 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7ffb2225b655 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#14 0x7ffb1f6922f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#15 0x7ffb188b54b2 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1001  

#16 0x7ffb188ba861 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#17 0x7ffb188aef4a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#18 0x7ffb1b2f0b9b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#19 0x7ffb1b2f3c69 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1159  

#20 0x7ffb1b2f2d9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#21 0x7ffb1b2eef15 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#22 0x7ffb1b2effe2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#23 0x7ffb14c0148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#24 0x7ff6b1d35b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#25 0x7ff6b1d32c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#26 0x7ff6b2132dff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ffbc7b97033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)

Thread T11 created by T0 here:  

#0 0x7ff6b1dee4b2 in \_\_asan\_wrap\_CreateThread C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_win.cpp:146  

#1 0x7ffb1f7d8b7e in base::`anonymous namespace'::CreateThreadInternal C:\b\s\w\ir\cache\builder\src\base\threading\platform\_thread\_win.cc:185  

#2 0x7ffb1f757503 in base::Thread::StartWithOptions C:\b\s\w\ir\cache\builder\src\base\threading\thread.cc:209  

#3 0x7ffb19502775 in content::BrowserTaskExecutor::CreateIOThread C:\b\s\w\ir\cache\builder\src\content\browser\scheduler\browser\_task\_executor.cc:399  

#4 0x7ffb1b2f3691 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1130  

#5 0x7ffb1b2f2d9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#6 0x7ffb1b2eef15 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#7 0x7ffb1b2effe2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#8 0x7ffb14c0148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#9 0x7ff6b1d35b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#10 0x7ff6b1d32c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#11 0x7ff6b2132dff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#12 0x7ffbc7b97033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#13 0x7ffbc81c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

SUMMARY: AddressSanitizer: heap-use-after-free (C:\chromium\_version\asan-win32-release\_x64-943819\chrome.dll+0x18240117e) in media::AudioManagerBase::`vcall'{168}'+0x3e  

Shadow bytes around the buggy address:  

0x04899e117a30: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x04899e117a40: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa  

0x04899e117a50: fd fd fd fa fa fa fd fd fd fd fa fa fd fd fd fd  

0x04899e117a60: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x04899e117a70: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa  

=>0x04899e117a80:[fd]fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa  

0x04899e117a90: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x04899e117aa0: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa  

0x04899e117ab0: fd fd fd fa fa fa fd fd fd fa fa fa fd fd fd fa  

0x04899e117ac0: fa fa fd fd fd fa fa fa fd fd fd fa fa fa fd fd  

0x04899e117ad0: fd fa fa fa fd fd fd fa fa fa fd fd fd fa fa fa  

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

==1680==ABORTING

# Container-overflow asan log: chrome.exe --user-data-dir=c:/tmp/asdf --enable-blink-features=MojoJS,MojoJSTest <http://localhost/poc1.html>

==16208==ERROR: AddressSanitizer: container-overflow on address 0x124391441ed8 at pc 0x7ffb1977006b bp 0x0072c93fe9e0 sp 0x0072c93fea28  

READ of size 8 at 0x124391441ed8 thread T0  

==16208==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffb1977006a in base::ObserverList[content::WebContentsObserver,0,1,base::internal::UncheckedObserverAdapter](javascript:void(0);)::AddObserver C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:271  

#1 0x7ffb18436725 in content::WebContentsObserver::WebContentsObserver C:\b\s\w\ir\cache\builder\src\content\public\browser\web\_contents\_observer.cc:13  

#2 0x7ffb18f93a38 in content::MediaStreamWebContentsObserver::MediaStreamWebContentsObserver C:\b\s\w\ir\cache\builder\src\content\browser\media\media\_stream\_web\_contents\_observer.cc:16  

#3 0x7ffb19210a21 in content::`anonymous namespace'::StartObservingWebContents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\media\media_stream_dispatcher_host.cc:57 #4 0x7ffb19215cce in base::internal::Invoker<base::internal::BindState<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > (\*)(int, int, base::RepeatingCallback<void ()>),int,int,base::RepeatingCallback<void ()> >,std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #5 0x7ffb19216215 in base::internal::ReturnAsParamAdapter<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > C:\b\s\w\ir\cache\builder\src\base\task\post_task_and_reply_with_result_internal.h:22 #6 0x7ffb192163dc in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>, std::__1::unique_ptr<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> >,std::__1::default_delete<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > > \*),base::OnceCallback<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>,base::internal::UnretainedWrapper<std::__1::unique_ptr<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> >,std::__1::default_delete<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > > > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #7 0x7ffb222540df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#8 0x7ffb22254923 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#9 0x7ffb1f7122a4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#10 0x7ffb22259f85 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#11 0x7ffb22259658 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#12 0x7ffb1f7b81e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#13 0x7ffb1f7b6478 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#14 0x7ffb2225b655 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#15 0x7ffb1f6922f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#16 0x7ffb188b54b2 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1001  

#17 0x7ffb188ba861 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#18 0x7ffb188aef4a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#19 0x7ffb1b2f0b9b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#20 0x7ffb1b2f3c69 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1159  

#21 0x7ffb1b2f2d9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#22 0x7ffb1b2eef15 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#23 0x7ffb1b2effe2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#24 0x7ffb14c0148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172  

#25 0x7ff6b1d35b45 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#26 0x7ff6b1d32c31 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#27 0x7ff6b2132dff in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#28 0x7ffbc7b97033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#29 0x7ffbc81c2650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x124391441ed8 is located 1496 bytes inside of 8192-byte region [0x124391441900,0x124391443900)  

allocated by thread T0 here:  

#0 0x7ff6b1de257b in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffb320d39fe in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffb15005221 in std::\_\_1::vector<base::internal::UncheckedObserverAdapter,std::\_\_1::allocator[base::internal::UncheckedObserverAdapter](javascript:void(0);) >::\_\_emplace\_back\_slow\_path[base::internal::UncheckedObserverAdapter](javascript:void(0);) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1666  

#3 0x7ffb19770000 in base::ObserverList[content::WebContentsObserver,0,1,base::internal::UncheckedObserverAdapter](javascript:void(0);)::AddObserver C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:276  

#4 0x7ffb18436725 in content::WebContentsObserver::WebContentsObserver C:\b\s\w\ir\cache\builder\src\content\public\browser\web\_contents\_observer.cc:13  

#5 0x7ffb18f93a38 in content::MediaStreamWebContentsObserver::MediaStreamWebContentsObserver C:\b\s\w\ir\cache\builder\src\content\browser\media\media\_stream\_web\_contents\_observer.cc:16  

#6 0x7ffb19210a21 in content::`anonymous namespace'::StartObservingWebContents C:\b\s\w\ir\cache\builder\src\content\browser\renderer_host\media\media_stream_dispatcher_host.cc:57 #7 0x7ffb19215cce in base::internal::Invoker<base::internal::BindState<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > (\*)(int, int, base::RepeatingCallback<void ()>),int,int,base::RepeatingCallback<void ()> >,std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #8 0x7ffb19216215 in base::internal::ReturnAsParamAdapter<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > C:\b\s\w\ir\cache\builder\src\base\task\post_task_and_reply_with_result_internal.h:22 #9 0x7ffb192163dc in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>, std::__1::unique_ptr<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> >,std::__1::default_delete<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > > \*),base::OnceCallback<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > ()>,base::internal::UnretainedWrapper<std::__1::unique_ptr<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> >,std::__1::default_delete<std::__1::unique_ptr<content::MediaStreamWebContentsObserver,std::__1::default_delete<content::MediaStreamWebContentsObserver> > > > > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #10 0x7ffb222540df in base::`anonymous namespace'::PostTaskAndReplyRelay::RunTaskAndPostReply C:\b\s\w\ir\cache\builder\src\base\threading\post\_task\_and\_reply\_impl.cc:100  

#11 0x7ffb22254923 in base::internal::Invoker<base::internal::BindState<void (\*)(base::(anonymous namespace)::PostTaskAndReplyRelay),base::(anonymous namespace)::PostTaskAndReplyRelay>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#12 0x7ffb1f7122a4 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135  

#13 0x7ffb22259f85 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#14 0x7ffb22259658 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#15 0x7ffb1f7b81e6 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:220  

#16 0x7ffb1f7b6478 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#17 0x7ffb2225b655 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#18 0x7ffb1f6922f3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#19 0x7ffb188b54b2 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1001  

#20 0x7ffb188ba861 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#21 0x7ffb188aef4a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#22 0x7ffb1b2f0b9b in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#23 0x7ffb1b2f3c69 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1159  

#24 0x7ffb1b2f2d9e in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#25 0x7ffb1b2eef15 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#26 0x7ffb1b2effe2 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#27 0x7ffb14c0148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:172

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.  

If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.  

SUMMARY: AddressSanitizer: container-overflow C:\b\s\w\ir\cache\builder\src\base\observer\_list.h:271 in base::ObserverList[content::WebContentsObserver,0,1,base::internal::UncheckedObserverAdapter](javascript:void(0);)::AddObserver  

Shadow bytes around the buggy address:  

0x044203508380: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x044203508390: 00 00 00 00 00 00 00 00 00 00 00 00 00 fc fc fc  

0x0442035083a0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0442035083b0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0442035083c0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

=>0x0442035083d0: fc fc fc fc fc fc fc fc fc fc fc[fc]fc fc fc fc  

0x0442035083e0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x0442035083f0: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x044203508400: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x044203508410: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

0x044203508420: fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc fc  

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

==16208==ABORTING

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 667 B)
- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 514 B)

## Timeline

### [Deleted User] (2021-11-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2021-11-23)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6719568669900800.

### mp...@chromium.org (2021-11-23)

I think there's a typo in copy_mojo_js_bindings.py, it creates a directory called "en" rather than "gen" within the current directory.

With that fixed, putting the attached files in the current working directory and then running
./copy_mojo_js_bindings.py ~/chromium/src/out/Asan
python -m http.server 80

This successfully reproduces on 98, but not 97.


### mp...@chromium.org (2021-11-23)

Looks like if when we run this code [1] which runs on the IO thread:

  base::PostTaskAndReplyWithResult(
      GetUIThreadTaskRunner({}).get(), FROM_HERE,
      base::BindOnce(&StartObservingWebContents, render_process_id_,
                     render_frame_id_, std::move(focus_callback)),
      base::BindOnce(&MediaStreamDispatcherHost::SetWebContentsObserver,
                     weak_factory_.GetWeakPtr()));

...the first callback passes a unique_ptr<MediaStreamWebContentsObserver> (which is only ever supposed to be created/used/destroyed on the UI thread) to the second callback (which runs on the IO thread). But the WeakPtr may already be invalid (e.g. if a reload happened. Or, since MediaStreamDispatcherHost is a SelfOwnedReceiver, a compromised renderer can delete the MediaStreamDispatcherHost directly). If the weak ptr is invalid, the callback never runs, so the callback's parameters (including the unique_ptr<MediaStreamWebContentsObserver>) are just dropped, on the IO thread. This class MediaStreamWebContentsObserver is only supposed to be destroyed on the UI thread, so race conditions occur, including this UAF and the container overflow.

[1] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/media/media_stream_dispatcher_host.cc;drc=de68be3f18ba99cc01d75903e167ca09bade253c;l=111-116

[Monorail components: Blink>GetUserMedia]

### [Deleted User] (2021-11-23)

[Empty comment from Monorail migration]

### ag...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-11-23)

Firing at https://crbug.com/chromium/1272208#c4 from the hip, I wonder if replacing the second callback with this could be a quick and dirty workaround:

  base::BindOnce([](std::unique_ptr<MediaStreamWebContentsObserver> observer,
                    base::WeakPtr<MediaStreamDispatcherHost> host) {
    if (host) {
      host->SetWebContentsObserver(std::move(observer));
    } else {  // WeakPtr invalidated.
      GetUIThreadTaskRunner({})->PostTask(
          FROM_HERE,
          base::BindOnce(
              [](std::unique_ptr<MediaStreamWebContentsObserver> observer) {
                // Drop |observer| on UI thread.
              },
              std::move(observer)));
    }
  })


### el...@chromium.org (2021-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-23)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-23)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### el...@chromium.org (2021-11-23)

There is a CL for this under review: https://chromium-review.googlesource.com/c/chromium/src/+/3284649

### gi...@appspot.gserviceaccount.com (2021-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/30504d2fcb3ee9f87d23380056d5ff664cc706fe

commit 30504d2fcb3ee9f87d23380056d5ff664cc706fe
Author: Palak Agarwal <agpalak@chromium.org>
Date: Mon Nov 29 22:35:11 2021

MediaStreamWebContentsObserver destructor should be called on UI thread

This CL removes the bug where it was possible for
unique_ptr<MediaStreamWebContentsObserver> to go out of scope on the IO
thread and thus also triggering its destructor on the IO thread.

Bug: 1272208, 1270128
Change-Id: I8eccceeb9828534b4623302c8a96032ddebc0ffa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3284649
Reviewed-by: Elad Alon <eladalon@chromium.org>
Reviewed-by: Dave Tapuska <dtapuska@chromium.org>
Reviewed-by: Matthew Denton <mpdenton@chromium.org>
Commit-Queue: Palak Agarwal <agpalak@chromium.org>
Cr-Commit-Position: refs/heads/main@{#946182}

[modify] https://crrev.com/30504d2fcb3ee9f87d23380056d5ff664cc706fe/content/browser/renderer_host/media/media_stream_dispatcher_host.h
[modify] https://crrev.com/30504d2fcb3ee9f87d23380056d5ff664cc706fe/content/browser/renderer_host/media/media_stream_dispatcher_host.cc


### ag...@chromium.org (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-30)

[Empty comment from Monorail migration]

### am...@google.com (2021-12-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-12-06)

Congratulations! The VRP Panel has decided to award you $15,000 for this report. Thank you for your efforts and excellent work!

### am...@google.com (2021-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-11)

Not requesting merge to dev (M98) because latest trunk commit (946182) appears to be prior to dev branch point (950365). If this is incorrect, please replace the Merge-NA-98 label with Merge-Request-98. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1272208?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057977)*
