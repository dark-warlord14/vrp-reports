# Use-After-Free via re-entrant attribute mutation during synchronous speculation-rules error dispatch

| Field | Value |
|-------|-------|
| **Issue ID** | [506347575](https://issues.chromium.org/issues/506347575) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 150.0.7849.0 |
| **Reporter** | pw...@gmail.com |
| **Assignee** | db...@chromium.org |
| **Created** | 2026-04-25 |
| **Bounty** | $1,000.00 |

## Description

---

### Report description

Heap-use-after-free read in `blink::Document::ProcessBaseElement` via re-entrant SpeculationRules error dispatch from `UpdateBaseURL`

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

`Document::ProcessBaseElement()` (`third_party/blink/renderer/core/dom/document.cc`) takes a raw `const AtomicString*` pointing into a `<base>` element's `Vector<Attribute, 4>` heap buffer, then calls `UpdateBaseURL()` whenever the base URL changes. `UpdateBaseURL()` walks every `HTMLScriptElement` in the document and invokes `ScriptLoader::DocumentBaseURLChanged()`, which for `type="speculationrules"` re-parses the original source through `AddSpeculationRuleSet()`; if the source is invalid (e.g., the JSON body `[]`, which is not an object), `AddSpeculationRuleSet()` synchronously dispatches a DOM `error` event on the script element. A page-supplied error listener can call `base.setAttribute(...)` on the very `<base>` whose attributes are being processed; once the attribute count exceeds the vector's heap capacity, the vector reallocates and frees the old buffer. When `ProcessBaseElement()` resumes, it dereferences the now-dangling `target` pointer for `target->Contains('\n')`, `target->Contains('<')`, and `base_target_ = *target`. ASAN reports a heap-use-after-free READ of size 8 inside the freed `Attribute` buffer.

## Affected versions

- Reproduced on **149.0.7802.0** Linux ASAN (`BuildId 239e7248443d7f82`).
- Source reviewed in a Chromium checkout at tag **`149.0.7779.3`**; all `file:line` anchors below are from this tag. The vulnerable code is unchanged between 149.0.7779.3 and the 149.0.7802.0 build used for the crash.

## Root cause

Three preconditions compose into the UAF.

1. **Raw pointer into vector storage is held across a re-entrant JS call.** `Document::ProcessBaseElement()` takes the address of `Attribute::value_` returned by `FastGetAttribute()` (`document.cc:5105-5110`):
   
   ```
   if (!target) {
     const AtomicString& value =
         base->FastGetAttribute(html_names::kTargetAttr);
     if (!value.IsNull())
       target = &value;
   }
   
   ```
   
   `target` is a plain `const AtomicString*` on the C++ stack, pointing inside the heap buffer that backs the `<base>` element's `Vector<Attribute, 4> attribute_vector_` (`AttributeVector` is `Vector<Attribute, 4>`, defined in `third_party/blink/renderer/core/dom/attribute_collection.h`).
2. **`UpdateBaseURL()` synchronously re-enters JavaScript through SpeculationRules.** When `base_element_url` changes (`document.cc:5143-5161`), `ProcessBaseElement` calls `UpdateBaseURL()`, which iterates every `HTMLScriptElement` in the document and calls `ScriptLoader::DocumentBaseURLChanged()` (`document.cc:5015-5018`):
   
   ```
   for (HTMLScriptElement& script :
        Traversal<HTMLScriptElement>::DescendantsOf(*this)) {
     script.Loader()->DocumentBaseURLChanged();
   }
   
   ```
   
   For a `type="speculationrules"` element, `DocumentBaseURLChanged()` re-parses the script's original source (`script_loader.cc:234-244`):
   
   ```
   void ScriptLoader::DocumentBaseURLChanged() {
     if (GetScriptType() != ScriptTypeAtPrepare::kSpeculationRules) return;
     if (SpeculationRuleSet* rule_set = RemoveSpeculationRuleSet()) {
       AddSpeculationRuleSet(rule_set->source());
     }
   }
   
   ```
   
   `AddSpeculationRuleSet()` dispatches the `error` event synchronously on JSON parse failure (`script_loader.cc:1372-1389`):
   
   ```
   speculation_rule_set_ = SpeculationRuleSet::Parse(source, context_window);
   ...
   if (speculation_rule_set_->error_type() ==
           SpeculationRuleSetErrorType::kSourceIsNotJsonObject ||
       ...) {
     element_->DispatchErrorEvent();   // synchronous
     ...
   }
   
   ```
   
   `HTMLScriptElement::DispatchErrorEvent()` runs registered JS error listeners on the script element before returning, while `ProcessBaseElement`'s stack frame is still live above on the stack.
3. **The error listener appends one more attribute and reallocates the vector.** `Vector<Attribute, 4>::ExpandCapacity()` doubles capacity once it leaves the inline 4 (cap progresses 4 -> 8 -> 16 -> ...). With seven attributes already on the element, `setAttribute('href', ...)` from JS appends the eighth, filling the heap buffer of capacity 8 and capturing `target` as a pointer into it. The error listener then calls `base.setAttribute('data-extra0', ...)`, taking the count to 9; `Vector::AppendSlowCase` -> `ExpandCapacity` -> `ReallocateBuffer` allocates a new capacity-16 buffer, copies the `Attribute` objects, and frees the old buffer that `target` still points into.

After `UpdateBaseURL()` returns, `ProcessBaseElement` reads through `target` (`document.cc:5164-5171`):

```
if (target) {
  if (target->contains('\n') || target->contains('\r')) { ... }
  if (target->contains('<')) { ... }
  base_target_ = *target;
}

```

The 8-byte load of `target->impl_` (a `scoped_refptr<StringImpl>`) from the freed region — inlined to `base/memory/scoped_refptr.h:319` — is what ASAN catches.

The `InsertedInto` path also reaches `ProcessBaseElement`, but DOM insertion runs under `ScriptForbiddenScope`, so `DispatchEvent` would CHECK-fail before the UAF; routing the trigger through `setAttribute` from already-running script avoids that scope and keeps the JS dispatch on the synchronous path.

## Primitive

Heap-use-after-free READ of 8 bytes from a freed 128-byte PartitionAlloc slot in the renderer. `target` aliases `&attr[i].value_` at a fixed offset inside that slot, and a same-bucket reuse fills the read with attacker-chosen bytes: the `<base>` element places `target` at attribute slot 6 so that `&attr[6].value_ = freed_base + 104`, and inside the error handler 116-LChar `document.createTextNode()` strings are allocated (StringImpl size = 12-byte header + 116 LChars = 128 B, same BufferPartition bucket; LIFO freelist hands the just-freed slot to the first allocation). Bytes 92..99 of the spray string land at offsets 104..111 of the reclaimed slot, so `target->impl_` loads 8 fully attacker-chosen bytes.

`ProcessBaseElement` then runs `base_target_ = *target` (`document.cc:5171`), which copies the inner `scoped_refptr<StringImpl>` and calls `Retain()` on the new `impl_`. `Retain()` atomically increments `StringImpl::ref_count_` at offset 0 of `*impl_` — a `lock add dword ptr [impl_], 1` at any attacker-chosen 4-byte aligned mapped address.

## Reproduction

Extract the attached `poc.html` and `asan.log` into an empty working directory and `cd` into it. All commands below are run from that directory; every path is relative.

1. Download the 149.0.7802.0 Linux ASAN build using `get_asan_chrome.py` (which ships in the Chromium source tree at `tools/get_asan_chrome/get_asan_chrome.py`) so that `chrome` and `llvm-symbolizer` end up in the working directory:
   
   ```
   python3 get_asan_chrome.py --version 149.0.7802.0 --output-dir .
   
   ```
2. Serve the PoC over loopback HTTP. SpeculationRules requires the page to be loaded over a secure context or a loopback origin; `127.0.0.1` qualifies, while `file://` does not parse the `<script type="speculationrules">` element. In one terminal:
   
   ```
   python3 -m http.server 18046 --bind 127.0.0.1
   
   ```
3. In another terminal, run the ASAN build against the PoC:
   
   ```
   ASAN_OPTIONS=detect_leaks=0:symbolize=1:allocator_may_return_null=1:external_symbolizer_path=./llvm-symbolizer ./chrome --no-sandbox --user-data-dir=./prof --headless=new --no-first-run --disable-breakpad --disable-crash-reporter "http://127.0.0.1:18046/poc.html" 2> asan.log
   
   ```
   
   The attached `asan.log` was captured with this command line.

## Crash evidence

### ASAN

Top of stack from `asan.log`:

```
==6248==ERROR: AddressSanitizer: heap-use-after-free on address 0x6d3d10d63d48
READ of size 8 at 0x6d3d10d63d48 thread T0 (chrome)
    #0 blink::Document::ProcessBaseElement()        third_party/blink/renderer/core/dom/document.cc (via base/memory/scoped_refptr.h:319)
    #1 blink::Element::AttributeChanged(...)        third_party/blink/renderer/core/dom/element.cc:3763
    #3 blink::Element::AppendAttributeInternal(...) third_party/blink/renderer/core/dom/element.cc:11580
    #4 blink::Element::SetAttributeHinted(...)      third_party/blink/renderer/core/dom/element.cc:13306
    #6 v8_element::SetAttributeOperationCallback    gen/.../v8_element.cc:5153

```

Free stack (the realloc fired from inside the error handler):

```
freed by thread T0 (chrome) here:
    #1 blink::Vector<blink::Attribute, 4u, blink::PartitionAllocator>::ReallocateBuffer
                                                       third_party/blink/renderer/platform/wtf/allocator/partition_allocator.h:45
    #3 blink::Vector<...>::AppendSlowCase             third_party/blink/renderer/platform/wtf/vector.h:2297
    #5 blink::Element::AppendAttributeInternal(...)   third_party/blink/renderer/core/dom/element.cc:7988
    ...
    #25 blink::HTMLScriptElement::DispatchErrorEvent() third_party/blink/renderer/core/html/html_script_element.cc:445
    #26 blink::ScriptLoader::AddSpeculationRuleSet     third_party/blink/renderer/core/script/script_loader.cc:1382
    #27 blink::Document::UpdateBaseURL                 third_party/blink/renderer/core/dom/document.cc:5017
    #28 blink::Document::ProcessBaseElement            third_party/blink/renderer/core/dom/document.cc:5160

```

The freed `128-byte region [0x6d3d10d63d40,0x6d3d10d63dc0)` is an `Attribute[8]` array (16 B per entry). The read at +8 hits `Attribute[0].value_`. `MiraclePtr Status: NOT PROTECTED` and `--type=renderer` in `ADDITIONAL INFO` confirm a renderer-side raw-pointer dereference.

### Release Build

`poc_release_4141.html` places `target` at slot 6 and sprays 116-LChar TextNode strings such that `chars[92..97] = 0x41 * 6` and `chars[98..99] = 0x00 * 2`, packing the 8 bytes at slot offset +104 into the canonical pointer `0x0000414141414141`. Run against the 149.0.7802.0 Chrome for Testing release build (`https://storage.googleapis.com/chrome-for-testing-public/149.0.7802.0/linux64/chrome-linux64.zip`) with the same flag set as the ASAN command above (drop `ASAN_OPTIONS` / `external_symbolizer_path` and point at `poc_release_4141.html`). Captured in `release_crash_4141.log`:

```
Received signal 11 SEGV_MAPERR 414141414149
 r12: 00000d0c00344ac0 r13: 00006133cacb9b98 r14: 00006133ca7325d0 r15: 0000414141414141
 trp: 000000000000000e msk: 0000000000000000 cr2: 0000414141414149

```

`r15 = 0x0000414141414141` is the 8-byte spray pattern loaded into `target->impl_`. `cr2 = 0x0000414141414149` is `impl_ + 8` — the first field read inside `target->contains('\n')` (the StringImpl header at offset +8) — confirming the dereference uses the attacker-chosen pointer. `trp = 0x0e` is `#PF` and `SEGV_MAPERR` says the page is unmapped. On a mapped `impl_`, the StringImpl reads succeed and `base_target_ = *target` reaches `scoped_refptr<StringImpl>::Retain()`, which issues `lock add dword ptr [impl_], 1` at the attacker-chosen address.

## Bisect

- **Commit**: `a354fb49e4c649b4726c7f07ae2f26296c93b486`
- **Subject**: `Fire error events for invalid speculation rules`
- **Date**: 2025-07-18
- **Gerrit CL**: <https://chromium-review.googlesource.com/c/chromium/src/+/6758353>

This commit added the synchronous `element_->DispatchErrorEvent()` call inside `ScriptLoader::AddSpeculationRuleSet()` for `kSourceIsNotJsonObject`:

```
+++ b/third_party/blink/renderer/core/script/script_loader.cc
@@ ScriptLoader::AddSpeculationRuleSet @@
   speculation_rule_set_ = SpeculationRuleSet::Parse(source, context_window);
   CHECK(speculation_rule_set_);
+
+  if (speculation_rule_set_->error_type() ==
+      SpeculationRuleSetErrorType::kSourceIsNotJsonObject) {
+    // For a JSON parse error, we fire an error event on the element, and
+    // then report an exception which will bubble to the window.
+    element_->DispatchErrorEvent();
+
+    ScriptState* script_state =
+        ToScriptStateForMainWorld(context_window->GetFrame());
+    ScriptState::Scope scope(script_state);
+    v8::Local<v8::Value> error = v8::Exception::TypeError(V8String(
+        script_state->GetIsolate(), speculation_rule_set_->error_message()));
+    V8ScriptRunner::ReportException(script_state->GetIsolate(), error);
+  }
+
   DocumentSpeculationRules::From(element_document)
       .AddRuleSet(speculation_rule_set_);

```

Before this commit, `AddSpeculationRuleSet()` returned without running script even on parse failure. The path from `Document::UpdateBaseURL()` into `ScriptLoader::DocumentBaseURLChanged()` and then `AddSpeculationRuleSet()` was already wired up at this point (<https://chromium-review.googlesource.com/c/chromium/src/+/5738414>), and the raw `target` pointer pattern in `ProcessBaseElement()` predates both, so the addition of the synchronous `DispatchErrorEvent()` is what makes the re-entrant UAF reachable for an inline `<script type="speculationrules">[]</script>`. A same-day companion commit `8a2757c24d78451ae3326ba975477ae7b0a13074` (<https://chromium-review.googlesource.com/c/chromium/src/+/6746174>) extends the same condition with `kInvalidRulesetLevelTag`, but the PoC trips the `kSourceIsNotJsonObject` path landed by `a354fb49`.

Verified bad: 149.0.7802.0 (crash captured, `asan.log`).

## Suggested patch

Hold a value copy of the target attribute across `UpdateBaseURL()` so the read after re-entry no longer aliases vector storage:

```
--- a/third_party/blink/renderer/core/dom/document.cc
+++ b/third_party/blink/renderer/core/dom/document.cc
@@ -5093,18 +5093,18 @@ void Document::ProcessBaseElement() {
   // Find the first href attribute in a base element and the first target
   // attribute in a base element.
   const AtomicString* href = nullptr;
-  const AtomicString* target = nullptr;
+  AtomicString target;
   for (HTMLBaseElement* base = Traversal<HTMLBaseElement>::FirstWithin(*this);
-       base && (!href || !target);
+       base && (!href || target.IsNull());
        base = Traversal<HTMLBaseElement>::Next(*base)) {
     if (!href) {
       const AtomicString& value = base->FastGetAttribute(html_names::kHrefAttr);
       if (!value.IsNull())
         href = &value;
     }
-    if (!target) {
+    if (target.IsNull()) {
       const AtomicString& value =
           base->FastGetAttribute(html_names::kTargetAttr);
       if (!value.IsNull())
-        target = &value;
+        target = value;
     }
@@ -5161,14 +5161,14 @@ void Document::ProcessBaseElement() {
   }

   AtomicString old_base_target = base_target_;
-  if (target) {
-    if (target->contains('\n') || target->contains('\r')) {
+  if (!target.IsNull()) {
+    if (target.contains('\n') || target.contains('\r')) {
       UseCounter::Count(*this, WebFeature::kBaseWithNewlinesInTarget);
     }
-    if (target->contains('<')) {
+    if (target.contains('<')) {
       UseCounter::Count(*this, WebFeature::kBaseWithOpenBracketInTarget);
     }
-    base_target_ = *target;
+    base_target_ = target;
   } else {
     base_target_ = g_null_atom;
   }

```

`AtomicString` owns a `scoped_refptr<StringImpl>`, so assigning by value increments the refcount and keeps the string data alive regardless of any subsequent reallocation of the source `<base>` element's attribute vector during `UpdateBaseURL()`. `href` is only read before `UpdateBaseURL()` and does not need the same treatment.

## Security impact

Heap-use-after-free in the renderer; the release demo faults with `cr2 = 0x0000414141414149` (`impl_ + 8` from the controlled spray value `r15 = 0x0000414141414141`), confirming the 8 bytes loaded into `target->impl_` are attacker-controlled. With `impl_` pointed at any mapped 4-byte aligned address the subsequent `base_target_ = *target` issues an atomic 4-byte increment at that address through `scoped_refptr<StringImpl>::Retain()`. The trigger is a single page visit carrying `<script type="speculationrules">[]</script>` and a `<base>` `href` mutation.

#### Impact analysis

Heap-use-after-free in the renderer; the release demo faults with `cr2 = 0x0000414141414149` (`impl_ + 8` from the controlled spray value `r15 = 0x0000414141414141`), confirming the 8 bytes loaded into `target->impl_` are attacker-controlled. With `impl_` pointed at any mapped 4-byte aligned address the subsequent `base_target_ = *target` issues an atomic 4-byte increment at that address through `scoped_refptr<StringImpl>::Retain()`. The trigger is a single page visit carrying `<script type="speculationrules">[]</script>` and a `<base>` `href` mutation.

---

### The cause

#### What version of Chrome have you found the security issue in?

149.0.7802.0 dev

#### Is the security issue related to a crash?

Yes, it is related to a crash.

#### Choose the type of vulnerability

Memory Corruption (in a sandboxed process)

#### How would you like to be publicly acknowledged for your report?

Wongi Lee (@\_qwerty\_po) of Theori, Jungwoo Lee (@physicube). with Xint Code

## Attachments

- [poc_release_4141.html](attachments/poc_release_4141.html) (text/html, 1005 B)
- [poc.html](attachments/poc.html) (text/html, 718 B)
- [asan.log](attachments/asan.log) (application/octet-stream, 21.3 KB)
- [release_crash_4141.log](attachments/release_crash_4141.log) (application/octet-stream, 5.3 KB)

## Timeline

### ke...@chromium.org (2026-04-28)

Thanks for the report.

nhiroki@, can you PTAL?

### ch...@google.com (2026-04-29)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2026-04-29)

Setting Priority to P1 to match Severity s1. To ensure SLOs are tracked correctly, priority must match or exceed severity.

### nh...@chromium.org (2026-05-27)

Sorry for the late action. The problem seems to be already fixed on [issue 515155946](https://issues.chromium.org/issues/515155946).

### qw...@gmail.com (2026-05-27)

Looking at the issue number alone, it seems like the upper report should indeed be a duplicate.

Therefore, could you say the reason our report was judged as a duplicate? Since we don't have access to the referenced issue, we're unable to check whether there was a prior report or check the reproducibility on our end.

We'd really appreciate it if you could share the reason.
Thank you!

### ch...@google.com (2026-09-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/506347575)*
