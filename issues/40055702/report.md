# Security: Heap-use-after-free in TabStripLayoutHelper::CalculateMinimumWidth

| Field | Value |
|-------|-------|
| **Issue ID** | [40055702](https://issues.chromium.org/issues/40055702) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2021-04-28 |
| **Bounty** | $7,500.00 |

## Description

Chrome Version: 92.0.4490.0 (Official Build) canary (x86\_64) and stable  

Operating System: MacOS

**REPRODUCTION CASE**

1. Install the extension.
2. Click on the first color indicator icon and drag the tab out of the tab strip.
3. Then drag it back to the tab strip.

==1071==ERROR: AddressSanitizer: heap-use-after-free on address 0x61800020bf30 at pc 0x00012d24ed7d bp 0x7fff55a85190 sp 0x7fff55a85188  

READ of size 1 at 0x61800020bf30 thread T0  

#0 0x12d24ed7c in TabStripLayoutHelper::CalculateIdealBounds(base::Optional<int>) optional.h:165  

#1 0x12d250e2a in TabStripLayoutHelper::CalculateMinimumWidth() tab\_strip\_layout\_helper.cc:229  

#2 0x12d22c136 in TabStrip::GetMinimumSize() const tab\_strip.cc:2474  

#3 0x12bc8dd34 in views::(anonymous namespace)::GetPreferredSize(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, views::View const\*, views::SizeBounds const&) flex\_layout\_types.cc:85  

#4 0x12bc8f240 in base::internal::Invoker<base::internal::BindState<gfx::Size (\*)(views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool, views::View const\*, views::SizeBounds const&), views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, views::MinimumFlexSizeRule, views::MaximumFlexSizeRule, bool>, gfx::Size (views::View const\*, views::SizeBounds const&)>::Run(base::internal::BindStateBase\*, views::View const\*, views::SizeBounds const&) bind\_internal.h:404  

#5 0x12bc84780 in views::FlexLayout::GetPreferredSizeForRule(base::RepeatingCallback<gfx::Size (views::View const\*, views::SizeBounds const&)> const&, views::View const\*, views::SizeBound const&) const callback.h:169  

#6 0x12bc7eb6e in views::FlexLayout::InitializeChildData(views::NormalizedSizeBounds const&, views::FlexLayout::FlexLayoutData&, std::\_\_1::map<int, std::\_\_1::list<unsigned long, std::\_\_1::allocator<unsigned long> >, std::\_\_1::less<int>, std::\_\_1::allocator<std::\_\_1::pair<int const, std::\_\_1::list<unsigned long, std::\_\_1::allocator<unsigned long> > > > >&) const flex\_layout.cc:545  

#7 0x12bc7d0ef in views::FlexLayout::CalculateProposedLayout(views::SizeBounds const&) const flex\_layout.cc:418  

#8 0x12bcb2d42 in views::LayoutManagerBase::GetAvailableSize(views::View const\*, views::View const\*) const layout\_manager\_base.cc:103  

#9 0x12bd15456 in views::View::GetAvailableSize(views::View const\*) const view.cc:536  

#10 0x12cdb0315 in TabStripRegionView::GetTabStripAvailableWidth() const tab\_strip\_region\_view.cc:381  

#11 0x12d21c8dc in TabStrip::OnGroupVisualsChanged(tab\_groups::TabGroupId const&, tab\_groups::TabGroupVisualData const\*, tab\_groups::TabGroupVisualData const\*) callback.h:169  

#12 0x12d1809b9 in BrowserTabStripController::OnTabGroupChanged(TabGroupChange const&) browser\_tab\_strip\_controller.cc:730  

#13 0x12c67c40f in TabStripModel::ChangeTabGroupVisuals(tab\_groups::TabGroupId const&, TabGroupChange::VisualsChange const&) tab\_strip\_model.cc:1219  

#14 0x12c6566d3 in TabGroup::AddTab() tab\_group.cc:68  

#15 0x12c679299 in TabStripModel::GroupTab(int, tab\_groups::TabGroupId const&) tab\_strip\_model.cc:2257  

#16 0x12c663f2c in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1782  

#17 0x12c66312e in TabStripModel::InsertWebContentsAt(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:388  

#18 0x12d1c2603 in TabDragController::Attach(TabDragContext\*, gfx::Point const&, bool) tab\_drag\_controller.cc:1222  

#19 0x12d1c77e2 in TabDragController::RunMoveLoop(gfx::Vector2d const&) tab\_drag\_controller.cc:1447  

#20 0x12d1cc239 in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) tab\_drag\_controller.cc:1390  

#21 0x12d1c9e5f in TabDragController::DragBrowserToNewTabStrip(TabDragContext\*, gfx::Point const&) tab\_drag\_controller.cc:865  

#22 0x12d1c7eeb in TabDragController::ContinueDragging(gfx::Point const&) tab\_drag\_controller.cc:831  

#23 0x12d1c0cc3 in TabDragController::Drag(gfx::Point const&) tab\_drag\_controller.cc:604  

#24 0x12d226117 in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) tab\_strip.cc:456  

#25 0x12d2336cb in TabStrip::OnMouseDragged(ui::MouseEvent const&) tab\_strip.cc:3745  

#26 0x12bd2485d in views::View::ProcessMouseDragged(ui::MouseEvent\*) view.cc:2996  

#27 0x123bb083f in ui::EventHandler::OnEvent(ui::Event\*) event\_handler.cc  

#28 0x123baeca2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:191  

#29 0x123bae550 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:84  

#30 0x12bd5eeda in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) root\_view.cc:457  

#31 0x12bd7a5d7 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1347  

#32 0x12bdb705c in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:809  

#33 0x127f9cebb in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:595  

#34 0x127f9a36d in -[BridgedContentView processCapturedMouseEvent:] bridged\_content\_view.mm:308  

#35 0x127fa823b in \_\_\_ZN12remote\_cocoa17CocoaMouseCapture14ActiveEventTap4InitEv\_block\_invoke mouse\_capture.mm:91  

#36 0x7fff958d87f9 in \_NSSendEventToObservers+0x173 (AppKit:x86\_64+0x1c77f9)  

#37 0x7fff95ed123e in -[NSApplication(NSEvent) sendEvent:]+0x36 (AppKit:x86\_64+0x7c023e)  

#38 0x1217a9104 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:335  

#39 0x120597569 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbdd9569)  

#40 0x1217a847e in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:319  

#41 0x7fff9574c3d6 in -[NSApplication run]+0x3e9 (AppKit:x86\_64+0x3b3d6)  

#42 0x1205abd4a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:717  

#43 0x1205a7938 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:157  

#44 0x1204ba40b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:460  

#45 0x1203f627e in base::RunLoop::Run(base::Location const&) run\_loop.cc:133  

#46 0x118ef8a08 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:990  

#47 0x118efd231 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:150  

#48 0x118ef166c in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#49 0x1201c90f6 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:598  

#50 0x1201c8394 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:956  

#51 0x1201c5526 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#52 0x1201c5b3c in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#53 0x1147c5005 in ChromeMain chrome\_main.cc:141  

#54 0x10a1771ef in main chrome\_exe\_main\_mac.cc:114  

#55 0x7fffad8ac234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x61800020bf30 is located 688 bytes inside of 840-byte region [0x61800020bc80,0x61800020bfc8)  

freed by thread T0 here:  

#0 0x10a373ff9 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x44ff9)  

#1 0x12d1f1dbb in TabGroupViews::~TabGroupViews() memory:1335  

#2 0x12d21bb64 in TabStrip::OnGroupCreated(tab\_groups::TabGroupId const&) memory:1596  

#3 0x12d180508 in BrowserTabStripController::OnTabGroupChanged(TabGroupChange const&) browser\_tab\_strip\_controller.cc:689  

#4 0x12c67ac6c in TabStripModel::CreateTabGroup(tab\_groups::TabGroupId const&) tab\_strip\_model.cc:1198  

#5 0x12c65664a in TabGroup::AddTab() tab\_group.cc:65  

#6 0x12c679299 in TabStripModel::GroupTab(int, tab\_groups::TabGroupId const&) tab\_strip\_model.cc:2257  

#7 0x12c663f2c in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1782  

#8 0x12c66312e in TabStripModel::InsertWebContentsAt(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:388  

#9 0x12d1c2603 in TabDragController::Attach(TabDragContext\*, gfx::Point const&, bool) tab\_drag\_controller.cc:1222  

#10 0x12d1c77e2 in TabDragController::RunMoveLoop(gfx::Vector2d const&) tab\_drag\_controller.cc:1447  

#11 0x12d1cc239 in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) tab\_drag\_controller.cc:1390  

#12 0x12d1c9e5f in TabDragController::DragBrowserToNewTabStrip(TabDragContext\*, gfx::Point const&) tab\_drag\_controller.cc:865  

#13 0x12d1c7eeb in TabDragController::ContinueDragging(gfx::Point const&) tab\_drag\_controller.cc:831  

#14 0x12d1c0cc3 in TabDragController::Drag(gfx::Point const&) tab\_drag\_controller.cc:604  

#15 0x12d226117 in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) tab\_strip.cc:456  

#16 0x12d2336cb in TabStrip::OnMouseDragged(ui::MouseEvent const&) tab\_strip.cc:3745  

#17 0x12bd2485d in views::View::ProcessMouseDragged(ui::MouseEvent\*) view.cc:2996  

#18 0x123bb083f in ui::EventHandler::OnEvent(ui::Event\*) event\_handler.cc  

#19 0x123baeca2 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:191  

#20 0x123bae550 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:84  

#21 0x12bd5eeda in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) root\_view.cc:457  

#22 0x12bd7a5d7 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1347  

#23 0x12bdb705c in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:809  

#24 0x127f9cebb in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:595  

#25 0x127f9a36d in -[BridgedContentView processCapturedMouseEvent:] bridged\_content\_view.mm:308  

#26 0x127fa823b in \_\_\_ZN12remote\_cocoa17CocoaMouseCapture14ActiveEventTap4InitEv\_block\_invoke mouse\_capture.mm:91  

#27 0x7fff958d87f9 in \_NSSendEventToObservers+0x173 (AppKit:x86\_64+0x1c77f9)  

#28 0x7fff95ed123e in -[NSApplication(NSEvent) sendEvent:]+0x36 (AppKit:x86\_64+0x7c023e)  

#29 0x1217a9104 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:335

previously allocated by thread T0 here:  

#0 0x10a373eb0 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x44eb0)  

#1 0x1202eff97 in operator new(unsigned long) new.cpp:67  

#2 0x12d1f1aac in TabGroupViews::TabGroupViews(TabStrip\*, tab\_groups::TabGroupId const&) memory:2006  

#3 0x12d21ba52 in TabStrip::OnGroupCreated(tab\_groups::TabGroupId const&) tab\_strip.cc:1487  

#4 0x12d180508 in BrowserTabStripController::OnTabGroupChanged(TabGroupChange const&) browser\_tab\_strip\_controller.cc:689  

#5 0x12c67ac6c in TabStripModel::CreateTabGroup(tab\_groups::TabGroupId const&) tab\_strip\_model.cc:1198  

#6 0x12c65664a in TabGroup::AddTab() tab\_group.cc:65  

#7 0x12c679299 in TabStripModel::GroupTab(int, tab\_groups::TabGroupId const&) tab\_strip\_model.cc:2257  

#8 0x12c686b96 in TabStripModel::MoveAndSetGroup(int, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:2198  

#9 0x12c676b2c in TabStripModel::MoveTabsAndSetGroupImpl(std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:2167  

#10 0x12c675b69 in TabStripModel::AddToNewGroupImpl(std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&, tab\_groups::TabGroupId const&) tab\_strip\_model.cc:2114  

#11 0x12c675595 in TabStripModel::AddToNewGroup(std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&) tab\_strip\_model.cc:1085  

#12 0x12b05a4eb in extensions::TabsGroupFunction::Run() tabs\_api.cc:1844  

#13 0x11b28d4d7 in ExtensionFunction::RunWithValidation() extension\_function.cc:471  

#14 0x11b2964f5 in extensions::ExtensionFunctionDispatcher::DispatchWithCallbackInternal(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, int, base::OnceCallback<void (ExtensionFunction::ResponseType, base::ListValue const&, std::\_\_1::basic\_string<char, std::\_\_1::char\_traits<char>, std::\_\_1::allocator<char> > const&)>) extension\_function\_dispatcher.cc:384  

#15 0x11b29551c in extensions::ExtensionFunctionDispatcher::Dispatch(extensions::mojom::RequestParams const&, content::RenderFrameHost\*, int) extension\_function\_dispatcher.cc:254  

#16 0x11b30e406 in extensions::ExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost\*) extension\_web\_contents\_observer.cc:346  

#17 0x12b0e0db3 in extensions::ChromeExtensionWebContentsObserver::OnMessageReceived(IPC::Message const&, content::RenderFrameHost\*) chrome\_extension\_web\_contents\_observer.cc:101  

#18 0x11a0404a7 in content::WebContentsImpl::OnMessageReceived(content::RenderFrameHostImpl\*, IPC::Message const&) web\_contents\_impl.cc:1120  

#19 0x119b27946 in content::RenderFrameHostImpl::OnMessageReceived(IPC::Message const&) render\_frame\_host\_impl.cc:1986  

#20 0x123aa542d in IPC::ChannelProxy::Context::OnDispatchMessage(IPC::Message const&) ipc\_channel\_proxy.cc:325  

#21 0x1204799e3 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#22 0x1204b91da in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:351  

#23 0x1204b89f7 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:264  

#24 0x1205aa368 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:384  

#25 0x120597569 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xbdd9569)  

#26 0x1205a8b15 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:360  

#27 0x7fff97c83e50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#28 0x7fff97c650cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#29 0x7fff97c645b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)

SUMMARY: AddressSanitizer: heap-use-after-free optional.h:165 in TabStripLayoutHelper::CalculateIdealBounds(base::Optional<int>)  

Shadow bytes around the buggy address:  

0x1c3000041790: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c30000417a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c30000417b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c30000417c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c30000417d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

=>0x1c30000417e0: fd fd fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd  

0x1c30000417f0: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa  

0x1c3000041800: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c3000041810: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3000041820: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3000041830: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

- [screen .mov](attachments/screen .mov) (video/quicktime, 6.4 MB)
- [poc.zip](attachments/poc.zip) (application/octet-stream, 6.6 KB)
- [background.js](attachments/background.js) (text/plain, 42 B)
- [manifest.json](attachments/manifest.json) (text/plain, 194 B)
- [poc.html](attachments/poc.html) (text/plain, 43 B)
- [poc.js](attachments/poc.js) (text/plain, 617 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 7.1 MB)
- [log.asan](attachments/log.asan) (text/plain, 28.0 KB)

## Timeline

### [Deleted User] (2021-04-28)

[Empty comment from Monorail migration]

### aj...@google.com (2021-04-28)

Hi tab strip people - could you suggest someone to take a look at this use-after-free.

Setting severity=medium as significant user interaction is required.

[Monorail components: UI>Browser>TabStrip]

### aj...@google.com (2021-04-28)

I have so far not been able to repro on Windows.

### [Deleted User] (2021-04-29)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-29)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@gmail.com (2021-04-30)

There is another easy way to repro this bug.

- Click on the first color indicator icon and move the tab to the right and drag it out of the tab strip then drag it back to the tab strip.



### aj...@google.com (2021-04-30)

Thanks - I have been able to repro on linux by changing the timeout in poc.js to 9s, waiting for the first splurge of tabs, then draging a tab left and right then in and out of the tab strip.

This is definitely on the very edge of what I would consider a security bug due to the complexity of the repro - let us know if you can repro entirely using a scripted approach.

Assigning to tbergquist based on history in browser_tab_strip_controller.cc - please reassign to someone else if they are better placed to investigate and address this security issue.

### [Deleted User] (2021-05-12)

tbergquist: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2021-05-12)

