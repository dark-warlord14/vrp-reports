# Security: heap-use-after-free in web_app::ShortcutInfoForExtensionAndProfile 

| Field | Value |
|-------|-------|
| **Issue ID** | [40058418](https://issues.chromium.org/issues/40058418) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | al...@chromium.org |
| **Created** | 2022-01-06 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

Creating an app shortcut after deleting a profile causes a heap UAF.

**VERSION**  

Chrome Version: 99.0.4800.0  

Operating System: Windows 10

**REPRODUCTION CASE**

1. Open chrome://apps
2. Right-click on the preinstalled Web Store app and select Create shortcuts
3. Open profile manager, click Delete on the profile but don't confirm yet
4. Click Delete to confirm profile deletion, then quickly click the "Create" button to create application shortcuts

Clicking the Create button before it's destroyed is tricky, but I've managed to reproduce this a few times.

# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION** Type of crash: browser

==40972==ERROR: AddressSanitizer: heap-use-after-free on address 0x13005d16e868 at pc 0x7ff828b8adfa bp 0x00d9ad5fd1f0 sp 0x00d9ad5fd238  

READ of size 8 at 0x13005d16e868 thread T0  

==40972==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ff828b8adf9 in http2::PriorityWriteScheduler<unsigned int>::NumRegisteredStreams C:\b\s\w\ir\cache\builder\src\net\third\_party\quiche\src\http2\core\priority\_write\_scheduler.h:267  

#1 0x7ff82e6e3e02 in web\_app::ShortcutInfoForExtensionAndProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\web\_applications\extensions\web\_app\_extension\_shortcut.cc:209  

#2 0x7ff82e6e3320 in web\_app::GetShortcutInfoForApp C:\b\s\w\ir\cache\builder\src\chrome\browser\web\_applications\extensions\web\_app\_extension\_shortcut.cc:160  

#3 0x7ff83fd7c2d0 in CreateChromeApplicationShortcutView::CreateChromeApplicationShortcutView C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\create\_application\_shortcut\_view.cc:67  

#4 0x7ff83fd7c006 in chrome::ShowCreateChromeAppShortcutsDialog C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\create\_application\_shortcut\_view.cc:40  

#5 0x7ff83fd8bdeb in AppInfoFooterPanel::CreateShortcuts C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\apps\app\_info\_dialog\app\_info\_footer\_panel.cc:129  

#6 0x7ff832d23989 in base::internal::Invoker<base::internal::BindState<`lambda at ../../ui/views/controls/button/button.cc:110:31',base::RepeatingCallback<void ()> >,void (const ui::Event &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:754  

#7 0x7ff832d2105b in views::Button::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:647  

#8 0x7ff832d1d379 in views::Button::DefaultButtonControllerDelegate::NotifyClick C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button.cc:66  

#9 0x7ff8356fa666 in views::ButtonController::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc:59  

#10 0x7ff832d5fd4c in views::View::ProcessMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3074  

#11 0x7ff83c545672 in ui::ScopedTargetHandler::OnEvent C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28  

#12 0x7ff833c83e91 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#13 0x7ff833c833b1 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#14 0x7ff833c82c9b in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#15 0x7ff833c828dc in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#16 0x7ff835775791 in views::internal::RootView::OnMouseReleased C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:485  

#17 0x7ff832d877a2 in views::Widget::OnMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1533  

#18 0x7ff833c83e91 in ui::EventDispatcher::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:190  

#19 0x7ff833c833b1 in ui::EventDispatcher::ProcessEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:139  

#20 0x7ff833c82c9b in ui::EventDispatcherDelegate::DispatchEventToTarget C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:83  

#21 0x7ff833c828dc in ui::EventDispatcherDelegate::DispatchEvent C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:55  

#22 0x7ff8386bc7c4 in ui::EventProcessor::OnEventFromSource C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49  

#23 0x7ff8357680d7 in ui::EventSource::DeliverEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:118  

#24 0x7ff835767d31 in ui::EventSource::SendEventToSinkFromRewriter C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:143  

#25 0x7ff835767833 in ui::EventSource::SendEventToSink C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:112  

#26 0x7ff8386ba2f3 in views::DesktopWindowTreeHostWin::HandleMouseEvent C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:1003  

#27 0x7ff83c5b2783 in views::HWNDMessageHandler::HandleMouseEventInternal C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3145  

#28 0x7ff83c5abbe7 in views::HWNDMessageHandler::\_ProcessWindowMessage C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.h:358  

#29 0x7ff83c5ab286 in views::HWNDMessageHandler::OnWndProc C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1019  

#30 0x7ff835ea9306 in gfx::WindowImpl::WndProc C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:306  

#31 0x7ff835ea7c21 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc> C:\b\s\w\ir\cache\builder\src\base\win\wrapped\_window\_proc.h:74  

#32 0x7ff8df85e7e7 in CallWindowProcW+0x3f7 (C:\WINDOWS\System32\user32.dll+0x18000e7e7)  

#33 0x7ff8df85e228 in DispatchMessageW+0x258 (C:\WINDOWS\System32\user32.dll+0x18000e228)  

#34 0x7ff8330c2fba in base::MessagePumpForUI::ProcessMessageHelper C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:542  

#35 0x7ff8330c0fe9 in base::MessagePumpForUI::ProcessNextWindowsMessage C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:504  

#36 0x7ff8330c08e3 in base::MessagePumpForUI::DoRunLoop C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:215  

#37 0x7ff8330bec18 in base::MessagePumpWin::Run C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:78  

#38 0x7ff835b4c331 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with\_message\_pump\_impl.cc:468  

#39 0x7ff832f969a3 in base::RunLoop::Run C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:140  

#40 0x7ff82c1af1b1 in content::BrowserMainLoop::RunMainMessageLoop C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:1048  

#41 0x7ff82c1b45d1 in content::BrowserMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:153  

#42 0x7ff82c1a8839 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:30  

#43 0x7ff82ec3ab73 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#44 0x7ff82ec3dbb3 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#45 0x7ff82ec3cce6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#46 0x7ff82ec38fbd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#47 0x7ff82ec3a048 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#48 0x7ff8284f148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177  

#49 0x7ff6dd605b85 in MainDllLoader::Launch C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169  

#50 0x7ff6dd602b5f in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:382  

#51 0x7ff6dda0753f in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#52 0x7ff8e0047033 in BaseThreadInitThunk+0x13 (C:\WINDOWS\System32\KERNEL32.DLL+0x180017033)  

#53 0x7ff8e06e2650 in RtlUserThreadStart+0x20 (C:\WINDOWS\SYSTEM32\ntdll.dll+0x180052650)

0x13005d16e868 is located 488 bytes inside of 560-byte region [0x13005d16e680,0x13005d16e8b0)  

freed by thread T0 here:  

#0 0x7ff6dd6b23fb in free C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:82  

#1 0x7ff82e074681 in extensions::ExtensionRegistrar::RemoveExtension C:\b\s\w\ir\cache\builder\src\extensions\browser\extension\_registrar.cc:184  

#2 0x7ff8352207f0 in extensions::ExtensionService::OnProfileMarkedForPermanentDeletion C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\extension\_service.cc:2191  

#3 0x7ff832e2d470 in ProfileManager::OnLoadProfileForProfileDeletion C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1991  

#4 0x7ff832e1c0ae in `anonymous namespace'::OnProfileLoaded C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:411 #5 0x7ff832e1ba6b in ProfileManager::CreateProfileAsync C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:815 #6 0x7ff832e1b58a in ProfileManager::LoadProfileByPath C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:768 #7 0x7ff832e21d1f in ProfileManager::FinishDeletingProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:2051 #8 0x7ff832e2d0b9 in ProfileManager::OnNewActiveProfileLoaded C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:2439 #9 0x7ff832e32caf in base::internal::Invoker<base::internal::BindState<void (ProfileManager::\*)(const base::FilePath &, const base::FilePath &, base::OnceCallback<void (Profile \*)> \*, Profile \*, Profile::CreateStatus),base::internal::UnretainedWrapper<ProfileManager>,base::FilePath,base::FilePath,base::internal::OwnedWrapper<base::OnceCallback<void (Profile \*)>,std::__1::default_delete<base::OnceCallback<void (Profile \*)> > > >,void (Profile \*, Profile::CreateStatus)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #10 0x7ff832e1ba6b in ProfileManager::CreateProfileAsync C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:815 #11 0x7ff832e20ca7 in ProfileManager::EnsureActiveProfileExistsBeforeDeletion C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1965 #12 0x7ff832e31ffd in base::internal::Invoker<base::internal::BindState<void (ProfileManager::\*)(base::OnceCallback<void (Profile \*)>, const base::FilePath &),base::internal::UnretainedWrapper<ProfileManager>,base::internal::PassedWrapper<base::OnceCallback<void (Profile \*)> > >,void (const base::FilePath &)>::Run C:\b\s\w\ir\cache\builder\src\base\bind_internal.h:754 #13 0x7ff835310253 in BrowserList::TryToCloseBrowserList C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_list.cc:225 #14 0x7ff83530fdc5 in BrowserList::CloseAllBrowsersWithProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser_list.cc:181 #15 0x7ff832e2019a in ProfileManager::ScheduleProfileForDeletion C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1090 #16 0x7ff832e1fd7e in ProfileManager::MaybeScheduleProfileForDeletion C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile_manager.cc:1068 #17 0x7ff83914fc90 in webui::DeleteProfileAtPath C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\profile_helper.cc:65 #18 0x7ff83cd381b7 in ProfilePickerHandler::HandleRemoveProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\webui\signin\profile_picker_handler.cc:824 #19 0x7ff82d1f9dcd in content::WebUIImpl::ProcessWebUIMessage C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:296 #20 0x7ff82d1f619e in content::WebUIImpl::Send C:\b\s\w\ir\cache\builder\src\content\browser\webui\web_ui_impl.cc:113 #21 0x7ff82b4bce6c in content::mojom::WebUIHostStubDispatch::Accept C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\content\common\web_ui.mojom.cc:159 #22 0x7ff8333658cd in mojo::InterfaceEndpointClient::HandleValidatedMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:900 #23 0x7ff835c91772 in mojo::MessageDispatcher::Accept C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\message_dispatcher.cc:43 #24 0x7ff8333690d8 in mojo::InterfaceEndpointClient::HandleIncomingMessage C:\b\s\w\ir\cache\builder\src\mojo\public\cpp\bindings\lib\interface_endpoint_client.cc:657 #25 0x7ff833be91ab in IPC::`anonymous namespace'::ChannelAssociatedGroupController::AcceptOnEndpointThread C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1008  

#26 0x7ff833be2dc7 in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message),scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>,mojo::Message>,void ()>::RunOnce C:\b\s\w\ir\cache\builder\src\base\bind\_internal.h:741  

#27 0x7ff833017e34 in base::TaskAnnotator::RunTaskImpl C:\b\s\w\ir\cache\builder\src\base\task\common\task\_annotator.cc:135

previously allocated by thread T0 here:  

#0 0x7ff6dd6b24fb in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7ff8457e513e in operator new d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7ff834766ccb in extensions::Extension::Create C:\b\s\w\ir\cache\builder\src\extensions\common\extension.cc:276  

#3 0x7ff83476659b in extensions::Extension::Create C:\b\s\w\ir\cache\builder\src\extensions\common\extension.cc:228  

#4 0x7ff837784481 in extensions::ComponentLoader::Load C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\component\_loader.cc:267  

#5 0x7ff8377840e7 in extensions::ComponentLoader::LoadAll C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\component\_loader.cc:179  

#6 0x7ff83520eb11 in extensions::ExtensionService::Init C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\extension\_service.cc:471  

#7 0x7ff83d6ff0d4 in extensions::ExtensionSystemImpl::Shared::Init C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\extension\_system\_impl.cc:283  

#8 0x7ff83d6ffb76 in extensions::ExtensionSystemImpl::InitForRegularProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\extension\_system\_impl.cc:382  

#9 0x7ff832e2a177 in ProfileManager::DoFinalInitForServices C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1591  

#10 0x7ff832e298e2 in ProfileManager::DoFinalInit C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1527  

#11 0x7ff832e1abf0 in ProfileManager::CreateAndInitializeProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:1842  

#12 0x7ff832e18436 in ProfileManager::GetProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\profiles\profile\_manager.cc:744  

#13 0x7ff838878334 in GetStartupProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\startup\startup\_browser\_creator.cc:1379  

#14 0x7ff83585dca5 in `anonymous namespace'::CreatePrimaryProfile C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:420  

#15 0x7ff83585ad32 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1425  

#16 0x7ff835859924 in ChromeBrowserMainParts::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1080  

#17 0x7ff82c1acbd2 in content::BrowserMainLoop::PreMainMessageLoopRun C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:978  

#18 0x7ff82cff502d in content::StartupTaskRunner::RunAllTasksNow C:\b\s\w\ir\cache\builder\src\content\browser\startup\_task\_runner.cc:43  

#19 0x7ff82c1ac02f in content::BrowserMainLoop::CreateStartupTasks C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:886  

#20 0x7ff82c1b3ac1 in content::BrowserMainRunnerImpl::Initialize C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:132  

#21 0x7ff82c1a87e4 in content::BrowserMain C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:26  

#22 0x7ff82ec3ab73 in content::RunBrowserProcessMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:646  

#23 0x7ff82ec3dbb3 in content::ContentMainRunnerImpl::RunBrowser C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1160  

#24 0x7ff82ec3cce6 in content::ContentMainRunnerImpl::Run C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:1026  

#25 0x7ff82ec38fbd in content::RunContentProcess C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398  

#26 0x7ff82ec3a048 in content::ContentMain C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:426  

#27 0x7ff8284f148e in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:177

SUMMARY: AddressSanitizer: heap-use-after-free C:\b\s\w\ir\cache\builder\src\net\third\_party\quiche\src\http2\core\priority\_write\_scheduler.h:267 in http2::PriorityWriteScheduler<unsigned int>::NumRegisteredStreams  

Shadow bytes around the buggy address:  

0x053468b2dcb0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa  

0x053468b2dcc0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x053468b2dcd0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x053468b2dce0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x053468b2dcf0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x053468b2dd00: fd fd fd fd fd fd fd fd fd fd fd fd fd[fd]fd fd  

0x053468b2dd10: fd fd fd fd fd fd fa fa fa fa fa fa fa fa fa fa  

0x053468b2dd20: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x053468b2dd30: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x053468b2dd40: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x053468b2dd50: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==40972==ABORTING

**CREDIT INFORMATION**  

Reporter credit: Thomas Orlita

## Attachments

- deleted (application/octet-stream, 0 B)
- [Screenshot from 2022-01-10 11-51-13.png](attachments/Screenshot from 2022-01-10 11-51-13.png) (image/png, 185.9 KB)
- [uaf.mp4](attachments/uaf.mp4) (video/mp4, 1.0 MB)
- [uaf.txt](attachments/uaf.txt) (text/plain, 19.3 KB)
- [cast.webm](attachments/cast.webm) (video/webm, 774.6 KB)

## Timeline

### [Deleted User] (2022-01-06)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-01-07)

I think it's possible there's a UAF here, but I personally can't manage to hit the button in time. Adding a security label assuming it reproduces as claimed.

alancutter@ - is it possible there's a narrow race condition with profile destruction?

[Monorail components: Platform>Apps]

### [Deleted User] (2022-01-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-07)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-07)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-01-10)

I too am too slow to press any buttons after deleting the profile. Should this be RBS?

From the stack trace it looks like the repro instructions are more like:
1. Open chrome:apps.
2. Right click Web Store app > App info.
3. Open profile manager and open delete profile confirmation.
4. Confirm delete profile and quickly press "Create shortcuts..." in the app info dialog.

### al...@chromium.org (2022-01-10)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-01-10)

Security team: Should this have RBS removed given it requires unusual user behaviour to invoke?

I'm currently seeking possible root cause fixes from the UI team as this problem seems quite generic to this circumstance.

### al...@chromium.org (2022-01-10)

Looks like this dialog is already listening for the subsystem's Shutdown() event and calling Widget::CloseWithReason() but that's an async process meaning the UI will still be alive while the chrome/browser stuff its pointing to internally has been freed.
Maybe views should generally check if the widget is closing before invoking any callbacks or firing any events and solve this entire class of UAF.

[Monorail components: UI>Browser]

### do...@chromium.org (2022-01-10)

Removing RBS - this is a browser process use after free, but the interaction required is extremely unusual, making it rather difficult to use this as an exploit vector.

### al...@chromium.org (2022-01-10)

> this dialog is already listening for the subsystem's Shutdown()

ShowCreateChromeAppShortcutsDialog() is being called by AppInfoFooterPanel's create_shortcuts_button_'s pressed callback.

AppInfoFooterPanel is a child of AppInfoDialog which has:
void AppInfoDialog::OnShutdown(extensions::ExtensionRegistry* registry) {
  DCHECK_EQ(extension_registry_, registry);
  StopObservingExtensionRegistry();
  Close();
}
void AppInfoDialog::Close() {
  GetWidget()->Close();
}

If Close() was a synchronous delete operation this would be okay but it's async so AppInfoFooterPanel continues to live with a dangling profile_ member that gets used in its UI event callbacks.

### [Deleted User] (2022-01-10)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### al...@chromium.org (2022-01-10)

RBS gets auto-added?

### al...@chromium.org (2022-01-10)

Quick fix in the CQ: https://chromium-review.googlesource.com/c/chromium/src/+/3375627

### al...@chromium.org (2022-01-10)

Filed https://bugs.chromium.org/p/chromium/issues/detail?id=1285753 for investigating a more systemic root cause fix.

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a340ac5379b5fdcda2a554cdad6fd0893bdd0dd2

commit a340ac5379b5fdcda2a554cdad6fd0893bdd0dd2
Author: Alan Cutter <alancutter@chromium.org>
Date: Tue Jan 11 00:11:06 2022

Check whether Widget is closed in AppInfoFooterPanel's create shortcuts handler

This CL adds a check to AppInfoFooterPanel::CreateShortcuts() for
whether the dialog has already been closed by the user in which case
we should not perform the action.

Bug: 1285116, 1285753
Change-Id: I8a0b8d203475b43885121488b5a8cb5f2b1423f1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3375627
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Alan Cutter <alancutter@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957331}

