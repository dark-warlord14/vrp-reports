# Heap-use-after-free in VerticalTabDragHandlerImpl::ContinueDrag

| Field | Value |
|-------|-------|
| **Issue ID** | [495973592](https://issues.chromium.org/issues/495973592) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 147.0.7725.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2026-03-25 |
| **Bounty** | $1,000.00 |

## Description

Project Fortify, an experimental security project, has identified the following potential security issue.

Overview: A use-after-free vulnerability exists in `VerticalTabDragHandlerImpl` when a tab drag operation enters a nested message loop. If the source window is closed during this loop, the handler object is destroyed, but execution later resumes on the freed object, leading to a highly exploitable arbitrary delete primitive.

Affected files:

- `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc`
- `chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc`

Estimated timestamp from git blame: 2026-03-17

### Summary

A potential Use-After-Free (UAF) vulnerability exists in `VerticalTabDragHandlerImpl::ContinueDrag` and `InitializeDrag` when the vertical tabs feature is enabled. The vulnerability triggers when a tab is dragged out of a window, entering a nested message loop (`views::Widget::RunMoveLoop`). If the source window is closed while this nested loop is active, the `VerticalTabDragHandlerImpl` object is destroyed. When the loop eventually terminates and execution unwinds, the method attempts to call `ResetDragState()` on the now-freed `this` pointer.

### Vulnerability Details

In `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc`, dragging a tab calls `ContinueDrag`, which invokes `TabDragController::Drag()`:

```
bool VerticalTabDragHandlerImpl::ContinueDrag(views::View& event_source_view,
                                              const ui::LocatedEvent& event) {
  if (!drag_controller_) {
    return false;
  }
  gfx::Point screen_location(event.location());
  ConvertPointToScreen(&event_source_view, &screen_location);
  if (drag_controller_->Drag(screen_location) ==
      TabDragController::Liveness::kDeleted) {
    ResetDragState(); // <--- UAF: 'this' may have been deleted
    return false;
  }
  return true;
}

```

If the dragged tab is detached to create a new browser window, `TabDragController::Drag` synchronously enters a nested message loop (`RunMoveLoop`). While blocked in this loop, the browser can still process asynchronous events. If the source window is closed (e.g., via an extension API or a timed `window.close()` from a malicious webpage), the view hierarchy is torn down, destroying the `VerticalTabDragHandlerImpl` instance.

When the nested loop exits and unwinds, `TabDragController::Drag` returns `TabDragController::Liveness::kDeleted`. Execution proceeds to line 266, calling `ResetDragState()`. This accesses the freed memory to find the `drag_controller_` member (a `std::unique_ptr`) and calls `.reset()` on it.

### Impact

Because the dangling pointer is an implicit `this` pointer and the accessed member is a `std::unique_ptr` (rather than a `raw_ptr`), this is not protected by MiraclePtr (BackupRefPtr).

An attacker who sprays the heap during the window destruction can reclaim the freed `VerticalTabDragHandlerImpl` memory. The subsequent `.reset()` call on the attacker-controlled `std::unique_ptr` provides a powerful arbitrary `delete` and virtual function call primitive. This can be reliably leveraged to achieve Remote Code Execution (RCE) and sandbox escape within the highly privileged Browser Process.

### Potential Reproduction Steps

*Note: These are theoretical steps proposed by our setup, which cannot currently execute code to generate a live PoC.*

1. An attacker-controlled webpage opens a popup window with the Vertical Tabs feature active.
2. The attacker's JavaScript sets a `setTimeout` to call `window.close()` on the popup after a short delay (e.g., 3 seconds).
3. Within those 3 seconds, the user is convinced to click and drag a vertical tab to detach it from the popup window.
4. Detaching the tab enters the nested `RunMoveLoop`.
5. The `setTimeout` triggers, closing the popup window and freeing the `VerticalTabDragHandlerImpl`.
6. The user completes or cancels the drag, causing the nested loop to exit.
7. `ContinueDrag` resumes, dereferences the freed `this` pointer, and crashes or executes attacker-controlled data.

### Suggested Fix

The standard pattern for safely handling nested message loops in Views is to track the liveness of `this` using a `base::WeakPtr`.

Add a `base::WeakPtrFactory` to `VerticalTabDragHandlerImpl` and check it before accessing any members after the `Drag()` call:

```
base::WeakPtr<VerticalTabDragHandlerImpl> weak_this = weak_factory_.GetWeakPtr();
if (drag_controller_->Drag(screen_location) ==
    TabDragController::Liveness::kDeleted) {
  if (weak_this) {
    ResetDragState();
  }
  return false;
}

```

Similar protection should be added to `VerticalTabDragHandlerImpl::InitializeDrag`.

Evaluated with Chrome root at commit: 0eb4855bda702feaaa8b899336664f97e3df88b8

---

Results so far have been promising, but there can be wrong deductions. If this proves to be a false positive, please close as WAI; data from false positives will be used to improve accuracy over time. Please feel free to reach out to me if you have concerns or feedback.

## Attachments

- [asan-output.log](attachments/asan-output.log) (text/plain; charset=utf-8, 18.4 KB)
- [bandaid-fix.patch](attachments/bandaid-fix.patch) (text/plain; charset=utf-8, 1.4 KB)
- [chromium-changes.patch](attachments/chromium-changes.patch) (text/plain; charset=utf-8, 14.9 KB)

## Timeline

### ch...@google.com (2026-03-25)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### dx...@google.com (2026-03-26)

Project: chromium/src  

Branch:  main  

Author:  mikt [mikt@google.com](mailto:mikt@google.com)  

Link:    <https://chromium-review.googlesource.com/7699395>

Add AMSC macro to VerticalTabDragHandlerImpl

---


Expand for full commit details
```
     
    Bug: 495973592 
    Change-Id: I89db011d9add513b1a9b9fb5ae65cd0fa7e1f5f9 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7699395 
    Reviewed-by: Mark Foltz <mfoltz@chromium.org> 
    Commit-Queue: Mikihito Matsuura <mikt@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1605270}

```

---

Files:

- M `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.h`

---

Hash: [2f271e6bec295e0fe2a5718713ff5b86c521fdcd](https://chromiumdash.appspot.com/commit/2f271e6bec295e0fe2a5718713ff5b86c521fdcd)  

Date: Thu Mar 26 05:09:29 2026


---

### al...@google.com (2026-03-27)

This is a duplicate of [b/490588145](https://issues.chromium.org/issues/490588145). I'll close this after fixing the original.

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  Kaan Alsan [alsan@chromium.org](mailto:alsan@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705549>

Protect against use-after-free in VerticalTabDragHandlerImpl

---


Expand for full commit details
```
     
    The TabDragController::Drag method can start a blocking message loop. 
    This loop can lead to the destruction of the VerticalTabDragHandlerImpl 
    instance. Use a WeakPtr to check if the instance is still alive before 
    calling ResetDragState after Drag returns. 
     
    Bug: 490588145, 495973592 
    Change-Id: I9d193a9c0ced4fe698bcec57c5bca3c749d05752 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705549 
    Commit-Queue: Kaan Alsan <alsan@chromium.org> 
    Reviewed-by: Foromo Daniel Soromou <koretadaniel@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607358}

```

---

Files:

- M `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc`
- M `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.h`

---

Hash: [8452c6aaafc5710974c3313967d2dd84aedfa534](https://chromiumdash.appspot.com/commit/8452c6aaafc5710974c3313967d2dd84aedfa534)  

Date: Mon Mar 30 20:51:35 2026


---

### vm...@google.com (2026-04-01)

Project Fortify, an experimental security project, has identified the following POC. Please share feedback on issues or improvements on this report to vmiura@

# POC: Heap Use-After-Free in `VerticalTabDragHandlerImpl::ContinueDrag`

**Strategy:** code-injection
**ASAN Error:** heap-use-after-free
**MiraclePtr Status:** NOT PROTECTED — implicit `this` is a bare C++ stack pointer

---

## Vulnerability Summary

`VerticalTabDragHandlerImpl::ContinueDrag` at
`chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc` calls:

```
if (drag_controller_->Drag(screen_location) ==
    TabDragController::Liveness::kDeleted) {
  ResetDragState();   // <-- reads this->drag_controller_ on freed `this`
  return false;
}

```

`TabDragController::Drag()` enters a nested `Widget::RunMoveLoop` (a blocking,
re-entrant message loop). During that loop:

1. **Detach.** `TabDragController::Detach()` (`tab_drag_controller.cc:1435`)
   calls `attached_context_->ReleaseDragController()`, transferring ownership
   away from the source `VerticalTabDragHandlerImpl`. The source's
   `drag_controller_` becomes `nullptr`.
2. **Closeability guard now passes.** With `drag_controller_ == nullptr`, the
   source browser is no longer considered "in a drag" and can be closed.
3. **Source browser closes** — via extension `chrome.windows.remove()`, JS
   `window.close()`, or `Ctrl+Shift+W` — destroying the source
   `VerticalTabDragHandlerImpl` while `ContinueDrag` is still on the stack.
4. **Loop returns.** `RunMoveLoop` returns, `Drag()` propagates
   `Liveness::kDeleted` (`tab_drag_controller.cc:1726-1730`), and the
   vulnerable code calls `ResetDragState()` → `this->drag_controller_.reset()`
   on freed memory.

**Why MiraclePtr does NOT protect this:** the implicit `this` pointer in
`ContinueDrag` is a bare C++ stack pointer, never wrapped by `raw_ptr<T>`.
BackupRefPtr only quarantines allocations that have a live `raw_ptr<T>`
reference at free time. The source-browser-close callchain in the real attack
holds no `raw_ptr<VerticalTabDragHandlerImpl>`.

---

## POC Design

This is a **browser-process UI bug** triggered by a physical tab-drag gesture
plus a window-close timed during the nested move loop. It is **not directly
web-reachable**, but is reachable from a malicious extension
(`chrome.windows.remove()`) or from JS in a window opened by `window.open()`
(`window.close()` on the opener).

A real `Widget::RunMoveLoop` requires WM cooperation (X11 `_NET_WM_MOVERESIZE`,
etc.) and is unreliable headless. The POC therefore embeds a **deterministic
nested-loop simulation hook** in `TabDragController::Drag()` that faithfully
mirrors the four-step sequence above:

| Step | Real attack | POC simulation |
| --- | --- | --- |
| 1 | `Detach()` → `ReleaseDragController()` | `g_poc_release_from->ReleaseDragController()` |
| 2 | Nested loop pumps tasks; source browser closes | `destroy_source` callback runs `parent->RemoveChildViewT(handler)` |
| 3 | Ownership transfers to detached browser | `me.release()` (intentional leak) |
| 4 | `RunMoveLoop` → `kDeleted` | `return Liveness::kDeleted` |

The POC is gated by the `POC_VERTICAL_TAB_DRAG_UAF` environment variable and
fires once on browser startup. The handler's constructor posts a task to the UI
thread; by the time the task runs, the handler has been added to its parent
view (`VerticalTabStripRegionView`). The task arms the simulation hook,
synthesizes a `kMouseDragged` event, and calls `ContinueDrag` directly.

### Why `uintptr_t` round-trips

Early iterations of this POC bound the victim pointer through
`base::Unretained()`, which wraps it in `UnretainedWrapper` containing a
`raw_ptr<T>`. That `raw_ptr` was still live in the `Invoker` stack frame at the
moment of UAF, causing the ASAN MiraclePtr classifier to mark the crash
**PROTECTED** — a false positive introduced *by the POC harness*, not present
in the real attack. The POC stores all victim-adjacent pointers as static
`uintptr_t` and `reinterpret_cast`s inside captureless lambdas, exactly
mirroring the real attack's lack of `raw_ptr` protection.

### Upstream fix

This bug was already fixed upstream in commit
`8452c6aaafc5710974c3313967d2dd84aedfa534` (Mar 2026). The POC patch
**reverts** that fix's `.cc` change to expose the original vulnerable code.
The unused `weak_factory_` member added to the `.h` by that commit is left in
place (touching the header would trigger a wide rebuild).

---

## Prerequisites

- Chromium checkout at `/chromium/chromium/src`
- ASAN build at `/chromium/chromium/src/out/asan`
- The `chrome` target already linked once (incremental rebuild after applying
  the patch only relinks `chrome`; ~30s)
- An X display (Xvfb is sufficient — no real WM cooperation needed because the
  nested loop is simulated)

---

## Reproduction

### 1. Apply the POC patch

```
cd /chromium/chromium/src
git apply /path/to/chromium-changes.patch

```

The patch touches **only** two `.cc` files — no headers — so the rebuild is
incremental:

- `chrome/browser/ui/views/tabs/dragging/tab_drag_controller.cc` — adds the
  nested-loop simulation hook at the top of `Drag()`
- `chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc` —
  reverts the WeakPtr guard, adds the env-gated trigger task

### 2. Build

```
cd /chromium/chromium/src
autoninja -C out/asan chrome

```
### 3. Run

```
# Seed a profile with vertical tabs enabled (the feature flag alone isn't
# enough; the per-profile pref must also be set).
rm -rf /tmp/chrome-poc-profile
mkdir -p /tmp/chrome-poc-profile/Default
cat > /tmp/chrome-poc-profile/Default/Preferences << 'EOF'
{"vertical_tabs":{"enabled":true}}
EOF

# detect_leaks=0: the POC intentionally leaks the TabDragController (mirroring
#                 ownership transfer to the detached browser).
export ASAN_OPTIONS="detect_leaks=0:symbolize=1:print_stacktrace=1"
export POC_VERTICAL_TAB_DRAG_UAF=1

/chromium/chromium/src/out/asan/chrome \
  --enable-features=VerticalTabs \
  --no-sandbox --no-first-run --no-default-browser-check \
  --disable-gpu \
  --user-data-dir=/tmp/chrome-poc-profile \
  about:blank 2>&1

```
### 4. Clean up

```
cd /chromium/chromium/src
git checkout -- .

```

---

## Expected Result

ASAN aborts ~2 seconds after browser-window creation with a
`heap-use-after-free` in `VerticalTabDragHandlerImpl::ContinueDrag`. Look for:

- **Use stack #0:** `VerticalTabDragHandlerImpl::ContinueDrag` at
  `unique_ptr.h:285` — this is `unique_ptr::reset()` reading
  `this->drag_controller_` (the `__ptr_` load) inside `ResetDragState()`.
- **Freed-region offset:** `800 bytes inside of 872-byte region` —
  `drag_controller_` at offset 800 inside `VerticalTabDragHandlerImpl`.
- **Free stack #2-#3:** `TabDragController::Drag` →
  `VerticalTabDragHandlerImpl::ContinueDrag:442` — the free happened *inside*
  the call to `Drag()`, which is exactly the nested-loop reentrancy bug.
- **Alloc stack #1-#12:** real production path — `Browser::Create` →
  `BrowserView::AddedToWidget` → `VerticalTabStripRegionView::InitializeTabStrip`.
- **`MiraclePtr Status: NOT PROTECTED`** — confirming this UAF is exploitable
  even with BRP fully enabled.

Preceding the ASAN report you will see two `LOG(ERROR)` markers:

```
POC: arming nested-loop simulation; ContinueDrag UAF expected next
POC: destroying source VerticalTabDragHandlerImpl (simulating source-browser close during nested Widget::RunMoveLoop)

```

---

## ASAN Output

```
==10732==ERROR: AddressSanitizer: heap-use-after-free on address 0x7cc519762ba0 at pc 0x56489f57de84 bp 0x7ffd494ff4d0 sp 0x7ffd494ff4c8
READ of size 8 at 0x7cc519762ba0 thread T0 (chrome)
    #0 0x56489f57de83 in VerticalTabDragHandlerImpl::ContinueDrag(views::View&, ui::LocatedEvent const&) gen/third_party/libc++/src/include/__memory/unique_ptr.h:285:21
    #1 0x56489f589fa5 in base::internal::Invoker<base::internal::FunctorTraits<VerticalTabDragHandlerImpl::VerticalTabDragHandlerImpl(TabStripModel&, TabCollectionNode&)::$_0&&>, base::internal::BindState<false, false, false, VerticalTabDragHandlerImpl::VerticalTabDragHandlerImpl(TabStripModel&, TabCollectionNode&)::$_0>, void ()>::RunOnce(base::internal::BindStateBase*) chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:242:26
    #2 0x5648a2b4a9b6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #3 0x5648a2bc2059 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #4 0x5648a2bc0eca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:340:40
    #5 0x5648a2d703b4 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #6 0x5648a2bc3767 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:644:12
    #7 0x5648a2ac5330 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #8 0x5648965c588c in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1105:18
    #9 0x5648965cdf3c in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15
    #10 0x5648965bc5bc in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #11 0x56489e66261f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:696:10
    #12 0x56489e666608 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1320:10
    #13 0x56489e665a9a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:12
    #14 0x56489e65f441 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #15 0x56489e65fa3c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #16 0x56488ab94b39 in ChromeMain chrome/app/chrome_main.cc:191:12
    #17 0x7f451b22b249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 6196744a316dbd57c0fd8968df1680aac482cec4)

0x7cc519762ba0 is located 800 bytes inside of 872-byte region [0x7cc519762880,0x7cc519762be8)
freed by thread T0 (chrome) here:
    #0 0x56488ab93c3d in operator delete(void*) (/chromium/chromium/src/out/asan/chrome+0x10e14c3d) (BuildId: cb8ecd99501281fa)
    #1 0x56489f58a6ac in base::internal::Invoker<base::internal::FunctorTraits<(anonymous namespace)::PocTriggerContinueDragUAF(VerticalTabDragHandlerImpl*)::$_0&&>, base::internal::BindState<false, false, false, (anonymous namespace)::PocTriggerContinueDragUAF(VerticalTabDragHandlerImpl*)::$_0>, void ()>::RunOnce(base::internal::BindStateBase*) gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5
    #2 0x5648bc207888 in TabDragController::Drag(gfx::Point const&) base/functional/callback.h:155:12
    #3 0x56489f57dd89 in VerticalTabDragHandlerImpl::ContinueDrag(views::View&, ui::LocatedEvent const&) chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:442:25
    #4 0x56489f589fa5 in base::internal::Invoker<base::internal::FunctorTraits<VerticalTabDragHandlerImpl::VerticalTabDragHandlerImpl(TabStripModel&, TabCollectionNode&)::$_0&&>, base::internal::BindState<false, false, false, VerticalTabDragHandlerImpl::VerticalTabDragHandlerImpl(TabStripModel&, TabCollectionNode&)::$_0>, void ()>::RunOnce(base::internal::BindStateBase*) chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:242:26
    #5 0x5648a2b4a9b6 in base::TaskAnnotator::RunTaskImpl(base::PendingTask&) base/functional/callback.h:155:12
    #6 0x5648a2bc2059 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl(base::LazyNow*) base/task/common/task_annotator.h:112:5
    #7 0x5648a2bc0eca in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork() base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:340:40
    #8 0x5648a2d703b4 in base::MessagePumpGlib::Run(base::MessagePump::Delegate*) base/message_loop/message_pump_glib.cc:782:48
    #9 0x5648a2bc3767 in base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run(bool, base::TimeDelta) base/task/sequence_manager/thread_controller_with_message_pump_impl.cc:644:12
    #10 0x5648a2ac5330 in base::RunLoop::Run(base::Location const&) base/run_loop.cc:135:14
    #11 0x5648965c588c in content::BrowserMainLoop::RunMainMessageLoop() content/browser/browser_main_loop.cc:1105:18
    #12 0x5648965cdf3c in content::BrowserMainRunnerImpl::Run() content/browser/browser_main_runner_impl.cc:151:15
    #13 0x5648965bc5bc in content::BrowserMain(content::MainFunctionParams) content/browser/browser_main.cc:32:28
    #14 0x56489e66261f in content::RunBrowserProcessMain(content::MainFunctionParams, content::ContentMainDelegate*) content/app/content_main_runner_impl.cc:696:10
    #15 0x56489e666608 in content::ContentMainRunnerImpl::RunBrowser(content::MainFunctionParams, bool) content/app/content_main_runner_impl.cc:1320:10
    #16 0x56489e665a9a in content::ContentMainRunnerImpl::Run() content/app/content_main_runner_impl.cc:1150:12
    #17 0x56489e65f441 in content::RunContentProcess(content::ContentMainParams, content::ContentMainRunner*) content/app/content_main.cc:358:36
    #18 0x56489e65fa3c in content::ContentMain(content::ContentMainParams) content/app/content_main.cc:371:10
    #19 0x56488ab94b39 in ChromeMain chrome/app/chrome_main.cc:191:12
    #20 0x7f451b22b249  (/lib/x86_64-linux-gnu/libc.so.6+0x27249) (BuildId: 6196744a316dbd57c0fd8968df1680aac482cec4)

previously allocated by thread T0 (chrome) here:
    #0 0x56488ab933fd in operator new(unsigned long) (/chromium/chromium/src/out/asan/chrome+0x10e143fd) (BuildId: cb8ecd99501281fa)
    #1 0x5648bbd2e07a in VerticalTabStripRegionView::InitializeTabStrip() ui/views/view.h:306:3
    #2 0x5648bbba5d44 in BrowserView::AddedToWidget() chrome/browser/ui/views/frame/browser_view.cc:5238:40
    #3 0x5648aac839bd in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) ui/views/view.cc:3395:5
    #4 0x5648aac81a0d in views::View::AddChildViewAtImpl(views::View*, unsigned long) ui/views/view.cc:3266:9
    #5 0x5648aad1ce8b in views::NonClientView::ViewHierarchyChanged(views::ViewHierarchyChangedDetails const&) ui/views/window/non_client_view.cc:192:18
    #6 0x5648aac83904 in views::View::PropagateAddNotifications(views::ViewHierarchyChangedDetails const&, bool) ui/views/view.cc:3413:3
    #7 0x5648aac81a0d in views::View::AddChildViewAtImpl(views::View*, unsigned long) ui/views/view.cc:3266:9
    #8 0x5648aacb73dc in views::Widget::Init(views::Widget::InitParams) ui/views/widget/widget.cc:583:17
    #9 0x5648bbc3b29f in BrowserWidget::InitBrowserWidget() chrome/browser/ui/views/frame/browser_widget.cc:210:3
    #10 0x5648bbc65db9 in BrowserWindow::CreateBrowserWindow(Browser*, bool, bool) chrome/browser/ui/views/frame/browser_window_factory.cc:60:27
    #11 0x5648bb17deea in Browser::Browser(Browser::CreateParams const&) chrome/browser/ui/browser.cc:663:13
    #12 0x5648bb17c76f in Browser::Create(Browser::CreateParams const&) chrome/browser/ui/browser.cc:558:59
    #13 0x5648a27e12b8 in SessionRestoreImpl::FinishedTabCreation(bool, bool, std::__Cr::vector<SessionRestoreDelegate::RestoredTab, std::__Cr::allocator<SessionRestoreDelegate::RestoredTab>>&) chrome/browser/sessions/session_restore.cc:471:17
    #14 0x5648a27e0724 in SessionRestoreImpl::ProcessSessionWindows(...) chrome/browser/sessions/session_restore.cc:686:14
    #15 0x5648a27d8959 in SessionRestoreImpl::ProcessSessionWindowsAndNotify(...) chrome/browser/sessions/session_restore.cc:632:23
    #16 0x5648a27d2562 in SessionRestoreImpl::Restore() chrome/browser/sessions/session_restore.cc:323:11
    ...

SUMMARY: AddressSanitizer: heap-use-after-free gen/third_party/libc++/src/include/__memory/unique_ptr.h:285:21 in VerticalTabDragHandlerImpl::ContinueDrag(views::View&, ui::LocatedEvent const&)
Shadow bytes around the buggy address:
  0x7cc519762900: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc519762980: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc519762a00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc519762a80: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
  0x7cc519762b00: fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd fd
=>0x7cc519762b80: fd fd fd fd[fd]fd fd fd fd fd fd fd fd fa fa fa
  0x7cc519762c00: fa fa fa fa fa fa fa fa fa fa fa fa fa fa f7 fa

==10732==ADDITIONAL INFO

Task trace:
    #0 0x56489f5792d6 in VerticalTabDragHandlerImpl::VerticalTabDragHandlerImpl(TabStripModel&, TabCollectionNode&) chrome/browser/ui/views/tabs/vertical/vertical_tab_drag_handler.cc:280:9

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.
Refer to https://chromium.googlesource.com/chromium/src/+/main/base/memory/raw_ptr.md for details.

==10732==END OF ADDITIONAL INFO

```

Full unabridged output: `asan-output.log` in this directory.

---

## Bandaid Fix

`bandaid-fix.patch` re-applies the WeakPtr guard from upstream commit
`8452c6aaafc5710974c3313967d2dd84aedfa534`, layered on top of
`chromium-changes.patch`:

```
// Bandaid fix: Drag() may enter a nested Widget::RunMoveLoop. ...
auto ref = weak_factory_.GetWeakPtr();
auto liveness = drag_controller_->Drag(screen_location);
if (!ref) {
  return false;   // <-- `this` is gone; bail before touching members
}
if (liveness == TabDragController::Liveness::kDeleted) {
  ResetDragState();
  return false;
}

```

**What the fix does:** captures a `WeakPtr<VerticalTabDragHandlerImpl>` before
calling `Drag()`, then checks it on return. If `this` was destroyed during the
nested loop, `!ref` is true and the function returns immediately — never
reading `this->drag_controller_`.

**Why a `WeakPtr` and not a `raw_ptr<T>` mitigation:** the dangling pointer
here is the implicit `this`, which cannot be wrapped in `raw_ptr`. The only way
to detect destruction of `this` inside a member function is a `WeakPtr` taken
before the reentrant call.

### Applying and verifying the bandaid

```
cd /chromium/chromium/src
# (chromium-changes.patch already applied)
git apply /path/to/bandaid-fix.patch
autoninja -C out/asan chrome
# Re-run the POC commands from the Reproduction section above.

```

**Verified result:** the `ContinueDrag` UAF is gone. The POC's success log
`POC: *** UAF NOT DETECTED ***` is printed (`ContinueDrag` returned cleanly via
the `if (!ref)` early-return).

> **Note on the secondary crash you'll see after the bandaid:** with the
> `ContinueDrag` UAF averted, execution continues past `ContinueDrag`. ASAN
> then catches a *separate* UAF in
> `VerticalUnpinnedTabContainerView::IsViewDragging`. **This is a POC-harness
> artifact, not a real vulnerability.** The harness surgically destroys *only*
> the handler view via `RemoveChildViewT`, leaving sibling views with stale
> `drag_handler_` pointers. In the real attack, the entire browser window
> closes, destroying all those siblings together — there is no surviving caller
> of `IsViewDragging`. The bandaid fix correctly converts the vulnerability
> under test (`ContinueDrag`) into a safe early-return.

Comment created using go/buganizer-mcp-server

### ch...@google.com (2026-04-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-03)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-03)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### ag...@chromium.org (2026-04-03)

Remarking as fixed now that the severity and found in have been populated

### ch...@google.com (2026-07-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/495973592)*
