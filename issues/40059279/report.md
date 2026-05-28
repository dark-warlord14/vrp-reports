# VideoTrackGenerator fails Security DCHECK(TypeConfuse) failure: IsA<Derived>(from) in casting.h

| Field | Value |
|-------|-------|
| **Issue ID** | [40059279](https://issues.chromium.org/issues/40059279) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>GetUserMedia |
| **Platforms** | Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ht...@chromium.org |
| **Created** | 2022-04-02 |
| **Bounty** | $8,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36

Steps to reproduce the problem:
#TestOn
asan-win32-release_x64-988236

#Reproduce
chrome --no-sandbox --enable-blink-test-features --user-data-dir=test fuzz-00005.html

What is the expected behavior?

What went wrong?
Type of crash
render tab

#Analysis
I speculate that the issue is introduced by this CL https://chromium-review.googlesource.com/c/chromium/src/+/3488047
The root cause of the issue is basically the same as the 1291472 I reported before. This time CL introduces VideoTrackGenerator.

#asan
[17832:12052:0402/111336.193:FATAL:casting.h(126)] Security DCHECK failed: IsA<Derived>(from).
Backtrace:
        base::debug::CollectStackTrace [0x00007FFADEA60492+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace_win.cc:305)
        base::debug::StackTrace::StackTrace [0x00007FFADE87A7FA+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack_trace.cc:218)
        logging::LogMessage::~LogMessage [0x00007FFADE8B2C2A+762] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:600)
        blink::To<blink::LocalDOMWindow,blink::ExecutionContext> [0x00007FFAEB77EC3C+420] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\platform\wtf\casting.h:126)
        blink::MediaStreamTrack::applyConstraints [0x00007FFAEE84A306+2018] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\modules\mediastream\media_stream_track.cc:805)
        blink::`anonymous namespace'::v8_media_stream_track::ApplyConstraintsOperationCallback [0x00007FFAEEDD789C+1923] (C:\b\s\w\ir\cache\builder\src\out\Release_x64\gen\third_party\blink\renderer\bindings\modules\v8\v8_media_stream_track.cc:376)
        v8::internal::FunctionCallbackArguments::Call [0x00007FFADA3F6A44+1140] (C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:152)
        v8::internal::`anonymous namespace'::HandleApiCallHelper<0> [0x00007FFADA3F3CE2+2786] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112)
        v8::internal::Builtin_Impl_HandleApiCall [0x00007FFADA3F0D81+1089] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:142)
        v8::internal::Builtin_HandleApiCall [0x00007FFADA3F006F+303] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130)
        (No symbol) [0x00007FFA77ECB8BC]

Did this work before? N/A 

Chrome version: 102.0.0.0  Channel: n/a
OS Version: 10.0

## Attachments

- [fuzz-00005.html](attachments/fuzz-00005.html) (text/plain, 338 B)
- [asan.txt](attachments/asan.txt) (text/plain, 16.6 KB)

## Timeline

### [Deleted User] (2022-04-02)

[Empty comment from Monorail migration]

### hc...@google.com (2022-04-04)

Reproduced on asan-win32-release_x64-988236, assigning to herre@ as owner of Blink>GetUserMedia

Security_Severity of low because its guarded by the --enable-blink-test-features flag

[Monorail components: Blink>GetUserMedia]

### [Deleted User] (2022-04-04)

[Empty comment from Monorail migration]

### m....@gmail.com (2022-04-04)

re https://crbug.com/chromium/1312670#c02

I think it is not appropriate to set Security_Severity-Low, it should be Security_Severity-High, Security-Impact_None label, more you can refer to this link
https://bugs.chromium.org/p/chromium/issues/detail?id=1280132#c9
https://source.chromium.org/chromium/chromium/src/+/main:docs/security/severity-guidelines.md
https://source.chromium.org/chromium/chromium/src/+/main:docs/security/security-labels.md
https://source.chromium.org/chromium/chromium/src/+/main:docs/security/vrp-faq.md

### hc...@google.com (2022-04-04)

ah right, my bad. Fixing:

### he...@google.com (2022-04-04)

Right, same behaviour as in crbug.com/1291472 -  VideoTrackGeneratorInWorker is enabled in "test", but the code isn't at all ready to actually have these objects in Worker scopes, as there are plenty of these assumptions that we can just do "To<LocalDOMWindow>(execution_context)". We've got crbug.com/1302819 to track making sure we fix these issues before enabling these features.

Harald, how do you want to handle this as part of the VTG rollout? Just disable VideoTrackGeneratorInWorker in test same as we did for MediaStreamTrackinWorker, and add this to crbug.com/1302819?

