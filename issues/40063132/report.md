# Security: Security DCHECK failed: IsA<Derived>(from) blink::StylePropertyMap::append style_property_map.cc:384

| Field | Value |
|-------|-------|
| **Issue ID** | [40063132](https://issues.chromium.org/issues/40063132) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2023-02-17 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

Chromium: 1106701

**REPRODUCTION CASE**

<https://clusterfuzz.com/testcase-detail/4781580571836416(Request> access from the security team)

Type of crash: [tab]

It seems that CF encountered some problems and did not report the problem automatically, I will provide minipoc later

ASAN

=================================================================  

==1==ERROR: AddressSanitizer: ILL on unknown address 0x564d1b02af73 (pc 0x564d1b02af73 bp 0x7fffefbe0210 sp 0x7fffefbde840 T0)  

SCARINESS: 10 (signal)  

#0 0x564d1b02af73 in ImmediateCrash base/immediate\_crash.h:144:3  

#1 0x564d1b02af73 in logging::LogMessage::~LogMessage() base/logging.cc:972:7  

#2 0x564d26d1e491 in To<blink::CSSValueList, blink::CSSValue> third\_party/blink/renderer/platform/wtf/casting.h:115:3  

#3 0x564d26d1e491 in blink::CSSValueList const\* blink::To<blink::CSSValueList, blink::CSSValue>(blink::CSSValue const\*) third\_party/blink/renderer/platform/wtf/casting.h:121:18  

#4 0x564d2bc41751 in blink::StylePropertyMap::append(blink::ExecutionContext const\*, WTF::String const&, blink::HeapVector<cppgc::internal::BasicMember<blink::V8UnionCSSStyleValueOrString, cppgc::internal::StrongMemberTag, cppgc::internal::DijkstraWriteBarrierPolicy, cppgc::internal::DisabledCheckingPolicy, cppgc::internal::CompressedPointer>, 0u> const&, blink::ExceptionState&) third\_party/blink/renderer/core/css/cssom/style\_property\_map.cc:384:21  

#5 0x564d2bc3a241 in blink::(anonymous namespace)::v8\_style\_property\_map::AppendOperationCallback(v8::FunctionCallbackInfo[v8::Value](javascript:void(0);) const&) gen/third\_party/blink/renderer/bindings/core/v8/v8\_style\_property\_map.cc:114:17  

#6 0x564d0f454402 in v8::internal::FunctionCallbackArguments::Call(v8::internal::CallHandlerInfo) v8/src/api/api-arguments-inl.h:146:3  

#7 0x564d0f452297 in v8::internal::MaybeHandle[v8::internal::Object](javascript:void(0);) v8::internal::(anonymous namespace)::HandleApiCallHelper<false>(v8::internal::Isolate\*, v8::internal::Handle[v8::internal::HeapObject](javascript:void(0);), v8::internal::Handle[v8::internal::FunctionTemplateInfo](javascript:void(0);), v8::internal::Handle[v8::internal::Object](javascript:void(0);), unsigned long\*, int) v8/src/builtins/builtins-api.cc:113:36  

#8 0x564d0f45048d in v8::internal::Builtin\_Impl\_HandleApiCall(v8::internal::BuiltinArguments, v8::internal::Isolate\*) v8/src/builtins/builtins-api.cc:148:5  

#7 0x564c9fed8ab4 (<unknown module>)  

#8 0x564c9fe4be65 (<unknown module>)  

#9 0x564c9fe4be65 (<unknown module>)

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 525 B)

## Timeline

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-02-17)

Minipoc
chrome--no-sandbox --user-data-dir=test --enable-logging=stderr poc.html

### th...@chromium.org (2023-02-17)

Adding Needs-Feedback for POC

### m....@gmail.com (2023-02-17)

already provided~

### [Deleted User] (2023-02-17)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2023-02-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5201365197586432.

### th...@chromium.org (2023-02-17)

Thanks! No luck with ClusterFuzz, but I can reproduce this on M110. verwaest@ -- could you help assess severity?

[Monorail components: Blink>JavaScript>Runtime]

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-18)

Detailed Report: https://clusterfuzz.com/testcase?key=4781580571836416

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::CSSValueList const* blink::To<blink::CSSValueList, blink::CSSValue>
  blink::StylePropertyMap::append
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1106701

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4781580571836416

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-02-18)

ClusterFuzz testcase 4781580571836416 appears to be flaky, updating reproducibility label.

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-02-21)

Similar to https://bugs.chromium.org/p/chromium/issues/detail?id=1407955

### m....@gmail.com (2023-02-24)

I recommend CC sesse@chromium.org to handle this

### th...@chromium.org (2023-02-24)