[modify] https://crrev.com/a340ac5379b5fdcda2a554cdad6fd0893bdd0dd2/chrome/browser/ui/views/apps/app_info_dialog/app_info_footer_panel.cc
[modify] https://crrev.com/a340ac5379b5fdcda2a554cdad6fd0893bdd0dd2/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views_browsertest.cc
[modify] https://crrev.com/a340ac5379b5fdcda2a554cdad6fd0893bdd0dd2/chrome/browser/ui/views/apps/app_info_dialog/app_info_footer_panel.h


### al...@chromium.org (2022-01-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/970872e9e03ce8f35dddbb2ca20a215ae52b34e5

commit 970872e9e03ce8f35dddbb2ca20a215ae52b34e5
Author: Mikel Astiz <mastiz@chromium.org>
Date: Tue Jan 11 10:15:11 2022

Revert "Check whether Widget is closed in AppInfoFooterPanel's create shortcuts handler"

This reverts commit a340ac5379b5fdcda2a554cdad6fd0893bdd0dd2.

Reason for revert: suspecting of introducing test failures in
AppInfoDialogBrowserTest.CreateShortcutsAfterProfileDeletion.

Bug: 1286240

Original change's description:
> Check whether Widget is closed in AppInfoFooterPanel's create shortcuts handler
>
> This CL adds a check to AppInfoFooterPanel::CreateShortcuts() for
> whether the dialog has already been closed by the user in which case
> we should not perform the action.
>
> Bug: 1285116, 1285753
> Change-Id: I8a0b8d203475b43885121488b5a8cb5f2b1423f1
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3375627
> Reviewed-by: Connie Wan <connily@chromium.org>
> Commit-Queue: Alan Cutter <alancutter@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#957331}

