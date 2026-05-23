# Security: UaF in TabStripModel::MoveWebContentsAtImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40056857](https://issues.chromium.org/issues/40056857) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip, UI>Browser>TopChrome>TabStrip>TabGroups |
| **Platforms** | Linux, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dp...@chromium.org |
| **Created** | 2021-08-12 |
| **Bounty** | $10,000.00 |

## Description

Chrome Version: 94.0.4603.0 Canary  

Operating System: Windows 7 and 10

**REPRODUCTION CASE**

1. Run chrome.exe --no-first-run --disable-popup-blocking <http://localhost/tabsff.html>
2. Add <http://localhost/tabsff.html> tab to a new group
3. Once all tabs are opened started dragging the group to the right

rax=6e696d6f636e6935 rbx=000002a4022b9a48 rcx=0000000000000000  

rdx=000002a4022b9a58 rsi=000002a4022b9a58 rdi=0000000000000010  

rip=000007feddadb86f rsp=00000000009fdc00 rbp=fffffffffffee5b0  

r8=000002a4022b9a60 r9=00000000009fdd18 r10=000002a402f4c860  

r11=000002a409bf1ba0 r12=000002a4022b9a60 r13=000002a401856408  

r14=0000000000000002 r15=00000000009fdd18  

iopl=0 nv up ei pl nz na po cy  

cs=0033 ss=0000 ds=0000 es=0000 fs=0053 gs=002b efl=00010207  

chrome!std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >::release [inlined in chrome!std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert+0x18f]:  

000007fe`ddadb86f 488b042b mov rax,qword ptr [rbx+rbp] ds:000002a4`022a7ff8=????????????????  

0:000> k  

\*\*\* Stack trace for last set context - .thread/.cxr resets it

# Child-SP RetAddr Call Site

00 (Inline Function) --------`-------- chrome!std::__1::unique_ptr<TabStripModel::WebContentsData,std::__1::default_delete<TabStripModel::WebContentsData> >::release [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\__memory\unique_ptr.h @ 305] 01 (Inline Function) --------`-------- chrome!std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >::operator= [C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_memory\unique\_ptr.h @ 234]  

02 (Inline Function) --------`-------- chrome!std::__1::__move_backward_constexpr+0x21 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\algorithm @ 1927] 03 (Inline Function) --------`-------- chrome!std::\_\_1::\_\_move\_backward+0x21 [C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\algorithm @ 1936]  

04 (Inline Function) --------`-------- chrome!std::__1::move_backward+0x21 [C:\b\s\w\ir\cache\builder\src\buildtools\third_party\libc++\trunk\include\algorithm @ 1967] 05 (Inline Function) --------`-------- chrome!std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::\_\_move\_range+0x59 [C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector @ 1763]  

06 00000000`009fdc00 000007fe`ddad9d9b chrome!std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert+0x18f [C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector @ 1815]  

07 00000000`009fdc80 000007fe`e20d1bde chrome!TabStripModel::MoveWebContentsAtImpl+0x22b [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc @ 2037]  

08 00000000`009fddf0 000007fe`e3074c21 chrome!TabStripModel::MoveGroupTo+0x7e [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc @ 701]  

09 00000000`009fde50 000007fe`e0f7f6c4 chrome!TabStripUIHandler::HandleMoveGroup+0x441 [C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\tab\_strip\tab\_strip\_ui\_handler.cc @ 775]  

0a (Inline Function) --------`-------- chrome!base::RepeatingCallback<void (const base::ListValue \*)>::Run+0xa [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 166] 0b (Inline Function) --------`-------- chrome!content::WebUIImpl::ProcessWebUIMessage+0x2a [C:\b\s\w\ir\cache\builder\src\content\browser\webui\web\_ui\_impl.cc @ 274]  

0c 00000000`009fe010 000007fe`e0b3cf71 chrome!content::WebUIImpl::Send+0x1d4 [C:\b\s\w\ir\cache\builder\src\content\browser\webui\web\_ui\_impl.cc @ 112]  

