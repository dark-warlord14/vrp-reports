# Security: Heap-use-after-free in media_router::WebContentsDisplayObserverView::OnBrowserSetLastActive

| Field | Value |
|-------|-------|
| **Issue ID** | [40055822](https://issues.chromium.org/issues/40055822) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Cast>UI |
| **Platforms** | Linux, Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | mu...@google.com |
| **Created** | 2021-05-12 |
| **Bounty** | $15,000.00 |

## Description

Chrome Version: 92.0.4504.0 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

1. out/asan/chrome --enable-features=GlobalMediaControlsCastStartStop --user-data-dir=/tmp/xxxx "about:blank" "<http://localhost:8000/poc.html>"
2. In <http://localhost:8000/poc.html> click on the button and wait for "<http://localhost:8000/poc.html>" tab to close
3. On the Zenith dialog try to turn on the live caption

==4662==ERROR: AddressSanitizer: heap-use-after-free on address 0x61e00089ac80 at pc 0x00012379f369 bp 0x7fff5d674050 sp 0x7fff5d674048  

READ of size 8 at 0x61e00089ac80 thread T0  

#0 0x12379f368 in media\_router::WebContentsDisplayObserverView::OnBrowserSetLastActive(Browser\*) web\_contents\_display\_observer\_view.cc:56  

#1 0x122d4d4ff in BrowserList::SetLastActive(Browser\*) browser\_list.cc:319  

#2 0x12363514b in BrowserView::OnWidgetActivationChanged(views::Widget\*, bool) browser\_view.cc:2631  

#3 0x1226695f5 in views::Widget::OnNativeWidgetActivationChanged(bool) widget.cc:1216  

#4 0x1226def3c in views::NativeWidgetMac::OnWindowKeyStatusChanged(bool, bool) native\_widget\_mac.mm:150  

#5 0x11e8ba0de in remote\_cocoa::NativeWidgetNSWindowBridge::OnWindowKeyStatusChangedTo(bool) native\_widget\_ns\_window\_bridge.mm:1008  

#6 0x7fff8fe24fbb in **CFNOTIFICATIONCENTER\_IS\_CALLING\_OUT\_TO\_AN\_OBSERVER**+0xb (CoreFoundation:x86\_64+0x9afbb)  

#7 0x7fff8fe24eba in \_CFXRegistrationPost+0x1aa (CoreFoundation:x86\_64+0x9aeba)  

#8 0x7fff8fe24c21 in \_\_\_CFXNotificationPost\_block\_invoke+0x31 (CoreFoundation:x86\_64+0x9ac21)  

#9 0x7fff8fde31b1 in -[\_CFXNotificationRegistrar find:object:observer:enumerator:]+0x7e1 (CoreFoundation:x86\_64+0x591b1)  

#10 0x7fff8fde219a in \_CFXNotificationPost+0x29a (CoreFoundation:x86\_64+0x5819a)  

#11 0x7fff91826e86 in -[NSNotificationCenter postNotificationName:object:userInfo:]+0x41 (Foundation:x86\_64+0x6e86)  

#12 0x7fff8da339d7 in -[NSWindow becomeKeyWindow]+0x5a4 (AppKit:x86\_64+0x1779d7)  

#13 0x7fff8da333f0 in \_NXSendWindowNotification+0xf7 (AppKit:x86\_64+0x1773f0)  

#14 0x7fff8da32c64 in -[NSWindow \_changeKeyAndMainLimitedOK:]+0x36c (AppKit:x86\_64+0x176c64)  

#15 0x7fff8dabb23c in -[NSWindow \_orderOutAndCalcKeyWithCounter:stillVisible:docWindow:]+0x503 (AppKit:x86\_64+0x1ff23c)  

#16 0x7fff8da35d47 in NSPerformVisuallyAtomicChange+0x92 (AppKit:x86\_64+0x179d47)  

#17 0x7fff8e1a4f01 in -[NSWindow \_doWindowOrderOutWithWithKeyCalc:forCounter:orderingDone:docWindow:]+0xdf (AppKit:x86\_64+0x8e8f01)  

#18 0x7fff8e1a5fd9 in -[NSWindow \_reallyDoOrderWindowOutRelativeTo:findKey:forCounter:force:isModal:]+0x203 (AppKit:x86\_64+0x8e9fd9)  

#19 0x7fff8da3e684 in -[NSWindow \_reallyDoOrderWindow:relativeTo:findKey:forCounter:force:isModal:]+0xab (AppKit:x86\_64+0x182684)  

#20 0x7fff8da3d6cd in -[NSWindow \_doOrderWindow:relativeTo:findKey:forCounter:force:isModal:]+0x410 (AppKit:x86\_64+0x1816cd)  

#21 0x7fff8da3d262 in -[NSWindow orderWindow:relativeTo:]+0x98 (AppKit:x86\_64+0x181262)  

#22 0x11e8acb40 in -[NativeWidgetMacNSWindow orderWindow:relativeTo:] native\_widget\_mac\_nswindow.mm:298  

#23 0x11e8b6222 in remote\_cocoa::NativeWidgetNSWindowBridge::CloseWindow() native\_widget\_ns\_window\_bridge.mm:628  

#24 0x1226634f9 in views::Widget::CloseWithReason(views::Widget::ClosedReason) widget.cc:645  

#25 0x118db248b in \_\_\_ZN2ui12BubbleCloserC2EP8NSWindowN4base17RepeatingCallbackIFvvEEE\_block\_invoke callback.h:169  

#26 0x7fff8da837f9 in \_NSSendEventToObservers+0x173 (AppKit:x86\_64+0x1c77f9)  

#27 0x7fff8e07c23e in -[NSApplication(NSEvent) sendEvent:]+0x36 (AppKit:x86\_64+0x7c023e)  

#28 0x1180f3f54 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:335  

#29 0x116f33fb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xc0aafb9)  

#30 0x1180f32ce in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:319  

#31 0x7fff8d8f73d6 in -[NSApplication run]+0x3e9 (AppKit:x86\_64+0x3b3d6)  

#32 0x116f48baa in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:729  

#33 0x116f44708 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:157  

#34 0x116e59005 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:466  

#35 0x116d9659e in base::RunLoop::Run(base::Location const&) run\_loop.cc:133  

#36 0x10f685718 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:993  

#37 0x10f689c51 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:152  

#38 0x10f67eccc in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#39 0x116b6ba82 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:597  

#40 0x116b6ad24 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:955  

#41 0x116b68036 in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#42 0x116b6864c in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#43 0x10ae90c35 in ChromeMain chrome\_main.cc:151  

#44 0x10258a31f in main chrome\_exe\_main\_mac.cc:114  

#45 0x7fffa5a57234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x61e00089ac80 is located 0 bytes inside of 2600-byte region [0x61e00089ac80,0x61e00089b6a8)  

freed by thread T0 here:  

#0 0x1027870d9 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x450d9)  

#1 0x122f27374 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications\*) memory:1335  

#2 0x122f2ee0c in TabStripModel::InternalCloseTabs(base::span<content::WebContents\* const, 18446744073709551615ul>, unsigned int) tab\_strip\_model.cc:1812  

#3 0x122f2fe00 in TabStripModel::CloseWebContentsAt(int, unsigned int) tab\_strip\_model.cc:759  

#4 0x11084232e in content::WebContentsImpl::Close(content::RenderViewHost\*) web\_contents\_impl.cc:6903  

#5 0x10d8260e3 in blink::mojom::LocalMainFrameHostStubDispatch::Accept(blink::mojom::LocalMainFrameHost\*, mojo::Message\*) frame.mojom.cc:19113  

#6 0x1185a4eb9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:857  

#7 0x1185b2bee in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:48  

#8 0x11a3fbe8c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ipc\_mojo\_bootstrap.cc:949  

#9 0x11a3f4a9c in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:509  

#10 0x116e198f9 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#11 0x116e57da2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:357  

#12 0x116e57587 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:270  

#13 0x116f47138 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:384  

#14 0x116f33fb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xc0aafb9)  

#15 0x116f458e5 in base::MessagePumpCFRunLoopBase::RunWorkSource(void\*) message\_pump\_mac.mm:360  

#16 0x7fff8fe2ee50 in **CFRUNLOOP\_IS\_CALLING\_OUT\_TO\_A\_SOURCE0\_PERFORM\_FUNCTION**+0x10 (CoreFoundation:x86\_64+0xa4e50)  

#17 0x7fff8fe100cb in \_\_CFRunLoopDoSources0+0x22b (CoreFoundation:x86\_64+0x860cb)  

#18 0x7fff8fe0f5b5 in \_\_CFRunLoopRun+0x3a5 (CoreFoundation:x86\_64+0x855b5)  

#19 0x7fff8fe0efb3 in CFRunLoopRunSpecific+0x1a3 (CoreFoundation:x86\_64+0x84fb3)  

#20 0x7fff8f36debb in RunCurrentEventLoopInMode+0xef (HIToolbox:x86\_64+0x30ebb)  

#21 0x7fff8f36dbf8 in ReceiveNextEventCommon+0xb7 (HIToolbox:x86\_64+0x30bf8)  

#22 0x7fff8f36db25 in \_BlockUntilNextEventMatchingListInModeWithFilter+0x46 (HIToolbox:x86\_64+0x30b25)  

#23 0x7fff8d902a03 in \_DPSNextEvent+0x45f (AppKit:x86\_64+0x46a03)  

#24 0x7fff8e07e7ed in -[NSApplication(NSEvent) \_nextEventMatchingEventMask:untilDate:inMode:dequeue:]+0xaeb (AppKit:x86\_64+0x7c27ed)  

#25 0x1180f1552 in \_\_71-[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:]\_block\_invoke chrome\_browser\_application\_mac.mm:237  

#26 0x116f33fb9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xc0aafb9)  

#27 0x1180f10ea in -[BrowserCrApplication nextEventMatchingMask:untilDate:inMode:dequeue:] chrome\_browser\_application\_mac.mm:236  

#28 0x7fff8d8f738a in -[NSApplication run]+0x39d (AppKit:x86\_64+0x3b38a)  

#29 0x116f48baa in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:729

previously allocated by thread T0 here:  

#0 0x102786f90 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x44f90)  

#1 0x116c94647 in operator new(unsigned long) new.cpp:67  

#2 0x1107b4cfb in content::WebContentsImpl::CreateWithOpener(content::WebContents::CreateParams const&, content::RenderFrameHostImpl\*) web\_contents\_impl.cc:1018  

#3 0x122d59279 in Navigate(NavigateParams\*) browser\_navigator.cc:456  

#4 0x12361fa4c in BrowserRootView::OnPerformDrop(ui::DropTargetEvent const&) browser\_root\_view.cc:259  

#5 0x12264e4a2 in views::DropHelper::OnDrop(ui::OSExchangeData const&, gfx::Point const&, int) drop\_helper.cc:102  

#6 0x1226aafdb in views::DragDropClientMac::Drop(id<NSDraggingInfo>) drag\_drop\_client\_mac.mm:107  

#7 0x11e89fdd5 in -[BridgedContentView performDragOperation:] bridged\_content\_view.mm:704  

#8 0x7fff8dba3eb8 in NSCoreDragReceiveMessageProc+0x2ec (AppKit:x86\_64+0x2e7eb8)  

#9 0x7fff8eae0869 in DoMultipartDropMessage+0x147 (HIServices:x86\_64+0xd869)  

#10 0x7fff8eae0573 in DoDropMessage+0x28 (HIServices:x86\_64+0xd573)  

#11 0x7fff8eae0544 in SendDropMessage+0x4f (HIServices:x86\_64+0xd544)  

#12 0x7fff8eadf0ba in DragInApplication+0x206 (HIServices:x86\_64+0xc0ba)  

#13 0x7fff8eade05a in CoreDragStartDragging+0x39c (HIServices:x86\_64+0xb05a)  

#14 0x7fff8dba092b in -[NSCoreDragManager \_dragUntilMouseUp:accepted:]+0x417 (AppKit:x86\_64+0x2e492b)  

#15 0x7fff8db9d8b5 in -[NSCoreDragManager dragImage:fromWindow:at:offset:event:pasteboard:source:slideBack:]+0x4a8 (AppKit:x86\_64+0x2e18b5)  

#16 0x7fff8db9d3fb in -[NSWindow(NSDrag) dragImage:at:offset:event:pasteboard:source:slideBack:]+0x86 (AppKit:x86\_64+0x2e13fb)  

#17 0x1109a8844 in -[WebDragSource startDrag] web\_drag\_source\_mac.mm:199  

#18 0x110a7cc53 in remote\_cocoa::WebContentsNSViewBridge::StartDrag(content::DropData const&, unsigned int, gfx::ImageSkia const&, gfx::Vector2d const&) web\_contents\_ns\_view\_bridge.mm:91  

#19 0x110a68396 in content::WebContentsViewMac::StartDragging(content::DropData const&, blink::DragOperationsMask, gfx::ImageSkia const&, gfx::Vector2d const&, blink::mojom::DragEventSourceInfo const&, content::RenderWidgetHostImpl\*) web\_contents\_view\_mac.mm:163  

#20 0x110439db3 in content::RenderWidgetHostImpl::StartDragging(mojo::StructPtr[blink::mojom::DragData](javascript:void(0);), blink::DragOperationsMask, SkBitmap const&, gfx::Vector2d const&, mojo::StructPtr[blink::mojom::DragEventSourceInfo](javascript:void(0);)) render\_widget\_host\_impl.cc:2788  

#21 0x10da9b1c9 in blink::mojom::FrameWidgetHostStubDispatch::Accept(blink::mojom::FrameWidgetHost\*, mojo::Message\*) widget.mojom.cc:3424  

#22 0x1185a4eb9 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message\*) interface\_endpoint\_client.cc:857  

#23 0x1185b2cd5 in mojo::MessageDispatcher::Accept(mojo::Message\*) message\_dispatcher.cc:43  

#24 0x11a3fbe8c in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ipc\_mojo\_bootstrap.cc:949  

#25 0x11a3f4a9c in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::\*)(mojo::Message), scoped\_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase\*) bind\_internal.h:509  

#26 0x116e198f9 in base::TaskAnnotator::RunTask(char const\*, base::PendingTask\*) callback.h:101  

#27 0x116e57da2 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence\_manager::LazyNow\*) thread\_controller\_with\_message\_pump\_impl.cc:357  

#28 0x116e57587 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread\_controller\_with\_message\_pump\_impl.cc:270  

#29 0x116f47138 in \_\_\_ZN4base24MessagePumpCFRunLoopBase13RunWorkSourceEPv\_block\_invoke message\_pump\_mac.mm:384

SUMMARY: AddressSanitizer: heap-use-after-free web\_contents\_display\_observer\_view.cc:56 in media\_router::WebContentsDisplayObserverView::OnBrowserSetLastActive(Browser\*)  

Shadow bytes around the buggy address:  

0x1c3c00113540: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3c00113550: fd fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa  

0x1c3c00113560: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c3c00113570: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x1c3c00113580: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x1c3c00113590:[fd]fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3c001135a0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3c001135b0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3c001135c0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3c001135d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c3c001135e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd  

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

- [poc.html](attachments/poc.html) (text/plain, 525 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 5.2 MB)

## Timeline

### [Deleted User] (2021-05-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-05-12)

[Comment Deleted]

### ch...@gmail.com (2021-05-12)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-05-12)

I think there is no need to use step-3 to repro this crash, as shown in the video.

### xi...@chromium.org (2021-05-12)

Thanks for the report! It's a browser UaF but requires the flag GlobalMediaControlsCastStartStop to be enabled, so marking as severity high for now. muyaoxu@, could you take a look? Thanks!

[Monorail components: Internals>Cast>UI]

### [Deleted User] (2021-05-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mu...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8f7f373eae000caeafabe17ceee433469b291767

commit 8f7f373eae000caeafabe17ceee433469b291767
Author: Muyao Xu <muyaoxu@google.com>
Date: Mon May 24 17:26:51 2021

[Zenith] Delete dummy notifications after the web page is closed

A dummy notification should be removed from the Zenith dialog when the
web page that's associated with the notification is closed or lost
focus. This matches what Cast dialog is doing.

This CL makes the PresentationRequestNotificationProducer own an
observer to the WebContents, which hides the dummy notification when
the WebContents is destroyed or lost focus.

Bug: b/188594540, 1208264
Change-Id: Ia1c61f501136e1270069fb138db1d5deb00f741c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2906430
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Muyao Xu <muyaoxu@google.com>
Cr-Commit-Position: refs/heads/master@{#885976}

[modify] https://crrev.com/8f7f373eae000caeafabe17ceee433469b291767/chrome/browser/ui/global_media_controls/presentation_request_notification_producer.cc
[modify] https://crrev.com/8f7f373eae000caeafabe17ceee433469b291767/chrome/browser/ui/global_media_controls/presentation_request_notification_producer.h


### mu...@google.com (2021-05-24)

[Empty comment from Monorail migration]

### ad...@google.com (2021-05-25)

muyaoxu@, is this fixed? Please mark it as such before merges will be considered - https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/security-labels.md#TOC-Merge-labels

### [Deleted User] (2021-05-25)

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
Owners: benmason@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-25)

It looks to me like this GlobalMediaControlsCastStartStop flag is disabled by default:
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/media/router/media_router_feature.cc;drc=74689f88041bdfe4c3c8233254d662092acb90e0;l=43

muyaoxu@ could you confirm? That will mean we will not merge this fix back to M91 or M92 unless there's a special reason?

### ad...@google.com (2021-05-25)

Flipping to None on the assumption of https://crbug.com/chromium/1208264#c12 and removing merge requests.

### ta...@chromium.org (2021-05-25)

Reinstating the merge request for M92, we want to (re)start non-stable experiments on that milestone.

### ad...@chromium.org (2021-05-25)

OK cool.

Approving merge to M92, branch 4515.

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-05-26)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/18220bf2128ad7d6c1588ec22492d06c762154b7

