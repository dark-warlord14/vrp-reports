# Security: Segv on unknown address in views::internal::NativeWidgetPrivate::ReparentNativeView

| Field | Value |
|-------|-------|
| **Issue ID** | [40059349](https://issues.chromium.org/issues/40059349) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Mac |
| **Reporter** | ch...@gmail.com |
| **Assignee** | av...@chromium.org |
| **Created** | 2022-04-11 |
| **Bounty** | $3,000.00 |

## Description

**VERSION**  

Chrome Version: 102.0.4996.0 (Official Build) canary (x86\_64)  

Operating System: macOS

**REPRODUCTION CASE**

1. Open index.html
2. Click on "Click here"
3. On poc.html, click on "trigger" then drag the tab and wait for 2 seconds and drop it.
4. On index.html, right-click on the top of tab >> Move Tab to Another Window >> untitled and -1 Other tabs.

This doesn't repro on stable version.

==7526==ERROR: AddressSanitizer: SEGV on unknown address 0x000b0002be80 (pc 0x7fff91cd601d bp 0x7fff5f457c90 sp 0x7fff5f457c78 T0)  

==7526==The signal is caused by a READ memory access.  

#0 0x7fff91cd601d in objc\_msgSend+0x1d (libobjc.A.dylib:x86\_64+0x701d) (BuildId: 4df3c25c52c23f01a3ef0d9d53a73c1c2400000010000000000c0a00000c0a00)  

#1 0x1288d33ee in views::internal::NativeWidgetPrivate::ReparentNativeView(gfx::NativeView, gfx::NativeView) native\_widget\_mac.mm:1093  

#2 0x1287ead3f in views::Widget::ReparentNativeView(gfx::NativeView, gfx::NativeView) widget.cc:283  

#3 0x12adf8996 in constrained\_window::NativeWebContentsModalDialogManagerViews::HostChanged(web\_modal::WebContentsModalDialogHost\*) native\_web\_contents\_modal\_dialog\_manager\_views.cc:188  

#4 0x127667ceb in web\_modal::WebContentsModalDialogManager::SetDelegate(web\_modal::WebContentsModalDialogManagerDelegate\*) web\_contents\_modal\_dialog\_manager.cc:32  

#5 0x1293e07ce in Browser::SetAsDelegate(content::WebContents\*, bool) browser.cc:2766  

#6 0x1293d4430 in Browser::OnTabInsertedAt(content::WebContents\*, int) browser.cc:2298  

#7 0x1293d3a03 in Browser::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser.cc:1155  

#8 0x1295a2a1c in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, absl::optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1896  

#9 0x1295b6609 in TabStripModel::AddWebContents(std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, ui::PageTransition, int, absl::optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1059  

#10 0x12941d521 in chrome::MoveTabsToExistingWindow(Browser\*, Browser\*, std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&) browser\_commands.cc:997  

#11 0x129444132 in chrome::BrowserTabStripModelDelegate::MoveToExistingWindow(std::\_\_1::vector<int, std::\_\_1::allocator<int> > const&, int) browser\_tab\_strip\_model\_delegate.cc:134  

#12 0x1295c7b24 in TabStripModel::ExecuteAddToExistingWindowCommand(int, int) tab\_strip\_model.cc:1640  

#13 0x12a43b7cc in non-virtual thunk to ExistingBaseSubMenuModel::ExecuteCommand(int, int) existing\_base\_sub\_menu\_model.cc:45  

#14 0x11f606bab in -[MenuControllerCocoa itemSelected:] menu\_controller.mm:327  

#15 0x7fff9284b3a6 in \_os\_activity\_initiate\_impl+0x34 (libsystem\_trace.dylib:x86\_64+0x33a6) (BuildId: ac63a7fe50d93a3096e6f6b7ff16e4652400000010000000000c0a00000c0a00)  

#16 0x7fff7ac42720 in -[NSApplication(NSResponder) sendAction:to:from:]+0x1c7 (AppKit:x86\_64+0x7c4720) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#17 0x11d74bcfc in \_\_43-[BrowserCrApplication sendAction:to:from:]\_block\_invoke chrome\_browser\_application\_mac.mm:297  

#18 0x11ea38559 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe621559) (BuildId: 4c4c44c255553144a1332972d7535eeb2400000010000000000b0a0000030c00)  

#19 0x11d74b757 in -[BrowserCrApplication sendAction:to:from:] chrome\_browser\_application\_mac.mm:296  

#20 0x7fff7a715665 in -[NSMenuItem \_corePerformAction]+0x143 (AppKit:x86\_64+0x297665) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#21 0x7fff7a7153d1 in -[NSCarbonMenuImpl performActionWithHighlightingForItemAtIndex:]+0x71 (AppKit:x86\_64+0x2973d1) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#22 0x7fff9284b3a6 in \_os\_activity\_initiate\_impl+0x34 (libsystem\_trace.dylib:x86\_64+0x33a6) (BuildId: ac63a7fe50d93a3096e6f6b7ff16e4652400000010000000000c0a00000c0a00)  

#23 0x7fff7a79e954 in -[NSMenu performActionForItemAtIndex:]+0x78 (AppKit:x86\_64+0x320954) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#24 0x7fff7a79e8cb in -[NSMenu \_internalPerformActionForItemAtIndex:]+0x5d (AppKit:x86\_64+0x3208cb) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#25 0x7fff7a79e6f8 in -[NSCarbonMenuImpl \_carbonCommandProcessEvent:handlerCallRef:]+0x6a (AppKit:x86\_64+0x3206f8) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#26 0x7fff7a65557f in NSSLMMenuEventHandler+0x3d9 (AppKit:x86\_64+0x1d757f) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#27 0x7fff7bf07d84 in DispatchEventToHandlers(EventTargetRec\*, OpaqueEventRef\*, HandlerCallRec\*)+0x6ab (HIToolbox:x86\_64+0x8d84) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#28 0x7fff7bf06ff5 in SendEventToEventTargetInternal(OpaqueEventRef\*, OpaqueEventTargetRef\*, HandlerCallRec\*)+0x1ab (HIToolbox:x86\_64+0x7ff5) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#29 0x7fff7bf1cd13 in SendEventToEventTarget+0x27 (HIToolbox:x86\_64+0x1dd13) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#30 0x7fff7bf693e5 in SendHICommandEvent(unsigned int, HICommand const\*, unsigned int, unsigned int, unsigned char, void const\*, OpaqueEventTargetRef\*, OpaqueEventTargetRef\*, OpaqueEventRef\*\*)+0x19a (HIToolbox:x86\_64+0x6a3e5) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#31 0x7fff7bf949fa in SendMenuCommandWithContextAndModifiers+0x3a (HIToolbox:x86\_64+0x959fa) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#32 0x7fff7bf949a9 in SendMenuItemSelectedEvent+0xbb (HIToolbox:x86\_64+0x959a9) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#33 0x7fff7bf9487c in FinishMenuSelection(SelectionData\*, MenuResult\*, MenuResult\*)+0x5f (HIToolbox:x86\_64+0x9587c) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#34 0x7fff7bf73b6a in PopUpMenuSelectCore(MenuData\*, Point, double, Point, unsigned short, unsigned int, Rect const\*, unsigned short, unsigned int, Rect const\*, Rect const\*, \_\_CFDictionary const\*, \_\_CFString const\*, OpaqueMenuRef\*\*, unsigned short\*)+0x7d6 (HIToolbox:x86\_64+0x74b6a) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#35 0x7fff7bf72bd2 in \_HandlePopUpMenuSelection8(OpaqueMenuRef\*, OpaqueEventRef\*, unsigned int, Point, unsigned short, unsigned int, Rect const\*, unsigned short, Rect const\*, Rect const\*, \_\_CFDictionary const\*, \_\_CFString const\*, OpaqueMenuRef\*\*, unsigned short\*)+0x263 (HIToolbox:x86\_64+0x73bd2) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#36 0x7fff7bf727aa in \_HandlePopUpMenuSelectionWithDictionary+0x11e (HIToolbox:x86\_64+0x737aa) (BuildId: 25e0ac2627fe32e59226f4d42b25ed302400000010000000000c0a00000c0a00)  

#37 0x7fff7a7955a6 in \_NSSLMPopUpCarbonMenu3+0x1849 (AppKit:x86\_64+0x3175a6) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#38 0x7fff7a8a8137 in -[NSCarbonMenuImpl \_popUpContextMenu:withEvent:forView:withFont:]+0xef (AppKit:x86\_64+0x42a137) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#39 0x7fff7a8a7f81 in -[NSMenu \_popUpContextMenu:withEvent:forView:withFont:]+0xc8 (AppKit:x86\_64+0x429f81) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#40 0x128580a0c in views::internal::MenuRunnerImplCocoa::RunMenuAt(views::Widget\*, views::MenuButtonController\*, gfx::Rect const&, views::MenuAnchorPosition, int, gfx::NativeView) menu\_runner\_impl\_cocoa.mm:554  

#41 0x12a450266 in BrowserTabStripController::ShowContextMenuForTab(Tab\*, gfx::Point const&, ui::MenuSourceType) browser\_tab\_strip\_controller.cc:124  

#42 0x12859b20e in views::ContextMenuController::ShowContextMenuForView(views::View\*, gfx::Point const&, ui::MenuSourceType) context\_menu\_controller.cc:29  

#43 0x1287a4367 in views::View::ProcessMousePressed(ui::MouseEvent const&) view.cc:3062  

#44 0x1287a3d09 in views::View::OnMouseEvent(ui::MouseEvent\*) view.cc:1436  

#45 0x120def922 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:190  

#46 0x120def1d2 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:83  

#47 0x1287dd141 in views::internal::RootView::OnMousePressed(ui::MouseEvent const&) root\_view.cc:418  

#48 0x1287fd0a7 in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1544  

#49 0x12889e40c in non-virtual thunk to views::NativeWidgetMacNSWindowHost::OnMouseEvent(std::\_\_1::unique\_ptr<ui::Event, std::\_\_1::default\_delete[ui::Event](javascript:void(0);) >) native\_widget\_mac\_ns\_window\_host.mm:912  

#50 0x12497b3db in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:616  

#51 0x7fff7adbbc0f in -[NSWindow(NSEventRouting) \_reallySendEvent:isDelayedEvent:]+0x1939 (AppKit:x86\_64+0x93dc0f) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#52 0x7fff7adb9f09 in -[NSWindow(NSEventRouting) sendEvent:]+0x21c (AppKit:x86\_64+0x93bf09) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#53 0x124986dd4 in -[NativeWidgetMacNSWindow sendEvent:] native\_widget\_mac\_nswindow.mm:298  

#54 0x7fff7ac3ee7d in -[NSApplication(NSEvent) sendEvent:]+0xc75 (AppKit:x86\_64+0x7c0e7d) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#55 0x11d74dabc in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:344  

#56 0x11ea38559 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xe621559) (BuildId: 4c4c44c255553144a1332972d7535eeb2400000010000000000b0a0000030c00)  

#57 0x11d74cacc in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:321  

#58 0x7fff7a4b93d6 in -[NSApplication run]+0x3e9 (AppKit:x86\_64+0x3b3d6) (BuildId: e39cd61301043e26b424be83ced656f92400000010000000000c0a00000c0a00)  

#59 0x11ea4c95a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:744  

#60 0x11ea48667 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:160  

#61 0x11e962675 in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:498  

#62 0x11e89248c in base::RunLoop::Run(base::Location const&) run\_loop.cc:141  

#63 0x1152c7ff2 in content::BrowserMainLoop::RunMainMessageLoop() browser\_main\_loop.cc:1067  

#64 0x1152cc6c1 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:155  

#65 0x1152c1835 in content::BrowserMain(content::MainFunctionParams) browser\_main.cc:30  

#66 0x11d59f82a in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate\*) content\_main\_runner\_impl.cc:640  

#67 0x11d5a2645 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content\_main\_runner\_impl.cc:1147  

#68 0x11d5a1914 in content::ContentMainRunnerImpl::Run() content\_main\_runner\_impl.cc:1019  

#69 0x11d59e16d in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner\*) content\_main.cc:407  

#70 0x11d59e8dd in content::ContentMain(content::ContentMainParams) content\_main.cc:435  

#71 0x11041baa1 in ChromeMain chrome\_main.cc:176  

#72 0x1007a2b65 in main chrome\_exe\_main\_mac.cc:208  

#73 0x7fff92619234 in start+0x0 (libdyld.dylib:x86\_64+0x5234) (BuildId: 4a0e66c1459638e6898ebd2660478d3d2400000010000000000c0a00000c0a00)

==7526==Register values:  

rax = 0x0000100027336b9b rbx = 0x00007fff5f457d00 rcx = 0x00001c32001416b7 rdx = 0x00000001399c5200  

rdi = 0x000061200015e140 rsi = 0x00007fff7b0e5fd8 rbp = 0x00007fff5f457c90 rsp = 0x00007fff5f457c78  

r8 = 0x0000200000000000 r9 = 0x0000000000000000 r10 = 0x0000000b0002be68 r11 = 0x00007fff7b0e5fd8  

r12 = 0x00007fff5f457ca0 r13 = 0x00001fffebe8af94 r14 = 0x0000100000000000 r15 = 0x0000100000000000  

AddressSanitizer can not provide additional info.  

SUMMARY: AddressSanitizer: SEGV (libobjc.A.dylib:x86\_64+0x701d) (BuildId: 4df3c25c52c23f01a3ef0d9d53a73c1c2400000010000000000c0a00000c0a00) in objc\_msgSend+0x1d  

==7526==ABORTING  

Abort trap: 6

## Attachments

- [index.html](attachments/index.html) (text/plain, 97 B)
- [poc.html](attachments/poc.html) (text/plain, 333 B)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 3.9 MB)