0d 00000000`009fe1c0 000007fe`df9a4e8b chrome!content::mojom::WebUIHostStubDispatch::Accept+0x111 [C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\content\common\web\_ui.mojom.cc @ 152]  

0e (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleValidatedMessage+0x462 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 898] 0f 00000000`009fe2d0 000007fe`df8ce399 chrome!mojo::InterfaceEndpointClient::HandleIncomingMessageThunk::Accept+0x48b [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc @ 329] 10 00000000`009fe3c0 000007fe`e00bfec3 chrome!mojo::MessageDispatcher::Accept+0x69 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc @ 43] 11 (Inline Function) --------`-------- chrome!mojo::InterfaceEndpointClient::HandleIncomingMessage+0x23 [C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface\_endpoint\_client.cc @ 655]  

12 (Inline Function) --------`-------- chrome!IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread+0xec [C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc @ 981]  

13 (Inline Function) --------`-------- chrome!base::internal::FunctorTraits<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),void>::Invoke+0x1a2 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 509] 14 (Inline Function) --------`-------- chrome!base::internal::InvokeHelper<0,void>::MakeItSo+0x1aa [C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h @ 648]  

15 (Inline Function) --------`-------- chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunImpl+0x1ae [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 721] 16 00000000`009fe440 000007fe`dbd308a4 chrome!base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce+0x1d3 [C:\b\s\w\ir\cache\builder\src\base\bind_internal.h @ 690] 17 (Inline Function) --------`-------- chrome!base::OnceCallback<void ()>::Run+0x16 [C:\b\s\w\ir\cache\builder\src\base\callback.h @ 98]  

18 00000000`009fe6c0 000007fe`df7ef5c7 chrome!base::TaskAnnotator::RunTask+0x1a4 [C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc @ 178]  

19 (Inline Function) --------`-------- chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl+0xf6 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 360] 1a 00000000`009fe810 000007fe`df9a9f90 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork+0x187 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 260] 1b 00000000`009feba0 000007fe`dbe2f3e4 chrome!base::MessagePumpForUI::DoRunLoop+0x180 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 221] 1c 00000000`009fed10 000007fe`dc5ff383 chrome!base::MessagePumpWin::Run+0x44 [C:\b\s\w\ir\cache\builder\src\base\message_loop\message_pump_win.cc @ 79] 1d 00000000`009fed60 000007fe`dc7e2c86 chrome!base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run+0x83 [C:\b\s\w\ir\cache\builder\src\base\task\sequence_manager\thread_controller_with_message_pump_impl.cc @ 470] 1e 00000000`009fedd0 000007fe`dcce767b chrome!base::RunLoop::Run+0x1a6 [C:\b\s\w\ir\cache\builder\src\base\run_loop.cc @ 136] 1f 00000000`009feee0 000007fe`de8ca914 chrome!content::BrowserMainLoop::RunMainMessageLoop+0xcb [C:\b\s\w\ir\cache\builder\src\content\browser\browser_main_loop.cc @ 998] 20 (Inline Function) --------`-------- chrome!content::BrowserMainRunnerImpl::Run+0x9 [C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc @ 152]  

21 00000000`009fef50 000007fe`dec4dc74 chrome!content::BrowserMain+0xf4 [C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc @ 47]  

22 (Inline Function) --------`-------- chrome!content::RunBrowserProcessMain+0x61 [C:\b\s\w\ir\cache\builder\src\content\app\content_main_runner_impl.cc @ 595] 23 (Inline Function) --------`-------- chrome!content::ContentMainRunnerImpl::RunBrowser+0x43e [C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc @ 1084]  

24 00000000`009feff0 000007fe`dc727db7 chrome!content::ContentMainRunnerImpl::Run+0x784 [C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc @ 953]  

