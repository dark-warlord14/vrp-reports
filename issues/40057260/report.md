# use after free in ash::sharesheet::SharesheetBubbleView::CloseBubble

| Field | Value |
|-------|-------|
| **Issue ID** | [40057260](https://issues.chromium.org/issues/40057260) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Sharing |
| **Platforms** | ChromeOS |
| **Reporter** | wx...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2021-09-14 |
| **Bounty** | $7,500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36

Steps to reproduce the problem:
1.I just want to test that the fixed https://crbug.com/chromium/1234050 
2.then follow my step in video.
3.

What is the expected behavior?

What went wrong?
browser crash

Did this work before? N/A 

Chrome version: 93.0.4577.82  Channel: stable
OS Version: 10.0

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 24.7 KB)
- [poc.mp4](attachments/poc.mp4) (video/mp4, 10.0 MB)
- [uaf.txt](attachments/uaf.txt) (text/plain, 69.8 KB)

## Timeline

### [Deleted User] (2021-09-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-09-14)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-09-14)

my chromium commit is 5731686672a2e8751f409a960da886f10849433b

### wx...@gmail.com (2021-09-14)

this bug is in OS-Chrome, and don't need any flags, so I think it should be set impact-head 

### wx...@gmail.com (2021-09-14)

And please also change the https://crbug.com/chromium/1234050 impact, because it doesn't need any flags,.

### wx...@gmail.com (2021-09-14)

[Comment Deleted]

### wx...@gmail.com (2021-09-14)

anather one is that I find accidentally When I try to reproduce this bug but I forgot its step. though the stack trace is a little different.

### wx...@gmail.com (2021-09-14)

[Empty comment from Monorail migration]

### ca...@chromium.org (2021-09-14)

Passing this to the Chrome OS sheriff

### do...@chromium.org (2021-09-17)

+kristipark - PTAL, my initial thought is that this appears to be some sort of dropped signal between two sharing hubs triggered by two different tabs. Let us know if the issue is in the underlying sharesheet implementation.

[Monorail components: UI>Browser>Sharing]

### [Deleted User] (2021-09-17)

[Empty comment from Monorail migration]

### wx...@gmail.com (2021-09-17)

I found just need one sharing hubs

### wx...@gmail.com (2021-09-17)

just need one  a tab with shaing hubs, move to anathor browser , then the shaing hub will disappera, then we close this tab to trigger uaf.

### [Deleted User] (2021-09-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-17)

This ReleaseBlock issue's priority is being increased in accordance with go/cros-bug-slo-guidelines#release-blockers.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-09-27)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-10-06)

The ASAN data:

Heap UAF at:
    #0 0x5596174bb497 in ash::sharesheet::SharesheetBubbleView::CloseBubble(views::Widget::ClosedReason) chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc:455:8
    #1 0x5596178b8379 in sharing_hub::SharingHubBubbleController::~SharingHubBubbleController() chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc:93:29
    #2 0x5596178b83c5 in sharing_hub::SharingHubBubbleController::~SharingHubBubbleController() chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc:84:59
...
    #20 0x55960376bff8 in content::WebContentsImpl::~WebContentsImpl() content/browser/web_contents/web_contents_impl.cc:1018:1

Free stack:
0x61b00028ee41 is located 1473 bytes inside of 1592-byte region [0x61b00028e880,0x61b00028eeb8)
freed by thread T0 (chrome) here:
    #0 0x5595fe923aed in operator delete(void*) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:152:3
    #1 0x559613034e1a in views::WidgetDelegate::DeleteDelegate() ui/views/widget/widget_delegate.cc:238:5
    #2 0x55961302a2eb in views::Widget::OnNativeWidgetDestroyed() ui/views/widget/widget.cc:1415:21
    #3 0x55961307469e in OnWindowDestroyed ui/views/widget/native_widget_aura.cc:965:14
    #4 0x55961307469e in non-virtual thunk to views::NativeWidgetAura::OnWindowDestroyed(aura::Window*) ui/views/widget/native_widget_aura.cc
    #5 0x5596116e6f68 in aura::Window::~Window() ui/aura/window.cc:226:16
    #6 0x5596116e8073 in aura::Window::~Window() ui/aura/window.cc:181:19
    #7 0x55961308ac96 in wm::TransientWindowManager::OnWindowDestroying(aura::Window*) ui/wm/core/transient_window_manager.cc:258:5
    #8 0x5596116e6d83 in aura::Window::~Window() ui/aura/window.cc:192:14

