# UAF in RenderFrameHostImpl::ExitFullscreen() — missing WeakPtr guard (variant of EnterFullscreen fix 91d5baaef742)

| Field | Value |
|-------|-------|
| **Issue ID** | [506684534](https://issues.chromium.org/issues/506684534) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@minico.ai |
| **Assignee** | jo...@chromium.org |
| **Created** | 2026-04-27 |
| **Bounty** | $2,000.00 |

## Description

# Use-After-Free in WebContentsImpl::SetWindowRect via ForSecurityDropFullscreen

## Summary

`WebContentsImpl::SetWindowRect()` calls `ForSecurityDropFullscreen()` which internally calls `ExitFullscreen()` on other WebContents. On Windows, this can spin a nested message loop via `::SetWindowPos`. During this nested loop, the calling WebContents can be destroyed (e.g., via `window.close()` from a popup's `fullscreenchange` handler). The subsequent call to `delegate_->SetContentsBounds(this, bounds)` then reads from the freed WebContentsImpl object.

This is a variant of my earlier report, [Bug 505045913](https://issues.chromium.org/issues/505045913) (UAF in `RenderFrameHostImpl::ExitFullscreen`). That fix added a WeakPtr guard in ExitFullscreen, but the same nested message loop race exists in `SetWindowRect` via `ForSecurityDropFullscreen` and was not addressed.

## Version

Chrome 149.0.7805.0, Windows x64, ASAN build (`is_asan=true is_debug=false symbol_level=1`)

## Steps to Reproduce

1. Build Chrome with ASAN
2. Apply `patch.diff` (RunLoop simulating `::SetWindowPos` nested message loop)
3. Launch: `chrome --no-sandbox poc.html`
4. Click **Start** — a popup opens
5. Click the popup body — it enters fullscreen, opener auto-resizes
6. ASAN reports heap-use-after-free in `SetWindowRect`

## Root Cause

`content/browser/web_contents/web_contents_impl.cc`:

```
void WebContentsImpl::SetWindowRect(const gfx::Rect& new_bounds) {
  // ...
  ForSecurityDropFullscreen(display_id).RunAndReset();  // [1]
  delegate_->SetContentsBounds(this, bounds);            // [2]
}

```

[1] `ForSecurityDropFullscreen` iterates fullscreen WebContents and calls `ExitFullscreen()` on each. On Windows, `ExitFullscreen` → `ExitFullscreenMode` → `::SetWindowPos` spins a nested message loop. During this loop, Mojo IPCs are processed — including `RequestClose` from the popup's `fullscreenchange` handler calling `opener.close()` — destroying this WebContents.

[2] `delegate_->SetContentsBounds(this, bounds)` reads `this->delegate_` from the freed 5592-byte WebContentsImpl allocation.

The ExitFullscreen fix ([Bug 505045913](https://issues.chromium.org/issues/505045913)) added a WeakPtr guard in `RenderFrameHostImpl::ExitFullscreen()`, but `SetWindowRect` reaches the same nested message loop via `ForSecurityDropFullscreen` without any guard.

## ASAN Trace

```
==17584==ERROR: AddressSanitizer: heap-use-after-free on address 0x1218f580c210
READ of size 8 at 0x1218f580c210 thread T0
    #0 in content::WebContentsImpl::SetWindowRect web_contents_impl.cc:9737
    #1 in content::RenderFrameHostImpl::SetWindowRect render_frame_host_impl.cc:7809

freed by thread T0 here:
    #0 in operator delete
    #1 in content::WebContentsImpl::~WebContentsImpl web_contents_impl.cc:1370
    #7 in content::WebContentsImpl::Close web_contents_impl.cc:9699
    #8 in content::RenderFrameHostImpl::ClosePageIgnoringUnloadEvents render_frame_host_impl.cc:7769

MiraclePtr Status: NOT PROTECTED
This crash is still exploitable with MiraclePtr.

```
## Patch Explanation

`patch.diff` adds a `base::RunLoop` pump between `ForSecurityDropFullscreen()` and `SetContentsBounds()`. This simulates the natural race from the `::SetWindowPos` nested message loop on Windows, allowing the pending `RequestClose` Mojo IPC to execute and destroy the WebContents.

## Suggested Fix

`fix.diff` adds a `base::WeakPtr` guard after `ForSecurityDropFullscreen()`, matching the pattern from the ExitFullscreen fix ([Bug 505045913](https://issues.chromium.org/issues/505045913)):

```
base::WeakPtr<WebContentsImpl> weak_this = weak_factory_.GetWeakPtr();
ForSecurityDropFullscreen(display_id).RunAndReset();
if (!weak_this) {
  return;
}
delegate_->SetContentsBounds(this, bounds);

```

Reporter Credit: Mihnea Nicolau

## Attachments

- [fix.diff](attachments/fix.diff) (text/x-diff, 917 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 791 B)
- [poc.html](attachments/poc.html) (text/html, 367 B)
- [popup.html](attachments/popup.html) (text/html, 390 B)

## Timeline

### da...@google.com (2026-04-29)

Triaging based on [issue 505045913](https://issues.chromium.org/issues/505045913). jophba, was this fixed as part of that bug, or is this separate?

### ch...@google.com (2026-04-30)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-30)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-05-07)

Project: chromium/src  

Branch:  main  

Author:  Jordan Bayles [jophba@chromium.org](mailto:jophba@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7818866>

content: Prevent UAF in WebContentsImpl related to drop fullscreen

---


Expand for full commit details
```
     
    ForSecurityDropFullscreen can synchronously destroy the WebContentsImpl 
    object. This CL updates ForSecurityDropFullscreen() to return a 
    std::optional<base::ScopedClosureRunner> that is std::nullopt if `this` 
    was destroyed, forcing callers to handle it explicitly. 
     
    Affected methods: 
    - ShowCreatedWindow 
    - ViewSource 
    - EnumerateDirectory 
    - RunJavaScriptDialog 
    - RunBeforeUnloadConfirm 
    - RunFileChooser 
    - SetWindowRect 
    - DidCallFocus 
     
    Bug: 506684534 
    Change-Id: Ieb700f4d5f3785adc6360f8c6c2f637be769be5d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7818866 
    Commit-Queue: Jordan Bayles <jophba@chromium.org> 
    Reviewed-by: Avi Drissman <avi@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1627248}

```

---

Files:

- M `chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc`
- M `chrome/browser/renderer_context_menu/render_view_context_menu.cc`
- M `chrome/browser/ui/browser.cc`
- M `chrome/browser/ui/views/media_router/media_router_dialog_controller_views.cc`
- M `chrome/browser/ui/views/permissions/chooser_bubble_ui.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_bubble.cc`
- M `chrome/browser/webshare/share_service_impl.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl.h`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/public/browser/web_contents.h`

---

Hash: [058c2d6ea49cf80034fe78cfdb88cf24be7435de](https://chromiumdash.appspot.com/commit/058c2d6ea49cf80034fe78cfdb88cf24be7435de)  

Date: Thu May 7 21:39:57 2026


---

### mi...@gmail.com (2026-05-10)

Hi Chrome VRP team,

I wanted to add a note about the PoC approach used here. This is similar to what I used in my earlier report, https://issues.chromium.org/u/1/issues/505045913, where I added a UI runloop yield to make the lifetime issue easier to reproduce.

Thank you for the clarification on that report. I understand now that yielding the UI runloop is not the same as Sleep, since it can change task ordering by allowing other tasks to run before the current task completes.

Sorry for repeating that pattern here. For future reports, I’ll avoid using UI runloop yielding in PoC patches and follow the VRP guidance more closely, including using Sleep() in privileged processes when simulating races.

Also, before any reward processing, I wanted to flag that I accidentally submitted this report from my personal Gmail instead of the email tied to my Bugcrowd account. If this report is reward-eligible, could the reward please be associated with my Bugcrowd account at:

mihnea.nicolau@minico.ai

I’m marking this comment as Restricted because it includes account/payment routing information.

Thank you, and sorry for the inconvenience.

### wf...@chromium.org (2026-05-12)

reporter: do not post restricted comments to issues. This violates the VRP rules where all reports will be public.

### wf...@chromium.org (2026-05-12)

reporter: spinning a nested runloop in your patch is not the same as a sleep, since it causes tasks to run in a different order. Please submit the patch with just a sleep that causes the current task to pause.

### sp...@google.com (2026-05-13)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

Lacking proof (including unusable patch) without ASAN trace.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925767](https://crbug.com/514925767) to have this merge reviewed.**

### ch...@google.com (2026-05-20)

**M149** merge request created. **Please update [crbug/514927486](https://crbug.com/514927486) to have this merge reviewed.**

### dx...@google.com (2026-06-02)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  Jordan Bayles [jophba@chromium.org](mailto:jophba@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7885917>

[M149] content: Prevent UAF in WebContentsImpl related to drop fullscreen

---


Expand for full commit details
```
     
    Original change's description: 
    > content: Prevent UAF in WebContentsImpl related to drop fullscreen 
    > 
    > ForSecurityDropFullscreen can synchronously destroy the WebContentsImpl 
    > object. This CL updates ForSecurityDropFullscreen() to return a 
    > std::optional<base::ScopedClosureRunner> that is std::nullopt if `this` 
    > was destroyed, forcing callers to handle it explicitly. 
    > 
    > Affected methods: 
    > - ShowCreatedWindow 
    > - ViewSource 
    > - EnumerateDirectory 
    > - RunJavaScriptDialog 
    > - RunBeforeUnloadConfirm 
    > - RunFileChooser 
    > - SetWindowRect 
    > - DidCallFocus 
    > 
    > Bug: 506684534 
    > Change-Id: Ieb700f4d5f3785adc6360f8c6c2f637be769be5d 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7818866 
    > Commit-Queue: Jordan Bayles <jophba@chromium.org> 
    > Reviewed-by: Avi Drissman <avi@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1627248} 
     
    (cherry picked from commit 058c2d6ea49cf80034fe78cfdb88cf24be7435de) 
     
    Bug: 514927486,506684534 
    Change-Id: Ieb700f4d5f3785adc6360f8c6c2f637be769be5d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7885917 
    Reviewed-by: Thomas Guilbert <tguilbert@chromium.org> 
    Commit-Queue: Jordan Bayles <jophba@chromium.org> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7827@{#2337} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc`
- M `chrome/browser/renderer_context_menu/render_view_context_menu.cc`
- M `chrome/browser/ui/browser.cc`
- M `chrome/browser/ui/views/media_router/media_router_dialog_controller_views.cc`
- M `chrome/browser/ui/views/permissions/chooser_bubble_ui.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_bubble.cc`
- M `chrome/browser/webshare/share_service_impl.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl.h`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/public/browser/web_contents.h`

---

Hash: [edd1b93b5ea1f6534a0cf57fcd43baae3e7570a1](https://chromiumdash.appspot.com/commit/edd1b93b5ea1f6534a0cf57fcd43baae3e7570a1)  

Date: Tue Jun 2 23:40:09 2026


---

### dx...@google.com (2026-06-23)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Jordan Bayles [jophba@chromium.org](mailto:jophba@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7953520>

[M148] content: Prevent UAF in WebContentsImpl related to drop fullscreen

---


Expand for full commit details
```
[M148] content: Prevent UAF in WebContentsImpl related to drop fullscreen

This was not a clean cherry pick due to some merge conflicts due to
https://chromium-review.git.corp.google.com/c/chromium/src/+/7756827 not
being cherry picked to M148, which originally added the fullscreen
blocker class to the media router dialog view.

Original change's description:
> content: Prevent UAF in WebContentsImpl related to drop fullscreen
>
> ForSecurityDropFullscreen can synchronously destroy the WebContentsImpl
> object. This CL updates ForSecurityDropFullscreen() to return a
> std::optional<base::ScopedClosureRunner> that is std::nullopt if `this`
> was destroyed, forcing callers to handle it explicitly.
>
> Affected methods:
> - ShowCreatedWindow
> - ViewSource
> - EnumerateDirectory
> - RunJavaScriptDialog
> - RunBeforeUnloadConfirm
> - RunFileChooser
> - SetWindowRect
> - DidCallFocus
>
> Bug: 506684534
> Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7818866
> Commit-Queue: Jordan Bayles <jophba@chromium.org>
> Reviewed-by: Avi Drissman <avi@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#1627248}

(cherry picked from commit 058c2d6ea49cf80034fe78cfdb88cf24be7435de)
https://chromium-review.git.corp.google.com/c/chromium/src/+/7818866

Bug: 506684534
Fixed: 514925767
Change-Id: Iff61aad85be7487fe1ef29ce887a25c0825c8f7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7953520
Reviewed-by: Ted (Chromium) Meyer <tmathmeyer@chromium.org>
Reviewed-by: Avi Drissman <avi@chromium.org>
Reviewed-by: Thomas Lukaszewicz <tluk@chromium.org>
Commit-Queue: Jordan Bayles <jophba@chromium.org>
Cr-Commit-Position: refs/branch-heads/7778@{#4410}
Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `chrome/browser/file_system_access/chrome_file_system_access_permission_context.cc`
- M `chrome/browser/renderer_context_menu/render_view_context_menu.cc`
- M `chrome/browser/ui/browser.cc`
- M `chrome/browser/ui/views/media_router/media_router_dialog_controller_views.cc`
- M `chrome/browser/ui/views/media_router/media_router_dialog_controller_views.h`
- M `chrome/browser/ui/views/permissions/chooser_bubble_ui.cc`
- M `chrome/browser/ui/views/permissions/permission_prompt_bubble.cc`
- M `chrome/browser/webshare/share_service_impl.cc`
- M `content/browser/file_system_access/file_system_access_manager_impl.cc`
- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl.h`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/public/browser/web_contents.h`

---

Hash: [3c6f02e2a861383500b7edc38dabf9898e719e84](https://chromiumdash.appspot.com/commit/3c6f02e2a861383500b7edc38dabf9898e719e84)  

Date: Tue Jun 23 02:03:23 2026


---

### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506684534)*