Bug: 1285116, 1285753
Change-Id: I1b5cba2c44c1ac4f7c60a74d924f4898e084e89c
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3380584
Owners-Override: Mikel Astiz <mastiz@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Mikel Astiz <mastiz@chromium.org>
Cr-Commit-Position: refs/heads/main@{#957491}

[modify] https://crrev.com/970872e9e03ce8f35dddbb2ca20a215ae52b34e5/chrome/browser/ui/views/apps/app_info_dialog/app_info_footer_panel.cc
[modify] https://crrev.com/970872e9e03ce8f35dddbb2ca20a215ae52b34e5/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views_browsertest.cc
[modify] https://crrev.com/970872e9e03ce8f35dddbb2ca20a215ae52b34e5/chrome/browser/ui/views/apps/app_info_dialog/app_info_footer_panel.h


### st...@gmail.com (2022-01-11)

Thanks for the updated steps in https://crbug.com/chromium/1285116#c6, yes, it should have been the "Create shortcuts..." button in the App info dialog instead.
I initially thought I was too slow to click the button so I tried clicking it really fast every time, when actually I was too quick and when I pressed the button the profile was still alive, so nothing happened.
Knowing this, I can now repro this reliably.

### st...@gmail.com (2022-01-11)

I can still reproduce this at commit position 957333 and 957369 (which are after the commit and before the revert).

### al...@chromium.org (2022-01-11)

CL was reverted.

### al...@chromium.org (2022-01-12)

How long does the Create Shortcuts button remain open for you after deleting the profile?
Can you share the crash stack you saw in #20?

### al...@chromium.org (2022-01-12)

I've not been able to repro this manually on Linux or Windows, the dialog closes too fast to be clicked.

### al...@chromium.org (2022-01-12)

In your video in #19 it looked as if the app info dialog sticks around longer than the browser window, in my testing it disappears at the same time.

### al...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### al...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### st...@gmail.com (2022-01-12)

https://crbug.com/chromium/1285116#c22: The whole App info dialog is still opened around 400-600ms after Delete is pressed.
https://crbug.com/chromium/1285116#c23: In the video, I focused the Delete button using Tab and positioned the mouse pointer over the Create shortcuts button, so then you can just press Enter and click. This is easier as you don't have to move the mouse at all. But I can repro using mouse only as well.
https://crbug.com/chromium/1285116#c24: I tried this on two Windows devices running an ASAN build, and on both the browser window is closed first and it takes a few hundred ms for the dialog to close. 

### st...@gmail.com (2022-01-12)

https://crbug.com/chromium/1285116#c22: This stack trace should be identical to the one in the video.

### al...@chromium.org (2022-01-13)

I get no time at all to press the button, unable to repro manually.

### al...@chromium.org (2022-01-13)

I see the issue now, this happens between Extension unloading and profile deletion.

freed by thread T0 here:
    #0 0x7ff6bd95234b in free C:\b\s\w\ir\cache\builder\src\third_party\llvm\compiler-rt\lib\asan\asan_malloc_win.cpp:82
    #1 0x7ff82de9daa1 in extensions::ExtensionRegistrar::RemoveExtension C:\b\s\w\ir\cache\builder\src\extensions\browser\extension_registrar.cc:184
    #2 0x7ff8350fd03c in extensions::ExtensionService::OnProfileMarkedForPermanentDeletion C:\b\s\w\ir\cache\builder\src\chrome\browser\extensions\extension_service.cc:2191

AppInfoDialog listens for OnExtensionUninstalled to close itself but not OnExtensionUnloaded. I suspect your machine takes a little while to unload the extensions for whatever reason.

[Monorail components: -Platform>Apps -UI>Browser Platform>Extensions]

### al...@chromium.org (2022-01-13)

Would you be able to patch in https://chromium-review.googlesource.com/c/chromium/src/+/3384896 to verify it fixes the UAF?

### st...@gmail.com (2022-01-13)

I tried the patch and can confirm I can't reproduce the bug anymore - `OnExtensionUnloaded` closes the dialog before I am able to press the button. This also fixes https://crbug.com/chromium/1286508 and 1286511.

### gi...@appspot.gserviceaccount.com (2022-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f6350c9fcc7d872d04343ad7df10ff469f16a32b

commit f6350c9fcc7d872d04343ad7df10ff469f16a32b
Author: Alan Cutter <alancutter@chromium.org>
Date: Thu Jan 13 22:01:59 2022

Close AppInfoPanel when corresponding Extension has been unloaded

This CL updates AppInfoPanel to close itself when its corresponding
Extension has been unloaded from the system.

Bug: 1285116, 1286508, 1286511
Change-Id: I02064540549c1fb0d33c6a3ef8e48398c849b3f8
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3384896
Reviewed-by: Connie Wan <connily@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Commit-Queue: Alan Cutter <alancutter@chromium.org>
Cr-Commit-Position: refs/heads/main@{#958854}

[modify] https://crrev.com/f6350c9fcc7d872d04343ad7df10ff469f16a32b/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views.h
[modify] https://crrev.com/f6350c9fcc7d872d04343ad7df10ff469f16a32b/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views.cc
[modify] https://crrev.com/f6350c9fcc7d872d04343ad7df10ff469f16a32b/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views_browsertest.cc
[modify] https://crrev.com/f6350c9fcc7d872d04343ad7df10ff469f16a32b/chrome/browser/extensions/extension_service.h


### al...@chromium.org (2022-01-14)

#32 thanks for the help!

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b24759852b71a4c7ae12ace050ff48601f4ba3a0

commit b24759852b71a4c7ae12ace050ff48601f4ba3a0
Author: Alan Cutter <alancutter@chromium.org>
Date: Wed Jan 19 06:58:45 2022

Follow up nits for https://chromium-review.googlesource.com/c/chromium/src/+/3384896

This CL fixes nits left in
https://chromium-review.googlesource.com/c/chromium/src/+/3384896 that
I forgot to check for before landing.

Bug: 1285116, 1286508, 1286511
Change-Id: I694eb40854d7f65490b9589c5a649a0b918b5b2d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3386336
Auto-Submit: Alan Cutter <alancutter@chromium.org>
Reviewed-by: Reilly Grant <reillyg@chromium.org>
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/heads/main@{#960810}

[modify] https://crrev.com/b24759852b71a4c7ae12ace050ff48601f4ba3a0/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views.h
[modify] https://crrev.com/b24759852b71a4c7ae12ace050ff48601f4ba3a0/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views.cc
[modify] https://crrev.com/b24759852b71a4c7ae12ace050ff48601f4ba3a0/chrome/browser/ui/views/apps/app_info_dialog/app_info_dialog_views_browsertest.cc
[modify] https://crrev.com/b24759852b71a4c7ae12ace050ff48601f4ba3a0/chrome/browser/extensions/extension_service.h


### al...@chromium.org (2022-01-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-22)

Not requesting merge to dev (M99) because latest trunk commit (960810) appears to be prior to dev branch point (961656). If this is incorrect, please replace the Merge-NA-99 label with Merge-Request-99. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-02-17)

[Empty comment from Monorail migration]

### am...@google.com (2022-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-02-18)

Hello, Thomas. Due to the lack of reliability in triggering this issue in our attempts to reproduce and that it requires an exceptionally high degree of user interaction, the VRP Panel has decided to award you $2,000 for this report. We appreciate your efforts with this issue and reporting it to us. 

### am...@google.com (2022-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1285116?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1286240]
[Monorail mergedwith: crbug.com/chromium/1286508]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40058418)*
