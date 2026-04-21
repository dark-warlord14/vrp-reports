# Security DCHECK failed: IsA<Derived>(from) blink::TimelineOffset::Create timeline_offset.cc:82

| Field | Value |
|-------|-------|
| **Issue ID** | [40063426](https://issues.chromium.org/issues/40063426) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>Animation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2023-03-07 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1113210

**REPRODUCTION CASE**  

chrome --no-sandbox --enable-blink-test-features --user-data-dir=test poc.html

Type of crash: [tab]

#ASAN  

[15204:9672:0307/104949.197:FATAL:casting.h(115)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FF95E80CF12+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FF96181291A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FF95E9DE448+744] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:730)  

blink::TimelineOffset::Create [0x00007FF970ABD19C+908] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\animation\timeline\_offset.cc:82)  

blink::`anonymous namespace'::ConvertRangeOffset [0x00007FF971BD120D+1405] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\animatable.cc:81) blink::Animatable::animate [0x00007FF971BCF85A+2522] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\animatable.cc:171) blink::`anonymous namespace'::v8\_element::AnimateOperationCallback [0x00007FF96FC7926C+1708] (C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\modules\v8\v8\_element.cc:2595)  

v8::internal::FunctionCallbackArguments::Call [0x00007FF955593CEA+1002] (C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:146)  

v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FF95559139F+2319] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:113)  

v8::internal::Builtin\_Impl\_HandleApiCall [0x00007FF95558EF22+1026] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:148)  

v8::internal::Builtin\_HandleApiCall [0x00007FF95558E291+305] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:135)  

Builtins\_CEntry\_Return1\_ArgvOnStack\_BuiltinExit [0x00007FF9742C123A+58]  

Builtins\_InterpreterEntryTrampoline [0x00007FF974234D66+230]  

Builtins\_InterpreterEntryTrampoline [0x00007FF974234D66+230]

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 458 B)
- [fix.diff](attachments/fix.diff) (text/plain, 653 B)

## Timeline

### [Deleted User] (2023-03-07)

[Empty comment from Monorail migration]

### m....@gmail.com (2023-03-07)

Introduce by this CL
https://chromium-review.googlesource.com/c/chromium/src/+/4198530


### m....@gmail.com (2023-03-07)

My fix suggestion, just check before the type case
```
diff --git a/third_party/blink/renderer/core/animation/timeline_offset.cc b/third_party/blink/renderer/core/animation/timeline_offset.cc
index 807c0d790dbb..bfb627bedae2 100644
--- a/third_party/blink/renderer/core/animation/timeline_offset.cc
+++ b/third_party/blink/renderer/core/animation/timeline_offset.cc
@@ -79,7 +79,7 @@ absl::optional<TimelineOffset> TimelineOffset::Create(
     return absl::nullopt;
   }
 
-  if (To<CSSValueList>(value_list)->length() != 1) {
+  if (IsA<CSSValueList>(value_list) || To<CSSValueList>(value_list)->length() != 1) {
     ThrowExcpetionForInvalidTimelineOffset(exception_state);
     return absl::nullopt;
   }
```

### ma...@chromium.org (2023-03-07)

Setting security_impact-none as this requires flag --enable-blink-test-features  (please let me know if this feature is enabled in any way that does not require a flag to use, eg origin trials, etc)

Severity high as this appears to be a renderer type-confusion bug that would cast and dereference as the wrong type in a non-dcheck build.

Does not seem to be os-specific. (reproduced on linux asan build)

fwiw, the suggested fix seems wrong (should be `!IsA<CSSValueList>` right?). But I'll leave deciding what the right fix is to kevers.

[Monorail components: Blink>Animation]

### cl...@chromium.org (2023-03-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6514246976995328.

### cl...@chromium.org (2023-03-08)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6250818546892800.

### pg...@google.com (2023-03-08)

(sorry ignore the first clusterfuzz link - I didn't put in the correct flags)

### cl...@chromium.org (2023-03-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-03-08)

Detailed Report: https://clusterfuzz.com/testcase?key=6250818546892800

Fuzzer: None
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::TimelineOffset::Create
  blink::ConvertRangeOffset
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1114270:1114271

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6250818546892800



### pg...@google.com (2023-03-08)

re-adding Security_Impact-None per https://crbug.com/chromium/1422110#c4

### gi...@appspot.gserviceaccount.com (2023-03-08)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b34de769aca3038f971a051e5bd71ebbe23ab0e0

commit b34de769aca3038f971a051e5bd71ebbe23ab0e0
Author: Kevin Ellis <kevers@google.com>
Date: Wed Mar 08 16:55:03 2023

Fix DCHECK failure with invalid animation range

Bug: 1422110
Change-Id: Ie6f03f7a3848ffcf15a333db21e7cc757a70f6b4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4319646
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1114583}

[add] https://crrev.com/b34de769aca3038f971a051e5bd71ebbe23ab0e0/third_party/blink/web_tests/external/wpt/scroll-animations/crashtests/invalid-animation-range.html
[modify] https://crrev.com/b34de769aca3038f971a051e5bd71ebbe23ab0e0/third_party/blink/renderer/core/animation/timeline_offset.cc


### cl...@chromium.org (2023-03-08)

Detailed Report: https://clusterfuzz.com/testcase?key=6250818546892800

Fuzzer: None
Job Type: windows_asan_chrome
Platform Id: windows

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::TimelineOffset::Create
  blink::ConvertRangeOffset
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1114270:1114271

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6250818546892800



### cl...@chromium.org (2023-03-09)

ClusterFuzz testcase 6250818546892800 is verified as fixed in https://clusterfuzz.com/revisions?job=windows_asan_chrome&range=1114555:1114583

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### ma...@chromium.org (2023-03-09)

resetting Security_Impact-None per https://crbug.com/chromium/1422110#c4


### [Deleted User] (2023-03-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts in discovering and reporting this issue to us! 

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-06-15)

This issue was migrated from crbug.com/chromium/1422110?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063426)*
