# `WindowOpenDisposition` should use mojo enum

| Field | Value |
|-------|-------|
| **Issue ID** | [486761170](https://issues.chromium.org/issues/486761170) |
| **Status** | Accepted |
| **Severity** | S0-Critical |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ha...@gmail.com |
| **Created** | 2026-02-23 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

A compromised renderer can detect whether specific URLs are open in any browser window by sending FrameHost::OpenURL with disposition=SWITCH_TO_TAB. The browser's behavior differs observably depending on whether a matching tab exists, creating a reliable side channel that leaks the user's browsing state across all windows of the same profile.

The renderer-supplied `disposition` field in FrameHost::OpenURL passes through the browser without validation. `VerifyOpenURLParams()` (content/browser/renderer_host/ipc_utils.cc:199-269) validates URL, origin, blob_url_token, and post_body — but never checks `disposition`. This allows a compromised renderer to inject `SWITCH_TO_TAB` (value 10), a disposition intended exclusively for browser-initiated navigations (omnibox, bookmarks) that is never produced by the renderer's `NavigationPolicyToDisposition()` (content/renderer/render_frame_impl.cc:1200-1219).

When the browser processes SWITCH_TO_TAB, it calls `GetIndexAndBrowserOfExistingTab()` (chrome/browser/ui/singleton_tabs.cc:169) which searches ALL windows of the same profile via `ForEachCurrentBrowserWindowInterfaceOrderedByActivation()`. The result produces two observably different behaviors:

- Tab FOUND: Browser activates the matched tab. Source tab is NOT navigated. No new tab created.
- Tab NOT FOUND: Falls through to SINGLETON_TAB (browser_navigator.cc:689-697), calls ShowSingletonTabOverwritingNTP(), creates a new tab.

The renderer can distinguish these cases by observing tab count changes, focus state (document.hasFocus), or visibility state (document.visibilityState), enabling reliable cross-origin tab enumeration.

Additionally, `WindowOpenDisposition::UNKNOWN` (value 0) reaches `GetBrowserAndTabForDisposition()` default case (browser_navigator.cc:339), hitting `NOTREACHED()` → `ImmediateCrash()`, crashing the browser process. Note: commit 4d0b870eebf23 fixed this same class of bug in CreateNewWindow but did not patch OpenURL.

VERSION
Chrome Version: 147.0.7682.0 (dev/trunk)
Operating System: macOS 26.2 (arm64)

The vulnerability exists in the current main branch and likely affects all current stable/beta/dev releases, as the disposition validation gap has been present since the SWITCH_TO_TAB disposition was introduced.

REPRODUCTION CASE

Browser tests are attached that demonstrate the vulnerability. To build and run:

1. Copy test files to the source tree:
   cp switch_to_tab_info_leak_browsertest.cc chromium/src/chrome/browser/ui/
   cp poc_death_test.cc chromium/src/chrome/browser/ui/

2. Add to chrome/test/BUILD.gn (in the browser_tests sources list):
   "../browser/ui/switch_to_tab_info_leak_browsertest.cc",
   "../browser/ui/poc_death_test.cc",

3. Build and run:
   autoninja -C out/Default browser_tests
   out/Default/browser_tests --gtest_filter="SwitchToTabInfoLeakTest.*:OpenURLDispositionDeathTest.*"

Test output (6/6 PASSED):

```
[1/6] SwitchToTabInfoLeakTest.CanDetectOpenTabsByURL (3432 ms)
[2/6] SwitchToTabInfoLeakTest.CrossWindowDetection (4319 ms)
[3/6] SwitchToTabInfoLeakTest.RapidURLEnumeration (5115 ms)
[4/6] OpenURLDispositionDeathTest.NavigateCrashesOnUnknownDisposition (5654 ms)
[5/6] OpenURLDispositionDeathTest.OpenURLCrashesOnUnknownDisposition (5911 ms)
[6/6] OpenURLDispositionDeathTest.ValidDispositionDoesNotCrash (3248 ms)
SUCCESS: all tests passed.
```

SWITCH_TO_TAB Information Leak (3/3 PASSED):
- CanDetectOpenTabsByURL: Probes a URL that IS open → tab switches, attacker tab unchanged. Probes a URL that is NOT open → new tab created. Observable difference confirms the side channel.
- CrossWindowDetection: Renderer in Window 2 detects a URL open in Window 1. Proves cross-window tab enumeration.
- RapidURLEnumeration: Probes 6 URLs (3 open, 3 not open). Achieves 100% detection accuracy with no rate limiting.

UNKNOWN Disposition Crash (3/3 PASSED):
- NavigateCrashesOnUnknownDisposition: Navigate(UNKNOWN) hits NOTREACHED() crash.
- OpenURLCrashesOnUnknownDisposition: Full WebContents::OpenURL chain with UNKNOWN crashes browser.
- ValidDispositionDoesNotCrash: CURRENT_TAB works normally (control test).

ATTACHED FILES
- switch_to_tab_info_leak_browsertest.cc: Browser test demonstrating the SWITCH_TO_TAB information leak side channel. Three tests verify same-window detection, cross-window detection, and rapid URL enumeration with 100% accuracy.
- poc_death_test.cc: Browser test demonstrating the UNKNOWN disposition browser process crash. Verifies the NOTREACHED() crash via both Navigate() and WebContents::OpenURL() code paths, plus a control test confirming valid dispositions work normally.
- renderer_trigger.patch: Patch for content/renderer/render_frame_impl.cc that overrides the disposition field to SWITCH_TO_TAB in RenderFrameImpl::OpenURL(), demonstrating that a compromised renderer can exploit this from the renderer process side.
- SETUP.txt: Step-by-step build and run instructions including BUILD.gn modification.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: browser process crash
Crash State:
```
[FATAL:chrome/browser/ui/browser_navigator.cc:339] NOTREACHED hit.
  GetBrowserAndTabForDisposition()  browser_navigator.cc:339
  Navigate()                        browser_navigator.cc
  Browser::OpenURLFromTab()         browser.cc
  WebContentsImpl::OpenURL()        web_contents_impl.cc
  RenderFrameHostImpl::OpenURL()    render_frame_host_impl.cc:9701
```

Death test output confirming the crash:
```
[  DEATH   ] [FATAL:chrome/browser/ui/browser_navigator.cc:339] NOTREACHED hit.
```

This crash is triggered by UNKNOWN disposition. The SWITCH_TO_TAB information leak does not crash but leaks browsing state.

SUGGESTED FIX

Add a disposition whitelist to VerifyOpenURLParams() in content/browser/renderer_host/ipc_utils.cc:

```cpp
static bool IsValidRendererDisposition(WindowOpenDisposition d) {
  switch (d) {
    case WindowOpenDisposition::CURRENT_TAB:
    case WindowOpenDisposition::NEW_FOREGROUND_TAB:
    case WindowOpenDisposition::NEW_BACKGROUND_TAB:
    case WindowOpenDisposition::NEW_POPUP:
    case WindowOpenDisposition::NEW_WINDOW:
    case WindowOpenDisposition::SAVE_TO_DISK:
    case WindowOpenDisposition::NEW_PICTURE_IN_PICTURE:
      return true;
    default:
      return false;
  }
}

if (!IsValidRendererDisposition(params->disposition)) {
  mojo::ReportBadMessage("Invalid disposition from renderer");
  return false;
}
```

This whitelist matches exactly the dispositions that NavigationPolicyToDisposition() can produce. It blocks UNKNOWN (crash), SWITCH_TO_TAB (info leak), SINGLETON_TAB, OFF_THE_RECORD, and IGNORE_ACTION in a single fix.

CREDIT INFORMATION
Reporter credit: heesun

## Attachments

- [switch_to_tab_info_leak_browsertest.cc](attachments/switch_to_tab_info_leak_browsertest.cc) (text/x-c++src, 10.7 KB)
- [poc_death_test.cc](attachments/poc_death_test.cc) (text/x-c++src, 4.2 KB)
- [renderer_trigger.patch](attachments/renderer_trigger.patch) (text/x-diff, 2.2 KB)
- [SETUP.txt](attachments/SETUP.txt) (text/plain, 1.3 KB)

## Timeline

### an...@chromium.org (2026-02-23)

Hello, please provide a PoC that can be run against Chrome itself to demonstrate reachability.

### yu...@gmail.com (2026-02-23)

 Hi, thank you for the review.

  This vulnerability is in content.mojom.FrameHost, which is a channel-associated interface not accessible through BrowserInterfaceBroker, so a pure MojoJS HTML PoC is not feasible for this particular bug.

  To demonstrate reachability against Chrome itself (not browser_tests), please apply the attached renderer_trigger.patch and build Chrome:

  cd src
  git apply renderer_trigger.patch
  autoninja -C out/Default chrome

  Reproduction steps:
  1. Launch out/Default/chrome
  2. Open https://www.google.com in Tab A
  3. Open https://example.com in Tab B (the "attacker" tab)
  4. Click any link in Tab B

  Expected result (bug present):
  - Instead of normal navigation, Chrome searches all windows for google.com
  - Tab A is activated (focus moves to it)
  - Tab B is NOT navigated — confirming the side channel

  Why this is reachable from a compromised renderer:
  - WindowOpenDisposition::SWITCH_TO_TAB (value 10) is within the valid Mojo enum range [0-11], so it passes Mojo deserialization
  - VerifyOpenURLParams() in ipc_utils.cc validates URL, origin, blob — but performs zero checks on the disposition field
  - The value reaches GetBrowserAndTabForDisposition() where it is processed as a trusted browser-initiated disposition

  The browser_tests PoC (switch_to_tab_info_leak_browsertest.cc) is also attached for automated verification — it uses the exact same browser-side code path as Chrome and achieves 100% detection accuracy across 6 URL probes.

### pe...@google.com (2026-02-23)

Thank you for providing more feedback. Adding the requester to the CC list.

### ts...@google.com (2026-03-02)

Because the impact is limited to inferring browsing history (a baseline Medium impact) and requires a heavy precondition (a compromised renderer), downgrading one level and assessing as  a Low severity vulnerability,

### me...@google.com (2026-03-04)

Looks like a similar issue was reported in [bug 373551504](https://issues.chromium.org/issues/373551504)

### me...@google.com (2026-03-04)

alexmos: Could you PTAL or reassign as appropriate? Thanks.

### dx...@google.com (2026-03-16)

Project: chromium/src  

Branch:  main  

Author:  Alex Moshchuk [alexmos@chromium.org](mailto:alexmos@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7667272>

Validate WindowOpenDisposition sent by the renderer.

---


Expand for full commit details
```
     
    A compromised renderer could send arbitrary WindowOpenDisposition 
    values to the browser process in params for OpenURL or CreateNewWindow 
    IPCs. This CL introduces validation of the disposition on both of 
    these paths, only considering a disposition to be valid if a 
    well-behaving renderer could've sent it, as defined by 
    NavigationPolicyToDisposition() in render_frame_impl.cc. 
     
    As part of this, the existing validation for UNKNOWN dispositions is 
    generalized and moved into VerifyCreateNewWindowParams() in 
    ipc_utils.cc. 
     
    Bug: 486761170 
    Change-Id: I2342e7be72890cff86d5aab766b072ffa6d2d1a2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7667272 
    Commit-Queue: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Liam Brady <lbrady@google.com> 
    Auto-Submit: Alex Moshchuk <alexmos@chromium.org> 
    Reviewed-by: Mark Pearson <mpearson@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600147}

```

---

Files:

- M `content/browser/bad_message.h`
- M `content/browser/renderer_host/ipc_utils.cc`
- M `content/browser/renderer_host/render_frame_host_impl.cc`
- M `content/browser/renderer_host/render_frame_host_impl.h`
- M `content/browser/security_exploit_browsertest.cc`
- M `tools/metrics/histograms/metadata/stability/enums.xml`

---

Hash: [4ccc2d90a6436e5afbb0c20719f1cce58d916c49](https://chromiumdash.appspot.com/commit/4ccc2d90a6436e5afbb0c20719f1cce58d916c49)  

Date: Mon Mar 16 21:53:10 2026


---

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. User information disclosure


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Baseline. User information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486761170)*
