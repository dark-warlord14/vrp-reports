# UAF in SetPreludeText

| Field | Value |
|-------|-------|
| **Issue ID** | [339877158](https://issues.chromium.org/issues/339877158) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2024-05-11 |
| **Bounty** | $500.00 |

## Description

Same as issue 339788215

void StyleRuleScope::SetPreludeText(const ExecutionContext* execution_context,
                                    String value,
                                    CSSNestingType nesting_type,
                                    StyleRule* parent_rule_for_nesting,
                                    bool is_within_scope,
                                    StyleSheetContents* style_sheet) {
  auto* parser_context =
      MakeGarbageCollected<CSSParserContext>(*execution_context);
  Vector<CSSParserToken, 32> tokens = CSSTokenizer(value).TokenizeToEOF();

  StyleRule* old_parent = style_scope_->RuleForNesting();
  style_scope_ =
      StyleScope::Parse(tokens, parser_context, nesting_type,
                        parent_rule_for_nesting, is_within_scope, style_sheet);

  // Reparent rules within the @scope's body.
  Reparent(old_parent, style_scope_->RuleForNesting());
}


## Timeline

### ad...@google.com (2024-05-11)

[Code is here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/style_rule.cc;l=710?q=StyleRuleScope::SetPreludeText)

I can't see any reason why this isn't a valid UaF which could be used to achieve renderer RCE - so rating as S1. I can't see evidence this code has changed recently, so assuming this impacts Extended Stable, and labelling thus.

### ti...@chromium.org (2024-05-11)

Note, this codepath can only be reached if devtools is open. So it might not be S1.

### ha...@gmail.com (2024-05-12)

Yes, this requires user interaction and the inspector needs to modify the css elements.

### ti...@chromium.org (2024-05-12)

Thanks for confirming hackyzh003@. Great variant analysis! Moving this one to S2, keeping the ParseDarkColorOverride bug at S1.

### pe...@google.com (2024-05-12)

Setting milestone because of s2 severity.

### pe...@google.com (2024-05-12)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2024-05-16)

Project: chromium/src
Branch: main

commit 3b8269266c842fdc8e1f4f5d61649b6ac032674b
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date:   Thu May 16 07:32:15 2024

    [@scope] Don't crash on escapes in StyleRuleScope::SetPreludeText
    
    The CSSTokenizer needs to stay alive at least as long as the tokens
    it produces, since those tokens can hold StringViews into the
    tokenizer's string pool.
    
    Fixed: 339877158
    Change-Id: Ia4bcde5b21d127e9920d329ebbed99e68cccc7ff
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5537901
    Reviewed-by: Vladimir Levin <vmpstr@chromium.org>
    Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1301796}

M       third_party/blink/renderer/core/css/style_rule.cc
M       third_party/blink/renderer/core/css/style_rule_test.cc

https://chromium-review.googlesource.com/5537901


### sp...@google.com (2024-06-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
thank you reward for a report of very highly mitigated potential memory corruption issue in a sandboxed process 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-21)

Thank you for your efforts and reporting this issue to us!

### pe...@google.com (2024-08-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/339877158)*