verwaest@ / leszeks@ -- could you help assess severity? And does sesse@ make sense as an owner?

(Bumping here for now, but I'll ping on Monday)

### th...@chromium.org (2023-02-24)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-02-24)

as per the stacktrace and test case in clusterfuzz (https://clusterfuzz.com/testcase-detail/4781580571836416 , it looks like this issue is related to CSS (blink::CSSValueList const* blink::To<blink::CSSValueList, blink::CSSValue>) rather than V8; based on the failure, I concur that this should be reassigned to sesse@ rather than anyone in V8. 

[Monorail components: -Blink>JavaScript>Runtime Blink>CSS]

### th...@chromium.org (2023-02-24)

Thanks for the correction! Reassigning to sesse@. Also, I am setting the severity to high since this is likely memory corruption in the renderer process.

### se...@chromium.org (2023-02-24)

Blink>CSS is the right component. I'll have a look on Monday, if I can find the time.

### [Deleted User] (2023-02-25)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2023-02-27)

I've confirmed the issue (excellent PoC; thank you). This is probably a shortcoming in the standard (it doesn't seem to cover this case); we'll need to see what the optimal behavior looks like.

### gi...@appspot.gserviceaccount.com (2023-02-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7301cf1e40fdd97594ea491676b867cf4e577edc

commit 7301cf1e40fdd97594ea491676b867cf4e577edc
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Mon Feb 27 11:57:46 2023

In Typed CSSOM, reject adding to something that is not a list.

Fixed: 1417176
Change-Id: Idef1a81af46d334c181979778c28f19ce6369718
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293477
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1110281}

[modify] https://crrev.com/7301cf1e40fdd97594ea491676b867cf4e577edc/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/inline/append.tentative.html
[modify] https://crrev.com/7301cf1e40fdd97594ea491676b867cf4e577edc/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### [Deleted User] (2023-02-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

Requesting merge to stable M110 because latest trunk commit (1110281) appears to be after stable branch point (1084008).

Requesting merge to beta M111 because latest trunk commit (1110281) appears to be after beta branch point (1097615).

Requesting merge to dev M112 because latest trunk commit (1110281) appears to be after dev branch point (1109224).

Merge approved: your change passed merge requirements and is auto-approved for M112. Please go ahead and merge the CL to branch 5615 (refs/branch-heads/5615) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

Merge review required: M110 is already shipping to stable.

Merge review required: M111 has already been cut for stable release.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [110, 111].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2023-03-01)

1. https://chromium-review.googlesource.com/c/chromium/src/+/4293477
2. It's shipping in Canary.
3. No potential stability risks.
4. No potential compatibility risks (only we ship Typed OM).
5. No manual verification needed.

### am...@chromium.org (2023-03-01)

M112 merge auto approved, please merge fix to branch 5615
M111 and M110 merges approved, please merge this fix to branches 5563 and 5615 respectively so this fix can be included in the first respins for M111/Stable and M110/Extended -- ty! 

### am...@chromium.org (2023-03-01)

** apologies -- this should have read, M111 and M110 merges approved, please merge this fix to branches 5563 and **5481** respectively so this fix can be included in the first respins for M111/Stable and M110/Extended -- ty!

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0008642a3f179db19f3ab314992f3ac3a922978f

commit 0008642a3f179db19f3ab314992f3ac3a922978f
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Thu Mar 02 15:06:57 2023

In Typed CSSOM, reject adding to something that is not a list.

(cherry picked from commit 7301cf1e40fdd97594ea491676b867cf4e577edc)

