# Security: UAF in content::DevToolsSession::DispatchProtocolResponse (browser process)

| Field | Value |
|-------|-------|
| **Issue ID** | [40061096](https://issues.chromium.org/issues/40061096) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2022-09-22 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in content::DevToolsSession::DispatchProtocolResponse (browser process)

**VERSION**  

Chromium 107.0.5302.0 (Developer Build) (64-bit)  

Revision ee2eb524203f1f0266e55b786ff63c1f5970e06c-refs/heads/main@{#1047250}  

OS Windows 10 Version 21H2 (Build 19044.2006)

**REPRODUCTION CASE**  

I test this issue in Windows && ChromiumOS and it can both be triggered.

Exploit the Chrome DevTools Protocol to triger the UAF

1. run the command and will trigger the UAF  
   
   chrome --remote-debugging-port=9222 --user-data-dir=any --load-extension="extension\_path" <http://127.0.0.1>

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

=================================================================  

==22516==ERROR: AddressSanitizer: heap-use-after-free on address 0x127c01c6f658 at pc 0x7ffd37b74cce bp 0x00a6985fe890 sp 0x00a6985fe8d8  

READ of size 8 at 0x127c01c6f658 thread T0  

==22516==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffd37b74ccd in std::Cr::list<content::DevToolsSession::PendingMessage,std::Cr::allocator[content::DevToolsSession::PendingMessage](javascript:void(0);) >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\list:1712  

#1 0x7ffd37b7a26d in content::DevToolsSession::DispatchProtocolResponse C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:502  

#2 0x7ffd36a89ca0 in blink::mojom::DevToolsSessionHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\public\mojom\devtools\devtools\_agent.mojom.cc:1354  

#3 0x7ffd40006235 in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:989  

#4 0x7ffd42d5834e in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#5 0x7ffd4000a2de in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:689  

#6 0x7ffd405a7bb7 in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1010  

#7 0x7ffd405a0dec in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#8 0x7ffd3fd45fca in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:133  

#9 0x7ffd42bf7585 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#10 0x7ffd42bf6556 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#11 0x7ffd3fdf5396 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#12 0x7ffd3fdf33db in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7ffd42bf981b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:577  

#14 0x7ffd3fce13a2 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#15 0x7ffd379ad057 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1046  

#16 0x7ffd379b3267 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#17 0x7ffd379a60d1 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#18 0x7ffd3f87183f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:698  

#19 0x7ffd3f8748f1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1232  

#20 0x7ffd3f87418f in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1091  

#21 0x7ffd3f87001b in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:342  

#22 0x7ffd3f8706fe in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:370  

#23 0x7ffd338e14ac in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:182  

#24 0x7ff648525bfe in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:162  

#25 0x7ff648522bd7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:395  

#26 0x7ff64893d93f in \_\_scrt\_common\_main\_seh d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7ffdf0ed7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#28 0x7ffdf20a26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x127c01c6f658 is located 8 bytes inside of 72-byte region [0x127c01c6f650,0x127c01c6f698)  

freed by thread T0 here:  

#0 0x7ff6485cf95c in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffd37b74c77 in std::Cr::list<content::DevToolsSession::PendingMessage,std::Cr::allocator[content::DevToolsSession::PendingMessage](javascript:void(0);) >::erase C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\list:1732  

#2 0x7ffd37b799dd in content::DevToolsSession::ClearPendingMessages C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:456  

#3 0x7ffd37cef09d in content::RenderFrameDevToolsAgentHost::UpdateFrameAlive C:\b\s\w\ir\cache\builder\src\content\browser\devtools\render\_frame\_devtools\_agent\_host.cc:585  

#4 0x7ffd37cee57c in content::RenderFrameDevToolsAgentHost::UpdateFrameHost C:\b\s\w\ir\cache\builder\src\content\browser\devtools\render\_frame\_devtools\_agent\_host.cc:498  

#5 0x7ffd38b134d8 in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::WebContents \*, content::WebContents \*),content::WebContentsImpl \*,content::WebContentsImpl \*> C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:1551  

#6 0x7ffd38b50c35 in content::WebContentsImpl::NotifyFrameSwapped C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:6766  

#7 0x7ffd38b65eca in content::WebContentsImpl::NotifySwappedFromRenderManager C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:8110  

#8 0x7ffd38730012 in content::RenderFrameHostManager::CommitPending C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:3657  

#9 0x7ffd387378d1 in content::RenderFrameHostManager::GetFrameHostForNavigation C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:1246  

#10 0x7ffd387364fc in content::RenderFrameHostManager::DidCreateNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_manager.cc:1007  

#11 0x7ffd3843d200 in content::FrameTreeNode::CreatedNavigationRequest C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\frame\_tree\_node.cc:609  

#12 0x7ffd38642371 in content::Navigator::Navigate C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigator.cc:714  

#13 0x7ffd3859f766 in content::NavigationControllerImpl::NavigateToExistingPendingEntry C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_controller\_impl.cc:3195  

#14 0x7ffd3859d2ec in content::NavigationControllerImpl::Reload C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\navigation\_controller\_impl.cc:804  

#15 0x7ffd37c684a7 in content::protocol::PageHandler::Reload C:\b\s\w\ir\cache\builder\src\content\browser\devtools\protocol\page\_handler.cc:422  

#16 0x7ffd376cd84c in content::protocol::Page::DomainDispatcherImpl::reload C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\browser\devtools\protocol\page.cc:1288  

#17 0x7ffd3cbf73d8 in v8\_crdtp::UberDispatcher::DispatchResult::Run C:\b\s\w\ir\cache\builder\src\v8\third\_party\inspector\_protocol\crdtp\dispatch.cc:511  

#18 0x7ffd37b77c15 in content::DevToolsSession::HandleCommandInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:346  

#19 0x7ffd37b779eb in content::DevToolsSession::HandleCommand C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:332  

#20 0x7ffd37b80f03 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsSession::\*)(base::span<const unsigned char,18446744073709551615>),base::WeakPtr[content::DevToolsSession](javascript:void(0);) >,void (base::span<const unsigned char,18446744073709551615>)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#21 0x7ffd45fbc2c8 in ChromeDevToolsSession::HandleCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\chrome\_devtools\_session.cc:109  

#22 0x7ffd429c9e02 in ChromeDevToolsManagerDelegate::HandleCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\chrome\_devtools\_manager\_delegate.cc:141  

#23 0x7ffd37b773aa in content::DevToolsSession::DispatchProtocolMessageInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:323  

#24 0x7ffd37b76558 in content::DevToolsSession::DispatchProtocolMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:291  

#25 0x7ffd37b28189 in content::DevToolsAgentHostImpl::DispatchProtocolMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:251  

#26 0x7ffd37b40b81 in content::DevToolsHttpHandler::OnWebSocketMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_http\_handler.cc:795  

#27 0x7ffd37b47de4 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsHttpHandler::\*)(int, std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >),base::WeakPtr[content::DevToolsHttpHandler](javascript:void(0);),int,std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843

previously allocated by thread T0 here:  

#0 0x7ff6485cfa5c in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffd53a8dbee in operator new d:\a01\_work\12\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffd37b7883a in std::Cr::list<content::DevToolsSession::PendingMessage,std::Cr::allocator[content::DevToolsSession::PendingMessage](javascript:void(0);) >::emplace<int &,crdtp::span<unsigned char> &,crdtp::span<unsigned char> &> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\list:1617  

#3 0x7ffd37b785ae in content::DevToolsSession::FallThrough C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:359  

#4 0x7ffd376abf60 in content::protocol::Network::DomainDispatcherImpl::setExtraHTTPHeaders C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\browser\devtools\protocol\network.cc:2137  

#5 0x7ffd3cbf73d8 in v8\_crdtp::UberDispatcher::DispatchResult::Run C:\b\s\w\ir\cache\builder\src\v8\third\_party\inspector\_protocol\crdtp\dispatch.cc:511  

#6 0x7ffd37b77c15 in content::DevToolsSession::HandleCommandInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:346  

#7 0x7ffd37b779eb in content::DevToolsSession::HandleCommand C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:332  

#8 0x7ffd37b80f03 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsSession::\*)(base::span<const unsigned char,18446744073709551615>),base::WeakPtr[content::DevToolsSession](javascript:void(0);) >,void (base::span<const unsigned char,18446744073709551615>)>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#9 0x7ffd45fbc2c8 in ChromeDevToolsSession::HandleCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\chrome\_devtools\_session.cc:109  

#10 0x7ffd429c9e02 in ChromeDevToolsManagerDelegate::HandleCommand C:\b\s\w\ir\cache\builder\src\chrome\browser\devtools\chrome\_devtools\_manager\_delegate.cc:141  

#11 0x7ffd37b773aa in content::DevToolsSession::DispatchProtocolMessageInternal C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:323  

#12 0x7ffd37b76558 in content::DevToolsSession::DispatchProtocolMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_session.cc:291  

#13 0x7ffd37b28189 in content::DevToolsAgentHostImpl::DispatchProtocolMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_agent\_host\_impl.cc:251  

#14 0x7ffd37b40b81 in content::DevToolsHttpHandler::OnWebSocketMessage C:\b\s\w\ir\cache\builder\src\content\browser\devtools\devtools\_http\_handler.cc:795  

#15 0x7ffd37b47de4 in base::internal::Invoker<base::internal::BindState<void (content::DevToolsHttpHandler::\*)(int, std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> >),base::WeakPtr[content::DevToolsHttpHandler](javascript:void(0);),int,std::Cr::basic\_string<char,std::Cr::char\_traits<char>,std::Cr::allocator<char> > >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:843  

#16 0x7ffd3fd45fca in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:133  

#17 0x7ffd42bf7585 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:422  

#18 0x7ffd42bf6556 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:292  

#19 0x7ffd3fdf5396 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:214  

#20 0x7ffd3fdf33db in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#21 0x7ffd42bf981b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:577  

#22 0x7ffd3fce13a2 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:141  

#23 0x7ffd379ad057 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1046  

#24 0x7ffd379b3267 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:157  

#25 0x7ffd379a60d1 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#26 0x7ffd3f87183f in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:698  

#27 0x7ffd3f8748f1 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1232

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\list:1712 in std::Cr::list<content::DevToolsSession::PendingMessage,std::Cr::allocator[content::DevToolsSession::PendingMessage](javascript:void(0);) >::erase  

Shadow bytes around the buggy address:  

0x127c01c6f380: fd fa fa fa f7 fa fd fd fd fd fd fd fd fd fd fa  

0x127c01c6f400: fa fa f7 fa fd fd fd fd fd fd fd fd fd fd fa fa  

0x127c01c6f480: f7 fa fd fd fd fd fd fd fd fd fd fd fa fa f7 fa  

0x127c01c6f500: fd fd fd fd fd fd fd fd fd fa fa fa f7 fa fd fd  

0x127c01c6f580: fd fd fd fd fd fd fd fa fa fa f7 fa fd fd fd fd  

=>0x127c01c6f600: fd fd fd fd fd fa fa fa f7 fa fd[fd]fd fd fd fd  

0x127c01c6f680: fd fd fd fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x127c01c6f700: fd fa fa fa f7 fa 00 00 00 00 00 00 00 00 00 fa  

0x127c01c6f780: fa fa f7 fa fd fd fd fd fd fd fd fd fd fa fa fa  

0x127c01c6f800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x127c01c6f880: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

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

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to the crash.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.  

==22516==ABORTING

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 422 B)
- [background.js](attachments/background.js) (text/plain, 472 B)
- [injection.js](attachments/injection.js) (text/plain, 1.1 KB)

## Timeline

### [Deleted User] (2022-09-22)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-23)

I can't reproduce this, but I'm also not sure I'm holding this correctly.

caseq@, could you take a quick look? if it looks benign/you can't repro easily feel free to close.

[Monorail components: Platform>DevTools>Platform]

### hc...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-24)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2022-09-26)

I also can't reproduce it, moreover I get "V8 error: Must use --expose-gc" unless I run with --js-flags=--expose-gc.

However, the code at https://source.chromium.org/chromium/chromium/src/+/main:content/browser/devtools/devtools_session.cc;l=502;drc=f97e7e130b02a0fee5a06aa9cdf25d3a0a3715d0;bpv=1;bpt=0 looks suspicious. Not sure why it even compiles. Andrey, wdyt, should we do another find to erase from the  pending_messages_?

### ca...@chromium.org (2022-09-27)

I could reproduce this, thanks for the report!

### gi...@appspot.gserviceaccount.com (2022-09-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c6182a217d455825a0fbe4b3e33313f15072c8c6

commit c6182a217d455825a0fbe4b3e33313f15072c8c6
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Thu Sep 29 14:52:32 2022

DevTools: maintain consistency between pending messages and calls waiting for response

Bug: 1366812
Change-Id: Ib06698b37f51e5edb8d628cbf0944a9e59dfc2fd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3926360
Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1052982}

