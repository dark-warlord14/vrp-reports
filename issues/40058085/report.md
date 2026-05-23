# Security: heap-use-after-free in network::server::HttpServer::FindConnection

| Field | Value |
|-------|-------|
| **Issue ID** | [40058085](https://issues.chromium.org/issues/40058085) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2021-12-01 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

[0] UiDevToolsServer class owns network::server::HttpServer,when UiDevToolsServer destroy,the server\_ ptr will delete  

<https://source.chromium.org/chromium/chromium/src/+/main:components/ui_devtools/devtools_server.h;l=111>

[1] And then UAF in HttpServer::FindConnection  

<https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/server/http_server.cc;l=525>

reproduce step

1. open chrome://inspect
2. click Inspect Native UI and then close this page
3. UAF occurs

=================================================================  

==11772==ERROR: AddressSanitizer: heap-use-after-free on address 0x1200fb18cf78 at pc 0x7fff96c98e21 bp 0x007a1f3fc9a0 sp 0x007a1f3fc9e8  

READ of size 8 at 0x1200fb18cf78 thread T0  

#0 0x7fff96c98e20 in network::server::HttpServer::FindConnection E:\src\chromium\src\services\network\public\cpp\server\http\_server.cc:525  

#1 0x7fff96c995a4 in network::server::HttpServer::OnWritable E:\src\chromium\src\services\network\public\cpp\server\http\_server.cc:350  

#2 0x7fffbb2045bb in mojo::SimpleWatcher::OnHandleReady E:\src\chromium\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#3 0x7fff98966b04 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#4 0x7fff989b19b9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#5 0x7fff989b1088 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#6 0x7fff98aabac6 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#7 0x7fff98aa957f in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#8 0x7fff989b3137 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#9 0x7fff988b1f43 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#10 0x7fff6b6b1aeb in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1001  

#11 0x7fff6b6b7923 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#12 0x7fff6b6ab43f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#13 0x7fff6d7f020e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#14 0x7fff6d7f33c1 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1159  

#15 0x7fff6d7f24f1 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#16 0x7fff6d7ee29f in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#17 0x7fff6d7ef307 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426  

#18 0x7fff703714a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome\_main.cc:172  

#19 0x7ff66c6b5544 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main\_dll\_loader\_win.cc:169  

#20 0x7ff66c6b2a02 in main E:\src\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#21 0x7ff66c8864ab in \_\_scrt\_common\_main\_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#22 0x7fffe5be7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)  

#23 0x7fffe7a22650 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x180052650)

0x1200fb18cf78 is located 72 bytes inside of 104-byte region [0x1200fb18cf30,0x1200fb18cf98)  

freed by thread T0 here:  

#0 0x7fffa934e46b in operator delete+0x8b (E:\src\chromium\src\out\Default\clang\_rt.asan\_dynamic-x86\_64.dll+0x18003e46b)  

#1 0x7fff666becb0 in ui\_devtools::UiDevToolsServer::~UiDevToolsServer E:\src\chromium\src\components\ui\_devtools\devtools\_server.cc:83  

#2 0x7fff666c1deb in ui\_devtools::UiDevToolsServer::~UiDevToolsServer E:\src\chromium\src\components\ui\_devtools\devtools\_server.cc:81  

#3 0x7fff666c1cf4 in ui\_devtools::UiDevToolsServer::OnClose E:\src\chromium\src\components\ui\_devtools\devtools\_server.cc:245  

#4 0x7fff96c9a19b in network::server::HttpServer::Close E:\src\chromium\src\services\network\public\cpp\server\http\_server.cc:160  

#5 0x7fff96c9c00d in network::server::HttpServer::HandleReadResult E:\src\chromium\src\services\network\public\cpp\server\http\_server.cc:277  

#6 0x7fff96c9b088 in network::server::HttpServer::OnReadable E:\src\chromium\src\services\network\public\cpp\server\http\_server.cc:257  

#7 0x7fffbb2045bb in mojo::SimpleWatcher::OnHandleReady E:\src\chromium\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#8 0x7fff98966b04 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#9 0x7fff989b19b9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#10 0x7fff989b1088 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#11 0x7fff98aabac6 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#12 0x7fff98aa957f in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#13 0x7fff989b3137 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#14 0x7fff988b1f43 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#15 0x7fff6b6b1aeb in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1001  

#16 0x7fff6b6b7923 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#17 0x7fff6b6ab43f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#18 0x7fff6d7f020e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#19 0x7fff6d7f33c1 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1159  

#20 0x7fff6d7f24f1 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#21 0x7fff6d7ee29f in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#22 0x7fff6d7ef307 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426  

#23 0x7fff703714a5 in ChromeMain E:\src\chromium\src\chrome\app\chrome\_main.cc:172  

#24 0x7ff66c6b5544 in MainDllLoader::Launch E:\src\chromium\src\chrome\app\main\_dll\_loader\_win.cc:169  

#25 0x7ff66c6b2a02 in main E:\src\chromium\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#26 0x7ff66c8864ab in \_\_scrt\_common\_main\_seh D:\agent\_work\13\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#27 0x7fffe5be7033 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017033)

previously allocated by thread T0 here:  

#0 0x7fffa934e17b in operator new+0x8b (E:\src\chromium\src\out\Default\clang\_rt.asan\_dynamic-x86\_64.dll+0x18003e17b)  

#1 0x7fff666bf8d9 in ui\_devtools::UiDevToolsServer::MakeServer E:\src\chromium\src\components\ui\_devtools\devtools\_server.cc:180  

#2 0x7fff666c2fd5 in base::internal::Invoker<base::internal::BindState<void (ui\_devtools::UiDevToolsServer::\*)(mojo::PendingRemote[network::mojom::TCPServerSocket](javascript:void(0);), int, const absl::optional[net::IPEndPoint](javascript:void(0);) &),base::WeakPtr<ui\_devtools::UiDevToolsServer>,mojo::PendingRemote[network::mojom::TCPServerSocket](javascript:void(0);) >,void (int, const absl::optional[net::IPEndPoint](javascript:void(0);) &)>::RunOnce E:\src\chromium\src\base\bind\_internal.h:741  

#3 0x7fff706b572b in network::mojom::NetworkContext\_CreateTCPServerSocket\_ForwardToCallback::Accept E:\src\chromium\src\out\Default\gen\services\network\public\mojom\network\_context.mojom.cc:11024  

#4 0x7fffb9b59884 in mojo::InterfaceEndpointClient::HandleValidatedMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:895  

#5 0x7fffb9b69a88 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#6 0x7fffb9b5d3c4 in mojo::InterfaceEndpointClient::HandleIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:657  

#7 0x7fffb9b76b4c in mojo::internal::MultiplexRouter::ProcessIncomingMessage E:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:1104  

#8 0x7fffb9b758e5 in mojo::internal::MultiplexRouter::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\multiplex\_router.cc:724  

#9 0x7fffb9b69a88 in mojo::MessageDispatcher::Accept E:\src\chromium\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:43  

#10 0x7fffb9b49a91 in mojo::Connector::DispatchMessageW E:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:556  

#11 0x7fffb9b4b584 in mojo::Connector::ReadAllAvailableMessages E:\src\chromium\src\mojo\public\cpp\bindings\lib\connector.cc:614  

#12 0x7fffbb2045bb in mojo::SimpleWatcher::OnHandleReady E:\src\chromium\src\mojo\public\cpp\system\simple\_watcher.cc:278  

#13 0x7fff98966b04 in base::TaskAnnotator::RunTaskImpl E:\src\chromium\src\base\task\common\task\_annotator.cc:135  

#14 0x7fff989b19b9 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:356  

#15 0x7fff989b1088 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:261  

#16 0x7fff98aabac6 in base::MessagePumpForUI::DoRunLoop E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:220  

#17 0x7fff98aa957f in base::MessagePumpWin::Run E:\src\chromium\src\base\message\_loop\message\_pump\_win.cc:78  

#18 0x7fff989b3137 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run E:\src\chromium\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#19 0x7fff988b1f43 in base::RunLoop::Run E:\src\chromium\src\base\run\_loop.cc:140  

#20 0x7fff6b6b1aeb in content::BrowserMainLoop::RunMainMessageLoop E:\src\chromium\src\content\browser\browser\_main\_loop.cc:1001  

#21 0x7fff6b6b7923 in content::BrowserMainRunnerImpl::Run E:\src\chromium\src\content\browser\browser\_main\_runner\_impl.cc:153  

#22 0x7fff6b6ab43f in content::BrowserMain E:\src\chromium\src\content\browser\browser\_main.cc:30  

#23 0x7fff6d7f020e in content::RunBrowserProcessMain E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:646  

#24 0x7fff6d7f33c1 in content::ContentMainRunnerImpl::RunBrowser E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1159  

#25 0x7fff6d7f24f1 in content::ContentMainRunnerImpl::Run E:\src\chromium\src\content\app\content\_main\_runner\_impl.cc:1026  

#26 0x7fff6d7ee29f in content::RunContentProcess E:\src\chromium\src\content\app\content\_main.cc:398  

#27 0x7fff6d7ef307 in content::ContentMain E:\src\chromium\src\content\app\content\_main.cc:426

SUMMARY: AddressSanitizer: heap-use-after-free E:\src\chromium\src\services\network\public\cpp\server\http\_server.cc:525 in network::server::HttpServer::FindConnection  

Shadow bytes around the buggy address:  

0x042b1a631990: fd fd fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

0x042b1a6319a0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x042b1a6319b0: fd fd fa fa fa fa fa fa fa fa fd fd fd fd fd fd  

0x042b1a6319c0: fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa fa  

0x042b1a6319d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa fa  

=>0x042b1a6319e0: fa fa fa fa fa fa fd fd fd fd fd fd fd fd fd[fd]  

0x042b1a6319f0: fd fd fd fa fa fa fa fa fa fa fa fa fd fd fd fd  

0x042b1a631a00: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x042b1a631a10: fa fa fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x042b1a631a20: fa fa fa fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x042b1a631a30: fd fd fd fd fd fd fa fa fa fa fa fa fa fa 00 00  

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

==11772==ABORTING

**VERSION**  

Chrome Version: 98.0.4738.0 dev x64  

Operating System: 21h1

Reporter credit: Zhihua Yao of Kunlun Lab

## Attachments

- [2021-12-01 13-18-40.mp4](attachments/2021-12-01 13-18-40.mp4) (video/mp4, 8.0 MB)

## Timeline

### [Deleted User] (2021-12-01)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-12-01)

It’s really weird, I can’t reproduce it now, but I’m analyzing it in detail now 

InspectMessageHandler::HandleLaunchUIDevToolsCommand [0] will set on_session_ended_  callback function to DestroyUiDevTools,when close [2],call the callback function [1] will reset devtools_server_,then
UiDevToolsServer class owns network::server::HttpServer,when UiDevToolsServer destroy,the server_[3] ptr will be deleted,Eventually UAF happens [4]

void InspectMessageHandler::HandleLaunchUIDevToolsCommand(
    const base::ListValue* args) {
  // Start the UI DevTools server if needed and launch the front-end.
  if (!ChromeBrowserMainExtraPartsViews::Get()->GetUiDevToolsServerInstance()) {
    ChromeBrowserMainExtraPartsViews::Get()->CreateUiDevTools();

    // Make the server only lasts for a session.
    const ui_devtools::UiDevToolsServer* server =
        ChromeBrowserMainExtraPartsViews::Get()->GetUiDevToolsServerInstance();
    server->SetOnSessionEnded(base::BindOnce([]() {
      if (ChromeBrowserMainExtraPartsViews::Get()
              ->GetUiDevToolsServerInstance())
        ChromeBrowserMainExtraPartsViews::Get()->DestroyUiDevTools();  [0] //
    }));
  }
......

void UiDevToolsServer::SetOnSessionEnded(base::OnceClosure callback) const {
  on_session_ended_ = std::move(callback);
}

---------------------------------

void ChromeBrowserMainExtraPartsViews::DestroyUiDevTools() {
  devtools_process_observer_.reset();
  devtools_server_.reset();  [1] // std::unique_ptr<ui_devtools::UiDevToolsServer> devtools_server_;
}
---------------------------------

void UiDevToolsServer::OnClose(int connection_id) {
  DCHECK_CALLED_ON_VALID_SEQUENCE(devtools_server_sequence_);
  auto it = connections_.find(connection_id);
  if (it == connections_.end())
    return;
  UiDevToolsClient* client = it->second;
  client->Disconnect();
  connections_.erase(it);

  if (connections_.empty() && on_session_ended_)
    std::move(on_session_ended_).Run();  [2]
}
---------------------------------

[2] https://source.chromium.org/chromium/chromium/src/+/main:components/ui_devtools/devtools_server.h;l=111

---------------------------------
HttpConnection* HttpServer::FindConnection(int connection_id) {
  auto it = id_to_connection_.find(connection_id);
  if (it == id_to_connection_.end())
    return nullptr;
  return it->second.get();
} [4] //UAF


### jd...@chromium.org (2021-12-02)

This seems like a UAF, but I'm not sure how one could exploit this practically speaking. hackyzh002@: can you propose a plausible scenario on how an attacker could use this?

yangguo@: can you take a look at this, feeling free to re-assign as needed?

[Monorail components: Platform>DevTools]

### [Deleted User] (2021-12-02)

[Empty comment from Monorail migration]

### ha...@gmail.com (2021-12-02)

Sorry jdeblasio@, at present, I don’t know how to exploit this kind of interaction, because I don’t know whether it can be triggered by other methods, such as javascript API, because I am not very familiar with this. You can refer to https://crbug.com/chromium/1232628 and https://crbug.com/chromium/1232617. At present, there are more UAFs of this kind. 

### ha...@gmail.com (2021-12-02)

If you want to reproduce this bug, you need to enable the Debugging tools for UI in chrome://flags/ 

### ya...@google.com (2021-12-02)

The DevTools team does not actually maintain UI DevTools, which is an alternate implementation of the backend, for Chrome UI.

Oshima, could you find an owner for this?

### jd...@chromium.org (2021-12-03)

I'm tentatively assigning security labels as a very heavily mitigated UAF in the browser process out of an abundance of caution, but it might not be a security bug at all. It should hopefully be a pretty straightforward fix once we find the correct owners, however, so oshima@, your help would be very appreciated. Thanks!

### [Deleted User] (2021-12-03)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-03)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### os...@chromium.org (2021-12-06)

UI Devtools is available for aura/views platform, not just for chromeos. (and this is reported on Windows) Assigning weili@ who is one of owners of ui devtools in chrome team.

### [Deleted User] (2021-12-16)

weili: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2021-12-27)

[Comment Deleted]

### [Deleted User] (2021-12-31)

weili: Uh oh! This issue still open and hasn't been updated in the last 30 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2022-01-07)

So is this owner still on holiday? 

### ct...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-01-12)

yuhengh@ could you take this bug following your investigation on https://crbug.com/chromium/1282735?

+ricea@ who is owner for net/server/ code -- could you advise how DevTools code should destroy an HttpServer instance? Thanks!

### ri...@chromium.org (2022-01-13)

This seems to be the //services/network/public/cpp/server version of HttpServer, not the //net/server version, although they're almost identical. The way it's currently implemented makes it difficult to tear down safely. Possibly we could modify it to track connections that are currently pending deletion and have a method that deletes the server after all active connections are gone.

### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### yu...@chromium.org (2022-02-07)

Not sure what's the best way to fix this, reassigning to code owner

### ha...@gmail.com (2022-02-14)

hello,the code owner looks like no longer on chrome

### ri...@chromium.org (2022-02-14)

Sending for re-triage.

### ha...@gmail.com (2022-02-23)

So someone reassign the owner? 

### ya...@google.com (2022-02-23)

[Empty comment from Monorail migration]

### ha...@gmail.com (2022-03-07)

--- chrome_browser_main_extra_parts_views.cc	2022-03-07 16:39:43.395067000 +0800
+++ chrome_browser_main_extra_parts_views_bak.cc	2022-03-07 16:39:43.395067000 +0800
@@ -208,5 +208,5 @@ ChromeBrowserMainExtraPartsViews::GetUiD
 
 void ChromeBrowserMainExtraPartsViews::DestroyUiDevTools() {
   devtools_process_observer_.reset();
-  devtools_server_.reset();
+  //devtools_server_.reset();
 }

With this patch, UAF will not happen 


### ri...@chromium.org (2022-03-07)

#25 Doesn't this just create a memory leak? It's not clear to me that it won't just move the UAF somewhere else, either.

### ha...@gmail.com (2022-03-07)

Maybe there will be a memory leak, the best way is to use weakptr 

### ja...@chromium.org (2022-03-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

[Empty comment from Monorail migration]

### ja...@chromium.org (2022-03-08)

hackyzh002@, do you have some reproduction instructions? I cannot even see the flags in chrome://flags on Linux or Windows (it looks like it might be ChromeOS-only - https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/about_flags.cc;l=4626;drc=97c2dc1068cf2a2f7eb95a128542bf7b064172de).

### ha...@gmail.com (2022-03-08)

[Comment Deleted]

### ha...@gmail.com (2022-03-08)

[Comment Deleted]

### ha...@gmail.com (2022-03-08)

https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/about_flags.cc;l=7426

        "ui-debug-tools"

### ja...@chromium.org (2022-03-08)

Thanks, that worked - I can now inspect. However, still no UAF (I tried both asan release and asan debug).

### yu...@chromium.org (2022-03-08)

FYI, it's easier to reproduce on Mac
https://crbug.com/1282735#c6

### ja...@chromium.org (2022-03-08)

I do not have a Mac, but I do have an idea for a fix. It would be great if someone could try out(?)

Here is the CL: https://chromium-review.googlesource.com/c/chromium/src/+/3510307

### gi...@appspot.gserviceaccount.com (2022-03-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8ef4631cac23a205c0d237c087dba82674f1ce6e

commit 8ef4631cac23a205c0d237c087dba82674f1ce6e
Author: Jaroslav Sevcik <jarin@chromium.org>
Date: Wed Mar 09 09:20:01 2022

Use weak pointers for devtools http server handlers

This makes sure that we do not call HttpServer message handlers
on a deallocated HttpServer instance.

Interestingly, the weak pointer factory was already there, but
it was unused.

Bug: chromium:1275414
Change-Id: Ic0c33319bb3e67e3c15349d07acbaad64a7f62e3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3510307
Reviewed-by: Robbie McElrath <rmcelrath@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Jaroslav Sevcik <jarin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#979140}

[modify] https://crrev.com/8ef4631cac23a205c0d237c087dba82674f1ce6e/services/network/public/cpp/server/http_server.cc


### ha...@gmail.com (2022-03-10)

This is fixed!Please change the status

### ja...@google.com (2022-03-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-17)

Hello, the VRP Panel has decided to award you $1,000 for this report. While we appreciate you efforts, we understand this reward amount may be less than you expected. The reasons for this reward judgement are:
1) there was no demonstrated exploitability or explanation how an attacker would leverage this bug 
2) the direct access and user interaction with dev tools required to trigger this issue 
3) the lack of reliability to reasonably trigger this issue 

