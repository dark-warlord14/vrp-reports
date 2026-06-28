# Type confusion in CSSRepeatValue via IsValueList() range check leads to renderer crash

| Field | Value |
|-------|-------|
| **Issue ID** | [492735383](https://issues.chromium.org/issues/492735383) |
| **Status** | Verified |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | je...@gmail.com |
| **Assignee** | sa...@microsoft.com |
| **Created** | 2026-03-15 |
| **Bounty** | $11,000.00 |

## Description

# Type confusion in CSSRepeatValue via IsValueList() range check leads to renderer crash

## Summary

A type confusion in the CSS value type dispatch system causes `CSSRepeatValue` to be misidentified as `CSSValueList`. When a gap decoration property using `repeat()` syntax is set as an inline style and the element is moved to a document with a different base URL, the engine attempts to iterate the internal memory of a `CSSRepeatValue` object as though it were a `CSSValueList`, dereferencing a garbage pointer and crashing the renderer. The bug requires the experimental `CSSGapDecoration` feature to be enabled and affects all platforms.

## Bisect

Introducing Commit: `ada052a6d2d4c0f1b70e0a57c583c24d6b5a2833`

- Date: 2024-10-04
- Author: Sam Davis Omekara Jr
- Review: <https://chromium-review.googlesource.com/c/chromium/src/+/5856542>

## Root Cause

The `CSSValue` class uses a `ClassType` enum and a range check to identify value list types. `IsValueList()` returns true for any `class_type_` at or above `kValueListClass`:

```
// third_party/blink/renderer/core/css/css_value.h:59
bool IsValueList() const { return class_type_ >= kValueListClass; }

```

All subclasses that actually inherit from `CSSValueList` (such as `CSSFunctionValue`, `CSSImageSetValue`, `CSSGridAutoRepeatValue`) have their enum entries placed after `kValueListClass` in the `ClassType` enum. The comment in the enum explicitly warns against placing non-list types in this range:

```
// third_party/blink/renderer/core/css/css_value.h:376-385
// List class types must appear after ValueListClass.
kValueListClass,
kFunctionClass,
kImageSetClass,
kGridLineNamesClass,
kGridAutoRepeatClass,
kGridIntegerRepeatClass,
kAxisClass,
kRepeatClass,
// Do not append non-list class types here.

```

The `kRepeatClass` entry was added at the end of this range as part of the CSS Gap Decorations feature. The problem is that `CSSRepeatValue` does not inherit from `CSSValueList`; it inherits directly from `CSSValue`:

```
// third_party/blink/renderer/core/css/css_repeat_value.h:21-42
class CSSRepeatValue : public CSSValue {
 public:
  explicit CSSRepeatValue(const CSSPrimitiveValue* repetitions,
                          const CSSValueList& values)
      : CSSValue(kRepeatClass), repetitions_(repetitions), values_(&values) {}
  // ...
 private:
  Member<const CSSPrimitiveValue> repetitions_;
  Member<const CSSValueList> values_;
};

```

Because `kRepeatClass` is numerically greater than or equal to `kValueListClass`, `IsValueList()` returns true for `CSSRepeatValue` objects. This poisons every code path that dispatches through `IsValueList()`, including `DowncastTraits<CSSValueList>`:

```
template <> struct DowncastTraits<CSSValueList> {
  static bool AllowFrom(const CSSValue& value) { return value.IsValueList(); }
};

```

The most direct crash path runs through `CSSValue::MayContainUrl()`:

```
// third_party/blink/renderer/core/css/css_value.cc:157-161
bool CSSValue::MayContainUrl() const {
  if (IsValueList()) {
    return To<CSSValueList>(*this).MayContainUrl();
  }
  return IsImageValue() || IsURIValue();
}

```

When called on a `CSSRepeatValue`, the `IsValueList()` guard passes, and `To<CSSValueList>(*this)` reinterprets the object as a `CSSValueList`. The `CSSValueList` class stores its children in a `HeapVector<Member<const CSSValue>, 4> values_`, which occupies substantially more space and sits at a different offset than the two `Member<>` fields in `CSSRepeatValue`. When `CSSValueList::MayContainUrl()` attempts to iterate this phantom vector, it reads `repetitions_` (a compressed pointer to a `CSSPrimitiveValue`) as the vector's internal buffer pointer. Dereferencing this fabricated address produces the observed SEGV.

```
// third_party/blink/renderer/core/css/css_value_list.cc:208-214
bool CSSValueList::MayContainUrl() const {
  for (const auto& value : values_) {  // <-- iterates with corrupted layout
    if (value->MayContainUrl()) {
      return true;
    }
  }
  return false;
}

```

This `MayContainUrl()` call is reachable from JavaScript through the cross-document adoption path. When an element with an inline style containing a gap decoration `repeat()` value is moved to a document with a different base URL, `Element::DidMoveToNewDocument()` calls `NeedsURLResolutionForInlineStyle()`, which iterates over all inline style property values calling `MayContainUrl()` on each:

```
// third_party/blink/renderer/core/dom/element.cc:11427-11445
static bool NeedsURLResolutionForInlineStyle(const Element& element,
                                             const Document& old_document,
                                             const Document& new_document) {
  if (old_document == new_document) { return false; }
  if (old_document.BaseURL() == new_document.BaseURL()) { return false; }
  const CSSPropertyValueSet* style = element.InlineStyle();
  if (!style) { return false; }
  for (const CSSPropertyValue& property : style->Properties()) {
    if (property.Value().MayContainUrl()) { return true; }
  }
  return false;
}

```

The top-level property value for a parsed gap decoration property like `column-rule-color: repeat(2, red)` is a `CSSValueList` that contains a `CSSRepeatValue` child. When the iteration reaches this child and calls `MayContainUrl()` on it, the type confusion triggers.

The same root cause also affects `CSSValue::HasFailedOrCanceledSubresources()` and `CSSValue::ReResolveUrl()`, both of which dispatch through `IsValueList()` with the same pattern.

## Reproduce

Tested on commit `7c89d33808e551aed6122c1f324864784011c158`.

Build configuration:

```
is_asan = true
is_debug = false
dcheck_always_on = false
target_cpu = "x64"
is_component_build = true

```
```
ASAN_OPTIONS=detect_odr_violation=0 \
~/chromium/src/out/asan-release/chrome \
  --no-sandbox --disable-gpu \
  --enable-blink-features=CSSGapDecoration \
  --user-data-dir=/tmp/poc-$(date +%s) \
  poc.html

```

The renderer process crashes immediately with SEGV at address 0x9007995f.

```
Received signal 11 SEGV_ACCERR 00009007995f
#0  chrome (base::debug::CollectStackTrace)
#1  libbase.so (base::debug::StackTrace::StackTrace)
#2  libbase.so (base::(anonymous namespace)::StackDumpSignalHandler)
#3  libbase.so (base::(anonymous namespace)::StackDumpSignalHandler)
#4  libc.so.6
#5  libblink_core.so (blink::CSSValueList::MayContainUrl) member-storage.h:92
#6  libblink_core.so (blink::CSSValueList::MayContainUrl) css_value_list.cc:210
#7  libblink_core.so (blink::NeedsURLResolutionForInlineStyle) element.cc:11441
#8  libblink_core.so (blink::Element::DidMoveToNewDocument) element.cc:11493
#9  libblink_core.so (blink::TreeScopeAdopter::MoveNodeToNewDocument) tree_scope_adopter.cc:300
#10 libblink_core.so (blink::TreeScopeAdopter::MoveTreeToNewScope) tree_scope_adopter.cc:71
#11 libblink_core.so (blink::TreeScopeAdopter::Execute) tree_scope_adopter.cc:45
#12 libblink_core.so (blink::TreeScope::AdoptIfNeeded) tree_scope.cc:602
#13 libblink_core.so (blink::ContainerNode::InsertNodeVector<AdoptAndAppendChild>) container_node.cc:438
#14 libblink_core.so (blink::ContainerNode::AppendChild) container_node.cc:1206
#15 libblink_core.so (blink::v8_node::AppendChildOperationCallbackForMainWorld) v8_node.cc:523

Registers:
  di: 000000008040cafe  si: 00000f64c19edcba  bp: 00007fff58220830
  dx: 00007b260cf6e5d0  ax: 000000001008195f  cx: 00000f628040cb03
  ip: 00007f2639331ecb  cr2: 000000009007995f

```
## Credit

Please use c6eed09fc8b174b0f3eebedcceb1e792 as the credit for this vulnerability. Thank you.

## Attachments

- [poc.html](attachments/poc.html) (text/html, 476 B)
- [asan.log](attachments/asan.log) (text/plain, 1.4 KB)

## Timeline

### ke...@chromium.org (2026-03-18)

Thanks for the report. I have confirmed the crash. This is Security\_Impact-None because `CSSGapDecoration` is an experimental flag.

Assigning to the author of that change.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Sam Davis Omekara [samomekarajr@microsoft.com](mailto:samomekarajr@microsoft.com)  

Link:    <https://chromium-review.googlesource.com/7681482>

[GapDecorations]: Fix CSSRepeatValue misclassified as CSSValueList

---


Expand for full commit details
```
     
    `CSSValue::IsValueList()` is implemented as a range check (class_type_ 
    >= kValueListClass) and assumes that only `CSSValueList` subclasses 
    occupy that enum range. `kRepeatClass` was placed in the list-class 
    section with `CSSRepeatValue` inherits directly from CSSValue, not 
    CSSValueList. As a result, `CSSRepeatValue` can be downcast via 
    To<CSSValueList> and interpreted to be the wrong object, causing type 
    confusion and a potential renderer crash (security risk). 
     
    This CL moves `kRepeatClass` out of the `CSSValueList` enum range, 
    allowing the list-class enum values correspond to actual `CSSValueList` 
    subclasses and preventing `CSSRepeatValue` from flowing through 
    list-only paths. 
     
    Bug: 492735383 
    Change-Id: I61aa45e70de0370128b99731cd041910d4aca085 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7681482 
    Reviewed-by: Kevin Babbitt <kbabbitt@microsoft.com> 
    Commit-Queue: Sam Davis Omekara <samomekarajr@microsoft.com> 
    Cr-Commit-Position: refs/heads/main@{#1602120}

```

---

Files:

- M `third_party/blink/renderer/core/css/css_value.h`
- A `third_party/blink/web_tests/fast/css-grid-layout/crash-css-repeat-value-type-confusion-via-is-value-list.html`

---

Hash: [b8ae1457c9902f05904f0880193342a95e3385c5](https://chromiumdash.appspot.com/commit/b8ae1457c9902f05904f0880193342a95e3385c5)  

Date: Thu Mar 19 18:23:40 2026


---

### sa...@microsoft.com (2026-03-20)

I think this is fixed per the CL above

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High Quality Bisect. Memory Corruption / RCE in a sandboxed process.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/492735383)*