[modify] https://crrev.com/c6182a217d455825a0fbe4b3e33313f15072c8c6/content/browser/devtools/devtools_session.cc
[modify] https://crrev.com/c6182a217d455825a0fbe4b3e33313f15072c8c6/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/c6182a217d455825a0fbe4b3e33313f15072c8c6/content/public/test/test_devtools_protocol_client.h


### ca...@chromium.org (2022-09-29)

This is fixed by the commit above, thanks a lot for an elaborate repro! That said, I don't think this is exploitable to escalate privileges in normal configuration (i.e. without --remote-debugging-port): this relies on the client being able to control CDP command ids, which is not the case with chrome.debugger extension API (the id is allocated by the API implementation) and can only be achieved by other protocol clients, which we generally consider trusted.

Also note that the attached exploit utilizes `Memory.prepareForLeakDetection` to crash the renderer. I filed this separately as https://crbug.com/chromium/1369663, though this is not really required to trigger the UaF (see the test in the CL above for another option).

### [Deleted User] (2022-09-29)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-30)

Requesting merge to beta M107 because latest trunk commit (1052982) appears to be after beta branch point (1047731).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-30)

Merge review required: M107 is already shipping to beta.

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ca...@chromium.org (2022-09-30)

I'm not sure if the severity of the bug warrants a merge to beta -- it's been around for a while, and it's not practically exploitable (more on that in the https://crbug.com/chromium/1366812#c9). Adrian, do you have an opinion on this?



