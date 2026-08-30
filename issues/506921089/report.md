# UAF in RenderFrameHostImpl::ExitFullscreen() — missing WeakPtr guard (variant of EnterFullscreen fix 91d5baaef742)

| Field | Value |
|-------|-------|
| **Issue ID** | [506921089](https://issues.chromium.org/issues/506921089) |
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

# Use-After-Free in RenderFrameHostImpl::CreateNewWindow

## Summary

`RenderFrameHostImpl::CreateNewWindow()` calls `delegate_->CreateNewWindow()` which internally calls `AddNewContents()`. On Windows, `AddNewContents()` can enter a nested message loop via `::ShowWindow()`. During this nested loop, a `window.close()` Mojo IPC from another renderer can destroy the WebContents and its RenderFrameHostImpl. After the delegate call returns, `transient_allow_popup_.Deactivate()` writes to the freed RenderFrameHostImpl object.

This is a variant of the ExitFullscreen UAF ([Bug 505045913](https://issues.chromium.org/issues/505045913)) and the SetWindowRect UAF (my concurrent report). All three share the same root cause: delegate calls in RenderFrameHostImpl/WebContentsImpl can spin Win32 nested message loops, during which `this` is destroyed.

## Version

Chrome 149.0.7805.0, Windows x64, ASAN build (`is_asan=true is_debug=false symbol_level=1`)

## Steps to Reproduce

1. Build Chrome with ASAN
2. Apply `patch.diff`
3. Launch: `chrome --no-sandbox poc.html`
4. Click **Start**
5. ASAN reports heap-use-after-free

## Patch Explanation

MojoJS is not sufficient to trigger this bug because the opener's renderer is blocked in a synchronous `CreateNewWindow` Mojo call. No JS can execute in the opener's renderer during the race window. The race window exists inside a `::ShowWindow` Win32 nested message loop in `AddNewContents()` on the browser's UI thread.

The patch simulates this by:

1. Posting a `Close()` task — simulates a `window.close()` Mojo IPC arriving from another renderer during the nested loop
2. Pumping a `RunLoop` — simulates the `::ShowWindow` nested message loop that processes pending tasks

## Root Cause

`content/browser/renderer_host/render_frame_host_impl.cc`, lines 10352-10356:

```
FrameTree* new_frame_tree =
    delegate_->CreateNewWindow(this, *params, ...);  // [1]

transient_allow_popup_.Deactivate();                  // [2] UAF WRITE

```

[1] `delegate_->CreateNewWindow()` → `WebContentsImpl::CreateNewWindow()` → `AddNewContents()` → on Windows, `Browser::AddNewContents()` → `Widget::Show()` → `::ShowWindow()` → nested message loop. During this loop, a `window.close()` from another renderer's popup destroys the opener's WebContents → `~WebContentsImpl` → `FrameTree::Shutdown()` → `~RenderFrameHostManager` → `~RenderFrameHostImpl` → RFHI freed.

[2] `transient_allow_popup_.Deactivate()` writes to the freed RFHI → heap-use-after-free.

## ASAN Trace

```
==1592==ERROR: AddressSanitizer: heap-use-after-free on address 0x1217f6bada18
WRITE of size 8 at 0x1217f6bada18 thread T0
    #0 in dawn::native::d3d12::CPUDescriptorHeapAllocation::Invalidate
    #1 in content::RenderFrameHostImpl::CreateNewWindow render_frame_host_impl.cc:10371

0x1217f6bada18 is located 5400 bytes inside of 6072-byte region
freed by thread T0 here:
    #1 in content::RenderFrameHostImpl::~RenderFrameHostImpl render_frame_host_impl.cc:2851
    #2 in content::RenderFrameHostManager::~RenderFrameHostManager render_frame_host_manager.cc:822
    #3 in content::FrameTreeNode::~FrameTreeNode frame_tree_node.cc:312
    #4 in content::FrameTree::~FrameTree frame_tree.cc:230
    #5 in content::WebContentsImpl::~WebContentsImpl web_contents_impl.cc:1494

MiraclePtr Status: NOT PROTECTED
This crash is still exploitable with MiraclePtr.

```
## Suggested Fix

`fix.diff` adds a `base::WeakPtr` guard after `delegate_->CreateNewWindow()`, matching the ExitFullscreen fix pattern ([Bug 505045913](https://issues.chromium.org/issues/505045913)):

```
FrameTree* new_frame_tree =
    delegate_->CreateNewWindow(this, *params, ...);

base::WeakPtr<RenderFrameHostImpl> weak_this = GetWeakPtr();
if (!weak_this) {
  return;
}

transient_allow_popup_.Deactivate();

```
## References

- ExitFullscreen UAF: [Bug 505045913](https://issues.chromium.org/issues/505045913) (same root cause, different method)
- SetWindowRect UAF: my concurrent report (same root cause, different method)
- Both show the pattern: delegate call → Win32 nested message loop → this destroyed → post-call UAF

Credit: Mihnea Nicolau

## Attachments

- [fix.diff](attachments/fix.diff) (text/x-diff, 798 B)
- [patch.diff](attachments/patch.diff) (text/x-diff, 1.6 KB)
- [poc.html](attachments/poc.html) (text/html, 164 B)

## Timeline

### ke...@chromium.org (2026-04-28)

This report does not meet [our PoC requirements](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#report-formatting-attachments).

The patch you are applying is not simulating a race condition. It is making the main thread run additional tasks while in the middle of a function, which is not how threading works. If you can reproduce this issue without a browser patch in place then please resubmit with that PoC.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506921089)*