commit 18220bf2128ad7d6c1588ec22492d06c762154b7
Author: Muyao Xu <muyaoxu@google.com>
Date: Wed May 26 23:56:47 2021

[Zenith] Delete dummy notifications after the web page is closed

A dummy notification should be removed from the Zenith dialog when the
web page that's associated with the notification is closed or lost
focus. This matches what Cast dialog is doing.

This CL makes the PresentationRequestNotificationProducer own an
observer to the WebContents, which hides the dummy notification when
the WebContents is destroyed or lost focus.

(cherry picked from commit 8f7f373eae000caeafabe17ceee433469b291767)

Bug: b/188594540, 1208264
Change-Id: Ia1c61f501136e1270069fb138db1d5deb00f741c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2906430
Reviewed-by: Takumi Fujimoto <takumif@chromium.org>
Reviewed-by: Tommy Steimel <steimel@chromium.org>
Commit-Queue: Muyao Xu <muyaoxu@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#885976}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2919660
Auto-Submit: Muyao Xu <muyaoxu@google.com>
Commit-Queue: Tommy Steimel <steimel@chromium.org>
Cr-Commit-Position: refs/branch-heads/4515@{#100}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/18220bf2128ad7d6c1588ec22492d06c762154b7/chrome/browser/ui/global_media_controls/presentation_request_notification_producer.cc
[modify] https://crrev.com/18220bf2128ad7d6c1588ec22492d06c762154b7/chrome/browser/ui/global_media_controls/presentation_request_notification_producer.h


### am...@google.com (2021-06-10)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-10)

Congratulations, Khalil! The VRP Panel has decided to award you $15,000 for this report. Nice work!

### am...@google.com (2021-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1208264?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055822)*