## Timeline

### [Deleted User] (2022-04-11)

[Empty comment from Monorail migration]

### ch...@gmail.com (2022-04-11)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-04-11)

Thanks, I can repro this in M102 but not M101.

avi: git blame says you’ve touched NativeWidgetPrivate::ReparentNativeView(). This could just be a bookkeeping bug in the menu model for the tab context menu, though.

[Monorail components: UI>Browser>TopChrome>TabStrip]

### [Deleted User] (2022-04-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-12)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-04-12)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2022-04-12)

(auto-cc on security bug)

### av...@chromium.org (2022-04-12)

I did touch this, but under the guidance of Chris. I’m not super up to speed on this; if this is super critical timewise we should have Chris look at this.

### rs...@chromium.org (2022-04-12)

Ack. Feel free to reassign as needed. This is Sev-High but it only appears to affect M102.

### av...@chromium.org (2022-04-12)

But that’s weird; nothing has changed in that file in a very very long time.

Rob: Is there anything you can think of that has changed in that time frame?

Alternatively, can we bisect with ASAN?

### rs...@chromium.org (2022-04-12)

bisect-builds.py seems to have a --asan flag, yes. As I noted above, it could be a MenuModel or some other model bookkeeping issue.

### ro...@chromium.org (2022-04-12)

