# Heap-use-after-free in CSS attribute rule matching via lazy style synchronization

| Field | Value |
|-------|-------|
| **Issue ID** | [492735384](https://issues.chromium.org/issues/492735384) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-03-15 |
| **Bounty** | $11,000.00 |

## Description

# Heap-use-after-free in CSS attribute rule matching via lazy style synchronization

## Summary

A use-after-free read exists in the Blink CSS rule matching engine on all platforms. During author style resolution, `ElementRuleCollector::CollectMatchingRulesInternal` iterates over an element's attributes using a `base::span` that becomes stale when `CollectMatchingRulesForList` triggers lazy synchronization of the `style` attribute. The synchronization appends a new attribute to the element's `UniqueElementData::attribute_vector_`, causing a heap reallocation that frees the buffer the span still references. A subsequent iteration of the inner rule set bundle loop then reads from the freed buffer. The bug is triggerable from web content via pure HTML, CSS, and JavaScript with no user interaction.

## Bisect

Introducing Commit: `88218b47b18ae0d640ea0b6cacf8fdf2cb7b8ae9`

- Date: 2025-01-27
- Author: Steinar H. Gunderson ([sesse@chromium.org](mailto:sesse@chromium.org))
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/6179412>

This commit ("Add property bitmaps to RuleSetGroup") refactored the attribute matching loop to use `RuleSetsWithAttrRules()` and introduced `NeedStyleSynchronized()` as a defense against lazy style attribute reallocation. The defense checks `HasBucketForStyleAttribute()` to decide whether to pre-synchronize, but `ExtractBestBucketingValues` only records the last attribute in a compound selector, so `[style][a]` is bucketed to `a` and bypasses the check entirely.

## Root Cause

`CollectMatchingRulesInternal` captures a `base::span<const Attribute>` over the element's attribute vector at the start of its attribute iteration loop. The code comment acknowledges that `CollectMatchingRulesForList` may cause reallocation and states the span should be refreshed "after every call," but the implementation only refreshes it after the inner bundle loop completes, not after each individual `CollectMatchingRulesForList` call within that loop.

```
// element_rule_collector.cc:913-948
base::span<const Attribute> attributes =
    GetAttributes(element, match_request.NeedStyleSynchronized());

for (unsigned attr_idx = 0; attr_idx < attributes.size(); ++attr_idx) {
  const AtomicString& attribute_name = attributes[attr_idx].LocalName();
  const AtomicString& lower_name = /* ... */ attribute_name;

  for (const auto bundle : match_request.RuleSetsWithAttrRules()) {
    base::span<const RuleData> list =
        bundle.rule_set->AttrRules(lower_name);
    if (list.empty() ||
        bundle.rule_set->CanIgnoreEntireList(
            list, lower_name, attributes[attr_idx].Value())) {
      continue;
    }
    CollectMatchingRulesForList<stop_at_first_match>(
        bundle.rule_set->AttrRules(lower_name), match_request,
        bundle.rule_set, bundle.style_sheet_index, checker, context);
  }
  // Span refresh happens here, AFTER the bundle loop — too late
  const AttributeCollection collection = element.AttributesWithoutUpdate();
  attributes = base::span(collection);
}

```

If the first bundle's `CollectMatchingRulesForList` causes the element's attribute vector to reallocate, the second bundle's access to `attributes[attr_idx].Value()` at the `CanIgnoreEntireList` call reads from the freed old buffer.

The reallocation is triggered through the CSS selector matching path. When `SelectorChecker::AnyAttributeMatches` encounters a `[style]` attribute selector, it calls `element.SynchronizeAttribute(selector_attr.LocalName())` to materialize any lazy attribute before comparing.

```
// selector_checker.cc:1333-1343
static bool AnyAttributeMatches(Element& element,
                                CSSSelector::MatchType match,
                                const CSSSelector& selector) {
  const QualifiedName& selector_attr = selector.Attribute();
  element.SynchronizeAttribute(selector_attr.LocalName());
  // ...

```

If the element has a dirty inline style (set via `element.style.setProperty()`), synchronizing the `style` attribute calls `SynchronizeStyleAttributeInternal`, which calls `SetSynchronizedLazyAttribute`, which calls `AppendAttributeInternal`. This appends a new `Attribute` to the element's `attribute_vector_`.

The reallocation is guaranteed because `UniqueElementData`'s constructor from `ShareableElementData` reserves exactly the number of existing attributes:

```
// element_data.cc:178-192
UniqueElementData::UniqueElementData(const ShareableElementData& other)
    : ElementData(other, true) {
  attribute_vector_.reserve(other.Attributes().size());
  for (auto& attribute : other.AttributesSpan()) {
    attribute_vector_.UncheckedAppend(attribute);
  }
}

```

When `AppendAttributeInternal` adds the style attribute to a full-capacity vector, `Vector::AppendSlowCase` allocates a new buffer, moves the existing attributes, and frees the old buffer. The stale span captured by `CollectMatchingRulesInternal` still points to the old, now-freed buffer.

To actually reach this code path, the attacker must bypass the `NeedStyleSynchronized()` pre-synchronization check. This check tests whether any rule set has rules specifically bucketed to the `style` attribute. If the compound selector is `[style][a]`, `RuleSet::ExtractBestBucketingValues` iterates the sub-selectors and overwrites the bucketing attribute name at each step, producing a final bucket key of `a` rather than `style`. This means `HasBucketForStyleAttribute()` returns false, `NeedStyleSynchronized()` returns false, and the attribute vector is not pre-synchronized before iteration begins.

The element needs at least five non-style attributes so that the `attribute_vector_` exceeds the `Vector<Attribute, 4>` inline capacity of four elements and is heap-allocated. With four or fewer attributes, the vector storage is inline within the `UniqueElementData` object and the old "buffer" is never freed.

Two separate `<style>` elements ensure two distinct rule set bundles in the inner loop, so the second bundle reads from the stale span after the first bundle's `CollectMatchingRulesForList` triggers the reallocation.

## Reproduce

Tested on commit `3ad31ba232d9a804b4de78d788e391f82b40a906` (Windows x64). No source modifications are required.

Build configuration (ASAN release, component build):

```
is_asan = true
is_debug = false
is_component_build = true
dcheck_always_on = false

```

Launch:

```
set ASAN_OPTIONS=detect_odr_violation=0
out\asan-release\chrome.exe --no-sandbox --disable-gpu --user-data-dir=%TEMP%\poc_attruaf poc.html

```

Opening the PoC crashes the renderer with a heap-use-after-free during `getComputedStyle()`.

```
==43424==ERROR: AddressSanitizer: heap-use-after-free on address 0x113708020930 at pc 0x7ffe4cf3c5da bp 0x002118df9680 sp 0x002118df96c8
READ of size 8 at 0x113708020930 thread T0
    #0 in blink::ElementRuleCollector::CollectMatchingRulesInternal<0>() element_rule_collector.cc:950
    #1 in blink::ScopedStyleResolver::CollectMatchingElementScopeRules() scoped_style_resolver.cc:308
    #2 in blink::StyleResolver::MatchAuthorRules() style_resolver.cc:1055
    #3 in blink::StyleResolver::MatchAllRules() style_resolver.cc:1294
    #4 in blink::StyleResolver::ApplyBaseStyleNoCache() style_resolver.cc:1825
    #5 in blink::StyleResolver::ApplyBaseStyle() style_resolver.cc:2074
    #6 in blink::StyleResolver::ResolveStyle() style_resolver.cc:1408
    #7 in blink::Element::OriginalStyleForLayoutObject() element.cc:4905
    #8 in blink::Element::StyleForLayoutObject() element.cc:4847
    #9 in blink::Element::RecalcOwnStyle() element.cc:5433
    ...
    #21 in blink::CSSComputedStyleDeclaration::GetPropertyCSSValue() css_computed_style_declaration.cc:349

0x113708020930 is located 16 bytes inside of 96-byte region [0x113708020920,0x113708020980)
freed by thread T0 here:
    #0 free
    #1 in Vector<Attribute,4,PartitionAllocator>::ReallocateBuffer() vector.h:2606
    #2 in Vector<Attribute,4,PartitionAllocator>::ExpandCapacity() vector.h:2060
    #3 in Vector<Attribute,4,PartitionAllocator>::AppendSlowCase() vector.h:2284
    #4 in blink::Element::AppendAttributeInternal() element.cc:7950
    #5 in blink::Element::SetSynchronizedLazyAttribute() element.cc:13029
    #6 in blink::Element::SynchronizeStyleAttributeInternal() element.cc:11732
    #7 in blink::Element::SynchronizeAttributeHinted() element.cc:12891
    #8 in blink::ElementRuleCollector::CollectMatchingRulesForListInternal<0,0>() element_rule_collector.cc:609
    #9 in blink::ElementRuleCollector::CollectMatchingRulesForList<0>() element_rule_collector.cc:753
    #10 in blink::ElementRuleCollector::CollectMatchingRulesInternal<0>() element_rule_collector.cc:939

previously allocated by thread T0 here:
    #0 malloc
    #1 in partition_alloc::PartitionRoot::Alloc<0>() partition_root.h:532
    #2 in VectorBufferBase<Attribute,PartitionAllocator>::AllocateBufferNoBarrier() vector.h:579
    #3 in Vector<Attribute,4,PartitionAllocator>::ReallocateBuffer() vector.h:2597
    #4 in blink::UniqueElementData::UniqueElementData(const ShareableElementData&) element_data.cc:188
    #5 in blink::ElementData::MakeUniqueCopy() element_data.cc:94
    #6 in blink::Element::CreateUniqueElementData() element.cc:11722
    #7 in blink::Element::EnsureMutableInlineStyle() element.cc:11759
    #8 in blink::AbstractPropertySetCSSStyleDeclaration::SetPropertyInternal() abstract_property_set_css_style_declaration.cc:273
    #9 in blink::AbstractPropertySetCSSStyleDeclaration::setProperty() abstract_property_set_css_style_declaration.cc:155

MiraclePtr Status: NOT PROTECTED
No raw_ptr<T> access to this region was detected prior to this crash.
This crash is still exploitable with MiraclePtr.

```

The complete ASAN log is attached as `asan.log`.

## References

- [element\_rule\_collector.cc — CollectMatchingRulesInternal, span capture and stale refresh](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/element_rule_collector.cc;l=913-948)
- [selector\_checker.cc — AnyAttributeMatches, SynchronizeAttribute call](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/selector_checker.cc;l=1333-1343)
- [element.cc — SynchronizeStyleAttributeInternal, SetSynchronizedLazyAttribute](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/element.cc;l=11726-11735)
- [element.cc — AppendAttributeInternal, vector append](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/element.cc;l=7941-7955)
- [element\_data.cc — UniqueElementData constructor, exact reserve](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/dom/element_data.cc;l=178-192)
- [rule\_set.cc — ExtractBestBucketingValues, last-attribute-wins bucketing](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/rule_set.cc;l=500-542)
- [match\_request.h — NeedStyleSynchronized, HasBucketForStyleAttribute](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/match_request.h;l=138-294)

## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 561 B)
- [asan.log](attachments/asan.log) (text/plain, 18.7 KB)
- [poc.html](attachments/poc_74361469.html) (text/html, 786 B)
- [asan.log](attachments/asan_74361470.log) (text/plain, 11.6 KB)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-03-15)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5083369209528320.

