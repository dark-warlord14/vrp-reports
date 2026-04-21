# Security: Heap-use-after-free in ash::ScopedOverviewHideWindows::~ScopedOverviewHideWindows

| Field | Value |
|-------|-------|
| **Issue ID** | [40061277](https://issues.chromium.org/issues/40061277) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Views>Desktop |
| **Platforms** | ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2022-10-08 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 108.0.5348.0  

Operating System: ChromeOS

**REPRODUCTION CASE**  

0. ./chrome --enable-features=DesksTemplates

1. Open Chromium browser
2. Press F5 >> Save desk as a template >> Use tamplate
3. Right-click on Chromium icon >> Close

=================================================================  

==12086==ERROR: AddressSanitizer: heap-use-after-free on address 0x615000907610 at pc 0x55c20e10d3dd bp 0x7fff09d12aa0 sp 0x7fff09d12a98  

READ of size 8 at 0x615000907610 thread T0 (chrome)  

==12086==WARNING: invalid path to external symbolizer!  

==12086==WARNING: Failed to use and restart external symbolizer!  

#0 0x55c20e10d3dc in begin ./../../buildtools/third\_party/libc++/trunk/include/vector:1374:33  

#1 0x55c20e10d3dc in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:44:37  

#2 0x55c20e10d3dc in begin<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &> ./../../base/ranges/ranges.h:105:10  

#3 0x55c20e10d3dc in find\_if<std::Cr::vector<base::internal::CheckedObserverAdapter, std::Cr::allocator[base::internal::CheckedObserverAdapter](javascript:void(0);) > &, (lambda at ../../base/observer\_list.h:287:21), base::identity, std::Cr::random\_access\_iterator\_tag> ./../../base/ranges/algorithm.h:483:26  

#4 0x55c20e10d3dc in base::ObserverList<aura::WindowObserver, true, true, base::internal::CheckedObserverAdapter>::RemoveObserver(aura::WindowObserver const\*) ./../../base/observer\_list.h:286:21  

#5 0x55c20f124def in ash::ScopedOverviewHideWindows::~ScopedOverviewHideWindows() ./../../ash/wm/overview/scoped\_overview\_hide\_windows.cc:24:20  

#6 0x55c20f124f55 in ash::ScopedOverviewHideWindows::~ScopedOverviewHideWindows() ./../../ash/wm/overview/scoped\_overview\_hide\_windows.cc:22:57  

#7 0x55c20f10c46b in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#8 0x55c20f10c46b in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#9 0x55c20f10c46b in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#10 0x55c20f10c46b in ash::OverviewSession::~OverviewSession() ./../../ash/wm/overview/overview\_session.cc:167:1  

#11 0x55c20f10c86b in ash::OverviewSession::~OverviewSession() ./../../ash/wm/overview/overview\_session.cc:159:37  

#12 0x55c208a987fc in Run ./../../base/functional/callback.h:145:12  

#13 0x55c208a987fc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:133:32  

#14 0x55c208addbc7 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:443:29)> ./../../base/task/common/task\_annotator.h:72:5  

#15 0x55c208addbc7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:441:21  

#16 0x55c208adcced in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:297:30  

#17 0x55c208adee14 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0  

#18 0x55c208bf04c8 in base::MessagePumpLibevent::Run(base::MessagePump::Delegate\*) ./../../base/message\_loop/message\_pump\_libevent.cc:294:55  

#19 0x55c208adf8c5 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:600:12  

#20 0x55c208a2c849 in base::RunLoop::Run(base::Location const&) ./../../base/run\_loop.cc:141:14  

#21 0x55c2010cbe04 in content::BrowserMainLoop::RunMainMessageLoop() ./../../content/browser/browser\_main\_loop.cc:1048:18  

#22 0x55c2010d0cd8 in content::BrowserMainRunnerImpl::Run() ./../../content/browser/browser\_main\_runner\_impl.cc:160:15  

#23 0x55c2010c62ba in content::BrowserMain(content::MainFunctionParams) ./../../content/browser/browser\_main.cc:30:28  

#24 0x55c2087dbfb5 in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) ./../../content/app/content\_main\_runner\_impl.cc:710:10  

#25 0x55c2087de66d in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) ./../../content/app/content\_main\_runner\_impl.cc:1243:10  

#26 0x55c2087de084 in content::ContentMainRunnerImpl::Run() ./../../content/app/content\_main\_runner\_impl.cc:1103:12  

#27 0x55c2087d7fb4 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) ./../../content/app/content\_main.cc:342:36  

#28 0x55c2087d8562 in content::ContentMain(content::ContentMainParams) ./../../content/app/content\_main.cc:370:10  

#29 0x55c1f8f45a30 in ChromeMain ./../../chrome/app/chrome\_main.cc:175:12  

#30 0x7f90c9aa50b2 in \_\_libc\_start\_main /build/glibc-sMfBJT/glibc-2.31/csu/../csu/libc-start.c:308:16

0x615000907610 is located 400 bytes inside of 504-byte region [0x615000907480,0x615000907678)  

freed by thread T0 (chrome) here:  

#0 0x55c1f8f43abd in operator delete(void\*) *asan\_rtl*:3  

#1 0x55c20e72295a in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#2 0x55c20e72295a in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#3 0x55c20e72295a in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#4 0x55c20e72295a in views::NativeViewHostAura::~NativeViewHostAura() ./../../ui/views/controls/native/native\_view\_host\_aura.cc:91:1  

#5 0x55c20e722ab3 in views::NativeViewHostAura::~NativeViewHostAura() ./../../ui/views/controls/native/native\_view\_host\_aura.cc:80:43  

#6 0x55c20e72086e in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#7 0x55c20e72086e in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#8 0x55c20e72086e in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#9 0x55c20e72086e in views::NativeViewHost::~NativeViewHost() ./../../ui/views/controls/native/native\_view\_host.cc:36:1  

#10 0x55c20e720bff in views::NativeViewHost::~NativeViewHost() ./../../ui/views/controls/native/native\_view\_host.cc:32:35  

#11 0x55c20e55f979 in views::View::~View() ./../../ui/views/view.cc:266:9  

#12 0x55c21afbe1cf in ContentsWebView::~ContentsWebView() ./../../chrome/browser/ui/views/frame/contents\_web\_view.cc:31:37  

#13 0x55c20e55f979 in views::View::~View() ./../../ui/views/view.cc:266:9  

#14 0x55c20e56049d in views::View::~View() ./../../ui/views/view.cc:231:15  

#15 0x55c20e5616f8 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#16 0x55c20e5616f8 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#17 0x55c20e5616f8 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#18 0x55c20e5616f8 in views::View::DoRemoveChildView(views::View\*, bool, bool, views::View\*) ./../../ui/views/view.cc:2738:1  

#19 0x55c20e561924 in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:340:5  

#20 0x55c21aec9d9c in BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:1025:3  

#21 0x55c21aecac75 in ~BrowserView ./../../chrome/browser/ui/views/frame/browser\_view.cc:985:29  

#22 0x55c21aecac75 in non-virtual thunk to BrowserView::~BrowserView() ./../../chrome/browser/ui/views/frame/browser\_view.cc:0:0  

#23 0x55c20e55f979 in views::View::~View() ./../../ui/views/view.cc:266:9  

#24 0x55c21aeb29c7 in BrowserNonClientFrameViewChromeOS::~BrowserNonClientFrameViewChromeOS() ./../../chrome/browser/ui/views/frame/browser\_non\_client\_frame\_view\_chromeos.cc:142:73  

#25 0x55c20e5c9493 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#26 0x55c20e5c9493 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#27 0x55c20e5c9493 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#28 0x55c20e5c9493 in views::NonClientView::~NonClientView() ./../../ui/views/window/non\_client\_view.cc:169:1  

#29 0x55c20e5c9581 in views::NonClientView::~NonClientView() ./../../ui/views/window/non\_client\_view.cc:165:33  

#30 0x55c20e5616f8 in operator() ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:49:5  

#31 0x55c20e5616f8 in reset ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:281:7  

#32 0x55c20e5616f8 in ~unique\_ptr ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:247:75  

#33 0x55c20e5616f8 in views::View::DoRemoveChildView(views::View\*, bool, bool, views::View\*) ./../../ui/views/view.cc:2738:1  

#34 0x55c20e561924 in views::View::RemoveAllChildViews() ./../../ui/views/view.cc:340:5  

#35 0x55c20e598492 in views::Widget::DestroyRootView() ./../../ui/views/widget/widget.cc:1844:15  

#36 0x55c20e5980b8 in views::Widget::~Widget() ./../../ui/views/widget/widget.cc:208:3  

#37 0x55c21aeaff3b in BrowserFrame::~BrowserFrame() ./../../chrome/browser/ui/views/frame/browser\_frame.cc:80:31  

#38 0x55c20e5ecdc0 in views::NativeWidgetAura::~NativeWidgetAura() ./../../ui/views/widget/native\_widget\_aura.cc:0:0  

#39 0x55c21afc29af in ~BrowserFrameAsh ./../../chrome/browser/ui/views/frame/browser\_frame\_ash.cc:89:38  

#40 0x55c21afc29af in BrowserFrameAsh::~BrowserFrameAsh() ./../../chrome/browser/ui/views/frame/browser\_frame\_ash.cc:89:37  

#41 0x55c20e105b30 in aura::Window::~Window() ./../../ui/aura/window.cc:230:16  

#42 0x55c20e106daf in aura::Window::~Window() ./../../ui/aura/window.cc:185:19  

#43 0x55c208a987fc in Run ./../../base/functional/callback.h:145:12  

#44 0x55c208a987fc in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) ./../../base/task/common/task\_annotator.cc:133:32  

#45 0x55c208addbc7 in RunTask<(lambda at ../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:443:29)> ./../../base/task/common/task\_annotator.h:72:5  

#46 0x55c208addbc7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow\*) ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:441:21  

#47 0x55c208adcced in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:297:30  

#48 0x55c208adee14 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() ./../../base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:0:0

previously allocated by thread T0 (chrome) here:  

#0 0x55c1f8f4325d in operator new(unsigned long) *asan\_rtl*:3  

#1 0x55c20e722e58 in make\_unique<aura::Window, views::NativeViewHostAura::ClippingWindowDelegate \*, aura::client::WindowType> ./../../buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:670:26  

#2 0x55c20e722e58 in views::NativeViewHostAura::CreateClippingWindow() ./../../ui/views/controls/native/native\_view\_host\_aura.cc:306:22  

#3 0x55c20e722b18 in views::NativeViewHostAura::AttachNativeView() ./../../ui/views/controls/native/native\_view\_host\_aura.cc:97:5  

#4 0x55c20e720d93 in views::NativeViewHost::Attach(aura::Window\*) ./../../ui/views/controls/native/native\_view\_host.cc:42:20  

#5 0x55c21b65d559 in views::WebView::AttachWebContentsNativeView() ./../../ui/views/controls/webview/webview.cc:403:12  

#6 0x55c21b65c553 in views::WebView::SetWebContents(content::WebContents\*) ./../../ui/views/controls/webview/webview.cc:107:3  

#7 0x55c21aecdf64 in BrowserView::OnActiveTabChanged(content::WebContents\*, content::WebContents\*, int, int) ./../../chrome/browser/ui/views/frame/browser\_view.cc:1620:25  

#8 0x55c21a1a901d in Browser::OnActiveTabChanged(content::WebContents\*, content::WebContents\*, int, int) ./../../chrome/browser/ui/browser.cc:2460:12  

#9 0x55c21a1a8076 in Browser::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/browser.cc:1204:3  

#10 0x55c21a2b0ad6 in TabStripModel::OnChange(TabStripModelChange const&, TabStripSelectionChange const&) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:413:14  

#11 0x55c21a2afd17 in TabStripModel::InsertWebContentsAtImpl(int, std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, int, absl::optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:1801:3  

#12 0x55c21a2bc614 in TabStripModel::AddWebContents(std::Cr::unique\_ptr<content::WebContents, std::Cr::default\_delete[content::WebContents](javascript:void(0);) >, int, ui::PageTransition, int, absl::optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/tabs/tab\_strip\_model.cc:972:3  

#13 0x55c21a1f042d in Navigate(NavigateParams\*) ./../../chrome/browser/ui/browser\_navigator.cc:827:41  

#14 0x55c21a1f94ab in chrome::AddTabAt(Browser\*, GURL const&, int, bool, absl::optional<tab\_groups::TabGroupId>) ./../../chrome/browser/ui/browser\_tabstrip.cc:43:3  

#15 0x55c21a85a145 in DesksTemplatesAppLaunchHandler::LaunchBrowsers() ./../../chrome/browser/ui/ash/desks/desks\_templates\_app\_launch\_handler.cc:212:9  

#16 0x55c21a8405df in DesksClient::LaunchAppsFromTemplate(std::Cr::unique\_ptr<ash::DeskTemplate, std::Cr::default\_delete[ash::DeskTemplate](javascript:void(0);) >) ./../../chrome/browser/ui/ash/desks/desks\_client.cc:435:12  

#17 0x55c21a839f92 in ChromeDesksTemplatesDelegate::LaunchAppsFromTemplate(std::Cr::unique\_ptr<ash::DeskTemplate, std::Cr::default\_delete[ash::DeskTemplate](javascript:void(0);) >) ./../../chrome/browser/ui/ash/desks/chrome\_desks\_templates\_delegate.cc:415:23  

#18 0x55c20f0944e1 in ash::SavedDeskPresenter::LaunchSavedDeskIntoNewDesk(std::Cr::unique\_ptr<ash::DeskTemplate, std::Cr::default\_delete[ash::DeskTemplate](javascript:void(0);) >, aura::Window\*, ash::Desk const\*) ./../../ash/wm/desks/templates/saved\_desk\_presenter.cc:578:45  

#19 0x55c20f093f2d in ash::SavedDeskPresenter::LaunchSavedDesk(std::Cr::unique\_ptr<ash::DeskTemplate, std::Cr::default\_delete[ash::DeskTemplate](javascript:void(0);) >, aura::Window\*) ./../../ash/wm/desks/templates/saved\_desk\_presenter.cc:421:3  

#20 0x55c20e426000 in base::RepeatingCallback<void (ui::Event const&)>::Run(ui::Event const&) const & ./../../base/functional/callback.h:267:12  

#21 0x55c20e420b5a in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ./../../ui/views/controls/button/button.cc:67:13  

#22 0x55c20e428782 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/controls/button/button\_controller.cc:0:0  

#23 0x55c20e3ef0f5 in ui::ScopedTargetHandler::OnEvent(ui::Event\*) ./../../ui/events/scoped\_target\_handler.cc:28:24  

#24 0x55c20af47667 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12  

#25 0x55c20af46b4c in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:139:5  

#26 0x55c20af46620 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:83:14  

#27 0x55c20af46390 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:55:15  

#28 0x55c20e58fa57 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) ./../../ui/views/widget/root\_view.cc:499:9  

#29 0x55c20e5a4ca6 in views::Widget::OnMouseEvent(ui::MouseEvent\*) ./../../ui/views/widget/widget.cc:1602:20  

#30 0x55c20af47667 in ui::EventDispatcher::DispatchEvent(ui::EventHandler\*, ui::Event\*) ./../../ui/events/event\_dispatcher.cc:190:12

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-1056661/chrome+0x241c93dc) (BuildId: 4d69127b5fe032a2)  