I'm not aware of anything that's changed significantly in Widget parenting during this 4 week time frame.

I would agree that asan bisecting would be useful in attempting to find the culprit. I'm attempting to bisect now, but the asan packages are huge, so it will be slow going.

### ro...@chromium.org (2022-04-12)

Looks like asan isn't correctly working for Mac builds, so I'll have to look at this later. I can get the first build, but the next build fails to launch.

### av...@chromium.org (2022-04-21)

A comment.

What happens is that the window being detached in step 3 goes fullscreen while being dragged. That seems to put it in some weird intermediate state. Then the first window pops a print dialog. That print dialog is supposed to kick the popup out of fullscreen.

In the “good” scenario, you have the detached tab ignore the request to drop out of fullscreen, so it ends stuck in this weird intermediate state of having gone to fullscreen, so there is no window chrome, but isn’t fullscreen, so it’s just a window. That itself is kinda bad.

In the “bad” scenario, you have the detached tab obey the request to drop out of fullscreen, and it just ✨disappears✨ but still really exists in some weird undead state. Therefore, in step 4, it shows up as the “untitled and -1 Other tabs” and to no surprise, trying to do anything with that window explodes.

The thing here is not to fix views::internal::NativeWidgetPrivate::ReparentNativeView. It’s no surprise it explodes. The thing here is to not allow the dragged tab to get into the weird state. Especially not the “bad” weird state where it’s invisible, but probably not allow it to get stuck like it does in the “good” state.

