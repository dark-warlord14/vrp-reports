# v8 crash in maglev::UseMarkingProcessor::MarkUse with maglev compiler

| Field | Value |
|-------|-------|
| **Issue ID** | [40062572](https://issues.chromium.org/issues/40062572) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Compiler>Maglev |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 5n...@gmail.com |
| **Assignee** | ve...@chromium.org |
| **Created** | 2023-01-10 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

v8 version:head  

build flag:  

gn gen out/x64\_release --args="target\_cpu="x64" symbol\_level=2 is\_debug=false is\_component\_build=false v8\_enable\_backtrace = true v8\_enable\_disassembler=true v8\_enable\_object\_print=true"

run flag:  

--allow-natives-syntax --maglev --maglev-inlining --stress-maglev

**Problem Description:**  

d8 crash on unreachable code with debug build

# Fatal error in ../../src/maglev/maglev-graph-builder.h, line 690

# unreachable code

# 

# 

# 

#FailureMessage Object: 0x7f62b4b65d70

For release build crash log,please see stacktrace.txt in attachments.

**Additional Comments:**

\*\*Chrome version: \*\* head \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [5_report.js](attachments/5_report.js) (text/plain, 2.6 KB)
- [stacktrace.txt](attachments/stacktrace.txt) (text/plain, 11.6 KB)
- [1406162.js](attachments/1406162.js) (text/plain, 536 B)

## Timeline

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### 5n...@gmail.com (2023-01-11)

For minimized poc.see attachments

### cl...@chromium.org (2023-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5985238978330624.

### cl...@chromium.org (2023-01-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5985238978330624

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x01fec9df5e08
Crash State:
  v8::internal::maglev::NodeBase::properties
  v8::internal::maglev::MaglevGraphBuilder::GetTaggedValue
  v8::internal::maglev::MaglevGraphBuilder::VisitSetKeyedProperty
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=83032:83033

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5985238978330624

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### dc...@chromium.org (2023-01-13)

Assigning to a random person from https://docs.google.com/document/d/13CwgSL4yawxuYg3iNlM-4ZPCB8RgJya6b8H_E2F-Aek/edit#heading=h.djws22xta9wz

[Monorail components: Blink>JavaScript>Compiler>Maglev]

### dc...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### le...@chromium.org (2023-01-13)

`--maglev-inlining` is still in development and not ready for fuzzing.

### 5n...@gmail.com (2023-01-13)

So how can we identify so many flags v8 have are ready for fuzzing or not?I know the difficulty to develop a new compiler,but I don't think it's convincing if you don't have files or notes but simply explain it as "not ready" when have issues.

### le...@chromium.org (2023-01-13)

We're currently discussing exactly this, very likely we'll add a mechanism for marking flags as "experimental" to help external researchers know which flags are fair play and which aren't.

+saelo

### sa...@google.com (2023-01-13)

Yes, we're currently discussion this. It's not clear just yet how exactly it'd look like, but we're aiming to make it so that it'll be very obvious from just looking at the flag definition if a feature is considered experimental (not ready for fuzzing) or not. Sorry for the trouble!

### 5n...@gmail.com (2023-01-13)

Thanks for the explanation,can understand.

### dc...@chromium.org (2023-01-17)

We had some internal discussion amongst the security team; my understanding is that these bugs should be left open, but with SI-None.

### cl...@chromium.org (2023-01-26)

ClusterFuzz testcase 5985238978330624 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=85474:85475

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-27)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-17)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-05)

This issue was migrated from crbug.com/chromium/1406162?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062572)*
