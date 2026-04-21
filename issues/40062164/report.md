# Security: Debug check failed: Shared heap must not have clients at teardown, leading to SEGV_ACCERR

| Field | Value |
|-------|-------|
| **Issue ID** | [40062164](https://issues.chromium.org/issues/40062164) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2022-12-10 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

## INTRODUCE

After bisect, it was determined that commit 31e17fe62d59968f6f89f5c33eaf8fa75d375b77 caused this problem.

- 84755 will not trigger crash: Debug check failed: (clients\_head\_) == nullptr.  
  
  <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-82755.zip?generation=1661554107768774&alt=media>
- And 84756 will cause crash: Debug check failed: Shared heap must not have clients at teardown  
  
  <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-82756.zip?generation=1661557584079080&alt=media>

commit 31e17fe62d59968f6f89f5c33eaf8fa75d375b77  

Author: Shu-yu Guo [syg@chromium.org](mailto:syg@chromium.org)  

Date: Fri Aug 26 22:07:04 2022

[shared-struct, api] Support shared isolates in API

Currently the ability to create shared isolates is partially exposed to  

API. Instead of fully exposing it, this CL makes shared isolate and  

shared heap handling transparent to the embedder.

If a flag that requires the shared heap is true (currently  

--shared-string-table and --harmony-struct), the first isolate created  

in the process will create and attach to a process-wide shared isolate.  

Subsequent isolates will attach to that shared isolate. When that first isolate is deleted, the shared isolate is also deleted.

## CRASH ANALYSIS

Although this poc requires the use of d8's quit() function to trigger, I believe that it is potentially also trigger in Chrome due to it being an implementation issue in the shared isolates API.  

At the moment, it appears to be an isolate lifecycle management issue, and it may be a potential UAF.

## CRASH LOG

- Debug output

# Fatal error in ../../src/heap/safepoint.cc, line 346

# Debug check failed: Shared heap must not have clients at teardown. The first isolate that is created (in a process that has no isolates) owns the lifetime of the shared heap and is considered the main isolate. The main isolate must outlive all other isolates..

- Release output  
  
  Received signal 11 SEGV\_ACCERR 2f04000432fc

==== C stack trace ===============================

[0x5592d05b0137]  

[0x7f4035a9a420]  

[0x5592cf90ef9f]  

[0x5592cfb97d85]  

[0x5592cfb97af6]  

[0x5592cfb9cc78]  

[0x5592cfb8f568]  

[0x5592cfbb9459]  

[0x5592cf734902]  

[0x5592cf73315d]  

[0x5592cf7347ad]  

[0x5592cf73315d]  

[0x5592cf73148f]  

[0x5592cf73272d]  

[0x5592cf73247b]  

[0x5592cfa18ca3]  

[0x5592cfa192c3]  

[0x5592cf9fb009]

**VERSION**  

Tested on v8 10.7.0-11.0.0

**REPRODUCTION CASE**

1. Download debug v8 from: <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-84768.zip?generation=1670646083479813&alt=media>  
   
   or  
   
   release v8 from: <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-release%2Fd8-linux-release-v8-component-84768.zip?generation=1670646632755071&alt=media>
2. Run: `d8-linux-release-v8-component-84768/d8 --harmony --harmony-struct poc.js`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 263 B)

## Timeline

### ki...@gmail.com (2022-12-10)

If you want to use clusterfuzz for classification, please note to include the flags: --harmony --harmony-struct.

### [Deleted User] (2022-12-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6207488035848192.

### ad...@google.com (2022-12-10)

Thanks for the report. Current results from ClusterFuzz: quit is not defined

### cl...@chromium.org (2022-12-10)

ClusterFuzz testcase 6207488035848192 is closed as invalid, so closing issue.

### cl...@chromium.org (2022-12-10)

Testcase 6207488035848192 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=6207488035848192.

### ki...@gmail.com (2022-12-11)

Hello, please remove the `--omit-quit` when reproducing in clusterfuzz to enable `quit` function in v8.  Thanks!
This issue currently requires the `quit` function to trigger, and I'm not sure if `quit` can be remove.

### ki...@gmail.com (2022-12-13)

Can anyone please help with confirmation and fix? thanks

### dc...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-17)

[Empty comment from Monorail migration]

### dc...@chromium.org (2023-01-17)

This was fixed by https://chromium.googlesource.com/v8/v8/+/aa7b01698ac801cb8ea21466bbf3a47ada54fff2. Using this as the canonical bug, since it was reported first.

[Monorail components: Blink>JavaScript>Runtime]

### dc...@chromium.org (2023-01-17)

None because:

> This requires at least --shared-string-table and therefore doesn't affect production.

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-18)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-26)

Congratulations, Zhenghang! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for reporting this issue to us -- nice work! 

### am...@google.com (2023-01-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-19)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-03-19)

This issue was migrated from crbug.com/chromium/1400051?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1406471, crbug.com/chromium/1406487]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062164)*