Windows should not be allowed to enter fullscreen while they’re being dragged.

### av...@chromium.org (2022-04-21)

I have a simple fix to not allow windows to enter fullscreen during drag.

For some weird reason this attempt to enter fullscreen will cause the window to close itself after the drag is complete, and this happens on a delay that I don’t have the ability to track down right now. But this should fix the crash as well as not leave the window in a weird state.

### av...@chromium.org (2022-04-22)

Re https://crbug.com/chromium/1315080#c15, the window closing itself is due to the poc.html file having the page ask for itself to be closed. So mystery solved there.

I’m going to send this fix out for review as it fixes the issue for me. Will ask for confirmation.

### gi...@appspot.gserviceaccount.com (2022-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/26594d7762617e3750cf1dd213ccad78fa291cc0

commit 26594d7762617e3750cf1dd213ccad78fa291cc0
Author: Avi Drissman <avi@chromium.org>
Date: Fri Apr 22 15:02:12 2022

Do not allow fullscreening during a drag

Do not allow a page to attempt to enter fullscreen while it is being
actively dragged. Things break.

Fixed: 1315080
Change-Id: Ia175339807284a3e0edddfbf8fb26a4b67fdaf04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3601249
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#995196}

[modify] https://crrev.com/26594d7762617e3750cf1dd213ccad78fa291cc0/chrome/browser/ui/browser.cc