### 24...@project.gserviceaccount.com (2026-03-15)

Testcase 5083369209528320 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5083369209528320.

### je...@gmail.com (2026-03-16)

Hello, I previously only tested on a standalone Windows machine. I have now adjusted the PoC on a Linux machine using the downloaded asan-linux-release-1516264 to trigger ASAN more stably.  

Could you restart ClusterFuzz and use this PoC?

### cl...@appspot.gserviceaccount.com (2026-03-16)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6082345048244224.

### ch...@google.com (2026-03-17)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-03-17)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### se...@chromium.org (2026-03-17)

The writeup is fairly confusing, but I'll have a look.

### 24...@project.gserviceaccount.com (2026-03-17)

Detailed Report: https://clusterfuzz.com/testcase?key=6082345048244224

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ 8
Crash Address: 0x7bbcf6af2c78
Crash State:
  blink::RuleSet::CanIgnoreEntireList
  bool blink::ElementRuleCollector::CollectMatchingRulesInternal<false>
  blink::ScopedStyleResolver::CollectMatchingElementScopeRules
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1002852:1002856

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6082345048244224

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### se...@chromium.org (2026-03-17)

The PoC is also confusing; it mentions the 50-rule limit, but that's typically for the Aho-Corasick logic, which is not mentioned in the bug text…?

