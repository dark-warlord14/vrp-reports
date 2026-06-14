# Type confusion in InspectorCSSAgent::setScopeText

| Field | Value |
|-------|-------|
| **Issue ID** | [490023239](https://issues.chromium.org/issues/490023239) |
| **Status** | Fixed |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>CSS |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-03-05 |
| **Bounty** | $2,000.00 |

## Description

### Summary

`CSS.setScopeText` (via [`InspectorCSSAgent::setScopeText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_css_agent.cc;l=3092)) desynchronizes nested `@scope` wrappers: [`CSSScopeRule::SetPreludeText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_scope_rule.cc;l=69) mutates only wrapper-local `group_rule_`, and later index-based reattach calls [`CSSGroupingRule::Reattach`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_grouping_rule.cc;l=363) with a non-group `StyleRule*`, leading to type confusion and the memory corruption.

> NOTE: this is a resubmission of the report 488270255, since the previous issue is repurposed.

### Details

`CSS.setScopeText` edits the prelude of an existing `@scope` rule by calling [`InspectorStyleSheet::SetScopeRuleText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/inspector/inspector_style_sheet.cc;l=1532), which locates the existing `CSSScopeRule` wrapper and invokes `CSSScopeRule::SetPreludeText`.

The key problem is that `CSSScopeRule::SetPreludeText` replaces the wrapper’s internal `group_rule_` pointer with a newly allocated `StyleRuleScope`, but does not replace the corresponding `StyleRuleScope` inside the stylesheet’s rule graph. This means the wrapper becomes detached from the real sheet contents, yet still participates in subsequent CSSOM calls and later `Reattach()` cascades (which assume wrapper/rule index+type stability).

In [`CSSScopeRule::SetPreludeText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_scope_rule.cc;l=69), the mutation ends by assigning a new rule object only to the wrapper field:

```
  HeapVector<Member<StyleRuleBase>> new_child_rules;
  new_child_rules.ReserveInitialCapacity(
      GetStyleRuleScope().ChildRules().size());
  for (StyleRuleBase* child_rule : GetStyleRuleScope().ChildRules()) {
    new_child_rules.push_back(
        child_rule->Clone(new_style_scope->RuleForNesting(),
                          /*mixin_parameter_bindings=*/nullptr));
  }
  group_rule_ = MakeGarbageCollected<StyleRuleScope>(
      *new_style_scope, std::move(new_child_rules));

```

After this, page JS can mutate the stale `CSSScopeRule` wrapper (e.g. `deleteRule()` then `insertRule('@media all {}', 0)`) such that the wrapper’s `child_rule_cssom_wrappers_` at index 0 becomes a `CSSMediaRule`, while the stylesheet-backed `@scope` still has a style rule at index 0.

Later, a parent rule mutation that performs a replacement+reattach (e.g. [`CSSStyleRule::setSelectorText`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_style_rule.cc;l=87)) reattaches nested wrappers by index. During that reattach, the stale scope wrapper forwards `ChildRules()[0]` (a `StyleRule*`) into the `CSSMediaRule` wrapper’s `Reattach()`. `CSSMediaRule` inherits `CSSGroupingRule::Reattach`, which performs an unchecked cast:

In [`CSSGroupingRule::Reattach`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/css_grouping_rule.cc;l=363), the downcast is a `static_cast` without runtime validation:

```
void CSSGroupingRule::Reattach(StyleRuleBase* rule) {
  DCHECK(rule);
  group_rule_ = static_cast<StyleRuleGroup*>(rule);
  for (unsigned i = 0; i < child_rule_cssom_wrappers_.size(); ++i) {
    if (child_rule_cssom_wrappers_[i]) {
      child_rule_cssom_wrappers_[i]->Reattach(
          group_rule_->ChildRules()[i].Get());
    }
  }
}

```

Once the wrapper’s `group_rule_` is miscast to a `StyleRuleGroup*`, subsequent CSSOM operations on that wrapper (notably `insertRule`) can write through the misinterpreted layout, corrupting the real `StyleRule` object fields. A reliable symptom is that later style resolution (RuleSet construction) crashes in `RuleSet::AddStyleRule`/`AddChildRules` while iterating nested rules, consistent with a corrupted `StyleRule::ChildRules()` pointer.

### Bisection

This issue is introduced by the commit: `ed46557e198a8fce6c1ef52b38e5c17734c99ba9` [css-nesting] Implement CSSScopeRule::SetPreludeText by rule replacement.

### Reproduction

Download the chrome from `https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1591355.zip`

Run the chrome with the attached extension:

```
./chrome --load-extension=/path/to/ext --no-sandbox

```

You would observe the ASAN stack trace shown in the `asan.txt`

### Suggested Fix

Harden `CSSGroupingRule::Reattach` against type mismatches by validating `rule` is a `StyleRuleGroup` before assigning it to `group_rule_` (e.g. `DynamicTo<StyleRuleGroup>`).

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 7.7 KB)
- [manifest.json](attachments/manifest.json) (application/json, 272 B)
- [service_worker.js](attachments/service_worker.js) (text/javascript, 8.8 KB)

## Timeline

### he...@gmail.com (2026-03-05)

To security team: Could you please cc [sesse@chromium.org](mailto:sesse@chromium.org) for this report (or set as owner), thank you very much!

### aj...@google.com (2026-03-05)

Adding folks from [issue 488270255](https://issues.chromium.org/issues/488270255) which this spawned from.

### aj...@google.com (2026-03-05)

sev low as this is mitigated by needing a powerful extension permission to trigger the issue.

### ch...@google.com (2026-03-06)

Setting Priority to P3 to match Severity s3. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### se...@chromium.org (2026-03-06)

We partially started working on this issue when the PoC was mistakenly submitted as part of [issue 488270255](https://issues.chromium.org/issues/488270255). In particular, <https://chromium-review.git.corp.google.com/c/chromium/src/+/7627755> is for this issue.

After that CL, the issue still reproduces, but is now a CHECK failure on the cast instead of an actual type confusion bug.

### se...@chromium.org (2026-03-06)

FWIW, in the future: It's usually easier to reproduce these using a devtools test instead of an extension (I suppose it will demonstrate equally that an attacker with high-permission devtools access can trigger the issue). See e.g. third\_party/blink/web\_tests/inspector-protocol/css/css-set-scope-text.js. I suppose this PoC is AI-generated, there's just so much… stuff. :-)

### he...@gmail.com (2026-03-06)

Thanks. Yes the extension POC is transformed by the LLM, although I've manually trimmed a lot already. It indeed contains too much defensive functions and should be minimized further. I'll try to reuse the devtool tests in the future report.

Many thanks!

### se...@chromium.org (2026-03-06)

I adapted it into a devtools test so that we have a regression test in the CL.

### dx...@google.com (2026-03-06)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7641210>

Fix CSSOM wrapper desync on setScopeText().

---


Expand for full commit details
```
     
    If setScopeText() was called on a @scope rule, especially a nested 
    scope rule, we'd only update the CSSOM wrapper, not the actual 
    StyleRule in the style sheet. This could cause type confusion when 
    modifying the StyleRule further. (This was hardened to a CHECK 
    failure in the previous CL related to this bug, changing to To<> 
    instead of static_cast.) 
     
    setScopeText() is only available to devtools (including extensions 
    with devtools permissions). 
     
    Fixed: 490023239 
    Change-Id: I3c64ede444c89144126acb75d854b9ac3b23d0ed 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7641210 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1595323}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_scope_rule.cc`
- A `third_party/blink/web_tests/inspector-protocol/css/css-set-scope-text-reattach-expected.txt`
- A `third_party/blink/web_tests/inspector-protocol/css/css-set-scope-text-reattach.js`

---

Hash: [dff61fda8560b68af87c699fa2ef4345b0ed2cce](https://chromiumdash.appspot.com/commit/dff61fda8560b68af87c699fa2ef4345b0ed2cce)  

Date: Fri Mar 6 12:42:22 2026


---

### ch...@google.com (2026-04-07)

WARNING: Removing security\_release value because the issue is not on security\_impact-stable or security\_impact-extended hotlists. Please add to the correct hotlist if the issue is on a release branch.

### he...@gmail.com (2026-04-22)

friendly ping - is there any updates on the VRP rewards? Thank you very much!

### sp...@google.com (2026-05-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
highly mitigated renderer crash + bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/490023239)*