### av...@chromium.org (2022-04-22)

That should do it. OP, can you confirm?

Requesting merge to M102. It’s broken in M101 too but not in a crashy way.

### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-04-23)

Merge approved: your change passed merge requirements and is auto-approved for M102. Please go ahead and merge the CL to branch 5005 (refs/branch-heads/5005) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-04-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b99201686f1e915ac21df8079fd146c96e2c9dca

commit b99201686f1e915ac21df8079fd146c96e2c9dca
Author: Avi Drissman <avi@chromium.org>
Date: Mon Apr 25 20:59:06 2022

Do not allow fullscreening during a drag

Do not allow a page to attempt to enter fullscreen while it is being
actively dragged. Things break.

(cherry picked from commit 26594d7762617e3750cf1dd213ccad78fa291cc0)

Fixed: 1315080
Change-Id: Ia175339807284a3e0edddfbf8fb26a4b67fdaf04
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3601249
Auto-Submit: Avi Drissman <avi@chromium.org>
Reviewed-by: Keren Zhu <kerenzhu@chromium.org>
Commit-Queue: Keren Zhu <kerenzhu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#995196}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3601574
Commit-Queue: Avi Drissman <avi@chromium.org>
Cr-Commit-Position: refs/branch-heads/5005@{#138}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/b99201686f1e915ac21df8079fd146c96e2c9dca/chrome/browser/ui/browser.cc


### am...@google.com (2022-04-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-04-28)

Congratulations, Khalil! The VRP Panel has decided to award you $3,000 for this report since this issue is mitigated by significant user interaction. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2022-05-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1315080?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059349)*