25 (Inline Function) --------`-------- chrome!content::RunContentProcess+0x330 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 386] 26 00000000`009ff140 000007fe`dc7264ef chrome!content::ContentMain+0x377 [C:\b\s\w\ir\cache\builder\src\content\app\content_main.cc @ 412] 27 00000000`009ff350 00000001`3f24f7b0 chrome!ChromeMain+0x18f [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_main.cc @ 154] 28 00000000`009ff460 00000001`3f24f34f chrome_exe!MainDllLoader::Launch+0x300 [C:\b\s\w\ir\cache\builder\src\chrome\app\main_dll_loader_win.cc @ 169] 29 00000000`009ff6e0 00000001`3f2b2972 chrome_exe!wWinMain+0xcaf [C:\b\s\w\ir\cache\builder\src\chrome\app\chrome_exe_main_win.cc @ 382] 2a (Inline Function) --------`-------- chrome\_exe!invoke\_main+0x21 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 118]  

2b 00000000`009ffb10 00000000`7700652d chrome\_exe!\_\_scrt\_common\_main\_seh+0x106 [d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl @ 288]  

2c 00000000`009ffb50 00000000`7713c521 kernel32!BaseThreadInitThunk+0xd  

2d 00000000`009ffb80 00000000`00000000 ntdll!RtlUserThreadStart+0x1d

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 1.7 MB)
- [tabsff.html](attachments/tabsff.html) (text/plain, 406 B)

## Timeline

### ch...@gmail.com (2021-08-12)

- Enable #top-chrome-touch-ui flag as in https://crbug.com/chromium/1228557. 



### [Deleted User] (2021-08-12)

[Empty comment from Monorail migration]

### wf...@chromium.org (2021-08-12)

Thanks for your report. TabStripModel is having a fun time these days. connily@chromium.org I wonder if you could take a look at this bug? Since this is direct from web to browser memory corruption, this would be a Critical, but the gesture/user-interaction lowers it to High.

[Monorail components: UI>Browser>TopChrome>TabStrip UI>Browser>TopChrome>TabStrip>TabGroups]

### [Deleted User] (2021-08-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-08-13)

Stack trace:

Received signal 11 SEGV_ACCERR 08e4016dfff8
#0 0x560daad8ac69 base::debug::CollectStackTrace()
#1 0x560daacf5673 base::debug::StackTrace::StackTrace()
#2 0x560daad8a741 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f2ed14ba890 (/lib/x86_64-linux-gnu/libpthread-2.27.so+0x1288f)
#4 0x560dad8b4129 std::__1::vector<>::insert()
#5 0x560dad8acc48 TabStripModel::MoveWebContentsAtImpl()
#6 0x560dad8ad7d0 TabStripModel::MoveGroupTo()
#7 0x560dadd69dca TabStripPageHandler::MoveGroup()
#8 0x560da95d9ce6 tab_strip::mojom::PageHandlerStubDispatch::Accept()
#9 0x560dab0d04d0 mojo::InterfaceEndpointClient::HandleValidatedMessage()
#10 0x560dab0d4a39 mojo::MessageDispatcher::Accept()
#11 0x560dab0d180a mojo::InterfaceEndpointClient::HandleIncomingMessage()
#12 0x560dab0d85f2 mojo::internal::MultiplexRouter::ProcessIncomingMessage()
#13 0x560dab0d7deb mojo::internal::MultiplexRouter::Accept()
#14 0x560dab0d4a39 mojo::MessageDispatcher::Accept()
#15 0x560dab0ce998 mojo::Connector::DispatchMessage()
#16 0x560dab0cf167 mojo::Connector::ReadAllAvailableMessages()
#17 0x560dab0e77be mojo::SimpleWatcher::OnHandleReady()
#18 0x560daa176a90 base::internal::Invoker<>::RunOnce()
#19 0x560daad4e793 base::TaskAnnotator::RunTask()
#20 0x560daad5f69e base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#21 0x560daad5f3ab base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#22 0x560daad5fa62 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#23 0x560daad11d2f base::MessagePumpGlib::Run()
#24 0x560daad5fcd5 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#25 0x560daad30f8b base::RunLoop::Run()
#26 0x560da89c1a73 content::BrowserMainLoop::RunMainMessageLoop()
#27 0x560da89c3352 content::BrowserMainRunnerImpl::Run()
#28 0x560da89bf44b content::BrowserMain()
#29 0x560daa8a2422 content::ContentMainRunnerImpl::RunBrowser()
#30 0x560daa8a1eeb content::ContentMainRunnerImpl::Run()
#31 0x560daa89f795 content::RunContentProcess()
#32 0x560daa8a02ae content::ContentMain()
#33 0x560da776d666 ChromeMain
#34 0x7f2ecca51b97 __libc_start_main
#35 0x560da776d46a _start

