# Security: Heap-buffer-overflow in TabStripModel::MoveWebContentsAtImpl

| Field | Value |
|-------|-------|
| **Issue ID** | [40055670](https://issues.chromium.org/issues/40055670) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | so...@chromium.org |
| **Created** | 2021-04-26 |
| **Bounty** | $10,000.00 |

## Description

Chrome Version: 92.0.4488.0 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

1. Install the extension.
2. Move the last "New Tab" to the left.

==700==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x606000d116d8 at pc 0x0001217a91ae bp 0x7fff5d3b8100 sp 0x7fff5d3b80f8  

READ of size 8 at 0x606000d116d8 thread T0  

#0 0x1217a91ad in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::\_\_move\_range(std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >\*, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >\*, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >\*) memory:1586  

#1 0x1217a085e in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert(std::\_\_1::\_\_wrap\_iter<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > const\*>, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >&&) vector:1820  

#2 0x121786db2 in TabStripModel::MoveWebContentsAtImpl(int, int, bool) tab\_strip\_model.cc:2022  

#3 0x1217886a9 in TabStripModel::MoveSelectedTabsToImpl(int, unsigned long, unsigned long) tab\_strip\_model.cc:2060  

#4 0x12178806a in TabStripModel::MoveSelectedTabsTo(int) tab\_strip\_model.cc:662  

#5 0x1222e6f8d in TabDragController::MoveAttached(gfx::Point const&, bool) tab\_drag\_controller.cc:1034  

#6 0x1222e40f6 in TabDragController::ContinueDragging(gfx::Point const&) tab\_drag\_controller.cc:847  

#7 0x1222dccc3 in TabDragController::Drag(gfx::Point const&) tab\_drag\_controller.cc:604  

#8 0x122342117 in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) tab\_strip.cc:456  

#9 0x12234f6cb in TabStrip::OnMouseDragged(ui::MouseEvent const&) tab\_strip.cc:3745  

#10 0x120e4085d in views::View::ProcessMouseDragged(ui::MouseEvent\*) view.cc:2996  

#11 0x118ccc83f in ui::EventHandler::OnEvent(ui::Event\*) event\_handler.cc  

#12 0x118ccaca2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:191  

#13 0x118cca550 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:84  

#14 0x120e7aeda in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) root\_view.cc:457  

#15 0x120e965d7 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1347  

#16 0x120ed305c in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:809  

#17 0x11d0b8ebb in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:595  

#18 0x11d0b636d in -[BridgedContentView processCapturedMouseEvent:] bridged\_content\_view.mm:308  

#19 0x11d0c423b in \_\_\_ZN12remote\_cocoa17CocoaMouseCapture14ActiveEventTap4InitEv\_block\_invoke mouse\_capture.mm:91  

#20 0x7fffb0f367f9 in \_NSSendEventToObservers+0x173 (AppKit:x86\_64+0x1c77f9)  

#21 0x7fffb152f23e in -[NSApplication(NSEvent) sendEvent:]+0x36 (AppKit:x86\_64+0x7c023e)  

#22 0x1168c5104 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:335  

#23 0x1156b3569 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbdd9569)  

#24 0x1168c447e in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:319  

#25 0x7fffb0daa3d6 in -[NSApplication run]+0x3e9 (AppKit:x86\_64+0x3b3d6)  

#26 0x1156c7d4a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:717  

#27 0x1156c3938 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:157  

#28 0x1155d640b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:460  

#29 0x11551227e in base::RunLoop::Run(base::Location const&) run\_loop.cc:133  

#30 0x10e014a08 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:990  

#31 0x10e019231 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:150  

#32 0x10e00d66c in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#33 0x1152e50f6 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:598  

#34 0x1152e4394 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:956  

#35 0x1152e1526 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#36 0x1152e1b3c in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#37 0x1098e1005 in ChromeMain chrome\_main.cc:141  

#38 0x1028461ef in main chrome\_exe\_main\_mac.cc:114  

#39 0x7fffc8f0a234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x606000d116d8 is located 8 bytes to the left of 64-byte region [0x606000d116e0,0x606000d11720)  

allocated by thread T0 here:  

#0 0x102a41eb0 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x44eb0)  

#1 0x11540bf97 in operator new(unsigned long) new.cpp:67  

#2 0x1217a0996 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::insert(std::\_\_1::\_\_wrap\_iter<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > const\*>, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >&&) memory:778  

#3 0x12177f6e3 in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1764  

#4 0x12178f961 in TabStripModel::AddWebContents(std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, ui::PageTransition, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1010  

#5 0x1215b2ca7 in Navigate(NavigateParams\*) browser\_navigator.cc:694  

#6 0x1202c819e in extensions::ExtensionTabUtil::OpenTab(ExtensionFunction\*, extensions::ExtensionTabUtil::OpenTabParams const&, bool, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> >\*) extension\_tab\_util.cc:316  

#7 0x12016c9bf in extensions::TabsCreateFunction::Run() tabs\_api.cc:1170  

#8 0x1103a94d7 in ExtensionFunction::RunWithValidation() extension\_function.cc:471  

#9 0x1103b24f5 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>) extension\_function\_dispatcher.cc:384  

#10 0x1103b151c in extensions::ExtensionFunctionDispatcher::Dispatch(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, int) extension\_function\_dispatcher.cc:254  

#11 0x11042a406 in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost\*) extension\_web\_contents\_observer.cc:346  

#12 0x1201fcdb3 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost\*) chrome\_extension\_web\_contents\_observer.cc:101  

#13 0x10f15c4a7 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl\*, IPC::Message const&) web\_contents\_impl.cc:1120  

#14 0x10ec43946 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) render\_frame\_host\_impl.cc:1986  

#15 0x118bc142d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc\_channel\_proxy.cc:325  

#16 0x1155959e3 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#17 0x1155d51da in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:351  

#18 0x1155d49f7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:264  

#19 0x1156c6368 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:384  

#20 0x1156b3569 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbdd9569)  

#21 0x1156c4b15 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:360  

#22 0x7fffb32e1e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#23 0x7fffb32c30cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#24 0x7fffb32c25b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)  

#25 0x7fffb32c1fb3 in CFRunLoopRunSpecific+0x1a3 (CoreFoundation:x86\_64+0x84fb3)  

#26 0x7fffb2820ebb in RunCurrentEventLoopInMode+0xef (HIToolbox:x86\_64+0x30ebb)  

#27 0x7fffb2820cf0 in ReceiveNextEventCommon+0x1af (HIToolbox:x86\_64+0x30cf0)  

#28 0x7fffb2820b25 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x46 (HIToolbox:x86\_64+0x30b25)  

#29 0x7fffb0db5a03 in \_DPSNextEvent+0x45f (AppKit:x86\_64+0x46a03)

SUMMARY: AddressSanitizer: heap-buffer-overflow memory:1586 in std::\_\_1::vector<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >, std::\_\_1::allocator<std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) > > >::\_\_move\_range(std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >\*, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >\*, std::\_\_1::unique\_ptr<TabStripModel::WebContentsData, std::\_\_1::default\_delete[TabStripModel::WebContentsData](javascript:void(0);) >\*)  

