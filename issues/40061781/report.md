# Security: global-buffer-overflow css_property.cc:27 in blink::CSSProperty::Get

| Field | Value |
|-------|-------|
| **Issue ID** | [40061781](https://issues.chromium.org/issues/40061781) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>CSS |
| **Platforms** | Linux, Mac |
| **Reporter** | m....@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-11-17 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**  

global-buffer-overflow css\_property.cc:27 in blink::CSSProperty::Get

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1068529

**REPRODUCTION CASE**  

chrome --no-sandbox --user-data-dir=test --enable-blink-test-features poc.html

Type of crash: [tab]

RCA  

DCHECK does not work in the release version[1]

```
https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/css/properties/css_property.cc;drc=b75fd5075a90ada27a3360df23fa08c83e24e995;l=24  
const CSSProperty& CSSProperty::Get(CSSPropertyID id) {  
  DCHECK_NE(id, CSSPropertyID::kInvalid);					<<\*\*\*[1]  
  DCHECK_LE(id, kLastCSSProperty);  // last property id		<<\*\*\*[1]  
  return To<CSSProperty>(CSSUnresolvedProperty::GetNonAliasProperty(id));  
}  

```
# ASAN

==17496==ERROR: AddressSanitizer: global-buffer-overflow on address 0x7ffac58717d0 at pc 0x7ffab419b238 bp 0x00e5c13fcc20 sp 0x00e5c13fcc68  

READ of size 8 at 0x7ffac58717d0 thread T0  

==17496==WARNING: Failed to use and restart external symbolizer!  

#0 0x7ffab419b237 in blink::CSSProperty::Get C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\properties\css\_property.cc:27  

#1 0x7ffab7aca38b in blink::StyleCascade::AnalyzeInterpolations C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:382  

#2 0x7ffab7ac0fd1 in blink::StyleCascade::Apply C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_cascade.cc:174  

#3 0x7ffab39665e1 in blink::StyleResolver::StyleForInterpolations C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\resolver\style\_resolver.cc:2047  

#4 0x7ffaba46448b in blink::AnimationUtils::ForEachInterpolatedPropertyValue C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\animation\_utils.cc:41  

#5 0x7ffab71870bd in blink::Animation::commitStyles C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\animation.cc:2803  

#6 0x7ffaba472b4d in blink::`anonymous namespace'::v8_animation::CommitStylesOperationCallback C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\core\v8\v8_animation.cc:694 #7 0x7ffaa21b553a in v8::internal::FunctionCallbackArguments::Call C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:146 #8 0x7ffaa21b2a21 in v8::internal::`anonymous namespace'::HandleApiCallHelper<0> C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112  

#9 0x7ffaa21b01d0 in v8::internal::Builtin\_Impl\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:143  

#10 0x7ffaa21af590 in v8::internal::Builtin\_HandleApiCall C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130  

#11 0x7ffa3fe97f3b (<unknown module>)

0x7ffac58717d0 is located 16 bytes before global variable '"..\..\third\_party\blink\renderer"...' defined in '../../third\_party/blink/renderer/platform/fonts/shaping/shape\_result\_view.cc' (0x7ffac58717e0) of size 77  

'"..\..\third\_party\blink\renderer"...' is ascii string '....\third\_party\blink\renderer\platform\fonts\shaping\shape\_result\_view.cc'  

0x7ffac58717d0 is located 34 bytes after global variable '"part == out->Parts().data() + ou"...' defined in '../../third\_party/blink/renderer/platform/fonts/shaping/shape\_result\_view.cc' (0x7ffac5871780) of size 46  

'"part == out->Parts().data() + ou"...' is ascii string 'part == out->Parts().data() + out->num\_parts\_'  

SUMMARY: AddressSanitizer: global-buffer-overflow C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\properties\css\_property.cc:27 in blink::CSSProperty::Get  

Shadow bytes around the buggy address:  

0x7ffac5871500: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7ffac5871580: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7ffac5871600: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7ffac5871680: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x7ffac5871700: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

=>0x7ffac5871780: 00 00 00 00 00 06 f9 f9 f9 f9[f9]f9 00 00 00 00  

0x7ffac5871800: 00 00 00 00 00 05 f9 f9 f9 f9 f9 f9 00 00 00 00  

0x7ffac5871880: 00 00 00 00 00 06 f9 f9 f9 f9 f9 f9 00 00 00 00  

0x7ffac5871900: 00 00 00 00 00 00 07 f9 f9 f9 f9 f9 00 00 00 00  

0x7ffac5871980: 00 00 07 f9 f9 f9 f9 f9 00 00 00 00 00 00 00 00  

0x7ffac5871a00: 00 00 06 f9 f9 f9 f9 f9 00 00 07 f9 f9 f9 f9 f9  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

Intra object redzone: bb  

ASan internal: fe  

Left alloca redzone: ca  

Right alloca redzone: cb  

==17496==ABORTING

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 4.3 KB)
- [poc.html](attachments/poc.html) (text/plain, 801 B)
- [fix.patch](attachments/fix.patch) (text/plain, 751 B)

## Timeline

### [Deleted User] (2022-11-17)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-11-17)

FIX
Turn DCHECK to CHECK