Alloc stack:
    #0 0x5595fe92328d in operator new(unsigned long) /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_new_delete.cpp:95:3
    #1 0x5596174b5113 in ash::sharesheet::SharesheetBubbleViewDelegate::SharesheetBubbleViewDelegate(aura::Window*, sharesheet::SharesheetServiceDelegate*) chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view_delegate.cc:22:11
    #2 0x55960bf19c30 in make_unique<ash::sharesheet::SharesheetBubbleViewDelegate, aura::Window *&, sharesheet::SharesheetServiceDelegate *> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:32
    #3 0x55960bf19c30 in sharesheet::SharesheetServiceDelegate::SharesheetServiceDelegate(aura::Window*, sharesheet::SharesheetService*) chrome/browser/sharesheet/sharesheet_service_delegate.cc:24:7
    #4 0x55960bf1110a in make_unique<sharesheet::SharesheetServiceDelegate, aura::Window *&, sharesheet::SharesheetService *> buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:725:32
    #5 0x55960bf1110a in sharesheet::SharesheetService::GetOrCreateDelegate(aura::Window*) chrome/browser/sharesheet/sharesheet_service.cc:345:9
    #6 0x55960bf10e7c in sharesheet::SharesheetService::ShowBubble(aura::Window*, mojo::StructPtr<apps::mojom::Intent>, bool, sharesheet::SharesheetMetrics::LaunchSource, base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>) chrome/browser/sharesheet/sharesheet_service.cc:83:39
    #7 0x55960bf10cb0 in sharesheet::SharesheetService::ShowBubble(content::WebContents*, mojo::StructPtr<apps::mojom::Intent>, bool, sharesheet::SharesheetMetrics::LaunchSource, base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>) chrome/browser/sharesheet/sharesheet_service.cc:69:3
    #8 0x55960bf10a01 in sharesheet::SharesheetService::ShowBubble(content::WebContents*, mojo::StructPtr<apps::mojom::Intent>, sharesheet::SharesheetMetrics::LaunchSource, base::OnceCallback<void (sharesheet::SharesheetResult)>, base::OnceCallback<void (views::Widget::ClosedReason)>) chrome/browser/sharesheet/sharesheet_service.cc:58:3
    #9 0x5596178b8a24 in sharing_hub::SharingHubBubbleController::ShowSharesheet(views::Button*) chrome/browser/ui/sharing_hub/sharing_hub_bubble_controller.cc:232:23

### el...@chromium.org (2021-10-06)

I think that what happened here conceptually is:

1. The CrOS share sheet dismisses & destroys itself when it observes the browser window is about to close (or by some other path)
2. The SharingHubBubbleController doesn't know the CrOS share sheet has dismissed itself and tries to close it during a later stage of window teardown

### el...@chromium.org (2021-10-06)

Ok - I believe this is a bug in the CrOS sharesheet, not in our code. Specifically, I think the bug is here:

  void SharesheetBubbleView::CloseWidgetWithReason(
      views::Widget::ClosedReason closed_reason) {
    View::GetWidget()->CloseWithReason(closed_reason);

    // Run |close_callback_| after the widget closes.
    if (close_callback_) {
      std::move(close_callback_).Run(closed_reason);
    }
    // Bubble is deleted here.
    delegate_->OnBubbleClosed(active_target_);
  }

That's how the `closed_callback_` gets run, but if the ash sharesheet is closed via teardown of the widget tree itself, that code will never be run - instead what will happen is that the ShareSheetBubbleView gets torn down "directly". I think that the best way to fix that is for the destructor of ShareSheetBubbleView to check if close_callback_ is not null and run it if so, to ensure that the client object of ShareSheetBubbleView is always notified.

