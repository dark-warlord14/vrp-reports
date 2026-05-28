# Security DCHECK failure: IsA<Derived>(from) in casting.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40062700](https://issues.chromium.org/issues/40062700) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>CSS |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **Reporter** | m....@gmail.com |
| **Assignee** | se...@chromium.org |
| **Created** | 2023-01-17 |
| **Bounty** | $9,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=4859881134948352

Fuzzer: b0ring_webidl_fuzzer
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::StylePropertyMap::append
  blink::v8_style_property_map::AppendOperationCallback
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1015824:1015832

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4859881134948352

Issue filed automatically.

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


## Timeline

### cl...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-17)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>CSS Blink>JavaScript>API]

### cl...@chromium.org (2023-01-17)

Automatically adding ccs based on suspected regression changelists:

Enable CSSPseudoHas by blee@igalia.com - https://chromium.googlesource.com/chromium/src/+/6fab0635006e8f6658a9b0db50855d9d374e25a2

In style_perftest, support running style recalc multiple times. by sesse@chromium.org - https://chromium.googlesource.com/chromium/src/+/7fca40e491de27121eac3a15ccd549cf3f1a8863

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label.

### [Deleted User] (2023-01-17)

[Empty comment from Monorail migration]

### bl...@igalia.com (2023-01-17)

I checked the minimized test case in the report page (clusterfuzz-testcase-minimized-4859881134948352.html), and found that it does not related to `:has()` pseudo class but related to the use of CSS variable (`var()`) in `transition` property.

