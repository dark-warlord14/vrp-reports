# Heap UaF in TabStrip::CloseTab

| Field | Value |
|-------|-------|
| **Issue ID** | [40052307](https://issues.chromium.org/issues/40052307) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **Reporter** | dm...@gmail.com |
| **Assignee** | tb...@chromium.org |
| **Created** | 2020-05-14 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:68.0) Gecko/20100101 Firefox/68.0

Steps to reproduce the problem:
1. Open PoC.html
2. Click Start.
    - Allow popups after closing (if necessary) and click Start again.
3. Start closing of new tabs (it's important to do this fast).

What is the expected behavior?
Tabs closing without crash with heap-use-after-free.

What went wrong?
# ASAN Log:
==35868==ERROR: AddressSanitizer: heap-use-after-free on address 0x61a000081920 at pc 0x000123a3d81d bp 0x7ffeef62ddd0 sp 0x7ffeef62ddc8
READ of size 1 at 0x61a000081920 thread T0
    #0 0x123a3d81c in TabStrip::CloseTab(Tab*, CloseTabSource) tab_strip.cc:1655
    #1 0x1239de4d0 in Tab::ButtonPressed(views::Button*, ui::Event const&) tab.cc:272
    #2 0x120fa2ad6 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) button_controller.cc
    #3 0x11a7e8e41 in ui::ScopedTargetHandler::OnEvent(ui::Event*) scoped_target_handler.cc:32
    #4 0x11a7dcb84 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:142
    #5 0x11a7dc0e0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:58
    #6 0x1211ec2c8 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) root_view.cc:467
    #7 0x121207df5 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1275
    #8 0x11ecb5184 in -[BridgedContentView mouseEvent:] bridged_content_view.mm:556
    #9 0x118e3ab39 in -[BaseView mouseUp:] base_view.mm:127
    #10 0x7fff347eaafe in -[NSWindow(NSEventRouting) _reallySendEvent:isDelayedEvent:]+0xab1 (AppKit:x86_64+0x1e6afe)
    #11 0x7fff347e9e28 in -[NSWindow(NSEventRouting) sendEvent:]+0x15c (AppKit:x86_64+0x1e5e28)
    #12 0x11ecc3863 in -[NativeWidgetMacNSWindow sendEvent:] native_widget_mac_nswindow.mm:276
    #13 0x7fff347e81b3 in -[NSApplication(NSEvent) sendEvent:]+0x15f (AppKit:x86_64+0x1e41b3)
    #14 0x116e1b918 in __34-[BrowserCrApplication sendEvent:]_block_invoke chrome_browser_application_mac.mm:328
    #15 0x1180db849 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd9d4849)
    #16 0x116e1aa01 in -[BrowserCrApplication sendEvent:] chrome_browser_application_mac.mm:309
    #17 0x7fff3463521e in -[NSApplication run]+0x2c2 (AppKit:x86_64+0x3121e)
    #18 0x1180f483a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) message_pump_mac.mm:836
    #19 0x1180ee4e9 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) message_pump_mac.mm:191
    #20 0x117f92e3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread_controller_with_message_pump_impl.cc:443
    #21 0x117ef4fdb in base::RunLoop::Run() run_loop.cc:124
    #22 0x116e44342 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome_browser_main.cc:1676
    #23 0x10f581e6b in content::BrowserMainLoop::RunMainMessageLoopParts() browser_main_loop.cc:1051
    #24 0x10f587a31 in content::BrowserMainRunnerImpl::Run() browser_main_runner_impl.cc:150
    #25 0x10f579457 in content::BrowserMain(content::MainFunctionParams const&) browser_main.cc:47
    #26 0x1166f294e in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content_main_runner_impl.cc:943
    #27 0x1166f1cc7 in content::ContentMainRunnerImpl::Run(bool) content_main_runner_impl.cc:845
    #28 0x121359729 in service_manager::Main(service_manager::MainParams const&) main.cc:454
    #29 0x1166efc4c in content::ContentMain(content::ContentMainParams const&) content_main.cc:19
    #30 0x10a70bad9 in ChromeMain chrome_main.cc:110
    #31 0x1005cf4ba in main chrome_exe_main_mac.cc:117
    #32 0x7fff7130ecc8 in start+0x0 (libdyld.dylib:x86_64+0x1acc8)

0x61a000081920 is located 672 bytes inside of 1224-byte region [0x61a000081680,0x61a000081b48)
freed by thread T0 here:
    #0 0x10087bbe6  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x43be6)
    #1 0x120f40db2 in views::BoundsAnimator::AnimationEndedOrCanceled(gfx::Animation const*, views::BoundsAnimator::AnimationEndType) bounds_animator.cc
    #2 0x120f3f5fc in views::BoundsAnimator::Cancel() bounds_animator.cc:145
    #3 0x123a3d4a7 in TabStrip::CloseTab(Tab*, CloseTabSource) tab_strip.cc:1642
    #4 0x1239de4d0 in Tab::ButtonPressed(views::Button*, ui::Event const&) tab.cc:272
    #5 0x120fa2ad6 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) button_controller.cc
    #6 0x11a7e8e41 in ui::ScopedTargetHandler::OnEvent(ui::Event*) scoped_target_handler.cc:32
    #7 0x11a7dcb84 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:142
    #8 0x11a7dc0e0 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) event_dispatcher.cc:58
    #9 0x1211ec2c8 in views::internal::RootView::OnMouseReleased(ui::MouseEvent const&) root_view.cc:467
    #10 0x121207df5 in views::Widget::OnMouseEvent(ui::MouseEvent*) widget.cc:1275
    #11 0x11ecb5184 in -[BridgedContentView mouseEvent:] bridged_content_view.mm:556
    #12 0x118e3ab39 in -[BaseView mouseUp:] base_view.mm:127
    #13 0x7fff347eaafe in -[NSWindow(NSEventRouting) _reallySendEvent:isDelayedEvent:]+0xab1 (AppKit:x86_64+0x1e6afe)
    #14 0x7fff347e9e28 in -[NSWindow(NSEventRouting) sendEvent:]+0x15c (AppKit:x86_64+0x1e5e28)
    #15 0x11ecc3863 in -[NativeWidgetMacNSWindow sendEvent:] native_widget_mac_nswindow.mm:276
    #16 0x7fff347e81b3 in -[NSApplication(NSEvent) sendEvent:]+0x15f (AppKit:x86_64+0x1e41b3)
    #17 0x116e1b918 in __34-[BrowserCrApplication sendEvent:]_block_invoke chrome_browser_application_mac.mm:328
    #18 0x1180db849 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd9d4849)
    #19 0x116e1aa01 in -[BrowserCrApplication sendEvent:] chrome_browser_application_mac.mm:309
    #20 0x7fff3463521e in -[NSApplication run]+0x2c2 (AppKit:x86_64+0x3121e)
    #21 0x1180f483a in base::MessagePumpNSApplication::DoRun(base::MessagePump::Delegate*) message_pump_mac.mm:836
    #22 0x1180ee4e9 in base::MessagePumpCFRunLoopBase::Run(base::MessagePump::Delegate*) message_pump_mac.mm:191
    #23 0x117f92e3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) thread_controller_with_message_pump_impl.cc:443
    #24 0x117ef4fdb in base::RunLoop::Run() run_loop.cc:124
    #25 0x116e44342 in ChromeBrowserMainParts::MainMessageLoopRun(int*) chrome_browser_main.cc:1676
    #26 0x10f581e6b in content::BrowserMainLoop::RunMainMessageLoopParts() browser_main_loop.cc:1051
    #27 0x10f587a31 in content::BrowserMainRunnerImpl::Run() browser_main_runner_impl.cc:150
    #28 0x10f579457 in content::BrowserMain(content::MainFunctionParams const&) browser_main.cc:47
    #29 0x1166f294e in content::ContentMainRunnerImpl::RunServiceManager(content::MainFunctionParams&, bool) content_main_runner_impl.cc:943

previously allocated by thread T0 here:
    #0 0x10087ba9d  (libclang_rt.asan_osx_dynamic.dylib:x86_64+0x43a9d)
    #1 0x116d02a67 in operator new(unsigned long) new.cpp:67
    #2 0x123a32950 in TabStrip::AddTabAt(int, TabRendererData, bool) tab_strip.cc:1110
    #3 0x1239b9aa2 in BrowserTabStripController::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) browser_tab_strip_controller.cc:539
    #4 0x12317ab77 in TabStripModel::InsertWebContentsAtImpl(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, base::Optional<tab_groups::TabGroupId>) tab_strip_model.cc:1646
    #5 0x12318923e in TabStripModel::AddWebContents(std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, ui::PageTransition, int, base::Optional<tab_groups::TabGroupId>) tab_strip_model.cc:977
    #6 0x1230437cb in Navigate(NavigateParams*) browser_navigator.cc:694
    #7 0x12304cb3a in chrome::AddWebContents(Browser*, content::WebContents*, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, GURL const&, WindowOpenDisposition, gfx::Rect const&) browser_tabstrip.cc:77
    #8 0x12300b8d0 in non-virtual thunk to Browser::AddNewContents(content::WebContents*, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, GURL const&, WindowOpenDisposition, gfx::Rect const&, bool, bool*) browser.cc:1698
    #9 0x1106abee7 in content::WebContentsImpl::ShowCreatedWindow(int, int, WindowOpenDisposition, gfx::Rect const&, bool) web_contents_impl.cc:3119
    #10 0x10dddb9e2 in content::mojom::FrameHostStubDispatch::Accept(content::mojom::FrameHost*, mojo::Message*) frame.mojom.cc:6422
    #11 0x1184ee356 in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) interface_endpoint_client.cc:554
    #12 0x1184f7144 in mojo::MessageDispatcher::Accept(mojo::Message*) message_dispatcher.cc:46
    #13 0x11a5d9a70 in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnProxyThread(mojo::Message) ipc_mojo_bootstrap.cc:934
    #14 0x11a5d34cb in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) bind_internal.h:678
    #15 0x117f52058 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) task_annotator.cc:142
    #16 0x117f91ba6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) thread_controller_with_message_pump_impl.cc:329
    #17 0x117f91536 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() thread_controller_with_message_pump_impl.cc:254
    #18 0x1180f1e58 in invocation function for block in base::MessagePumpCFRunLoopBase::RunWorkSource(void*) message_pump_mac.mm:477
    #19 0x1180db849 in base::mac::CallWithEHFrame(void () block_pointer)+0x9 (Chromium Framework:x86_64+0xd9d4849)
    #20 0x1180efd55 in base::MessagePumpCFRunLoopBase::RunWorkSource(void*) message_pump_mac.mm:476
    #21 0x7fff373c7f11 in __CFRUNLOOP_IS_CALLING_OUT_TO_A_SOURCE0_PERFORM_FUNCTION__+0x10 (CoreFoundation:x86_64h+0x83f11)
    #22 0x7fff373c7eb0 in __CFRunLoopDoSource0+0x66 (CoreFoundation:x86_64h+0x83eb0)
    #23 0x7fff373c7cca in __CFRunLoopDoSources0+0xd0 (CoreFoundation:x86_64h+0x83cca)
    #24 0x7fff373c69f9 in __CFRunLoopRun+0x39e (CoreFoundation:x86_64h+0x829f9)
    #25 0x7fff373c5ffd in CFRunLoopRunSpecific+0x1cd (CoreFoundation:x86_64h+0x81ffd)
    #26 0x7fff35ff9abc in RunCurrentEventLoopInMode+0x123 (HIToolbox:x86_64+0x2fabc)
    #27 0x7fff35ff97d4 in ReceiveNextEventCommon+0x247 (HIToolbox:x86_64+0x2f7d4)
    #28 0x7fff35ff9578 in _BlockUntilNextEventMatchingListInModeWithFilter+0x3f (HIToolbox:x86_64+0x2f578)
    #29 0x7fff34644c98 in _DPSNextEvent+0x372 (AppKit:x86_64+0x40c98)

SUMMARY: AddressSanitizer: heap-use-after-free tab_strip.cc:1655 in TabStrip::CloseTab(Tab*, CloseTabSource)
Shadow bytes around the buggy address:
  0x1c34000102d0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c34000102e0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c34000102f0: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c3400010300: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c3400010310: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x1c3400010320: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fd fd fd
  0x1c3400010330: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c3400010340: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c3400010350: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x1c3400010360: fd fd fd fd fd fd fd fd fd fa fa fa fa fa fa fa
  0x1c3400010370: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==35868==ABORTING
Received signal 6
 [0x0001180afb39]
 [0x000117e0fbb3]
 [0x0001180af5a7]
 [0x7fff715075fd]
 [0x0001008d1008]
 [0x7fff713dd808]
 [0x00010089a766]
 [0x00010089a154]
 [0x0001008820f4]
 [0x00010088198e]
 [0x000100882418]
 [0x000123a3d81d]
 [0x0001239de4d1]
 [0x000120fa2ad7]
 [0x00011a7e8e42]
 [0x00011a7dcb85]
 [0x00011a7dc0e1]
 [0x0001211ec2c9]
 [0x000121207df6]
 [0x00011ecb5185]
 [0x000118e3ab3a]
 [0x7fff347eaaff]
 [0x7fff347e9e29]
 [0x00011ecc3864]
 [0x7fff347e81b4]
 [0x000116e1b919]
 [0x0001180db84a]
 [0x000116e1aa02]
 [0x7fff3463521f]
 [0x0001180f483b]
 [0x0001180ee4ea]
 [0x000117f92e3c]
 [0x000117ef4fdc]
 [0x000116e44343]
 [0x00010f581e6c]
 [0x00010f587a32]
 [0x00010f579458]
 [0x0001166f294f]
 [0x0001166f1cc8]
 [0x00012135972a]
 [0x0001166efc4d]
 [0x00010a70bada]
 [0x0001005cf4bb]
 [0x7fff7130ecc9]
 [0x000000000001]
[end of stack trace]

# Versions
Chromium: v. 84.0.4147.0 (Developer Build) (64-bit)
OS: Mac OS Catalina v.10.15.4

# Reproduce
See attached video (ChromiumHeapUaFPoC.mov).

Did this work before? N/A 

Chrome version: 84.0.4147.0 (Developer Build) (64-bit)  Channel: dev
OS Version: OS X 10.15.4
Flash Version: Shockwave Flash 30.0 r0

I check this in Google Chrome (v. 81.0.4044.138 (Official Build) (64-bit) (latest available version for MacOS)), but this issue not working in this browser.

## Attachments

- [ChromiumHeapUaFPoC.mov](attachments/ChromiumHeapUaFPoC.mov) (video/quicktime, 4.6 MB)
- [PoC.html](attachments/PoC.html) (text/plain, 398 B)
- [bug1082755-asan.log](attachments/bug1082755-asan.log) (text/plain, 13.3 KB)

## Timeline

### ct...@chromium.org (2020-05-14)

Tentatively setting Security_Severity-High (UaF in browser, but requires substantial user interaction) but it's unclear how exploitable this would be versus just being a crash. Per reporter it sounds like this affects M-84 but not M-81, so tentatively setting Security_Impact-Head until I repro and test more versions and platforms.

Adding some chrome/browser/ui/views/tabs/OWNERS as it looks like this is occurring within TabStrip code.



[Monorail components: UI>Browser>TabStrip]

### [Deleted User] (2020-05-14)

Setting milestone and target because of Security_Impact=Head and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pk...@chromium.org (2020-05-14)

In brief, it looks to me like CloseTab() calls StopAnimating(), which completes the tab animation, which (probably -- call stack is elided) calls back to OnTabCloseAnimationCompleted() via the animation delegate, which deletes the tab.  Then later CloseTab() tries to deref the |tab_| pointer.

The bandaid fix is to move code around so we don't access |tab_| after we've potentially freed it.  Before doing that it's worth thinking briefly on the larger expectations of lifetimes etc. to make sure we're not violating any implicit expectations and won't reintroduce this in the future.  For example, CloseTab() only calls StopAnimating() if !in_tab_close_, which looks on its face likes no tabs are closing -- but I think that's only set for a subset of tab-closing cases, so the code is probably correct-but-potentially-misleading.  Maybe better names/comments are warranted.

->connily as a better owner to triage since I'm a bit of an "emeritus" owner at this point.

### co...@chromium.org (2020-05-14)

Passing along to Taylor, who has been working with animations lately. Taylor, let me know if you want to sync on this, happy to help!

### [Deleted User] (2020-05-14)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tb...@chromium.org (2020-05-15)

PK is basically right. I can add that this is specifically happening in the case where the tab under the cursor is already closing, and is forwarding its mouse events to the tab to its right. In that case, |model_index| is updated to reflect the new target, but |tab| is not, so when that already-closing tab is destroyed by StopAnimation, |tab| becomes a landmine.

I'll fix it.

### tb...@chromium.org (2020-05-15)

Okay, https://chromium-review.googlesource.com/c/chromium/src/+/2204259 should fix it according to my understanding of the issue. I'm not able to reproduce the issue locally - I can't click that fast, I guess - so I can't verify the fix myself.

### ct...@chromium.org (2020-05-16)

I was able to repro on macOS ASAN builds r737173 (M-81 Stable), r756037 (M-83 Beta), and r769468 (~head), so updating Impact label.

Granting the popup exception first and refreshing the page helped make it easier to repro (it would popup two tabs and basically immediately trigger the UAF crash). I've attached my ASAN log as well in case it's useful.

### ct...@chromium.org (2020-05-19)

Re: #7, to reproduce you'll likely need to test in an ASAN build (if you weren't already)

Pre-built archives: https://commondatastorage.googleapis.com/chromium-browser-asan/index.html
Instructions for compiling (to test your fix): https://chromium.googlesource.com/chromium/src/+/HEAD/docs/asan.md

### [Deleted User] (2020-05-20)

[Empty comment from Monorail migration]

### sr...@google.com (2020-05-20)

adetaylor@ can you review if this should block ramp up for stable release or can we wait for re-spin ?

### ad...@chromium.org (2020-05-20)

Per https://crbug.com/chromium/1082755#c8 it's not a M83 regression; it can wait for respin.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ec2b409fc0b3bac329b02eafe6b9c5ba47c3fd90

commit ec2b409fc0b3bac329b02eafe6b9c5ba47c3fd90
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Wed May 20 21:00:08 2020

Fix UAF when closing tabs very quickly.

Bug: 1082755
Change-Id: Id8e174625f16e9a319000eb7427ec8659174c7d4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2204259
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Commit-Position: refs/heads/master@{#770758}

[modify] https://crrev.com/ec2b409fc0b3bac329b02eafe6b9c5ba47c3fd90/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/ec2b409fc0b3bac329b02eafe6b9c5ba47c3fd90/chrome/browser/ui/views/tabs/tab_strip.h
[modify] https://crrev.com/ec2b409fc0b3bac329b02eafe6b9c5ba47c3fd90/chrome/browser/ui/views/tabs/tab_strip_unittest.cc


### sr...@google.com (2020-05-27)

what are next steps here? Is this ready for merge?

### ad...@chromium.org (2020-05-27)

tbergquist@ please mark it as Fixed if it is. Not a regression so removing RBS.

### mp...@chromium.org (2020-06-03)

[Empty comment from Monorail migration]

### tb...@chromium.org (2020-06-18)

Oh, whoops, yes, this is fixed.

### ad...@chromium.org (2020-06-19)

Thanks. Sheriffbot will soon add Merge-Request-83 and Merge-Request-84 labels, so I'm going to short cut the process. Sheriffbot will also ask you a lot of questions - as you answer them, please could you also comment on stability risks from merging this back. As it's been in Canary for such a long time, I expect we'd have seen any new problems by now. In practice we're almost certainly too late for M83 so this will go into M84. I'm not sure if it will make it into the first M84 release or a refresh.

### [Deleted User] (2020-06-19)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-20)

[Empty comment from Monorail migration]

### na...@google.com (2020-06-22)

[Empty comment from Monorail migration]

### sr...@google.com (2020-06-22)

adetaylor@ pls remove merge-request-83 label for this as we are done with M83 re-spins

### ad...@chromium.org (2020-06-23)

> "we are done with M83 re-spins"

Hahahaha. Jinx.

### pb...@google.com (2020-06-23)

adetaylor@ can you please approve the CL for M84 branch so that we can we can get the CL in this week Beta/Stable RC.

### ad...@chromium.org (2020-06-23)

I don't feel comfortable approving this without hearing from tbergquist re https://crbug.com/chromium/1082755#c18 and https://crbug.com/chromium/1082755#c19, and ideally having him confirm that he's looked for evidence of adverse stability impacts in Canary and it's all fine. I was waiting for comment before approving.

Then again. As this has been in Canary for five weeks, I'm just going to approve it. tbergquist@ please confirm there are no known problems in Canary and then merge to branch 4147.

### [Deleted User] (2020-06-23)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-06-23)

[Empty comment from Monorail migration]

### tb...@chromium.org (2020-06-23)

Hey, sorry I haven't been responsive enough here, I've had a busy few days.

I don't expect any extra stability risks from merging this back to 84. I'll go ahead and do the merge.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/37b55d52cae83c948d1e027ea461e4aa7abac347

commit 37b55d52cae83c948d1e027ea461e4aa7abac347
Author: Taylor Bergquist <tbergquist@chromium.org>
Date: Tue Jun 23 18:19:44 2020

Fix UAF when closing tabs very quickly.

TBR=tbergquist@chromium.org

(cherry picked from commit ec2b409fc0b3bac329b02eafe6b9c5ba47c3fd90)

Bug: 1082755
Change-Id: Id8e174625f16e9a319000eb7427ec8659174c7d4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2204259
Commit-Queue: Taylor Bergquist <tbergquist@chromium.org>
Reviewed-by: Peter Kasting <pkasting@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#770758}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2261154
Reviewed-by: Taylor Bergquist <tbergquist@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#763}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/37b55d52cae83c948d1e027ea461e4aa7abac347/chrome/browser/ui/views/tabs/tab_strip.cc
[modify] https://crrev.com/37b55d52cae83c948d1e027ea461e4aa7abac347/chrome/browser/ui/views/tabs/tab_strip.h
[modify] https://crrev.com/37b55d52cae83c948d1e027ea461e4aa7abac347/chrome/browser/ui/views/tabs/tab_strip_unittest.cc


### mm...@chromium.org (2020-06-30)

tbergquist@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

dmitriefdaniil@gmail.com thank you for the report - how would you like to be credited in the Chrome release notes?

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### dm...@gmail.com (2020-07-13)

Hi, adetaylor@chromium.org

You can use my nickname: DDV_UA

Thanks!

### na...@google.com (2020-07-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-07-16)

Congrats! The Panel decided to award $5,000 for this report!

### na...@google.com (2020-07-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1082755?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1083832]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052307)*