### ca...@chromium.org (2022-09-30)

+Michael and Yang for the context on https://crbug.com/chromium/1369663,

### am...@chromium.org (2022-10-03)

A security bug being around for awhile does not discount backmerge; however, if lack of exploitability would. Despite the practicality of real world exploitation of this issue being limited and this issue being quite mitigated, the POC and extension provided do allow it to reproduce and result in a UAF in the browser process. 
Medium severity seems to be fairly accurate severity rating and feel like it would be prudent to go ahead and backmerge to stable (unless there are stability or complexity concerns). 
Tentatively approving merge to 107 unless there are stability or other concerns in backmerging;  please merge to branch 5304 at your earliest convenience. 

### pb...@google.com (2022-10-05)

[Bulk Edit] Merge approved for M107 Branch:Refer to go/chrome-branches for branch info, Please goahead and get the changes cherrypick asap.

Note : We are cutting M107 Beta RC today i.e., Oct-05th, Please cherry pick the changes  before 1PM PST or earlier.


### [Deleted User] (2022-10-07)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-10)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-10-10)

[Bulk Edit] Your change has been approved for M107 Branch, please help complete your merges asap (before 3pm PST) today, so the change can be included in this week's RC build for beta releases.

We would like to get the changes as much beta time as possible, so please complete your merges asap to M107 branch(go/chrome-branches).


