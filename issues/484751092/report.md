# Heap-buffer-overflow in StyleCascade::ConsumeVariableName

| Field | Value |
|-------|-------|
| **Issue ID** | [484751092](https://issues.chromium.org/issues/484751092) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-02-16 |
| **Bounty** | $11,000.00 |

## Description

### Summary

`StyleCascade` resolves `env()`/`attr()` substitutions by reading the function’s first argument as an ident via [`ConsumeVariableName`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=84), but it only `DCHECK`s the token type and then calls `CSSParserToken::Value()`. In release builds, CSS Typed OM can inject syntactically-invalid `env(0)` into an `unparsed` declaration (via `attributeStyleMap.set()`), so the resolver ends up calling `Value()` on a non-string-backed token (e.g. `kNumberToken`), producing a `StringView` with uninitialized pointer/length and cause OOB in `ToAtomicString()`.

### Details

During variable/substitution resolution, [`StyleCascade::ResolveTokensInto`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=1604) detects `env()` and calls [`StyleCascade::ResolveEnvInto`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=2258), which consumes the environment variable name using `ConsumeVariableName`.

The key issue is that `ConsumeVariableName` relies on a debug-only type assertion before calling `Value()`:

[`ConsumeVariableName`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=84):

```
AtomicString ConsumeVariableName(CSSParserTokenStream& stream) {
  stream.ConsumeWhitespace();
  CSSParserToken ident_token = stream.ConsumeIncludingWhitespaceRaw();
  DCHECK_EQ(ident_token.GetType(), kIdentToken);
  return ident_token.Value().ToAtomicString();
}

```

In a normal stylesheet parse pipeline, invalid `env()` syntax is expected to be rejected before this point. However, CSS Typed OM can store `CSSUnparsedValue` content as a `CSSUnparsedDeclarationValue` without enforcing `env()`’s argument grammar, so a value like `env(0)` can reach the substitution resolver.

For `env(0)`, the token after the `(` is a `kNumberToken`, which is not string-backed. `CSSParserToken::Value()` does not check `GetType()`/`HasStringBacking()`; it constructs a `StringView` from the token’s internal `value_*` fields:

[`CSSParserToken::Value`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.h;l=130):

```
StringView Value() const {
  return value_is_8bit_ ? StringView(Span8()) : StringView(Span16());
}

```

For non-string-backed tokens (such as `kNumberToken`), the `value_length_` / `value_data_char_raw_` fields are not initialized as a meaningful string payload. Calling `Value()` on such a token therefore yields a `StringView` with a garbage pointer/length. The subsequent `ToAtomicString()` tries to hash/copy from that span, leading to an out-of-bounds memory access.

### Bisection

This issue was introduced in commit [`27932c039882c41ae25df71df3078a5bbfb38795`](https://chromium.googlesource.com/chromium/src/+/27932c039882c41ae25df71df3078a5bbfb38795) ("StyleCascade, Phase 1") by Anders Hartvoll Ruud on 2019-07-23 ([CL 1605418](https://chromium-review.googlesource.com/c/chromium/src/+/1605418)).

### Reproduction

Using <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1585188.zip>

Run:

```
./chrome --no-sandbox --user-data-dir=/tmp/xx poc.html

```

This would trigger ASAN crash shown in `asan.txt`

### Suggested Fix

Treat non-ident first arguments in [`ConsumeVariableName`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/resolver/style_cascade.cc;l=84) as untrusted.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 42.4 KB)
- [poc.html](attachments/poc.html) (text/html, 620 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6105235680329728.

### an...@chromium.org (2026-02-18)

[security shepherd]: Thanks for the report! Triaging this to @an...@chromium.org who works on this file regularly. Hi @an...@chromium.org , would you be able to provide insight on this report? Thanks!

### ch...@google.com (2026-02-19)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2026-02-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6105235680329728

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN
Crash Address: 0x7ee14fa34000
Crash State:
  blink::AtomicStringTable::Add
  blink::AtomicString::AtomicString
  blink::StringView::ToAtomicString
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1480779:1480788

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6105235680329728

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7600415>

Stringify CSSUnparsedValues via toString, as normal

---


Expand for full commit details
```
     
    CSSUnparsedValue exposes a special stringification function 
    ToUnparsedString() in addition to the regular toString(). 
    The documentation says it returns "tokens without substituting 
    variables", but it's not clear what this means; we don't substitute 
    any variables in CSSStyleValue::toString() either. 
     
    This CL makes ToUnparsedString() private (and renames it). 
    Clients needing to serialize a CSSUnparsedValue can do so via 
    the normal toString() function. (If ToUnparsedString() existed 
    for performance reasons, that should have been documented.) 
     
    Also, the /**/-"fixup" pass over the value has been folded into 
    ToStringInternal(). This is to make it easy to find the canonical string 
    representation of this value within CSSUnparsedValue (without going 
    through a CSSValue). 
     
    The main point of this CL is to prepare for validating 
    the "argument grammar" of the value during the StyleValue-to-CSSValue 
    conversion in StylePropertyMap (which requires item (2) above). 
     
    We now jump through additional hoops to ultimately get a string 
    from the outside of CSSUnparsedValue, but there should otherwise 
    be no behavior change. 
     
    Bug: 484751092 
    Change-Id: I5db45ad85f780c67a2ea3ba8482c390ebab10068 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7600415 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590041}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/cross_thread_style_value_test.cc`
- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.h`
- M `third_party/blink/renderer/core/css/cssom/paint_worklet_style_property_map_test.cc`
- M `third_party/blink/renderer/core/css/properties/computed_style_utils.cc`

---

Hash: [05e4b544803cee54fba51bf1360ac736a30fd140](https://chromiumdash.appspot.com/commit/05e4b544803cee54fba51bf1360ac736a30fd140)  

Date: Wed Feb 25 11:24:31 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  main  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7595347>

Validate CSSUnparsedValues upon assignment

---


Expand for full commit details
```
     
    CSS Typed OM has a concept of a value "matching a grammar" (or not) 
    upon assignment to a property [1]. For CSSUnparsedValues, we currently 
    don't perform any significant validation, and as a consequence 
    we allow "invalid" CSSUnparsedDeclarationValues to be created 
    (causing DCHECKs later in the pipeline). 
     
    This CL makes sure values can be parsed using CSSVariableParser:: 
    ConsumeUnparsedDeclaration before assignment. 
     
    We're still not handling the value in the context of the destination 
    property, which we probably should. This is also a problem with 
    current state of things, however, so for now the goal is primarily 
    to avoid the DCHECKs in Issue 484751092. 
     
    Finally, I opened an issue against the specification [2], which 
    currently doesn't define any of this. 
     
    [1] https://drafts.css-houdini.org/css-typed-om-1/#create-an-internal-representation 
    [2] https://github.com/w3c/csswg-drafts/issues/13547 
     
    Fixed: 484751092 
    Change-Id: Id7f888a6df8c02ade24910900f5d01909cb2dfad 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7595347 
    Reviewed-by: Steinar H Gunderson <sesse@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1590110}

```

---

Files:

- M `third_party/blink/renderer/build/scripts/core/css/templates/cssom_types.cc.tmpl`
- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.h`
- D `third_party/blink/web_tests/external/wpt/css/css-typed-om/missing-variable-in-unparsed-value-crash.html`
- A `third_party/blink/web_tests/external/wpt/css/css-typed-om/set-invalid-untyped-value-crash.html`

---

Hash: [5efc7a0127a6a735e252e67cecaced918d5bf42a](https://chromiumdash.appspot.com/commit/5efc7a0127a6a735e252e67cecaced918d5bf42a)  

Date: Wed Feb 25 14:21:21 2026


---

### ch...@google.com (2026-02-25)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### 24...@project.gserviceaccount.com (2026-02-27)

ClusterFuzz testcase 6105235680329728 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1590105:1590112

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### an...@chromium.org (2026-02-27)

> If there are multiple CLs required, please list all.

One CL was indeed missing from the list, since I linked it to the wrong bug by accident. Now added.

### ch...@google.com (2026-02-27)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### he...@gmail.com (2026-03-03)

Thank you. I can verify that the commits indeed fix the issue on the ToT. We may need to set "Fixed By Code" field with the gerrit change 7606599, 7600415, 7595347 to meet the bot's requirements and mark the status as fixed.

Many thanks!

### ch...@google.com (2026-03-04)

Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1590110) appears to be after beta branch point (1582197).
Security Merge Request - Manual Review: Merge review required: M146 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [146].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### an...@chromium.org (2026-03-04)

3. Maybe. I'd rather not merge these three CLs.

However, we could land a trivial DCHECK->CHECK change in addition to all this, and merge that? (Converting this into a "safe" crash.) EDIT: <https://chromium-review.googlesource.com/c/chromium/src/+/7633403>

### dr...@chromium.org (2026-03-04)

If you have concerns about stability, I'd definitely support the CL from [#comment17](https://issues.chromium.org/issues/484751092#comment17) instead of merging.

### dr...@chromium.org (2026-03-07)

andruud@ - do you still plan to land <https://crrev.com/c/7633403>? I do think that's the better merge candidate.

### an...@chromium.org (2026-03-07)

Apologies, I missed your [comment #18](https://issues.chromium.org/issues/484751092#comment18) from a few days ago. Yes, let's land it and merge it.

EDIT: "It" being: <https://chromium-review.googlesource.com/c/chromium/src/+/7633403>

### dx...@google.com (2026-03-09)

Project: chromium/src  

Branch:  main  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7633403>

CHECK token type in ConsumeVariableName

---


Expand for full commit details
```
     
    CL:7595347, CL:7600415, and CL:7606599 already fixed Issue 484751092, 
    however they are too complicated to backport safely. 
     
    Using a CHECK here eliminates any security issues that could 
    arise from failing the DCHECK. 
     
    Bug: 484751092 
    Change-Id: I676362a5009259652b973abaafd7f3ee35435abc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633403 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1596248}

```

---

Files:

- M `third_party/blink/renderer/core/css/resolver/style_cascade.cc`

---

Hash: [93e47ab8bdc18c07e2a0e581d0a7fb6dbc82ad49](https://chromiumdash.appspot.com/commit/93e47ab8bdc18c07e2a0e581d0a7fb6dbc82ad49)  

Date: Mon Mar 9 11:06:49 2026


---

### an...@chromium.org (2026-03-09)

drubery@: <https://chromium-review.googlesource.com/c/chromium/src/+/7633403> is in --- I suggest merging that CL (and only that CL) to 146.

### dr...@chromium.org (2026-03-09)

Yep, thank you. Approved to merge to M146.

### dx...@google.com (2026-03-12)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7658324>

CHECK token type in ConsumeVariableName

---


Expand for full commit details
```
     
    CL:7595347, CL:7600415, and CL:7606599 already fixed Issue 484751092, 
    however they are too complicated to backport safely. 
     
    Using a CHECK here eliminates any security issues that could 
    arise from failing the DCHECK. 
     
    (cherry picked from commit 93e47ab8bdc18c07e2a0e581d0a7fb6dbc82ad49) 
     
    Bug: 484751092 
    Change-Id: I676362a5009259652b973abaafd7f3ee35435abc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633403 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1596248} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7658324 
    Auto-Submit: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#2388} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/css/resolver/style_cascade.cc`

---

Hash: [e6065b6de436da359140e20efa246c48a58fed6b](https://chromiumdash.appspot.com/commit/e6065b6de436da359140e20efa246c48a58fed6b)  

Date: Thu Mar 12 00:30:54 2026


---

### pe...@google.com (2026-03-12)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### pe...@google.com (2026-03-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-03-12)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7659463
2. Low - There was no conflict.
3. 146
4. Yes, the bug was introduced by the suspected CL[1] in 2019. Thus, the issue might occur in M138.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/1605418

### sp...@google.com (2026-03-20)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High-quality report of demonstrated memory corruption in a sandboxed process and a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### an...@google.com (2026-03-27)

Approved for LTS 138.

### dx...@google.com (2026-04-08)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7659463>

[M138-LTS] CHECK token type in ConsumeVariableName

---


Expand for full commit details
```
     
    CL:7595347, CL:7600415, and CL:7606599 already fixed Issue 484751092, 
    however they are too complicated to backport safely. 
     
    Using a CHECK here eliminates any security issues that could 
    arise from failing the DCHECK. 
     
    (cherry picked from commit 93e47ab8bdc18c07e2a0e581d0a7fb6dbc82ad49) 
     
    Bug: 484751092 
    Change-Id: I676362a5009259652b973abaafd7f3ee35435abc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633403 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1596248} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7659463 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3526} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/core/css/resolver/style_cascade.cc`

---

Hash: [f9694e5cd23ace9b556b2271d3b45daadeb0fccd](https://chromiumdash.appspot.com/commit/f9694e5cd23ace9b556b2271d3b45daadeb0fccd)  

Date: Wed Apr 8 02:06:07 2026


---

### pe...@google.com (2026-05-08)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-05-08)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/7825570>
2. Low - There was no conflict.
3. 146
4. Yes, the bug was introduced by the suspected CL in 2019. Thus, the issue might occur in M144.

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7825570>

[M144-LTS] CHECK token type in ConsumeVariableName

---


Expand for full commit details
```
     
    CL:7595347, CL:7600415, and CL:7606599 already fixed Issue 484751092, 
    however they are too complicated to backport safely. 
     
    Using a CHECK here eliminates any security issues that could 
    arise from failing the DCHECK. 
     
    (cherry picked from commit 93e47ab8bdc18c07e2a0e581d0a7fb6dbc82ad49) 
     
    Bug: 484751092 
    Change-Id: I676362a5009259652b973abaafd7f3ee35435abc 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7633403 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1596248} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7825570 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Reviewed-by: Giovanni Pezzino <giovax@google.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4868} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/css/resolver/style_cascade.cc`

---

Hash: [13fdb0a9cd1aa4ba1f646a2dde5059143c1aa012](https://chromiumdash.appspot.com/commit/13fdb0a9cd1aa4ba1f646a2dde5059143c1aa012)  

Date: Mon May 18 09:13:50 2026


---

### ch...@google.com (2026-06-10)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484751092)*
