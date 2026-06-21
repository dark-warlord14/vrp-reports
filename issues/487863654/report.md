# One click Chrome Sanitizer API bypass via xlink:href:x

| Field | Value |
|-------|-------|
| **Issue ID** | [487863654](https://issues.chromium.org/issues/487863654) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>SanitizerAPI |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ne...@akorlith.com |
| **Assignee** | vo...@chromium.org |
| **Created** | 2026-02-26 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

One click Chrome Sanitizer API bypass via xlink:href:x

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/sanitizer/sanitizer.cc>

---

### The problem

#### Please describe the technical details of the vulnerability

One vector for XSS is setting the `xlink:href` attribute via the `<set attributeName="xlink:href">` tag inside an SVG. Chrome combats this inside the sanitizer API as follows:

```
void RemoveAttributeIfValueIsHref(Element* element,
                                  const QualifiedName& attribute) {
  const AtomicString& value = element->getAttribute(attribute);
  if (value == "href" or value == "xlink:href") {
    element->removeAttribute(attribute);
  }
}

```

However, this is not sufficient. For some reason, Chrome interprets the attribute name `xlink:href:x` the same as `xlink:href`, leading to a bypass of the Sanitizer API.

To reproduce, simply open the attached file or paste the following HTML into the Sanitizier sandbox at <https://sanitizer-api.dev/> with a permissive config:

```
<svg viewBox="0 0 240 80" xmlns:xlink="http://www.w3.org/1999/xlink"><a id="foo"><text x="20" y="20">click me</text></a><set href="#foo" attributeName="xlink:href:x" to="javascript:alert()"></set></svg>

```

Then click the text that says `click me`.

The Sanitizer API is available by default in Chrome 146 which is shipping soon on desktop and has already shipped for some users. If you are on Chrome 145 or below, you will need to enable experimental web platform features in chrome://flags .

#### Impact analysis

This is a one click XSS bypass for the Sanitizer API in its permissive config (`new Sanitizer({})`), rendering `setHTML` dangerous under these circumstances. This violates the API's promise that all scripts are removed.

---

### The cause

#### What version of Chrome have you found the security issue in?

145.0.7632.117 (with experimental web features enabled) or 146.x beta

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Other

#### How would you like to be publicly acknowledged for your report?

hashkitten

## Attachments

- [poc_sanitizer.html](attachments/poc_sanitizer.html) (text/html, 391 B)
- [poc_sanitizer.html](attachments/poc_sanitizer_73766353.html) (text/html, 391 B)

## Timeline

### li...@chromium.org (2026-02-26)

@vo...@chromium.org do you mind taking a look at this or rerouting as necessary?

### vo...@google.com (2026-02-27)

Thank you for the report!

This repros on current beta. It's indeed a security issue, as it violates Sanitizer's anti-XSS guarantee.

### vo...@google.com (2026-02-27)

The Sanitizer part is, technically, compliant with the spec, which prescribes a string compare (after whitespace normalization). The surprising part IMHO is that an `<svg:set attributeName="xlink:href:x" ...>` parses as xlink:href and modifies the element. So there's a mismatch between what the Sanitizer checks for, and what SVG will later accept as valid values.

Preliminary root cause:

- SVGSetElement derives from SVGAnimateElement
- SVGAnimateElement::ParseAttribute for kAttributeNameAttr calls ConstructQualifiedName to obtain a QName
- ConstructQualifedName calls Document::ParseQualifiedName
  - This will return AnyQName if an error occurs. I'd have expected "xlink:href:x" to be an error.
- Document::ParseQualifiedName visits each character with ParseQualifiedNameInternal.
  - Interestingly, the code afterword expressedly checked for kQNMultipleColons error code, which
    sounds a lot like what should happen here.
  - Even more interestingly, ParseQualifiedNameInternal, will check for a second colon, but never
    returns that error code. It only uses it to delimit parsing of the local name.
  - In fact, the check is the sole use of kQNMultipleColons I can find in the code. It's never set
    anywhere.

It seems the root cause is that ParseQualifiedNameInternal is expected to return kQNMultipleColons for "xlink:href:x", but doesn't.

This "smells" a lot like a refactoring, where a check may have been dropped from the code.

### vo...@google.com (2026-02-27)

- <https://chromium-review.git.corp.google.com/c/chromium/src/+/6700961>
  - modifies ParseQualifiedNameInternal and adds logic to check for a second colon.
  - But kQNMultipleColons wasn't raised before or after.
- <https://chromium-review.git.corp.google.com/c/chromium/src/+/4251683>
  - adds ParseQualifiedNameInternalNewSpec, adding to a previous ParseQualifiedNameInternal
  - ParseQualifiedNameInternalNewSpec is the current ParseQualifiedNameInternal.
  - The old ParseQualifiedNameInternal would return kQNMultipleColons when a second colon was found.

It seems 4251683 dropped the colon check.

Both CLs look quite deliberate, and aim to improve standards compliance. I'll have to check whether the colon situation was intentional.

### vo...@google.com (2026-02-27)

On second thought, maybe "xlink:href:x" is valid? In curent DOM and HTML specs, I can't find any rule that says local names cannot contain one or several colons. (E.g. <https://html.spec.whatwg.org/#attributes-2> seem to allow colons in arbitrary quantity. `:::::` would be valid attribute name?) But in that case, surely it shouldn't be parsed as "xlink:href" ?

It seems that second CL, <https://chromium-review.git.corp.google.com/c/chromium/src/+/6700961> + <https://github.com/whatwg/dom/issues/1387> where about that issue. That CL -- as I read it -- discard anything from the second colon onwards, leading to the behaviour observed in this bug.

### vo...@google.com (2026-02-27)

First fix attempt is to just re-establish the colon check. That triggers setAttributeNS-namespace-err.html failures. That test suggests multiple colons are indeed allowed.

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/web_tests/fast/dom/Element/setAttributeNS-namespace-err.html;l=69?q=setAttributeNS-namespace-err.html>

### vo...@google.com (2026-02-27)

Second fix attempt is to just ask SVGAnimateElement to parse the attribute name for us. This should ensure that we're always in sync with SVG animation logic.

### fs...@opera.com (2026-02-27)

Relying on `ConstructQualifiedName()` could have issues if the context of the element changes, because the resolution of the prefix depends on context (what defines the prefix). I'd suggest just parsing the attribute into `<prefix, localname>` (using the `ParseQualifiedName()` - or a non-throwing derivation) and then just do essentially `localname == "href"` - that should avoid the context dependency and achieve the same thing (and from the perspective of SMIL/SVG it should make no difference).

### vo...@google.com (2026-02-27)

Fix: <https://chromium-review.git.corp.google.com/c/chromium/src/+/7617147> Now follows [#comment9](https://issues.chromium.org/issues/487863654#comment9).

### vo...@google.com (2026-02-27)

Current solution is to parse the value using Document::ParseQualifiedName and to check against the result.

It's still baffling to me that `attributeName="xlink:href:x"` gets parsed as "xlink:href". If that is spec conforming, we'd also need to update the Sanitizer spec. If it's not spec conforming, then I think we need to fix that, too.

From a security perspective, the current fix should be good enough.

### vo...@google.com (2026-02-27)

After some back-and-forth, this does look like a spec issue.

DOM says: <https://dom.spec.whatwg.org/#validate-and-extract:~:text=If%20qualifiedName%20contains,splitResult%5B1%5D>

"Validate and extract", step 4.3, indeed reads like anything after the second colon would be dropped from the name. Thus, a string comparison (<https://wicg.github.io/sanitizer-api/#sanitize-core>, step 1.5.9.5.3) is insufficient.

### vo...@google.com (2026-02-27)

Plan is to:

1. Land <https://chromium-review.git.corp.google.com/c/chromium/src/+/7617147> & back-merge.
2. Then try to fix the spec.
3. Update the implementation to whatever the spec decides, if necessary.

### dx...@google.com (2026-02-28)

Project: chromium/src  

Branch:  main  

Author:  Daniel Vogelheim [vogelheim@chromium.org](mailto:vogelheim@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7617147>

[Sanitizer] Check for SVG animate targets by parsing the QName.

---


Expand for full commit details
```
     
    To check whether an <svg:set> (& other animate elements) targets a 
    href/xlink:href attribute, we presently use a string comparison. 
    That is what the spec says. This may fail, because the actual 
    interpretation of that value is more complex. Instead, we properly 
    parse the attribute name, just like SVGAnimateElement::ConstructQualifiedName does. 
     
    Bug: 487863654 
    Change-Id: Ib263b10493952775a8efa7dc66191f9bc90a0920 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7617147 
    Commit-Queue: Daniel Vogelheim <vogelheim@chromium.org> 
    Reviewed-by: Joey Arhar <jarhar@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1592033}

```

---

Files:

- M `third_party/blink/renderer/core/sanitizer/build.gni`
- M `third_party/blink/renderer/core/sanitizer/sanitizer.cc`
- M `third_party/blink/renderer/core/sanitizer/sanitizer.h`
- A `third_party/blink/renderer/core/sanitizer/sanitizer_unittest.cc`

---

Hash: [99dfc1af6343a7e33446157fcaf463a714097f48](https://chromiumdash.appspot.com/commit/99dfc1af6343a7e33446157fcaf463a714097f48)  

Date: Sat Feb 28 16:16:43 2026


---

### vo...@google.com (2026-03-02)

Analysis:

- [Spec says](https://dom.spec.whatwg.org/#validate-and-extract:~:text=If%20qualifiedName%20contains,splitResult%5B1%5D):
  - Let splitResult be the result of running strictly split given qualifiedName and U+003A (:).
  - Set prefix to splitResult[0].
  - Set localName to splitResult[1].
- This means, "xlink:href:x" is parsed as prefix: "xlink", localName: "href". The ":x" suffix gets dropped.
- [SVG Animations](https://svgwg.org/specs/animations/#SetElement) isn't particularly precise at all about what `attributeName=` means. But interpreting it the same as DOM `setAttributeNS` strikes me as very reasonable.
- Thus, `attributeName="xlink:href:x"` animating the `xlink:href` attribute seems surprising, but aligned with the specs.
- Thus, the [Sanitizer test for string equality](https://wicg.github.io/sanitizer-api/#sanitize-core) is insufficient.

I'll raise this in the spec meeting.

[The fix](https://chromium-review.googlesource.com/7617147) uses `Document::ParseQualifiedName` to parse the attribute, and then blocks the localName "href", regardless of prefix. Not sure if that'll hold up in the spec discussions, but it won't be hard to adapt.

### vo...@google.com (2026-03-02)

I'm unsure about severity and backmerge. (Severity guidlines)[https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md] list "universal XSS" as S1; but have no other XSS-related examples.

For this bug: If a page uses `.setHTML` with a non-default configuration that allows SVG, then this is a pretty much complete bypass of the `.setHTML` guarantees and an easy XSS. It does, however, require the page to use `.setHTML` / Sanitizer with a non-default config that allows `<svg:set>`. To me, that clearly isn't "universal", and thus not S1. Based on the guidelines, "Bugs that would normally be rated at a higher severity level with unusual mitigating factors may be rated as medium severity." => S2.

### ch...@google.com (2026-03-02)

Merge review required: M146 has already been cut for stable release.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), None (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### vo...@google.com (2026-03-02)

> 1 Why does your merge fit within the merge criteria for these milestones?

I'm a little unsure, honestly, but per [#comment16](https://issues.chromium.org/issues/487863654#comment16): If a page uses the new `.SetHTML` method with a configuration that allows `<svg:set>`, then this bug provides for a complete bypass and XSS. Using that method with a custom configuration is very much an allowed and expected usage. Because it does require a particular usage I don't think it counts as "universal XSS" (and thus S1); so I picked S2.

> What changes specifically would you like to merge? Please link to Gerrit.

<https://chromium-review.git.corp.google.com/c/chromium/src/+/7617147>

> Have the changes been released and tested on canary?

Per Chromium dash, the change has made it into 147.0.7712.0

> Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

This is part of the "Sanitizer API" feature, behind the SanitizerAPI Finch flag. It's been default-enabled since M146.

### dr...@chromium.org (2026-03-03)

Thanks! Based on the severity here, I don't think we need to merge this.

### vo...@google.com (2026-03-04)

[#comment19](https://issues.chromium.org/issues/487863654#comment19): Thanks, makes sense.

---

This has now been raised on the revelant spec(s). It seems this is moving towards changing the DOM/SVG behaviour.

- <https://github.com/WICG/sanitizer-api/issues/373>
- <https://github.com/whatwg/dom/issues/1453>

### ch...@google.com (2026-06-09)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Exploit mitigation bypass.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/487863654)*