### [Deleted User] (2021-08-13)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-13)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### co...@chromium.org (2021-08-13)

Assigning to David but marking Untriaged. David could you take a look at this in the context of work you've done recently and see if it's addressed or fixable?

### [Deleted User] (2021-08-13)

[Empty comment from Monorail migration]

### co...@chromium.org (2021-08-13)

[Empty comment from Monorail migration]

### dp...@chromium.org (2021-08-16)

Taking a look at this now.

### dp...@chromium.org (2021-08-16)

This doesn't repro on mac. I'll be removing mac from the OS list.

### dp...@chromium.org (2021-08-19)

This issue is due to differences in the contents_data_ size and the visual representation of the size in the tab strip. I am going to add a CHECK before the move to verify that the index is contained in the contents data to prevent the OOB since we need to unblock release.

### gi...@appspot.gserviceaccount.com (2021-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9e6fa01067b1b0f07cf53e0e942a373cf0135d04

commit 9e6fa01067b1b0f07cf53e0e942a373cf0135d04
Author: David Pennington <dpenning@chromium.org>
Date: Fri Aug 20 03:35:03 2021

Prevent OOB on dragging tab group by checking Contents Data size

On windows in touch mode, when dragging a tab group header, it is
possible for a web page to close itself. If that happens, the contents
data size will change and the tab strip will start animating out its
tab, however in the case of TabGroups when dragging the group header,
first it kicks the tab out of the group, changing the index, then it
closes the tab. If the header is dragged past that closing group and
the user ends the drag session, then index of the tab group header may
be incorrect, causing a UaF. To prevent the security issue, a check
is added before accessing contents data that blocks invalid index
access.

Bug: 1239057
Change-Id: I026c11ba4b67219d6c823ed286a09ee6bf564f5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3108409
Commit-Queue: David Pennington <dpenning@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Commit-Position: refs/heads/main@{#913631}

[modify] https://crrev.com/9e6fa01067b1b0f07cf53e0e942a373cf0135d04/chrome/browser/ui/tabs/tab_strip_model.cc


### dp...@chromium.org (2021-08-20)

[Empty comment from Monorail migration]

### dp...@chromium.org (2021-08-20)

[Empty comment from Monorail migration]

### dp...@chromium.org (2021-08-20)

[Comment Deleted]

### dp...@chromium.org (2021-08-20)

CC m93 Desktop Release owner @pbommana Lets merge this into M93 as well. this is a low risk CL that moves a Security bug to be a Safe Crash with a CHECK.

### [Deleted User] (2021-08-20)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), govind@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-21)

Your change meets the bar and is auto-approved for M94. Please go ahead and merge the CL to branch 4606 (refs/branch-heads/4606) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2021-08-23)

hi depenning@, this appears to be a safe and trivial fix for this high severity issue, merge approved to M93. Please go ahead and merge to branch 4577 asap (before 1pm PDT today) so it can be included in today's cut of M93. Thank you!

Also, you can also go ahead and merge to branch 4606, for M94 merge. Thanks!

### dp...@chromium.org (2021-08-23)

Merging changes to M93/M94

### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f39e2b6fc93a6e1043978db0932f6e452e19808

commit 6f39e2b6fc93a6e1043978db0932f6e452e19808
Author: David Pennington <dpenning@chromium.org>
Date: Mon Aug 23 19:01:39 2021

Prevent OOB on dragging tab group by checking Contents Data size

