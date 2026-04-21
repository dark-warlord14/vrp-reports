# Security: Security DCHECK failed: IsA<Derived>(from) blink::CSSPrimitiveValue::ConvertToLength

| Field | Value |
|-------|-------|
| **Issue ID** | [40061865](https://issues.chromium.org/issues/40061865) |
| **Status** | Fixed |
| **Severity** | S4-Minimal |
| **Priority** | P4 |
| **Component** | Blink>Animation, Blink>CSS |
| **Platforms** | Linux, Windows |
| **Reporter** | m....@gmail.com |
| **Assignee** | ke...@google.com |
| **Created** | 2022-11-22 |
| **Bounty** | $7,000.00 |

## Description

**VERSION**  

WIN10 X64  

asan-win32-release\_x64-1073735

**REPRODUCTION CASE**  

chrome --no-sandbox --user-data-dir=test --enable-blink-test-features poc.html

Type of crash: [tab]

RCA  

Coming soon

ASAN  

[4360:16768:1122/112517.488:FATAL:casting.h(115)] Security DCHECK failed: IsA<Derived>(from).  

Backtrace:  

base::debug::CollectStackTrace [0x00007FFCD6CF72F2+18] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace\_win.cc:329)  

base::debug::StackTrace::StackTrace [0x00007FFCD9827B7A+26] (C:\b\s\w\ir\cache\builder\src\base\debug\stack\_trace.cc:218)  

logging::LogMessage::~LogMessage [0x00007FFCD6B53F98+696] (C:\b\s\w\ir\cache\builder\src\base\logging.cc:719)  

blink::CSSPrimitiveValue::ConvertToLength [0x00007FFCDFD69083+883] (C:\b\s\w\ir\cache\builder\src\third\_party\blink\renderer\core\css\css\_primitive\_value.cc:467)  

blink::`anonymous namespace'::InsetValueToLength [0x00007FFCE6AD46FE+1950] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\view_timeline.cc:149) blink::ViewTimeline::Create [0x00007FFCE6AD2C9F+1263] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\animation\view_timeline.cc:185) blink::`anonymous namespace'::v8\_view\_timeline::ConstructorCallback [0x00007FFCE6AD9CE9+1801] (C:\b\s\w\ir\cache\builder\src\out\Release\_x64\gen\third\_party\blink\renderer\bindings\core\v8\v8\_view\_timeline.cc:160)  

v8::internal::FunctionCallbackArguments::Call [0x00007FFCCDFC4AFB+1019] (C:\b\s\w\ir\cache\builder\src\v8\src\api\api-arguments-inl.h:146)  

v8::internal::`anonymous namespace'::HandleApiCallHelper<1> [0x00007FFCCDFC0E0A+1930] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:112) v8::internal::Builtin_Impl_HandleApiCall [0x00007FFCCDFBF733+851] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:139) v8::internal::Builtin_HandleApiCall [0x00007FFCCDFBEB51+305] (C:\b\s\w\ir\cache\builder\src\v8\src\builtins\builtins-api.cc:130) (No symbol) [0x00007FFC7FE97F3C] Task trace: Backtrace: blink::HTMLDocumentParser::ScheduleEndIfDelayed [0x00007FFCDF87F5AF+911] (C:\b\s\w\ir\cache\builder\src\third_party\blink\renderer\core\html\parser\html_document_parser.cc:817) IPC::`anonymous namespace'::ChannelAssociatedGroupController::Accept [0x00007FFCD74F4A25+3579] (C:\b\s\w\ir\cache\builder\src\ipc\ipc\_mojo\_bootstrap.cc:1022)  

Crash keys:

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 419 B)
- [asan.txt](attachments/asan.txt) (text/plain, 2.2 KB)

## Timeline

### [Deleted User] (2022-11-22)

[Empty comment from Monorail migration]

### ct...@chromium.org (2022-11-22)

Thanks for your report! One quick question (while I work on repro-ing and determining labels): are you able to reproduce this without the --no-sandbox flag?

### m....@gmail.com (2022-11-23)

 --no-sandbox is just to make it easier to generate ASAN logs, and has nothing to do with the vulnerability itself.

### m....@gmail.com (2022-11-24)

Bitset
Introduce by this CL https://chromium-review.googlesource.com/c/chromium/src/+/4010320

### cl...@chromium.org (2022-11-28)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6236789225488384.

### cl...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-29)

Detailed Report: https://clusterfuzz.com/testcase?key=6236789225488384

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Security DCHECK failure
Crash Address: 
Crash State:
  IsA<Derived>(from) in casting.h
  blink::CSSPrimitiveValue::ConvertToLength
  blink::InsetValueToLength
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1069374:1069412

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6236789225488384

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2022-11-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>Animation Blink>CSS]

### cl...@chromium.org (2022-11-29)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/chromium/src/+/7fc4465e5f2e449bfc3a801791e991947dcb5768 (Add support for inset auto and relative length units.).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### gi...@appspot.gserviceaccount.com (2022-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5a402276ffd99b62c9099f1164f04b008464eddf

commit 5a402276ffd99b62c9099f1164f04b008464eddf
Author: Kevin Ellis <kevers@google.com>
Date: Tue Nov 29 21:47:47 2022

[view-timeline] Fix handling of invalid inset

Bug: 1392588
Change-Id: I2f251564c8319cc73d87eefca223d3ce084ee5ce
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4062958
Reviewed-by: Mustaq Ahmed <mustaq@chromium.org>
Commit-Queue: Kevin Ellis <kevers@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1077089}

[modify] https://crrev.com/5a402276ffd99b62c9099f1164f04b008464eddf/third_party/blink/web_tests/external/wpt/scroll-animations/view-timelines/view-timeline-inset.html
[modify] https://crrev.com/5a402276ffd99b62c9099f1164f04b008464eddf/third_party/blink/renderer/core/animation/view_timeline.cc


### ke...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-29)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-11-30)

ClusterFuzz testcase 6236789225488384 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1077084:1077092

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-16)

Congratulations! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@google.com (2022-12-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-09)

This issue was migrated from crbug.com/chromium/1392588?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Animation, Blink>CSS]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061865)*