This one will be fixed by https://chromium-review.googlesource.com/c/chromium/src/+/2891080

### ch...@gmail.com (2021-05-13)

Great! so I will verify this bug once the fix is landed.

### so...@chromium.org (2021-05-17)

crrev.com/c/2891080 merged.

### ch...@gmail.com (2021-05-17)

Fixed on Chromium 92.0.4511.0 (Developer Build) (x86_64) refs/heads/master@{#883573}.

### ch...@gmail.com (2021-05-21)

Fixed?

### tb...@chromium.org (2021-05-21)

Yes! Fixed, sorry! Thanks for verifying.

### [Deleted User] (2021-05-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-22)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M91. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to future beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M92. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-22)

This bug requires manual review: We are only 2 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-23)

Your change meets the bar and is auto-approved for M92. Please go ahead and merge the CL to branch 4515 (refs/branch-heads/4515) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: govind@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-05-27)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-06-03)

Rejecting merge to M91 because the fix is textually quite big (even if it's relatively simple) and as a medium severity security bug, it doesn't justify accepting any stability risk for M91. Better to release in M92... but tbergquist@ please go ahead and merge to M92.

### ad...@google.com (2021-06-03)

In fact, this was already merged to M91 so adjusting labels appropriately.

### as...@google.com (2021-06-04)

Marking as not applicable for LTS-86. There already was an attempt to merge the fix:
https://chromium-review.googlesource.com/c/chromium/src/+/2919770

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-07)

rel notes updated 

### am...@google.com (2021-06-07)

[Empty comment from Monorail migration]

### as...@google.com (2021-06-08)

[Empty comment from Monorail migration]

### gi...@google.com (2021-06-09)

[Empty comment from Monorail migration]

### am...@google.com (2021-06-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-16)

Congratulations, Khalil - another one! The VRP Panel has decided to award you $7,500 fro this report. Another good one! 

### am...@google.com (2021-06-18)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-23)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1203607?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055702)*
