#  heap-use-after-free in v8_inspector::V8DebuggerAgentImpl::setBreakpointByUrl

| Field | Value |
|-------|-------|
| **Issue ID** | [493631402](https://issues.chromium.org/issues/493631402) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | sz...@google.com |
| **Created** | 2026-03-17 |
| **Bounty** | $3,000.00 |

## Description

VULNERABILITY DETAILS
UAF in v8_inspector::V8DebuggerAgentImpl::setBreakpointByUrl

VERSION
Chrome Version: 148.0.7728.0（Developer Build）
Operating System: Ubuntu

REPRODUCTION CASE
1. put manifest.json/background.js into the extension_path
2. run the command:
 ./chrome --user-data-dir=./noexist --no-sandbox --load-extension="extension_path"

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: see asan.log file

Please note that this bug is very similar to https://issues.chromium.org/u/2/issues/40063469.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: sakana

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 29.2 KB)
- deleted (application/octet-stream, 0 B)
- [manifest.json](attachments/manifest.json) (application/json, 209 B)
- [background.js](attachments/background.js) (text/javascript, 1.3 KB)

## Timeline

### ch...@google.com (2026-03-19)

This V8 bug has been marked as either a release blocker or a vulnerability bug. V8 bugs affect all OSs supported by Chrome, so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

### ar...@google.com (2026-03-19)

I could reproduce it on a Chrome ASan build, I will re-assign to DevTools to take a better look. Simon CYPTAL? It looks similar to http://crbug.com/485683106 but I am not an expert in this area.

### dx...@google.com (2026-03-23)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7690996>

[inspector] Don't emit scriptFailedToParse on setBreakpoint

---


Expand for full commit details
```
     
    Setting breakpoints triggers re-compilation if V8 hasn't compiled the 
    script yet or the GC evicted it. 
     
    If the top-level compilation fails, the inspector receives another 
    'scriptFailedToParse' event. 
     
    The "real" fix would be to forward a "CLEAR_EXCEPTION" bit into 
    'CompileTopLevel' in V8. 
     
    For now, we prevent setting breakpoints on broken scripts, they can't be 
    run in any case. 
     
    Drive-by: Catch exceptions when setting breakpoints in case there are 
    other ways where we re-enter V8 (e.g. via the regex). 
     
    R=bmeurer@chromium.org 
     
    Bug: 493631402 
    Change-Id: I18ec510a8288fd2a4bc44921ba538613ee8e1201 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7690996 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105967}

```

---

Files:

- M `src/inspector/v8-debugger-agent-impl.cc`
- M `src/inspector/v8-debugger-agent-impl.h`
- M `src/inspector/v8-debugger-script.cc`
- M `src/inspector/v8-debugger-script.h`
- M `src/inspector/v8-debugger.cc`
- A `test/inspector/debugger/set-breakpoint-by-url-in-broken-script-expected.txt`
- A `test/inspector/debugger/set-breakpoint-by-url-in-broken-script.js`

---

Hash: [606a11949ee0fecbb3cae68b0191814b6efb5cb1](https://chromiumdash.appspot.com/commit/606a11949ee0fecbb3cae68b0191814b6efb5cb1)  

Date: Mon Mar 23 11:43:12 2026


---

### dx...@google.com (2026-03-23)

Project: v8/v8  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7691238>

[inspector] Abort setBreakpointByUrl if Debugger domain was disabled

---


Expand for full commit details
```
     
    'setBreakpointByUrl' can trigger a debugger pause, where a client 
    could disable the Debugger domain all-together. This means we clear 
    m_scripts while still iterating it. 
     
    This CL guards against this by checking the 'enabled' state after 
    setting each breakpoint. 
     
    The regression test will be added on the blink side, due to specific 
    timing requirements of a V8 interrupt that we can't reproduce in 
    inspector-test. 
     
    R=bmeurer@chromium.org 
     
    Fixed: 493631402 
    Change-Id: I9d088e53c6d93bdbcc891d955bf4d3212a62345d 
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/7691238 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#105969}

```

---

Files:

- M `src/inspector/v8-debugger-agent-impl.cc`

---

Hash: [3942e1b16e4404c138df60655be1e27812e4d65c](https://chromiumdash.appspot.com/commit/3942e1b16e4404c138df60655be1e27812e4d65c)  

Date: Mon Mar 23 13:02:25 2026


---

### ch...@google.com (2026-03-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### dx...@google.com (2026-03-24)

Project: chromium/src  

Branch:  main  

Author:  Simon Zünd [szuend@chromium.org](mailto:szuend@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7693973>

[inspector] Add regression test for pause during setBreakpointByUrl

---


Expand for full commit details
```
     
    R=bmeurer@chromium.org 
     
    Bug: 493631402 
    Change-Id: Ibaeb22ba4cccf977e2067293a52c5023921dea36 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7693973 
    Commit-Queue: Benedikt Meurer <bmeurer@chromium.org> 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Simon Zünd <szuend@chromium.org> 
    Auto-Submit: Simon Zünd <szuend@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1603908}

```

---

Files:

- A `third_party/blink/web_tests/http/tests/inspector-protocol/debugger/regress-493631402-expected.txt`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/debugger/regress-493631402.js`
- A `third_party/blink/web_tests/http/tests/inspector-protocol/debugger/resources/broken.html`

---

Hash: [2fbc50835adc3d2047fd5f59f727f5bbc0224546](https://chromiumdash.appspot.com/commit/2fbc50835adc3d2047fd5f59f727f5bbc0224546)  

Date: Tue Mar 24 06:29:05 2026


---

### ch...@google.com (2026-03-24)

Setting milestone because of s2 severity.

### sa...@gmail.com (2026-04-15)

deleted

### sa...@gmail.com (2026-05-05)

Hi, any update?

### wf...@chromium.org (2026-06-25)

[vrp panel] please do not delete attachments, this is against the rules of the VRP. If you need to replace them, just add new ones and comment that they supercede previous ones.

### sp...@google.com (2026-06-29)

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

### ch...@google.com (2026-06-30)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493631402)*
