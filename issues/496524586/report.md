# setHTML() fails open on invalid SanitizerConfig, inserting unsanitized HTML with active scripts into the live DOM

| Field | Value |
|-------|-------|
| **Issue ID** | [496524586](https://issues.chromium.org/issues/496524586) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qw...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2026-03-26 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

setHTML() fails open on invalid SanitizerConfig, inserting unsanitized HTML with active scripts into the live DOM

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src>

---

### The problem

#### Please describe the technical details of the vulnerability

## Summary

`Element.setHTML()` fails open on invalid `SanitizerConfig`, inserting unsanitized HTML with active scripts into the live DOM.

When `Sanitizer::Create` throws a `TypeError` due to an invalid config (e.g., both `elements` and `removeElements` specified), the parsed but unsanitized `DocumentFragment` is inserted into the DOM. Event handler attributes such as `ontoggle` and `onerror` execute JavaScript immediately after insertion.

## Chrome Version

- Tested on Chrome 146.0.7680.164 (Official Build, 64-bit), Linux x86\_64
- Affected on All Chrome versions with the Sanitizer API enabled

## Root Cause

### `SanitizeSafeInternal` does not clear fragment on Sanitizer creation failure

File: `third_party/blink/renderer/core/sanitizer/sanitizer_api.cc`

When `SanitizerFromSafeOptions` fails, the function returns without clearing the fragment at lines 107–109:

```
if (exception_state.HadException()) {
    return;  // BUG: does NOT clear root_element
}

```

The earlier error path in the same function at lines 90–92 correctly clears it:

```
if (exception_state.HadException()) {
    root_element->setTextContent("");  // CORRECT: clears unsanitized content
    return;
}

```

The unsanitized fragment is unconditionally inserted into the live DOM. The TypeError propagates to JS, but the DOM is already modified and event handlers have already fired.

## Reproduction

`Sanitizer::setFrom()` returns false when the config is invalid per spec:

- Both `elements` and `removeElements` present (sanitizer.cc:1170)
- Both `attributes` and `removeAttributes` present (sanitizer.cc:1175)
- `elements` and `replaceWithChildrenElements` overlap (sanitizer.cc:1184)
- Duplicate entries in any list (sanitizer.cc:1058)

`Sanitizer::Create` then throws TypeError at sanitizer.cc:65, entering the fail-open path.

### Example

```
var el = document.createElement('div');
document.body.appendChild(el);
try {
  el.setHTML(
    '<details open ontoggle="alert(document.domain)"><summary>x</summary></details>' +
    '<img src=x onerror="alert(\'onerror XSS\')">',
    { sanitizer: { elements: ['div'], removeElements: ['span'] } }
  );
} catch(e) { console.log(e.message); }
console.log(el.innerHTML);

```

Expected: TypeError thrown, element remains empty and no script execution.

Actual: TypeError thrown but element contains unsanitized HTML. `alert(document.domain)` fires via ontoggle. `alert('onerror XSS')` fires via onerror. `<script>`, `<iframe>`, `javascript:` URLs all survive in the DOM.

## Suggested Fix

### Clear fragment on exception in `SanitizeSafeInternal`

The bug is that the error path at lines 107–109 does not clear the fragment, unlike the correct pattern at lines 90–92. The fix is to add `root_element->setTextContent("")` so all error paths consistently clear unsanitized content.

File: `third_party/blink/renderer/core/sanitizer/sanitizer_api.cc`

`SanitizeSafeInternal`, around line 107:

```
  const Sanitizer* sanitizer =
      SanitizerFromSafeOptions(options, exception_state);

  if (exception_state.HadException()) {
+   root_element->setTextContent("");
    return;
  }

```

This matches the existing correct pattern already used earlier:

```
// Lines 90-92 (SanitizeSafeInternal)
if (exception_state.HadException()) {
    root_element->setTextContent("");  // Already correctly clears fragment here
    return;
}

```
#### Impact analysis

setHTML() fails to sanitize HTML when given an invalid SanitizerConfig. The unsanitized content, including event handlers and script tags, is inserted into the live DOM and executes. This violates the spec guarantee that setHTML() always strips XSS-unsafe content.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.164 stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Cross-site scripting (XSS)

#### How would you like to be publicly acknowledged for your report?

Jungwoo Lee (@physicube) and Wongi Lee (@\_qwerty\_po)

## Attachments

- [poc.html](attachments/poc.html) (text/html, 433 B)
- [poc.html](attachments/poc_74810585.html) (text/html, 433 B)

## Timeline

### vo...@google.com (2026-03-26)

Can reproduce. Thanks for the report.

Well, that one is rather embarrasing... we throw an exception and still perform the operation! :-(

### vo...@google.com (2026-03-26)

The fix proposed -- clearing the result fragment -- certainly works, and would IMHO indeed be the root cause. But, we usually have an invariant that when a function raises a JS exception, it also shouldn't return a result. Which none of the callers adhere to. So, despite a pending exception being signalled, they all just return the processing result anyway. I think that ought to be fixed as well.

### vo...@google.com (2026-03-26)

Tentative fix in <https://chromium-review.googlesource.com/c/chromium/src/+/7705032>

### vo...@google.com (2026-03-26)

This situation is covered by plenty of WPT tests, but *of course* for exception cases these test only verify whether an exception was thrown. The idea that an exception was thrown but the operation was performed anyways wasn't considered.

### ch...@google.com (2026-03-27)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-27)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### qw...@gmail.com (2026-03-27)

Could you please add jwlee2217@gmail.com to the CC list (or the Reporter field) so that both accounts can access the issue?

### dx...@google.com (2026-04-02)

Project: chromium/src  

Branch:  main  

Author:  Daniel Vogelheim [vogelheim@chromium.org](mailto:vogelheim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7705032>

[Sanitizer] Ensure content is removed when an exception is thrown.

---


Expand for full commit details
```
     
    When the sanitize operation throws an exception, we don't clear the 
    parse result. Also, the callers will pass through the exception, but 
    will return the incomplete result to the callers. 
     
    Fixed: 496524586 
    Change-Id: I3a6402afacb5d5275f546dfdefdac5d270e96d1f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7705032 
    Reviewed-by: Noam Rosenthal <nrosenthal@google.com> 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Commit-Queue: Daniel Vogelheim <vogelheim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1609133}

```

---

Files:

- M `third_party/blink/renderer/core/dom/document.cc`
- M `third_party/blink/renderer/core/dom/document_test.cc`
- M `third_party/blink/renderer/core/html/parser/fragment_parser.cc`
- M `third_party/blink/renderer/core/sanitizer/sanitizer_api.cc`
- M `third_party/blink/web_tests/external/wpt/sanitizer-api/sethtml-tree-construction.tentative.html`

---

Hash: [54315b858250350774108ce6b986606e0d77efe7](https://chromiumdash.appspot.com/commit/54315b858250350774108ce6b986606e0d77efe7)  

Date: Thu Apr 2 12:39:20 2026


---

### aj...@google.com (2026-06-03)

-> Low as this requires a website misconfiguration.

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. UXSS || Site isolation bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-07-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ch...@google.com (2026-07-11)

This Blink bug has been marked as either a release blocker or a vulnerability bug. Blink bugs affect all OSs supported by Chrome (except iOS), so the OS field has been updated to reflect this. Please update the bug with the correct OS field if it only affects a subset of OSes.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/496524586)*