Shadow bytes around the buggy address:  

0x615000907380: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x615000907400: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x615000907480: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x615000907500: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x615000907580: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x615000907600: fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd fd fa  

0x615000907680: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x615000907700: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x615000907780: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x615000907800: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x615000907880: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

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

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 2.1 MB)
- [screen .webm](attachments/screen .webm) (video/webm, 2.2 MB)
- [screen.webm](attachments/screen.webm) (video/webm, 911.9 KB)

## Timeline

### [Deleted User] (2022-10-08)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-10-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-10-08)

I think this change https://chromium-review.googlesource.com/c/chromium/src/+/3902689 has caused this crash.

### lz...@google.com (2022-10-10)

I will let the cl owner to take a look. Thanks!

### lz...@google.com (2022-10-10)

[Empty comment from Monorail migration]

[Monorail components: Internals>Views>Desktop]

### yo...@google.com (2022-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-10)

[Empty comment from Monorail migration]

### ad...@google.com (2022-10-10)

(auto-cc on security bug)

### ch...@gmail.com (2022-10-11)

I think the severity here should be higher than low sev (at latest medium sev) as in https://crbug.com/chromium/1327087 and https://crbug.com/chromium/1317875. 

Also, you can repro this without step-4, just click on "Save desk for later".

### yo...@google.com (2022-10-11)

