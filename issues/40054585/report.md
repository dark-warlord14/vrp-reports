# Security: container-overflow in TabStrip::SetSelection

| Field | Value |
|-------|-------|
| **Issue ID** | [40054585](https://issues.chromium.org/issues/40054585) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2021-01-27 |
| **Bounty** | $10,000.00 |

## Description

**VERSION**  

Chrome Version: 90.0.4399.0 (Official Build) canary (x86\_64)  

Operating System: MacOS

**REPRODUCTION CASE**

Similar to <https://crbug.com/chromium/1138911>

1. Run chrome with "about:blank" "<http://localhost:8000/poc.html>" "about:blank"
2. In the second tab click on the button then to drag the third tab "about:blank" out of the current tab strip slowly >> crash

==5135==ERROR: AddressSanitizer: container-overflow on address 0x60800020d438 at pc 0x000123203fb9 bp 0x7fff5a5c91f0 sp 0x7fff5a5c91e8  

READ of size 8 at 0x60800020d438 thread T0  

#0 0x123203fb8 in TabStrip::SetSelection(ui::ListSelectionModel const&) view\_model.h:81  

#1 0x123166f4a in BrowserTabStripController::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser\_tab\_strip\_controller.cc:689  

#2 0x122673a0b in TabStripModel::SetSelection(ui::ListSelectionModel, TabStripModelObserver::ChangeReason, bool) tab\_strip\_model.cc:1884  

#3 0x12267ba92 in TabStripModel::SetSelectionFromModel(ui::ListSelectionModel) tab\_strip\_model.cc:915  

#4 0x1231ba9b2 in TabDragController::RestoreInitialSelection() tab\_drag\_controller.cc:1673  

#5 0x1231b641c in TabDragController::Detach(TabDragController::ReleaseCapture) tab\_drag\_controller.cc:1322  

#6 0x1231b530d in TabDragController::DetachIntoNewBrowserAndRunMoveLoop(gfx::Point const&) tab\_drag\_controller.cc:1373  

#7 0x1231b30bf in TabDragController::DragBrowserToNewTabStrip(TabDragContext\*, gfx::Point const&) tab\_drag\_controller.cc:865  

#8 0x1231b03f4 in TabDragController::ContinueDragging(gfx::Point const&) tab\_drag\_controller.cc:831  

#9 0x1231a908a in TabDragController::Drag(gfx::Point const&) tab\_drag\_controller.cc:604  

#10 0x123209f97 in TabStrip::TabDragContextImpl::ContinueDrag(views::View\*, ui::LocatedEvent const&) tab\_strip.cc:462  

#11 0x12321690b in TabStrip::OnMouseDragged(ui::MouseEvent const&) tab\_strip.cc:3654  

#12 0x12212480d in views::View::ProcessMouseDragged(ui::MouseEvent\*) view.cc:2976  

#13 0x119ba5e8f in ui::EventHandler::OnEvent(ui::Event\*) event\_handler.cc  

#14 0x119ba4279 in ui::EventDispatcher::ProcessEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:191  

#15 0x119ba3a54 in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:84  

#16 0x119ba3780 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget\*, ui::Event\*) event\_dispatcher.cc:56  

#17 0x1221576fa in views::internal::RootView::OnMouseDragged(ui::MouseEvent const&) root\_view.cc:452  

#18 0x12217296a in views::Widget::OnMouseEvent(ui::MouseEvent\*) widget.cc:1326  

#19 0x11e056b3c in -[BridgedContentView mouseEvent:] bridged\_content\_view.mm:586  

#20 0x11e053dd7 in -[BridgedContentView processCapturedMouseEvent:] bridged\_content\_view.mm:308  

#21 0x11e06242b in \_\_\_ZN12remote\_cocoa17CocoaMouseCapture14ActiveEventTap4InitEv\_block\_invoke mouse\_capture.mm:91  

#22 0x7fff95ecb7f9 in \_NSSendEventToObservers+0x173 (AppKit:x86\_64+0x1c77f9)  

#23 0x7fff964c423e in -[NSApplication(NSEvent) sendEvent:]+0x36 (AppKit:x86\_64+0x7c023e)  

#24 0x117751474 in \_\_34-[BrowserCrApplication sendEvent:]\_block\_invoke chrome\_browser\_application\_mac.mm:327  

#25 0x11653e1b9 in base::mac::CallWithEHFrame(void () block\_pointer)+0x9 (Chromium Framework:x86\_64+0xb4221b9)  

#26 0x1177504c6 in -[BrowserCrApplication sendEvent:] chrome\_browser\_application\_mac.mm:311  

#27 0x7fff95d3f3d6 in -[NSApplication run]+0x3e9 (AppKit:x86\_64+0x3b3d6)  

#28 0x1165525da in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate\*) message\_pump\_mac.mm:691  

#29 0x11654e1b8 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate\*) message\_pump\_mac.mm:149  

#30 0x11646281b in base::sequence\_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread\_controller\_with\_message\_pump\_impl.cc:460  

#31 0x1163a888b in base::RunLoop::Run() run\_loop.cc:131  

#32 0x116a74261 in ChromeBrowserMainParts::MainMessageLoopRun(int\*) chrome\_browser\_main.cc:1736  

#33 0x10f94bef9 in content::BrowserMainLoop::RunMainMessageLoopParts() browser\_main\_loop.cc:970  

#34 0x10f9514c1 in content::BrowserMainRunnerImpl::Run() browser\_main\_runner\_impl.cc:150  

#35 0x10f94376c in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:47  

#36 0x116185175 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:555  

#37 0x1161844c3 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:926  

#38 0x11618125b in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#39 0x11618191c in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398  

#40 0x10b121a35 in ChromeMain chrome\_main.cc:141  

#41 0x105633eff in main chrome\_exe\_main\_mac.cc:114  

#42 0x7fffade9f234 in start+0x0 (libdyld.dylib:x86\_64+0x5234)

0x60800020d438 is located 24 bytes inside of 96-byte region [0x60800020d420,0x60800020d480)  

allocated by thread T0 here:  

#0 0x105818d30 (libclang\_rt.asan\_osx\_dynamic.dylib:x86\_64+0x45d30)  

#1 0x1162a6387 in operator new(unsigned long) new.cpp:67  

#2 0x12214b6f6 in std::\_\_1::vector<views::ViewModelBase::Entry, std::\_\_1::allocator[views::ViewModelBase::Entry](javascript:void(0);) >::insert(std::\_\_1::\_\_wrap\_iter<views::ViewModelBase::Entry const\*>, views::ViewModelBase::Entry const&) \_\_split\_buffer:318  

#3 0x12214c032 in views::ViewModelBase::AddUnsafe(views::View\*, int) view\_model.cc:74  

#4 0x1231f8c82 in TabStrip::AddTabAt(int, TabRendererData, bool) tab\_strip.cc:1271  

#5 0x123161e4d in BrowserTabStripController::AddTab(content::WebContents\*, int, bool) browser\_tab\_strip\_controller.cc:775  

#6 0x123166a40 in BrowserTabStripController::OnTabStripModelChanged(TabStripModel\*, TabStripModelChange const&, TabStripSelectionChange const&) browser\_tab\_strip\_controller.cc:639  

#7 0x12266e30e in TabStripModel::InsertWebContentsAtImpl(int, std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:1726  

#8 0x12267c317 in TabStripModel::AddWebContents(std::\_\_1::unique\_ptr<content::WebContents, std::\_\_1::default\_delete[content::WebContents](javascript:void(0);) >, int, ui::PageTransition, int, base::Optional<tab\_groups::TabGroupId>) tab\_strip\_model.cc:986  

#9 0x1224bb48a in Navigate(NavigateParams\*) browser\_navigator.cc:715  

#10 0x122636642 in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser\*, bool, std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&) startup\_browser\_creator\_impl.cc:273  

#11 0x122638ddf in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::\_\_1::vector<StartupTab, std::\_\_1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) startup\_browser\_creator\_impl.cc:519  

#12 0x122635682 in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool, std::\_\_1::vector<GURL, std::\_\_1::allocator<GURL> > const&) startup\_browser\_creator\_impl.cc:383  

#13 0x122634c6a in StartupBrowserCreatorImpl::Launch(Profile\*, std::\_\_1::vector<GURL, std::\_\_1::allocator<GURL> > const&, bool, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) startup\_browser\_creator\_impl.cc:186  

#14 0x122628448 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile\*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::\_\_1::unique\_ptr<LaunchModeRecorder, std::\_\_1::default\_delete<LaunchModeRecorder> >) startup\_browser\_creator.cc:523  

#15 0x1226304cc in StartupBrowserCreator::ProcessLastOpenedProfiles(base::CommandLine const&, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:1034  

#16 0x12262fc7a in StartupBrowserCreator::LaunchBrowserForLastProfiles(base::CommandLine const&, base::FilePath const&, bool, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:984  

#17 0x1226278f5 in StartupBrowserCreator::ProcessCmdLineImpl(base::CommandLine const&, base::FilePath const&, bool, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:922  

#18 0x122625b27 in StartupBrowserCreator::Start(base::CommandLine const&, base::FilePath const&, Profile\*, std::\_\_1::vector<Profile\*, std::\_\_1::allocator<Profile\*> > const&) startup\_browser\_creator.cc:475  

#19 0x116a71b98 in ChromeBrowserMainParts::PreMainMessageLoopRunImpl() chrome\_browser\_main.cc:1636  

#20 0x116a6f276 in ChromeBrowserMainParts::PreMainMessageLoopRun() chrome\_browser\_main.cc:1041  

#21 0x10f94bae2 in content::BrowserMainLoop::PreMainMessageLoopRun() browser\_main\_loop.cc:944  

#22 0x110ac0c3f in content::StartupTaskRunner::RunAllTasksNow() callback.h:101  

#23 0x10f94803c in content::BrowserMainLoop::CreateStartupTasks() browser\_main\_loop.cc:854  

#24 0x10f950adc in content::BrowserMainRunnerImpl::Initialize(content::MainFunctionParams const&) browser\_main\_runner\_impl.cc:129  

#25 0x10f94371a in content::BrowserMain(content::MainFunctionParams const&) browser\_main.cc:43  

#26 0x116185175 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content\_main\_runner\_impl.cc:555  

#27 0x1161844c3 in content::ContentMainRunnerImpl::Run(bool) content\_main\_runner\_impl.cc:926  

#28 0x11618125b in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner\*) content\_main.cc:372  

#29 0x11618191c in content::ContentMain(content::ContentMainParams const&) content\_main.cc:398

HINT: if you don't care about these errors you may set ASAN\_OPTIONS=detect\_container\_overflow=0.  

If you suspect a false positive see also: <https://github.com/google/sanitizers/wiki/AddressSanitizerContainerOverflow>.  

SUMMARY: AddressSanitizer: container-overflow view\_model.h:81 in TabStrip::SetSelection(ui::ListSelectionModel const&)  

Shadow bytes around the buggy address:  

0x1c1000041a30: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x1c1000041a40: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x1c1000041a50: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x1c1000041a60: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c1000041a70: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa  

=>0x1c1000041a80: fa fa fa fa 00 00 00[fc]fc fc fc fc fc fc fc fc  

0x1c1000041a90: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fa  

0x1c1000041aa0: fa fa fa fa 00 00 00 00 00 00 fc fc fc fc fc fc  

0x1c1000041ab0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c1000041ac0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd  

0x1c1000041ad0: fa fa fa fa 00 00 00 fc fc fc fc fc fc fc fc fc  

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

- deleted (application/octet-stream, 0 B)
- [poc.html](attachments/poc.html) (text/plain, 176 B)
- [screen.mov](attachments/screen.mov) (video/quicktime, 3.6 MB)
- [screen.mov](attachments/screen.mov) (video/quicktime, 5.5 MB)

## Timeline

### [Deleted User] (2021-01-27)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-01-27)

Thanks for reporting this.

I'm unable to reproduce this issue, as the window.close() call in your trigger is blocked due to long-standing policies that prevent scripts from closing windows. Could you provide more details about your steps to reproduce?

[Monorail components: UI>Browser>TabStrip]

### rs...@chromium.org (2021-01-27)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-01-27)

Okey, I have another way to repro.

1. Run chrome with "about:blank" "http://localhost:8000/poc.html" "about:blank"

2. In the second tab (http://localhost:8000/poc.html) click on the button then drag the third tab to the right and wait till http://localhost:8000/poc.html is closed then try to get it back to the left (next to the first tab).


### [Deleted User] (2021-01-27)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-01-27)

Sorry I wasn't clearer: Your trigger button does not close the window, because it's being blocked from doing so due to existing security policies (specifically, the attempt to close the window is blocked by this line: https://source.chromium.org/chromium/chromium/src/+/master:third_party/blink/renderer/core/frame/dom_window.cc;l=347;drc=e1facbdd9b6cfe6f5ec53f8b20e662c934e75045 )

I wanted to make sure you're not running with any custom command-line flags or options here that would be useful to verify the repro.

### ch...@gmail.com (2021-01-28)

I'm able to repro this in a fresh profile.

Can you attach a screen recording using Quicktime?

### [Deleted User] (2021-01-28)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2021-01-28)

No.

### ch...@gmail.com (2021-01-28)

Note: window.close() requires that your tab has no history to close the window (won't work unless you have a fresh browsing session.)

Please chrome as:

$ out/asan/chrome --user-data-dir=/tmp/xxxx "about:blank" "http://localhost:8000/poc.html" "about:blank"


### ch...@gmail.com (2021-01-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-01-28)

Thanks for confirming there are added command-line flags! ;-) Indeed, I was attempting to better understand the launch scenario, precisely because of the line mentioned in https://crbug.com/chromium/1171049#c6 provides several mitigations to prevent arbitrary window.close()ing

I'm not seeing this reproduce in 90.0.4401.0 (r847401),  nor in 90.0.4399.0 (r 846616), on macOS or Linux, with an ASAN build, with file:// URLs or a local server, with dragging within the window or detaching.

### rs...@chromium.org (2021-01-28)

(To be clear, the Window does indeed close, but no ASAN errors)

### rs...@chromium.org (2021-01-28)

Nevermind, it's clear that it's detach-after-close rather than release-after-close :)

### rs...@chromium.org (2021-01-28)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-01-28)

Sky: Could you help route this appropriately?

### [Deleted User] (2021-01-28)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sk...@chromium.org (2021-01-29)

tbergquist is likely the right person.

### rs...@chromium.org (2021-02-01)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-02-04)

rsleevi@ Thanks for https://crbug.com/chromium/1171049#c14 

### [Deleted User] (2021-02-10)

tbergquist: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2021-02-10)

Hey, I've fixed a number of similar bugs lately but this one somehow slipped under my radar. Could I ask you to please check if this still reproduces on the latest Canary?

### ch...@gmail.com (2021-02-10)

Yes, I'm still able to repro this on Canary 90.0.4414.0.

### tb...@chromium.org (2021-02-11)

Okay, I've posted a WIP candidate fix here: https://chromium-review.googlesource.com/c/chromium/src/+/2688619/
I can't test this (I only have a mac to work on) but CCing Connie who can. Meanwhile reviving my cloudtop in case I need more iteration than this.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/248d3eb06950a4055afc8975fb801334fb8b2118

commit 248d3eb06950a4055afc8975fb801334fb8b2118
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Thu Feb 11 22:48:12 2021

Fix crash when detaching a drag after a tab closed.

Bug: 1171049
Change-Id: Ia47934714f4bb5376d1f8abbabbe0a3cd22422a3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2688619
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Connie Wan <connily@chromium.org>
Cr-Commit-Position: refs/heads/master@{#853260}

[modify] https://crrev.com/248d3eb06950a4055afc8975fb801334fb8b2118/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/248d3eb06950a4055afc8975fb801334fb8b2118/chrome/browser/ui/tabs/tab_strip_model.cc


### ch...@gmail.com (2021-02-15)

Fixed on Canary 90.0.4418.0. Thanks as ever!

### tb...@chromium.org (2021-02-16)

:D

### [Deleted User] (2021-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-17)

[Empty comment from Monorail migration]

### [Deleted User] (2021-02-17)

Requesting merge to stable M88 because latest trunk commit (853260) appears to be after stable branch point (827102).

Requesting merge to beta M89 because latest trunk commit (853260) appears to be after beta branch point (843830).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-02-17)

This bug requires manual review: We are only 12 days from stable.
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

### tb...@google.com (2021-02-17)

1) I'd want security's input on whether the merge is warranted. It's a lowish-complexity fix, mostly I'm unsure how critical of a security issue it is vs the bar for a later merge.
2) https://chromium-review.googlesource.com/c/chromium/src/+/2688619
3) Yes
4) It could go into 88, but it already has the label for that.
5) It fixes an exploitable bug
6) No
7) N/A

