# heap-use-after-free READ in ElementRuleCollector InputRules path, page load, MiraclePtr unprotected

| Field | Value |
|-------|-------|
| **Issue ID** | [493837911](https://issues.chromium.org/issues/493837911) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Linux, ChromeOS |
| **Chrome Version** | 146.0.7680.x |
| **Reporter** | nn...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-03-18 |
| **Bounty** | $5,000.00 |

## Description

---

### Report description

Use-After-Free in ElementRuleCollector via input-type attribute reference invalidation

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/>

---

### The problem

#### Please describe the technical details of the vulnerability

## Description

`ElementRuleCollector::CollectMatchingRulesInternal()` in `element_rule_collector.cc` stores `input_type` as a `const AtomicString&` — a reference directly into the element's heap-allocated attribute vector. When iterating over multiple RuleSet bundles containing input-type rules, the first bundle's `CollectMatchingRulesForList()` can trigger `SynchronizeAttribute("style")` through a `[style]` component in the compound selector. This synchronization appends the style attribute to the vector, which may reallocate the underlying storage and free the old buffer. The second bundle then reads `input_type` from freed memory.

This is a variant of the bug fixed in commit `515ce02da3726` ("Fix a use-after-free with lazy style attributes", 2026-03-17). That fix addressed attribute-span invalidation in the `attr_rules` loop but missed this identical pattern in the `input_rules` loop. The root cause is the same: a reference into the attribute vector becomes dangling when `SynchronizeAttribute` triggers a reallocation.

**Why the existing fix doesn't cover this path:** A CSS rule like `input[style][type="text"]` is bucketed into `input_rules_` (not `attr_rules_`), because `ExtractBestBucketingValues` picks `[type="text"]` as the best bucket (it appears last and is an exact-match on `<input>`). Since the rule doesn't land in `attr_rules_`, `has_bucket_for_style_attr_` is never set, and the style attribute is not eagerly synchronized before the input-rules section.

## Steps to reproduce

1. Download the ASAN build of Chromium 146 for Linux x64 (or use `tools/get_asan_chrome.py` from the Chromium source tree).
2. Save the attached `poc.html` to disk.
3. Run with **zero flags**:
   
   ```
   chrome /path/to/poc.html
   
   ```
4. ASAN reports heap-use-after-free in stderr:
   
   ```
   ==PID==ERROR: AddressSanitizer: heap-use-after-free on address 0x...
   READ of size 8 at 0x... thread T0 (chrome)
   
   ```

No flags, no server, no user interaction required. Opening `poc.html` as a local `file://` URL is sufficient. The bug triggers during the first style resolution on page load.

## PoC

Attached: `poc.html`

The PoC is 17 lines. It creates an `<input type="text">` with 20 attributes (to ensure heap-allocated attribute vector near capacity), two `<style>` blocks that place rules in `input_rules_["text"]`, and two lines of JavaScript:

- `elem.style.color = 'red'` — dirties the style attribute (lazy, not yet in the vector)
- `getComputedStyle(elem).color` — triggers style resolution, exercising the vulnerable code path

## ASAN trace

Attached: `asan_trace.txt`

Key lines:

```
==PID==ERROR: AddressSanitizer: heap-use-after-free on address 0x...
READ of size 8 at 0x... thread T0 (chrome)

0x... is located 8 bytes inside of 352-byte region [0x...,0x...)
freed by thread T0 (chrome) here:
    #0 ... operator delete[]
    #1 ... (attribute vector reallocation during SynchronizeAttribute)

```
## Bisection

**Introducing commit:** `beb11ee6e2b1e` ("Add a separate selector bucket for input[type="..."] rules", 2025-06-13, Cr-Commit-Position: refs/heads/main@{#1473469})

This commit added the `input_rules_` bucket feature, introducing the `input_type` variable as a `const AtomicString&` reference into the attribute vector. The reference was never safe — it can be invalidated whenever `CollectMatchingRulesForList()` triggers lazy style synchronization. The closely-related `attr_rules` loop already had protection against this (via the `NeedStyleSynchronized` mechanism), but the new `input_rules` code didn't replicate that protection.

**Incomplete fix:** `515ce02da3726` ("Fix a use-after-free with lazy style attributes", 2026-03-17) fixed the analogous issue in the `attr_rules` loop by changing `lower_name` from `const AtomicString&` to `const AtomicString` and refreshing the attribute span inside the inner loop. The `input_type` reference in the `input_rules` section was not similarly fixed.

**Affected release channels:** The introducing commit landed at position `@{#1473469}` (June 2025). Based on the Chrome release schedule, this affects approximately **Chrome 138 through Chrome 146** (current tip-of-tree). All stable, beta, and dev channels with this code are affected.

## Suggested fix

Change `input_type` from `const AtomicString&` to `const AtomicString` (value copy) in `CollectMatchingRulesInternal()`, matching the fix applied to `lower_name` in commit `515ce02da3726`.

#### Impact analysis

## Impact

A web page with crafted CSS selectors and two lines of JavaScript triggers a heap-use-after-free (8-byte read from a freed 352-byte region) in the renderer process. The freed memory is from the element's attribute vector. No user interaction is required beyond visiting the page.

---

### The cause

#### What version of Chrome have you found the security issue in?

Chromium 146.0.7680.0 (ASAN build, linux x64)

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

M. Fauzan Wijaya (Gh05t666nero)

## Attachments

- [asan_trace.txt](attachments/asan_trace.txt) (text/plain, 20.6 KB)
- [poc.html](attachments/poc.html) (text/html, 593 B)
- [symbolized_asan_report.txt](attachments/symbolized_asan_report.txt) (text/plain, 49.1 KB)
- [asan_trace_symbolized.txt](attachments/asan_trace_symbolized.txt) (text/plain, 8.6 KB)

## Timeline

### ts...@google.com (2026-03-18)

You'll need to symbolize your ASAN stack trace before we can accept such a a report.

### oj...@gmail.com (2026-03-18)

Thanks. You are right that the originally attached ASAN log was not symbolized correctly.

I have now symbolized the trace and attached the full symbolized report as `symbolized_asan_report.txt`. I also included a shorter excerpt in `asan_trace_symbolized.txt` for convenience.

The `invalid path to external symbolizer` lines in the log are from the original run; the attached file is the offline-symbolized version of that same ASAN report.

The top of the symbolized crash resolves to:

```
#0 blink::AtomicString::LowerASCII() const
#1 blink::ElementRuleCollector::CollectMatchingRulesInternal<false>(...)
   third_party/blink/renderer/core/css/element_rule_collector.cc:957

```

The free side resolves to attribute-vector reallocation during lazy style attribute synchronization:

```
blink::Vector<blink::Attribute>::ReallocateBuffer(...)
blink::MutableAttributeCollection::Append(...)
blink::Element::AppendAttributeInternal(...)
blink::Element::SetSynchronizedLazyAttribute(...)
blink::Element::SynchronizeStyleAttributeInternal() const
blink::Element::SynchronizeAttributeHinted(...) const

```

This matches the reported root cause: in the `input_rules` path, `input_type` is kept as a `const AtomicString&` from the element's attribute storage, and a later selector match can lazily synchronize the `style` attribute, reallocating the attribute vector before the next `input_rules` bundle reads `input_type`.

The primary attachment is `symbolized_asan_report.txt`.

### oj...@gmail.com (2026-04-01)

Following up, since my symbolized report from 2026-03-19 did not receive a further response.

After re-checking current Chromium source, this issue appears to match a fix that landed on 2026-03-20:

d8b01057f740d3bb0ec880b34372da63147c2521
"Fix another use-after-free with lazy style attributes."

That change patches the exact input[type] / lazy style synchronization path described in this report. Specifically, in ElementRuleCollector::CollectMatchingRulesInternal(), it adds a note that the input\_type reference may become dangling if CollectMatchingRulesForList() adds lazy attributes, then copies the value into a stable AtomicString before iterating the input-rules loop.

This is the same root cause described here:
a const AtomicString& obtained from the element’s attribute storage can become invalid when lazy style attribute synchronization reallocates the attribute vector during selector matching.

The fixing change also adds a regression test:
third\_party/blink/web\_tests/external/wpt/css/css-values/crashtests/chrome-bug-493952652.html

That test covers the same material pattern:

- input[style][type="text"]
- lazy style synchronization
- repeated input-rules evaluation using type="text"

For timeline context:

- this report was filed on 2026-03-18
- my symbolized follow-up was posted on 2026-03-19
- the fix landed on 2026-03-20

The commit references [issue 493952652](https://issues.chromium.org/issues/493952652) rather than this issue, so this may have been fixed under another tracker entry. If so, could this report please be re-evaluated as a duplicate / precursor of the fixed issue rather than remaining in “Won’t Fix / Not Reproducible”, and could reporter credit be reviewed accordingly?

If useful, I can provide a direct mapping between the reported root cause and commit d8b01057f740d3bb0ec880b34372da63147c2521.

### ch...@google.com (2026-04-01)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### ch...@google.com (2026-06-25)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493837911)*
