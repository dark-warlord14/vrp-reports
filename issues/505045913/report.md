# UAF in RenderFrameHostImpl::ExitFullscreen() — missing WeakPtr guard (variant of EnterFullscreen fix 91d5baaef742)

| Field | Value |
|-------|-------|
| **Issue ID** | [505045913](https://issues.chromium.org/issues/505045913) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>FullScreen |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | mi...@minico.ai |
| **Assignee** | jo...@chromium.org |
| **Created** | 2026-04-21 |
| **Bounty** | $2,000.00 |

## Description

# VULNERABILITY DETAILS

Use-after-free in `RenderFrameHostImpl::ExitFullscreen()` due to missing `base::WeakPtr` guard after `delegate_->ExitFullscreenMode()`. The delegate call can spin a nested message loop on Windows (via `::SetWindowPos`), during which the `RenderFrameHostImpl` can be destroyed (e.g., via `popup.close()`). The code then dereferences freed `this` via `GetOutermostMainFrame()->GetLocalRenderWidgetHost()->SynchronizeVisualProperties()`.

The identical sibling method `EnterFullscreen()` was explicitly fixed for this exact pattern in commit `91d5baaef742` (April 2, 2026), with the comment "This may spin the message loop and destroy this object." `ExitFullscreen()`, located 21 lines below in the same file, was missed.

At `content/browser/renderer_host/render_frame_host_impl.cc:9323`:

```
void RenderFrameHostImpl::ExitFullscreen() {
  base::RecordAction(base::UserMetricsAction("ExitFullscreen_API"));
  delegate_->ExitFullscreenMode(/*will_cause_resize=*/true);
  // ^^^ Can spin a nested message loop on Windows (::SetWindowPos)
  // During the loop, this RenderFrameHostImpl can be destroyed

  // NO WEAKPTR CHECK — `this` may already be freed
  GetOutermostMainFrame()                          // ← UAF HERE
      ->GetLocalRenderWidgetHost()
      ->SynchronizeVisualProperties();
}

```

Compare with the FIXED `EnterFullscreen()` at line 9300:

```
  // This may spin the message loop and destroy this object.
  // See crbug.com/1506535, crbug.com/498752242.
  base::WeakPtr<RenderFrameHostImpl> weak_ptr = GetWeakPtr();
  delegate_->EnterFullscreenMode(this, *options);
  if (!weak_ptr) {
    return;
  }

```
## Impact

This is a use-after-free in the **browser process** (unsandboxed). The `ExitFullscreen()` method is a Mojo IPC handler on `blink::mojom::LocalFrameHost`, directly callable from any renderer. The `this` pointer is the literal C++ `this`, NOT a `raw_ptr<>`.

**MiraclePtr Status: NOT PROTECTED** — confirmed in the ASAN trace. No `raw_ptr<T>` access to this region was detected. This crash is exploitable.

## ASAN Trace

```
==22092==ERROR: AddressSanitizer: heap-use-after-free on address 0x1297e5f35100
READ of size 8 at 0x1297e5f35100 thread T0
    #0 content::RenderFrameHostImpl::ExitFullscreen render_frame_host_impl.cc:9345
    #1 blink::mojom::LocalFrameHostStubDispatch::Accept frame.mojom.cc:9502
    #2 mojo::InterfaceEndpointClient::HandleValidatedMessage
    ...

freed by thread T0 here:
    #0 operator delete
    #1 content::RenderFrameHostImpl::~RenderFrameHostImpl render_frame_host_impl.cc:2844
    #2 content::RenderFrameHostManager::~RenderFrameHostManager
    #3 content::FrameTreeNode::~FrameTreeNode
    #4 content::FrameTree::~FrameTree
    #5 content::WebContentsImpl::~WebContentsImpl
    ...
    #12 content::WebContentsImpl::Close
    #13 content::RenderFrameHostImpl::ClosePageIgnoringUnloadEvents
    #14 content::RenderFrameHostImpl::RequestClose

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```

The RFHI is freed via `RequestClose` (triggered by `popup.close()` from the opener) → `WebContentsImpl::Close` → `~WebContentsImpl` → `~RenderFrameHostImpl`. Then `ExitFullscreen` dereferences the freed `this` at `GetOutermostMainFrame()`.

# VERSION

Chrome Version: 149.0.7803.0 (built from source with ASAN)
Operating System: Windows 11

Bug affects all Stable/Beta/Dev versions on Windows.

# REPRODUCTION CASE

Attached: `poc.html`, `rfhi_exit_fullscreen_runloop.patch`

The race requires the RFHI to be destroyed during the ExitFullscreen call. To widen the race window for reliable reproduction, the attached patch adds a task-pumping `base::RunLoop` in `RenderFrameHostImpl::ExitFullscreen()` between the delegate call and the `GetOutermostMainFrame()` dereference, per VRP FAQ guidance ("Use Sleep() in privileged processes to simulate a race").

Steps to reproduce:

1. Apply `rfhi_exit_fullscreen_runloop.patch` to `content/browser/renderer_host/render_frame_host_impl.cc`
2. Build Chrome with ASAN: `gn gen out/asan --args='is_asan=true is_debug=false symbol_level=1'` then `autoninja -C out/asan chrome`
3. Run: `out\asan\chrome.exe --no-sandbox --user-data-dir=<temp_dir> poc.html`
4. Click "1. Start" to open a popup window
5. Click inside the blue popup to enter fullscreen
6. Click "2. Race" in the original window
7. ASAN detects heap-use-after-free in `RenderFrameHostImpl::ExitFullscreen`

## Relationship to fixed bugs

| Method | File:Line | WeakPtr Guard? | Fixed In |
| --- | --- | --- | --- |
| `EnterFullscreen()` | render\_frame\_host\_impl.cc:9300 | **YES** | 91d5baaef742 (April 2, 2026) |
| **`ExitFullscreen()`** | **render\_frame\_host\_impl.cc:9323** | **NO** | **UNFIXED** |
| `WebContentsImpl::ExitFullscreenMode()` | web\_contents\_impl.cc:4839 | YES | 40947201 (2024) |
| `WebContentsImpl::DidNavigateAnyFramePreCommit()` | web\_contents\_impl.cc:7928 | YES | 8e95aab414bf (April 15, 2026) |
| `Navigator::DidNavigate()` | navigator.cc:528 | YES | 8e95aab414bf (April 15, 2026) |

# SUGGESTED FIX

Add a `base::WeakPtr` guard in `ExitFullscreen()`, identical to `EnterFullscreen()`:

```
void RenderFrameHostImpl::ExitFullscreen() {
  base::RecordAction(base::UserMetricsAction("ExitFullscreen_API"));
+ base::WeakPtr<RenderFrameHostImpl> weak_ptr = GetWeakPtr();
  delegate_->ExitFullscreenMode(/*will_cause_resize=*/true);
+ if (!weak_ptr) {
+   return;
+ }
  GetOutermostMainFrame()
      ->GetLocalRenderWidgetHost()
      ->SynchronizeVisualProperties();
}

```
# CREDIT INFORMATION

Reporter credit: Mihnea Nicolau

## Attachments

- [poc.html](attachments/poc.html) (text/html, 2.2 KB)
- [rfhi_exit_fullscreen_runloop.patch](attachments/rfhi_exit_fullscreen_runloop.patch) (text/x-diff, 1.1 KB)

## Timeline

### me...@google.com (2026-04-21)

jophba@: Looks like variants of this have already been reported. Was this also fixed as part of [bug 497769116](https://issues.chromium.org/issues/497769116)? If so, could you please merge this into that?

### ch...@google.com (2026-04-22)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-04-24)

Project: chromium/src  

Branch:  main  

Author:  Jordan Bayles [jophba@chromium.org](mailto:jophba@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7787660>

Fix Use-After-Free in RenderFrameHostImpl::ExitFullscreen()

---


Expand for full commit details
```
     
    The call to delegate_->ExitFullscreenMode() can synchronously destroy 
    the RenderFrameHostImpl object (e.g., if the tab is closed). 
    Subsequent calls in ExitFullscreen() then operate on the deleted object, 
    causing a Use-After-Free. 
     
    This CL adds a base::WeakPtr guard to detect if the object has been 
    destroyed and returns early if so. This is a variant of the fix for 
    EnterFullscreen in commit 91d5baaef742. 
     
    Bug: 505045913 
    Change-Id: Id2b34bea77bb80a3b6c11372cc8813a812e34a2e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7787660 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Commit-Queue: Jordan Bayles <jophba@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1620376}

```

---

Files:

- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl_unittest.cc`

---

Hash: [f2c344251df5af8f78971bb681e54b46c0513c33](https://chromiumdash.appspot.com/commit/f2c344251df5af8f78971bb681e54b46c0513c33)  

Date: Fri Apr 24 19:02:55 2026


---

### wf...@chromium.org (2026-05-05)

The yield of the UI runloop you add in your patch is not functionally equivalent to a Sleep, since it changes the order of tasks (allows other tasks to run before this current one completes), so please try and avoid using this type of POC code in future.

### sp...@google.com (2026-05-05)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Below baseline, highly mitigated


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-20)

Requesting merge to M148 because latest trunk commit is in 149.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

### ch...@google.com (2026-05-20)

**M148** merge request created. **Please update [crbug/514925169](https://crbug.com/514925169) to have this merge reviewed.**

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/505045913)*
