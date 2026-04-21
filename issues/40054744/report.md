# Security: Heap-buffer-overflow in TabStripModel::IsTabPinned

| Field | Value |
|-------|-------|
| **Issue ID** | [40054744](https://issues.chromium.org/issues/40054744) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2021-02-08 |
| **Bounty** | $10,000.00 |

## Description

Chrome Version: Chromium 90.0.4413.0 and stable  

Operating System: Windows 7 and Linux

**REPRODUCTION CASE**

1. python -m SimpleHTTPServer
2. chrome.exe "about:blank" "<http://localhost:8000/poc.html>"
3. Add "about:blank" tab to a new group.
4. Switch "<http://localhost:8000/poc.html>" tab and click on the button
5. Right-click over "<http://localhost:8000/poc.html>" tab and wait until the tab is closed then select "Add tab to new group" >> "about:blank"

=================================================================  

==3588==ERROR: AddressSanitizer: container-overflow on address 0x0105411fe0d8 at pc 0x07fecdef8a75 bp 0x00000088d580 sp 0x00000088d5c8  

READ of size 8 at 0x0105411fe0d8 thread T0  

#0 0x7fecdef8a74 in std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >::operator-> C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\i  

nclude\memory:2602  

#1 0x7fecdef8a74 in TabStripModel::IsTabPinned C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:816  

#2 0x7fecdef8a74 in TabStripModel::MoveAndSetGroup(int, int, class base::Optional<class tab\_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2136:18  

#3 0x7fecdeedf63 in TabStripModel::MoveTabsAndSetGroupImpl(class std::\_\_1::vector<int, class std::\_\_1::allocator<int>> const &, int, class base::Optional<class tab\_groups::TabGroupId>) C:\b\s\w\ir\cache\bu  

ilder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:2122:5  

#4 0x7fecdeed686 in TabStripModel::AddToExistingGroupImpl(class std::\_\_1::vector<int, class std::\_\_1::allocator<int>> const &, class tab\_groups::TabGroupId const &) C:\b\s\w\ir\cache\builder\src\chrome\bro  

wser\ui\tabs\tab\_strip\_model.cc:2094:3  

#5 0x7fecdef5a26 in TabStripModel::AddToExistingGroup C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1070  

#6 0x7fecdef5a26 in TabStripModel::ExecuteAddToExistingGroupCommand(int, class tab\_groups::TabGroupId const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1471:3  

#7 0x7fed817e439 in ExistingTabGroupSubMenuModel::ExecuteExistingCommand(int) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\existing\_tab\_group\_sub\_menu\_model.cc:92:12  

#8 0x7fed63fa713 in views::MenuModelAdapter::ExecuteCommand(int, int) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_model\_adapter.cc:165:12  

#9 0x7fed3ea9eff in views::internal::MenuRunnerImpl::OnMenuClosed(enum views::internal::MenuControllerDelegate::NotifyType, class views::MenuItemView \*, int) C:\b\s\w\ir\cache\builder\src\ui\views\controls  

\menu\menu\_runner\_impl.cc:244:29  

#10 0x7fed63feb9c in views::MenuController::ExitMenu(void) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:3041:13  

#11 0x7fed6403514 in views::MenuController::Accept C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:1727  

#12 0x7fed6403514 in views::MenuController::OnMouseReleased(class views::SubmenuView \*, class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\controls\menu\menu\_controller.cc:818:7  

#13 0x7fec969b6ba in views::Widget::OnMouseEvent(class ui::MouseEvent \*) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1318:20  

#14 0x7feca507f74 in ui::EventHandler::OnEvent(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_handler.cc:37:5  

#15 0x7feca506979 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191:12  

#16 0x7feca505de8 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140:5  

#17 0x7feca5057d4 in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84:14  

#18 0x7feca505418 in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56:15  

#19 0x7fecedfeea0 in ui::EventProcessor::OnEventFromSource(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49:17  

#20 0x7fecbe90f03 in ui::EventSource::DeliverEventToSink(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113:16  

#21 0x7fecbe90b5d in ui::EventSource::SendEventToSinkFromRewriter(class ui::Event const \*, class ui::EventRewriter const \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:138:12  

#22 0x7fecbe9065b in ui::EventSource::SendEventToSink(class ui::Event const \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:107:10  

#23 0x7fecedfbd01 in views::DesktopWindowTreeHostWin::HandleMouseEvent(class ui::MouseEvent \*) C:\b\s\w\ir\cache\builder\src\ui\views\widget\desktop\_aura\desktop\_window\_tree\_host\_win.cc:958:3  

#24 0x7fed2c737c9 in views::HWNDMessageHandler::HandleMouseEventInternal(unsigned int, unsigned \_\_int64, \_*int64, bool) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:3130:26  

#25 0x7fed2c6cc0b in views::HWNDMessageHandler::OnMouseRange C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1956  

#26 0x7fed2c6cc0b in views::HWNDMessageHandler::*ProcessWindowMessage(struct HWND**\*, unsigned int, unsigned \_\_int64, \_\_int64, \_\_int64 &, unsigned long) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_mess  

age\_handler.h:356:5  

#27 0x7fed2c6c325 in views::HWNDMessageHandler::OnWndProc(unsigned int, unsigned \_\_int64, **int64) C:\b\s\w\ir\cache\builder\src\ui\views\win\hwnd\_message\_handler.cc:1009:7  

#28 0x7fecc6296dc in gfx::WindowImpl::WndProc(struct HWND**\*, unsigned int, unsigned \_\_int64, **int64) C:\b\s\w\ir\cache\builder\src\ui\gfx\win\window\_impl.cc:305:18  

#29 0x7fecc628083 in base::win::WrappedWindowProc<&gfx::WindowImpl::WndProc(struct HWND**\*, unsigned int, unsigned \_\_int64, **int64)>(struct HWND**\*, unsigned int, unsigned \_*int64, **int64) C:\b\s\w\ir\ca  

che\builder\src\base\win\wrapped\_window\_proc.h:74:10  

#30 0x4539bd0 (C:\Windows\system32\USER32.dll+0x78c39bd0)  

#31 0x45398d9 (C:\Windows\system32\USER32.dll+0x78c398d9)  

#32 0x7fec98a7fb3 in base::MessagePumpForUI::ProcessMessageHelper(struct tagMSG const &) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:537:3  

#33 0x7fec98a5eba in base::MessagePumpForUI::ProcessNextWindowsMessage(void) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:504:31  

#34 0x7fec98a57ac in base::MessagePumpForUI::DoRunLoop(void) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:219:35  

#35 0x7fec98a332a in base::MessagePumpWin::Run(class base::MessagePump::Delegate \*) C:\b\s\w\ir\cache\builder\src\base\message\_loop\message\_pump\_win.cc:80:3  

#36 0x7fecbfaf7cf in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, class base::TimeDelta) C:\b\s\w\ir\cache\builder\src\base\task\sequence\_manager\thread\_controller\_with*  

message\_pump\_impl.cc:460:12  

#37 0x7fec97a8303 in base::RunLoop::Run(class base::Location const &) C:\b\s\w\ir\cache\builder\src\base\run\_loop.cc:133:14  

#38 0x7fecc0ea238 in ChromeBrowserMainParts::MainMessageLoopRun(int \*) C:\b\s\w\ir\cache\builder\src\chrome\browser\chrome\_browser\_main.cc:1740:15  

#39 0x7fec33dfd01 in content::BrowserMainLoop::RunMainMessageLoopParts(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_loop.cc:970:29  

#40 0x7fec33e5a8f in content::BrowserMainRunnerImpl::Run(void) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main\_runner\_impl.cc:150:15  

#41 0x7fec33d8512 in content::BrowserMain(struct content::MainFunctionParams const &) C:\b\s\w\ir\cache\builder\src\content\browser\browser\_main.cc:47:28  

#42 0x7fec9563353 in content::RunBrowserProcessMain(struct content::MainFunctionParams const &, class content::ContentMainDelegate \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:5  

16:10  

#43 0x7fec9565cab in content::ContentMainRunnerImpl::RunBrowser(struct content::MainFunctionParams &, bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:997:10  

#44 0x7fec9565027 in content::ContentMainRunnerImpl::Run(bool) C:\b\s\w\ir\cache\builder\src\content\app\content\_main\_runner\_impl.cc:875:12  

#45 0x7fec956220e in content::RunContentProcess(struct content::ContentMainParams const &, class content::ContentMainRunner \*) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:372:36  

#46 0x7fec95627f8 in content::ContentMain(struct content::ContentMainParams const &) C:\b\s\w\ir\cache\builder\src\content\app\content\_main.cc:398:10  

#47 0x7febf78145a in ChromeMain C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_main.cc:141:12  

#48 0x13f3e5ac1 in MainDllLoader::Launch(struct HINSTANCE**\*, class base::TimeTicks) C:\b\s\w\ir\cache\builder\src\chrome\app\main\_dll\_loader\_win.cc:169:12  

#49 0x13f3e29b7 in main C:\b\s\w\ir\cache\builder\src\chrome\app\chrome\_exe\_main\_win.cc:351:20  

#50 0x13f7c0dbf in invoke\_main d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:78  

#51 0x13f7c0dbf in \_\_scrt\_common\_main\_seh d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\startup\exe\_common.inl:288  

#52 0x7768652c (C:\Windows\system32\kernel32.dll+0x78d3652c)  

#53 0x778bc520 (C:\Windows\SYSTEM32\ntdll.dll+0x78e7c520)

0x0105411fe0d8 is located 8 bytes inside of 16-byte region [0x0105411fe0d0,0x0105411fe0e0)  

allocated by thread T0 here:  

#0 0x13f4842ab in malloc C:\b\s\w\ir\cache\builder\src\third\_party\llvm\compiler-rt\lib\asan\asan\_malloc\_win.cpp:98  

#1 0x7fedbbfacaa in operator new(unsigned \_\_int64) d:\A01\_work\6\s\src\vctools\crt\vcstartup\src\heap\new\_scalar.cpp:35  

#2 0x7fecdef6a1f in std::\_\_1::\_\_libcpp\_allocate C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\new:253  

#3 0x7fecdef6a1f in std::\_\_1::allocator<std::unique\_ptr<TabStripModel::WebContentsData,std::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > >::allocate C:\b\s\w\ir\cache\builder\src\buildtools\third\_party  

\libc++\trunk\include\memory:1853  

#4 0x7fecdef6a1f in std::\_\_1::allocator\_traits<std::allocator<std::unique\_ptr<TabStripModel::WebContentsData,std::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::allocate C:\b\s\w\ir\cache\builder\sr  

c\buildtools\third\_party\libc++\trunk\include\memory:1570  

#5 0x7fecdef6a1f in std::\_\_1::\_\_split\_buffer<std::unique\_ptr<TabStripModel::WebContentsData,std::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >,std::allocator<std::unique\_ptr<TabStripModel::WebContentsDa  

ta,std::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > &>::\_\_split\_buffer C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\_\_split\_buffer:318  

#6 0x7fecdef6a1f in std::\_\_1::vector<class std::\_\_1::unique\_ptr<class TabStripModel::WebContentsData, struct std::\_\_1::default\_delete<class TabStripModel::WebContentsData>>, class std::\_\_1::allocator<class  

std::\_\_1::unique\_ptr<class TabStripModel::WebContentsData, struct std::\_\_1::default\_delete<class TabStripModel::WebContentsData>>>>::insert(class std::\_\_1::\_\_wrap\_iter<class std::\_\_1::unique\_ptr<class TabStri  

pModel::WebContentsData, struct std::\_\_1::default\_delete<class TabStripModel::WebContentsData>> const \*>, class std::\_\_1::unique\_ptr<class TabStripModel::WebContentsData, struct std::\_\_1::default\_delete<class
TabStripModel::WebContentsData>> &&) C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\vector:1825:53  

#7 0x7fecdede5c1 in TabStripModel::InsertWebContentsAtImpl(int, class std::\_\_1::unique\_ptr<class content::WebContents, struct std::\_\_1::default\_delete<class content::WebContents>>, int, class base::Optiona  

l<class tab\_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:1715:18  

#8 0x7fecdeeaed2 in TabStripModel::AddWebContents(class std::\_\_1::unique\_ptr<class content::WebContents, struct std::\_\_1::default\_delete<class content::WebContents>>, int, enum ui::PageTransition, int, cla  

ss base::Optional<class tab\_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\tabs\tab\_strip\_model.cc:982:3  

#9 0x7fecbaee07e in Navigate(struct NavigateParams \*) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_navigator.cc:702:41  

#10 0x7fecf4a675d in chrome::AddTabAt(class Browser \*, class GURL const &, int, bool, class base::Optional<class tab\_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browser\_tabstrip.cc  

:40:3  

#11 0x7fecfb41e2d in chrome::BrowserTabStripModelDelegate::AddTabAt(class GURL const &, int, bool, class base::Optional<class tab\_groups::TabGroupId>) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\browse  

r\_tab\_strip\_model\_delegate.cc:53:3  

#12 0x7fed3599411 in BrowserTabStripController::CreateNewTab(void) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\browser\_tab\_strip\_controller.cc:464:23  

#13 0x7fed35b50ce in TabStrip::NewTabButtonPressed(class ui::Event const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\tab\_strip.cc:2613:16  

#14 0x7fed66236ec in NewTabButton::NotifyClick(class ui::Event const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\new\_tab\_button.cc:140:16  

#15 0x7fecbe5549a in views::ButtonController::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\controls\button\button\_controller.cc:58:34  

#16 0x7fed66234c2 in NewTabButton::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\chrome\browser\ui\views\tabs\new\_tab\_button.cc:115:25  

#17 0x7fec9673b0c in views::View::ProcessMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\view.cc:3021:5  

#18 0x7feca507f74 in ui::EventHandler::OnEvent(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_handler.cc:37:5  

#19 0x7fed2c15846 in ui::ScopedTargetHandler::OnEvent(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\scoped\_target\_handler.cc:28:24  

#20 0x7feca506979 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191:12  

#21 0x7feca505de8 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140:5  

#22 0x7feca5057d4 in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84:14  

#23 0x7feca505418 in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56:15  

#24 0x7fecbea18f2 in views::internal::RootView::OnMouseReleased(class ui::MouseEvent const &) C:\b\s\w\ir\cache\builder\src\ui\views\widget\root\_view.cc:475:9  

#25 0x7fec969b6ba in views::Widget::OnMouseEvent(class ui::MouseEvent \*) C:\b\s\w\ir\cache\builder\src\ui\views\widget\widget.cc:1318:20  

#26 0x7feca507f74 in ui::EventHandler::OnEvent(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_handler.cc:37:5  

#27 0x7feca506979 in ui::EventDispatcher::DispatchEvent(class ui::EventHandler \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:191:12  

#28 0x7feca505de8 in ui::EventDispatcher::ProcessEvent(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:140:5  

#29 0x7feca5057d4 in ui::EventDispatcherDelegate::DispatchEventToTarget(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:84:14  

#30 0x7feca505418 in ui::EventDispatcherDelegate::DispatchEvent(class ui::EventTarget \*, class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_dispatcher.cc:56:15  

#31 0x7fecedfeea0 in ui::EventProcessor::OnEventFromSource(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_processor.cc:49:17  

#32 0x7fecbe90f03 in ui::EventSource::DeliverEventToSink(class ui::Event \*) C:\b\s\w\ir\cache\builder\src\ui\events\event\_source.cc:113:16

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.  

If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.  

SUMMARY: AddressSanitizer: container-overflow C:\b\s\w\ir\cache\builder\src\buildtools\third\_party\libc++\trunk\include\memory:2602 in std::\_\_1::unique\_ptr<TabStripModel::WebContentsData,std::default\_delete<Ta
bStripModel::WebContentsData> >::operator->  

Shadow bytes around the buggy address:  

0x0021e91bfbc0: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa  

0x0021e91bfbd0: fa fa fd fd fa fa fd fd fa fa fd fa fa fa fd fa  

0x0021e91bfbe0: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0021e91bfbf0: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa  

0x0021e91bfc00: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa  

=>0x0021e91bfc10: fa fa fd fa fa fa fd fa fa fa 00[fc]fa fa fd fa  

0x0021e91bfc20: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fa  

0x0021e91bfc30: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fd  

0x0021e91bfc40: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0021e91bfc50: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

0x0021e91bfc60: fa fa fd fd fa fa fd fd fa fa fd fd fa fa fd fd  

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

Shadow gap: cc  

==3588==ABORTING

## Attachments

- [screen.mov](attachments/screen.mov) (video/quicktime, 7.3 MB)
- [poc.html](attachments/poc.html) (text/plain, 176 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 2.5 MB)

## Timeline

### [Deleted User] (2021-02-08)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-02-09)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>TabStrip]

### ch...@gmail.com (2021-02-09)

Sorry! I forgot to attach the test case.

### [Deleted User] (2021-02-09)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2021-02-13)

Okay, many possible solutions to this, roughly from easy to hard:
- if a command is targeting a nonexistent tab, abort the command
- make the tab context menus track their tabs by webcontents pointer instead of model index, so they can handle their tab being moved or destroyed
- close tab context menus if the associated tab is destroyed or moved
- prevent tabs from closing if there is a tab context menu open (this happens today on Mac, just as with drag sessions)

I'm inclined to go with option 2 for now, but 4 is interesting since it could maybe be applied to the drag-related issues as well.

### tb...@chromium.org (2021-02-16)

Ah, I misunderstood how the context menu kept its state - it tracks by Tab* rather than index. So what's happening here is exclusively that the index for the destroyed Tab is kNoTab, and executing a command with kNoTab will crash.

So solution #1 seems very sufficient to me, in that case.

### tb...@chromium.org (2021-02-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/12d27cd07326e226c2af8d9885ed9bea2029ddef

commit 12d27cd07326e226c2af8d9885ed9bea2029ddef
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed Feb 17 23:35:58 2021

Fix crash when executing a context menu command on a closed tab.

Bug: 1175992
Change-Id: I87c8b98986589420c386269a44ccb70958e98bc5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2698641
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/master@{#855015}

[modify] https://crrev.com/12d27cd07326e226c2af8d9885ed9bea2029ddef/chrome/browser/ui/tabs/tab_strip_model.cc


### tb...@chromium.org (2021-02-19)

Khalil, could I ask you to verify this fix too? :)
Also adding merge request labels since this probably should be merged if the others were.

### [Deleted User] (2021-02-19)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2021-02-19)

Oh! I'm still able to repro this bug on Canary 90.0.4423.0 on Windows, I thought there was more work here that is why I said nothing.

### [Deleted User] (2021-02-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-20)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-22)

Reopening per https://crbug.com/chromium/1175992#c11.

### ch...@gmail.com (2021-02-25)

[Empty comment from Monorail migration]

### tb...@chromium.org (2021-02-26)

Okay, I see what happened here. The add to new/existing group/window commands work differently, they *do* keep track of a tabstrip model index instead of a Tab*, unlike all the commands directly in the context menu.

### [Deleted User] (2021-03-03)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-03-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/953a2de72f60e07289dcfcc38dc8bad127e7092f

commit 953a2de72f60e07289dcfcc38dc8bad127e7092f
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed Mar 03 18:33:24 2021

Fix container overflow in add to existing window and group tab context menu commands.

Bug: 1175992
Change-Id: I8ea739c12d030a1fec9d7ee6116d67b9cdd72f5f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2724815
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/heads/master@{#859460}

[modify] https://crrev.com/953a2de72f60e07289dcfcc38dc8bad127e7092f/chrome/browser/ui/tabs/existing_base_sub_menu_model.cc
[modify] https://crrev.com/953a2de72f60e07289dcfcc38dc8bad127e7092f/chrome/browser/ui/tabs/existing_base_sub_menu_model.h
[modify] https://crrev.com/953a2de72f60e07289dcfcc38dc8bad127e7092f/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/953a2de72f60e07289dcfcc38dc8bad127e7092f/chrome/browser/ui/tabs/existing_window_sub_menu_model.cc
[modify] https://crrev.com/953a2de72f60e07289dcfcc38dc8bad127e7092f/chrome/browser/ui/tabs/tab_strip_model.cc


### ch...@gmail.com (2021-03-03)

Verified on Chromium 91.0.4436.0 (master/859461). Fixed.

### tb...@google.com (2021-03-03)

Cool cool! Adding merge request again.

### [Deleted User] (2021-03-04)

Your change meets the bar and is auto-approved for M90. Please go ahead and merge the CL to branch 4430 (refs/branch-heads/4430) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-03-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f262c020294eb14092dc8cab4386cc9df3e46e54

commit f262c020294eb14092dc8cab4386cc9df3e46e54
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Fri Mar 05 01:29:11 2021

Fix container overflow in add to existing window and group tab context menu commands.

(cherry picked from commit 953a2de72f60e07289dcfcc38dc8bad127e7092f)

Bug: 1175992
Change-Id: I8ea739c12d030a1fec9d7ee6116d67b9cdd72f5f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2724815
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#859460}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2737937
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4430@{#139}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/f262c020294eb14092dc8cab4386cc9df3e46e54/chrome/browser/ui/tabs/existing_base_sub_menu_model.cc
[modify] https://crrev.com/f262c020294eb14092dc8cab4386cc9df3e46e54/chrome/browser/ui/tabs/existing_base_sub_menu_model.h
[modify] https://crrev.com/f262c020294eb14092dc8cab4386cc9df3e46e54/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/f262c020294eb14092dc8cab4386cc9df3e46e54/chrome/browser/ui/tabs/existing_window_sub_menu_model.cc
[modify] https://crrev.com/f262c020294eb14092dc8cab4386cc9df3e46e54/chrome/browser/ui/tabs/tab_strip_model.cc


### ad...@google.com (2021-03-10)

Re-adding merge request for M89 for consideration, as is normal practice for high severity security fixes.

### [Deleted User] (2021-03-10)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-03-10)

I think I'd like to leave this to bake a few more days in M90/trunk before approving M89 merge.

### am...@google.com (2021-03-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-03-10)

Congratulations, Khalil! The VRP Panel has decided to reward you $10,000 for this report. Great work! 

### am...@google.com (2021-03-11)

[Empty comment from Monorail migration]

### ad...@google.com (2021-03-23)

Approving merge to M89, branch 4389.

### pb...@google.com (2021-03-25)

The change has been merged to M89 branch as part and here it is : https://chromium-review.googlesource.com/c/chromium/src/+/2785341

Also verified that the change is part of https://chromium.googlesource.com/chromium/src.git/+log/refs/branch-heads/4389, hence dropping Merge-Approved-89 and adding "merge-merged-4389 and merge-merged-89"

### ad...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-29)

[Empty comment from Monorail migration]

### as...@google.com (2021-03-30)

[Empty comment from Monorail migration]

### su...@chromium.org (2021-03-30)

Merge approved for LTS-86

### gi...@appspot.gserviceaccount.com (2021-03-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ee0e4067563a692552f872e37323abdf0f602298

commit ee0e4067563a692552f872e37323abdf0f602298
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed Mar 31 19:26:03 2021

Fix container overflow in add to existing window and group tab context menu commands.

M86 merge conflicts and resolution:
* chrome/browser/ui/tabs/tab_strip_model.cc
  No actual conflicts. Automerge could not handle empty lines.
* chrome/browser/ui/tabs/tab_strip_model.cc
  Dropped DCHECK on base::ranges::is_sorted because the method not present in M86.

(cherry picked from commit 953a2de72f60e07289dcfcc38dc8bad127e7092f)

(cherry picked from commit efe9d14d92248b93ad4fadde00df0c4dc49e7193)

Bug: 1175992
Change-Id: I8ea739c12d030a1fec9d7ee6116d67b9cdd72f5f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2724815
Reviewed-by: Connie Wan <connily@chromium.org>
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#859460}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2785341
Reviewed-by: Prudhvi Kumar Bommana <pbommana@google.com>
Reviewed-by: Krishna Govind <govind@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Prudhvi Kumar Bommana <pbommana@google.com>
Cr-Original-Commit-Position: refs/branch-heads/4389@{#1596}
Cr-Original-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2794550
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Reviewed-by: Artem Sumaneev <asumaneev@google.com>
Auto-Submit: Artem Sumaneev <asumaneev@google.com>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4240@{#1588}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/ee0e4067563a692552f872e37323abdf0f602298/chrome/browser/ui/tabs/existing_base_sub_menu_model.cc
[modify] https://crrev.com/ee0e4067563a692552f872e37323abdf0f602298/chrome/browser/ui/tabs/existing_base_sub_menu_model.h
[modify] https://crrev.com/ee0e4067563a692552f872e37323abdf0f602298/chrome/browser/ui/tabs/existing_tab_group_sub_menu_model.cc
[modify] https://crrev.com/ee0e4067563a692552f872e37323abdf0f602298/chrome/browser/ui/tabs/existing_window_sub_menu_model.cc
[modify] https://crrev.com/ee0e4067563a692552f872e37323abdf0f602298/chrome/browser/ui/tabs/tab_strip_model.cc


### as...@google.com (2021-03-31)

[Empty comment from Monorail migration]

### am...@google.com (2021-04-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-07-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1175992?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054744)*
