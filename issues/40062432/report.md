# Security: segmentation fault in ResizableArrayBuffer in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40062432](https://issues.chromium.org/issues/40062432) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ma...@chromium.org |
| **Created** | 2022-12-29 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

## INTRODUCE

After bisect, it was determined that commit ce18b115c29de846dbe397c5958160bcd39c8d09 caused this problem.

- 81696 will not trigger crash  
  
  <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-81696.zip?generation=1657727248895399&alt=media>
- And 81697 will trigger crash  
  
  <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-81697.zip?generation=1657729214312462&alt=media>

```
commit	ce18b115c29de846dbe397c5958160bcd39c8d09	[log] [tgz]  
author	Marja Hölttä <marja@chromium.org>	Wed Jul 13 08:33:15 2022  
committer	V8 LUCI CQ <v8-scoped@luci-project-accounts.iam.gserviceaccount.com>	Wed Jul 13 16:14:44 2022  
tree	39a7e9eeecbcca25f6da68dd109e1cf9c7fd4851  
parent	f4547fbe8fdb38a50ac2ea26a225cd9bd5ee15e9 [diff]  
  
[rab/gsab] Decommit the memory whenever possible  
  
Bug: v8:11111  
Change-Id: Ic07628bcf6018ea9814a38a0dab3667a7d8f0d69  
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3755145  
Commit-Queue: Marja Hölttä <marja@chromium.org>  
Reviewed-by: Shu-yu Guo <syg@chromium.org>  
Reviewed-by: Jakob Kummerow <jkummerow@chromium.org>  
Cr-Commit-Position: refs/heads/main@{#81697}  

```
## CRASH LOG

- Debug output

```
d8-linux-debug-v8-component-85034/d8  --future --harmony poc.js   
Received signal 11 SEGV_ACCERR 09970017400b  
  
==== C stack trace ===============================  
  
 [0x7f9ddbec4f83]  
 [0x7f9ddbec4ec2]  
 [0x7f9ddba05420]  
 [0x7f9d4000461f]  
[end of stack trace]  
[2]    266474 segmentation fault (core dumped)  d8-linux-debug-v8-component-85034/d8 --future --harmony poc.js  

```

**VERSION**  

Tested on v8 version： 10.5.0-11.1.0

**REPRODUCTION CASE**

1. Download debug v8 from: <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-85034.zip?generation=1672292656958122&alt=media>
2. Run: d8-linux-debug-v8-component-85034/d8 --future --harmony poc.js

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 289 B)

## Timeline

### [Deleted User] (2022-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5128400602857472.

### li...@chromium.org (2022-12-29)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Runtime]

### li...@chromium.org (2022-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5075994412253184.

### li...@chromium.org (2022-12-29)

Assigning to the owner of that CL to take a closer look at this.

### cl...@chromium.org (2022-12-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-12-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>API]

### cl...@chromium.org (2022-12-29)

Detailed Report: https://clusterfuzz.com/testcase?key=5075994412253184

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN WRITE
Crash Address: 0x7e670019c000
Crash State:
  Builtins_StringSubstring
  Builtins_ConstructProxy
  Builtins_ConstructProxy
  
Sanitizer: address (ASAN)

Recommended Security Severity: High

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=82282:82283

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5075994412253184

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### [Deleted User] (2022-12-29)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-31)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ki...@gmail.com (2023-01-08)

Hello, is there still active? Thanks!

### ma...@chromium.org (2023-01-09)

Thanks for the report! I was out of office but now I'm back; I'll have a look.

### ma...@chromium.org (2023-01-09)

Interesting, looks like this is coming from Maglev:

--harmony -> no crash
--harmony --maglev -> crash

Filed https://bugs.chromium.org/p/v8/issues/detail?id=13645 to track the Maglev implementation.

Removing security impact labels, as neither Maglev nor RAB / GSAB are shipping.

### cl...@chromium.org (2023-01-10)

ClusterFuzz testcase 5075994412253184 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=85170:85171

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-10)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations, Zhenghang! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work!

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1404079?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript>API, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062432)*