### je...@gmail.com (2026-03-17)

Yes, that's because the new PoC is a stable version added later, so there wasn't time to update the text accordingly. I can update it today if you need.

### se...@chromium.org (2026-03-17)

I see, the entire problem is the call to CanIgnoreEntireList() in the first place.

### se...@chromium.org (2026-03-17)

The issue isn't really limited to [style]; any lazy attribute would trigger this. So the PoC's use of [style][a] is probably a bit roundabout, although it demonstrates the issue; however, it means that changing NeedsStyleSynchronized() would not be sufficient.

### dx...@google.com (2026-03-17)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7673597>

Fix a use-after-free with lazy style attributes.

---


Expand for full commit details
```
     
    Running selector checking on an element could add new attributes to it, 
    invalidating the Attribute pointers we are iterating over. We knew this 
    and had code in place for it, but that code was defeated when we added 
    RuleSet bundles; we'd refresh the Attribute span after we'd processed 
    the entire bundle instead of after each RuleSet, and since the 
    Aho-Corasick code wanted to read a value from one of the attributes, 
    we could have use-after-free. 
     
    We also appeared to hold a reference to the name, but it is actually 
    harmless; since ToAsciiLower() returns a value, so does the entire 
    ternary expression and it's just a normal value that's kept alive 
    by C++'s reference extension. 
     
    Style perftest is neutral. 
     
    Fixed: 492735384 
    Change-Id: Ib9b56eedbc8bd89978973717be8543b37584b730 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7673597 
    Reviewed-by: Rune Lillesveen <futhark@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1600463}

```

---

Files:

- M `third_party/blink/renderer/core/css/element_rule_collector.cc`
- A `third_party/blink/web_tests/external/wpt/css/css-values/crashtests/chrome-bug-492735384.html`

---

Hash: [515ce02da3726b98d18d5b25845ced973d8323dc](https://chromiumdash.appspot.com/commit/515ce02da3726b98d18d5b25845ced973d8323dc)  

Date: Tue Mar 17 12:10:44 2026


---

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### aj...@google.com (2026-06-24)

S1 renderer UAF.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High Quality. Renderer RCE / memory corruption in a sandboxed process with bisect.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492735384)*
