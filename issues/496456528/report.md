# Security: T0 Heap-Use-After-Free in views::Widget during Browser Teardown

| Field | Value |
|-------|-------|
| **Issue ID** | [496456528](https://issues.chromium.org/issues/496456528) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>UserEducation |
| **Platforms** | Mac |
| **Chrome Version** | 148.0.7751.0 |
| **Reporter** | ba...@gmail.com |
| **Assignee** | aj...@google.com |
| **Created** | 2026-03-26 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

Hello, I encountered a crash while running tests on Chromium. I'm not sure if it's related to my HTML file, but the terminal output indicates the root cause of the problem.
Obviously, to recreate this problem, I'm compiling Chromium from scratch on a different computer. I know the problem will recur if I encounter this bubble when I log in, but I've only encountered it once in 4 days. I suspect it's a promotional bubble shown to new users, so I'll try compiling from scratch on another computer.

# Problem Description

I downloaded and compiled Chromium for the first time on my computer; this was my first time using the Chromium browser. My HTML file contained instructions to open the calculator, and coincidentally, perhaps because I had just downloaded it, a blue promotional bubble for Chromium appeared in the upper right corner. At the same time, a window popped up asking if I wanted to open the calculator because of my HTML file, but I ignored both warnings and closed the tabs by clicking the 'X' buttons. Meanwhile, the browser crashed and gave an error output in my terminal.
VULNERABILITY DETAILS
Heap-Use-After-Free (Read of size 8) in the main Browser Process (T0), which completely bypasses the sandbox. The vulnerable object is `views::Widget`, and ASan confirms it is NOT protected by MiraclePtr/BackupRefPtr.

ROOT CAUSE ANALYSIS
This is a synchronous race condition between Chromium's Browser teardown sequence (`Browser::~Browser()`) and the macOS native window notification system (`NSNotificationCenter`).

Phase A (Allocation):
The IPH system triggers a Help Bubble (e.g., `CustomWebUIHelpBubble::CreateForController<extensions::ZeroStatePromoController>`).

Phase B (The Free):
When the browser is closed (via Cmd+Q), `Browser::~Browser()` initiates the destruction sequence. The `BubbleWidget` is destroyed and its memory is synchronously freed via `user_education::HelpBubble::Close()`.

Phase C (The Use):
Although the C++ object is freed, the macOS `NSNotificationCenter` fires a `windowWillClose:` notification. This invokes `remote_cocoa::NativeWidgetNSWindowBridge::OnWindowWillClose()`, which calls back into `views::NativeWidgetMac::WindowDestroying()` and `views::Widget::HandleWidgetDestroying()`. This attempts to read the freed C++ Widget state, causing a critical T0 UAF.

REPRODUCTION STEPS
Note: Reproducing this consistently on a local, unbranded build is extremely difficult because the `FeatureEngagementTracker` heuristics block the `ZeroStatePromo` bubble from rendering reliably (e.g., it waits for "browser initialization complete" and checks Finch configs).

To reproduce internally:

1. Use internal developer flags to force a WebUI Help Bubble to render (e.g., force `IPH_ExtensionsZeroStatePromo` on `chrome://extensions`).
2. While that blue Help Bubble is actively visible on the macOS screen, force-close the browser (Cmd + Q).
3. The ASan trace will immediately catch the UAF during teardown.

Please review the attached ASan log for the complete stack trace. Given the T0 context and lack of MiraclePtr protection, I kindly request a review of the severity.

# Summary

Security: T0 Heap-Use-After-Free in views::Widget during Browser Teardown

# Custom Questions

#### Type of crash:

browser

#### Crash state:

AddressSanitizer: heap-use-after-free (Read of size 8)
Crash location: views::Widget::HandleWidgetDestroying()

Thread: T0 (Main Browser Process)
MiraclePtr Status: NOT PROTECTED

- Please see the attached ASan log (.txt) for the complete allocation, free, and crash stack traces.

#### Reporter credit:

Batuhan Eşref KOÇ

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [crash1.txt](attachments/crash1.txt) (text/plain, 44.0 KB)
- [poc_reproduce.patch](attachments/poc_reproduce.patch) (text/x-diff, 2.6 KB)
- [asan_output.txt](attachments/asan_output.txt) (text/plain, 42.8 KB)
- [PoC.html](attachments/PoC.html) (text/html, 518 B)
- [exploit_poc_crash.ips](attachments/exploit_poc_crash.ips) (application/octet-stream, 155.2 KB)

## Timeline

### el...@chromium.org (2026-03-26)

Security shepherd: thanks for the report.

So, I cannot actually reproduce this locally - getting the IPH bubble to show up reliably is itself challenging. However, I find the ASAN stack attached to the report very convincing, so thank you for that. I agree with your analysis also - during BrowserWidget::~BrowserWidget() we're (ultimately) destroying a BubbleWidget too early.

From the ASAN stack, it sort of looks like we're in Widget::HandleWidgetDestroying() for the BubbleWidget, but the MakeCloseSynchronous() path (which we reach there) causes the Widget to be destroyed while we're still in the middle of HandleWidgetDestroying (!) with dire consequences. It does not seem safe to enter the synchronous close path from inside HandleWidgetDestroying like this.

I'm going to call this Sev-1 since, while it is a web-reachable UaF (JS can use window.close() to provoke this code path), it's very unreliable to actually trigger it and not clear how an attacker would get any control over the data being UaFed.

Over to dfried@ from //components/user\_education/OWNERS.

### el...@chromium.org (2026-03-26)

Note: FoundIn is speculative; I didn't check this against stable or extended stable.

### el...@chromium.org (2026-03-26)

The particular problem is likely this:

```
void HelpBubbleViews::OnWidgetDestroying(views::Widget* widget) {
  Close(CloseReason::kBubbleElementDestroyed);
}

```

This isn't safe, because ::OnWidgetDestroying() means the observed Widget *is already being destroyed*, and Close()ing it here, if that Close() is synchronous, will lead to a UaF back up the stack.

### er...@chromium.org (2026-03-27)

Thanks for the analysis. MakeCloseSynchronous is only intended for use with CLIENT_OWNS_WIDGET, and it looks like the help bubble is not yet using that:
https://source.chromium.org/chromium/chromium/src/+/main:components/user_education/views/help_bubble_views.cc;l=278?q=HelpBubbleViews&ss=chromium

In addition to fixing this error, could we update MakeCloseSynchronous to CHECK that the widget uses CLIENT_OWNS_WIDGET?

### ch...@google.com (2026-03-27)

Setting milestone because of s0/s1 severity.

### dx...@google.com (2026-03-30)

Project: chromium/src  

Branch:  main  

Author:  Elly [ellyjones@chromium.org](mailto:ellyjones@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7706718>

views: forbid destruction of Widget from Widget callbacks

---


Expand for full commit details
```
     
    This change: 
    * Adds a mechanism to Widget for CHECKing that one of its own callbacks 
      is not on the stack, and 
    * Adds some uses of that mechanisms to the highest-risk code paths 
      (which are themselves mostly around destruction) 
     
    This turns an entire class of lifetime bugs around Widget destruction 
    from use-after-frees into CHECK failures, which makes them not security 
    bugs. 
     
    If this works well, it can be extended to other Widget callbacks too. 
     
    AI-Model: none 
    Bug: 496456528 
    Change-Id: I15565c526d123c6b3501638b6e6af6cc71ed0d27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7706718 
    Commit-Queue: Elly FJ <ellyjones@chromium.org> 
    Reviewed-by: Robert Liao <robliao@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1607160}

```

---

Files:

- M `ui/views/widget/widget.cc`
- M `ui/views/widget/widget.h`

---

Hash: [6b983206a48f34c8d21ca41a456c6b8c26d15a2e](https://chromiumdash.appspot.com/commit/6b983206a48f34c8d21ca41a456c6b8c26d15a2e)  

Date: Mon Mar 30 16:37:00 2026


---

### ba...@gmail.com (2026-03-30)

Thank you for your interest and prompt response. Have a good week.


### df...@google.com (2026-04-09)

This is not a HelpBubble; it is a CustomWebUIHelpBubble, which does in fact use `CLIENT_OWNS_WIDGET`.

See: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/user_education/custom_webui_help_bubble.h;l=152>

Invoked from: <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/user_education/browser_user_education_service.cc;l=719>

They do appear to be doing everything right with this IPH, which suggests that either the `NativeWidgetMac` isn't getting properly torn down during the synchronous close, or that we need a weak reference somewhere in the callback chain:

```
    #0 0x00037ff72ba4 in views::Widget::HandleWidgetDestroying()+0x31c (/Users/beksem/chromium/src/out/Asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7751.0/Chromium Framework:arm64+0x2186eba4)
    #1 0x00037ff89b20 in views::Widget::OnNativeWidgetDestroying()+0x11c (/Users/beksem/chromium/src/out/Asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7751.0/Chromium Framework:arm64+0x21885b20)
    #2 0x00038002d9c4 in views::NativeWidgetMac::WindowDestroying()+0x184 (/Users/beksem/chromium/src/out/Asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7751.0/Chromium Framework:arm64+0x219299c4)
    #3 0x00037ffea750 in views::NativeWidgetMacNSWindowHost::OnWindowWillClose()+0x184 (/Users/beksem/chromium/src/out/Asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7751.0/Chromium Framework:arm64+0x218e6750)
    #4 0x00037c774c5c in remote_cocoa::NativeWidgetNSWindowBridge::OnWindowWillClose()+0x1b8 (/Users/beksem/chromium/src/out/Asan/Chromium.app/Contents/Frameworks/Chromium Framework.framework/Versions/148.0.7751.0/Chromium Framework:arm64+0x1e070c5c)

```

### df...@google.com (2026-04-09)

(Standard Views help bubbles not yet being migrated to `CLIENT_OWNS_WIDGET` is a separate issue that is not quite as high-priority; though the fact that `CustomWebUIHelpBubble`s already support it means one could probably make the conversion without having to re-engineer too much.)

Given this, I'm not sure what else can be done here. I'll throw in a regression test that opens a CustomWebUIHelpBubble and then closes the browser, and see what happens.

### df...@google.com (2026-04-09)

Regression test in y'all's inbox.

### df...@google.com (2026-04-09)

I will attempt to reproduce on a Mac ASAN issue ASAP; however, running the test which reproduces the steps on a Mac ASAN bot does not reproduce the crash.

### dx...@google.com (2026-04-10)

Project: chromium/src  

Branch:  main  

Author:  Dana Fried [dfried@chromium.org](mailto:dfried@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7744144>

[User Education] Regression test for issue in custom IPH teardown

---


Expand for full commit details
```
     
    Test verifies the browser can be closed while a custom WebUI IPH is 
    showing without crashing anything. 
     
    The Custom WebUI help bubble uses CLIENT_OWNS_WIDGET and 
    MakeCloseSynchronous, so it should be torn down synchronously and safely 
    on close, regardless of how that close happens. 
     
    Bug: 496456528 
    Change-Id: I1e0d06b092eb2f3dbc1c1a3d285401862f9e5f32 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744144 
    Commit-Queue: Dana Fried <dfried@chromium.org> 
    Reviewed-by: Elly FJ <ellyjones@chromium.org> 
    Auto-Submit: Dana Fried <dfried@chromium.org> 
    Reviewed-by: Erik Chen <erikchen@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1612816}

```

---

Files:

- M `chrome/browser/ui/views/user_education/custom_webui_help_bubble_interactive_uitest.cc`

---

Hash: [75b59de8d3a458b62dc1c284f1ea005df067bf01](https://chromiumdash.appspot.com/commit/75b59de8d3a458b62dc1c284f1ea005df067bf01)  

Date: Fri Apr 10 13:41:34 2026


---

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  main  

Author:  Dana Fried [dfried@chromium.org](mailto:dfried@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7744206>

[User Education] Harden help bubble teardown

---


Expand for full commit details
```
     
    This changes all Views-based help bubbles (which is nearly all of them) 
    to use MakeCloseSynchronous(). It also streamlines the teardown logic to 
    prevent UAFs: 
     - All execution paths in help bubbles that can call callbacks are 
       safe against `this` being deleted. 
     - Code paths that could be called during teardown early-exit if 
       teardown has started. 
     - Help bubble teardown can be synchronous if desired. 
     - `HelpBubbleFactoryRegistry` will no longer briefly hold a reference 
       to a help bubble that may have been deleted. 
     - HelpBubbleViewsAsh has been eliminated in favor of wrapping a 
       HelpBubbleViewAsh in a HelpBubbleViews. 
     
    This CL breaks `AddOnCloseCallback()` into `AddOnClosingCallback()` and 
    `AddOnClosedCallback()`, and uses them in the appropriate places. 
     
    Primary files to review would be: 
     - help_bubble.h|cc 
     - help_bubble_view.h|cc 
     - help_bubble_views.h|cc 
     
    The vast majority of other changes are just refactors due to API 
    changes. 
     
    In a follow-up, we may replace `AddOnCloseCallback()` with a 
    `MakeCloseSynchronous()` type method that further ties it to help bubble 
    ownership. 
     
    Bug: 496456528 
    Change-Id: Ie999b965cf40e2e091f2de99f2f7b80338bcce15 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744206 
    Commit-Queue: Dana Fried <dfried@chromium.org> 
    Reviewed-by: Elly <ellyjones@chromium.org> 
    Reviewed-by: Erik Chen <erikchen@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1614772}

```

---

Files:

- M `ash/BUILD.gn`
- M `ash/user_education/user_education_help_bubble_controller.cc`
- M `ash/user_education/user_education_help_bubble_controller.h`
- M `ash/user_education/user_education_help_bubble_controller_unittest.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.h`
- M `ash/user_education/views/help_bubble_view_ash.cc`
- M `ash/user_education/views/help_bubble_view_ash.h`
- M `ash/user_education/views/help_bubble_view_ash_pixeltest.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.h`
- M `ash/user_education/views/help_bubble_view_ash_unittest.cc`
- M `chrome/browser/ui/ash/user_education/views/help_bubble_factory_views_ash_browsertest.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page_browsertest.cc`
- M `chrome/browser/ui/views/user_education/custom_webui_help_bubble_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_views_browsertest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_webui_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_view_timeout_unittest.cc`
- M `components/user_education/common/feature_promo/feature_promo_lifecycle_unittest.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.h`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl_unittest.cc`
- M `components/user_education/common/help_bubble/help_bubble.cc`
- M `components/user_education/common/help_bubble/help_bubble.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.cc`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry_unittest.cc`
- M `components/user_education/common/tutorial/tutorial_service.cc`
- M `components/user_education/common/tutorial/tutorial_service.h`
- M `components/user_education/common/tutorial/tutorial_unittest.cc`
- M `components/user_education/test/test_help_bubble.cc`
- M `components/user_education/test/test_help_bubble.h`
- M `components/user_education/views/BUILD.gn`
- M `components/user_education/views/help_bubble_factory_mac.mm`
- M `components/user_education/views/help_bubble_factory_views.cc`
- M `components/user_education/views/help_bubble_factory_views_unittest.cc`
- M `components/user_education/views/help_bubble_view.cc`
- M `components/user_education/views/help_bubble_view.h`
- A `components/user_education/views/help_bubble_view_info.cc`
- A `components/user_education/views/help_bubble_view_info.h`
- M `components/user_education/views/help_bubble_view_unittest.cc`
- M `components/user_education/views/help_bubble_views.cc`
- M `components/user_education/views/help_bubble_views.h`
- M `components/user_education/views/help_bubble_views_unittest.cc`
- M `components/user_education/webui/help_bubble_handler.cc`
- M `components/user_education/webui/help_bubble_handler.h`
- M `components/user_education/webui/help_bubble_handler_unittest.cc`
- M `components/user_education/webui/help_bubble_webui.cc`
- M `components/user_education/webui/help_bubble_webui.h`
- M `ui/base/interaction/interaction_sequence_test_util.h`

---

Hash: [e7b909682621f1b969f7f845fc9c41728a03072c](https://chromiumdash.appspot.com/commit/e7b909682621f1b969f7f845fc9c41728a03072c)  

Date: Tue Apr 14 22:56:53 2026


---

### dx...@google.com (2026-04-15)

Project: chromium/src  

Branch:  main  

Author:  Simon Ziegltrum [ziegltrum@google.com](mailto:ziegltrum@google.com)  

Link:    <https://chromium-review.googlesource.com/7762386>

Revert "[User Education] Harden help bubble teardown"

---


Expand for full commit details
```
     
    This reverts commit e7b909682621f1b969f7f845fc9c41728a03072c. 
     
    Reason for revert: Failing tests UserEducationHelpBubbleControllerTest.Metadata All/HelpBubbleFactoryViewsAshBrowserTest.CreateBubble/1 
    Example: https://ci.chromium.org/ui/p/chromium/builders/ci/linux-chromeos-dbg/44923/overview 
     
    Original change's description: 
    > [User Education] Harden help bubble teardown 
    > 
    > This changes all Views-based help bubbles (which is nearly all of them) 
    > to use MakeCloseSynchronous(). It also streamlines the teardown logic to 
    > prevent UAFs: 
    >  - All execution paths in help bubbles that can call callbacks are 
    >    safe against `this` being deleted. 
    >  - Code paths that could be called during teardown early-exit if 
    >    teardown has started. 
    >  - Help bubble teardown can be synchronous if desired. 
    >  - `HelpBubbleFactoryRegistry` will no longer briefly hold a reference 
    >    to a help bubble that may have been deleted. 
    >  - HelpBubbleViewsAsh has been eliminated in favor of wrapping a 
    >    HelpBubbleViewAsh in a HelpBubbleViews. 
    > 
    > This CL breaks `AddOnCloseCallback()` into `AddOnClosingCallback()` and 
    > `AddOnClosedCallback()`, and uses them in the appropriate places. 
    > 
    > Primary files to review would be: 
    >  - help_bubble.h|cc 
    >  - help_bubble_view.h|cc 
    >  - help_bubble_views.h|cc 
    > 
    > The vast majority of other changes are just refactors due to API 
    > changes. 
    > 
    > In a follow-up, we may replace `AddOnCloseCallback()` with a 
    > `MakeCloseSynchronous()` type method that further ties it to help bubble 
    > ownership. 
    > 
    > Bug: 496456528 
    > Change-Id: Ie999b965cf40e2e091f2de99f2f7b80338bcce15 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744206 
    > Commit-Queue: Dana Fried <dfried@chromium.org> 
    > Reviewed-by: Elly <ellyjones@chromium.org> 
    > Reviewed-by: Erik Chen <erikchen@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1614772} 
     
    Bug: 496456528 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: I9e890e46cd13bfc1f58520eefffa11a1805e0da2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7762386 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Owners-Override: Simon Ziegltrum <ziegltrum@google.com> 
    Commit-Queue: Simon Ziegltrum <ziegltrum@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1615005}

```

---

Files:

- M `ash/BUILD.gn`
- M `ash/user_education/user_education_help_bubble_controller.cc`
- M `ash/user_education/user_education_help_bubble_controller.h`
- M `ash/user_education/user_education_help_bubble_controller_unittest.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.h`
- M `ash/user_education/views/help_bubble_view_ash.cc`
- M `ash/user_education/views/help_bubble_view_ash.h`
- M `ash/user_education/views/help_bubble_view_ash_pixeltest.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.h`
- M `ash/user_education/views/help_bubble_view_ash_unittest.cc`
- M `chrome/browser/ui/ash/user_education/views/help_bubble_factory_views_ash_browsertest.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page_browsertest.cc`
- M `chrome/browser/ui/views/user_education/custom_webui_help_bubble_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_views_browsertest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_webui_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_view_timeout_unittest.cc`
- M `components/user_education/common/feature_promo/feature_promo_lifecycle_unittest.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.h`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl_unittest.cc`
- M `components/user_education/common/help_bubble/help_bubble.cc`
- M `components/user_education/common/help_bubble/help_bubble.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.cc`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry_unittest.cc`
- M `components/user_education/common/tutorial/tutorial_service.cc`
- M `components/user_education/common/tutorial/tutorial_service.h`
- M `components/user_education/common/tutorial/tutorial_unittest.cc`
- M `components/user_education/test/test_help_bubble.cc`
- M `components/user_education/test/test_help_bubble.h`
- M `components/user_education/views/BUILD.gn`
- M `components/user_education/views/help_bubble_factory_mac.mm`
- M `components/user_education/views/help_bubble_factory_views.cc`
- M `components/user_education/views/help_bubble_factory_views_unittest.cc`
- M `components/user_education/views/help_bubble_view.cc`
- M `components/user_education/views/help_bubble_view.h`
- D `components/user_education/views/help_bubble_view_info.cc`
- D `components/user_education/views/help_bubble_view_info.h`
- M `components/user_education/views/help_bubble_view_unittest.cc`
- M `components/user_education/views/help_bubble_views.cc`
- M `components/user_education/views/help_bubble_views.h`
- M `components/user_education/views/help_bubble_views_unittest.cc`
- M `components/user_education/webui/help_bubble_handler.cc`
- M `components/user_education/webui/help_bubble_handler.h`
- M `components/user_education/webui/help_bubble_handler_unittest.cc`
- M `components/user_education/webui/help_bubble_webui.cc`
- M `components/user_education/webui/help_bubble_webui.h`
- M `ui/base/interaction/interaction_sequence_test_util.h`

---

Hash: [ba9f9ef4244dd3a351ee3d57a00ce4edb5821b8f](https://chromiumdash.appspot.com/commit/ba9f9ef4244dd3a351ee3d57a00ce4edb5821b8f)  

Date: Wed Apr 15 08:55:30 2026


---

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  main  

Author:  Dana Fried [dfried@chromium.org](mailto:dfried@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7765574>

Reland "[User Education] Harden help bubble teardown"

---


Expand for full commit details
```
     
    This reverts commit ba9f9ef4244dd3a351ee3d57a00ce4edb5821b8f. 
     
    Reason for revert: Fixed tests on linux-chromeos-debug CI builder. 
     
    Tests on that builder are one of the few component builds left in 
    Desktop chrome; the tests were using metadata that was not component 
    build safe. We added back in the HelpBubbleViewsAsh class to make those 
    tests safe on that builder. This should not appreciably affect 
    production Chrome. 
     
    Original change's description: 
    > Revert "[User Education] Harden help bubble teardown" 
    > 
    > This reverts commit e7b909682621f1b969f7f845fc9c41728a03072c. 
    > 
    > Reason for revert: Failing tests UserEducationHelpBubbleControllerTest.Metadata All/HelpBubbleFactoryViewsAshBrowserTest.CreateBubble/1 
    > Example: https://ci.chromium.org/ui/p/chromium/builders/ci/linux-chromeos-dbg/44923/overview 
    > 
    > Original change's description: 
    > > [User Education] Harden help bubble teardown 
    > > 
    > > This changes all Views-based help bubbles (which is nearly all of them) 
    > > to use MakeCloseSynchronous(). It also streamlines the teardown logic to 
    > > prevent UAFs: 
    > >  - All execution paths in help bubbles that can call callbacks are 
    > >    safe against `this` being deleted. 
    > >  - Code paths that could be called during teardown early-exit if 
    > >    teardown has started. 
    > >  - Help bubble teardown can be synchronous if desired. 
    > >  - `HelpBubbleFactoryRegistry` will no longer briefly hold a reference 
    > >    to a help bubble that may have been deleted. 
    > >  - HelpBubbleViewsAsh has been eliminated in favor of wrapping a 
    > >    HelpBubbleViewAsh in a HelpBubbleViews. 
    > > 
    > > This CL breaks `AddOnCloseCallback()` into `AddOnClosingCallback()` and 
    > > `AddOnClosedCallback()`, and uses them in the appropriate places. 
    > > 
    > > Primary files to review would be: 
    > >  - help_bubble.h|cc 
    > >  - help_bubble_view.h|cc 
    > >  - help_bubble_views.h|cc 
    > > 
    > > The vast majority of other changes are just refactors due to API 
    > > changes. 
    > > 
    > > In a follow-up, we may replace `AddOnCloseCallback()` with a 
    > > `MakeCloseSynchronous()` type method that further ties it to help bubble 
    > > ownership. 
    > > 
    > > Bug: 496456528 
    > > Change-Id: Ie999b965cf40e2e091f2de99f2f7b80338bcce15 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744206 
    > > Commit-Queue: Dana Fried <dfried@chromium.org> 
    > > Reviewed-by: Elly <ellyjones@chromium.org> 
    > > Reviewed-by: Erik Chen <erikchen@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1614772} 
    > 
    > Bug: 496456528 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I9e890e46cd13bfc1f58520eefffa11a1805e0da2 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7762386 
    > Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    > Owners-Override: Simon Ziegltrum <ziegltrum@google.com> 
    > Commit-Queue: Simon Ziegltrum <ziegltrum@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1615005} 
     
    Bug: 496456528 
    Change-Id: Ib602979553a5cd8d257c317834258625fb8ca763 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7765574 
    Reviewed-by: Darryl James <dljames@chromium.org> 
    Auto-Submit: Dana Fried <dfried@chromium.org> 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Commit-Queue: Dana Fried <dfried@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1616015}

```

---

Files:

- M `ash/BUILD.gn`
- M `ash/user_education/user_education_help_bubble_controller.cc`
- M `ash/user_education/user_education_help_bubble_controller.h`
- M `ash/user_education/user_education_help_bubble_controller_unittest.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.h`
- M `ash/user_education/views/help_bubble_view_ash.cc`
- M `ash/user_education/views/help_bubble_view_ash.h`
- M `ash/user_education/views/help_bubble_view_ash_pixeltest.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.h`
- M `ash/user_education/views/help_bubble_view_ash_unittest.cc`
- M `chrome/browser/ui/ash/user_education/views/help_bubble_factory_views_ash_browsertest.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page_browsertest.cc`
- M `chrome/browser/ui/views/user_education/custom_webui_help_bubble_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_views_browsertest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_webui_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_view_timeout_unittest.cc`
- M `components/user_education/common/feature_promo/feature_promo_lifecycle_unittest.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.h`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl_unittest.cc`
- M `components/user_education/common/help_bubble/help_bubble.cc`
- M `components/user_education/common/help_bubble/help_bubble.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.cc`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry_unittest.cc`
- M `components/user_education/common/tutorial/tutorial_service.cc`
- M `components/user_education/common/tutorial/tutorial_service.h`
- M `components/user_education/common/tutorial/tutorial_unittest.cc`
- M `components/user_education/test/test_help_bubble.cc`
- M `components/user_education/test/test_help_bubble.h`
- M `components/user_education/views/BUILD.gn`
- M `components/user_education/views/help_bubble_factory_mac.mm`
- M `components/user_education/views/help_bubble_factory_views.cc`
- M `components/user_education/views/help_bubble_factory_views_unittest.cc`
- M `components/user_education/views/help_bubble_view.cc`
- M `components/user_education/views/help_bubble_view.h`
- A `components/user_education/views/help_bubble_view_info.cc`
- A `components/user_education/views/help_bubble_view_info.h`
- M `components/user_education/views/help_bubble_view_unittest.cc`
- M `components/user_education/views/help_bubble_views.cc`
- M `components/user_education/views/help_bubble_views.h`
- M `components/user_education/views/help_bubble_views_unittest.cc`
- M `components/user_education/webui/help_bubble_handler.cc`
- M `components/user_education/webui/help_bubble_handler.h`
- M `components/user_education/webui/help_bubble_handler_unittest.cc`
- M `components/user_education/webui/help_bubble_webui.cc`
- M `components/user_education/webui/help_bubble_webui.h`
- M `ui/base/interaction/interaction_sequence_test_util.h`

---

Hash: [62fb787c83e538d31a5aebe8cf402f340f5f06fd](https://chromiumdash.appspot.com/commit/62fb787c83e538d31a5aebe8cf402f340f5f06fd)  

Date: Thu Apr 16 18:28:22 2026


---

### ch...@google.com (2026-04-16)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2026-04-19)

Requesting merge to M146 because latest trunk commit (1614772) appears to be after M146 branch point (1582197).

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M147 because latest trunk commit (1614772) appears to be after M147 branch point (1596535).

Requesting merge to M148 because latest trunk commit (1614772) appears to be after M148 branch point (1610480).

### ch...@google.com (2026-04-19)

**M146** merge request created. **Please update [crbug/504232802](https://crbug.com/504232802) to have this merge reviewed.**

### ch...@google.com (2026-04-19)

**M147** merge request created. **Please update [crbug/504233802](https://crbug.com/504233802) to have this merge reviewed.**

### ch...@google.com (2026-04-19)

**M148** merge request created. **Please update [crbug/504234053](https://crbug.com/504234053) to have this merge reviewed.**

### ba...@gmail.com (2026-04-21)

Thanks for the updates and work, I hope I can win a nice prize.


### df...@google.com (2026-04-21)

I'm not sure that these changes can be merged back. We'll see what happens.

### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  refs/branch-heads/7727  

Author:  Dana Fried [dfried@chromium.org](mailto:dfried@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7792918>

[147] "[User Education] Harden help bubble teardown"

---


Expand for full commit details
```
     
    This reverts commit ba9f9ef4244dd3a351ee3d57a00ce4edb5821b8f. 
     
    Reason for revert: Fixed tests on linux-chromeos-debug CI builder. 
     
    Tests on that builder are one of the few component builds left in 
    Desktop chrome; the tests were using metadata that was not component 
    build safe. We added back in the HelpBubbleViewsAsh class to make those 
    tests safe on that builder. This should not appreciably affect 
    production Chrome. 
     
    Original change's description: 
    > Revert "[User Education] Harden help bubble teardown" 
    > 
    > This reverts commit e7b909682621f1b969f7f845fc9c41728a03072c. 
    > 
    > Reason for revert: Failing tests UserEducationHelpBubbleControllerTest.Metadata All/HelpBubbleFactoryViewsAshBrowserTest.CreateBubble/1 
    > Example: https://ci.chromium.org/ui/p/chromium/builders/ci/linux-chromeos-dbg/44923/overview 
    > 
    > Original change's description: 
    > > [User Education] Harden help bubble teardown 
    > > 
    > > This changes all Views-based help bubbles (which is nearly all of them) 
    > > to use MakeCloseSynchronous(). It also streamlines the teardown logic to 
    > > prevent UAFs: 
    > >  - All execution paths in help bubbles that can call callbacks are 
    > >    safe against `this` being deleted. 
    > >  - Code paths that could be called during teardown early-exit if 
    > >    teardown has started. 
    > >  - Help bubble teardown can be synchronous if desired. 
    > >  - `HelpBubbleFactoryRegistry` will no longer briefly hold a reference 
    > >    to a help bubble that may have been deleted. 
    > >  - HelpBubbleViewsAsh has been eliminated in favor of wrapping a 
    > >    HelpBubbleViewAsh in a HelpBubbleViews. 
    > > 
    > > This CL breaks `AddOnCloseCallback()` into `AddOnClosingCallback()` and 
    > > `AddOnClosedCallback()`, and uses them in the appropriate places. 
    > > 
    > > Primary files to review would be: 
    > >  - help_bubble.h|cc 
    > >  - help_bubble_view.h|cc 
    > >  - help_bubble_views.h|cc 
    > > 
    > > The vast majority of other changes are just refactors due to API 
    > > changes. 
    > > 
    > > In a follow-up, we may replace `AddOnCloseCallback()` with a 
    > > `MakeCloseSynchronous()` type method that further ties it to help bubble 
    > > ownership. 
    > > 
    > > Bug: 496456528 
    > > Change-Id: Ie999b965cf40e2e091f2de99f2f7b80338bcce15 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744206 
    > > Commit-Queue: Dana Fried <dfried@chromium.org> 
    > > Reviewed-by: Elly <ellyjones@chromium.org> 
    > > Reviewed-by: Erik Chen <erikchen@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1614772} 
    > 
    > Bug: 496456528 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I9e890e46cd13bfc1f58520eefffa11a1805e0da2 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7762386 
    > Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    > Owners-Override: Simon Ziegltrum <ziegltrum@google.com> 
    > Commit-Queue: Simon Ziegltrum <ziegltrum@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1615005} 
     
    (cherry picked from commit 62fb787c83e538d31a5aebe8cf402f340f5f06fd) 
     
    Bug: 496456528 
    Fixed: 504233802 
    Change-Id: Ib602979553a5cd8d257c317834258625fb8ca763 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7765574 
    Reviewed-by: Darryl James <dljames@chromium.org> 
    Auto-Submit: Dana Fried <dfried@chromium.org> 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Commit-Queue: Dana Fried <dfried@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1616015} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7792918 
    Reviewed-by: Muhammad Salmaan <musalmaan@chromium.org> 
    Reviewed-by: Foromo Daniel Soromou <koretadaniel@chromium.org> 
    Commit-Queue: Foromo Daniel Soromou <koretadaniel@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7727@{#3842} 
    Cr-Branched-From: ce01102937348db7b88c8a4257ee4b3ac702eb1a-refs/heads/main@{#1596535}

```

---

Files:

- M `ash/BUILD.gn`
- M `ash/user_education/user_education_help_bubble_controller.cc`
- M `ash/user_education/user_education_help_bubble_controller.h`
- M `ash/user_education/user_education_help_bubble_controller_unittest.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.h`
- M `ash/user_education/views/help_bubble_view_ash.cc`
- M `ash/user_education/views/help_bubble_view_ash.h`
- M `ash/user_education/views/help_bubble_view_ash_pixeltest.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.h`
- M `ash/user_education/views/help_bubble_view_ash_unittest.cc`
- M `chrome/browser/ui/ash/user_education/views/help_bubble_factory_views_ash_browsertest.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page_browsertest.cc`
- M `chrome/browser/ui/views/user_education/custom_webui_help_bubble_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_views_browsertest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_webui_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_view_timeout_unittest.cc`
- M `components/user_education/common/feature_promo/feature_promo_lifecycle_unittest.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.h`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl_unittest.cc`
- M `components/user_education/common/help_bubble/help_bubble.cc`
- M `components/user_education/common/help_bubble/help_bubble.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.cc`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry_unittest.cc`
- M `components/user_education/common/tutorial/tutorial_service.cc`
- M `components/user_education/common/tutorial/tutorial_service.h`
- M `components/user_education/common/tutorial/tutorial_unittest.cc`
- M `components/user_education/test/test_help_bubble.cc`
- M `components/user_education/test/test_help_bubble.h`
- M `components/user_education/views/BUILD.gn`
- M `components/user_education/views/help_bubble_factory_mac.mm`
- M `components/user_education/views/help_bubble_factory_views.cc`
- M `components/user_education/views/help_bubble_factory_views_unittest.cc`
- M `components/user_education/views/help_bubble_view.cc`
- M `components/user_education/views/help_bubble_view.h`
- A `components/user_education/views/help_bubble_view_info.cc`
- A `components/user_education/views/help_bubble_view_info.h`
- M `components/user_education/views/help_bubble_view_unittest.cc`
- M `components/user_education/views/help_bubble_views.cc`
- M `components/user_education/views/help_bubble_views.h`
- M `components/user_education/views/help_bubble_views_unittest.cc`
- M `components/user_education/webui/help_bubble_handler.cc`
- M `components/user_education/webui/help_bubble_handler.h`
- M `components/user_education/webui/help_bubble_handler_unittest.cc`
- M `components/user_education/webui/help_bubble_webui.cc`
- M `components/user_education/webui/help_bubble_webui.h`
- M `ui/base/interaction/interaction_sequence_test_util.h`

---

Hash: [22fcaa0ec583c8a27c3bf55c78f0883ab9b39911](https://chromiumdash.appspot.com/commit/22fcaa0ec583c8a27c3bf55c78f0883ab9b39911)  

Date: Mon Apr 27 14:54:27 2026


---

### ba...@gmail.com (2026-04-27)

Hi again, I haven't been able to pay much attention lately due to some work commitments, but I've finally found some time. If you'd like to reproduce the issue locally, please apply the patch below and launch Chrome in its simplest form. After the help bubble appears, close the tab.  Changes made:

extensions_toolbar_desktop.cc — Forces the ZeroState promo bubble to appear every time Chromium starts, bypassing all conditions and timers. In the original code, the extension had to be uninstalled, promotions had to be active, and the timer had to have passed for the bubble to appear. This patch removes all conditions and triggers the bubble with guaranteed results.

git checkout 53229ae9ce8b1 — go to this commit
Implement the poc_reproduce.patch process: git application poc_reproduce.patch
Compile with ASAN build.
Launch Chromium ASAN_OPTIONS="detect_leaks=0:symbolize=1" ./out/Asan/Chromium.app/Contents/MacOS/Chromium
Close the tab two seconds after you see the help bubble.



### dx...@google.com (2026-04-27)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  Dana Fried [dfried@chromium.org](mailto:dfried@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7791140>

[148] "[User Education] Harden help bubble teardown"

---


Expand for full commit details
```
     
    This reverts commit ba9f9ef4244dd3a351ee3d57a00ce4edb5821b8f. 
     
    Reason for revert: Fixed tests on linux-chromeos-debug CI builder. 
     
    Tests on that builder are one of the few component builds left in 
    Desktop chrome; the tests were using metadata that was not component 
    build safe. We added back in the HelpBubbleViewsAsh class to make those 
    tests safe on that builder. This should not appreciably affect 
    production Chrome. 
     
    Original change's description: 
    > Revert "[User Education] Harden help bubble teardown" 
    > 
    > This reverts commit e7b909682621f1b969f7f845fc9c41728a03072c. 
    > 
    > Reason for revert: Failing tests UserEducationHelpBubbleControllerTest.Metadata All/HelpBubbleFactoryViewsAshBrowserTest.CreateBubble/1 
    > Example: https://ci.chromium.org/ui/p/chromium/builders/ci/linux-chromeos-dbg/44923/overview 
    > 
    > Original change's description: 
    > > [User Education] Harden help bubble teardown 
    > > 
    > > This changes all Views-based help bubbles (which is nearly all of them) 
    > > to use MakeCloseSynchronous(). It also streamlines the teardown logic to 
    > > prevent UAFs: 
    > >  - All execution paths in help bubbles that can call callbacks are 
    > >    safe against `this` being deleted. 
    > >  - Code paths that could be called during teardown early-exit if 
    > >    teardown has started. 
    > >  - Help bubble teardown can be synchronous if desired. 
    > >  - `HelpBubbleFactoryRegistry` will no longer briefly hold a reference 
    > >    to a help bubble that may have been deleted. 
    > >  - HelpBubbleViewsAsh has been eliminated in favor of wrapping a 
    > >    HelpBubbleViewAsh in a HelpBubbleViews. 
    > > 
    > > This CL breaks `AddOnCloseCallback()` into `AddOnClosingCallback()` and 
    > > `AddOnClosedCallback()`, and uses them in the appropriate places. 
    > > 
    > > Primary files to review would be: 
    > >  - help_bubble.h|cc 
    > >  - help_bubble_view.h|cc 
    > >  - help_bubble_views.h|cc 
    > > 
    > > The vast majority of other changes are just refactors due to API 
    > > changes. 
    > > 
    > > In a follow-up, we may replace `AddOnCloseCallback()` with a 
    > > `MakeCloseSynchronous()` type method that further ties it to help bubble 
    > > ownership. 
    > > 
    > > Bug: 496456528 
    > > Change-Id: Ie999b965cf40e2e091f2de99f2f7b80338bcce15 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7744206 
    > > Commit-Queue: Dana Fried <dfried@chromium.org> 
    > > Reviewed-by: Elly <ellyjones@chromium.org> 
    > > Reviewed-by: Erik Chen <erikchen@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1614772} 
    > 
    > Bug: 496456528 
    > No-Presubmit: true 
    > No-Tree-Checks: true 
    > No-Try: true 
    > Change-Id: I9e890e46cd13bfc1f58520eefffa11a1805e0da2 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7762386 
    > Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    > Owners-Override: Simon Ziegltrum <ziegltrum@google.com> 
    > Commit-Queue: Simon Ziegltrum <ziegltrum@google.com> 
    > Cr-Commit-Position: refs/heads/main@{#1615005} 
     
    (cherry picked from commit 62fb787c83e538d31a5aebe8cf402f340f5f06fd) 
     
    Bug: 496456528 
    Fixed: 504234053 
    Change-Id: Ib602979553a5cd8d257c317834258625fb8ca763 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7765574 
    Reviewed-by: Darryl James <dljames@chromium.org> 
    Auto-Submit: Dana Fried <dfried@chromium.org> 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Commit-Queue: Dana Fried <dfried@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1616015} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7791140 
    Reviewed-by: Muhammad Salmaan <musalmaan@chromium.org> 
    Reviewed-by: Foromo Daniel Soromou <koretadaniel@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7778@{#1772} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `ash/BUILD.gn`
- M `ash/user_education/user_education_help_bubble_controller.cc`
- M `ash/user_education/user_education_help_bubble_controller.h`
- M `ash/user_education/user_education_help_bubble_controller_unittest.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.cc`
- M `ash/user_education/views/help_bubble_factory_views_ash.h`
- M `ash/user_education/views/help_bubble_view_ash.cc`
- M `ash/user_education/views/help_bubble_view_ash.h`
- M `ash/user_education/views/help_bubble_view_ash_pixeltest.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.cc`
- M `ash/user_education/views/help_bubble_view_ash_test_base.h`
- M `ash/user_education/views/help_bubble_view_ash_unittest.cc`
- M `chrome/browser/ui/ash/user_education/views/help_bubble_factory_views_ash_browsertest.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page.cc`
- M `chrome/browser/ui/user_education/show_promo_in_page_browsertest.cc`
- M `chrome/browser/ui/views/user_education/custom_webui_help_bubble_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_views_browsertest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_factory_webui_interactive_uitest.cc`
- M `chrome/browser/ui/views/user_education/help_bubble_view_timeout_unittest.cc`
- M `components/user_education/common/feature_promo/feature_promo_lifecycle_unittest.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.cc`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl.h`
- M `components/user_education/common/feature_promo/impl/feature_promo_controller_impl_unittest.cc`
- M `components/user_education/common/help_bubble/help_bubble.cc`
- M `components/user_education/common/help_bubble/help_bubble.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.cc`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry.h`
- M `components/user_education/common/help_bubble/help_bubble_factory_registry_unittest.cc`
- M `components/user_education/common/tutorial/tutorial_service.cc`
- M `components/user_education/common/tutorial/tutorial_service.h`
- M `components/user_education/common/tutorial/tutorial_unittest.cc`
- M `components/user_education/test/test_help_bubble.cc`
- M `components/user_education/test/test_help_bubble.h`
- M `components/user_education/views/BUILD.gn`
- M `components/user_education/views/help_bubble_factory_mac.mm`
- M `components/user_education/views/help_bubble_factory_views.cc`
- M `components/user_education/views/help_bubble_factory_views_unittest.cc`
- M `components/user_education/views/help_bubble_view.cc`
- M `components/user_education/views/help_bubble_view.h`
- A `components/user_education/views/help_bubble_view_info.cc`
- A `components/user_education/views/help_bubble_view_info.h`
- M `components/user_education/views/help_bubble_view_unittest.cc`
- M `components/user_education/views/help_bubble_views.cc`
- M `components/user_education/views/help_bubble_views.h`
- M `components/user_education/views/help_bubble_views_unittest.cc`
- M `components/user_education/webui/help_bubble_handler.cc`
- M `components/user_education/webui/help_bubble_handler.h`
- M `components/user_education/webui/help_bubble_handler_unittest.cc`
- M `components/user_education/webui/help_bubble_webui.cc`
- M `components/user_education/webui/help_bubble_webui.h`
- M `ui/base/interaction/interaction_sequence_test_util.h`

---

Hash: [84ffbba0b543b09ee98c0121051b875ee29b8ca5](https://chromiumdash.appspot.com/commit/84ffbba0b543b09ee98c0121051b875ee29b8ca5)  

Date: Mon Apr 27 18:23:25 2026


---

### ba...@gmail.com (2026-04-28)

Also, regarding el...@chromium.org's comment that "it's unclear how UaF will have control over processed data," I've done some work on that and found that the write operation was successful.
Although there is only a small offset difference at the moment, I have confirmed that the crash address is 4141414141414451.


Received signal 11 SEGV_ACCERR 4141414141414451
 [0x00012ce2fde8]
 [0x00012ce22cac]
 [0x00012ce2fd3c]
 [0x0001832d3744]
 [0x00012fab1e64]
 [0x00012fadf470]
 [0x00012fad04ec]
 [0x00012eb59fa8]
 [0x00012eb5ebcc]
 [0x00018335f484]
 [0x0001833c3f34]
 [0x0001833c3e78]
 [0x00018333df9c]
 [0x00018555f308]
 [0x000188460a54]
 [0x0001878986d4]
 [0x00012eb50494]
 [0x00012eb58a28]
 [0x00012facd2ac]
 [0x00012fab4a98]
 [0x00012fab2314]
 [0x000132e56290]
 [0x000132e563ec]
 [0x000132ba37b4]
 [0x000132ba3d84]
 [0x000132bc8b20]
 [0x00012cdce1ac]
 [0x00012cde8e68]
 [0x00012cde8a20]
 [0x00012ce3aa30]
 [0x00012ce36068]
 [0x00012ce3a1a0]
 [0x0001833689e8]
 [0x00018336897c]
 [0x0001833686e8]
 [0x000183367378]
 [0x00018342135c]
 [0x00018fe24768]
 [0x00018fe27a90]
 [0x00018ffb1308]
 [0x000187c783c0]
 [0x000187771e34]
 [0x00018823ff44]
 [0x00018823fc50]
 [0x00012cb2d0f8]
 [0x00012ce36068]
 [0x00012cb2d040]
 [0x00018776a780]
 [0x00012ce3b104]
 [0x00012ce39b14]
 [0x00012cde94dc]
 [0x00012cdaef1c]
 [0x00012a0b908c]
 [0x00012a0ba8d0]
 [0x00012a0b67c4]
 [0x00012bdf4e0c]
 [0x00012bdf629c]
 [0x00012bdf5d90]
 [0x00012bdf43c8]
 [0x00012bdf4588]
 [0x000127608ee8]
 [0x0001048f48d8]
 [0x000182f01d54]
[end of stack trace]
[0428/120945.458870:WARNING:third_party/crashpad/crashpad/util/process/process_memory_mac.cc:94] mach_vm_read(0x16b508000, 0x8000): (os/kern) invalid address (1)
zsh: segmentation fault  ./out/Release/Chromium.app/Contents/MacOS/Chromium ~/Desktop/spray_poc5.html 

### ba...@gmail.com (2026-04-28)

Thread 0 crashed with ARM Thread State (64-bit):
    x0: 0x4141414141414141   x1: 0x0000000000000000   x2: 0x00000000000120a8   x3: 0x00000001efc9d790
    x4: 0x000001140b3df240   x5: 0x0000000000000000   x6: 0x0000000000000000   x7: 0x0000000000000000
    x8: 0x0000000000000000   x9: 0x00000001efca21f0  x10: 0x0000000000000002  x11: 0x0000010000000000
   x12: 0x00000000fffffffd  x13: 0x0000000000000000  x14: 0x0000000000000000  x15: 0x0000000000000000
   x16: 0x0000000183287608  x17: 0x00000001f12912b0  x18: 0x0000000000000000  x19: 0x0000011408e8cf00
   x20: 0x000001140a330000  x21: 0x000001140ce63e80  x22: 0x0000000000000000  x23: 0x00000110000102a0
   x24: 0x0000000000000000  x25: 0x0000000000041400  x26: 0x0000000000000000  x27: 0x000000fd000000f4
   x28: 0x000000016b507a48   fp: 0x000000016b507840   lr: 0x000000012fab1e64
    sp: 0x000000016b507820   pc: 0x000000012fac7b94 cpsr: 0x20000000
   far: 0x0000000000000000  esr: 0x56000080 (Syscall)


### df...@google.com (2026-04-28)

Thank you for the information. We have patched across all versions where it was possible to, which includes current stable.

### ba...@gmail.com (2026-04-28)

Yes, I saw it. Thank you for your work and interest. As I mentioned in my comment, "it's unclear how UaF will have control over processed data," this was a study I conducted as proof of impact and exploitability. I updated it because I needed to prove it myself. It's a bit late because I'm still in the development phase, improving myself in this field, and I'm very new to it. 
I request that evidence of impact be considered in the award decision. Thank you everyone.


### aj...@google.com (2026-05-06)

Severity Medium as this requires browser shutdown.

### ba...@gmail.com (2026-05-06)

Hello again, I do not agree with your opinion, and as stated in the first comment,

JS can use window.close() 


 el...@chromium.org<el...@chromium.org> #2Mar 26, 2026 11:53PM
Assigned to df...@chromium.org.
Security shepherd: thanks for the report.

So, I cannot actually reproduce this locally - getting the IPH bubble to show up reliably is itself challenging. However, I find the ASAN stack attached to the report very convincing, so thank you for that. I agree with your analysis also - during BrowserWidget::~BrowserWidget() we're (ultimately) destroying a BubbleWidget too early.

From the ASAN stack, it sort of looks like we're in Widget::HandleWidgetDestroying() for the BubbleWidget, but the MakeCloseSynchronous() path (which we reach there) causes the Widget to be destroyed while we're still in the middle of HandleWidgetDestroying (!) with dire consequences. It does not seem safe to enter the synchronous close path from inside HandleWidgetDestroying like this.

I'm going to call this Sev-1 since, while it is a web-reachable UaF (JS can use window.close() to provoke this code path), it's very unreliable to actually trigger it and not clear how an attacker would get any control over the data being UaFed.
 
Over to dfried@ from //components/user_education/OWNERS. 

### ba...@gmail.com (2026-05-06)

Hello,

I respectfully disagree with the S2 downgrade. As noted in comment #2 by el...@chromium.org:
"This is a web-accessible UaF (JavaScript can trigger this code path using window.close())"
This was explicitly identified as S1 by the original security reviewer. The bug does not require the user to manually close the browser — a malicious web page can trigger this code path programmatically via JavaScript's window.close(). No user interaction beyond visiting a page is required.
Additionally, I have provided proof of write control (x0: 0x4141414141414141) in comment #28, which further demonstrates exploitability.
I kindly request reconsideration of the severity back to S1, as the triggering condition is web-accessible and does not depend solely on the user closing the browser manually.
Thank you for your time.

### sp...@google.com (2026-05-06)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Moderately mitigated (non-sandboxed) 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ba...@gmail.com (2026-05-06)

I respectfully disagree with this reward decision. In comment #2, the original security reviewer explicitly stated: "This is a web-accessible UaF (JavaScript can trigger this code path using window.close())" and assigned S1 severity.
The downgrade to S2 appears inconsistent with this initial assessment. Additionally, I provided proof of write control (x0: 0x4141414141414141) in comment #28, demonstrating exploitability beyond a simple crash.
I kindly request the panel to reconsider this reward in light of the S1 assessment and the write control demonstration. 

### ba...@gmail.com (2026-05-07)


Hello again, esteemed VRP Jury Members. 

I added my report to the Award appeals list because...
  
First, when I look at the Policy documents, there is an explanation like "https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md" "Critical severity (S0)
Critical severity (S0) issues allow an attacker to read or write arbitrary resources (including but not limited to the file system, registry, network, etc.) on the underlying platform, with the user's full privileges.

Example bugs:

"Memory corruption in the browser process (319125) which is directly or indirectly reachable from web content." 
Based on this statement, my report's rating is clearly stated as "S0" according to your own policies and documents. 

However, looking at comment number 2, my report was initially assigned "S1", whereas overall, considering the document, this report should have been "S0". Let's say there's a mitigating circumstance due to the irregular display of the promotional balloon, and therefore it was assigned "S1".

our comment, "Comment number 2," clearly states that this is accessible to you via the web, occurs in the browser, and can be triggered with "JavaScript, window.close()" without requiring user interaction with JS

It seems contradictory to me that my report was labeled "S1" for almost 40 days and then changed to "S2" just 30 minutes before the reward was issued.

Please don't take my criticism here personally; your professionalism is undeniable, but there may have been some oversights.

Considering your assessment, the report was assigned as S1; however, based on the document's findings, the report should be S0.

If we reduce the rating by one degree due to the irregularity in the balloon representation, the S1 assignment in the second comment was the correct decision.

Another point is that I submitted controlled write evidence in my report; yes, I did this after it was forwarded to the reward panel, before the reward was given, but I provided everything as evidence, including the crash address and the reconstruction steps.

Looking at the reports in general, after the award was challenged, more detailed analyses showed the effects and the award rates were significantly increased, with some researchers receiving substantial additional awards.

If you tell me, "You've demonstrated that you performed a controlled write operation after submitting it to the rewards panel," when I review the reports, I see that many reports based on fundamental memory corruption in unprotected browser operations accessible via the web have received rewards of at least $30,000.

Thank you for your understanding and your time. I apologize if my tone was inappropriate; this is not due to any disrespect, but rather to my insufficient level of English.
 Best regards
Batuhan Eşref KOÇ

### aj...@google.com (2026-05-07)

Returning to the panel for further consideration, see comment 36.

### aj...@google.com (2026-05-12)

The panel has reviewed the issue and believes it is heavily mitigated in practice, so the reward is correct.

### ba...@gmail.com (2026-05-12)

Thank you


### ch...@google.com (2026-08-14)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496456528)*