I'll send a CL to fix it.

### el...@chromium.org (2021-10-06)

[Empty comment from Monorail migration]

### el...@chromium.org (2021-10-06)

Hm. In the process of trying to write a CL for #21, I discovered that, during Aura window teardown, the NativeWidget does lose activation:

#5  0x0000555567ae761e in ash::sharesheet::SharesheetBubbleViewTest::OnBubbleClosed(views::Widget::ClosedReason) ()
    at ../../chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view_unittest.cc:103
#6  0x000055557c0c8208 in Run () at ../../base/callback.h:142
#7  0x000055557c0c80cd in CloseWidgetWithReason () at ../../chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc:738
#8  0x00007fffcf0a3e50 in Run () at ../../base/callback.h:142
#9  0x00007fffcf0a3d06 in ui::ClosureAnimationObserver::OnImplicitAnimationsCompleted() ()
    at ../../ui/compositor/closure_animation_observer.cc:18
#10 0x00007fffcf1155d6 in ~ScopedLayerAnimationSettings () at ../../ui/compositor/scoped_layer_animation_settings.cc:138
#11 0x00007fffcf115836 in ui::ScopedLayerAnimationSettings::~ScopedLayerAnimationSettings() ()
    at ../../ui/compositor/scoped_layer_animation_settings.cc:125
#12 0x000055557c0c6d45 in operator() () at ../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:54
#13 reset () at ../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:315
#14 ~unique_ptr () at ../../buildtools/third_party/libc++/trunk/include/__memory/unique_ptr.h:269
#15 CloseWidgetWithAnimateFadeOut () at ../../chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc:730
#16 0x00007fffe506768d in OnNativeWidgetActivationChanged () at ../../ui/views/widget/widget.cc:1343
#17 0x00007fffe50d37f7 in views::NativeWidgetAura::OnWindowActivated(wm::ActivationChangeObserver::ActivationReason, aura::Window*, aura::Window*) () at ../../ui/views/widget/native_widget_aura.cc:1066
#18 0x00007fffe54c9059 in SetActiveWindow () at ../../ui/wm/core/focus_controller.cc:375
#19 0x00007fffe54c7b8f in WindowLostFocusFromDispositionChange () at ../../ui/wm/core/focus_controller.cc:441
#20 0x00007fffe54c7d74 in OnWindowDestroying () at ../../ui/wm/core/focus_controller.cc:166
#21 0x00007fffcf1f3f1a in ~Window () at ../../ui/aura/window.cc:194
#22 0x00007fffcf1f593a in aura::Window::~Window() () at ../../ui/aura/window.cc:183
#23 0x00007fffe506299f in CloseNow () at ../../ui/views/widget/widget.cc:715

so the theory in #21 isn't right - we do always end up going through SharesheetBubbleView::CloseWidgetWithReason, albeit via a weird path.

### el...@chromium.org (2021-10-06)

It sounds like the repro steps in #13 were:

1. In window 1, create tabs 1A & 1B
2. Open the sharing hub with tab 1B active
3. Switch to window 2, which causes the sharing hub in window 1 to dismiss
4. Switch back to window 1 and close tab 1B

### el...@chromium.org (2021-10-07)

There's something kind of suspect here, but I haven't yet figured out exactly what it is. I know that:

* aura::Window::~Window() will synthesize a focus-loss event for the window
* SharesheetBubbleView handles that loss of focus by starting an animated fadeout of the sharesheet (SharesheetBubbleView::CloseWidgetWithAnimateFadeOut)
* SharingHubBubbleController::~SharingHubBubbleController tries to call SharesheetBubbleViewDelegate::CloseBubble, which calls SharesheetBubbleView::CloseBubble()

