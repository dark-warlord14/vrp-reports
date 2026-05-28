# KeyframeEffect constructor leaks UA shadow root.

| Field | Value |
|-------|-------|
| **Issue ID** | [464173573](https://issues.chromium.org/issues/464173573) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Animation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | dr...@gmail.com |
| **Assignee** | ke...@google.com |
| **Created** | 2025-11-28 |
| **Bounty** | $2,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

When a Keyframe is constructed with the `pseudoElement` option, animations are applied to the corresponding pseudo-element, but the `target` property still refers to the originating element:
```
effect = new KeyframeEffect(element, [], {pseudoElement: "::placeholder"});
effect.target == inputElement;
```
But when cloning from another KeframeEffect, the element the animations are applied to is used as the target too:
```
effect = new KeyframeEffect(effect);
effect.target != inputElement;
```.

This element may be a pseudo element or a "styled" pseudo element residing in a target element's shadow tree. The placeholder attribute rendered within an <input> element's shadow tree is a an example of an element that can be animated but should not be accessible.

Attached example observers and logs changes to an input's ::placeholder pseudo element. If the user has an saved address in chrome, hovering over the suggested address will disclose it without confirmation.

Many other internal elements may be accessed this way. They can be identified in blink source by use of the `Element::SetShadowPseudoId` method.

VERSION
Chrome Version: Version 144.0.7533.0 (Developer Build) (64-bit)
Operating System: Linux

REPRODUCTION CASE
Visit chrome://settings/addresses and add an address with at least a street address
Open poc.html in chrome served from an HTTP server.
Click on or tab to the input under the Address header.
Hover over suggested address or press down arrow.
Observe the street address is printed to the output.


CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Brendan Draper

## Attachments

- [poc.html](attachments/poc.html) (text/html, 552 B)

## Timeline

### me...@google.com (2025-11-28)

Thanks for the report.

futhark: Could you please take a look? This looks similar to [bug 41386421](https://issues.chromium.org/issues/41386421). Thanks.

### fu...@chromium.org (2025-11-28)

Repro:

```
<!DOCTYPE html>
<input id="inp" type="text" placeholder="Hello">
<script>
  let effect = new KeyframeEffect(inp, [], {pseudoElement: "::placeholder"});
  effect = new KeyframeEffect(effect);
  alert("UA shadow root? " + effect.target.parentNode);
</script>

```

### dr...@gmail.com (2025-11-28)

https://chromium.googlesource.com/chromium/src.git/+/471ed5d216b0ab35f773f67478cc198101f5bd53
introduces pseudo elements referring to user-agent shadow elements with the `Element::GetStyledPseudoElement` method, which may return elements from within the shadow tree that are not `IsPseudoElement()`.

Earlier,
https://chromium.googlesource.com/chromium/src.git/+/af8c16d9f8422ffbfec26fbbf958b4df9a955786
assumes in the KeyframeEffect constructor that the given element is either the target or a pseudo element of the target.

KeyframeEffect* KeyframeEffect::Create(ScriptState* script_state,
@@ -103,23 +155,63 @@
                                EventDelegate* event_delegate)
     : AnimationEffect(timing, event_delegate),
       effect_target_(target),
+      target_element_(target),
+      target_pseudo_(),
       model_(model),
       sampled_effect_(nullptr),
       priority_(priority) {
   DCHECK(model_);
+
+  // fix target for css animations and transitions
+  if (target && target->IsPseudoElement()) {
+    target_element_ = target->parentElement();
+    DCHECK(!target_element_->IsPseudoElement());
+    target_pseudo_ = target->tagName();
+  }
 }


### ch...@google.com (2025-11-28)

Setting milestone because of s2 severity.

### ch...@google.com (2025-11-28)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-12-12)

Project: chromium/src  

Branch:  main  

Author:  Kevin Ellis [kevers@google.com](mailto:kevers@google.com)  

Link:    <https://chromium-review.googlesource.com/7247696>

Prevent exposing UA shadow-DOM in KeyframeEffect constructor

---


Expand for full commit details
```
     
    Bug: 464173573 
    Change-Id: I241cf3e1d22e95a694590d207018c2503ad65166 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7247696 
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org> 
    Commit-Queue: Kevin Ellis <kevers@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1558126}

```

---

Files:

- M `third_party/blink/renderer/core/animation/keyframe_effect.cc`
- D `third_party/blink/web_tests/external/wpt/web-animations/interfaces/Animatable/animate-expected.txt`
- M `third_party/blink/web_tests/external/wpt/web-animations/interfaces/KeyframeEffect/copy-constructor.html`
- M `third_party/blink/web_tests/external/wpt/web-animations/interfaces/KeyframeEffect/target-expected.txt`

---

Hash: [18889dd338aac93fa4f9b375744ff1688c307a36](https://chromiumdash.appspot.com/commit/18889dd338aac93fa4f9b375744ff1688c307a36)  

Date: Fri Dec 12 17:46:51 2025


---

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
baseline lower impact user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dr...@chromium.org (2026-01-09)

[security triage] Looks like our automation dropped the ball here, but since this is Medium severity we should consider this for a merge to M144. Manually doing the merge request now, and I'll review the fix shortly.

### dr...@chromium.org (2026-01-12)

On a further look, there's nothing to merge here. On the day this was fixed, our automation should have tagged this for a merge to M144 Beta. But today M144 has been cut for Stable and M145 is about to be in Beta. We don't merge Medium severity bugs into Stable, so we'll have to be content with this being fixed in M145.

### ch...@google.com (2026-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/464173573)*