Shadow bytes around the buggy address:  

0x1c0c001a2280: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fa  

0x1c0c001a2290: fa fa fa fa fd fd fd fd fd fd fd fd fa fa fa fa  

0x1c0c001a22a0: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd  

0x1c0c001a22b0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd  

0x1c0c001a22c0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

=>0x1c0c001a22d0: 00 00 00 00 00 00 00 00 fa fa fa[fa]00 00 00 00  

0x1c0c001a22e0: 00 00 fc fc fa fa fa fa fd fd fd fd fd fd fd fa  

0x1c0c001a22f0: fa fa fa fa fd fd fd fd fd fd fd fa fa fa fa fa  

0x1c0c001a2300: fd fd fd fd fd fd fd fa fa fa fa fa 00 00 00 00  

0x1c0c001a2310: 00 00 00 fa fa fa fa fa 00 00 00 00 00 00 00 fa  

0x1c0c001a2320: fa fa fa fa 00 00 00 00 00 00 00 fa fa fa fa fa  

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

## Attachments

- [background.js](attachments/background.js) (text/plain, 664 B)
- [manifest.json](attachments/manifest.json) (text/plain, 389 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 2.4 MB)

## Timeline

### [Deleted User] (2021-04-26)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-04-27)

Assigning severity medium since this requires a specific extension to be installed.

kelvingjiang: Can you help further triage this? Thanks.

[Monorail components: Platform>Extensions]

### ca...@chromium.org (2021-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-27)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2021-04-27)

I'll try to get to it today (OOO yesterday). If I can't then I will punt this to someone else.