There's this puzzling comment at the bottom of SharesheetBubbleView::CloseWidgetWithAnimateFadeOut():

  // We are closing the native widget during the close animation which results
  // in destroying the layer and the animation and the observer not calling
  // back. Thus it is safe to use base::Unretained here.
  scoped_settings->AddObserver(new ui::ClosureAnimationObserver(
      base::BindOnce(&SharesheetBubbleView::CloseWidgetWithReason,
                     base::Unretained(this), closed_reason)));

I think that *if*:

1. The SharesheetBubbleView's widget has lost focus as part of its own destruction
2. That results in SharesheetBubbleView::CloseWidgetWithAnimateFadeOut
3. While that animation is waiting to complete, SharesheetBubbleView's widget finishes destroying (destroying SharesheetBubbleView itself), and teardown of the parent tab starts
4. Teardown of the parent tab causes unloading of its WebContents, causing destruction of SharingHubBubbleController
5. Destruction of SharingHubBubbleController causes a reference to the now-destroyed SharesheetBubbleView

Since the animation from step (3) didn't complete yet, the close callback for SharesheetBubbleView was never run, so SharingHubBubbleController has no idea the SharesheetBubbleView is gone.

The main question here is what the behavior of the animation created in CloseWidgetWithAnimateFadeOut is when the widget is destroyed. It appears that LayerAnimator *doesn't* notify LayerAnimationObservers:

  void LayerAnimationSequence::OnAnimatorDestroyed() {
    for (LayerAnimationObserver& observer : observers_) {
      if (!observer.RequiresNotificationWhenAnimatorDestroyed()) {
        // Remove the observer, but do not allow notifications to be sent.
        observers_.RemoveObserver(&observer);
        observer.DetachedFromSequence(this, false);
      }
    }
  }

... but some of these classes are refcounted, so it's hard to know what the lifetimes are.

### el...@chromium.org (2021-10-07)

Here's a (possible) fix: https://chromium-review.googlesource.com/c/chromium/src/+/3212769

### me...@chromium.org (2021-10-07)

Is this the same bug as: https://crbug.com/1254648#c9?

### gi...@appspot.gserviceaccount.com (2021-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a232c3e690f7db2e647c2d364afccedee7d0cdaa

commit a232c3e690f7db2e647c2d364afccedee7d0cdaa
Author: Elly Fong-Jones <ellyjones@chromium.org>
Date: Thu Oct 07 23:54:12 2021

sharesheet: ensure close callback is run on destruction

The current theory for the linked bug is that there exist some paths
during window destruction that can lead to the close callback on
the share sheet not getting run. If it hasn't been run yet when the
sharesheet is being destroyed, run it then to ensure it is.

Bug: 1249491
Change-Id: I51ad1bcef682ed41e285b5fba187a9bb95964241
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3212769
Auto-Submit: Elly Fong-Jones <ellyjones@chromium.org>
Commit-Queue: Melissa Zhang <melzhang@chromium.org>
Reviewed-by: Melissa Zhang <melzhang@chromium.org>
Cr-Commit-Position: refs/heads/main@{#929499}

[modify] https://crrev.com/a232c3e690f7db2e647c2d364afccedee7d0cdaa/chrome/browser/ui/ash/sharesheet/sharesheet_bubble_view.cc


### el...@chromium.org (2021-10-08)

#27: I believe this is the same bug as https://crbug.com/chromium/1254648, yes.

I never had a local repro of this bug - the fix in #28 is based on reasoning from the ASAN stack trace & the code :(. Perhaps the original reporter can re-test with a build incorporating a232c3e690f7db2e647c2d364afccedee7d0cdaa?

### wx...@gmail.com (2021-10-10)

I confirm this bug has been fixed by the CL.

### me...@chromium.org (2021-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-11)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-11)

Not requesting merge to dev (M96) because latest trunk commit (929499) appears to be prior to dev branch point (929512). If this is incorrect, please replace the Merge-NA-96 label with Merge-Request-96. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-10-13)

The VRP Panel has decided to award you $7500 for this report. Thank you for this report and nice finding! 

### el...@chromium.org (2021-10-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-01-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-05-24)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1249491?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1254648]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057260)*