On windows in touch mode, when dragging a tab group header, it is
possible for a web page to close itself. If that happens, the contents
data size will change and the tab strip will start animating out its
tab, however in the case of TabGroups when dragging the group header,
first it kicks the tab out of the group, changing the index, then it
closes the tab. If the header is dragged past that closing group and
the user ends the drag session, then index of the tab group header may
be incorrect, causing a UaF. To prevent the security issue, a check
is added before accessing contents data that blocks invalid index
access.

(cherry picked from commit 9e6fa01067b1b0f07cf53e0e942a373cf0135d04)

Bug: 1239057
Change-Id: I026c11ba4b67219d6c823ed286a09ee6bf564f5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3108409
Commit-Queue: David Pennington <dpenning@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114685
Reviewed-by: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#1070}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/6f39e2b6fc93a6e1043978db0932f6e452e19808/chrome/browser/ui/tabs/tab_strip_model.cc


### gi...@appspot.gserviceaccount.com (2021-08-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c84f372692a3b17911ccfa53fd8721586793a448

commit c84f372692a3b17911ccfa53fd8721586793a448
Author: David Pennington <dpenning@chromium.org>
Date: Mon Aug 23 19:35:14 2021

Prevent OOB on dragging tab group by checking Contents Data size

On windows in touch mode, when dragging a tab group header, it is
possible for a web page to close itself. If that happens, the contents
data size will change and the tab strip will start animating out its
tab, however in the case of TabGroups when dragging the group header,
first it kicks the tab out of the group, changing the index, then it
closes the tab. If the header is dragged past that closing group and
the user ends the drag session, then index of the tab group header may
be incorrect, causing a UaF. To prevent the security issue, a check
is added before accessing contents data that blocks invalid index
access.

(cherry picked from commit 9e6fa01067b1b0f07cf53e0e942a373cf0135d04)

Bug: 1239057
Change-Id: I026c11ba4b67219d6c823ed286a09ee6bf564f5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3108409
Commit-Queue: David Pennington <dpenning@chromium.org>
Reviewed-by: Peter Boström <pbos@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3114471
Reviewed-by: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#232}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/c84f372692a3b17911ccfa53fd8721586793a448/chrome/browser/ui/tabs/tab_strip_model.cc


### am...@google.com (2021-08-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-08-25)

Congratulations, Khalil! The VRP Panel has decided to award you $10,000 for this report. Nice finding and we appreciate your efforts in reporting this issue to us! 

### am...@google.com (2021-08-27)

[Empty comment from Monorail migration]

### rz...@google.com (2021-11-01)

[Empty comment from Monorail migration]

### gi...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-11-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6af6c77b17d4f84f9f4dff6c38add3bc371e2940

commit 6af6c77b17d4f84f9f4dff6c38add3bc371e2940
Author: David Pennington <dpenning@chromium.org>
Date: Thu Nov 04 15:09:56 2021

[M90-LTS] Prevent OOB on dragging tab group by checking Contents Data size

On windows in touch mode, when dragging a tab group header, it is
possible for a web page to close itself. If that happens, the contents
data size will change and the tab strip will start animating out its
tab, however in the case of TabGroups when dragging the group header,
first it kicks the tab out of the group, changing the index, then it
closes the tab. If the header is dragged past that closing group and
the user ends the drag session, then index of the tab group header may
be incorrect, causing a UaF. To prevent the security issue, a check
is added before accessing contents data that blocks invalid index
access.

(cherry picked from commit 9e6fa01067b1b0f07cf53e0e942a373cf0135d04)

Bug: 1239057
Change-Id: I026c11ba4b67219d6c823ed286a09ee6bf564f5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3108409
Commit-Queue: David Pennington <dpenning@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#913631}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3250739
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1656}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/6af6c77b17d4f84f9f4dff6c38add3bc371e2940/chrome/browser/ui/tabs/tab_strip_model.cc


### rz...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2021-11-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1239057?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: UI>Browser>TopChrome>TabStrip, UI>Browser>TopChrome>TabStrip>TabGroups]
[Monorail mergedwith: crbug.com/chromium/1228478]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056857)*