In the minimized test case, there is one style rule using `:has()`:
...
.cs49:has(~#id236:not(.cs50+.cs58~.cs32 .cs19)){
transition: top var(--myvar_8);

1. It still crashes after `:has()` selector removed:
...
.cs49 {
transition: top var(--myvar_8);

2. It does not crash after `var()` removed:
...
.cs49 {
transition: top 2s; 

The call-stack shows that it crashes while appending a style property:
[580869:1:0117/174254.985553:FATAL:casting.h(115)] Security DCHECK failed: IsA<Derived>(from). 
#0 0x7f086cd9ba0c base::debug::CollectStackTrace()
#1 0x7f086cac51ea base::debug::StackTrace::StackTrace()
#2 0x7f086cac51a5 base::debug::StackTrace::StackTrace()
#3 0x7f086cb15d19 logging::LogMessage::~LogMessage()
#4 0x7f0834e488d7 blink::To<>()
#5 0x7f0834fbf030 blink::To<>()
#6 0x7f083503d094 blink::StylePropertyMap::append()
#7 0x7f0837ed50d7 blink::(anonymous namespace)::v8_style_property_map::AppendOperationCallback()
#8 0x7f082cb17d4a v8::internal::FunctionCallbackArguments::Call()
#9 0x7f082cb1630e v8::internal::(anonymous namespace)::HandleApiCallHelper<>()
#10 0x7f082cb14a37 v8::internal::Builtin_Impl_HandleApiCall()
#11 0x7f082cb14327 v8::internal::Builtin_HandleApiCall()
#12 0x7f07bf998fbf <unknown>
Task trace:
#0 0x7f0836c8a19c blink::ImageLoader::ImageNotifyFinished()
#1 0x7f0836c8b434 blink::ImageLoader::DispatchErrorEvent()
#2 0x7f08644283a0 mojo::SimpleWatcher::Context::Notify()

`:has()` is a CSS selector. It doesn't seem to have anything to do with appending style properties.

### [Deleted User] (2023-01-17)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-17)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### bl...@igalia.com (2023-01-18)

Added 'Test-Predator-Wrong-CLs' since it doesn't related to the CL about ':has()'
- Enable CSSPseudoHas by blee@igalia.com - https://chromium.googlesource.com/chromium/src/+/6fab0635006e8f6658a9b0db50855d9d374e25a2

The above CL makes `:has()` a valid selector.

It means, before the CL, below style rule will be dropped since the selector is invalid:

.cs49:has(~#id236:not(.cs50+.cs58~.cs32 .cs19)){
transition: top var(--myvar_8);
}

In other words, before the CL, the above style rule is equivalent to:

.cs49:foo {
transition: top var(--myvar_8);
}

So reverting the CL unintentionally removes the 'transition: top var(--myvar_8);' line which is the actual suspect of this issue.

It would be helpful to get regression range after removing the :has() from the test-case as I tested at https://bugs.chromium.org/p/chromium/issues/detail?id=1407955#c5:

.cs49 {
transition: top var(--myvar_8);

### cl...@chromium.org (2023-01-19)

This does not look JS related; removing that component.

[Monorail components: -Blink>JavaScript>API]

### bo...@google.com (2023-01-21)

Hi @sesse, would you please take a closer look? We need a Googler to own security reports so we can make sure the cause is understood and a fix is landed quickly. Feel free to reroute if you know of someone better suited to investigate this particular issue; I CCed other OWNERS from third_party/blink/renderer/core/css/OWNERS for visibility. 

I'm adding other platforms on the assumption that this is a core CSS issue that impacts Chromium elsewhere, but omitting iOS because the Clusterfuzz report suggests v8 may be required to reach this bug. 

### se...@chromium.org (2023-01-23)

[Comment Deleted]

### se...@chromium.org (2023-01-23)

Simpler:

<!DOCTYPE html>                                                                                                                  
<style>
.x {                                                                                                                             
        transition-duration: var(--a);                                                                                           
}                                                                                                                                
</style>                                                                                                                         
<script>                                                                                                                         
document.styleSheets[0].cssRules[0].styleMap.append("transition-duration", "100ms");                                             
</script>  

### se...@chromium.org (2023-01-23)

Crashes in 100.0.4896.96, so not an immediate regression.

### gi...@appspot.gserviceaccount.com (2023-01-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2eb85f28b3716e31a8081a738228a250767033e3

commit 2eb85f28b3716e31a8081a738228a250767033e3
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Mon Jan 23 14:18:26 2023

Fix DCHECK when appending to a Typed CSSOM property with var().

Fixed: 1407955
Change-Id: I7dd6274bc9c18b09fe2b878039d73f43bbfd0655
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4187438
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1095615}

[modify] https://crrev.com/2eb85f28b3716e31a8081a738228a250767033e3/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/declared/append.tentative.html
[modify] https://crrev.com/2eb85f28b3716e31a8081a738228a250767033e3/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### [Deleted User] (2023-01-23)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $2,000 fuzzer bonus. Thank you for your efforts toward Chrome Fuzzing -- nice work! 

### [Deleted User] (2023-01-27)

Not requesting merge to dev (M111) because latest trunk commit (1095615) appears to be prior to dev branch point (1097615). If this is incorrect, please replace the Merge-NA-111 label with Merge-Request-111. If other changes are required to fix this bug completely, please request a merge if necessary.

Merge approved: your change passed merge requirements and is auto-approved for M111. Please go ahead and merge the CL to branch 5563 (refs/branch-heads/5563) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: harrysouders (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-01-27)

this fix landed on M111, no merge needed here 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-30)

ClusterFuzz testcase 4859881134948352 is still reproducing on tip-of-tree build (trunk).

Please re-test your fix against this testcase and if the fix was incorrect or incomplete, please re-open the bug. Otherwise, ignore this notification and add the ClusterFuzz-Wrong label.

### se...@chromium.org (2023-01-30)

Seemingly the test case was fixed only for longhands, not shorthands; this still crashes (the only difference is transition-duration => transition):



<!DOCTYPE html>
<style>
.x {                                                                                                                             
        transition: var(--a);                                                                                                    
}                                                                                                                                
</style>                                                                                                                         
<script>                                                                                                                         
document.styleSheets[0].cssRules[0].styleMap.append("transition-duration", "100ms");                                             
</script>

### am...@chromium.org (2023-01-30)

reopening this issue since it is not fully resolved; removing merge label as M111 may no longer be head by the time the new fix lands 

### gi...@appspot.gserviceaccount.com (2023-01-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f5d11dbbff20106322c5f2eb310c3b9cd81f86f6

commit f5d11dbbff20106322c5f2eb310c3b9cd81f86f6
Author: Steinar H. Gunderson <sesse@chromium.org>
Date: Tue Jan 31 11:38:57 2023

Fix DCHECK when appending to a Typed CSSOM property with var().

The previous fix was incomplete; this fixes another case (when trying
to set a shorthand on top of a longhand).

Fixed: 1407955
Change-Id: I5448aef7416ae0a28626e367861409446cb21c5c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4206433
Commit-Queue: Steinar H Gunderson <sesse@chromium.org>
Reviewed-by: Anders Hartvoll Ruud <andruud@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1099182}

[modify] https://crrev.com/f5d11dbbff20106322c5f2eb310c3b9cd81f86f6/third_party/blink/web_tests/external/wpt/css/css-typed-om/the-stylepropertymap/declared/append.tentative.html
[modify] https://crrev.com/f5d11dbbff20106322c5f2eb310c3b9cd81f86f6/third_party/blink/renderer/core/css/cssom/style_property_map.cc


### cl...@chromium.org (2023-01-31)

ClusterFuzz testcase 4859881134948352 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1099180:1099182

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-02-01)

This release blocking issue appears to be targeted for one or more milestones which may have already branched:

 - M111, which branched on 2023-01-26 (Chromium branch: 5563, Chromium branch position: 1097615)

Because this issue was marked as fixed on or after branch day, a merge of any CLs which landed on or after branch day may be required.

If no merge is needed (e.g. the necessary CLs are already present in the relevant branch), please remove the Merge-TBD-## label and replace it with a Merge-NA-## label (where ## corresponds to the milestone under evaluation). If a merge is necessary, please add the appropriate Merge-Request-## labels. If you're not sure, reach out to the relevant release manager (can be found at https://chromiumdash.appspot.com/schedule).

To learn more about the merge process, including how to land any required merges, see https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2023-02-06)

per https://crbug.com/chromium/1407955#c19 and https://crbug.com/chromium/1407955#c23

### [Deleted User] (2023-05-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1407955?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062700)*