```
diff --git a/third_party/blink/renderer/core/css/properties/css_property.cc b/third_party/blink/renderer/core/css/properties/css_property.cc
index da7e6c0b3a2..72e67e349b2 100644
--- a/third_party/blink/renderer/core/css/properties/css_property.cc
+++ b/third_party/blink/renderer/core/css/properties/css_property.cc
@@ -22,8 +22,8 @@ bool CSSProperty::HasEqualCSSPropertyName(const CSSProperty& other) const {
 }
 
 const CSSProperty& CSSProperty::Get(CSSPropertyID id) {
-  DCHECK_NE(id, CSSPropertyID::kInvalid);
-  DCHECK_LE(id, kLastCSSProperty);  // last property id
+  CHECK_NE(id, CSSPropertyID::kInvalid);
+  CHECK_LE(id, kLastCSSProperty);  // last property id
   return To<CSSProperty>(CSSUnresolvedProperty::GetNonAliasProperty(id));
 }
 
```

### cl...@chromium.org (2022-11-17)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5000846439022592.

### cl...@chromium.org (2022-11-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-18)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS]

### cl...@chromium.org (2022-11-18)

Detailed Report: https://clusterfuzz.com/testcase?key=5000846439022592

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x60a000072690
Crash State:
  blink::CSSProperty::Get
  blink::StyleCascade::AnalyzeInterpolations
  blink::StyleCascade::Apply
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=793326:793333

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5000846439022592

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### dr...@chromium.org (2022-11-19)

An out of bounds read is Medium severity, and triaging to code owners

### [Deleted User] (2022-11-19)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### an...@chromium.org (2022-11-21)

[Empty comment from Monorail migration]

### an...@chromium.org (2022-11-21)

Problem appears to be that commitStyles sends SVG attribute animations to the style resolver.

https://chromium-review.googlesource.com/c/chromium/src/+/4040133


### gi...@appspot.gserviceaccount.com (2022-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e911e4a74d668826c02a10f9451ff74d5f3c427b

commit e911e4a74d668826c02a10f9451ff74d5f3c427b
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Mon Nov 21 20:04:55 2022

Ignore SVG attribute animations for commitStyles

We currently send SVG attribute interpolations to StyleResolver::
StyleForInterpolations, which cannot handle such interpolations.

Fixed by filtering out PropertyHandles which are not CSS properties.

Note that AnimationUtils::ForEachInterpolatedPropertyValue performs
the same filtering already, so this CL should have no effect on the
functionality of commitStyles.

Fixed: 1385691
Change-Id: I17bc21f0ddac25cee521404d089ba0b4b64a2a5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4040133
Reviewed-by: Kevin Ellis <kevers@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1074213}

[add] https://crrev.com/e911e4a74d668826c02a10f9451ff74d5f3c427b/third_party/blink/web_tests/external/wpt/web-animations/interfaces/Animation/commitStyles-svg-crash.html
[modify] https://crrev.com/e911e4a74d668826c02a10f9451ff74d5f3c427b/third_party/blink/renderer/core/animation/keyframe_effect.cc


### cl...@chromium.org (2022-11-22)

ClusterFuzz testcase 5000846439022592 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1074212:1074229

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-23)

Requesting merge to dev M109 because latest trunk commit (1074213) appears to be after dev branch point (1070088).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-23)

Merge approved: your change passed merge requirements and is auto-approved for M109. Please go ahead and merge the CL to branch 5414 (refs/branch-heads/5414) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pb...@google.com (2022-11-28)

[Bulk Edit] This merge has been approved for M109, please help complete your merges asap (before 4pm PST) today, so the change can be included in this week's RC build for dev/beta releases

### gi...@appspot.gserviceaccount.com (2022-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/120d291f5ff3874538a94c266e2d80e8f336c933

commit 120d291f5ff3874538a94c266e2d80e8f336c933
Author: Anders Hartvoll Ruud <andruud@chromium.org>
Date: Tue Nov 29 16:30:37 2022

Ignore SVG attribute animations for commitStyles

We currently send SVG attribute interpolations to StyleResolver::
StyleForInterpolations, which cannot handle such interpolations.

Fixed by filtering out PropertyHandles which are not CSS properties.

Note that AnimationUtils::ForEachInterpolatedPropertyValue performs
the same filtering already, so this CL should have no effect on the
functionality of commitStyles.

(cherry picked from commit e911e4a74d668826c02a10f9451ff74d5f3c427b)

Fixed: 1385691
Change-Id: I17bc21f0ddac25cee521404d089ba0b4b64a2a5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4040133
Reviewed-by: Kevin Ellis <kevers@chromium.org>
Commit-Queue: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1074213}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4063753
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Auto-Submit: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/branch-heads/5414@{#285}
Cr-Branched-From: 4417ee59d7bf6df7a9c9ea28f7722d2ee6203413-refs/heads/main@{#1070088}

[add] https://crrev.com/120d291f5ff3874538a94c266e2d80e8f336c933/third_party/blink/web_tests/external/wpt/web-animations/interfaces/Animation/commitStyles-svg-crash.html
[modify] https://crrev.com/120d291f5ff3874538a94c266e2d80e8f336c933/third_party/blink/renderer/core/animation/keyframe_effect.cc


### am...@google.com (2022-12-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-02)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1385691?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061781)*
