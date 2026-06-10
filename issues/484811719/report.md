# Heap-buffer-overflow in CSSUnparsedValue::FindVariableName

| Field | Value |
|-------|-------|
| **Issue ID** | [484811719](https://issues.chromium.org/issues/484811719) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2026-02-16 |
| **Bounty** | $11,000.00 |

## Description

### Summary

`CSSUnparsedValue`’s var()/env() tokenization path assumes the first argument is always string-backed, and calls [`FindVariableName()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc;l=20) as `stream.Consume().Value().ToString()` without validating the token type. When the first token inside `var(...)` is a comma (e.g. `var(,)`), the consumed token is `kCommaToken` (not string-backed), so [`CSSParserToken::Value()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.h;l=130) constructs a `StringView` from uninitialized `value_length_`/`value_data_char_raw_`.Therefore, OOB happens when we convert that `StringView` to a `String` copies an attacker-influenced size from an invalid pointer.

### Details

When converting a serialized custom property back into Typed OM segments, [`ParserTokenStreamToTokens()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc;l=41) treats any `var()`/`env()` function token as a variable-reference and immediately parses a “variable name” token.

In [`css_unparsed_value.cc`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc;l=20), the variable-name extraction does not check token type or whether the token is string-backed:

```
String FindVariableName(CSSParserTokenStream& stream) {
  stream.ConsumeWhitespace();
  return stream.Consume().Value().ToString();
}

```

For malformed input like `var(,)`, after consuming whitespace the next token is a comma (`kCommaToken`). Comma tokens are not string-backed (see [`CSSParserToken::HasStringBacking()`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.cc;l=126)), but `FindVariableName()` still calls `Value()`.

In [`css_parser_token.h`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.h;l=130), `CSSParserToken::Value()` returns a `StringView` built from `value_length_` and `value_data_char_raw_`:

```
StringView Value() const {
  return value_is_8bit_ ? StringView(Span8()) : StringView(Span16());
}

```

In [`css_parser_token.h`](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/parser/css_parser_token.h;l=87), non-string-backed tokens constructed via `CSSParserToken(CSSParserTokenType, BlockType)` do not initialize the “value” fields, so `value_length_` and `value_data_char_raw_` contain indeterminate data:

```
explicit CSSParserToken(CSSParserTokenType type,
                        BlockType block_type = kNotBlock)
    : type_(type),
      block_type_(block_type),
      numeric_value_type_(0),
      numeric_sign_(0),
      unit_(0),
      value_is_inline_(false),
      value_is_8bit_(false),
      padding_(0) {}

```

As a result, `Value().ToString()` can attempt to copy an attacker-controlled large length from an attacker-controlled pointer, leading to the OOB during the copy inside `StringView::ToString()`.

### Bisection

This issue was introduced in commit [`fb6b1c467f2705a7d8c607d512cacefd17f1488d`](https://chromium.googlesource.com/chromium/src/+/fb6b1c467f2705a7d8c607d512cacefd17f1488d) ("Convert CSSUnparsedValue parsing to the streaming parser") by Steinar H. Gunderson on 2024-08-27 ([CL 5803173](https://chromium-review.googlesource.com/c/chromium/src/+/5803173)).

### Reproduction

Using <https://storage.googleapis.com/chromium-browser-asan/linux-release/asan-linux-release-1585188.zip>

Run:

```
./chrome --no-sandbox --user-data-dir=/tmp/xx poc.html

```

You should ASAN crash which shown in the `asan.txt`

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 38.3 KB)
- [poc.html](attachments/poc.html) (text/html, 459 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2026-02-18)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4515451723776000.

### an...@chromium.org (2026-02-18)

[security shepherd]: Thanks for the report. Triaging this to @se...@chromium.org who have worked on this component. Hi @se...@chromium.org , would you be able to provide insight to whether this report is valid? Thanks!

### se...@chromium.org (2026-02-18)

I haven't verified beyond skimming the bug report and the PoC, but on the surface of it, this looks like a legitimate issue to me. Exploitability is unclear.

### ch...@google.com (2026-02-19)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-19)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2026-02-19)

Project: chromium/src  

Branch:  main  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7593255>

Fix reading of invalid data in Typed OM.

---


Expand for full commit details
```
     
    After seeing var(, we would not properly check that the next token 
    was an ident, and would just call Value(), potentially reading 
    uninitialized data. Our fix has a little defense in depth: 
     
     1. For this specific case, we check the token type. (The spec is not 
        exactly clear on exactly _what_ we should do, but right now, 
        we abort the parsing. We should probably throw an exception, 
        but getting an ExceptionState all the way down here is not trivial.) 
     2. For CSSParserTokens without a value, we add a DCHECK if someone 
        calls Value(). 
     3. In addition, we explicitly initialize data_length_ to zero, 
        so that if someone calls Value() in a non-DCHECK build, we'll 
        get an empty token instead of uninitialized data. 
     
    Style perftest parsing performance is neutral. 
     
    Fixed: 484811719 
    Change-Id: I749989639af9836abc74f90de9135c08cad804d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7593255 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1587044}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/parser/css_parser_token.h`
- A `third_party/blink/web_tests/external/wpt/css/css-typed-om/missing-variable-in-unparsed-value-crash.html`

---

Hash: [2e0a8f0ab03e48d823d391d9f77e1e96d68b7796](https://chromiumdash.appspot.com/commit/2e0a8f0ab03e48d823d391d9f77e1e96d68b7796)  

Date: Thu Feb 19 13:43:25 2026


---

### 24...@project.gserviceaccount.com (2026-02-19)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2026-02-19)

Detailed Report: https://clusterfuzz.com/testcase?key=4515451723776000

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Segv on unknown address
Crash Address: 
Crash State:
  blink::StringImpl::Create8BitIfPossible
  blink::StringView::ToString
  blink::ParserTokenStreamToTokens
  
Sanitizer: address (ASAN)

Recommended Security Severity: Critical

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1482097:1482103

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4515451723776000

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary.

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### se...@chromium.org (2026-02-19)

I don't understand what ClusterFuzz is doing here. It's hijacking the bug to basically repeat the test case as the author gave (it removed a line of error handling or something), then moving it to the WTF subcomponent?

### 24...@project.gserviceaccount.com (2026-02-20)

ClusterFuzz testcase 4515451723776000 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1587043:1587044

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### ch...@google.com (2026-02-20)

Security Merge Request Consideration: Requesting merge to beta (M146) because latest trunk commit (1587044) appears to be after beta branch point (1582197).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2026-02-20)

Merge review required: M146 is already shipping to beta.

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

### dr...@chromium.org (2026-02-21)

No crashes in Canary. Given this was found in 144, we should also merge to M145 and M144. Approving merge to all three channels.

### he...@gmail.com (2026-02-21)

Hi, I would like the change my credit to "Syn4pse" if this is will be assigned with a CVE. Thank you very much.

### go...@google.com (2026-02-24)

Please merge your change to M146 by 11:00 AM PT, Tuesday, Feb 24th so it gets picked up for M146 Early Stable release. Thank you.

### go...@google.com (2026-02-24)

[Bulk Edit]

Please merge your change to M146 by 12:30 PM PT, today, Feb 24th so it gets picked up for M146 Early Stable release tomorrow. Thank you.

### sr...@chromium.org (2026-02-24)

I wont be able to land this CP i started on 146 - https://chromium-review.googlesource.com/c/chromium/src/+/7603241 as i dont have OO permission, 

please help land it so it can go out in next week stable RC

### sr...@chromium.org (2026-02-24)

I am cutting stable RC #1 for early stable release tomorrow for 146 today around 2pm PST, please help complete all your merges before that time to be included in tomorrow release, if this is critcal and missing that timeline, please reach out to me asap

### se...@chromium.org (2026-02-24)

It is a bit unclear who you are asking; the documentation I read said that authors should stay out of security merges, but perhaps that's not the case since there are nags here? In any case, it seems to me that the CL you are referring to has OO+1.

### wf...@chromium.org (2026-02-24)

this is not sev-critical. it's a memory corruption in a sandboxed process which is sev-high.

### dx...@google.com (2026-02-24)

Project: chromium/src  

Branch:  refs/branch-heads/7680  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603241>

Fix reading of invalid data in Typed OM.

---


Expand for full commit details
```
     
    After seeing var(, we would not properly check that the next token 
    was an ident, and would just call Value(), potentially reading 
    uninitialized data. Our fix has a little defense in depth: 
     
     1. For this specific case, we check the token type. (The spec is not 
        exactly clear on exactly _what_ we should do, but right now, 
        we abort the parsing. We should probably throw an exception, 
        but getting an ExceptionState all the way down here is not trivial.) 
     2. For CSSParserTokens without a value, we add a DCHECK if someone 
        calls Value(). 
     3. In addition, we explicitly initialize data_length_ to zero, 
        so that if someone calls Value() in a non-DCHECK build, we'll 
        get an empty token instead of uninitialized data. 
     
    Style perftest parsing performance is neutral. 
     
    (cherry picked from commit 2e0a8f0ab03e48d823d391d9f77e1e96d68b7796) 
     
    Fixed: 484811719 
    Change-Id: I749989639af9836abc74f90de9135c08cad804d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7593255 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587044} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603241 
    Owners-Override: Krishna Govind <govind@chromium.org> 
    Reviewed-by: Krishna Govind <govind@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7680@{#1268} 
    Cr-Branched-From: 76b7d80e5cda23fe6537eed26d68c92e995c7f39-refs/heads/main@{#1582197}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/parser/css_parser_token.h`
- A `third_party/blink/web_tests/external/wpt/css/css-typed-om/missing-variable-in-unparsed-value-crash.html`

---

Hash: [a5cfacd70f668b48f6372b2323789869fa0a7bf5](https://chromiumdash.appspot.com/commit/a5cfacd70f668b48f6372b2323789869fa0a7bf5)  

Date: Tue Feb 24 21:58:30 2026


---

### pe...@google.com (2026-02-24)

LTS Milestone M144

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ch...@google.com (2026-02-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7632  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7609009>

Fix reading of invalid data in Typed OM.

---


Expand for full commit details
```
     
    After seeing var(, we would not properly check that the next token 
    was an ident, and would just call Value(), potentially reading 
    uninitialized data. Our fix has a little defense in depth: 
     
     1. For this specific case, we check the token type. (The spec is not 
        exactly clear on exactly _what_ we should do, but right now, 
        we abort the parsing. We should probably throw an exception, 
        but getting an ExceptionState all the way down here is not trivial.) 
     2. For CSSParserTokens without a value, we add a DCHECK if someone 
        calls Value(). 
     3. In addition, we explicitly initialize data_length_ to zero, 
        so that if someone calls Value() in a non-DCHECK build, we'll 
        get an empty token instead of uninitialized data. 
     
    Style perftest parsing performance is neutral. 
     
    (cherry picked from commit 2e0a8f0ab03e48d823d391d9f77e1e96d68b7796) 
     
    Fixed: 484811719 
    Change-Id: I749989639af9836abc74f90de9135c08cad804d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7593255 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587044} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7609009 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7632@{#3382} 
    Cr-Branched-From: 0bbdf2913883391365383b0a5dfe7bf9fd1a5213-refs/heads/main@{#1568190}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/parser/css_parser_token.h`
- A `third_party/blink/web_tests/external/wpt/css/css-typed-om/missing-variable-in-unparsed-value-crash.html`

---

Hash: [8d2acc195738bf6243997d949df4b1feed6ad441](https://chromiumdash.appspot.com/commit/8d2acc195738bf6243997d949df4b1feed6ad441)  

Date: Wed Feb 25 20:50:58 2026


---

### dx...@google.com (2026-02-25)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7609324>

Fix reading of invalid data in Typed OM.

---


Expand for full commit details
```
     
    After seeing var(, we would not properly check that the next token 
    was an ident, and would just call Value(), potentially reading 
    uninitialized data. Our fix has a little defense in depth: 
     
     1. For this specific case, we check the token type. (The spec is not 
        exactly clear on exactly _what_ we should do, but right now, 
        we abort the parsing. We should probably throw an exception, 
        but getting an ExceptionState all the way down here is not trivial.) 
     2. For CSSParserTokens without a value, we add a DCHECK if someone 
        calls Value(). 
     3. In addition, we explicitly initialize data_length_ to zero, 
        so that if someone calls Value() in a non-DCHECK build, we'll 
        get an empty token instead of uninitialized data. 
     
    Style perftest parsing performance is neutral. 
     
    (cherry picked from commit 2e0a8f0ab03e48d823d391d9f77e1e96d68b7796) 
     
    Fixed: 484811719 
    Change-Id: I749989639af9836abc74f90de9135c08cad804d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7593255 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587044} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7609324 
    Owners-Override: Srinivas Sista <srinivassista@chromium.org> 
    Commit-Queue: Srinivas Sista <srinivassista@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#4762} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/parser/css_parser_token.h`
- A `third_party/blink/web_tests/external/wpt/css/css-typed-om/missing-variable-in-unparsed-value-crash.html`

---

Hash: [cb055b2324ce90ca4ddc48cc7c71de22fb81554f](https://chromiumdash.appspot.com/commit/cb055b2324ce90ca4ddc48cc7c71de22fb81554f)  

Date: Wed Feb 25 21:31:13 2026


---

### pe...@google.com (2026-02-26)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-02-26)

1. https://chromium-review.git.corp.google.com/c/chromium/src/+/7603614
2. Low - There was no conflict.
3. 144, 145, and 146
4. Yes, M138 includes the suspected CL[1]. Thus, we need to merge back the fix to M138.

[1] https://chromium-review.git.corp.google.com/c/chromium/src/+/5803173

### dx...@google.com (2026-03-03)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Steinar H. Gunderson [sesse@chromium.org](mailto:sesse@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7603614>

[M138-LTS] Fix reading of invalid data in Typed OM.

---


Expand for full commit details
```
     
    After seeing var(, we would not properly check that the next token 
    was an ident, and would just call Value(), potentially reading 
    uninitialized data. Our fix has a little defense in depth: 
     
     1. For this specific case, we check the token type. (The spec is not 
        exactly clear on exactly _what_ we should do, but right now, 
        we abort the parsing. We should probably throw an exception, 
        but getting an ExceptionState all the way down here is not trivial.) 
     2. For CSSParserTokens without a value, we add a DCHECK if someone 
        calls Value(). 
     3. In addition, we explicitly initialize data_length_ to zero, 
        so that if someone calls Value() in a non-DCHECK build, we'll 
        get an empty token instead of uninitialized data. 
     
    Style perftest parsing performance is neutral. 
     
    (cherry picked from commit 2e0a8f0ab03e48d823d391d9f77e1e96d68b7796) 
     
    Fixed: 484811719 
    Change-Id: I749989639af9836abc74f90de9135c08cad804d2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7593255 
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org> 
    Commit-Queue: Steinar H Gunderson <sesse@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1587044} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7603614 
    Reviewed-by: Victor Gabriel Savu <vsavu@google.com> 
    Owners-Override: Victor Gabriel Savu <vsavu@google.com> 
    Commit-Queue: Gyuyoung Kim (xWF) <qkim@google.com> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3494} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `third_party/blink/renderer/core/css/cssom/css_unparsed_value.cc`
- M `third_party/blink/renderer/core/css/parser/css_parser_token.h`
- A `third_party/blink/web_tests/external/wpt/css/css-typed-om/missing-variable-in-unparsed-value-crash.html`

---

Hash: [f174ea65c8530fbdae321166463029d78e862de3](https://chromiumdash.appspot.com/commit/f174ea65c8530fbdae321166463029d78e862de3)  

Date: Tue Mar 3 01:21:01 2026


---

### sp...@google.com (2026-03-11)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
High Quality & Bisect. Renderer RCE / memory corruption in a sandboxed process


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/484811719)*