Hi chromium.khalil@ thanks for flagging! I marked this as because it's a required filed for this bug report. In my two cents, it's low because the DesksTemplates is disabled by default. Most user should only see save for later button and the save for later section in the library page. It seems also requires some corner case steps to trigger the use-after-free bug. In the long run, I think we would like to adjust the overall design. For now we put the desk-template/save-and-recall stuff in overview, which makes the logic way too complex. If we pack everything for saved desk into a standalone container, interface switch/management could be much simpler and less error-prone. However, I'm not very familiar with how security severity is defined, so if you still feel it's a high risk, please go ahead and update the ticket. Thanks for filing this very helpful bug report:)

### yo...@google.com (2022-10-11)

Note: Since we migrated bug tracking system to buganizer, I copy-paste the bulk of the report to b/253089269. I'll be posting progress in buganizer instead.

### [Deleted User] (2022-10-12)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2022-10-14)

I verified the repro steps on 109.0.5360.0  (Revision - 1059220). The bug is fixed.

Thanks for the quick fix!

### ch...@gmail.com (2022-10-18)

Should this be marked as fixed?

### jo...@chromium.org (2022-10-18)

Merges are still happening but this is fixed.

### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-19)

[Empty comment from Monorail migration]

### yo...@google.com (2022-10-21)

[Empty comment from Monorail migration]

### wf...@chromium.org (2022-11-10)

This seems medium to me. Memory corruption in an unsandboxed process, mitigated by gestures.

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-11-11)

Congratulations on another one, Khalil! The VRP Panel has decided to award you $2,000 for this heavily mitigated security bug. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/1372746?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061277)*