### gi...@appspot.gserviceaccount.com (2022-10-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8e944de7c0627a76202fc39d15d3ab4de304d20d

commit 8e944de7c0627a76202fc39d15d3ab4de304d20d
Author: Andrey Kosyakov <caseq@chromium.org>
Date: Tue Oct 11 01:21:23 2022

[m107] DevTools: maintain consistency between pending messages and calls waiting for response

(cherry picked from commit c6182a217d455825a0fbe4b3e33313f15072c8c6)

Bug: 1366812
Change-Id: Ib06698b37f51e5edb8d628cbf0944a9e59dfc2fd
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3926360
Reviewed-by: Peter Kvitek <kvitekp@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Andrey Kosyakov <caseq@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1052982}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3943839
Auto-Submit: Andrey Kosyakov <caseq@chromium.org>
Commit-Queue: Peter Kvitek <kvitekp@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#619}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/8e944de7c0627a76202fc39d15d3ab4de304d20d/content/browser/devtools/devtools_session.cc
[modify] https://crrev.com/8e944de7c0627a76202fc39d15d3ab4de304d20d/content/browser/devtools/protocol/devtools_protocol_browsertest.cc
[modify] https://crrev.com/8e944de7c0627a76202fc39d15d3ab4de304d20d/content/public/test/test_devtools_protocol_client.h


### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations on another one, asnine! The VRP Panel has decided to award you $1,000 for this report of a heavily mitigated security bug. Thank you for your efforts finding and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1366812?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061096)*
