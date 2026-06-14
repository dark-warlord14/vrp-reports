# Security: Potential Use-After-Free in GetAttrSubstitutionValue


| Field | Value |
|-------|-------|
| **Issue ID** | [365802556](https://issues.chromium.org/issues/365802556) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 128.0.0.0 |
| **Reporter** | kd...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2024-09-10 |
| **Bounty** | $11,000.00 |

## Description

# Steps to reproduce the problem

This is found by static analyzer, I write a unit test to demonstrate how the vulnerability can occurs.
But this may still require your manual analysis, thanks for your efforts!
To reproduce, you can apply the unittest diff and run blink\_unittests --gtest\_filter=CSSParserTokenTest.SerializeDoubles

# Problem Description

```

// third_party/blink/renderer/core/css/resolver/style_cascade.cc

std::optional<CSSParserToken> GetAttrSubstitutionValue(
    const String& attribute_value,
    const CSSAttrType& attribute_type,
    const CSSParserContext& context)
    {

  CSSParserTokenStream stream(attribute_value); // [1] create a temp CSSParserTokenStream from context

  stream.ConsumeWhitespace();
  CSSParserToken token = stream.ConsumeIncludingWhitespaceRaw();      // [2] token may contain reference to the stream,
                                                                      // which is destroy after func return 
                                                                      // this is similar to CSSTokenizer
  if (!stream.AtEnd()) {
    // Only single token is allowed, see
    // https://drafts.csswg.org/css-values-5/#attr-notation.
    return std::nullopt;
  }
  
  return token;                                                       // [3] returned token may ref to the stream, which is freed

}

```

In `GetAttrSubstitutionValue`, a temporary class `CSSParserTokenStream` is created to consume the
tokens[1]. And the generated `CSSParserToken` is return as a copy.
But `CSSParserToken` has an interesting feature : it can point to the `CSSTokenizer` instead of the
string. This feature causes many prior bugs ([b/339877158](https://issues.chromium.org/issues/339877158), [b/339788215](https://issues.chromium.org/issues/339788215), [b/339458177](https://issues.chromium.org/issues/339458177)), and `CSSTokenizer`
is rewritten to avoid this issue. Now I notice that `CSSParserToken` can also points to the `CSSParserTokenStream`[2].
As long as we enter a specific attribute\_value, the token is point to the `stream`, which is destroyed after
the function return[3].

.

```

bool StyleCascade::ResolveAttrInto(CSSParserTokenStream& stream,
                                   CascadeResolver& resolver,
                                   const CSSParserContext& context,
                                   TokenSequence& out) {

 std::optional<CSSParserToken> substitution_value =
      GetAttrSubstitutionValue(attribute_value, attribute_type, context);
  // ...
  if (substitution_value.has_value()) {
    StringBuilder serialized_substitution_value;
    substitution_value->Serialize(serialized_substitution_value);  // used after free!
    out.Append(*substitution_value, serialized_substitution_value);
    AppendTaintToken(out);
    return true;
  }
}

```

And the returned token is used for serialize the stringbuilder, which cause a UAF.

Now I only create a small unittest to simulate the bug condition, The assumption is that adversary
can control the `context` by giving a malicious HTML file, in this case the UAF can happen.

I attach the unittest diff and asan below for your reference.

# Summary

Security: Potential Use-After-Free in GetAttrSubstitutionValue

# Custom Questions

#### Type of crash:

tab

#### Reporter credit:

Han Zheng (HexHive)

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- [css_tokenizer.debug.diff](attachments/css_tokenizer.debug.diff) (text/x-diff, 6.0 KB)
- [asan.txt](attachments/asan.txt) (text/plain, 17.6 KB)
- css_tokenizer.debug.diff (text/x-diff, 2.6 KB)
- [test.html](attachments/test.html) (text/html, 320 B)
- [asan.log](attachments/asan.log) (text/plain, 37.9 KB)

## Timeline

### kd...@gmail.com (2024-09-10)

sorry, the uploaded diff is for debug, please refer to the new diff, which is simpler

### kd...@gmail.com (2024-09-11)

I successfully conduct a PoC that works!
To reproduce, the command is ./chrome --enable-blink-features=CSSAdvancedAttrFunction --no-sandbox test.html

EDIT:
also reproduce on 1351127, which is the latest dev (130.0.6699.3) asan build, and the HEAD as well, which has one commit change a31015e6290f3def6f4895dd05661d27a03fec35, but does not mitigate the bug occurance

### kd...@gmail.com (2024-09-11)

## bisec

<https://chromium.googlesource.com/chromium/src.git/+/ced989bb8ad9516b68c91584923a4a2a84a5cd37> introduce the new feature `CSSAdvancedAttrFunction` and `ResolveAttrInto`
In this `ResolveAttrInto` implementation, the developer first use

```
+  CSSTokenizer tokenizer(attribute_value);
+  auto tokens = tokenizer.TokenizeToEOF();

```

which still have the same issue, i.e. `tokens` point to `CSSTokenizer`, which is destroyed after return

while the commit <https://chromium.googlesource.com/chromium/src.git/+/5144028324892737477df1cff767e3e96c201f60%5E%21/#F34> rewrite the `CSSTokenizer` to `CSSTokenizerStream`, as `CSSParserTokenStream` contains a `CSSTokenizer` that handle the token Consume, so the returned token point to the `CSSTokenizer` inside `CSSToeknizerStream`, the UAF still exists.

IMO the root cause is the commit ced989bb8ad9516b68c91584923a4a2a84a5cd37.

## patch suggestion

ensure the `CSSParserTokenStream` lives as long as token, I would suggest moving `CSSParserTokenStream stream(attribute_value)` to its caller `ResolveAttrInto` and pass a `CSSParserTokenStream&` to the function GetAttrSubstitutionValue as argument

### cl...@appspot.gserviceaccount.com (2024-09-11)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5841772634636288.

### an...@chromium.org (2024-09-11)

ClusterFuzz hasn't come back with anything so resorting to manual triage as the information provided (static analysis, asan log) looks pretty convincing.
Thanks for the analysis and bisect info!

Assigning to moonira@ based on bisect information. Feel free to re-route if necessary.
moonira@, can you clarify if CSSAdvancedAttrFunction is enabled by default?

Also, set FoundIn to 128 based on bisect info, Severity to S1 as it is a renderer memory UAF.

### kd...@gmail.com (2024-09-12)

Hi, my colleague Philipp is now working on an exploit. Could you add [maophilipp@gmail.com](mailto:maophilipp@gmail.com) to the CC list so he can share the findings if he succeeds?

Additionally, I would like to update the credit info (if there is) to : Han Zheng and Philipp Mao (HexHive)

### mo...@google.com (2024-09-12)

@anunoy CSSAdvancedAttrFunction is disabled by default.

### ap...@google.com (2024-09-13)

Project: chromium/src
Branch: main

commit 7244e2e57abb36ed1dac069f4ee06f9a1ebbb02f
Author: Munira Tursunova <moonira@google.com>
Date:   Fri Sep 13 10:58:48 2024

    Fix UAF in GetAttrSubstitutionValue
    
    CSSParserTokenStream needs to stay alive until the CSSParserToken is
    appended to out TokenSequence, since CSSParserToken is holding a
    reference to CSSParserTokenStream.
    
    Bug: 365802556
    Change-Id: Ic3f5a5277d5ab754630eb26fad120f217dab2ea2
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5853990
    Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
    Commit-Queue: Munira Tursunova <moonira@google.com>
    Cr-Commit-Position: refs/heads/main@{#1355099}

M       third_party/blink/renderer/core/css/resolver/style_cascade.cc
M       third_party/blink/web_tests/VirtualTestSuites
A       third_party/blink/web_tests/external/wpt/css/css-values/attr-crash.html

https://chromium-review.googlesource.com/5853990


### pe...@google.com (2024-09-13)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2024-09-13)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### am...@chromium.org (2024-09-13)

Thank for the fast fix, moonira@. Issues that are specific to features that are not enabled retain the same severity, but a lower priority and are designated as `security_impact-none`. I've update this issue accordingly, as well as closed this issue as fixed.
There's no backmerge of this fix required since this feature is currently disabled by default.

### sp...@google.com (2024-09-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $11000.00 for this report.

Rationale for this decision:
$10,000 for high quality report of memory corruption in a sandboxed process / the renderer + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-09-19)

Congratulations Han! Thank you for your efforts and reporting this issue to us -- very nice work!

### pe...@google.com (2024-12-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/365802556)*
