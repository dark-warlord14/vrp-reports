# Security: UAF in ash::diagnostics::AsyncLog::Append

| Field | Value |
|-------|-------|
| **Issue ID** | [40065267](https://issues.chromium.org/issues/40065267) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | zh...@gmail.com |
| **Assignee** | st...@google.com |
| **Created** | 2023-06-04 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**

While revisiting the fix for my previously reported issue ([b/280378934](https://issues.chromium.org/issues/280378934)),  

I came across another UAF issue in ash/system/diagnostics/async\_log.cc.

The issue is quite straightforward: when running in the thread pool [0],  

|AsyncLog::AppendImpl| accesses the |file\_path\_| member variable [1],  

which may have already been destroyed by  

|DiagnosticsLogController::ResetAndInitializeLogWriters|.

The weak pointer approach did not work in this case because the task bound  

to AppendImpl might have already started running before the destructor  

function was called.

Fortunately, reproducing this issue in the stable channel of ChromeOS may  

be challenging. This is because ResetAndInitializeLogWriters is only called  

from DiagnosticsDialog::ShowDialog, which includes UI operations that make  

it less likely for ResetAndInitializeLogWriters to win the race condition.

However, we can simulate slow IO in CreateFile by adding a sleep(3), please  

refer to the REPRODUCTION CASE section for more information.

[0] <https://source.chromium.org/chromium/chromium/src/+/main:ash/system/diagnostics/async_log.cc;l=28-30;drc=3a215d1e60a3b32928a50d00ea07ae52ea491a16>  

[1] <https://source.chromium.org/chromium/chromium/src/+/main:ash/system/diagnostics/async_log.cc;l=49-76;drc=3a215d1e60a3b32928a50d00ea07ae52ea491a16>

**VERSION**  

Bitset: <https://chromium-review.googlesource.com/c/chromium/src/+/3811019>  

Operating System: ChromeOS

FIX SUGGESTION  

<https://chromium-review.googlesource.com/c/chromium/src/+/4583920>

**REPRODUCTION CASE**

1. Git apply repro\_async\_log\_uaf.patch. NOTE: The PlayStore app in ChromeOS calls DiagnosticsDialog::ShowDialog, which is not available in linux-chromeos.  
   
   However, with this patch, we can easily test the problem. See [b/280378934](https://issues.chromium.org/issues/280378934) or  
   
   <https://crbug.com/1441306> for more information.
2. Go to chrome://certificate-manager/ and run following js code in console.

```
setInterval(()=> {chrome.send("testShowDiagnosticsDialog")}, 1000);  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State: see attached async\_log\_uaf.asan

**CREDIT INFORMATION**  

Reporter credit: Chaobin Zhang

## Attachments

- [async_log_uaf.asan](attachments/async_log_uaf.asan) (text/plain, 18.6 KB)
- [repro_async_log_uaf.patch](attachments/repro_async_log_uaf.patch) (text/plain, 2.9 KB)

## Timeline

### [Deleted User] (2023-06-04)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-07)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286210532). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed.

### st...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

[Monorail blocked-on: b/286210532]

### ch...@google.com (2023-06-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-06-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/5dba614575fa69815ade768452c4e52911b3a73c

commit 5dba614575fa69815ade768452c4e52911b3a73c
Author: ChaobinZhang <zhchbin@gmail.com>
Date: Wed Jun 14 15:44:35 2023

diagnostics: avoid race condition in AsyncLog

- Change AppendImpl and CreateFile to free functions in anonymous namespace, which prevent accessing member variables from the thread pool.
- Test that log append task does not crash after log destroyed.

Bug: 1451164, b/286210532
Test: Ran ash_unittests.



Change-Id: I2bc798a9a8b7de25dc6c2c4f7dd4b609be6b75ac
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4583920
Commit-Queue: Gavin Williams <gavinwill@chromium.org>
Reviewed-by: Gavin Williams <gavinwill@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1157551}

[modify] https://crrev.com/5dba614575fa69815ade768452c4e52911b3a73c/ash/system/diagnostics/async_log.h
[modify] https://crrev.com/5dba614575fa69815ade768452c4e52911b3a73c/ash/system/diagnostics/async_log_unittest.cc
[modify] https://crrev.com/5dba614575fa69815ade768452c4e52911b3a73c/ash/system/diagnostics/async_log.cc


### ch...@google.com (2023-06-20)

Project: chromium/src
Branch: main

commit 5dba614575fa69815ade768452c4e52911b3a73c
Author: ChaobinZhang <zhchbin@gmail.com>
Date:   Wed Jun 14 15:44:35 2023

    diagnostics: avoid race condition in AsyncLog
   
    - Change AppendImpl and CreateFile to free functions in anonymous namespace, which prevent accessing member variables from the thread pool.
    - Test that log append task does not crash after log destroyed.
   
    Bug: 1451164, b/286210532
    Test: Ran ash_unittests.
   
   
   
    Change-Id: I2bc798a9a8b7de25dc6c2c4f7dd4b609be6b75ac
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4583920
    Commit-Queue: Gavin Williams <gavinwill@chromium.org>
    Reviewed-by: Gavin Williams <gavinwill@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1157551}

M       ash/system/diagnostics/async_log.cc
M       ash/system/diagnostics/async_log.h
M       ash/system/diagnostics/async_log_unittest.cc

https://chromium-review.googlesource.com/4583920
17:45
17:45
CLs: Merged:​<none>      crrev/c/4583920
CLs: Pending:​crrev/c/4583920      <none>

### [Deleted User] (2023-06-20)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-21)

Bugjuggler: wait 1d -> b/components/1356334 

### [Deleted User] (2023-06-21)

[Empty comment from Monorail migration]

### am...@google.com (2023-06-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-06-27)

Congratulations, Chaobin Zhang! The VRP Panel has decided to award you $2,000 for this report of a heavily mitigated security bug, + $2,000 patch bonus (since your patch was non-trivial and you committed it directly yourself) + $1,000 bisect bonus. Thank you for your efforts and reporting (and patching) this issue! 

### zh...@gmail.com (2023-06-28)

Thank you very much!

### am...@google.com (2023-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-09-26)

This issue was migrated from crbug.com/chromium/1451164?no_tracker_redirect=1

[Monorail blocked-on: b/286210532]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065267)*
