# Heap-use-after-free in blink::StyleVariables::operator==

| Field | Value |
|-------|-------|
| **Issue ID** | [40060747](https://issues.chromium.org/issues/40060747) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Animation, Blink>CSS |
| **Platforms** | Linux, Mac |
| **Reporter** | m....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-09-01 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5172717810810880

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-use-after-free READ {*}
Crash Address: 0x60b00019b6ac
Crash State:
  blink::StyleVariables::operator==
  blink::ComputedStyle::ComputeDifferenceIgnoringInheritedFirstLineStyle
  blink::ComputedStyle::ComputeDifference
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1041943

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5172717810810880

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Attachments

- [fixpatch.diff](attachments/fixpatch.diff) (text/plain, 866 B)

## Timeline

### cl...@chromium.org (2022-09-01)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-09-06)

@ping~

### [Deleted User] (2022-09-06)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-09-07)

#RCA
1. CSSParserToken class member value_data_char_raw_ holds a raw pointer from StringView by string.Bytes()[1];
2. There is no guarantee that the value_data_char_raw_ is valid for the life cycle of the CSSParserToken, resulting in UAF

```
third_party/blink/renderer/core/css/parser/css_parser_token.h:178
  void InitValueFromStringView(StringView string) {
    value_length_ = string.length();
    value_is_8bit_ = string.Is8Bit();
    value_data_char_raw_ = string.Bytes();	<<[]
  }
```

### m....@gmail.com (2022-09-07)

#PATCH
1. StringView storage is implemented by StringImpl
2. StringImpl uses reference counting to ensure the correct life cycle
3. We can solve the UAF problem by keeping a reference to StringImpl in CSSParserToken

```
diff --git a/third_party/blink/renderer/core/css/parser/css_parser_token.h b/third_party/blink/renderer/core/css/parser/css_parser_token.h
index a6e62228a8c..dc44b39d30f 100644
--- a/third_party/blink/renderer/core/css/parser/css_parser_token.h
+++ b/third_party/blink/renderer/core/css/parser/css_parser_token.h
@@ -179,6 +179,7 @@ class CORE_EXPORT CSSParserToken {
     value_length_ = string.length();
     value_is_8bit_ = string.Is8Bit();
     value_data_char_raw_ = string.Bytes();
+    impl_ = base::WrapRefCounted(string.SharedImpl());
   }
   bool ValueDataCharRawEqual(const CSSParserToken& other) const;
 
@@ -192,6 +193,7 @@ class CORE_EXPORT CSSParserToken {
   bool value_is_8bit_ : 1;
   unsigned value_length_;
   const void* value_data_char_raw_;  // Either LChar* or UChar*.
+  scoped_refptr<StringImpl> impl_;
 
   union {
     UChar delimiter_;

```

### [Deleted User] (2022-09-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### m....@gmail.com (2022-09-09)

@ping Does anyone take this issue?

### am...@chromium.org (2022-09-12)

This bug appears to have gone untriaged by a security sheriff and only handled by clusterfuzz, assigning owner and updating component accordingly 

[Monorail components: Blink>Animation Blink>CSS]

### sc...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/90fea0a15a1811043b81bf4d4cb7b52577ae12ba

commit 90fea0a15a1811043b81bf4d4cb7b52577ae12ba
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Wed Sep 14 12:41:56 2022

Add CSSTokenizer-created strings to CSSVariableData's backing strings

When computing the value of a registered custom property, we create
a CSSVariableData object equivalent to the computed CSSValue by
serializing that CSSValue to a String, then tokenizing that value.

The problem is that CSSTokenizer can create *new* string objects
during the tokenization process (see calls to CSSTokenizer::
RegisterString), without communicating that fact to the call-site.

Therefore, this CL adds a way to access those strings so they can
be added to the backing strings of the CSSVariableData.

Also added a DCHECK to verify that we don't have any tokens with
non-backed string pointers.

Fixed: 1358907
Change-Id: Ib4585cbb419b616713bb3709c7b81ca1708880ea
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3892782
Reviewed-by: Steinar H Gunderson <sesse@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1046868}

