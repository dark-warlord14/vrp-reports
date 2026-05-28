# Security: Compromised renderer can control mouse after single tap (UXSS, sandbox escape, and more)

| Field | Value |
|-------|-------|
| **Issue ID** | [447172715](https://issues.chromium.org/issues/447172715) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Views |
| **Platforms** | Windows |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | da...@chromium.org |
| **Created** | 2025-09-25 |
| **Bounty** | $30,000.00 |

## Description

## SUMMARY

Similar to [issue 370856871](https://issues.chromium.org/issues/370856871), on Windows a compromised renderer can call `StartDragging()` to control the mouse and perform clicks. The existing mitigations can be bypassed after a single user tap until browser shutdown, allowing for many of the same impacts as the referenced issue. After the initial tap, all attacks can be performed an infinite amount of times, in any combination, at any time (such as when user is away from computer).

Standalone, we have a one-tap sandbox escape, UXSS, and other impacts.

When chained with other vulnerabilities, we have a one-tap sandbox escape with Mark of the Web (MOTW) bypass. I'll post the chain in comments.

## VULNERABILITY DETAILS

### Background

A compromised renderer can call [`RFHI::StartDragging()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=797;drc=f98c3dd3dc0193d10d5cfe549c98e2651244d567), which eventually calls [`WebContentsViewAura::StartDragging()`](https://source.chromium.org/chromium/chromium/src/+/main:content/browser/web_contents/web_contents_view_aura.cc;l=1108;drc=181e7a80687c55d02e2e74d7d5db3d75ad53c0de) which ultimately calls [`DesktopDragDropClientWin::StartDragAndDrop()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc;l=68;drc=181e7a80687c55d02e2e74d7d5db3d75ad53c0de).

`StartDragAndDrop()` performs mouse clicks through OS API calls in [`DesktopWindowTreeHostWin::StartTouchDrag() + ::FinishTouchDrag()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_window_tree_host_win.cc;l=151-167;drc=0540bffebe0ced2a9ad02793b159a8af1a930b31) and also calls the OS `::DoDragDrop()` method.

Important concept: An `aura::Window` "represents virtual windows, including tabs, bubbles and menus" (source: [crbug comment](https://issues.chromium.org/issues/40053103#comment48)). It doesn't always correspond to what a user typically considers a window. As a mental shortcut, in the main browser window, any UI that is typically visible immediately after navigating to a web page is likely within the same window as the web page content.

### Bugs in existing mitigations

The fix for [issue 370856871](https://issues.chromium.org/issues/370856871) [added two checks](https://chromium-review.googlesource.com/c/chromium/src/+/5943487) within `StartDragAndDrop()`:

1. `touch_down` mitigation: Checks if Aura [`is_touch_down()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/env.h;l=97;drc=89f6321d4c72ccc4b16de1d3e700e66b878e624b) returns true. This will return true if on any `aura::Window`, a touch was started (`kTouchPressed`) but has not finished (`kTouchReleased`) or cancelled (`kTouchCancelled`). Aura only [tracks touches](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/env_input_state_controller.cc;l=46-60;drc=181e7a80687c55d02e2e74d7d5db3d75ad53c0de) initiated by physical touch, privileged CDP client, or OS input APIs.
2. `touch_over_other_window` mitigation: Checks if cursor is over the current `aura::Window`. This fails if it's over a non-`aura::Window` or a different `aura::Window`.

Unfortunately, bugs prevent both of these mitigations from working as intended. There are also no restrictions on drag/clicks within the same `aura::Window`, which can still have serious impacts.

```
  if (source == ui::mojom::DragEventSource::kTouch) {
    // ...
    aura::Window* window =
        screen->GetWindowAtScreenPoint(screen->GetCursorScreenPoint());  // <-- Gets window at cursor (cursor is not necessarily at touch_screen_point)
    // ...
    bool touch_down = aura::Env::GetInstance()->is_touch_down();
    bool touch_over_other_window =
        !window || window->GetRootWindow() != root_window;
    // Check that the cursor is over the window being dragged from. If not,
    // don't start the drag because ::DoDragDrop will not do the drag.
    if (!touch_down || touch_over_other_window) {                        // <-- Checks safe states before starting drag
      return ui::PreferredDragOperation(
          ui::DragDropTypes::DropEffectToDragOperation(DROPEFFECT_NONE));
    }
    desktop_host_->StartTouchDrag(touch_screen_point);                   // <-- Sends mouse left down and mouse move events
  }
  // ...
  ::DoDragDrop(...)                                                      // <-- Starts OS drag. Waits until drag finishes before continuing with funciton.
  // ...
  desktop_host_->FinishTouchDrag(touch_screen_point);                    // <-- Sends mouse left up event (to finish click) after drag completed

```
### `touch_down` bypass

Due to an Aura bug, `is_touch_down()` can persistently return true and bypass the check after a single tap by user. The bypass persists until a full browser restart.

In our PoC, to reach the persistent touch down state, the user only needs to make a single tap. During the tap, the page opens a tab in the same window (and optionally closes the tab) within the `touchstart` event handler. After this, the touch down state is persistently true even after user finishes the tap, and attacks can be launched at any time until browser restart.

See Root Cause Analysis in comment for details, including other (potentially natural) ways to reach persistent touch down state.

### `touch_over_other_window` bypass

This is a generally solid mitigation that mitigates most impacts against bubbles, menus, other browser windows, and non-browser windows. However, a race condition allows menus (e.g. browser menu, context menu) to bypass this check, despite being a different `aura::Window`.

If timed correctly, `touch_over_other_window` will be false when calling `StartDragging()` over a menu that is opening. The menu item will then be clicked as it opens. I am not sure exactly why this occurs, but it's reliable enough for an attacker to use (usually works the first time, but in case of failure we can repeat infinitely with adjusted timing until we succeed). This means top-level menu options (i.e. not nested menu options) can be clicked on using `StartDragging()`.

We can open and click on the browser menu (three dots on top-right of browser window) and context menu (renderer can call [`ShowContextMenu()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=567;drc=f98c3dd3dc0193d10d5cfe549c98e2651244d567) to open it).

### Same `aura::Window` drag/click allowed

As mentioned earlier, an `aura::Window` is conceptually different than what a user typically considers a window. If an interesting target exists within the same `aura::Window`, it can be clicked on because there is no mitigation against this.

We can click on any page contents, bookmarks bar, address bar, docked DevTools, and anything else within same `aura::Window`. We can also drag to bookmarks bar and address bar. We may also be able to drag to other UI elements.

## IMPACTS

After the initial tap to trigger persistent touch down state, all attacks can be performed an infinite amount of times, in any combination, at any time (such as when user is away from computer).

Roughly divided by cause, or prerequsite of extension or chained vuln:

### Impacts when chained with unfixed [issue 443255991](https://issues.chromium.org/issues/443255991)

- **Sandbox escape with MOTW bypass**: We can remove all user interaction requirements for [issue 443255991](https://issues.chromium.org/issues/443255991)'s PoCs. I'll post details and chained PoCs in comments. Current PoC requires an extension.

### Impacts due to same `aura::Window` allowed

- **Create, click JS bookmarks (universal XSS)**: Web pages can create drags with `javascript:` URLs, and the bookmarks bar will create/run bookmarks with `javascript:` URLs (bookmarklets). Therefore, attacker can drag a `javascript:` URL to the bookmarks bar, open a tab to the target website, and then click the attacker-created bookmark in the bookmarks bar. This gives us Universal XSS (UXSS) on any `http(s)://` page and non-component `chrome-extension://` page. WebUI pages and component `chrome-extension://` pages are not allowed to run bookmarklets therefore they are not impacted.
- **Click on other page**: We can open a tab to any web page and click anywhere on it. We can also click on any visible tab content, such as WebUI pages and docked DevTools.
- **Click on side panel**: We can click on any open side panel, such as Bookmarks side panel, GLIC side panel, extension side panels, etc.

### Impacts due to `touch_over_other_window` bypass (menu race condition)

- **Open Downloads page, run/open download (sandbox escape)**: We can click the browser menu button, then click "Downloads" to open the WebUI page. We can then click on downloaded items to run/open them and escape sandbox, bypassing user interaction requirements within browser.
- **Open, click on split tab**: Renderer can call [`ShowContextMenu()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=567;drc=f98c3dd3dc0193d10d5cfe549c98e2651244d567) to open context menu, click on "Open link in Split View", and then click on the other side of the split tab.
- **Open Settings, change most settings**: We can click the browser menu button, then click "Settings" to open the WebUI page. Most settings can be be changed, if they are buttons, toggles, dropdown menus, or otherwise clickable. This includes disabling Safe Browsing, and showing/hiding bookmarks bar (useful for UXSS impact).
- **Open, click on DevTools**: Renderer can call [`ShowContextMenu()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/frame/frame.mojom;l=567;drc=f98c3dd3dc0193d10d5cfe549c98e2651244d567) to open context menu, and then click on "Inspect" to open DevTools.

### Impacts with malicious extension

An extension with no permissions can open any `chrome://` URL that web pages cannot open. We can also enable internal debugging URLs in `chrome://chrome-urls` and open them.

- **Open Extensions page, change extension settings (enable file access, incognito access)**: We can navigate to `chrome://extensions/?id={extId}`, then click on the page to enable file access and incognito access.
- **Open site permissions, allow permissions**: We can navigate to `chrome://settings/content/siteDetails?site={origin}` and click to allow any listed permission, notably: camera, microphone, location, clipboard read, and local network access.
- **Toggle any chrome://flags**: We can navigate to `chrome://flags`, change any flags, and then restart the browser. This could be used to further exploit vulnerabilities in experimental Web/JS/GPU features or relax some security features.
- **Open DevTools for any target**: We can open DevTools for any target through `chrome://inspect`. We can then interact with the DevTools instance if it is docked to the same Aura window. With additional user interaction, there are significant impacts here that I'm still exploring (similar to [issue 402791076](https://issues.chromium.org/issues/402791076): unrestricted CDP access, sandbox escape).

### Prior impacts when chained with fixed [issue 404000989](https://issues.chromium.org/issues/404000989)

Prior to [issue 404000989](https://issues.chromium.org/issues/404000989) being fixed in March 2025, a web page could drag/drop restricted URLs such as `chrome://` or `devtools://` URLs. The standalone vuln required drag and click user interactions to create bookmarks with restricted URLs and then navigate to them. With this drag/click vuln we can do both with one tap (or zero clicks after persistent touch down state). This would allow web pages to launch attacks that currently require extensions.

### Prior impacts when chained with fixed [issue 402791076](https://issues.chromium.org/issues/402791076)

Prior to [issue 402791076](https://issues.chromium.org/issues/402791076) being fixed in March 2025, we could gain XSS on DevTools. The standalone vuln required user clicking on a specific part of a page and then opening DevTools manually, but with this drag/click vuln we can do both with one tap (or zero clicks after persistent touch down state). This would allow further impacts, such as unrestricted CDP access, sandbox escape, and UXSS on any page (including WebUI pages).

## BISECT

Can't do proper bisect with custom build, but the initial fix was introduced in r1371525 (Oct 21, 2024). I started testing in ~r1508700 (August 29th, 2025) where it reproduced, although it likely reproduced since the fix on October 2024.

## PROPOSED FIXES

One or more of these should mitigate most impacts:

- Check position of renderer-provided drag start position in [`StartDragAndDrop()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc;l=68;drc=181e7a80687c55d02e2e74d7d5db3d75ad53c0de) to ensure it is within web page boundaries. Currently, code checks if the cursor position is within the `aura::Window`, which also allows parent `aura::Window`s such as the main browser window. The cursor check should remain for the functional reasons documented in code, but a security check should be added to validate the drag position itself. This does not mitigate all attacks (such as clicking on page context menu or on web page content), but mitigates most impacts.
- Ensure renderer that initiates drag is visible when calling `StartDragging()`. This would prevent attacks on other tabs in the same window.
- Remove `event.HasNativeEvent()` early break in [`EnvInputStateController::UpdateStateForTouchEvent`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/env_input_state_controller.cc;l=53;drc=e4f1aef5f3ec30a28950d766612cc2c04c822c71). After doing some archeology on the `HasNativeEvent()` check, it was [added in January 2013](https://crrev.com/ea7f83787239ae91db4ec297225905b0c8a5a595) as a fix for [an X11 bug](https://crbug.com/169177). The function [`TouchEventIsGeneratedHack()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/events/x/events_x_utils.cc;l=109;drc=ffec0aed60ca494f2a228d0deba095d43ad8748b) is still present and used in X11 code, so it may still be needed to not regress the bug. If it's still needed, we can add the `HasNativeEvent()` check only when using X11 (only Linux?) as a short-term fix. In theory the persistent `is_touch_down()` state may also occur in Linux, but should not have any security impacts there.
- Ensure only one drag is occuring at a time, and/or throttling drag starts. Some of the behaviors currently depend on multiple drags happening simultaneously or in close succession, so restricting active drags and throttling drags may make exploitation more difficult.

Additional mitigation:

- Prevent drag start from prerendered pages. I noticed that when we are in the persistent touch down state, we can initiate drags from a prerendered page. You can test this by triggering persistent touch down state, closing the page, and then typing/pasting the URL into address bar without navigating to the page. This may be useful in some attack scenarios.

## VERSION

Chrome version: Verified with custom build based on `0ecd794f626107687c4844683a828953f49fb2b3` (Sept 11th, 2025)

Operating System: Windows 10

## REPRODUCTION CASE

### Patch to simulate compromised renderer

For all scenarios, apply attached patch and build Chromium.

The patch adds exploit logic to renderer:

1. Adds calls to `StartDragging()` and `ShowContextMenu()` in `third_party/blink/renderer/core/dom/document.cc` for use by the exploit page. (This is loosely based on patch from [issue 370856871](https://issues.chromium.org/issues/370856871).)
2. Bypasses popup blocker in `content/renderer/render_frame_impl.cc` (this is same as [earlier issue's patch](https://issues.chromium.org/issues/370856871#comment17)).
3. Disables multiple context menu check in `third_party/blink/renderer/core/page/context_menu_controller.cc` which helps with context menu attacks.

The patch also adds logging and disables a DCHECK, only for development/debugging purposes:

1. Disables DCHECK in `base/message_loop/message_pump_win.cc` that we hit during PoCs. You can alternatively build with DCHECKs disabled.
2. Adds logging in `content/browser/renderer_host/render_widget_host_view_aura.cc` to show when `Hide()` is called (which would trigger persistent touch down state if tap is in progress).
3. Adds logging in `ui/aura/env.cc` to show `SetTouchDown(bool)` calls.
4. Adds logging in `ui/aura/env_input_state_controller.cc` to show state of touch tracking and processed touch events.
5. Adds logging in `ui/views/widget/desktop_aura/desktop_drag_drop_client_win.cc` to show when operations occur, and if `touch_over_other_window` mitigation is hit.
6. Adds logging in `ui/views/widget/desktop_aura/desktop_window_tree_host_win.cc` to show when mouse events are generated due to touch/drag operations.

### Prerequisites

- A touch-enabled device or another way for OS/Aura to receive touch events (CDP should work).
- Compromised renderer (apply attached patch to simulate).

### Web page scenario: Universal XSS (UXSS)

1. Navigate to <https://alesandroortiz.com/security/chromium/touch-drag-click-cr.html?mode=uxss>
2. Tap anywhere, or do nothing if using autorun.

Observed:

- If bookmarks bar is hidden: Renderer opens Settings page through browser menu, clicks on Appearance, and enables "Show bookmarks bar". Then continues below:
- If bookmarks bar is shown: Renderer opens tab to target website, drags a `javascript:` URL to bookmarks bar to create bookmarklet, then clicks bookmarklet to run the JS payload on target site.

Expected: Renderer cannot click on bookmarks bar. Drag cannot start from background tab. Renderer can still start a `javascript:` URL drag to create a bookmarklet, since this is supported functionality.

### Web page scenario: Click on page

1. Navigate to <https://alesandroortiz.com/security/chromium/touch-drag-click-cr.html?mode=click-page>
2. Tap anywhere, or do nothing if using autorun.

Observed: Renderer opens tab to target website, and performs multiple clicks on target page. In this case, the clicks trigger navigations, but any action triggerable with clicks is possible.

Expected: Renderer cannot click on page on another tab. Drag cannot start from background tab.

### Web page scenario: Open and click on split tab

1. Navigate to <https://alesandroortiz.com/security/chromium/touch-drag-click-cr.html?mode=click-split-tab>
2. Tap anywhere, or do nothing if using autorun.

Observed: Renderer opens split tab to target website by opening and clicking on context menu (this may take several attempts). After opening split tab, renderer performs multiple clicks on the other split tab. In this case, the clicks trigger navigations, but any action triggerable with clicks is possible.

Expected: Renderer cannot click on context menu. Renderer cannot click on the other split tab.

### Web page scenario: Open Settings and disable Safe Browsing

1. Navigate to <https://alesandroortiz.com/security/chromium/touch-drag-click-cr.html?mode=open-settings-disable-safebrowsing>
2. Tap anywhere, or do nothing if using autorun.

Observed: Renderer opens Settings page by clicking on browser menu button, and then clicking "Settings" menu item. Renderer then performs multiple clicks on Settings page to disable Safe Browsing.

Expected: Renderer cannot click on browser menu button nor on browser menu items. Renderer cannot click on page on another tab. Drag cannot start from background tab.

### Web page scenario: pwn all the things! 💥

Runs all web page scenarios. Use autorun for maximum pwnage.

1. Navigate to <https://alesandroortiz.com/security/chromium/touch-drag-click-cr.html?mode=combo&autorun=1>
2. Do nothing. :)

Observed: After one tap, renderer can make multiple `StartDragging()` calls anytime until browser restart. This means attacker can run any scenario with no user interaction.

Expected: After one tap, renderer can only make a single `StartDragging()` call if drag isn't currently occurring. `is_touch_down()` is true only when a physical or otherwise safe touch event is in progress.

## Credit Information

Reporter credit: Alesandro Ortiz <https://AlesandroOrtiz.com>

## Attachments

- [dragclick-patch.diff](attachments/dragclick-patch.diff) (text/x-diff, 16.5 KB)
- [touch-drag-click-cr.html](attachments/touch-drag-click-cr.html) (text/html, 18.0 KB)
- [dragclick-uxss.mp4](attachments/dragclick-uxss.mp4) (video/mp4, 1.7 MB)
- [dragclick-uxss-open-settings-show-bookmarks-bar.mp4](attachments/dragclick-uxss-open-settings-show-bookmarks-bar.mp4) (video/mp4, 659.8 KB)
- [dragclick-pwn-all-the-things.mp4](attachments/dragclick-pwn-all-the-things.mp4) (video/mp4, 4.3 MB)
- [manifest.json](attachments/manifest.json) (application/json, 402 B)
- background.js (text/javascript, 6.3 KB)
- [page.html](attachments/page.html) (text/html, 390 B)
- page.js (text/javascript, 9.2 KB)
- [self-closing.html](attachments/self-closing.html) (text/html, 90 B)
- [self-closing.js](attachments/self-closing.js) (text/javascript, 15 B)
- dragclick-ext-chained-sbx-esc-downloads-api-open.mp4 (video/mp4, 1.6 MB)
- dragclick-ext-chained-sbx-esc-downloads-page-open.mp4 (video/mp4, 2.0 MB)
- [drag_diffs.txt](attachments/drag_diffs.txt) (text/plain, 1.2 KB)
- [mitigations.txt](attachments/mitigations.txt) (text/plain, 20.2 KB)
- [persistent-touch-state.html](attachments/persistent-touch-state.html) (text/html, 620 B)
- [basic-click-demo.html](attachments/basic-click-demo.html) (text/html, 2.0 KB)
- [click-monitor.html](attachments/click-monitor.html) (text/html, 535 B)
- [basic-repro.log](attachments/basic-repro.log) (text/plain, 7.0 KB)
- deleted (application/octet-stream, 0 B)
- [touch_diffs.txt](attachments/touch_diffs.txt) (text/plain, 4.3 KB)
- [dragclick-web-contents-bounds-bypass.mp4](attachments/dragclick-web-contents-bounds-bypass.mp4) (video/mp4, 1.3 MB)

## Timeline

### al...@alesandroortiz.com (2025-09-25)

redacted

### al...@alesandroortiz.com (2025-09-25)

### In case of trouble reproducing

PoCs currently assume UI of default configuration for external unbranded Chromium builds:

- Unbranded build (default)
- Sync disabled in build (default)
- NOT set as default system browser (default)
- Signed in to Google account

You may need to adjust click positions if target is in different position due to browser configuration. PoCs should work with any medium/large/maximized window. Small windows require additional PoC development to handle different layouts.

Timing is fast and optimized for my environment. For better reliability across different environments, slightly more time between attack steps will help. Reliability due to timing should not be an issue for a determined attacker.

---

## Root Cause Analysis

### `touch_down` bypass

Aura tracks the touch state through [`EnvInputStateController::UpdateStateForTouchEvent()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/env_input_state_controller.cc;l=42;drc=181e7a80687c55d02e2e74d7d5db3d75ad53c0de):

```
    case ui::EventType::kTouchPressed:
      touch_ids_down_ |= (1 << event.pointer_details().id);
      env_->SetTouchDown(touch_ids_down_ != 0);
      break;
    // Handle EventType::kTouchCancelled only if it has a native event.
    case ui::EventType::kTouchCancelled:
      if (!event.HasNativeEvent())                    // <-- This is always false for synthesized events
        break;
      [[fallthrough]];
    case ui::EventType::kTouchReleased:
      touch_ids_down_ = (touch_ids_down_ | (1 << event.pointer_details().id)) ^
                        (1 << event.pointer_details().id);
      env_->SetTouchDown(touch_ids_down_ != 0);
      break;

```

When user starts a tap, `kTouchPressed` is emitted and `SetTouchDown(true)` is called. When user finishes the tap, `kTouchReleased` is typically emitted and `SetTouchDown(false)` is called.

However, if the `aura::Window` is hidden during a tap, then a synthesized (non-native) `kTouchCancelled` is emitted. Therefore, the break in the switch statement is hit and both `touch_ids_down_` and `SetTouchDown(false)` are not updated/called. After a user finishes the tap, `kTouchReleased` is never emitted. This means `Env::is_touch_down()` will return true even after the user finished the tap.

This state is persistent or "sticky" because `touch_ids_down_` will always be a positive integer after reaching this state, due to the initial touch ids not being substracted. Therefore, any future touch events will always call `SetTouchDown(true)` even for future `kTouchReleased` events. This state is only reset on full browser restart.

An attacker can easily reach this state by asking the user to start a tap. During the tap, the page opens a tab in the same window (and optionally closes the tab) within the `touchstart` event handler. Opening a new tab hides the previous tab, which creates the synthesized `kTouchCancelled` event through this stack:

- [`WindowEventDispatcher::OnWindowHidden()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window_event_dispatcher.cc;l=399;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18) -> [`WindowEventDispatcher::CleanupGestureState()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window.cc;l=1336;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18) for primary window + [child windows](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window.cc;l=1362;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18)
- -> (for a child window) [`GestureRecognizerImpl::CancelActiveTouches()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/events/gestures/gesture_recognizer_impl.cc;l=259;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18) -> `GestureRecognizerImpl::CancelActiveTouchesImpl()` -> [`WindowEventDispatcher::DispatchSyntheticTouchEvent()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window_event_dispatcher.cc;l=648;drc=48d6f7175422b2c969c14258f9f8d5b196c28d18)

For reference (non-exhaustive), there are other ways of triggering persistent touch down state during a tap, such as crashing the tab's renderer, manually creating a new tab thorugh Ctrl+T, switching tabs using keyboard, or minimizing the window.

Other actions trigger a non-persistent touch down state that may still benefit an attacker, such as dragging regular links to new tab, dragging link to a split pane, or tapping a popup window and closing the popup during the tap. Some of these actions are done naturally by users, so an attacker may not need to prompt the user to perform these actions (which means zero-click attacks are possible in this state).

### al...@alesandroortiz.com (2025-09-25)

That's all for now, folks. I'll add more PoCs in the coming days if they're better than existing PoCs. Let me know if you are interested in any particular impact's PoC that isn't already attached (especially if it would help with VRP reward).

Sorry for another lengthy report. I tried making it short, but it's a lot of impacts and multiple bugs. :)

### wf...@chromium.org (2025-09-25)

Thank you for your report. This is quite a large amount for us to analyze so might take us some time so bear with us.

### wf...@chromium.org (2025-09-25)

Thank you again for your report. This does look like it has similar impact to [issue 370856871](https://issues.chromium.org/issues/370856871) so I'm assigning this provisionally high sev (S1) to match that, although I think the racey nature and additional requirements here MIGHT bump it down to Medium (S2)

### mu...@chromium.org (2025-09-25)

Nice catch! Apparently `RenderFrameHostImpl::StartDragging` was not designed with the consideration for untrusted renderer calls!!

To me the proposed fixes seem necessary even though only #1 could be enough if, additionally, the browser has a way to correlate the `StartDragging` request with the event it has already sent to the renderer.

### ch...@google.com (2025-09-26)

Setting milestone because of s0/s1 severity.

### da...@chromium.org (2025-09-29)

I built with the patch but was unable to reproduce the first case, apparently due to timing issues, per the displayed alert. I'll try playing with the timings.

Another mitigation I think we should do is make the touch drag drop use right mouse down and up events instead of left mouse button down. I've attached a diff that does that. Right button mouse events are somewhat less powerful than left button mouse events, though we still need the other mitigations, especially because context menu items are selectable with the right mouse button.

The renderer has an experiment for html touch drag, which appears to be off by default for Windows. It may be possible to check that experiment in the browser and ignore touch drag api calls if it's not set, as another short term mitigation.

### al...@alesandroortiz.com (2025-09-29)

If you got the "failed to open context menu" alert, try using any scenario that doesn't depend on the context menu. For the UXSS scenario, you can manually enable Bookmarks Bar, reload page, then try again since the rest of the steps are fairly reliable.

The reliability issue is mostly with anything related to context menus, but for PoCs that don't need to open context menu the reliability is fairly solid (at least on my device under different load factors, power settings, etc.)

### al...@alesandroortiz.com (2025-09-29)

Re: right mouse button, I agree it's a good idea but only in addition to other mitigations. Using right mouse button can be a bit more dangerous, since we can open context menu on other surfaces (not just web page) and then select "Paste" to insert text almost anywhere that accepts text, including DevTools. That could be used for unrestricted CDP access and sandbox escape. :)

There would be a lot more impacts if an attacker could automatically paste text into DevTools, other pages, etc. but for reasons I'll investigate later, I was only able to drag text into browser-native surfaces like the address bar and bookmarks bar. Automatically dragging text to other pages or docked DevTools didn't work. With one user click, we *can* drag text into DevTools but it requires user to click once while DevTools is open, so it's not a great attack scenario due unless attack is obscured.

### da...@chromium.org (2025-10-01)

I think part of my issue is that I've been doing this with a debug build, under the debugger, which definitely throws off the timing. The one exploit I have reproduced is the opening of example.com. Can you say how that happens? I have mitigations in place to avoid simultaneous drag drops, and drag drops started outside the web contents area (I think - I saw that check getting hit a few times but haven't seen it in a while). How are you controlling where you drag to, since you can only generate mouse down (and a corresponding mouse move) and mouse up events. I haven't done the hidden renderer check yet; is that involved somehow? I would have thought that getting a mouse down event in the middle of the drag would cancel the drag, but perhaps it's just looking for a mouse up.

### da...@chromium.org (2025-10-01)

I have  several mitigations in place, and running "pwn all the things" doesn't generate any mouse events from drag, but example.com is opened in another tab, so perhaps that's not part of the exploit. I'll attach a diff of what I have so far.

### da...@chromium.org (2025-10-01)

Attached mitigations.txt - it includes all of drag_diffs.txt as well, for simplicity.

Mitigations include:
Ignore touch drags outside of the source 
+    if (!source_window->GetBoundsInScreen().Contains(screen_location)) {
+      LOG(ERROR) << "touch location not in source window";
+      return ui::PreferredDragOperation(
+          ui::DragDropTypes::DropEffectToDragOperation(DROPEFFECT_NONE));
+    }
 
cancel touch even if there isn't a native event (except for Linux)
+#if BUILDFLAG(IS_LINUX)
+      // Handle EventType::kTouchCancelled only if it has a native event.
+      if (!event.HasNativeEvent()) {
         break;
+ #endif // BUILDFLAG(IS_LINUX)
 
don't allow overlapping touch calls
See DesktopDragDropClientWin::touch_drag_drop_in_progress_

Don't let RenderFrameHostImpl start a drag if it's hidden:
+  if (GetVisibilityState() == PageVisibilityState::kHidden) {
+    LOG(ERROR) << "view hidden, not dragging";
+    return;
+  }

Please let me know if I'm missing something, thx!

### al...@alesandroortiz.com (2025-10-04)

Hi, thanks for taking a look! Sorry for delayed response, was busy with Google bugSWAT/Escal8 event. :) Let me know if I missed a question below.

Regarding repro difficulties, what are you seeing in the logs from `EnvInputStateController::UpdateStateForTouchEvent()` and `DesktopDragDropClientWin::StartDragAndDrop()`? It's likely the browser is not entering the persistent touch down state, since that's a core prerequisite for everything else happening. The attack should cause *something* user-visible to happen once you have persistent touch down state even if the attack partially fails, so the fact that nothing appears to happen is indicative of that prerequisite state not being reached.

> The one exploit I have reproduced is the opening of example.com. Can you say how that happens?

This isn't an interesting part of the exploit. There's many well-known ways to bypass the popup blocker from renderer. I mentioned in the report where the bypass is within the compromised renderer: "Bypasses popup blocker in `content/renderer/render_frame_impl.cc`" (the `allow_popup` change). This part will still work even when the main touch/drag vuln is fixed.

> How are you controlling where you drag to, since you can only generate mouse down (and a corresponding mouse move) and mouse up events.

For the basic drag scenarios, the mouse move event is what sets the drag position. The browser does this for us, so there's no special tricks we do.

AFAICT since the OS handles the drag, and assumes that well-behaved applications will only initiate one drag at a time, the OS treats any mouse move as part of the first drag. This is why at least 2 drags in quick succession result in the first drag moving while not being cancelled/finished. (This is applicable to the context menu repro where we can click in two different locations).

I'll get some fresh logs to explain the mouse move, mouse click, and drag finish/cancel behaviors in more detail in a follow-up comment.

> I haven't done the hidden renderer check yet; is that involved somehow?

No, attack works the same regardless of whether compromised renderer is visible or hidden.

> I would have thought that getting a mouse down event in the middle of the drag would cancel the drag, but perhaps it's just looking for a mouse up.

Windows OS will finish or cancel the drag based on the result of [`DragSourceWin::QueryContinueDrag()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/dragdrop/drag_source_win.cc;l=17;drc=6578f830408266d4a69c0c336109efd5782295bc). ~~AFAICT there's some sort of race condition or weird state when attacker initiates two drags in quick succession that causes things to happen in unexpected order, leading to one drag affecting the other drag in a way that benefits the attacker (to perform click which registers as a successful drag finish, which then results in a click on the UI where the cursor is)~~ One click is sufficient, the issue is due to popup opening... see follow-up comment.

Part of it is also due to the popup window that's briefly opened right before each touch sequence, which I think also causes things to occur in unexpected order or helps with timing.

I'll provide more specifics in a follow-up comment.

> Attached mitigations.txt - it includes all of drag\_diffs.txt as well, for simplicity.

I'll do a build in the coming days to verify mitigations, but overall looks good.

To clarify, does `source_window` in `DesktopDragDropClientWin::StartDragAndDrop()` refer to the page contents' `aura::Window`, not the whole browser's `aura::Window`? If it's only page contents, then it's all good. For the CL, adding a comment explaining it refers to page contents would be helpful since it's not intuitive to folks less familiar with Views (like me).

### al...@alesandroortiz.com (2025-10-04)

Here is a basic repro for the persistent touch down state, along with the expected logs.

To repro, tap anywhere on page and then look at logs; it should hit `kTouchCancelled` case which fails to update `is_touch_down` as described in report. You can verify `is_touch_down` is persistently true due to `touch_ids_down_` not being reset properly by tapping again and then looking at logs.

```
(First tap)

[18520:3624:1004/144508.084:ERROR:ui\aura\env_input_state_controller.cc:51] AODEBUG: UpdateStateForTouchEvent, kTouchPressed. new touch_ids_down_: 1, for window: 0x269402380700, has native event? 0
[18520:3624:1004/144508.084:ERROR:ui\aura\env.cc:158] AODEBUG: SetTouchDown, setting is_touch_down to: 1 (was 0)
[18520:3624:1004/144508.101:WARNING:components\input\render_input_router.cc:56] Input request on unbound interface
[18520:3624:1004/144508.120:ERROR:ui\aura\env_input_state_controller.cc:61] AODEBUG: UpdateStateForTouchEvent, kTouchCancelled. for window: 0x269402380700, has native event? 0
[18520:3624:1004/144508.124:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called
[18520:3624:1004/144511.189:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called

(Second tap to show that is_touch_down was already true)

[18520:3624:1004/144520.909:ERROR:ui\aura\env_input_state_controller.cc:51] AODEBUG: UpdateStateForTouchEvent, kTouchPressed. new touch_ids_down_: 3, for window: 0x269402380700, has native event? 0
[18520:3624:1004/144520.909:ERROR:ui\aura\env.cc:158] AODEBUG: SetTouchDown, setting is_touch_down to: 1 (was 1)
[18520:3624:1004/144520.921:WARNING:components\input\render_input_router.cc:56] Input request on unbound interface
[18520:3624:1004/144520.939:ERROR:ui\aura\env_input_state_controller.cc:61] AODEBUG: UpdateStateForTouchEvent, kTouchCancelled. for window: 0x269402380700, has native event? 0
[18520:3624:1004/144520.944:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called
[18520:3624:1004/144524.010:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called

```

### al...@alesandroortiz.com (2025-10-04)

I clarified [#comment15](https://issues.chromium.org/issues/447172715#comment15) a bit (I misremembered some details).

Also, here is basic page click PoC so you can observe more easily through logs.

In this PoC, you can see that opening a popup right before calling `StartDragging()` will result in the drag being finished (successfully) and a click. If you modify the PoC to delay the `openPopup()` call, you will see the drag is not finished automatically (and therefore the click does not occur automatically.)

Logs should look like what I've attached. I've annotated the logs a bit for proper context.

Repro:

1. Host `basic-click-demo.html` and `click-monitor.html` somewhere.
2. Open `basic-click-demo.html` and tap when prompted (this assumes browser is NOT in persistent touch down state; if it's already in that state, the tap is technically not needed even though we still ask for it.)
3. Observe clicks every ~3 seconds on `click-monitor.html` (and in logs).

~~I'll provide additional info in the next day.~~

Click works with a single drag, so these are the actual logs for a single drag that is finished when a popup is opened (the attached log was for two drags, which isn't necessary for basic PoC).

```
[24620:7036:1005/123140.186:WARNING:components\input\render_input_router.cc:56] Input request on unbound interface
[24360:24356:1005/123140.436:ERROR:third_party\blink\renderer\core\dom\document.cc:4900] AODEBUG: StartDragging() called, using default params
[24360:24356:1005/123140.436:ERROR:third_party\blink\renderer\core\dom\document.cc:4909] AODEBUG: Renderer is calling StartDragging with point (224, 224)
[24620:7036:1005/123140.453:ERROR:ui\views\widget\desktop_aura\desktop_drag_drop_client_win.cc:77] AODEBUG: StartDragAndDrop called with source == kTouch
[24620:7036:1005/123140.453:ERROR:ui\views\widget\desktop_aura\desktop_drag_drop_client_win.cc:95] AODEBUG: StartDragAndDrop, calling StartTouchDrag()
[24620:7036:1005/123140.453:ERROR:ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:152] AODEBUG: StartTouchDrag called
[24620:7036:1005/123140.473:ERROR:ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:160] AODEBUG: StartTouchDrag, sent mouse left down + move events
[24620:7036:1005/123140.473:ERROR:ui\views\widget\desktop_aura\desktop_drag_drop_client_win.cc:117] AODEBUG: StartDragAndDrop, calling ::DoDragDrop() momentarily
[24620:7036:1005/123140.503:ERROR:ui\views\widget\desktop_aura\desktop_drag_drop_client_win.cc:123] AODEBUG: StartDragAndDrop, AFTER ::DoDragDrop()
[24620:7036:1005/123140.503:ERROR:ui\views\widget\desktop_aura\desktop_drag_drop_client_win.cc:128] AODEBUG: StartDragAndDrop, calling CleanupGestureState()
[24620:7036:1005/123140.503:ERROR:ui\views\widget\desktop_aura\desktop_drag_drop_client_win.cc:132] AODEBUG: StartDragAndDrop, calling FinishTouchDrag()
[24620:7036:1005/123140.503:ERROR:ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:164] AODEBUG: FinishTouchDrag called (but may not send mouse event)
[24620:7036:1005/123140.503:ERROR:ui\views\widget\desktop_aura\desktop_window_tree_host_win.cc:169] AODEBUG: FinishTouchDrag, sent mouse left up event
[24620:7036:1005/123140.525:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called
[24620:7036:1005/123140.654:INFO:CONSOLE:17] "[object PointerEvent]", source: https://aogarantiza.com/chromium/cr-sbx/click-monitor.html (17)

```

### al...@alesandroortiz.com (2025-10-05)

Looking at some other logging I did a few days ago in [`QueryContinueDrag()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/base/dragdrop/drag_source_win.cc;l=21;drc=6578f830408266d4a69c0c336109efd5782295bc), the drag ends due to mouse event conditional being true, so it returns `DRAGDROP_S_DROP`, ends the drag, and then performs the click (mouse up) per the previous comment's logs.

I'm not sure why opening a popup or otherwise opening another `aura::Window` (like download bubble) will result in the conditional being true, but it works reliably (with the right order of operations, as mentioned in report's patch and PoC comments). For some reason some animations or OS window operations causes things to happen slightly out of order in a way that benefits attacker.

I have a feeling it might be due to the mouse down being processed by OS *after* it enters drag state in `::DoDragDrop()`, which means that from the beginning of the drag the conditional in `QueryContinueDrag()` is true (no mouse button is pressed down yet), which means browser will tell OS to finish the drag successfully.

Then, when we're out of the OS drag, when browser emits the the mouse down and mouse up events, the browser treats that as a proper click.

```
HRESULT DragSourceWin::QueryContinueDrag(BOOL escape_pressed, DWORD key_state) {
  if (cancel_drag_ || escape_pressed)
    return DRAGDROP_S_CANCEL;

  if (!(key_state & MK_LBUTTON) && !(key_state & MK_RBUTTON)) {       <-- This is true when popup is opened for some reason
    OnDragSourceDrop();
    return DRAGDROP_S_DROP;
  }

  return S_OK;
}

```

### da...@chromium.org (2025-10-06)

I've attached a slightly different version of the patch - it moves the event location check to web_contents_view_aura, which makes it clearer that it's the web contents view whose location we are checking. 

Your site seems to be in a bad state at the moment so I can't get the logs you asked for. Tapping just displays some text about back-door...

I did run across the QueryContinueDrag code a few days ago - I can imagine the key state is cleared when another window opens. I'm not sure when the OS calls QueryContinueDrag but I can add some tracing.

Are the logs in #17 with the mitigations applied?

### da...@chromium.org (2025-10-06)

With mitigations applied, log for POC is, when I do a single touch:

[35552:37760:1006/151117.611:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called
[35552:37760:1006/151117.628:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called
[35552:37760:1006/151119.693:ERROR:ui\aura\env_input_state_controller.cc:52] AODEBUG: UpdateStateForTouchEvent, kTouchPressed. new touch_ids_down_: 2, for window: 0x46340aacc500, has native event? 0
[35552:37760:1006/151119.693:ERROR:ui\aura\env.cc:158] AODEBUG: SetTouchDown, setting is_touch_down to: 1 (was 0)
[35552:37760:1006/151119.755:ERROR:ui\aura\env_input_state_controller.cc:75] AODEBUG: UpdateStateForTouchEvent, kTouchReleased. new touch_ids_down_: 0, for window: 0x46340aacc500, has native event? 0
[35552:37760:1006/151119.755:ERROR:ui\aura\env.cc:158] AODEBUG: SetTouchDown, setting is_touch_down to: 0 (was 1)
[35552:38800:1006/151124.427:ERROR:google_apis\gcm\engine\registration_request.cc:292] Registration response error message: DEPRECATED_ENDPOINT
[35552:37760:1006/151145.597:ERROR:content\browser\renderer_host\render_widget_host_view_aura.cc:427] AODEBUG: Hide called

with one click received.


### da...@chromium.org (2025-10-07)

added correct diff

### dx...@google.com (2025-10-09)

Project: chromium/src  

Branch:  main  

Author:  David Bienvenu [davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7017633>

Sanity check event location in StartDragging

---


Expand for full commit details
```
     
    If the event location in WebContentsViewAura::StartDragging is not 
    in the view location, don't start the drag. 
     
    This required making TestRenderWidgetHostView have non-zero bounds. 
     
    Bug: 447172715 
    Change-Id: Ia0ebf8464e411be775a47f96ac497e4c87589a98 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7017633 
    Reviewed-by: Rakina Zata Amni <rakina@chromium.org> 
    Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1527477}

```

---

Files:

- M `content/browser/web_contents/web_contents_view_aura.cc`
- M `content/browser/web_contents/web_contents_view_aura.h`
- M `content/browser/web_contents/web_contents_view_aura_unittest.cc`
- M `content/test/test_render_view_host.cc`

---

Hash: [4bbd4e65443e83dfc919cdd92d8975de15a73966](https://chromiumdash.appspot.com/commit/4bbd4e65443e83dfc919cdd92d8975de15a73966)  

Date: Thu Oct 9 13:39:37 2025


---

### al...@alesandroortiz.com (2025-10-15)

Logs from [#comment17](https://issues.chromium.org/issues/447172715#comment17) are without mitigation. Since I was looking to troubleshoot the repro issues you were having, I was requesting logs without mitigation.

I'll apply mitigations on my build to verify. By EOD tomorrow, will update checkout and try repro without mitigations to see if it still repros in HEAD (without the Oct 9 patch, in case that's the reason you had repro issues).

### al...@alesandroortiz.com (2025-10-15)

I tested the mitigations from [#comment21](https://issues.chromium.org/issues/447172715#comment21):

- Cancel touch on non-ChromeOS builds (<https://crrev.com/c/7032454>): Mitigates all scenarios (since the persistent touch down state is never reached). This by itself is probably the most effective fix.
- Page visibility check: Mitigates most scenarios, except split tab scenario. Combined with the existing checks that prevent cross-window actions, this generally is effective against attacks that require showing another tab in same window.
- Only one simultaneous drag allowed: Does not seem to mitigate any scenario. AFAICT the code runs the drags sequentially, so even if the renderer sends the message simultaneously, they're processed in parallel within browser (2nd drag only starts after 1st drag). Seems okay to abandon this mitigation, or leave it as defense-in-depth for a theoretical attack that actually manages to do two drags at once.
- Web contents bounds check (<https://crrev.com/c/7017633>): Does not seem to mitigate most scenarios. Only mitigates opening browser menu. In the UXSS scenario, the attacker can still drag into the bookmarks bar and click on it. Not sure if `content_native_view` is still including the browser UI or if there is some other issue with this mitigation.

### al...@alesandroortiz.com (2025-10-16)

FYI, I'm still able to repro at commit 44b2e34e898c67b896a61ca1e68e4601eeb02e0a (HEAD from a few hours ago) with original report's simulated compromised renderer patch, so nothing has changed in the past few weeks that would break repro. (Other than the October 9 patch for the browser menu-dependent scenario.)

> Your site seems to be in a bad state at the moment so I can't get the logs you asked for. Tapping just displays some text about back-door...

You must have accidentally run a non-patched renderer, since we use `document.writeln()` to tell renderer to send drag message to browser. In non-patched renderer, it'll write the command to the page instead of sending the message.

### dx...@google.com (2025-10-16)

Project: chromium/src  

Branch:  main  

Author:  David Bienvenu [davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7032454>

Fix handling of touch state in EnvInputStateController

---


Expand for full commit details
```
     
    Change-Id: I7357dff83de347207e6f0016429b3314daf2d5a1 
    Bug: 447172715 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7032454 
    Reviewed-by: Nico Weber <thakis@chromium.org> 
    Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1531080}

```

---

Files:

- M `ui/aura/env_input_state_controller.cc`

---

Hash: [083cac2c44a50242c7ac100f8fed5fc66ead9958](https://chromiumdash.appspot.com/commit/083cac2c44a50242c7ac100f8fed5fc66ead9958)  

Date: Thu Oct 16 21:29:16 2025


---

### da...@chromium.org (2025-10-16)

Thanks, Alesandro. I'll land the page visibility check next. It might take me a little while to come up with a test for that.

Re simultaneous drag, drags are sequential (::DoDragDrop is blocking/synchronous). But there are situations where we get nested event loops during ::DoDragDrop and conceivably we could attempt to start a new drag drop, with the synthesized mouse events, while in ::DoDragDrop. I think ::DoDragDrop handles some but not all messages. I don't think I was able to trigger that with your patch and page, however, so maybe it's not possible. 

The web contents bound check is correct, I believe, from what I could see with my logging. But I'll double check, and attach both a log and a patch with the logging.

### al...@alesandroortiz.com (2025-10-16)

As mentioned in [#comment21](https://issues.chromium.org/issues/447172715#comment21), <https://crrev.com/7032454> should mitigate all scenarios so this can be marked as fixed if you want. The rest of the patches aren't as urgent because they are more defense-in-depth for specific scenarios, and can be tracked in a separate crbug.

> The web contents bound check is correct

Hm, I'll also investigate (either Friday or Monday) since I have a hunch about why the bookmarks UXSS might still work despite this mitigation.

Thanks for all the patches, David!

### al...@alesandroortiz.com (2025-10-17)

I determined the web contents bounds check doesn't work when the drag-initiating web contents is hidden. This is why the UXSS scenario works (attacker page is hidden) but the browser menu attack doesn't work as-is (attacker page is visible). This means that <https://crrev.com/c/7017633> isn't effective without preventing drags from background tabs.

To demonstrate this, in PoC you can update `runOpenSettingsDisableSafeBrowsing()` to include a `window.open('/')` call at the beginning (before the `runAttack()` declaration). Running that scenario will open a new tab to hide the attacker tab, and the existing attack code will now succeed.

Attached video is build that includes <https://crrev.com/c/7017633>, to show bypass.

Logs from test showing `GetBoundsInScreen()` and `event_info.location` values:

- No repro (attacker tab visible)

```
AODEBUG: Renderer is calling StartDragging with point (1784, 208)
AODEBUG: StartDragging, content_native_view->GetBoundsInScreen(): 184,269 1607x840, event_info.location: 1784,208
AODEBUG: StartDragging, OUTSIDE web contents bounds, ending drag

```

- Repro (attacker tab hidden)

```
AODEBUG: Renderer is calling StartDragging with point (1784, 208)
AODEBUG: StartDragging, content_native_view->GetBoundsInScreen(): 184,148 1607x840, event_info.location: 1784,208
AODEBUG: StartDragging, INSIDE web contents bounds, allowing drag

```

Seems like when web contents is hidden, the upper bounds of the web contents is calculated above the actual web contents (`148`, which is above browser UI); when visible it's calculated as expected (`269`, which is below browser UI).

Logs from the beginning of [`GetBoundsInScreen()`](https://source.chromium.org/chromium/chromium/src/+/main:ui/aura/window.cc;l=426;drc=33aa41994c585274ba016ef43a3b8baa3c6334a0), seems like `GetBoundsInRootWindow()` returns different values when tab is visible vs. hidden:

```
Tab visible (mitigation works, attack fails):
[ui\aura\window.cc:428] AODEBUG: GetBoundsInScreen, bounds at beginning (GetBoundsInRootWindow()): 0,121 1611x840

```
```
Tab hidden (mitigation fails, attack succeeds):
[ui\aura\window.cc:428] AODEBUG: GetBoundsInScreen, bounds at beginning (GetBoundsInRootWindow()): 0,0 1611x840

```

### dx...@google.com (2025-10-22)

Project: chromium/src  

Branch:  main  

Author:  David Bienvenu [davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7050902>

sanity check renderer frame visibility in StartDragging

---


Expand for full commit details
```
     
    Change-Id: Icd76538eea2ef5569c30c5077e6a95a83cfdacba 
    Bug: 447172715 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7050902 
    Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Alex Moshchuk <alexmos@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1533589}

```

---

Files:

- M `content/browser/web_contents/web_contents_view_aura.cc`
- M `content/browser/web_contents/web_contents_view_aura.h`
- M `content/browser/web_contents/web_contents_view_aura_unittest.cc`

---

Hash: [c2d88ede477e0e15010fcdc156d32184fb273185](https://chromiumdash.appspot.com/commit/c2d88ede477e0e15010fcdc156d32184fb273185)  

Date: Wed Oct 22 14:18:49 2025


---

### al...@alesandroortiz.com (2025-10-22)

Thanks for the visibility patch, David! I've verified this mitigates the concern from [#comment29](https://issues.chromium.org/issues/447172715#comment29).

Are you okay marking this as fixed, or are there other patches pending? All scenarios should be mitigated with existing patches, particularly <https://crrev.com/c/7032454>.

### da...@chromium.org (2025-10-22)

Thanks for verifying the visibility patch! Yes, I'm OK w/ marking this fixed. I'll hold off on the enforcement of a single drag unless it can be shown to be useful. Thanks for all your help with this!

### ch...@google.com (2025-10-22)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### al...@alesandroortiz.com (2025-10-23)

Thanks for quick work on this, David!

**For VRP Panel**:

If reward would increase by adding a PoC for a particular impact that doesn't currently have a PoC, please let me know and I'll add the PoC. If you also have any questions about prereqs or attack scenarios, let me know.

Compared to issue [issue 370856871](https://issues.chromium.org/issues/370856871), there's some additional prerequisites (one tap anytime during lifetime of browser vs. no interaction; touch screen required). But when chained with [issue 443255991](https://issues.chromium.org/issues/443255991), we can bypass MOTW-triggered checks (such Windows SmartScreen and potentially AV checks) which was cited as mitigating factor in <https://issues.chromium.org/issues/370856871#comment41>. The timing and resolution preconditions can also be optimized away by a determined attacker. The attack can occur at any point after initial tap, so the attack may not be visible to user (attacker can wait for device to be idle if page remains open, even in background tab or a small popup window).

### ch...@google.com (2025-10-24)

Security Merge Request Consideration: Requesting merge to extended stable (M140) because latest trunk commit (1533589) appears to be after extended stable branch point (1496484).
Security Merge Request Consideration: Requesting merge to stable (M141) because latest trunk commit (1533589) appears to be after stable branch point (1509326).
Security Merge Request Consideration: Requesting merge to beta (M142) because latest trunk commit (1533589) appears to be after beta branch point (1522585).
Security Merge Request - Manual Review: Merge review required: M140 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M141 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M142 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141, 142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### da...@chromium.org (2025-10-24)

https://crrev.com/c/7032454 is apparently sufficient to mitigate all known attacks.

 It has been verified on Canary.

I don't think there are any stability risks.

It has the potential to cause compatibility issues, though none have been found so far. Touch handling isn't well tested with automated tests, and touch isn't commonly used. I did manual testing on canary of touch handling and didn't see any issues.

The change is fairly low level,  and affects whenever touches are cancelled with synthetic events, i.e., events that Chrome itself generates when certain things happen, like a tab being closed, or dragged between windows. Manual testing would involve testing touch handling, especially drag drop, on Windows and ChromeOS devices.

To avoid the risk of backporting CL's that might cause regressions, it's probably not worth backporting the other fixes.  https://chromium-review.googlesource.com/7017633 has apparently caused a web ui tab strip drag regression when used with split tab.

Note that the security exploit is Windows-specific, but the fixes affect Linux, Windows, and ChromeOS (though the one we're proposing backporting does not affect ChromeOS).



### ya...@chromium.org (2025-10-27)

Thanks, please go ahead and merge to all branches.

### dx...@google.com (2025-10-28)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  David Bienvenu [davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7087511>

M142 Fix handling of touch state in EnvInputStateController

---


Expand for full commit details
```
     
    (cherry picked from commit 083cac2c44a50242c7ac100f8fed5fc66ead9958) 
     
    Change-Id: I7357dff83de347207e6f0016429b3314daf2d5a1 
    Bug: 447172715 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7032454 
    Reviewed-by: Nico Weber <thakis@chromium.org> 
    Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1531080} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7087511 
    Reviewed-by: Mitsuru Oshima <oshima@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7444@{#2179} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `ui/aura/env_input_state_controller.cc`

---

Hash: [ab19bea9cb6ea292f2bfdcee27c18f7d919568da](https://chromiumdash.appspot.com/commit/ab19bea9cb6ea292f2bfdcee27c18f7d919568da)  

Date: Tue Oct 28 00:27:08 2025


---

### dx...@google.com (2025-10-28)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  David Bienvenu [davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7087573>

M140 Fix handling of touch state in EnvInputStateController

---


Expand for full commit details
```
     
    (cherry picked from commit 083cac2c44a50242c7ac100f8fed5fc66ead9958) 
     
    Change-Id: I7357dff83de347207e6f0016429b3314daf2d5a1 
    Bug: 447172715 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7032454 
    Reviewed-by: Nico Weber <thakis@chromium.org> 
    Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1531080} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7087573 
    Reviewed-by: Mitsuru Oshima <oshima@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7339@{#3803} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `ui/aura/env_input_state_controller.cc`

---

Hash: [56ca847e9ea70a5c56fa3d634361da1002fb284b](https://chromiumdash.appspot.com/commit/56ca847e9ea70a5c56fa3d634361da1002fb284b)  

Date: Tue Oct 28 00:43:50 2025


---

### dx...@google.com (2025-10-28)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  David Bienvenu [davidbienvenu@chromium.org](mailto:davidbienvenu@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7088068>

M141 Fix handling of touch state in EnvInputStateController

---


Expand for full commit details
```
     
    (cherry picked from commit 083cac2c44a50242c7ac100f8fed5fc66ead9958) 
     
    Change-Id: I7357dff83de347207e6f0016429b3314daf2d5a1 
    Bug: 447172715 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7032454 
    Reviewed-by: Nico Weber <thakis@chromium.org> 
    Commit-Queue: David Bienvenu <davidbienvenu@chromium.org> 
    Reviewed-by: Mustaq Ahmed <mustaq@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1531080} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7088068 
    Reviewed-by: Eliot Courtney <edcourtney@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7390@{#3098} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `ui/aura/env_input_state_controller.cc`

---

Hash: [bb72c6cb6bcdd69e2de17fd1c09047b72bb783a5](https://chromiumdash.appspot.com/commit/bb72c6cb6bcdd69e2de17fd1c09047b72bb783a5)  

Date: Tue Oct 28 03:46:11 2025


---

### sp...@google.com (2025-11-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $30000.00 for this report.

Rationale for this decision:
sandbox escape // UXSS mitigated by needing a colluding extension


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### al...@alesandroortiz.com (2025-11-12)

Thanks for the reward!

To clarify, the UXSS and the sandbox escape impacts do *not* require an extension. I'm referring to these impacts from the original report:

> - Create, click JS bookmarks (universal XSS): Web pages can create drags with javascript: URLs, and the bookmarks bar will create/run bookmarks with javascript: URLs (bookmarklets). Therefore, attacker can drag a javascript: URL to the bookmarks bar, open a tab to the target website, and then click the attacker-created bookmark in the bookmarks bar. This gives us Universal XSS (UXSS) on any http(s):// page and non-component chrome-extension:// page. WebUI pages and component chrome-extension:// pages are not allowed to run bookmarklets therefore they are not impacted.

> - Open Downloads page, run/open download (sandbox escape): We can click the browser menu button, then click "Downloads" to open the WebUI page. We can then click on downloaded items to run/open them and escape sandbox, bypassing user interaction requirements within browser.

The scenario that does require extension is the sandbox escape with MOTW bypass, because the chained MOTW bypass requires an extension. Quoting from original report:

> - Sandbox escape with MOTW bypass: We can remove all user interaction requirements for [issue 443255991](https://issues.chromium.org/issues/443255991)'s PoCs. I'll post details and chained PoCs in comments. Current PoC requires an extension.

If the non-extension sandbox escape might be rewarded higher, can I request a review by the VRP Panel?

### ch...@google.com (2026-01-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/447172715)*
