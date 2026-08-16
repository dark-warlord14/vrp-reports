# Use-after-free in DevToolsRendererChannel::ForceDetachWorkerSessions via duplicate ChildTargetCreated for dedicated workers

| Field | Value |
|-------|-------|
| **Issue ID** | [507332299](https://issues.chromium.org/issues/507332299) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2026-6919 |
| **Reporter** | je...@gmail.com |
| **Assignee** | yy...@chromium.org |
| **Created** | 2026-04-28 |
| **Bounty** | $26,000.00 |

## Description

**Summary:** Use-After-Free in DevTools EmulationHandler - dangling Unretained ScreenOrientationProvider callback

**Program:** Google VRP

**Vulnerability type:** Memory Corruption (in a non-sandboxed process)

### Details

## Vulnerability Description

`EmulationHandler::UpdateScreenOrientationEmulation(true)` registers a repeating callback with `base::Unretained(this)` on the `ScreenOrientationProvider` owned by the `WebContents`:

```
// content/browser/devtools/protocol/emulation_handler.cc:1298-1299
provider->SetOrientationLockChangedCallback(base::BindRepeating(
    &EmulationHandler::OnOrientationLockChanged, base::Unretained(this)));

```

When `SetRenderer(nullptr)` is called on the handler (e.g., during `DisconnectWebContents` triggered by prerender activation), `host_` becomes null. When the DevTools session subsequently closes, `Dispose()` calls `Disable()`, which attempts to clear the callback but fails:

```
// emulation_handler.cc:172-177
Response EmulationHandler::Disable() {
  if (device_emulation_enabled_) {
    if (screen_orientation_lock_emulation_enabled_) {
      UpdateScreenOrientationEmulation(false);  // tries to clear callback
    }
  }
}

// emulation_handler.cc:1287-1289
void EmulationHandler::UpdateScreenOrientationEmulation(bool enabled) {
  WebContentsImpl* web_contents = GetWebContents();
  if (!web_contents) {
    return;  // ← EARLY RETURN! Callback NOT cleared!
  }
}

```

`GetWebContents()` returns nullptr because `host_` is null after `SetRenderer(nullptr)`.

The destructor performs no cleanup:

```
// emulation_handler.cc:134
EmulationHandler::~EmulationHandler() = default;  // NO cleanup!

```

The handler is then destroyed via `DevToolsSession::Dispose()` (`devtools_session.cc:164-165`): `pair.second->Disable()` followed by `handlers_.clear()`.

The `ScreenOrientationProvider` (owned by the surviving `WebContents`) retains the dangling `Unretained` callback. When any subsequent orientation lock event fires, the provider invokes the callback on freed memory:

```
// screen_orientation_provider.cc:71
if (lock_changed_callback_) {
  lock_changed_callback_.Run(true, orientation);  // calls freed handler → UAF
}

```

Additionally, `EmulationHandler::SetRenderer()` does NOT clear the orientation callback when transitioning to a new frame:

```
// emulation_handler.cc:143-155
void EmulationHandler::SetRenderer(int process_host_id,
                                   RenderFrameHostImpl* frame_host) {
  host_ = frame_host;
  if (touch_emulation_enabled_)
    UpdateTouchEventEmulationState();
  if (device_emulation_enabled_)
    UpdateDeviceEmulationState(...);
  // NO UpdateScreenOrientationEmulation — callback not cleared!
}

```

**The incomplete cleanup pattern:**

The cleanup logic incorrectly depends on `GetWebContents()` returning non-null, even though the callback is stored on a `WebContents`-owned object. This mismatch causes callback deregistration to silently fail during normal teardown sequences.

```
SetRenderer(nullptr)         → host_ = null, callback NOT cleared
Disable()                    → GetWebContents() returns nullptr → early return
~EmulationHandler() = default → NO cleanup
Provider retains callback    → next orientation event → UAF

```

**Production code path to `SetRenderer(nullptr)`:**

`WillSwapFrameTreeNode` (`render_frame_host_impl.cc:19512`) → `DisconnectWebContents()` (`render_frame_devtools_agent_host.cc:757`) → `UpdateFrameHost(nullptr)` → `SetRendererInternal()` (`devtools_renderer_channel.cc:50`) → `pair.second->SetRenderer(_, nullptr)` (line 98)

This follows the same lifetime mismanagement pattern as CVE-2026-6919 (dangling DevTools callback, [bug 493652473](https://issues.chromium.org/issues/493652473)), suggesting incomplete mitigation of this vulnerability class.

## Attack Preconditions

This issue is reachable in environments where DevTools protocol access is available, including:

- Chrome extensions with the `debugger` permission (`chrome.debugger`)
- Remote debugging (`--remote-debugging-port`)
- Automation frameworks (e.g., Puppeteer, Selenium)

These contexts are explicitly considered part of Chromium's attack surface, as DevTools handlers execute in the browser process and operate on live `WebContents`.

A malicious extension with `debugger` permission can:

1. Attach to a tab and call `Emulation.setDeviceMetricsOverride` with `screenOrientationLockEmulation: true`
2. Trigger a frame lifecycle transition (e.g., navigation, prerender activation, or renderer termination), causing `SetRenderer(nullptr)`
3. Detach the debugger (frees the handler while the callback persists on the provider)
4. The dangling callback is subsequently triggered through orientation state transitions

## Security Model Alignment

This issue is reachable under Chromium's security model where DevTools protocol handlers are trusted browser-process code operating on live `WebContents`.

The `ScreenOrientationProvider::LockOrientation` path at `screen_orientation_provider.cc:71` fires the callback synchronously — no timing or race condition required.

The dangling callback persists after DevTools detachment and is invoked independently of DevTools, meaning the lifetime violation crosses component boundaries. The `ScreenOrientationProvider` is owned by `WebContents` and outlives the DevTools session, meaning the dangling callback persists beyond the lifetime of the `EmulationHandler`. The callback is invoked by `ScreenOrientationProvider` during orientation state transitions (e.g., via `LockOrientation`). The callback is invoked synchronously within `ScreenOrientationProvider::LockOrientation`, making the use-after-free deterministic and not dependent on timing or race conditions. The attacker does not need ongoing DevTools access after the initial setup.

## Reproduction Steps / PoC

**Target:** Chromium latest main (commit 844eb6dff4, April 28 2026)
**OS:** macOS 15, Apple M2
**Build:** `is_asan=true is_debug=false symbol_level=0 is_component_build=false dcheck_always_on=false`

**Step 1:** Add the attached `test_emulation_orientation_uaf.cc` to `content/browser/devtools/protocol/` and add to `content/test/BUILD.gn` after the `screen_orientation_provider_unittest.cc` entry:

```
"../browser/devtools/protocol/emulation_handler_orientation_unittest.cc",

```

**Step 2:** Build and run:

```
autoninja -C out/asan content_unittests
out/asan/content_unittests --gtest_filter="*OrientationCallback*"

```

The test uses the **real `EmulationHandler`** class — no simulation. It:

1. Creates a real `EmulationHandler`
2. Calls real `SetRenderer()` with a test RenderFrameHost
3. Calls real `SetDeviceMetricsOverride()` with `screenOrientationLockEmulation: true` — this registers the `Unretained(this)` callback on the provider via production code path at `emulation_handler.cc:1299`
4. Calls real `SetRenderer(nullptr)` — simulates `DisconnectWebContents`
5. Calls real `Disable()` — simulates session teardown; callback NOT cleared because `GetWebContents()` returns nullptr
6. Destroys the real handler — `~EmulationHandler() = default`
7. Calls `ScreenOrientationProvider::LockOrientation()` — provider fires the dangling callback → UAF

**ASAN output:**

```
==14547==ERROR: AddressSanitizer: heap-use-after-free on address 0x6160000818e0
READ of size 8 at 0x6160000818e0 thread T0
    #0 content::protocol::EmulationHandler::OnOrientationLockChanged(...)
        emulation_handler.cc
    #1 base::RepeatingCallback<...>::Run(...)
        callback.h
    #2 content::ScreenOrientationProvider::LockOrientation(...)
        screen_orientation_provider.cc

0x6160000818e0 is located 608 bytes inside of 624-byte region
freed by thread T0 here:
    #0 __asan_memmove
    #1 EmulationHandlerOrientationCallbackTest_RealHandlerDanglingCallbackCrash_Test::TestBody()
        emulation_handler_orientation_unittest.cc

```

The crash confirms:

- The **real production `EmulationHandler::OnOrientationLockChanged`** is called after the handler is freed
- `ScreenOrientationProvider::LockOrientation` at `screen_orientation_provider.cc` fires the dangling callback
- The freed 624-byte `EmulationHandler` is accessed — heap-use-after-free

The crash is deterministic and does not rely on timing or race conditions.

The full ASAN log is attached.

### Attack scenario

This is a use-after-free in the browser process (unsandboxed), reachable via DevTools protocol interactions.

This is a browser-process heap-use-after-free caused by an unsafe `base::Unretained(this)` callback pattern in production DevTools code. The callback is registered on a `ScreenOrientationProvider` that outlives the `EmulationHandler`, and the cleanup path fails silently when `host_` is null.

The freed `EmulationHandler` (624 bytes) is accessed when the provider fires the dangling callback. The callback invocation results in a method call (`EmulationHandler::OnOrientationLockChanged`) on a freed object. If the freed memory is reused with attacker-influenced data, this may result in type confusion or control-flow hijacking within the browser process.

Critically, the trigger (orientation state transitions via `ScreenOrientationProvider`) operates independently of DevTools after the initial setup. This creates a cross-component lifetime violation where a DevTools-owned object (`EmulationHandler`) is referenced by a `WebContents`-owned subsystem (`ScreenOrientationProvider`) with a longer lifetime. The lifetime violation crosses component boundaries — the bug is set up through DevTools (`Blink>DevTools`) but triggered through the screen orientation subsystem (`content/browser/screen_orientation`), meaning the dangling callback persists and can fire long after the DevTools session is gone.

**Suggested fix:**

1. Replace `base::Unretained(this)` with `WeakPtr`:

```
// In emulation_handler.h — add:
base::WeakPtrFactory<EmulationHandler> weak_factory_{this};

// In emulation_handler.cc:1298 — change to:
provider->SetOrientationLockChangedCallback(base::BindRepeating(
    &EmulationHandler::OnOrientationLockChanged,
    weak_factory_.GetWeakPtr()));

```

2. Add explicit destructor cleanup (defense-in-depth):

```
EmulationHandler::~EmulationHandler() {
  if (host_) {
    if (auto* wc = WebContents::FromRenderFrameHost(host_)) {
      auto* provider = static_cast<WebContentsImpl*>(wc)
          ->GetScreenOrientationProvider();
      if (provider) {
        provider->SetOrientationLockChangedCallback({});
      }
    }
  }
}

```

3. `SetRenderer()` should clear the orientation callback on the old WebContents before updating `host_`.
4. Additionally, clearing the callback unconditionally during teardown (independent of `GetWebContents()` returning non-null) would prevent silent failure of cleanup.

**Related bugs:** [Bug 493652473](https://issues.chromium.org/issues/493652473) (CVE-2026-6919)
**Component:** Blink>DevTools

## Attachments

- [real_handler_uaf.log](attachments/real_handler_uaf.log) (application/octet-stream, 12.8 KB)
- [test_emulation_orientation_uaf.cc](attachments/test_emulation_orientation_uaf.cc) (application/octet-stream, 4.5 KB)

## Timeline

### sp...@google.com (2026-04-28)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### ye...@google.com (2026-04-29)

This report does not provide enough information for us to quickly understand and
reproduce a problem. It will be closed as Won't Fix. Once you have gathered the
required information please open a new issue with a brief description that
attaches all necessary pocs, traces and patches as individual files.

In particular:

- attach a minimized reproduction case as `poc.html` or `poc.js`

For more information see: <https://chromium.googlesource.com/chromium/src/+/master/docs/security/vrp-faq.md#best-practices-for-security-bug-reporting>

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507332299)*