### pb...@google.com (2021-02-18)

+Adetaylor@(Security TPM) for merge review

### ad...@chromium.org (2021-02-19)

Yes, please merge to M89, branch 4389.

There's unlikely to be another M88 release but I'll keep the Merge-Request-88 label until we're certain.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-02-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3ad5c3e55c9353d7c60f4ad1424039c96d598cce

commit 3ad5c3e55c9353d7c60f4ad1424039c96d598cce
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Sat Feb 20 00:22:19 2021

Fix crash when detaching a drag after a tab closed.

(cherry picked from commit 248d3eb06950a4055afc8975fb801334fb8b2118)

Bug: 1171049
Change-Id: Ia47934714f4bb5376d1f8abbabbe0a3cd22422a3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2688619
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Connie Wan <connily@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#853260}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2708624
Auto-Submit: Taylor Bergquist <tbergquist@chromium.org>
Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/4389@{#1229}
Cr-Branched-From: 9251c5db2b6d5a59fe4eac7aafa5fed37c139bb7-refs/heads/master@{#843830}

[modify] https://crrev.com/3ad5c3e55c9353d7c60f4ad1424039c96d598cce/chrome/browser/ui/views/tabs/tab_drag_controller.cc
[modify] https://crrev.com/3ad5c3e55c9353d7c60f4ad1424039c96d598cce/chrome/browser/ui/tabs/tab_strip_model.cc


### am...@google.com (2021-02-24)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-02-25)

Congratulations, Khalil! The VRP Panel has decided to award you $10,000 for this report. Nice work!

### ad...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-26)

[Empty comment from Monorail migration]

### ad...@google.com (2021-02-26)

Not merging to M88 - no further releases planned.

### as...@google.com (2021-03-01)

Marking as not applicable for LTS since introducing code landed after M86 (same as https://crbug.com/1163845).

### ad...@google.com (2021-03-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-05-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1171049?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054585)*
