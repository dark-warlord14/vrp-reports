# Security: heap-use-after-free on aura::Window::CleanupGestureState

| Field | Value |
|-------|-------|
| **Issue ID** | [432497641](https://issues.chromium.org/issues/432497641) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Input |
| **Platforms** | Windows |
| **Reporter** | xp...@gmail.com |
| **Assignee** | ga...@microsoft.com |
| **Created** | 2025-07-17 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

Hello,

As I was investigating this user's bug, [370856871](https://issues.chromium.org/issues/370856871), I discovered a UAF.

# Steps to reproduce:

1: Apply patch.diff. Patch mimics a compromised renderer/touch screen user.
2: In your browser, navigate to poc.html (make sure your cursor is within the page).

# Bisect:

<https://chromium-review.googlesource.com/c/chromium/src/+/6574862>

# Root Cause:

What I believe is happening is that `::DoDragDrop` enters a message loop on the current thread when a user initiates a drag operation [1](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc;drc=5b9155c665a4d35b52fd6c5b61421d23a326a875;l=84):

```
  HRESULT result = ::DoDragDrop(
      ui::OSExchangeDataProviderWin::GetIDataObject(*data.get()),
      drag_source_.Get(),
      ui::DragDropTypes::DragOperationToDropEffect(allowed_operations),
      &effect);

```

While a user is dragging, the process associated with the `view` can die/crash for the current `Widget`. This causes the the `View` to call `view_->RenderProcessGone();`[2](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_impl.cc;drc=cc69c44b7132de8755c22cd3d31bd15eb5a2c016;l=2253):

```
void RenderWidgetHostImpl::RendererExited() {
  ...

  if (view_) {
    view_->RenderProcessGone();
    SetView(nullptr);  // The View should be deleted by RenderProcessGone.
  }
}

```

`view_->RenderProcessGone();` will go on to delete the current window for the widget/view through `RenderWidgetHostViewAura::Destroy()` [3](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/render_widget_host_view_aura.cc;drc=e220311b8860464fe96844d7107367473e413a10;l=964):

```
void RenderWidgetHostViewAura::Destroy() {
  // Beware, this function is not called on all destruction paths. If |window_|
  // has been created, then it will implicitly end up calling
  // ~RenderWidgetHostViewAura when |window_| is destroyed. Otherwise, The
  // destructor is invoked directly from here. So all destruction/cleanup code
  // should happen there, not here.
  in_shutdown_ = true;
  // Call this here in case any observers need access to `this` before we
  // destruct the derived class.
  NotifyObserversAboutShutdown();

  if (window_)
    delete window_;
  else
    delete this;
}

```

The exit of the renderer causes the user to drop the currently dragged `widget` and thus exit the message loop caused by `::DoDragDrop`. We will reenter the stack frame from which `::DoDragDrop` was called.

Just below `::DoDragDrop`, use-after-free occurs when accessing the now deleted window and accessing a member variable for the object within the function `Window::CleanupGestureState()` [4](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc;drc=5b9155c665a4d35b52fd6c5b61421d23a326a875;l=92), [5](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window.cc;drc=d0260a368e65b2be56d179d21fab90976fd494b8;l=1344):

```
ui::mojom::DragOperation DesktopDragDropClientWin::StartDragAndDrop(
    ...) {
  
  ...
  
  HRESULT result = ::DoDragDrop(
      ui::OSExchangeDataProviderWin::GetIDataObject(*data.get()),
      drag_source_.Get(),
      ui::DragDropTypes::DragOperationToDropEffect(allowed_operations),
      &effect);
  if (source == ui::mojom::DragEventSource::kTouch) {
    // Kill the gesture that initiated the drag to avoid issues with lingering
    // touch events.
    source_window->CleanupGestureState(); // Exec func on now deleted window [4]
    if (alive) {
      desktop_host_->FinishTouchDrag(touch_screen_point);
    }
  }

  ...
}

bool Window::CleanupGestureState() { // [5]
  // If it's in the process already, clean up the consumer state. Reentrant can
  // happen through some event handlers for CancelActiveTouches().
  Env* env = Env::GetInstance();
  if (cleaning_up_gesture_state_) { // [ UAF! ]
    return env->gesture_recognizer()->CleanupStateForConsumer(this);
  }

  ...
}

```
# Security Impact:

A renderer crash during an active drag-n-drop operation triggers a use-after-free in Window::CleanupGestureState(). This vulnerability can be exploited by an attacker-controlled renderer or through an OOM/rendererc crash scenario, resulting in memory corruption and potentially arbitrary code execution within the browser process, furthermore facilitating a sandbox escape.

# Additional Notes:

**1:** This can be triggered without a renderer patch if the user is using a device with touch e.g. kiosk mode at a caffe, tablet with touch screen, art tablet, etc. and then crashing the page while the user is dragging via OOM.

**2:** The provided patch.diff makes changes to the browser code, however this is done to mimic the normal flow of a touch user. Otherwise, a comprimised renderer can spoof this as demonstrated in [370856871](https://issues.chromium.org/issues/370856871).

# Problem Description



# Additional Comments



# Summary

Security: heap-use-after-free on aura::Window::CleanupGestureState

# Custom Questions

#### Type of crash:

browser

#### Crash state:



#### Reporter credit:

Sven Dysthe @svn\_dy

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: Yes \

## Attachments

- asan.txt (text/plain, 19.5 KB)
- patch.diff (text/x-diff, 5.0 KB)
- poc.html (text/html, 451 B)
- poc_uaf_reproduction.mp4 (video/mp4, 31.9 MB)

## Timeline

### xi...@chromium.org (2025-07-17)

Thanks for the report. I didn't reproduce it because I don't have a windows machine, but the analysis and the video look convincing. Assigning to the original CL author to take a look. Setting severity to S2 since this is memory corruption in renderer process that requires drag and drop.

### xp...@gmail.com (2025-07-17)

Re #2:

Thanks for triaging!

Small correction to "memory corruption in renderer process". I believe the crash is in the browser process. 1 click if on a touch deivce (dragging something), 0 click through a compromised renderer as demonstrated in `patch.diff`.

Thank you.

### da...@chromium.org (2025-07-17)

I think it's the render process that has crashed in this scenario, leading to memory corruption/UAF in the browser process. There is only one browser process, and if it crashes, there won't be any UAF.

Aura windows don't support weak references, that I can see, so i don't think we can determine if this has happened just by looking at the window object.



### xp...@gmail.com (2025-07-17)

Sorry, I meant the memory corruption (UAF) is in the browser process not the renderer process like #2 stated.

You're right, the crash **causing** the memory corruption in the browser occurs in the renderer (my patch purposely does this).

### ch...@google.com (2025-07-18)

Setting milestone because of s2 severity.

### ch...@google.com (2025-07-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ch...@google.com (2025-07-18)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### da...@chromium.org (2025-07-18)

> The provided patch.diff makes changes to the browser code, however this is done to mimic the normal flow of a touch user. Otherwise, a comprimised renderer can spoof this as demonstrated in 370856871.

If I understand this correctly, this is no longer the case. The user does have to have to have touch down in order for the touch drag code to be invoked, otherwise we don't start the drag:
    if (touch_drag_cursor_sync && (!touch_down || touch_over_other_window)) {
      return ui::PreferredDragOperation(
          ui::DragDropTypes::DropEffectToDragOperation(DROPEFFECT_NONE));
    }

 The first scenario does apply, where the user is actually doing a touch drag.

### xp...@gmail.com (2025-07-18)

Re #9: That's true. Apologies, I missed that.

We would enter `if (source == ui::mojom::DragEventSource::kTouch)` and return on

```
return ui::PreferredDragOperation(
          ui::DragDropTypes::DropEffectToDragOperation(DROPEFFECT_NONE));

```

A real touch device device event would be needed to trigger this UAF.

### ga...@microsoft.com (2025-07-21)

Thanks for reporting this, I'm taking a look and will put up a patch shortly.

### da...@chromium.org (2025-07-21)

@gastonr, thanks. One possibility is to have the drag drop client be a window observer, so it would get notified if/when the source_window is deleted.

### dx...@google.com (2025-07-25)

Project: chromium/src  

Branch:  main  

Author:  Gastón Rodríguez [gastonr@microsoft.com](mailto:gastonr@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6779234>

Make DesktopDragDropClientWin a Window observer to avoid UAF

---


Expand for full commit details
```
     
    If the renderer process crashes while a drag and drop is happening, the 
    Window object for the source_window in 
    DesktopDragDropClientWin::StartDragAndDrop will be freed. When the drag 
    and drop is finished, the function will try to access the freed object, 
    causing a use after free exception. 
     
    This CL fixes this issue by temporarily adding the drag and drop client 
    as an observer of the Window. The Window will notify it's observers when 
    it's being destroyed, and with this we can avoid accessing the freed 
    object. 
     
    I was able to reproduce the crash following the steps in the linked 
    bug, and stopped observing after the changes in this CL were 
    implemented. 
     
    Bug: 432497641 
    Change-Id: Ic05aadcd9005c9f5eb8b660a7d5a182b859e62eb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6779234 
    Reviewed-by: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Robert Liao <robliao@chromium.org> 
    Commit-Queue: Gaston Rodriguez <gastonr@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1492096}

```

---

Files:

- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: [a4c579c9a8e4e05f3b3ec012c40cb36c6ae89e11](http://crrev.com/a4c579c9a8e4e05f3b3ec012c40cb36c6ae89e11)  

Date: Fri Jul 25 16:08:49 2025


---

### xp...@gmail.com (2025-07-28)

Good evening,

On my side, the patch fixes the UAF 💯. If there isn't additional work to be done, could you please close this issue as fixed?

Thank you.

### ga...@microsoft.com (2025-07-29)

Thanks for reporting and verifying, Sven!

### ch...@google.com (2025-07-29)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M139. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [139].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ga...@microsoft.com (2025-07-29)

1. **Which CLs should be backmerged?** Only the CL with the fix: <https://chromium-review.googlesource.com/c/chromium/src/+/6779234> The original CL that introduced the issue was merged on May 30th, which means it made it into 139 and does not need to be cherry picked.
2. **Has this fix been verified on Canary to not pose any stability regressions?** The change has been in canary for 4 days, and I couldn't find any item open related to it.
3. **Does this fix pose any potential non-verifiable stability risks?** I don't think so. The conditions on which this issue is reproduced are very specific, and hidden behind a disabled-by-default feature flag (TouchDragAndDrop)
4. **Does this fix pose any known compatibility risks?** No.
5. **Does it require manual verification by the test team? If so, please describe required testing.** Reproducing this issue requires crashing the renderer process while a touch drag and drop happens, I don't know of a way to reliably crash it for us to test this repro.

### da...@chromium.org (2025-07-29)

https://issues.chromium.org/issues/432497641#comment13 has the Chromium repo commit.

### pg...@google.com (2025-07-31)

139 Merge approved for <https://chromium-review.googlesource.com/c/chromium/src/+/6779234>! Nothing relevant in canary as far as I can tell. Although I am usually hesitant to backmerge UI impacting fixes since canary can be less useful to rely on, this change is short and resoves a release blocker.

please merge asap to branch 7258 to attempt to get this fix in the next 139 release!

### ch...@google.com (2025-08-04)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-05)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ga...@microsoft.com (2025-08-06)

Disabling nags and won't CP to 139 until <https://issues.chromium.org/issues/435623339> is addressed. A [CL is already up](https://chromium-review.googlesource.com/c/chromium/src/+/6821521).

### dx...@google.com (2025-08-07)

Project: chromium/src  

Branch:  main  

Author:  Gastón Rodríguez [gastonr@microsoft.com](mailto:gastonr@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6821521>

Reset DragDrop window observator to avoid UAF

---


Expand for full commit details
```
     
    CL:6779234 introduced a scoped observation to avoid calling the window 
    after it had been freed when a drag and drop was ongoing. This fix 
    introduced another UAF in a similar scenario; when the 
    ScopedObservation is being deleted it attempts to access the window to 
    remove itself as an observer. If the window has been deleted, then a 
    UAF happens. This CL calls Reset on the ScopedObserver when the window 
    is destroyed to avoid this call after the fact. 
     
    Steps to repro: 
    1. Open the HTML linked in the crbug in an ASAN build. 
    2. Click the button that says "Open new tab with draggable element" 
    3. On the new tab, drag the red square and hold the drag for a second. 
     
    The window should close, and you should see the UAF stack trace on the 
    console. After this patch, this problem is gone. 
     
    Bug: 435623339, 432497641 
    Change-Id: Ie0d54d6c07834cbc305e126156e7e23d92283c01 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6821521 
    Reviewed-by: David Bienvenu <davidbienvenu@chromium.org> 
    Commit-Queue: Gaston Rodriguez <gastonr@microsoft.com> 
    Reviewed-by: Dana Fried <dfried@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1498283}

```

---

Files:

- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: [52f3b7419bc8892f011643006a1a075b5a7a9c82](http://crrev.com/52f3b7419bc8892f011643006a1a075b5a7a9c82)  

Date: Thu Aug 7 16:23:45 2025


---

### ga...@microsoft.com (2025-08-07)

I will let this CL ([#24](https://issues.chromium.org/issues/432497641#comment24)) sit in Canary for the weekend, and then add it to the CP to 139 <https://chromium-review.googlesource.com/c/chromium/src/+/6816386> on Monday.

### sr...@chromium.org (2025-08-11)

@ga...@microsoft.com, Please land this CL to M139 asap ( i am cutting RC for respin today and this is one of the last pending bugs in approved queue)

### ga...@microsoft.com (2025-08-11)

Added to commit queue, should be merged soon. Created the CP for the follow-up as well.

### dx...@google.com (2025-08-11)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Gastón Rodríguez [gastonr@microsoft.com](mailto:gastonr@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6816386>

[CP-139] Make DesktopDragDropClientWin a Window observer to avoid UAF

---


Expand for full commit details
```
     
    This CL is a cherry-pick to M139 of CL:6779234 as requested in the 
    linked crbug. 
     
    If the renderer process crashes while a drag and drop is happening, the 
    Window object for the source_window in 
    DesktopDragDropClientWin::StartDragAndDrop will be freed. When the drag 
    and drop is finished, the function will try to access the freed object, 
    causing a use after free exception. 
     
    This CL fixes this issue by temporarily adding the drag and drop client 
    as an observer of the Window. The Window will notify it's observers when 
    it's being destroyed, and with this we can avoid accessing the freed 
    object. 
     
    I was able to reproduce the crash following the steps in the linked bug, 
    and stopped observing after the changes in this CL were implemented. 
     
    (cherry picked from commit a4c579c9a8e4e05f3b3ec012c40cb36c6ae89e11) 
     
    Bug: 432497641 
    Change-Id: Ic05aadcd9005c9f5eb8b660a7d5a182b859e62eb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6779234 
    Reviewed-by: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Robert Liao <robliao@chromium.org> 
    Commit-Queue: Gaston Rodriguez <gastonr@microsoft.com> 
    Cr-Original-Commit-Position: refs/heads/main@{#1492096} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6816386 
    Cr-Commit-Position: refs/branch-heads/7258@{#2568} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: [7e194ceae03dd45790d663d5c114d645390f0436](https://chromiumdash.appspot.com/commit/7e194ceae03dd45790d663d5c114d645390f0436)  

Date: Mon Aug 11 17:48:53 2025


---

### da...@chromium.org (2025-08-11)

@ga...@microsoft.com, did you include the .Reset() in OnWindowDestroying part of the fix for m139? If not, that should be CP'd as well.

### ga...@microsoft.com (2025-08-11)

I didn’t include that change because it’s part of a different bug, and its corresponding CP to 139 hasn’t been approved yet. Since the task is still pending, I wasn’t sure if it would’ve been appropriate to include it in this task's CP. [The CL](https://chromium-review.googlesource.com/c/chromium/src/+/6837176) is ready to land as soon as it gets a +1, barring the need for the tasks' approval.

### da...@chromium.org (2025-08-11)

I see - IMO opinion, it would have been better to CP the "complete" fix, a little less churn...but we just need to make sure that the other CP gets included before 139 is respun.

### da...@chromium.org (2025-08-11)

@sr...@google.com, 139 shouldn't go out with just  https://chromium-review.googlesource.com/6816386 - https://chromium-review.googlesource.com/c/chromium/src/+/6821521 should also be cherry-picked into 139 as well.

### sr...@chromium.org (2025-08-11)

i chatted with @am...@chromium.org and she is approving the second bug, will get the second CL merged for respin as well

### ga...@microsoft.com (2025-08-11)

Thanks for handling this and getting the second CL approved.

### dx...@google.com (2025-08-11)

Project: chromium/src  

Branch:  refs/branch-heads/7258  

Author:  Gastón Rodríguez [gastonr@microsoft.com](mailto:gastonr@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6837176>

[CP-139] Reset DragDrop window observator to avoid UAF

---


Expand for full commit details
```
     
    Follow up to CL:6816386 
    ---- 
     
    CL:6779234 introduced a scoped observation to avoid calling the window 
    after it had been freed when a drag and drop was ongoing. This fix 
    introduced another UAF in a similar scenario; when the 
    ScopedObservation is being deleted it attempts to access the window to 
    remove itself as an observer. If the window has been deleted, then a 
    UAF happens. This CL calls Reset on the ScopedObserver when the window 
    is destroyed to avoid this call after the fact. 
     
    Steps to repro: 
    1. Open the HTML linked in the crbug in an ASAN build. 
    2. Click the button that says "Open new tab with draggable element" 
    3. On the new tab, drag the red square and hold the drag for a second. 
     
    The window should close, and you should see the UAF stack trace on the 
    console. After this patch, this problem is gone. 
     
    (cherry picked from commit 52f3b7419bc8892f011643006a1a075b5a7a9c82) 
     
    Bug: 435623339, 432497641 
    Change-Id: Ie0d54d6c07834cbc305e126156e7e23d92283c01 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6821521 
    Reviewed-by: David Bienvenu <davidbienvenu@chromium.org> 
    Commit-Queue: Gaston Rodriguez <gastonr@microsoft.com> 
    Reviewed-by: Dana Fried <dfried@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1498283} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6837176 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7258@{#2576} 
    Cr-Branched-From: f600d0656fd5b5fe4a82981f533d31ed6939e2e4-refs/heads/main@{#1477651}

```

---

Files:

- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: [a4b90faf56bcf4c0b94ba071f6fd8615435a3f21](https://chromiumdash.appspot.com/commit/a4b90faf56bcf4c0b94ba071f6fd8615435a3f21)  

Date: Mon Aug 11 20:56:16 2025


---

### sp...@google.com (2025-08-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of mildly mitigated memory corruption in a non-sandboxed process 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### dx...@google.com (2025-08-13)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Gastón Rodríguez [gastonr@microsoft.com](mailto:gastonr@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/6834701>

[CP-140] Reset DragDrop window observator to avoid UAF

---


Expand for full commit details
```
     
    CL:6779234 introduced a scoped observation to avoid calling the window 
    after it had been freed when a drag and drop was ongoing. This fix 
    introduced another UAF in a similar scenario; when the 
    ScopedObservation is being deleted it attempts to access the window to 
    remove itself as an observer. If the window has been deleted, then a 
    UAF happens. This CL calls Reset on the ScopedObserver when the window 
    is destroyed to avoid this call after the fact. 
     
    Steps to repro: 
    1. Open the HTML linked in the crbug in an ASAN build. 
    2. Click the button that says "Open new tab with draggable element" 
    3. On the new tab, drag the red square and hold the drag for a second. 
     
    The window should close, and you should see the UAF stack trace on the 
    console. After this patch, this problem is gone. 
     
    (cherry picked from commit 52f3b7419bc8892f011643006a1a075b5a7a9c82) 
     
    Bug: 435623339, 432497641 
    Change-Id: Ie0d54d6c07834cbc305e126156e7e23d92283c01 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6821521 
    Reviewed-by: David Bienvenu <davidbienvenu@chromium.org> 
    Commit-Queue: Gaston Rodriguez <gastonr@microsoft.com> 
    Reviewed-by: Dana Fried <dfried@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1498283} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6834701 
    Reviewed-by: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Robert Liao <robliao@chromium.org> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7339@{#548} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc`

---

Hash: [d11868c4f84180831069011ec0e11cef3ba0c883](https://chromiumdash.appspot.com/commit/d11868c4f84180831069011ec0e11cef3ba0c883)  

Date: Wed Aug 13 22:44:13 2025


---

### xp...@gmail.com (2025-08-14)

Hi Amy,

Does this issue qualify for the bisect bonus?

Best,

Sven

### am...@chromium.org (2025-08-21)

Hi Sven, it does look like the bisect was used here in triage and that we did not account for that in our reward decision. We'll take a look at the next VRP panel session.

### sp...@google.com (2025-09-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Additional $1,000 bisect bonus (apologies for the delay!)


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### xp...@gmail.com (2025-09-04)

Thank you for the reward. I wish you the best on your new endeavors amy@.

### ch...@google.com (2025-11-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of mildly mitigated memory corruption in a non-sandboxed process

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/432497641)*