Fixed: 1417176
Change-Id: Idef1a81af46d334c181979778c28f19ce6369718
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293477
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1110281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4302969
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5563@{#945}
Cr-Branched-From: 3ac59a6729cdb287a7ee629a0004c907ec1b06dc-refs/heads/main@{#1097615}

[modify] https://crrev.com/0008642a3f179db19f3ab314992f3ac3a922978f/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/inline/append.tentative.html
[modify] https://crrev.com/0008642a3f179db19f3ab314992f3ac3a922978f/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### [Deleted User] (2023-03-02)

LTS Milestone M108

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### se...@chromium.org (2023-03-02)

1. No, this is longstanding.
2. No, this is longstanding.

### gi...@appspot.gserviceaccount.com (2023-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8bdeff95e395e809a4ce9b2a6f37f794bcda861d

commit 8bdeff95e395e809a4ce9b2a6f37f794bcda861d
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Thu Mar 02 17:28:14 2023

In Typed CSSOM, reject adding to something that is not a list.

(cherry picked from commit 7301cf1e40fdd97594ea491676b867cf4e577edc)

Fixed: 1417176
Change-Id: Idef1a81af46d334c181979778c28f19ce6369718
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293477
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1110281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4300053
Commit-Queue: Rune Lillesveen <futhark@chromium.org>
Auto-Submit: Steinar H Gunderson <sesse@chromium.org>
Reviewed-by: Rune Lillesveen <futhark@chromium.org>
Cr-Commit-Position: refs/branch-heads/5481@{#1315}
Cr-Branched-From: 130f3e4d850f4bc7387cfb8d08aa993d288a67a9-refs/heads/main@{#1084008}

[modify] https://crrev.com/8bdeff95e395e809a4ce9b2a6f37f794bcda861d/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/inline/append.tentative.html
[modify] https://crrev.com/8bdeff95e395e809a4ce9b2a6f37f794bcda861d/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### am...@google.com (2023-03-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-02)

Congratulations on another one! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and great work! 

### rz...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### rz...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-03-03)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-03-03)

1. https://crrev.com/c/4306796 for 108, https://chromium-review.googlesource.com/c/chromium/src/+/4307470 for 102
2. Low, only a simple conflict on both branches
3. 110, 111
4. Yes

### am...@google.com (2023-03-03)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-06)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-03-06)

[Empty comment from Monorail migration]

### se...@chromium.org (2023-03-07)

Is there anything I need to do here? (It's unclear to me what is “any appropriate branches” in this context, and if I'm supposed to do it or if LTS maintainers will.)

### am...@chromium.org (2023-03-07)

Hi sesse@ you shouldn't have to do anything else here now that the backmerges for standard active release channels has been completed. Owners / patch authors are only responsible for those, but are not responsible for LTS merges. LTS maintainers will evaluate fixes for LTS backmerges and complete those.  

### am...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### pg...@google.com (2023-03-07)

[Empty comment from Monorail migration]

### sr...@google.com (2023-03-07)

This bug has been approved for Merge to M112 , please help complete the merges asap so the change can get into the next M112 weekly beta release. ( M112 beta promotion is this thursday and weekly beta happens every wednesday after that) [Bulk Edit message]

### am...@google.com (2023-03-07)

Hi sesse@ the automessage above points out something I missed, this issue was auto-approved for a M112 merge, however, only the 111 and 110 backmerges were completed. Sorry, I missed that. 
Can you please merge this fix to branch 5615 ASAP. TY

### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c1fcd43e56311d66a95fcacd459c6be93d0a0b11

commit c1fcd43e56311d66a95fcacd459c6be93d0a0b11
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Wed Mar 08 01:07:51 2023

In Typed CSSOM, reject adding to something that is not a list.

(cherry picked from commit 7301cf1e40fdd97594ea491676b867cf4e577edc)

Fixed: 1417176
Change-Id: Idef1a81af46d334c181979778c28f19ce6369718
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293477
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1110281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4316170
Commit-Queue: Srinivas Sista <srinivassista@chromium.org>
Reviewed-by: Prudhvikumar Bommana <pbommana@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Owners-Override: Prudhvikumar Bommana <pbommana@google.com>
Commit-Queue: Prudhvikumar Bommana <pbommana@google.com>
Cr-Commit-Position: refs/branch-heads/5615@{#281}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/c1fcd43e56311d66a95fcacd459c6be93d0a0b11/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/inline/append.tentative.html
[modify] https://crrev.com/c1fcd43e56311d66a95fcacd459c6be93d0a0b11/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### se...@chromium.org (2023-03-09)

Seems like someone merged to 5615 now, so not doing more here.

### am...@chromium.org (2023-03-09)

Ah it looks like the release team took care of it before cutting M112 

### gm...@google.com (2023-03-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/26bfa5807606f6c7fc3ec575123e53894215c49c

commit 26bfa5807606f6c7fc3ec575123e53894215c49c
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Tue Mar 14 15:53:57 2023

[M108-LTS] In Typed CSSOM, reject adding to something that is not a list.

M108 merge issues:
  third_party/blink/renderer/core/css/cssom/style_property_map.cc:
    The check before the added IsValueList check isn't present in 108

(cherry picked from commit 7301cf1e40fdd97594ea491676b867cf4e577edc)

Fixed: 1417176
Change-Id: Idef1a81af46d334c181979778c28f19ce6369718
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4293477
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1110281}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4306796
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Steinar H Gunderson <sesse@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5359@{#1405}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/26bfa5807606f6c7fc3ec575123e53894215c49c/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/inline/append.tentative.html
[modify] https://crrev.com/26bfa5807606f6c7fc3ec575123e53894215c49c/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### vo...@google.com (2023-03-15)

[Empty comment from Monorail migration]

### gm...@google.com (2023-04-28)

Rejecting Merge for LTS-102 as there is no plans for another respin.

### [Deleted User] (2023-06-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1417176?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063132)*