### [Deleted User] (2022-04-04)

[Empty comment from Monorail migration]

### ht...@chromium.org (2022-04-05)

A sane approach would be to guard the relevant places by if (IsInWindow) { do the usual } else { NOTIMPLEMENTED() }

This would document that we plan to get there eventually, but aren't there now.


### bo...@chromium.org (2022-04-22)

This is your friendly Security Marshal checking in since it's been a few weeks without activity. 

@hta, is there a CL in the works to implement the proposal in https://crbug.com/chromium/1312670#c8? Should someone else be involved to help? 

Setting severity to Medium since that's upper limit when reachability requires using a non-standard flag. 

### an...@chromium.org (2022-05-09)

@hta: Another ping to see if there is an update on this issue. Can someone else take this on if you are not able to? Thanks!

### ht...@chromium.org (2022-05-10)

@herre, how exactly did you disable MediaStreamTrack in worker (per #6)?
MediaStreamTrackInWorker doesn't seem to be referenced in other than generated code.



### he...@google.com (2022-05-10)

crrev.com/c/3488386 - just removed the 'status: "test",' line in third_party/blink/renderer/platform/runtime_enabled_features.json5. That means it can be enabled by commandline flag, but isn't on for any test environments (including fuzzers)

### ht...@chromium.org (2022-05-10)

got it - not listing a status means "off", which is more restrictive than "test".


### gi...@appspot.gserviceaccount.com (2022-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/05f9476b6d4ec29e6036d1f99aa986d1bdd2d50a

commit 05f9476b6d4ec29e6036d1f99aa986d1bdd2d50a
Author: Harald Alvestrand <hta@chromium.org>
Date: Wed May 11 06:13:21 2022

Disable VideoTrackGeneratorInWorker for test

The underlying infrastructure is not ready for worker.

Bug: chromium:1312670
Change-Id: Ic9fb16ceb51b31c1727bae5b090441201a095eb7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3637771
Commit-Queue: Harald Alvestrand <hta@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1001929}

[modify] https://crrev.com/05f9476b6d4ec29e6036d1f99aa986d1bdd2d50a/third_party/blink/renderer/platform/runtime_enabled_features.json5
[modify] https://crrev.com/05f9476b6d4ec29e6036d1f99aa986d1bdd2d50a/third_party/blink/web_tests/platform/generic/webexposed/global-interface-listing-dedicated-worker-expected.txt
[modify] https://crrev.com/05f9476b6d4ec29e6036d1f99aa986d1bdd2d50a/third_party/blink/web_tests/platform/generic/http/tests/serviceworker/webexposed/global-interface-listing-service-worker-expected.txt
[modify] https://crrev.com/05f9476b6d4ec29e6036d1f99aa986d1bdd2d50a/third_party/blink/web_tests/platform/generic/webexposed/global-interface-listing-shared-worker-expected.txt


### ht...@chromium.org (2022-05-11)

Hidden. Further work to actually make it work will be tracked in https://bugs.chromium.org/p/chromium/issues/detail?id=1302819 .


### [Deleted User] (2022-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-11)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-21)

putting this issue under temporary RV-SE until all issues in 1302819 have been resolved 

### [Deleted User] (2022-08-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-12-12)

https://crbug.com/chromium/1302819 has been resolved / closed (https://ccrev.com/c/4084786) as per https://bugs.chromium.org/p/chromium/issues/detail?id=1302819#c15 
-- from herre@ on that bug "Worker support for MST is actually no longer in scope for crbug.com/1288839 (we're focussing on Window -> Window transfers), so there's no anticipated date for any further Worker work.
I'll remove the "Exposed Worker MediaStreamTrackinWorker" feature flag exposure to make this clearer and close this bug." 

https://bugs.chromium.org/p/chromium/issues/detail?id=1302819#c17: 
"Feature flag to enabled Worker exposure reverted, so closing this as obsolete."

### am...@chromium.org (2022-12-15)

Thank you for this report and your patience to get it resolved. Unfortunately, this issue was in code there are no plans to ship. Since this issue has not / will not impact users, this report is unfortunately not eligible for a VRP reward. 

### am...@chromium.org (2023-01-09)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-06-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-09)

Congratulations! Since this code has remained in Chrome and presented additional security issues in the year since your report, we feel that since you brought the initial issues in this feature to light, you deserved a VRP reward for this report. The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-06-09)

[Empty comment from Monorail migration]

### is...@google.com (2023-06-09)

This issue was migrated from crbug.com/chromium/1312670?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-28)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/chrome-blintz-user-guide

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059279)*
