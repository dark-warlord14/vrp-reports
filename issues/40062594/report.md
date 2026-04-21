# v8 oobr on an obj

| Field | Value |
|-------|-------|
| **Issue ID** | [40062594](https://issues.chromium.org/issues/40062594) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 5n...@gmail.com |
| **Assignee** | le...@chromium.org |
| **Created** | 2023-01-11 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

v8 version:head  

build flag:  

gn gen out/x64\_release --args="target\_cpu="x64" symbol\_level=2 is\_debug=false is\_component\_build=false v8\_enable\_backtrace = true v8\_enable\_disassembler=true v8\_enable\_object\_print=true"

run flag:  

--allow-natives-syntax --maglev --maglev-inlining --stress-maglev

**Problem Description:**  

v8 oob read on an obj.gdb crash info shows:

RAX 0x8840018456d ◂— 0x590018458d001840  

RBX 0x7ffddd3e0650 —▸ 0x7ffddd3e0730 —▸ 0x7ffddd3e07e0 —▸ 0x7ffddd3e0948 —▸ 0x7ffddd3e09a8 ◂— ...  

RCX 0x55adfff81400 ◂— mov rbx, rbp  

RDX 0x8840006ef81 ◂— 0x900000008001915  

RDI 0x5  

RSI 0x4  

R8 0x8840019bdf9 ◂— 0xd50000007200002a /\* '\*' \*/  

R9 0x41  

R10 0x5200c  

R11 0x17  

R12 0x8840019bdf9 ◂— 0xd50000007200002a /\* '\*' \*/  

R13 0x55ae7aad2870 —▸ 0x88400000000 ◂— 0xb000  

R14 0x88400000000 ◂— 0xb000  

R15 0x55ae7ab04ca0 —▸ 0x55adfff80a00 ◂— add r9, 1  

RBP 0x7ffddd3e0650 —▸ 0x7ffddd3e0730 —▸ 0x7ffddd3e07e0 —▸ 0x7ffddd3e0948 —▸ 0x7ffddd3e09a8 ◂— ...  

RSP 0x7ffddd3e05f0 —▸ 0x55adffe4beec ◂— mov r12, qword ptr [rbp - 0x20]  

RIP 0x55adfff8141a ◂— mov eax, dword ptr [rdx + rdi\*4 + 7]  

───────────────────────────────────[ DISASM ]───────────────────────────────────  

► 0x55adfff8141a mov eax, dword ptr [rdx + rdi\*4 + 7]

**Additional Comments:**

\*\*Chrome version: \*\* 108.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Windows

## Attachments

- [4_report.js](attachments/4_report.js) (text/plain, 5.0 KB)
- [1406429.js](attachments/1406429.js) (text/plain, 1.6 KB)

## Timeline

### [Deleted User] (2023-01-11)

[Empty comment from Monorail migration]

### 5n...@gmail.com (2023-01-11)

[Comment Deleted]

### 5n...@gmail.com (2023-01-11)

Tried to minimize this poc,seems some object's prototype chain has been modified in poc,not sure if can be minimized more.

### cl...@chromium.org (2023-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=4739456233046016.

### cl...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API Blink>JavaScript>Runtime]

### cl...@chromium.org (2023-01-13)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/e4077cc01d356ae2bb162b36b0c341f6f1809513 (Revert "[ext-code-space] Change compression scheme for Code pointers").

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2023-01-13)

Detailed Report: https://clusterfuzz.com/testcase?key=4739456233046016

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: Trap
Crash Address: 0x000000000000
Crash State:
  Builtins_StringToLowerCaseIntl
  Builtins_StringSubstring
  Builtins_StringGreaterThan
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=84334:84335

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=4739456233046016

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### dc...@chromium.org (2023-01-13)

I'm not entirely sure what's triggering this sigtrap (in the rest of Chrome, it's usually a CHECK or DCHECK failure); nonetheless, I'm going to treat this as a high-severity bug for now out of an abundance of caution.

leszeks@, once the cause of the trap is a bit clearer, hopefully we can get a better idea of whether or not this has a security implications.

### le...@chromium.org (2023-01-13)

I see that --maglev-inlining is on. This flag is still in development and not yet ready for fuzzing. 

### dc...@chromium.org (2023-01-17)

My understanding is we should be leaving these bugs open but marked as SI-None to make sure they are fixed before launch (and I believe these bugs are still potentially VRP-eligible)

### le...@chromium.org (2023-01-18)

+saelo to clarify, since there's a wide gap between `--maglev` (which we hope to launch ~soon and has already been reasonably thoroughly tested) and `--maglev-inlining` (which is known to be a broken, partial implementation, and we haven't yet started trying to make it work).

### 5n...@gmail.com (2023-01-18)

RE c12:
I think maybe you shouldn't have the flag before you test it internally and ready to "make it work",it will save both you and our external reserchers' time.Just remove these flags seems much less work than thought out a way to mark them "experimental" obviously.
And I have to say that,experimental flags in other chrome modules are considered security_impact_none and security issues.

### [Deleted User] (2023-01-18)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@chromium.org (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-19)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-19)

[Empty comment from Monorail migration]

### le...@chromium.org (2023-01-20)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-02-04)

ClusterFuzz testcase 4739456233046016 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=85650:85651

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-02-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-04)

[Empty comment from Monorail migration]

### am...@google.com (2023-02-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-02-09)

[Comment Deleted]

### am...@chromium.org (2023-02-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. This issue was reported before the V8 --experimental flag and feature status was introduced. In the future such issues will not be eligible until the feature is no longer in Experimental status. 
Thank you for your efforts and reporting this issue to us! 

### 5n...@gmail.com (2023-02-10)

Thanks

### am...@google.com (2023-02-11)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-13)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-05-13)

This issue was migrated from crbug.com/chromium/1406429?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062594)*