Was I linked to this because of a specific revision I wrote which could have caused this? (I don't see anything obvious from the stack trace).
And if so, could I get a link to said revision?

### ke...@chromium.org (2021-04-27)

Passing over to Solomon for now, but I'm interested to see the outcome.



### so...@chromium.org (2021-04-29)

The example extension no longer crashes with a recent CL merge. The new behavior if a tab drag is in progress is that there will be no highlight but an error will be sent to chrome.runtime.lastError. crrev.com/c/2860505.

### so...@chromium.org (2021-04-29)

CC for CL review.

### [Deleted User] (2021-05-14)

solomonkinard: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@chromium.org (2021-05-14)

crrev.com/c/2891080

### so...@chromium.org (2021-05-14)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33109f1824b9ae3d488b7372f9aca68f611be606

commit 33109f1824b9ae3d488b7372f9aca68f611be606
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Mon May 17 19:28:43 2021

[Extensions][Tabs] Ensure tab strip is editable before editing

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Ic51669a7f7b17a35cd2c0ed018abcfeddf068a26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2891080
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#883567}

[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tab_groups/tab_groups_api.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tab_groups/tab_groups_api_unittest.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/33109f1824b9ae3d488b7372f9aca68f611be606/chrome/test/base/test_browser_window.h


### so...@chromium.org (2021-05-17)

crrev.com/c/2891080 merged.

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5ae8693fcb042797de12b6b9cc055da0090a80a

commit f5ae8693fcb042797de12b6b9cc055da0090a80a
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed May 19 00:09:39 2021

[M91][Extensions][Tabs] Ensure tab strip is editable before editing

(cherry picked from commit 33109f1824b9ae3d488b7372f9aca68f611be606)

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Ic51669a7f7b17a35cd2c0ed018abcfeddf068a26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2891080
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#883567}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2904568
Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
Cr-Commit-Position: refs/branch-heads/4472@{#1169}
Cr-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}

[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tab_groups/tab_groups_api.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tab_groups/tab_groups_api_unittest.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/f5ae8693fcb042797de12b6b9cc055da0090a80a/chrome/test/base/test_browser_window.h


### gi...@appspot.gserviceaccount.com (2021-05-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7260804a2f0823fdec95e69de0e449bb9fed1f35

commit 7260804a2f0823fdec95e69de0e449bb9fed1f35
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed May 19 19:41:28 2021

[Extensions][Tabs] Include error message if not model isn't editable

See crrev.com/c/2904568.

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Idc6f1a1e336e08926de75226debcff799d703d00
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2903572
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Cr-Commit-Position: refs/heads/master@{#884626}

[modify] https://crrev.com/7260804a2f0823fdec95e69de0e449bb9fed1f35/chrome/browser/extensions/api/tabs/tabs_api.cc


### ad...@google.com (2021-06-03)

carlosil@ you have said Security_Impact-Head here; have you confirmed this doesn't affect Stable? We would like to credit the reporter in the release notes but that only applies if it impacts stable.

### gi...@appspot.gserviceaccount.com (2021-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7aeab825dc9b93ba302d1c124c572213c4967b53

commit 7aeab825dc9b93ba302d1c124c572213c4967b53
Author: Solomon Kinard <solomonkinard@chromium.org>
Date: Wed Jun 09 15:54:57 2021

[M90-LTS][Extensions][Tabs] Ensure tab strip is editable before editing

(cherry picked from commit 33109f1824b9ae3d488b7372f9aca68f611be606)

(cherry picked from commit f5ae8693fcb042797de12b6b9cc055da0090a80a)

Bug: 1198717,1197146,1197888,1196309,1202598
Change-Id: Ic51669a7f7b17a35cd2c0ed018abcfeddf068a26
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2891080
Commit-Queue: Solomon Kinard <solomonkinard@chromium.org>
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Karan Bhatia <karandeepb@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/master@{#883567}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2904568
Auto-Submit: Solomon Kinard <solomonkinard@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4472@{#1169}
Cr-Original-Branched-From: 3d60439cfb36485e76a1c5bb7f513d3721b20da1-refs/heads/master@{#870763}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2944872
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Artem Sumaneev <asumaneev@google.com>
Owners-Override: Artem Sumaneev <asumaneev@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1503}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tab_groups/tab_groups_api.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tab_groups/tab_groups_api_unittest.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_api.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_api_unittest.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_constants.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/api/tabs/tabs_constants.h
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/extension_tab_util.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/browser/extensions/extension_tab_util.h
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/test/base/test_browser_window.cc
[modify] https://crrev.com/7aeab825dc9b93ba302d1c124c572213c4967b53/chrome/test/base/test_browser_window.h


### am...@chromium.org (2021-06-16)

these CLs already merged and released in M91 

### am...@google.com (2021-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-16)

Congratulations, Khalil! The VRP Panel has decided to award you $10,000 for this report. Nice work! 

### am...@google.com (2021-06-18)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-29)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pg...@google.com (2023-07-31)

seems the relnotes label was added by accident here - removing!

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1202598?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055670)*