[modify] https://crrev.com/90fea0a15a1811043b81bf4d4cb7b52577ae12ba/third_party/blink/renderer/core/css/resolver/style_builder_converter.cc
[modify] https://crrev.com/90fea0a15a1811043b81bf4d4cb7b52577ae12ba/third_party/blink/web_tests/external/wpt/css/css-properties-values-api/registered-property-computation-expected.txt
[modify] https://crrev.com/90fea0a15a1811043b81bf4d4cb7b52577ae12ba/third_party/blink/renderer/core/css/parser/css_tokenizer.h
[modify] https://crrev.com/90fea0a15a1811043b81bf4d4cb7b52577ae12ba/third_party/blink/web_tests/external/wpt/css/css-properties-values-api/registered-property-computation.html
[modify] https://crrev.com/90fea0a15a1811043b81bf4d4cb7b52577ae12ba/third_party/blink/renderer/core/css/css_variable_data.h
[modify] https://crrev.com/90fea0a15a1811043b81bf4d4cb7b52577ae12ba/third_party/blink/renderer/core/css/css_variable_data.cc


### [Deleted User] (2022-09-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-14)

Requesting merge to extended stable M104 because latest trunk commit (1046868) appears to be after extended stable branch point (1012729).

Requesting merge to stable M105 because latest trunk commit (1046868) appears to be after stable branch point (1027018).

Requesting merge to beta M106 because latest trunk commit (1046868) appears to be after beta branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-09-14)

ClusterFuzz testcase 5172717810810880 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1046867:1046868

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-09-15)

Merge review required: M106 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-15)

Merge review required: M105 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-15)

Merge review required: M104 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-09-19)

There are no further planned releases of M105/stable and M104/extended stable. 
M106 merge approved, as long as there are no stability issues or other concerns with backmerging this fix to the forthcoming stable release, please go ahead and merge to branch 5249 at soonest so this fix can be included in tomorrow's stable cut of M106 for release next week. Thank you! 

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc

commit 1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Tue Sep 20 17:43:47 2022

Add CSSTokenizer-created strings to CSSVariableData's backing strings

When computing the value of a registered custom property, we create
a CSSVariableData object equivalent to the computed CSSValue by
serializing that CSSValue to a String, then tokenizing that value.

The problem is that CSSTokenizer can create *new* string objects
during the tokenization process (see calls to CSSTokenizer::
RegisterString), without communicating that fact to the call-site.

Therefore, this CL adds a way to access those strings so they can
be added to the backing strings of the CSSVariableData.

Also added a DCHECK to verify that we don't have any tokens with
non-backed string pointers.

Fixed: 1358907
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3892782
Reviewed-by: Steinar H Gunderson <sesse@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1046868}
Change-Id: Ifb6d194508e99030a5a3ed5fbad5496b7263bdc1
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3905727
Auto-Submit: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#518}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc/third_party/blink/renderer/core/css/resolver/style_builder_converter.cc
[modify] https://crrev.com/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc/third_party/blink/renderer/core/css/parser/css_tokenizer.h
[modify] https://crrev.com/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc/third_party/blink/web_tests/external/wpt/css/css-properties-values-api/registered-property-computation.html
[modify] https://crrev.com/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc/third_party/blink/renderer/core/css/css_variable_data.h
[modify] https://crrev.com/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc/third_party/blink/renderer/core/css/css_variable_data.cc
[modify] https://crrev.com/1eb1e18ad41d85cab74e7ddbd325bf1700fc13dc/third_party/blink/web_tests/platform/generic/external/wpt/css/css-properties-values-api/registered-property-computation-expected.txt


### ad...@google.com (2022-09-21)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your efforts toward Chrome Fuzzing and great work! 

### am...@chromium.org (2022-09-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### am...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-22)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1358907?no_tracker_redirect=1

[Multiple monorail components: Blink>Animation, Blink>CSS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060747)*
