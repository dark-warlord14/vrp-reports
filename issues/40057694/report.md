# Security: Heap-use-after-free in AccessibilityUIMessageHandler::RequestWebContentsTree

| Field | Value |
|-------|-------|
| **Issue ID** | [40057694](https://issues.chromium.org/issues/40057694) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Internals>Accessibility |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tl...@chromium.org |
| **Created** | 2021-10-25 |
| **Bounty** | $7,000.00 |

## Description

Chrome Version: 97.0.4681.0 (Developer Build) (64-bit)  

Operating System: Linux

**REPRODUCTION CASE**

- Enable chrome://flags/#top-chrome-touch-ui

1. launch chrome
2. Go to chrome://accessibility and click on 'Show accessibility tree' button of chrome://tab-strip.top-chrome page

==496693==ERROR: AddressSanitizer: heap-use-after-free on address 0x61f00008b280 at pc 0x561fcf41cc32 bp 0x7fff6f12d970 sp 0x7fff6f12d968  

READ of size 8 at 0x61f00008b280 thread T0 (chrome)  

#0 0x561fcf41cc31 in AccessibilityUIMessageHandler::RequestWebContentsTree(base::ListValue const\*) chrome/browser/accessibility/accessibility\_ui.cc:623:21  

#1 0x561fc61bdfbb in Run base/callback.h:241:12  

#2 0x561fc61bdfbb in content::WebUIImpl::ProcessWebUIMessage(GURL const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, base::ListValue const&) content/browser/webui/web\_ui\_impl.cc:288:38  

#3 0x561fc61b8a6d in content::WebUIImpl::Send(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, base::Value) content/browser/webui/web\_ui\_impl.cc:112:3  

#4 0x561fc31d4dc2 in content::mojom::WebUIHostStubDispatch::Accept(content::mojom::WebUIHost\*, mojo::Message\*) gen/content/common/web\_ui.mojom.cc:156:13  

#5 0x561fd102993a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:900:54  

#6 0x561fd10474f7 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#7 0x561fd102e301 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:657:20  

#8 0x561fd2d2769a in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:984:24  

#9 0x561fd2d1d7ab in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:531:12  

#10 0x561fd2d1d7ab in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:711:12  

#11 0x561fd2d1d7ab in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_1::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind\_internal.h:784:12  

#12 0x561fd2d1d7ab in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:753:12  

#13 0x561fd039a70f in Run base/callback.h:142:12  

#14 0x561fd039a70f in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#15 0x561fd0404e55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:358:23  

#16 0x561fd0403b08 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:261:30  

#17 0x561fd0405c51 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#18 0x561fd025f319 in HandleDispatch base/message\_loop/message\_pump\_glib.cc:375:46  

#19 0x561fd025f319 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:125:43  

#20 0x7f516a6ef17c in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x5217c)

0x61f00008b280 is located 0 bytes inside of 3112-byte region [0x61f00008b280,0x61f00008bea8)  

freed by thread T0 (chrome) here:  

#0 0x561fbe25026d in operator delete(void\*) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:152:3  

#1 0x561fdd912180 in operator() buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:54:5  

#2 0x561fdd912180 in reset buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:315:7  

#3 0x561fdd912180 in views::WebView::SetWebContents(content::WebContents\*) ui/views/controls/webview/webview.cc:105:15  

#4 0x561fdd911d97 in views::WebView::~WebView() ui/views/controls/webview/webview.cc:73:3  

#5 0x561fdd91257d in views::WebView::~WebView() ui/views/controls/webview/webview.cc:71:21  

#6 0x561fdb5b6ece in views::View::~View() ui/views/view.cc:254:9  

#7 0x561fdd8cfa1d in WebUITabStripContainerView::~WebUITabStripContainerView() chrome/browser/ui/views/frame/webui\_tab\_strip\_container\_view.cc:494:59  

#8 0x561fdcc23c7c in BrowserView::MaybeInitializeWebUITabStrip() chrome/browser/ui/views/frame/browser\_view.cc:3354:5  

#9 0x561fc32e5721 in ui::AXPlatformNode::NotifyAddAXModeFlags(ui::AXMode) ui/accessibility/platform/ax\_platform\_node.cc:105:14  

#10 0x561fcf41c367 in AccessibilityUIMessageHandler::RequestWebContentsTree(base::ListValue const\*) chrome/browser/accessibility/accessibility\_ui.cc:612:3  

#11 0x561fc61bdfbb in Run base/callback.h:241:12  

#12 0x561fc61bdfbb in content::WebUIImpl::ProcessWebUIMessage(GURL const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, base::ListValue const&) content/browser/webui/web\_ui\_impl.cc:288:38  

#13 0x561fc61b8a6d in content::WebUIImpl::Send(std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&, base::Value) content/browser/webui/web\_ui\_impl.cc:112:3  

#14 0x561fc31d4dc2 in content::mojom::WebUIHostStubDispatch::Accept(content::mojom::WebUIHost\*, mojo::Message\*) gen/content/common/web\_ui.mojom.cc:156:13  

#15 0x561fd102993a in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:900:54  

#16 0x561fd10474f7 in mojo::MessageDispatcher::Accept(mojo::Message\*) mojo/public/cpp/bindings/lib/message\_dispatcher.cc:43:19  

#17 0x561fd102e301 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message\*) mojo/public/cpp/bindings/lib/interface\_endpoint\_client.cc:657:20  

#18 0x561fd2d2769a in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc\_mojo\_bootstrap.cc:984:24  

#19 0x561fd2d1d7ab in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:531:12  

#20 0x561fd2d1d7ab in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind\_internal.h:711:12  

#21 0x561fd2d1d7ab in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), std::\_\_1::tuple<scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind\_internal.h:784:12  

#22 0x561fd2d1d7ab in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) base/bind\_internal.h:753:12  

#23 0x561fd039a70f in Run base/callback.h:142:12  

#24 0x561fd039a70f in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) base/task/common/task\_annotator.cc:178:33  

#25 0x561fd0404e55 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:358:23  

#26 0x561fd0403b08 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc:261:30  

#27 0x561fd0405c51 in non-virtual thunk to base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence\_manager/thread\_controller\_with\_message\_pump\_impl.cc  

#28 0x561fd025f319 in HandleDispatch base/message\_loop/message\_pump\_glib.cc:375:46  

#29 0x561fd025f319 in base::(anonymous namespace)::WorkSourceDispatch(\_GSource\*, int (\*)(void\*), void\*) base/message\_loop/message\_pump\_glib.cc:125:43  

#30 0x7f516a6ef17c in g\_main\_context\_dispatch (/lib/x86\_64-linux-gnu/libglib-2.0.so.0+0x5217c)

previously allocated by thread T0 (chrome) here:  

#0 0x561fbe24fa0d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third\_party/llvm/compiler-rt/lib/asan/asan\_new\_delete.cpp:95:3  

#1 0x561fc5fa52e8 in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl\*) content/browser/web\_contents/web\_contents\_impl.cc:1077:7  

#2 0x561fdd912bdc in views::WebView::CreateWebContents(content::BrowserContext\*, base::Location) ui/views/controls/webview/webview.cc:445:12  

#3 0x561fdd912871 in views::WebView::GetWebContents(base::Location) ui/views/controls/webview/webview.cc:80:17  

#4 0x561fdd8ce205 in WebUITabStripContainerView::WebUITabStripContainerView(BrowserView\*, views::View\*, views::View\*, views::View\*) chrome/browser/ui/views/frame/webui\_tab\_strip\_container\_view.cc:477:14  

#5 0x561fdcc23f2e in make\_unique<WebUITabStripContainerView, BrowserView \*, views::View \*&, TopContainerView \*&, OmniboxViewViews \*> buildtools/third\_party/libc++/trunk/include/\_\_memory/unique\_ptr.h:725:32  

#6 0x561fdcc23f2e in BrowserView::MaybeInitializeWebUITabStrip() chrome/browser/ui/views/frame/browser\_view.cc:3345:11  

#7 0x561fdcc3161a in BrowserView::AddedToWidget() chrome/browser/ui/views/frame/browser\_view.cc:3238:3  

#8 0x561fdb5e2de2 in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) ui/views/view.cc:2688:5  

#9 0x561fdb5e11ff in views::View::AddChildViewAtImpl(views::View\*, int) ui/views/view.cc:2574:9  

#10 0x561fdb6c698d in views::NonClientView::ViewHierarchyChanged(views::ViewHierarchyChangedDetails const&) ui/views/window/non\_client\_view.cc:310:18  

#11 0x561fdb5e2802 in views::View::ViewHierarchyChangedImpl(views::ViewHierarchyChangedDetails const&) ui/views/view.cc:2705:3  

#12 0x561fdb5e2da6 in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) ui/views/view.cc:2686:3  

#13 0x561fdb5e11ff in views::View::AddChildViewAtImpl(views::View\*, int) ui/views/view.cc:2574:9  

#14 0x561fdb624523 in AddChildView[views::View](javascript:void(0);) ui/views/view.h:423:5  

#15 0x561fdb624523 in views::internal::RootView::SetContentsView(views::View\*) ui/views/widget/root\_view.cc:230:3  

#16 0x561fdb634f0c in views::Widget::Init(views::Widget::InitParams) ui/views/widget/widget.cc:422:17  

#17 0x561fdcc453c2 in BrowserFrame::InitBrowserFrame() chrome/browser/ui/views/frame/browser\_frame.cc:122:3  

#18 0x561fdcde3c13 in BrowserWindow::CreateBrowserWindow(std::\_\_1::unique\_ptr<Browser, std::\_\_1::default\_delete<Browser> >, bool, bool) chrome/browser/ui/views/frame/browser\_window\_factory.cc:54:18  

#19 0x561fdc262adb in CreateBrowserWindow chrome/browser/ui/browser.cc:315:10  

#20 0x561fdc262adb in Browser::Browser(Browser::CreateParams const&) chrome/browser/ui/browser.cc:529:29  

#21 0x561fdc260fc6 in Browser::Create(Browser::CreateParams const&) chrome/browser/ui/browser.cc:449:14  

#22 0x561fdc452d37 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser\*, bool, std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&) chrome/browser/ui/startup/startup\_browser\_creator\_impl.cc:281:15  

#23 0x561fdc4562c4 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) chrome/browser/ui/startup/startup\_browser\_creator\_impl.cc:616:13  

#24 0x561fdc45212f in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool) chrome/browser/ui/startup/startup\_browser\_creator\_impl.cc:425:22  

#25 0x561fdc45157e in StartupBrowserCreatorImpl::Launch(Profile\*, bool, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup\_browser\_creator\_impl.cc:206:32  

#26 0x561fdc446bd3 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile\*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup\_browser\_creator.cc:624:31  

#27 0x561fdc92942d in profiles::FindOrCreateNewWindowForProfile(Profile\*, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, bool) chrome/browser/profiles/profile\_window.cc:136:19  

#28 0x561fdc929bd8 in profiles::OpenBrowserWindowForProfile(base::OnceCallback<void (Profile\*, Profile::CreateStatus)>, bool, bool, bool, Profile\*, Profile::CreateStatus) chrome/browser/profiles/profile\_window.cc:216:3  

#29 0x561fdc92b416 in Invoke<void (\*const &)(base::OnceCallback<void (Profile \*, Profile::CreateStatus)>, bool, bool, bool, Profile \*, Profile::CreateStatus), const base::RepeatingCallback<void (Profile \*, Profile::CreateStatus)> &, const bool &, const bool &, const bool &, Profile \*, Profile::CreateStatus> base/bind\_internal.h:426:12  

#30 0x561fdc92b416 in MakeItSo<void (\*const &)(base::OnceCallback<void (Profile \*, Profile::CreateStatus)>, bool, bool, bool, Profile \*, Profile::CreateStatus), const base::RepeatingCallback<void (Profile \*, Profile::CreateStatus)> &, const bool &, const bool &, const bool &, Profile \*, Profile::CreateStatus> base/bind\_internal.h:711:12  

#31 0x561fdc92b416 in RunImpl<void (\*const &)(base::OnceCallback<void (Profile \*, Profile::CreateStatus)>, bool, bool, bool, Profile \*, Profile::CreateStatus), const std::\_\_1::tuple<base::RepeatingCallback<void (Profile \*, Profile::CreateStatus)>, bool, bool, bool> &, 0UL, 1UL, 2UL, 3UL> base/bind\_internal.h:784:12  

#32 0x561fdc92b416 in base::internal::Invoker<base::internal::BindState<void (\*)(base::OnceCallback<void (Profile\*, Profile::CreateStatus)>, bool, bool, bool, Profile\*, Profile::CreateStatus), base::RepeatingCallback<void (Profile\*, Profile::CreateStatus)>, bool, bool, bool>, void (Profile\*, Profile::CreateStatus)>::Run(base::internal::BindStateBase\*, Profile\*, Profile::CreateStatus) base/bind\_internal.h:766:12  

#33 0x561fcf5bb2ca in Run base/callback.h:241:12  

#34 0x561fcf5bb2ca in RunCallbacks chrome/browser/profiles/profile\_manager.cc:2192:18  

#35 0x561fcf5bb2ca in ProfileManager::OnProfileCreationFinished(Profile\*, Profile::CreateMode, bool, bool) chrome/browser/profiles/profile\_manager.cc:1839:3  

#36 0x561fcf5493c1 in ProfileImpl::DoFinalInit(Profile::CreateMode) chrome/browser/profiles/profile\_impl.cc:803:16  

#37 0x561fcf54fd4e in ProfileImpl::OnLocaleReady(Profile::CreateMode) chrome/browser/profiles/profile\_impl.cc:1108:3

SUMMARY: AddressSanitizer: heap-use-after-free chrome/browser/accessibility/accessibility\_ui.cc:623:21 in AccessibilityUIMessageHandler::RequestWebContentsTree(base::ListValue const\*)  

Shadow bytes around the buggy address:  

0x0c3e80009600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3e80009610: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3e80009620: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c3e80009630: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c3e80009640: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c3e80009650:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3e80009660: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3e80009670: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3e80009680: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3e80009690: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x0c3e800096a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

==496693==ABORTING

## Attachments

- [screen.webm](attachments/screen.webm) (video/webm, 2.8 MB)
- [screen  .webm](attachments/screen  .webm) (video/webm, 743.2 KB)

## Timeline

### [Deleted User] (2021-10-25)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-10-25)

Thanks for the report. I'm going to tentatively mark this as Low severity out of an abundance of caution. If it's only reachable from chrome://accessibility then I think we can consider it a functional rather than security bug, but I'll leave it marked as Low in case it turns out to be exploitable elsewhere.

accessibility owners, PTAL?

[Monorail components: Internals>Accessibility]

### [Deleted User] (2021-10-25)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-26)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ab...@google.com (2021-11-01)

I played around with this and I have a partial understanding of what is going on. The new top chrome feature has a WebUI, Tab List, which comes up in chrome://accessibility. However, it seems like the Tab List web contents does not exist when the "show accessibility tree" button is clicked. There are two slightly different cases which have slightly different results:

1. If I try to get another page's accessibility tree, and then I request the tree for Tab List, there is no crash. We reach the clause [1] in which we attempt to get a render frame host for the provided IDs and it returns nullptr. Although this is a graceful fail, it still shouldn't be happening at all; if a render frame host doesn't exist, ideally we wouldn't list it as an option in the pages.
2. If I load the page and immediately click "Show accessibility tree" for Tab List, I get a seg fault. I placed some log statements through the relevant function and found that the seg fault occurs at this line [2]: web_contents->DumpAccessibilityTree(). I'm confused why doing web_contents->SetAccessibilityMode() a few lines up doesn't cause any issue. How can the pointer to web_contents be fine on that line and fail just a few lines later?

Adding pkasting who I believe is working on this feature. Peter, can you provide any insight on the lifetime of the Tab List web contents?

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/accessibility/accessibility_ui.cc;l=600?q=accessibility_ui%20%22renderer%20no%20longer%20exists%22&ss=chromium
[2] https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/accessibility/accessibility_ui.cc;l=623?q=accessibility_ui%20dumpaccessibilitytree&ss=chromium

### [Deleted User] (2021-11-18)

[Empty comment from Monorail migration]

### ab...@google.com (2021-12-28)

Reassigning to pkasting for visibility. Peter, will you please take a look at my https://crbug.com/chromium/1262902#c5?

### pk...@chromium.org (2021-12-28)

Sorry, I'm not working on this feature.  I'm not sure who is.  tluk@ may know.

### [Deleted User] (2022-01-04)

[Empty comment from Monorail migration]

### tl...@chromium.org (2022-01-07)

Suspecting this is a dup of 1277328, fix landed earlier this morning in https://crrev.com/c/3368621. Will verify once the patch has propagated in tomorrow's canary.

### ch...@gmail.com (2022-01-07)

Fixed on Chromium 99.0.4813.0 (Developer Build) (64-bit).

### ch...@gmail.com (2022-01-07)

[Empty comment from Monorail migration]

### tl...@chromium.org (2022-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-03-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-03-23)

Congratulations on another one, Khalil. The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-03-25)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-13)

Hello -- this issue was resolved by https://ccrev.com/c/3368621 and because this fix links another crbug # and also was landed on an issue labeled as impacting head, our automation was not able to tag this include this issue for inclusion in release notes and CVE processing -- sincere apologies about that! 
The fix for this issue was released in 99/Stable (v 99.0.4844.51). Labeling accordingly so this can be updated accordingly. 

### am...@chromium.org (2022-12-13)

[Empty comment from Monorail migration]

### pg...@google.com (2023-02-12)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### pg...@google.com (2023-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2023-07-28)

This issue was migrated from crbug.com/chromium/1262902?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1277328]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057694)*
