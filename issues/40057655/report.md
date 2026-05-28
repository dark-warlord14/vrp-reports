# Security: UAF during sharesheet teardown with animation running

| Field | Value |
|-------|-------|
| **Issue ID** | [40057655](https://issues.chromium.org/issues/40057655) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P2 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-10-19 |
| **Bounty** | $7,500.00 |

## Description

Chrome Version: 97.0.4674.0  

Operating System: Ozone X11

**REPRODUCTION CASE**

1. Open a new tab
2. Click on 'Sharesheet' icon and close the tab (sometimes looks like it can take several tries to repro the crash).

==3334==ERROR: AddressSanitizer: heap-use-after-free on address 0x6070000d0900 at pc 0x560bf6aa5243 bp 0x7ffffbdd0450 sp 0x7ffffbdd0448  

READ of size 8 at 0x6070000d0900 thread T0 (chrome)  

==3334==WARNING: invalid path to external symbolizer!  

==3334==WARNING: Failed to use and restart external symbolizer!  

#0 0x560bf6aa5242 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26e56242)  

#1 0x560bf668d9dc (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26a3e9dc)  

#2 0x560bf668e8ca (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26a3f8ca)  

#3 0x560bf088655c (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20c3755c)  

#4 0x560bf0886ab3 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20c37ab3)  

#5 0x560bf0889c36 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20c3ac36)  

#6 0x560bf0893a20 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20c44a20)  

#7 0x560bf0895224 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20c46224)  

#8 0x560bf089b89e (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20c4c89e)  

#9 0x560bf083e0a1 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x20bef0a1)  

#10 0x560bef85bfe9 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1fc0cfe9)  

#11 0x560bef85d60f (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1fc0e60f)  

#12 0x560bef85f2a9 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1fc102a9)  

#13 0x560bea80d293 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abbe293)  

#14 0x560bea8453d9 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf63d9)  

#15 0x560bea844c42 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf5c42)  

#16 0x560bea845d31 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf6d31)  

#17 0x560bea984a9d (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1ad35a9d)  

#18 0x560bea8463ee (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf73ee)  

#19 0x560bea786b9c (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1ab37b9c)  

#20 0x560be1519648 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x118ca648)  

#21 0x560be151da7f (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x118cea7f)  

#22 0x560be1513c8f (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x118c4c8f)  

#23 0x560bea557e37 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1a908e37)  

#24 0x560bea55a44d (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1a90b44d)  

#25 0x560bea559892 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1a90a892)  

#26 0x560bea5549e3 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1a9059e3)  

#27 0x560bea554e86 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1a905e86)  

#28 0x560bdd390646 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0xd741646)  

#29 0x7f41f4b360b2 (/lib/x86\_64-linux-gnu/libc.so.6+0x270b2)

0x6070000d0900 is located 16 bytes inside of 72-byte region [0x6070000d08f0,0x6070000d0938)  

freed by thread T0 (chrome) here:  

#0 0x560bdd38e69d (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0xd73f69d)  

#1 0x560bea80119d (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb219d)  

#2 0x560bea801151 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb2151)  

#3 0x560bea801151 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb2151)  

#4 0x560bea801131 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb2131)  

#5 0x560bea801151 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb2151)  

#6 0x560bea801151 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb2151)  

#7 0x560bea801151 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb2151)  

#8 0x560bea800c98 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abb1c98)  

#9 0x560be235ec4e (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1270fc4e)  

#10 0x560be23603cf (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x127113cf)  

#11 0x560bf6144265 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x264f5265)  

#12 0x560bf61495d7 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x264fa5d7)  

#13 0x560bf614a17a (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x264fb17a)  

#14 0x560be00b2ef3 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x10463ef3)  

#15 0x560bebf10a91 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1c2c1a91)  

#16 0x560bebf20b90 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1c2d1b90)  

#17 0x560bebf13596 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1c2c4596)  

#18 0x560bebed6f34 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1c287f34)  

#19 0x560bebed0de9 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1c281de9)  

#20 0x560bea80d293 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abbe293)  

#21 0x560bea8453d9 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf63d9)  

#22 0x560bea844c42 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf5c42)  

#23 0x560bea845d31 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf6d31)  

#24 0x560bea984a9d (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1ad35a9d)  

#25 0x560bea8463ee (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1abf73ee)  

#26 0x560bea786b9c (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1ab37b9c)  

#27 0x560be1519648 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x118ca648)  

#28 0x560be151da7f (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x118cea7f)  

#29 0x560be1513c8f (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x118c4c8f)

previously allocated by thread T0 (chrome) here:  

#0 0x560bdd38de3d (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0xd73ee3d)  

#1 0x560bf6aa4495 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26e55495)  

#2 0x560bf6aa4441 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26e55441)  

#3 0x560bf6ef8dd8 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x272a9dd8)  

#4 0x560bf6dbfc8c (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x27170c8c)  

#5 0x560bf6ce268a (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x2709368a)  

#6 0x560bf701d6f3 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x273ce6f3)  

#7 0x560bf6031928 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x263e2928)  

#8 0x560bf602e562 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x263df562)  

#9 0x560bf602d5b7 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x263de5b7)  

#10 0x560bf61412e5 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x264f22e5)  

#11 0x560bf614d87e (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x264fe87e)  

#12 0x560bf60721bd (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x264231bd)  

#13 0x560bf607ac50 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x2642bc50)  

#14 0x560bf6076657 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26427657)  

#15 0x560bf6f3227b (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x272e327b)  

#16 0x560bf6f85bf2 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x27336bf2)  

#17 0x560bf6f3f237 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x272f0237)  

#18 0x560bf1f5beaa (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x2230ceaa)  

#19 0x560bf1f63826 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x22314826)  

#20 0x560bf1f31dbf (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x222e2dbf)  

#21 0x560bed8103d5 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc13d5)  

#22 0x560bed80f994 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc0994)  

#23 0x560bed80f45c (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc045c)  

#24 0x560bed80f1c9 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc01c9)  

#25 0x560bf20b250a (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x2246350a)  

#26 0x560bf20c98cc (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x2247a8cc)  

#27 0x560bed8103d5 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc13d5)  

#28 0x560bed80f994 (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc0994)  

#29 0x560bed80f45c (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x1dbc045c)

SUMMARY: AddressSanitizer: heap-use-after-free (/home/lbstyle/Desktop/asan-linux-release-932757/chrome+0x26e56242)  

Shadow bytes around the buggy address:  

0x0c0e800120d0: fd fd fd fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c0e800120e0: 00 fa fa fa fa fa fd fd fd fd fd fd fd fd fd fd  

0x0c0e800120f0: fa fa fa fa fd fd fd fd fd fd fd fd fd fa fa fa  

0x0c0e80012100: fa fa fd fd fd fd fd fd fd fd fd fa fa fa fa fa  

0x0c0e80012110: 00 00 00 00 00 00 00 00 00 fa fa fa fa fa fd fd  

=>0x0c0e80012120:[fd]fd fd fd fd fd fd fa fa fa fa fa fd fd fd fd  

0x0c0e80012130: fd fd fd fd fd fa fa fa fa fa fd fd fd fd fd fd  

0x0c0e80012140: fd fd fd fa fa fa fa fa fd fd fd fd fd fd fd fd  

0x0c0e80012150: fd fa fa fa fa fa fd fd fd fd fd fd fd fd fd fa  

0x0c0e80012160: fa fa fa fa 00 00 00 00 00 00 00 00 00 fa fa fa  

0x0c0e80012170: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa  

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

- [screen.mp4](attachments/screen.mp4) (video/mp4, 2.7 MB)

## Timeline

### [Deleted User] (2021-10-19)

[Empty comment from Monorail migration]

### es...@chromium.org (2021-10-20)

Sharesheet owners, could you please take a look? Marking as Medium severity because it doesn't seem very exploitable due to the user interaction required.

[Monorail components: Platform>Apps>Foundation>Sharesheet]

### [Deleted User] (2021-10-20)

[Empty comment from Monorail migration]

### me...@chromium.org (2021-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-20)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-20)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-10-20)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2021-10-21)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Sharing]

### me...@chromium.org (2021-10-21)

Do you think this is related to https://crbug.com/1249491?

+kristipark + ellyjones

### el...@chromium.org (2021-10-21)

It could be?

Reporter, can you get a symbolized stack trace please?

### ch...@gmail.com (2021-10-21)

Sorry, I couldn't get a symbolized stack trace.

### el...@chromium.org (2021-10-21)

Rats, okay.

Can you paste your gn args here please? I'll try to repro locally.

### ch...@gmail.com (2021-10-21)

[Comment Deleted]

### ch...@gmail.com (2021-10-24)

[Comment Deleted]

### ch...@gmail.com (2021-10-25)

Symbolized trace looks like:

==487960==ERROR: AddressSanitizer: heap-use-after-free on address 0x607000f1a090 at pc 0x55f338dfd66d bp 0x7ffed6fd7370 sp 0x7ffed6fd7368
READ of size 8 at 0x607000f1a090 thread T0 (chrome)
    #0 0x55f338dfd66c in view ui/views/view_tracker.h:23:25
    #1 0x55f338dfd66c in sharing_hub::SharingHubBubbleController::OnSharesheetClosed(views::Widget::ClosedReason) chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc:267:59
    #2 0x55f338940dcb in base::OnceCallback<void (views::Widget::ClosedReason)>::Run(views::Widget::ClosedReason) && base/callback.h:142:12
    #3 0x55f338948440 in ash::sharesheet::SharesheetBubbleView::CloseWidgetWithReason(views::Widget::ClosedReason) chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc:739:32
    #4 0x55f31aacb157 in base::OnceCallback<void ()>::Run() && base/callback.h:142:12
    #5 0x55f338949be9 in ui::ClosureAnimationObserver::OnImplicitAnimationsCompleted() ui/compositor/closure_animation_observer.cc:18:23
    #6 0x55f33198ad86 in CheckCompleted ui/compositor/layer_animation_observer.cc:128:5
    #7 0x55f33198ad86 in ui::ImplicitAnimationObserver::OnDetachedFromSequence(ui::LayerAnimationSequence*) ui/compositor/layer_animation_observer.cc:122:3
    #8 0x55f331989ba2 in ui::LayerAnimationObserver::DetachedFromSequence(ui::LayerAnimationSequence*, bool) ui/compositor/layer_animation_observer.cc:55:5
    #9 0x55f33198a1fa in ui::ImplicitAnimationObserver::OnLayerAnimationEnded(ui::LayerAnimationSequence*) ui/compositor/layer_animation_observer.cc:89:13
    #10 0x55f33198e6d6 in ui::LayerAnimationSequence::NotifyEnded() ui/compositor/layer_animation_sequence.cc:289:14
    #11 0x55f33198f468 in ui::LayerAnimationSequence::ProgressToEnd(ui::LayerAnimationDelegate*) ui/compositor/layer_animation_sequence.cc:167:5
    #12 0x55f33199ba2c in ProgressAnimationToEnd ui/compositor/layer_animator.cc:472:13
    #13 0x55f33199ba2c in ui::LayerAnimator::FinishAnimation(ui::LayerAnimationSequence*, bool) ui/compositor/layer_animator.cc:624:5
    #14 0x55f33199f178 in ui::LayerAnimator::StopAnimatingInternal(bool) ui/compositor/layer_animator.cc:529:5
    #15 0x55f33194ea05 in StopAnimating ui/compositor/layer_animator.h:207:26
    #16 0x55f33194ea05 in ui::Layer::CompleteAllAnimations() ui/compositor/layer.cc:1177:12
    #17 0x55f3318cd94b in aura::Window::~Window() ui/aura/window.cc:188:14
    #18 0x55f3318cf3b7 in aura::Window::~Window() ui/aura/window.cc:183:19
    #19 0x55f3336f66ea in wm::TransientWindowManager::OnWindowDestroying(aura::Window*) ui/wm/core/transient_window_manager.cc:258:5
    #20 0x55f3318cda57 in aura::Window::~Window() ui/aura/window.cc:194:14
    #21 0x55f3318cf3b7 in aura::Window::~Window() ui/aura/window.cc:183:19
    #22 0x55f32a98c939 in Run base/callback.h:142:12
    #23 0x55f32a98c939 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #24 0x55f32a9f4265 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:23
    #25 0x55f32a9f2f3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #26 0x55f32a9f5041 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #27 0x55f32ac32abc in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:200:55
    #28 0x55f32a9f5de6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #29 0x55f32a90235e in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #30 0x55f31efa9db1 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1005:18
    #31 0x55f31efaf237 in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:152:15
    #32 0x55f31efa3a1a in content::BrowserMain(content::MainFunctionParams const&) content/browser/browser_main.cc:49:28
    #33 0x55f32a6748e7 in content::RunBrowserProcessMain(content::MainFunctionParams const&, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:641:10
    #34 0x55f32a677171 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams&, bool) content/app/content_main_runner_impl.cc:1137:10
    #35 0x55f32a676470 in content::ContentMainRunnerImpl::Run(bool) content/app/content_main_runner_impl.cc:1004:12
    #36 0x55f32a6710bb in content::RunContentProcess(content::ContentMainParams const&, content::ContentMainRunner*) content/app/content_main.cc:390:36
    #37 0x55f32a671577 in content::ContentMain(content::ContentMainParams const&) content/app/content_main.cc:418:10
    #38 0x55f319ac268b in ChromeMain chrome/app/chrome_main.cc:172:12
    #39 0x7fa0e5e7e0b2 in __libc_start_main /build/glibc-eX1tMB/glibc-2.31/csu/../csu/libc-start.c:308:16

0x607000f1a090 is located 16 bytes inside of 72-byte region [0x607000f1a080,0x607000f1a0c8)
freed by thread T0 (chrome) here:
    #0 0x55f319ac06ed in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x55f32a97c3ad in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #2 0x55f32a97c3ad in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #3 0x55f32a97c3ad in ~unique_ptr buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269:19
    #4 0x55f32a97c3ad in ~pair buildtools/third_party/libc++/trunk/include/utility:394:29
    #5 0x55f32a97c3ad in destroy<std::__1::pair<const void *const, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void, void> buildtools/third_party/libc++/trunk/include/__memory/allocator_traits.h:318:15
    #6 0x55f32a97c3ad in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1801:9
    #7 0x55f32a97c361 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #8 0x55f32a97c361 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #9 0x55f32a97c341 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1798:9
    #10 0x55f32a97c361 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #11 0x55f32a97c361 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #12 0x55f32a97c361 in std::__1::__tree<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::__map_value_compare<void const*, std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, std::__1::less<void const*>, true>, std::__1::allocator<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > > > >::destroy(std::__1::__tree_node<std::__1::__value_type<void const*, std::__1::unique_ptr<base::SupportsUserData::Data, std::__1::default_delete<base::SupportsUserData::Data> > >, void*>*) buildtools/third_party/libc++/trunk/include/__tree:1799:9
    #13 0x55f32a97c067 in ~__tree buildtools/third_party/libc++/trunk/include/__tree:1789:3
    #14 0x55f32a97c067 in ~map buildtools/third_party/libc++/trunk/include/map:1103:5
    #15 0x55f32a97c067 in base::SupportsUserData::~SupportsUserData() base/supports_user_data.cc:71:1
    #16 0x55f3201f5233 in ~WebContents content/public/browser/web_contents.h:316:28
    #17 0x55f3201f5233 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1066:1
    #18 0x55f3201f67f5 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:968:37
    #19 0x55f33833a0c3 in operator() buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54:5
    #20 0x55f33833a0c3 in reset buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315:7
    #21 0x55f33833a0c3 in TabStripModel::SendDetachWebContentsNotifications(TabStripModel::DetachNotifications*) chrome/browser/ui/tabs/tab_strip_model.cc:555:27
    #22 0x55f33833fab6 in TabStripModel::CloseTabs(base::span<content::WebContents* const, 18446744073709551615ul>, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:1797:5
    #23 0x55f33834043a in TabStripModel::CloseWebContentsAt(int, unsigned int) chrome/browser/ui/tabs/tab_strip_model.cc:766:10
    #24 0x55f338248f5f in chrome::CloseWebContents(Browser*, content::WebContents*, bool) chrome/browser/ui/browser_tabstrip.cc:91:31
    #25 0x55f31aacb157 in base::OnceCallback<void ()>::Run() && base/callback.h:142:12
    #26 0x55f31d30294a in blink::mojom::LocalMainFrame_ClosePage_ForwardToCallback::Accept(mojo::Message*) gen/third_party/blink/public/mojom/frame/frame.mojom.cc:17192:26
    #27 0x55f32c39caba in mojo::InterfaceEndpointClient::HandleValidatedMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:895:23
    #28 0x55f32c3b5351 in mojo::MessageDispatcher::Accept(mojo::Message*) mojo/public/cpp/bindings/lib/message_dispatcher.cc:43:19
    #29 0x55f32c3a0201 in mojo::InterfaceEndpointClient::HandleIncomingMessage(mojo::Message*) mojo/public/cpp/bindings/lib/interface_endpoint_client.cc:657:20
    #30 0x55f32c3501ab in IPC::(anonymous namespace)::ChannelAssociatedGroupController::AcceptOnEndpointThread(mojo::Message) ipc/ipc_mojo_bootstrap.cc:984:24
    #31 0x55f32c3487da in Invoke<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:531:12
    #32 0x55f32c3487da in MakeItSo<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message> base/bind_internal.h:711:12
    #33 0x55f32c3487da in RunImpl<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), std::__1::tuple<scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, 0UL, 1UL> base/bind_internal.h:784:12
    #34 0x55f32c3487da in base::internal::Invoker<base::internal::BindState<void (IPC::(anonymous namespace)::ChannelAssociatedGroupController::*)(mojo::Message), scoped_refptr<IPC::(anonymous namespace)::ChannelAssociatedGroupController>, mojo::Message>, void ()>::RunOnce(base::internal::BindStateBase*) base/bind_internal.h:753:12
    #35 0x55f32a98c939 in Run base/callback.h:142:12
    #36 0x55f32a98c939 in base::TaskAnnotator::RunTask(char const*, base::PendingTask*) base/task/common/task_annotator.cc:178:33
    #37 0x55f32a9f4265 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::sequence_manager::LazyNow*) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:358:23
    #38 0x55f32a9f2f3b in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:261:30
    #39 0x55f32a9f5041 in non-virtual thunk to base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc
    #40 0x55f32ac32abc in base::MessagePumpLibevent::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_libevent.cc:200:55
    #41 0x55f32a9f5de6 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:463:12
    #42 0x55f32a90235e in base::RunLoop::Run(base::Location const&) base/run_loop.cc:140:14
    #43 0x55f31efa9db1 in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1005:18

previously allocated by thread T0 (chrome) here:
    #0 0x55f319abfe8d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x55f338dfc5e3 in void content::WebContentsUserData<sharing_hub::SharingHubBubbleController>::CreateForWebContents<>(content::WebContents*) content/public/browser/web_contents_user_data.h:47:28
    #2 0x55f338dfc4e1 in sharing_hub::SharingHubBubbleController::CreateOrGetFromWebContents(content::WebContents*) chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc:90:3
    #3 0x55f339309cb0 in GetController chrome/browser/ui/views/sharing_hub/sharing_hub_icon_view.cc:110:10
    #4 0x55f339309cb0 in sharing_hub::SharingHubIconView::UpdateImpl() chrome/browser/ui/views/sharing_hub/sharing_hub_icon_view.cc:70:44
    #5 0x55f3391a494c in PageActionIconController::UpdateAll() chrome/browser/ui/views/page_action/page_action_icon_controller.cc:250:23
    #6 0x55f3390a72a6 in LocationBarView::Update(content::WebContents*) chrome/browser/ui/views/location_bar/location_bar_view.cc:799:3
    #7 0x55f339460335 in ToolbarView::Update(content::WebContents*) chrome/browser/ui/views/toolbar/toolbar_view.cc:425:20
    #8 0x55f3381f48a2 in Browser::UpdateToolbar(bool) chrome/browser/ui/browser.cc:2482:12
    #9 0x55f3381f1129 in Browser::OnActiveTabChanged(content::WebContents*, content::WebContents*, int, int) chrome/browser/ui/browser.cc:2394:3
    #10 0x55f3381f00a8 in Browser::OnTabStripModelChanged(TabStripModel*, TabStripModelChange const&, TabStripSelectionChange const&) chrome/browser/ui/browser.cc:1187:3
    #11 0x55f338336cf0 in TabStripModel::InsertWebContentsAtImpl(int, std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:1770:14
    #12 0x55f338344f86 in TabStripModel::AddWebContents(std::__1::unique_ptr<content::WebContents, std::__1::default_delete<content::WebContents> >, int, ui::PageTransition, int, absl::optional<tab_groups::TabGroupId>) chrome/browser/ui/tabs/tab_strip_model.cc:1029:3
    #13 0x55f33823e7ce in Navigate(NavigateParams*) chrome/browser/ui/browser_navigator.cc:696:41
    #14 0x55f33832184e in StartupBrowserCreatorImpl::OpenTabsInBrowser(Browser*, bool, std::__1::vector<StartupTab, std::__1::allocator<StartupTab> > const&) chrome/browser/ui/startup/startup_browser_creator_impl.cc:316:5
    #15 0x55f338323ac7 in StartupBrowserCreatorImpl::RestoreOrCreateBrowser(std::__1::vector<StartupTab, std::__1::allocator<StartupTab> > const&, StartupBrowserCreatorImpl::BrowserOpenBehavior, unsigned int, bool, bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:616:13
    #16 0x55f33832089d in StartupBrowserCreatorImpl::DetermineURLsAndLaunch(bool) chrome/browser/ui/startup/startup_browser_creator_impl.cc:425:22
    #17 0x55f33831fe0f in StartupBrowserCreatorImpl::Launch(Profile*, bool, std::__1::unique_ptr<LaunchModeRecorder, std::__1::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator_impl.cc:206:32
    #18 0x55f338319b20 in StartupBrowserCreator::LaunchBrowser(base::CommandLine const&, Profile*, base::FilePath const&, chrome::startup::IsProcessStartup, chrome::startup::IsFirstRun, std::__1::unique_ptr<LaunchModeRecorder, std::__1::default_delete<LaunchModeRecorder> >) chrome/browser/ui/startup/startup_browser_creator.cc:624:31
    #19 0x55f32d7af779 in SessionService::RestoreIfNecessary(std::__1::vector<GURL, std::__1::allocator<GURL> > const&, Browser*, bool) chrome/browser/sessions/session_service.cc:511:23
    #20 0x55f33820964c in chrome::NewEmptyWindow(Profile*, bool) chrome/browser/ui/browser_commands.cc:487:27
    #21 0x55f33899d000 in BrowserShortcutShelfItemController::ItemSelected(std::__1::unique_ptr<ui::Event, std::__1::default_delete<ui::Event> >, long, ash::ShelfLaunchSource, base::OnceCallback<void (ash::ShelfAction, std::__1::vector<ash::ShelfItemDelegate::AppMenuItem, std::__1::allocator<ash::ShelfItemDelegate::AppMenuItem> >)>, base::RepeatingCallback<bool (aura::Window*)> const&) chrome/browser/ui/ash/shelf/browser_shortcut_shelf_item_controller.cc:126:44
    #22 0x55f33663fa03 in ash::ShelfView::ButtonPressed(views::Button*, ui::Event const&, views::InkDrop*) ash/shelf/shelf_view.cc:802:42
    #23 0x55f3334d333a in views::Button::DefaultButtonControllerDelegate::NotifyClick(ui::Event const&) ui/views/controls/button/button.cc:66:13
    #24 0x55f3334db126 in views::ButtonController::OnMouseReleased(ui::MouseEvent const&) ui/views/controls/button/button_controller.cc
    #25 0x55f3365dc90c in ash::ShelfAppButton::OnMouseReleased(ui::MouseEvent const&) ash/shelf/shelf_app_button.cc:619:16
    #26 0x55f3334a2261 in ui::ScopedTargetHandler::OnEvent(ui::Event*) ui/events/scoped_target_handler.cc:28:24
    #27 0x55f32e30849b in ui::EventDispatcher::DispatchEvent(ui::EventHandler*, ui::Event*) ui/events/event_dispatcher.cc:191:12
    #28 0x55f32e307684 in ui::EventDispatcher::ProcessEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:140:5
    #29 0x55f32e30714c in ui::EventDispatcherDelegate::DispatchEventToTarget(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:84:14
    #30 0x55f32e306eb9 in ui::EventDispatcherDelegate::DispatchEvent(ui::EventTarget*, ui::Event*) ui/events/event_dispatcher.cc:56:15

SUMMARY: AddressSanitizer: heap-use-after-free ui/views/view_tracker.h:23:25 in view
Shadow bytes around the buggy address:
  0x0c0e801db3c0: fd fd fd fd fd fd fa fa fa fa fd fd fd fd fd fd
  0x0c0e801db3d0: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0e801db3e0: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c0e801db3f0: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
  0x0c0e801db400: fa fa fd fd fd fd fd fd fd fd fd fd fa fa fa fa
=>0x0c0e801db410: fd fd[fd]fd fd fd fd fd fd fa fa fa fa fa fd fd
  0x0c0e801db420: fd fd fd fd fd fd fd fd fa fa fa fa fd fd fd fd
  0x0c0e801db430: fd fd fd fd fd fd fa fa fa fa fd fd fd fd fd fd
  0x0c0e801db440: fd fd fd fd fa fa fa fa fd fd fd fd fd fd fd fd
  0x0c0e801db450: fd fd fa fa fa fa fd fd fd fd fd fd fd fd fd fd
  0x0c0e801db460: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fa fa
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
==487960==ABORTING


### el...@chromium.org (2021-10-25)

The ASAN stack trace (thanks!) looks exactly like https://crbug.com/chromium/1249491 - an animation completing and referencing a destroyed SharingHubBubbleController. However, 1249491 was a UAF of SharesheetBubbleView *by* SharingHubBubbleController, and its fix (a232c3e690f7db2e647c2d364afccedee7d0cdaa) landed in 96.0.4664.0, so it appears that either the fix from https://crbug.com/chromium/1249491 simply moved the UAF elsewhere, or there's a second UAF. :(

I did the fix for 1249491 and I think I remember the code so I'll take this one.

### el...@chromium.org (2021-10-25)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### kr...@chromium.org (2021-10-28)

[Empty comment from Monorail migration]

### ch...@gmail.com (2021-10-28)

Is this report qualified for reward-topanel label (as this issue is older than https://crbug.com/chromium/1264282)? 

Thanks.

### kr...@chromium.org (2021-10-28)

I believe so since the root cause is the same. Could someone from the security team verify?

### am...@google.com (2021-10-29)

We will make a note to bring this issue manually to the panel for reassessment for a potential VRP reward. (I won't add reward-topanel, as sheriffbot will just remove it since this one is marked as a duplicate.) Based on data presented in https://crbug.com/chromium/1264282, we will still need to consider that report for a potential VRP reward as well.

### am...@chromium.org (2021-11-03)

[Empty comment from Monorail migration]

### am...@google.com (2021-11-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-11-03)

Congratulations, Khalil -- the VRP Panel has decided to award you $7500 for this report. Nice finding! 

### am...@google.com (2021-11-04)

[Empty comment from Monorail migration]

### [Deleted User] (2022-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1261516?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Platform>Apps>Foundation>Sharesheet, UI>Browser>Sharing]
[Monorail mergedinto: crbug.com/chromium/1264282]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057655)*
