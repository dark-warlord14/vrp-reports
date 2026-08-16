# UAF in RenderFrameHostImpl::ExitFullscreen() — missing WeakPtr guard (variant of EnterFullscreen fix 91d5baaef742)

| Field | Value |
|-------|-------|
| **Issue ID** | [507138723](https://issues.chromium.org/issues/507138723) |
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

---

### Report description

Heap UAF in WebContentsImpl::FullscreenStateChanged

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

Hi team, there's a heap-use-after-free in `WebContentsImpl::FullscreenStateChanged` at HEAD that mirrors [b/505045913](https://issues.chromium.org/issues/505045913) (*Fix Use-After-Free in RenderFrameHostImpl::ExitFullscreen*) one method over. when `delegate_->FullscreenStateChangedForTab(...)` synchronously destroys the WebContents (the supported path is Android via `WebContentsDelegateAndroid` > JNI to embedder Java), control returns to `WebContentsImpl::FullscreenStateChanged` and reads `this->fullscreen_frames_` on freed memory

### summary

chromium 149.0.7812.0 (built from HEAD `c24831282aab5f8c5456e8c2ab04be70547c4a22`). re-verified today against origin/main. the buggy lines at web\_contents\_impl.cc:4892/4895 and render\_frame\_host\_impl.cc:9302-9320 are byte-identical at origin/main HEAD. one upstream commit (bcd48391b3707) touches web\_contents\_impl.cc but at L5412 in `CreateNewWindow`'s DocPiP branch, not at the FullscreenStateChanged site

build: `out/libfuzzer/`, GN args:

```
use_libfuzzer = true
is_asan = true
is_debug = false
is_component_build = false
symbol_level = 1
dcheck_always_on = false
target_cpu = "x64"
optimize_for_fuzzing = true
use_siso = false

```
### bug shape

primary site at `content/browser/web_contents/web_contents_impl.cc:4874-4900` (HEAD):

```
void WebContentsImpl::FullscreenStateChanged(
    RenderFrameHostImpl* rfh,
    bool is_fullscreen,
    blink::mojom::FullscreenOptionsPtr options) {
  ...
  if (is_fullscreen) {
    ...
    if (delegate_) {
      delegate_->FullscreenStateChangedForTab(rfh, *options);     // L4892, may sync-destroy this
    }

    if (bool was_inserted = fullscreen_frames_.insert(rfh).second; // L4895, reads this->fullscreen_frames_ on freed this
        was_inserted) {
      FullscreenFrameSetUpdated();
    }
  }
  ...
}

```

`fullscreen_frames_` is a member of `WebContentsImpl` (`std::set<base::raw_ptr<RenderFrameHostImpl, SetExperimental>>` at `web_contents_impl.h:2653`). reaching it requires reading `this->fullscreen_frames_`. when `delegate_->FullscreenStateChangedForTab(rfh, *options)` synchronously destroys the WebContents, `this` is freed and the L4895 access dereferences freed memory.

caller at `content/browser/renderer_host/render_frame_host_impl.cc:9302-9320` is the entry path:

```
base::WeakPtr<RenderFrameHostImpl> weak_ptr = GetWeakPtr();              // L9302
delegate_->EnterFullscreenMode(this, *options);                          // L9303 - guarded by 91d5baaef742d
if (!weak_ptr) { return; }                                               // L9304-9306
delegate_->FullscreenStateChanged(this, /*is_fullscreen=*/true,          // L9307-9308 UNGUARDED
                                  std::move(options));
GetOutermostMainFrame()                                                  // L9318-9320 UNGUARDED
    ->GetLocalRenderWidgetHost()
    ->SynchronizeVisualProperties();

```

after `delegate_->FullscreenStateChanged(...)` returns from the dead WebContents, control returns to `RenderFrameHostImpl::EnterFullscreen`. the RFH itself was also destroyed transitively (the WebContents owns the frame tree), so `this` of the RFH is dangling too. `GetOutermostMainFrame()` at L9318 reads through a dead RFH, a secondary UAF on the same destruction event.

second reach surface: `RenderFrameHostImpl::FullscreenStateChanged(bool, blink::mojom::FullscreenOptionsPtr)` at `render_frame_host_impl.cc:8495-8501` is the renderer-IPC handler that the renderer calls to inform the browser of fullscreen state changes. its body is:

```
if (IsInactiveAndDisallowActivation(...)) { return; }
delegate_->FullscreenStateChanged(this, is_fullscreen, std::move(options));

```

this is a second caller of the same vulnerable `WebContentsImpl::FullscreenStateChanged` (the WCI-side fix in `suggested_fix.patch` covers it). flagging it for completeness so triage doesn't have to discover it later.

### ASan

the `ExitFullscreenDestruction` test added by `f2c344251df5a` at `render_frame_host_impl_unittest.cc:202-219` demonstrates the test pattern: a `DestructionDelegate` extending `WebContentsDelegate` whose `ExitFullscreenModeForTab` override calls `RenderViewHostTestHarness::DeleteContents` synchronously. the analogous test for the new bug overrides `FullscreenStateChangedForTab` instead, lands the destruction inside the second hop, and fires immediately:

```
==537873==ERROR: AddressSanitizer: heap-use-after-free on address 0x781255c06a60 at pc 0x57d55133d85c
READ of size 8 at 0x781255c06a60 thread T0
    #0 std::__tree __static_fancy_pointer_cast (libc++ tree node insert plumbing)
    ...
    #7 std::set::insert
    #8 content::WebContentsImpl::FullscreenStateChanged(content::RenderFrameHostImpl*, bool, mojo::StructPtr<blink::mojom::FullscreenOptions>)
       content/browser/web_contents/web_contents_impl.cc:4895:48
    #9 content::RenderFrameHostImpl::EnterFullscreen(...)
       content/browser/renderer_host/render_frame_host_impl.cc:9307:14
    #10 content::RenderFrameHostImplTest_EnterFullscreenDestruction_Test::TestBody()
       content/browser/renderer_host/render_frame_host_impl_unittest.cc:268:20

```

freed-memory attribution:

```
0x781255c06a60 is located 4448 bytes inside of 5408-byte region [0x781255c05900,0x781255c06e20)
freed by thread T0 here:
    #0 operator delete(void*)
    ...
    #6 content::RenderFrameHostImplTest_EnterFullscreenDestruction_Test::TestBody()::DestructionDelegate::FullscreenStateChangedForTab
       content/browser/renderer_host/render_frame_host_impl_unittest.cc:248:41
    #7 content::WebContentsImpl::FullscreenStateChanged(...)
       content/browser/web_contents/web_contents_impl.cc:4892:18
    #8 content::RenderFrameHostImpl::EnterFullscreen(...)
       content/browser/renderer_host/render_frame_host_impl.cc:9307:14
previously allocated by thread T0 here:
    #0 operator new(unsigned long)
    #1 operator new in content/public/browser/web_contents.h:178:3
    #2 content::TestWebContents::Create(...) at content/test/test_web_contents.cc:74:7
    #3 content::RenderViewHostTestHarness::CreateTestWebContents()
    ...

```

the freed allocation is the `TestWebContents` (a `WebContentsImpl` subclass), 5408 bytes total. the READ at offset 4448 falls inside `WebContentsImpl::fullscreen_frames_` (specifically `__tree_.__end_node_.__left_` per the std::set internal layout). `set::insert(rfh)` only compares pointer values via `raw_ptr<T, SetExperimental>::operator<=>` and does not dereference `rfh`. the dangling pointer is **`this` of `WebContentsImpl`**, freed when `delegate_->FullscreenStateChangedForTab` synchronously called `DeleteContents`.

### repro

apply the attached `unittest_diff.patch` (one new test, only modifies the existing in-tree test file content/browser/renderer\_host/render\_frame\_host\_impl\_unittest.cc from f2c344251df5a) and rebuild content\_unittests:

```
cd /path/to/chromium/src
git apply unittest_diff.patch
autoninja -C out/asan content_unittests

```

run under ASAN (Aura needs a display, xvfb works):

```
xvfb-run -a /path/to/chromium/src/out/asan/content_unittests \
  --gtest_filter='RenderFrameHostImplTest.EnterFullscreenDestruction' \
  --gtest_color=no

```

fires within ~10 seconds.

### reachability

the synchronous-destroy chain this bug requires is **not exposed to vanilla web content on desktop chrome**. checked all `FullscreenStateChangedForTab` overrides in the tree:

- `content/public/browser/web_contents_delegate.h:540`, virtual default is `{}`, no-op
- `content/public/browser/prerender_web_contents_delegate.cc:93`, `NOTREACHED()`, never reached
- `components/embedder_support/android/delegate/web_contents_delegate_android.cc:348`, **Android only**, attaches JNIEnv and calls into Java embedder via `Java_WebContentsDelegateAndroid_fullscreenStateChangedForTab`
- `content/browser/web_contents/web_contents_impl_browsertest.cc:1758`, test-only

`chrome::Browser` (chrome's primary `WebContentsDelegate`) does not override this method. confirmed by tree-wide grep across `chrome/`, `android_webview/`, `headless/`, `ash/`, `chromecast/`, `ios/`, `components/`, `extensions/`. ran a real-chrome PoC under ASAN with 4 trigger variants (cross-origin iframe + `iframe.remove()` in `fullscreenchange`, popup + `window.close()`, opener-driven close, sibling-tab orchestrator). all produced legitimate `fullscreenchange` events, none fired ASAN, consistent with the structural finding above.

reachable paths at HEAD:

1. **Android Chrome / WebView via JNI**: `WebContentsDelegateAndroid::FullscreenStateChangedForTab` calls into the embedder's Java `onFullscreenStateChanged` handler. an embedder app whose Java handler synchronously calls `WebContents.destroy()` (or removes the `WebContents` from its parent layout in a way that triggers immediate native destruction) reaches this UAF. WebView apps are first-party callers here. this matches the Android-targeted reachability that `f2c344251df5a` covers for `ExitFullscreen`.
2. **Future overrides**: any new `WebContentsDelegate` subclass that overrides `FullscreenStateChangedForTab` and synchronously destroys the WebContents (or its frame tree) within the callback hits this bug. defense-in-depth value matches what `f2c344251df5a` provided for `ExitFullscreen`.
3. **Test harnesses + fuzzing**: any unit test that installs a delegate matching the unit-test pattern (which is by definition supported behavior since the just-landed CL relies on it).

#### Impact analysis

browser-process heap-use-after-free, web-reachable on Android via `WebContentsDelegateAndroid::FullscreenStateChangedForTab` JNI to a host-app Java handler that synchronously destroys the WebContents. on the C++ side the freed object is `WebContentsImpl` (5408-byte allocation, offset 4448 reads through `fullscreen_frames_.__tree_.__end_node_.__left_`). secondary read at `render_frame_host_impl.cc:9318` (`GetOutermostMainFrame()`) on the dead RFH is a second UAF site if the first were patched. structurally equivalent to `f2c344251df5a`[b/505045913](https://issues.chromium.org/issues/505045913) (`ExitFullscreen`). Linux desktop chrome and stock chromium with default `Browser` delegate are NOT reachable from web content alone, so this is best framed as defense-in-depth on desktop, exploitable on Android in embedder-mediated scenarios.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7812.0

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption

#### How would you like to be publicly acknowledged for your report?

Andrew Boni

## Attachments

- [chromium_tree_android_fix_cc.patch](attachments/chromium_tree_android_fix_cc.patch) (application/octet-stream, 4.5 KB)
- [suggested_fix.patch](attachments/suggested_fix.patch) (application/octet-stream, 1.8 KB)
- [unittest_diff.patch](attachments/unittest_diff.patch) (application/octet-stream, 2.9 KB)
- [destructive_java_trigger.patch](attachments/destructive_java_trigger.patch) (application/octet-stream, 1.4 KB)
- [chromium_tree_android_fix_buildgn.patch](attachments/chromium_tree_android_fix_buildgn.patch) (application/octet-stream, 1.7 KB)
- [asan.log](attachments/asan.log) (application/octet-stream, 20.5 KB)
- [build.log](attachments/build.log) (application/octet-stream, 3.8 MB)

## Timeline

### ke...@chromium.org (2026-04-28)

This report does not meet [our PoC requirements](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules#report-formatting-attachments).

In particular, tests can create program states that are unreachable in production Chrome, and therefore do not demonstrate real bugs. PoCs should run on an unmodified Chrome build.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507138723)*
