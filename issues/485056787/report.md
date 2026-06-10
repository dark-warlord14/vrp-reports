# UAF in RouteMatching

| Field | Value |
|-------|-------|
| **Issue ID** | [485056787](https://issues.chromium.org/issues/485056787) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Images>Codecs |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2026-02-17 |
| **Bounty** | $3,000.00 |

## Description

### Summary

`@route` descriptor parsing for `pattern:` accepts `url-pattern(...)` and calls [`css_parsing_utils::ConsumeUrlPattern()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/properties/css_parsing_utils.cc;l=1824), which only `DCHECK`s that the first token inside the function is a `kStringToken` before interning `AtomicString(token.Value())`. With malformed inputs such as `pattern: url-pattern(0)` or `pattern: url-pattern(,)`, the consumed token becomes a non-string-backed token (Number/Comma), so [`CSSParserToken::Value()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.h;l=130) constructs a `StringView` from uninitialized `value_length_`/`value_data_char_raw_`, leading to the UAF during atomic string creation.

> NOTE that the root cause of this issue is totally different from the previous issue I reported in 484811719, 484751092.

### Details

The `@route` rule’s `pattern:` descriptor is parsed via [`AtRuleDescriptorParser::ParseAtRouteDescriptor()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/at_rule_descriptor_parser.cc;l=571), which delegates directly to `ConsumeUrlPattern()`:

```
CSSValue* AtRuleDescriptorParser::ParseAtRouteDescriptor(
    AtRuleDescriptorID id,
    CSSParserTokenStream& stream,
    const CSSParserContext& context) {
  switch (id) {
    case AtRuleDescriptorID::Pattern:
      return css_parsing_utils::ConsumeUrlPattern(stream, context);
    ...
  }
}

```

In [`css_parsing_utils::ConsumeUrlPattern()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/properties/css_parsing_utils.cc;l=1824), the implementation consumes the first token inside the `url-pattern(...)` block, but only enforces the required `kStringToken` type with a `DCHECK` before calling `token.Value()`:

```
CSSURLPatternValue* ConsumeUrlPattern(CSSParserTokenStream& stream,
                                      const CSSParserContext& context) {
  stream.EnsureLookAhead();

  CSSParserToken token = stream.Peek();
  if (token.GetType() != kFunctionToken ||
      token.FunctionId() != CSSValueID::kUrlPattern) {
    return nullptr;
  }

  {
    CSSParserTokenStream::RestoringBlockGuard guard(stream);
    stream.ConsumeWhitespace();
    token = stream.ConsumeIncludingWhitespace();
    if (token.GetType() == kBadStringToken || !stream.AtEnd()) {
      return nullptr;
    }
    guard.Release();
  }
  DCHECK_EQ(token.GetType(), kStringToken);
  stream.ConsumeWhitespace();

  return MakeGarbageCollected<CSSURLPatternValue>(AtomicString(token.Value()));
}

```

When the function argument is *not* a string token but the block still ends immediately (e.g. `url-pattern(0)` or `url-pattern(,)`), the `token.GetType() == kBadStringToken` check does not trigger and `stream.AtEnd()` becomes true after consuming the single token. In release builds, the `DCHECK_EQ(token.GetType(), kStringToken)` doesn't work, and the code calls `AtomicString(token.Value())` on a non-string-backed token.

For non-string-backed tokens like `kNumberToken` and `kCommaToken`, the constructors intentionally do not initialize the string value fields. For example, the `kNumberToken` constructor in [`css_parser_token.cc`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.cc;l=29) does not initialize `value_is_8bit_`, `value_length_`, or `value_data_char_raw_`:

```
CSSParserToken::CSSParserToken(CSSParserTokenType type,
                               double numeric_value,
                               NumericValueType numeric_value_type,
                               NumericSign sign)
    : type_(type),
      block_type_(kNotBlock),
      numeric_value_type_(numeric_value_type),
      numeric_sign_(sign),
      unit_(static_cast<unsigned>(CSSPrimitiveValue::UnitType::kNumber)),
      value_is_inline_(false) {
  DCHECK_EQ(type, kNumberToken);
  numeric_value_ = ClampTo<double>(numeric_value, ...);
}

```

As a result, calling `Value()` on these tokens constructs a `StringView` with an indeterminate pointer/length, and the downstream `AtomicString(...)` interning/hashing reads from that invalid region. Therefore, this lead to the `heap-use-after-free` in Blink.

### Bisection

This issue is introduced by the commit `8e04761fa566d59ce3072549fcf12130616e7c3d` ([RouteMatching] Add CSS @route rule).

### Reproduction

Download <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1585188.zip>

Run:

```
./chrome --no-sandbox --enable-blink-features=RouteMatching poc.html

```

This would trigger UAF crash shown in the `asan.txt`

### Suggested Fix

In `css_parsing_utils::ConsumeUrlPattern()`, replace the `DCHECK_EQ(token.GetType(), kStringToken)` with hard **CHECK(...)** or other conditional check.

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 48.6 KB)
- [poc.html](attachments/poc.html) (text/html, 670 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6674858570088448.

### an...@chromium.org (2026-02-18)

[security shepherd]: Thanks for the report. Triaging this to @an...@chromium.org . Hi @an...@chromium.org , would you be able to help investigate this further? Thanks!

### 24...@project.gserviceaccount.com (2026-02-19)

Detailed Report: https://clusterfuzz.com/testcase?key=6674858570088448

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Null-dereference READ
Crash Address: 0x000000000010
Crash State:
  blink::AtomicStringTable::Add
  blink::AtomicString::AtomicString
  blink::css_parsing_utils::ConsumeUrlPattern
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1586704:1586708

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6674858570088448

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### he...@gmail.com (2026-02-19)

deleted

### 24...@project.gserviceaccount.com (2026-02-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### he...@gmail.com (2026-02-19)

Not sure why cf only report the nullderef in the comment, looking in the cf detail report page, other chrome build type in clusterfuzz such as linux\_asan\_chrome\_media did reproduce the uaf already.

### ch...@google.com (2026-02-20)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-20)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### 24...@project.gserviceaccount.com (2026-02-23)

ClusterFuzz testcase 6674858570088448 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1588468:1588469

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### an...@chromium.org (2026-02-23)

I doubt that's correct.

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  main  

Author:  Anders Hartvoll Ruud [andruud@chromium.org](mailto:andruud@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7594807>

[@route] Make ConsumeUrlPattern more robust

---


Expand for full commit details
```
     
    We currently check for kBadStringToken specifically (and unexpected 
    extra tokens), but we really only accept *one* token type inside 
    the url-pattern() function: kStringToken. 
     
    I've also removed the attr()-tainting code, which does not need 
    to be handled here. (That should be handled when parsing URLs 
    that can lead to network requests against those URLs.) 
     
    Fixed: 485056787 
    Change-Id: I74e8ad8831fbac81fd3c47a4911b86da6979bd48 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7594807 
    Reviewed-by: Morten Stenshorne <mstensho@chromium.org> 
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1589309}

```

---

Files:

- M `third_party/blink/renderer/core/css/properties/css_parsing_utils.cc`
- M `third_party/blink/renderer/core/css/properties/css_parsing_utils.h`
- M `third_party/blink/renderer/core/css/properties/css_parsing_utils_test.cc`
- A `third_party/blink/web_tests/wpt_internal/route/crashtests/invalid-url-pattern-argument.html`

---

Hash: [e932b16b6478e38438451e93284db03baaa9e08d](https://chromiumdash.appspot.com/commit/e932b16b6478e38438451e93284db03baaa9e08d)  

Date: Tue Feb 24 12:12:22 2026


---

### ch...@google.com (2026-02-24)

Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1589309) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-25)

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

### dr...@chromium.org (2026-02-25)

<https://chromestatus.com/feature/4771962874363904> says RouteMatching is still being developed. Since this isn't shipping to users (not yet in OT), there's no need for a merge.

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Low impact user information disclosure with bisect


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-06-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/485056787)*
