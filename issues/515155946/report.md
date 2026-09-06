# Heap-use-after-free read in `blink::Document::ProcessBaseElement` via re-entrant SpeculationRules error dispatch from `UpdateBaseURL`

| Field | Value |
|-------|-------|
| **Issue ID** | [515155946](https://issues.chromium.org/issues/515155946) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>Loader>Preload |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | qw...@gmail.com |
| **Assignee** | nh...@chromium.org |
| **Created** | 2026-05-20 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

1. Download ASAN Chromium Download [asan-win32-release\_x64-1633823.zip](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/win32-release_x64%2Fasan-win32-release_x64-1633823.zip?generation=1779317172944118&alt=media)
2. Launch Chrome

```
chrome.exe --no-sandbox poc.html

```
# Problem Description

`Document::ProcessBaseElement` borrows a raw `const AtomicString*` into a `<base>` element's mutable `AttributeVector` slot and then calls `Document::UpdateBaseURL`. `UpdateBaseURL` synchronously dispatches a JavaScript `error` event on any speculation-rules `<script>` whose source is not a JSON object. The handler can mutate the same `<base>` element so the `AttributeVector` backing buffer is freed and the slot pointed to by the saved raw pointer is reclaimed. When the outer call resumes, it reads `target->impl_` from the freed bucket via `StringImpl::find` and `scoped_refptr::operator=`, dereferencing freed memory and calling `StringImpl::AddRef` on an attacker-influenced pointer value.

Any `b.href = ...` or `b.target = ...` from script enters `Document::ProcessBaseElement` via `HTMLBaseElement::ParseAttribute` (`third_party/blink/renderer/core/html/html_base_element.cc:36`). That function saves a raw `const AtomicString*` pointing into the first `<base>`'s `target` attribute storage, then calls `UpdateBaseURL` while that pointer is still live on the stack:

```
// Document::ProcessBaseElement  third_party/blink/renderer/core/dom/document.cc:5099
5099:    const AtomicString* href = nullptr;
5100:    const AtomicString* target = nullptr;
...
5113:          target = &value;  // raw pointer into a mutable Attribute slot inside AttributeVector
...
5147:    if (base_element_url != base_element_url_) {  // forced true by the attacker changing `b.href`
...
5164:      UpdateBaseURL();  // synchronous callout while `target` is still borrowed above
5165:    }

```

`UpdateBaseURL` (`document.cc:5019`) iterates every `HTMLScriptElement` descendant on the same stack and calls `ScriptLoader::DocumentBaseURLChanged` on each. For a `<script type="speculationrules">` element, that re-parses the original source under the new base URL via `AddSpeculationRuleSet`, which fires an `error` event when the JSON parses to anything other than an object (e.g., the top-level array `[]`):

```
// ScriptLoader::AddSpeculationRuleSet  third_party/blink/renderer/core/script/script_loader.cc:1380
1380:    if (speculation_rule_set_->error_type() ==
1381:            SpeculationRuleSetErrorType::kSourceIsNotJsonObject ||  // `[]` is JSON but not an object, this branch fires
1382:        speculation_rule_set_->error_type() ==
1383:            SpeculationRuleSetErrorType::kInvalidRulesetLevelTag) {
...
1386:      element_->DispatchErrorEvent();  // runs attacker `onerror` JS on the same stack while `target` is still borrowed

```

A single `setAttribute` from the `onerror` handler is enough to free the buffer `target` borrowed from. `Vector::push_back` falls into `Vector::AppendSlowCase` when at capacity, which allocates a new `BufferPartition` buffer, moves the elements over, and frees the old one:

```
// Vector::AppendSlowCase  third_party/blink/renderer/platform/wtf/vector.h:2380
2382:  Vector<T, InlineCapacity, Allocator>::AppendSlowCase(U&& val) {
2383:    DCHECK_EQ(size(), capacity());
...
2386:    ptr = ExpandCapacity(size() + 1, ptr);  // allocates new buffer, copies, FREES the buffer `target` points into
2392:  }

```

With six attributes the `AttributeVector` (`Vector<Attribute, 4>`) already uses an external 96-byte buffer, one `setAttribute` grows it and frees that buffer, leaving `target` dangling.

When the error event returns, `Document::ProcessBaseElement` resumes and dereferences the stale pointer three times:

```
// Document::ProcessBaseElement  third_party/blink/renderer/core/dom/document.cc:5167
5167:    AtomicString old_base_target = base_target_;
5168:    if (target) {
5169:      if (target->contains('\n') || target->contains('\r')) {  // UAF
...
5172:      if (target->contains('<')) {                              // UAF
...
5175:      base_target_ = *target;                                   // UAF

```
# Summary

Use-After-Free via re-entrant attribute mutation during synchronous speculation-rules error dispatch

# Custom Questions

#### Type of crash:

renderer

#### Crash state:

Please see asan.log

#### Reporter credit:

pwn2addr

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- [poc.html](attachments/poc.html) (text/html, 197 B)
- [asan.log](attachments/asan.log) (text/plain, 58.1 KB)
- [symbolized_stacktrace.txt](attachments/symbolized_stacktrace.txt) (text/plain, 45.0 KB)

## Timeline

### ja...@google.com (2026-05-21)

[security triage]

Thanks for the report. I was able to reproduce this on 150.0.7848.0 (Developer Build) custom (64-bit) for Linux. I've attached the stacktrace.

### ja...@google.com (2026-05-21)

[security triage]

Severity tentatively looks good at High (S1) for memory corruption in the renderer process: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md#toc-high-severity>

Added the other desktop OSes since it impacts at least Linux and Windows.

Set component to Blink > HTML and added some OWNERS to cc.

### cl...@appspot.gserviceaccount.com (2026-05-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5946281507717120.

### ch...@google.com (2026-05-21)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### 24...@project.gserviceaccount.com (2026-05-21)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-05-21)

Detailed Report: https://clusterfuzz.com/testcase?key=5946281507717120

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x76d63da10d68
Crash State:
  blink::Document::ProcessBaseElement
  blink::Element::AttributeChanged
  blink::HTMLElement::AttributeChanged
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1488631:1488632

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5946281507717120

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### db...@chromium.org (2026-05-21)

Changing severity back to S1 because this is only in the renderer process, per [guidelines](https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md#TOC-High-severity).

### dx...@google.com (2026-05-22)

Project: chromium/src  

Branch:  main  

Author:  David Baron [dbaron@chromium.org](mailto:dbaron@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7868910>

Make Document::ProcessBaseElement store strings rather than pointers to strings.

---


Expand for full commit details
```
     
    This changes Document::ProcessBaseElement to use AtomicString rather 
    than using const AtomicString* that point into an element's attribute 
    storage (which could be modified in the middle of the function). 
     
    Fixed: 515155946 
    Change-Id: I56dba34c3df8e0b3752b4bfcc2ee6c248694bcc0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7868910 
    Reviewed-by: Mason Freed <masonf@chromium.org> 
    Commit-Queue: David Baron <dbaron@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1634618}

```

---

Files:

- M `third_party/blink/renderer/core/dom/document.cc`
- A `third_party/blink/web_tests/external/wpt/html/semantics/document-metadata/the-base-element/crashtests/base-with-speculation-rules-onerror.html`

---

Hash: [dffb572d0b0cdf92d0aaef482ffc4d22cef4cabc](https://chromiumdash.appspot.com/commit/dffb572d0b0cdf92d0aaef482ffc4d22cef4cabc)  

Date: Fri May 22 00:23:40 2026


---

### ch...@google.com (2026-05-22)

Setting milestone because of s0/s1 severity.

### 24...@project.gserviceaccount.com (2026-05-22)

ClusterFuzz testcase 5946281507717120 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1634613:1634627

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-05-23)

Requesting merge to M148 because latest trunk commit is in 150.

Security Merge Request:

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Requesting merge to M149 because latest trunk commit is in 150.

### ch...@google.com (2026-05-23)

**M148** merge request created. **Please update [crbug/515954109](https://crbug.com/515954109) to have this merge reviewed.**

### ch...@google.com (2026-05-23)

**M149** merge request created. **Please update [crbug/515953855](https://crbug.com/515953855) to have this merge reviewed.**

### dx...@google.com (2026-05-23)

Project: chromium/src  

Branch:  refs/branch-heads/7778  

Author:  David Baron [dbaron@chromium.org](mailto:dbaron@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869838>

[M148] Make Document::ProcessBaseElement store strings rather than pointers to strings.

---


Expand for full commit details
```
     
    Original change's description: 
    > Make Document::ProcessBaseElement store strings rather than pointers to strings. 
    > 
    > This changes Document::ProcessBaseElement to use AtomicString rather 
    > than using const AtomicString* that point into an element's attribute 
    > storage (which could be modified in the middle of the function). 
    > 
    > Fixed: 515155946 
    > Change-Id: I56dba34c3df8e0b3752b4bfcc2ee6c248694bcc0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7868910 
    > Reviewed-by: Mason Freed <masonf@chromium.org> 
    > Commit-Queue: David Baron <dbaron@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1634618} 
     
    (cherry picked from commit dffb572d0b0cdf92d0aaef482ffc4d22cef4cabc) 
     
    Bug: 515954109,515155946 
    Change-Id: I56dba34c3df8e0b3752b4bfcc2ee6c248694bcc0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869838 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7778@{#3568} 
    Cr-Branched-From: 77f495ee216d4c3cc784d33658bad4778c0680ee-refs/heads/main@{#1610480}

```

---

Files:

- M `third_party/blink/renderer/core/dom/document.cc`
- A `third_party/blink/web_tests/external/wpt/html/semantics/document-metadata/the-base-element/crashtests/base-with-speculation-rules-onerror.html`

---

Hash: [c48d8866a56122d6c5bd526e60224489193ec4e9](https://chromiumdash.appspot.com/commit/c48d8866a56122d6c5bd526e60224489193ec4e9)  

Date: Sat May 23 13:59:40 2026


---

### dx...@google.com (2026-05-23)

Project: chromium/src  

Branch:  refs/branch-heads/7827  

Author:  David Baron [dbaron@chromium.org](mailto:dbaron@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7869837>

[M149] Make Document::ProcessBaseElement store strings rather than pointers to strings.

---


Expand for full commit details
```
     
    Original change's description: 
    > Make Document::ProcessBaseElement store strings rather than pointers to strings. 
    > 
    > This changes Document::ProcessBaseElement to use AtomicString rather 
    > than using const AtomicString* that point into an element's attribute 
    > storage (which could be modified in the middle of the function). 
    > 
    > Fixed: 515155946 
    > Change-Id: I56dba34c3df8e0b3752b4bfcc2ee6c248694bcc0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7868910 
    > Reviewed-by: Mason Freed <masonf@chromium.org> 
    > Commit-Queue: David Baron <dbaron@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1634618} 
     
    (cherry picked from commit dffb572d0b0cdf92d0aaef482ffc4d22cef4cabc) 
     
    Bug: 515953855,515155946 
    Change-Id: I56dba34c3df8e0b3752b4bfcc2ee6c248694bcc0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7869837 
    Commit-Queue: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: rubber-stamper@appspot.gserviceaccount.com <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7827@{#1577} 
    Cr-Branched-From: 9f3e9aaccba63bd2ec30334e45e0bfd07ebcc8f1-refs/heads/main@{#1625079}

```

---

Files:

- M `third_party/blink/renderer/core/dom/document.cc`
- A `third_party/blink/web_tests/external/wpt/html/semantics/document-metadata/the-base-element/crashtests/base-with-speculation-rules-onerror.html`

---

Hash: [f10ad92d63df3d7354bb73a5c1e1353a32132afe](https://chromiumdash.appspot.com/commit/f10ad92d63df3d7354bb73a5c1e1353a32132afe)  

Date: Sat May 23 14:05:37 2026


---

### pe...@google.com (2026-05-23)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### db...@chromium.org (2026-05-23)

Re [comment #17](https://issues.chromium.org/issues/515155946#comment17), regarding LTS Milestone M144:

1. No, it's been around for a while (though I didn't check exactly when).
2. No.

### nh...@chromium.org (2026-05-27)

FYI: [issue 506347575](https://issues.chromium.org/issues/506347575) was merged into this issue. It was filed on Apr 25.

### sp...@google.com (2026-05-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
ASAN Write, UAF. Other Processes - Renderer


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### qk...@google.com (2026-07-30)

Add `LTS-NotApplicable-144`, as the patch required additional dependent CLs[1], which in turn necessitated further changes. Consequently, it is not safe to merge all of them back into the M144 LTS.

[1] <https://chromium-review.git.corp.google.com/c/chromium/src/+/7533096>

### ch...@google.com (2026-08-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> ASAN Write, UAF. Other Processes - Renderer

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/515155946)*