### ha...@gmail.com (2022-03-17)



Hello,this vulnerability attack is also relatively simple. The victim directly accesses devtools://devtools/bundled/devtools_app.html?uiDevTools=true&ws=127.0.0.1:9223/0, and then closes the tab page to trigger this vulnerability. I think it is necessary to Raise the bounty for this bug 

### ha...@gmail.com (2022-03-17)

And you can see this microsoft's attack scenarios for devtools. https://microsoftedge.github.io/edgevr/posts/attacking-the-devtools/

### ja...@chromium.org (2022-03-17)

Re #43, additionally, the attacker would need to activate the "ui-debug-tools" experimental flag (which is off by default).

### am...@chromium.org (2022-03-17)

hello, as expressed in https://crbug.com/chromium/1275414#c43- yes, "relatively simple" in terms of steps, however, not as simple in comparison to exploitation via remote content or a single click remote POC, as this requires direct UI access to dev tools and convincing a user to engage in these steps for an attacker to leverage this bug. 

I will still run it back by the panel for reconsideration, however, as conveyed in previous comms and the email to the researcher community about the updates to our rules and policies [1]: 
"There is a recent trend of reports away from issues triggered by remote content to issues that are strongly or solely dependent on user interaction. While we appreciate your efforts to discover and report these bugs, these issues are not as impactful or exploitable as those that demonstrate exploitability through remote content.

The amounts listed are for good quality reports that don't require complex or unlikely user interaction. Reports of issues that rely heavily or solely on user interaction, instead of being triggered by remote content, will generally receive significantly reduced rewards. Less convincing or more constrained bug submissions will likely qualify for reduced reward amounts, as chosen at the discretion of the reward panel.
Reports of issues that involve implausible interaction, interactions a user would not be realistically convinced to perform, may not be rewarded."

[1] https://g.co/chrome/vrp 

### ha...@gmail.com (2022-03-18)

Yes. But the bounty is unreasonable, I think it is very likely to dampen the research enthusiasm of researchers 

### am...@chromium.org (2022-03-23)

Hello, the VRP Panel has decided that the award amount is sufficient for this issue as conveyed by this report. As mentioned in comments #43 and https://crbug.com/chromium/1275414#c47, if you are able to provide a demonstration of exploitability via remote content or and not requiring direct user interaction via dev tools, we are happy to reassess this issue and the reward amount. 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-04-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-04-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-07-29)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1275414?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1282735]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058085)*
