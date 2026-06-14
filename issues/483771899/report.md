# HTML5 Sandbox Security Model Violation with auxiliary browsing contexts being created despite the lack of "allow-popups" keyword within iframes

| Field | Value |
|-------|-------|
| **Issue ID** | [483771899](https://issues.chromium.org/issues/483771899) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>IFrameSandbox |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2017-2371 |
| **Reporter** | ci...@exploit.cat |
| **Assignee** | ja...@chromium.org |
| **Created** | 2026-02-11 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

HTML5 Sandbox Security Model Violation with auxiliary browsing contexts being created despite the lack of "allow-popups" keyword within iframes

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/loader/navigation_policy.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

The vulnerability exists within the Blink rendering engine's handling of navigation policies derived from mouse events. Specifically, the function `NavigationPolicyFromEventInternal` in `third_party/blink/renderer/core/loader/navigation_policy.cc` fails to validate the `isTrusted` property of a `MouseEvent` before honoring modifier keys (such as `ctrlKey` or `metaKey`).

In a standard HTML5 sandbox environment, an iframe without the `allow-popups` flag is prohibited from opening new auxiliary browsing contexts (windows or tabs). However, this restriction relies on the renderer correctly calculating the Navigation Policy for a given action.

When a user performs a `Ctrl+Click` (or `Cmd+Click` on macOS) on a link, Blink translates this into a navigation policy of `kNavigationPolicyNewBackgroundTab` or `kNavigationPolicyNewForegroundTab`. The vulnerability arises because JavaScript within a sandboxed iframe can programmatically construct a synthetic `MouseEvent` with these modifier keys set to `true` and dispatch it against an anchor element.

Because `NavigationPolicyFromEventInternal` does not check if the event is trusted (`event.isTrusted()`), it blindly processes the synthetic modifiers. Consequently, the renderer calculates a "New Tab" navigation policy and requests the browser to open a new window. This effectively bypasses the `allow-popups` restriction, as the browser treats the request as a legitimate link navigation with a specific disposition, rather than a blocked `window.open` call.

#### Impact analysis

This vulnerability is a security bypass of the HTML5 sandbox `allow-popups` restriction. While typically classified as a sandbox escape in standard browsers (allowing untrusted content to annoy users or facilitate phishing via popups), the impact is significantly amplified in certain Electron-based applications, such as the Discord Desktop Client, where it can serve as a primitive for Remote Code Execution (RCE).

**Core Impact: Sandbox Escape & Security Control Bypass**

The vulnerability allows sandboxed content (explicitly restricted from creating new windows) to force the creation of an auxiliary browsing context. This directly violates the integrity of the `sandbox` attribute, rendering the `allow-popups` flag ineffective against a malicious actor capable of executing JavaScript.

**High-Severity Exploitation in Electron (Discord RCE Chain)**

In the context of the Discord Desktop Client, this sandbox escape bridges the gap between a restricted renderer process and privileged system operations.

- Mechanism: Electron applications often intercept new window creation events (such as via `webContents.on('new-window')` or `setWindowOpenHandler`) to delegate external link handling to the operating system using `shell.openExternal()`.
- The Bypass: Discord implements checks to prevent sandboxed iframes from triggering this flow. However, because the vulnerability forces the Blink engine to classify the synthetic event as a legitimate, user-initiated "New Tab" navigation (via the `kNavigationPolicyNewForegroundTab` policy), it bypasses renderer-side checks that rely on standard `window.open` restrictions.
- RCE Vector: By successfully triggering `shell.openExternal()` with a malicious payload, we demonstrated the ability to execute arbitrary code on the host machine.
  - Violation: This directly violates the Electron security best practice: *" Do not use shell.openExternal with untrusted content"*. [Electron Checklist #15](https://www.electronjs.org/docs/latest/tutorial/security#15-do-not-use-shellopenexternal-with-untrusted-content)
  - Chain: `Sandboxed Iframe` -> `Synthetic Ctrl+Click` -> `Sandbox Bypass (New Window Request)` -> `Electron Interception` -> `shell.openExternal(malicious_URI)` -> `RCE`.

This finding confirms that the "One Permitted Navigator" principle and standard event validation are insufficient in their current state to protect embedding contexts from synthetic input attacks.

---

### The cause

#### What version of Chrome have you found the security issue in?

[145.0.7632.46]

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Sandbox Escape

#### How would you like to be publicly acknowledged for your report?

Credit to my GitHub @Ciarands

## Attachments

- [2026-02-11_21-58-01.ffmpeg.mp4](attachments/2026-02-11_21-58-01.ffmpeg.mp4) (video/mp4, 126.9 KB)
- [index.html](attachments/index.html) (text/html, 1.8 KB)
- [popups_bypass.html](attachments/popups_bypass.html) (text/html, 1.2 KB)
- [electron-test.zip](attachments/electron-test.zip) (application/zip, 1.3 KB)
- [drive_by_download_demo.html](attachments/drive_by_download_demo.html) (text/html, 1.1 KB)

## Timeline

### om...@chromium.org (2026-02-12)

This is not a V8 sandbox issue. It relates to the Chromium sandbox.

### za...@google.com (2026-02-12)

ah! thanks.
Assigning this to blink loader owner - japhet@, can you please take a look at this and help investigate?

### ch...@google.com (2026-02-12)

Setting milestone because of s0/s1 severity.

### ma...@google.com (2026-02-13)

Security shepherd: Provisionally setting OS

### ja...@chromium.org (2026-02-17)

I have a CL that fixes this (https://chromium-review.googlesource.com/c/chromium/src/+/7572487), now I'm just trying to figure out whether I can include a good regression test.

One subtlety that I hadn't appreciated at first: this still requires the user to click the link. Our general popup blocking mechanism detects and blocks this if the Ctrl+Click is *entirely* synthetic. But this does allow a sandboxed iframe to "upgrade" a user activation into a popup when it shouldn't be able to.

### ci...@exploit.cat (2026-02-17)

Hey Japhet,

Thanks for the update. Wanted to build on your observation. A user doesn't need to directly interact with the iframe. If the user interacts with the window containing the iframe (A click or keyboard event) then we can trigger our synthetic `Ctrl+Click`. Attached is a POC to demo this.
In the context of Electron apps like the Discord desktop client, we don't actually have to deal with the popup blocking mechanism at all, we can trigger URI protocols arbitrarily without user input.

### ja...@chromium.org (2026-02-17)

Thanks for the additional repro variant! This example is somewhat mitigated (at least in a regular chromium build, I assume electron too?) by our navigation throttling mechanism, which makes `fireClickEvent()` unreliable because we're trying to navigate so frequently. Eventually a click somewhere in the embedding window will result in the popup, though.

### ci...@exploit.cat (2026-02-17)

No problem, thanks for the confirmation! I can confirm that it seems no such mitigations are present in electron latest. However, this might be best separately brought to the attention of the Electron devs? Attached is a POC for you to be able to test, this should pop 4 calculators without user interaction. (Please take care if testing the popups_bypass.html payload, I accidentally fork bombed myself with this...)

### ci...@exploit.cat (2026-02-18)

After a bit more investigation, it seems the navigation throttling mechanism can also be rendered ineffective by adding a check for `navigator.userActivation.isActive` (https://developer.mozilla.org/en-US/docs/Web/API/Navigator/userActivation) before firing the `MouseEvent`. Making `fireClickEvent` consistently reliable within the regular chromium build too.

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  main  

Author:  Nate Chapin [japhet@chromium.org](mailto:japhet@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7572487>

FrameLoader::StartNavigation should not allow emulated Ctrl+click from sandboxed iframes

---


Expand for full commit details
```
     
    Fixed: 483771899 
    Change-Id: I1e134f0c9dcfbb4760d339d909a7d7339a5e3077 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7572487 
    Commit-Queue: Nate Chapin <japhet@chromium.org> 
    Reviewed-by: Daniel Cheng <dcheng@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1587969}

```

---

Files:

- M `third_party/blink/renderer/core/frame/frame_test_helpers.h`
- M `third_party/blink/renderer/core/frame/web_frame_test.cc`
- M `third_party/blink/renderer/core/loader/frame_loader.cc`
- M `third_party/blink/renderer/core/testing/data/core_test_bundle_data.filelist`
- A `third_party/blink/renderer/core/testing/data/sandboxed-srcdoc-ctrl-click.html`

---

Hash: [874355605d632c59770046b1a1fc1582f68361dc](https://chromiumdash.appspot.com/commit/874355605d632c59770046b1a1fc1582f68361dc)  

Date: Fri Feb 20 19:02:15 2026


---

### ch...@google.com (2026-02-21)

Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1587969) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1587969) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-21)

Merge review required: M146 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2026-02-21)

Merge review required: M145 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-02-24)

I don't think the security consequences for Chrome merit a merge here. The consequences for Chrome in the initial report are just "annoy users or facilitate phishing via popups". That would not be a vulnerability in Chrome's threat model. Given this could have much worse consequences in Electron, I'll leave this as a Low severity vulnerability to avoid disclosing this before they can pick up the fix from [#comment11](https://issues.chromium.org/issues/483771899#comment11).

### ci...@exploit.cat (2026-02-26)

Thanks for the feedback! I completely agree that if we are only factoring in the previously discussed "tab spam" consequences in Chrome, this does not meet the criteria for an S1 vulnerability.

I would like to respectfully request a re-evaluation of this as an S2 vulnerability, as the core issue is the bypass of the HTML5 iframe sandbox security boundaries, not just the resulting annoyance that was previously demonstrated. By escaping the sandbox, we are able to perform "tab-nabbing" attacks (like WebKit's CVE-2017-2371 https://nvd.nist.gov/vuln/detail/CVE-2017-2371) and, as demonstrated in this additional variant, perform unrestricted "drive-by downloads." without users consent.

In the attached PoC, the injected iframe is sandboxed with limited privileges: sandbox="allow-scripts allow-same-origin". Lacking flags such as "allow-popups" and "allow-downloads". Under the web platform security model, this iframe should be completely restricted from performing actions such as opening new windows or triggering downloads, regardless of user interaction.

Could we please re-evaluate this primitive as a HTML5 sandbox violation and user-activation bypass?

### ci...@exploit.cat (2026-02-27)

I should add, the impact of this variant could realistically affect any site which has an untrusted iframe (for advertisement or similar integrations) alongside a legitimate download page. A sandboxed iframe abusing this primitive could trigger downloads of attacker-controlled binaries that appear to originate from the legitimate application's download flow, undermining the protection that the HTML5 sandbox boundary is meant to provide.

### es...@chromium.org (2026-02-28)

Note: the downloads variant of this bug was previously reported in issue 40061220. https://chromium-review.googlesource.com/7572487 fixes both this and the other bug. I'm not sure if we should consider them duplicates or not.

### ci...@exploit.cat (2026-04-27)

As this is still an issue downstream in electron and separately in Firefox, just wanted to check that this would remain restricted until all affected vendors are able to resolve?
In electron the OpenURLFromTab doesn't check user_gesture making this 0click, and when no `setWindowOpenHandler` is defined a new BrowserWindow is created which does not inherit restrictions added to the original window.
I have created a GHSA for Electron and separately reported this on Mozillas bug tracker. I will be able to provide updates as these other vendors are able to resolve this independently.

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Web Platform Privilege Escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ci...@exploit.cat (2026-05-30)

This is still an issue downstream. Was this meant to be made public?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/483771899)*
