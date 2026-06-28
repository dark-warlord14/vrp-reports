# SubAppsServiceImpl::Remove() use-after-free: ReportBadMessageAndDeleteThis() mid-loop deletes `this`, next iteration accesses freed memory

| Field | Value |
|-------|-------|
| **Issue ID** | [492465356](https://issues.chromium.org/issues/492465356) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>WebAppInstalls>Isolated |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | os...@gmail.com |
| **Assignee** | by...@google.com |
| **Created** | 2026-03-13 |
| **Bounty** | $36,000.00 |

## Description

---

### Report description

SubAppsServiceImpl::Remove() use-after-free: ReportBadMessageAndDeleteThis() mid-loop deletes `this`, next iteration accesses freed memory

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/sub_apps_service_impl.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

`SubAppsServiceImpl::Remove()` iterates over `manifest_id_paths` calling `RemoveSubApp()` for each. `RemoveSubApp()` calls `ReportBadMessageAndDeleteThis()` when a cross-origin path is detected (via `ASSIGN_OR_RETURN` + `ConvertPathToUrl()`). This synchronously calls `delete this`, but the loop continues — the next iteration calls `render_frame_host()` on the deleted `SubAppsServiceImpl`, causing a heap-use-after-free in the browser process.

**Vulnerable file:** [sub\_apps\_service\_impl.cc](https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/web_applications/sub_apps_service_impl.cc) — `Remove()` loop at L535-538, `RemoveSubApp()` RBM at L554

The developer was partially aware — comment at L532 says "Take weak pointer early as this may get deleted by RemoveSubApp()" — but only guarded the `.Done()` callback, not the loop body.

**Steps to reproduce:**

1. Check out stable tag: `git checkout 146.0.7680.32`
2. `git apply poc_patch.diff`
3. Build with ASAN:
   ```
   gn gen out/ASAN --args='is_asan=true is_debug=false is_component_build=false symbol_level=1 use_remoteexec=false dcheck_always_on=true enable_nacl=false'
   autoninja -C out/ASAN chrome
   
   ```
4. Place `serve.py`, `index.html`, and `poc.js` in a directory and start the server:
   ```
   python3 serve.py
   
   ```
5. Launch Chrome (the IWA dev proxy installs and opens the app automatically):
   ```
   ASAN_OPTIONS="detect_leaks=0:symbolize=1:halt_on_error=1:print_scariness=1" \
     out/ASAN/Chromium.app/Contents/MacOS/Chromium \
     --enable-features=IsolatedWebApps,IsolatedWebAppDevMode,SubApps \
     --install-isolated-web-app-from-url=http://localhost:8080/ \
     --no-first-run --disable-default-apps \
     --user-data-dir=/tmp/subapps1-poc
   
   ```
6. On macOS, a Chromium Apps folder opens. Open the installed IWA app. macOS Gatekeeper may block it — go to System Settings → Privacy & Security, scroll down, and click "Open Anyway".
7. The PoC page loads inside the IWA and calls `navigator.subApps.remove()`. ASAN reports heap-use-after-free in the browser process (see `asan.txt`).

The renderer patch (`poc_patch.diff`) modifies only `sub_apps.cc` — it bypasses the renderer-side path validation so `remove()` sends a full cross-origin URL (`https://evil.com/...`) instead of a root-relative path. The browser-side code is unmodified. The IWA runs via dev mode proxy with proper isolation (COOP/COEP/IsolatedContext), and the SubApps Mojo service binds naturally through `CreateIfAllowed()`.

**Bisect:**

- Introducing commit: `919adcfad6f29` — Sam Thiesen, 2023-04-12, M114. Changed Remove() from single-app to list-based, introducing the loop over `manifest_id_paths` that calls `RemoveSubApp()` per path.
- Affected: M114 through M146 (current stable).

**Fix:** Check the existing `weak_ptr` after each `RemoveSubApp()` call; return early if `this` was deleted. Attached as `fix.diff`.

#### Impact analysis

A compromised IWA renderer can trigger a heap-use-after-free in the browser process by sending a `Remove()` IPC with a cross-origin first path and any second path. The UAF reads 8 bytes from freed heap (SCARINESS: 51), accessing `SubAppsServiceImpl` member data via `render_frame_host()`. MiraclePtr does NOT protect this access. The SubApps API requires IWAs, which are behind the `kIsolatedWebApps` flag on non-ChromeOS (enabled by default on ChromeOS) and the `kSubApps` flag (`Security_Impact-None`).

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.32 (Stable)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a non-sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Tianyi Hu

## Attachments

- [fix.diff](attachments/fix.diff) (application/octet-stream, 1.2 KB)
- [index.html](attachments/index.html) (text/html, 773 B)
- [poc.js](attachments/poc.js) (text/javascript, 2.2 KB)
- [poc_patch.diff](attachments/poc_patch.diff) (application/octet-stream, 1.0 KB)
- [serve.py](attachments/serve.py) (text/x-python-script, 2.7 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 41.4 KB)

## Timeline

### os...@gmail.com (2026-03-13)

CL with fix + browser test:

<https://chromium-review.googlesource.com/c/chromium/src/+/7666579>

### dc...@chromium.org (2026-03-13)

I think this requires a compromised renderer, so I'm marking this as high instead of critical.

### gr...@google.com (2026-03-13)

We haven't launched this API yet, so it's not really critical just yet. Nice catch anyway!

### dc...@chromium.org (2026-03-13)

Marking this as no security impact since this is not yet launched (if there's a launch bug might be good to mark it as blocked on this though)

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Tianyi Hu [oscarhuthu@gmail.com](mailto:oscarhuthu@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7666579>

Check weak\_ptr after each RemoveSubApp() in Remove() loop

---


Expand for full commit details
```
     
    SubAppsServiceImpl::Remove() iterates over manifest_id_paths 
    calling RemoveSubApp() for each entry. RemoveSubApp() may call 
    ReportBadMessageAndDeleteThis() when a cross-origin path is 
    detected, which synchronously deletes `this`. The loop then 
    continues and accesses the freed SubAppsServiceImpl on the 
    next iteration via render_frame_host(). 
     
    Add a weak_ptr check after each RemoveSubApp() call and return 
    early if `this` has been deleted. The existing weak_ptr was 
    already taken but only guarded the .Done() callback, not the 
    loop body. 
     
    Bug: 492465356 
    Change-Id: I4a828d077df66731dd9a373a12ca63a66e8dda54 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7666579 
    Commit-Queue: Dominik Bylica <bylica@google.com> 
    Reviewed-by: Dominik Bylica <bylica@google.com> 
    Reviewed-by: Marijn Kruisselbrink <mek@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600670}

```

---

Files:

- M `chrome/browser/web_applications/sub_apps_service_impl.cc`
- M `chrome/browser/web_applications/sub_apps_service_impl_browsertest.cc`

---

Hash: [2adbbf0c1a523cdf9398f88bea6fec1d4f0b67db](https://chromiumdash.appspot.com/commit/2adbbf0c1a523cdf9398f88bea6fec1d4f0b67db)  

Date: Tue Mar 17 18:00:58 2026


---

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $36000.00 for this report.

Rationale for this decision:
High quality with bisect. Sandbox escape / Memory corruption / RCE in a non-sandboxed process


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492465356)*
