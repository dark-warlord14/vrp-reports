# Security: Debug check failed: old_entry.IsRegularEntry() in v8

| Field | Value |
|-------|-------|
| **Issue ID** | [40062610](https://issues.chromium.org/issues/40062610) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | di...@chromium.org |
| **Created** | 2023-01-12 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

## INTRODUCE

After bisect, it was determined that commit 39975b4f33e4e9704c2463b7e196c8f1cc8c13e0 caused this problem.

- 83529 will trigger crash: SEGV\_MAPERR 000000000ef8  
  
  <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-83529.zip?generation=1664959372737646&alt=media>
- And 83530 will cause crash: Debug check failed: old\_entry.IsRegularEntry()  
  
  <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-83530.zip?generation=1664959531195838&alt=media>

```
commit	39975b4f33e4e9704c2463b7e196c8f1cc8c13e0	[log] [tgz]  
author	Dominik Inführ <dinfuehr@chromium.org>	Wed Oct 05 07:39:35 2022  
committer	V8 LUCI CQ <v8-scoped@luci-project-accounts.iam.gserviceaccount.com>	Wed Oct 05 08:30:26 2022  
tree	3dfb9f73af3bd7ab65e42fa6d0e9845b5b5c89cb  
parent	2cd18db11ffc243c26fd6ea1b2ea1ce62edb50cc [diff]  
[heap] Fix remaining test failures with --shared-heap  
  
This CL fixes the remaining test failures when running test with the  
--shared-heap flag locally:  
  
\* Remove uses of shared_isolate()  
\* Fix slot recording in Mark-Compact and Scavenger  
\* Fixes DCHECKs in tests that do not hold with --shared-heap  
  
Bug: v8:13267  
Change-Id: I6869ece70f1e6156d9bb1281e6cd876cf8d471eb  
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3918377  
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>  
Reviewed-by: Jakob Linke <jgruber@chromium.org>  
Reviewed-by: Shu-yu Guo <syg@chromium.org>  
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>  
Cr-Commit-Position: refs/heads/main@{#83530}  

```

Note: after f8eebf33656666990ea29e9b788080757e94413a, the flag `--shared-space` is enabled by default.  

Therefore if you try to reproduce poc in earlier version(< 85175), please add this flag manually.

## CRASH LOG

- Debug output

```
➜  git:(main) ✗ /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/d8 --expose-gc --harmony-struct /tmp/poc.js  
  
  
#  
# Fatal error in ../../src/sandbox/external-pointer-table-inl.h, line 47  
# Debug check failed: old_entry.IsRegularEntry().  
#  
#  
#  
#FailureMessage Object: 0x7ffcbc82d920  
==== C stack trace ===============================  
  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x13) [0x7fb0454ac4b3]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8_libplatform.so(+0x187ed) [0x7fb0454517ed]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x182) [0x7fb04548b632]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8_libbase.so(+0x2c0a5) [0x7fb04548b0a5]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8.so(v8::internal::ExternalPointerTable::Exchange(unsigned int, unsigned long, v8::internal::ExternalPointerTag)+0xa2) [0x7fb0477e0fd2]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8.so(v8::internal::JSAtomicsCondition::StateT v8::internal::detail::WaiterQueueNode::EncodeHead<v8::internal::JSAtomicsCondition>(v8::internal::Isolate\*, v8::internal::detail::WaiterQueueNode\*)+0x2b) [0x7fb0477e084b]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8.so(v8::internal::JSAtomicsCondition::WaitFor(v8::internal::Isolate\*, v8::internal::Handle<v8::internal::JSAtomicsCondition>, v8::internal::Handle<v8::internal::JSAtomicsMutex>, v8::base::Optional<v8::base::TimeDelta>)+0x26c) [0x7fb0477e055c]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8.so(+0x19ae19b) [0x7fb046e6619b]  
    /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/libv8.so(v8::internal::Builtin_AtomicsConditionWait(int, unsigned long\*, v8::internal::Isolate\*)+0x97) [0x7fb046e658c7]  
    [0x7fafdf9a47bf]  
[1]    3016135 trace trap (core dumped)  /tmp/d8-linux-debug-v8-component-85237/d8-linux-debug-v8-component-85237/d8  

```

**VERSION**  

Tested on v8 version 11.1.0

NOTE OF CLUSTERFUZZ  

If you want to use clusterfuzz for classification, please note to include the flags: --expose-gc --harmony-struct

**REPRODUCTION CASE**

1. Download debug v8 from: <https://www.googleapis.com/download/storage/v1/b/v8-asan/o/linux-debug%2Fd8-linux-debug-v8-component-85237.zip?generation=1673468853557731&alt=media>
2. Run: ./d8 --expose-gc --harmony-struct /tmp/poc.js

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: Zhenghang Xiao (@Kipreyyy)

## Attachments

- [Debug-check-poc.js](attachments/Debug-check-poc.js) (text/plain, 258 B)

## Timeline

### [Deleted User] (2023-01-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5843270881181696.

### cl...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-01-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2023-01-13)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/f8eebf33656666990ea29e9b788080757e94413a ([heap] Enable --shared-space by default).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2023-01-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5843270881181696

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  old_entry.IsRegularEntry() in external-pointer-table-inl.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85174:85175

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5843270881181696

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### dc...@chromium.org (2023-01-13)

Tentatively marking this high as violating DCHECKs in the past has often preceded imminent memory safety issues.

### di...@chromium.org (2023-01-13)

[Empty comment from Monorail migration]

### ki...@gmail.com (2023-01-16)

Hello, is there still active? Thanks!

### di...@chromium.org (2023-01-16)

I was able to reproduce this issue and have a CL to fix it. This does not affect production as this requires the --harmony-struct flag.

### gi...@appspot.gserviceaccount.com (2023-01-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/601913ded3a918ddf4db97adbaec292d5e53c4c1

commit 601913ded3a918ddf4db97adbaec292d5e53c4c1
Author: Dominik Inführ <dinfuehr@chromium.org>
Date: Fri Jan 13 12:40:54 2023

[heap] Mark main isolates WaiterQueueNode in EPT with --shared-space

With --shared-space we weren't marking the main isolate's entry in
the EPT for the WaiterQueueNode.

Bug: v8:13267, chromium:1406729
Change-Id: I833b0a9f93d6b129529dcda71084c3bff5417bad
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4162927
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Commit-Queue: Dominik Inführ <dinfuehr@chromium.org>
Cr-Commit-Position: refs/heads/main@{#85309}

[add] https://crrev.com/601913ded3a918ddf4db97adbaec292d5e53c4c1/test/mjsunit/shared-memory/mutex-lock-twice.js
[modify] https://crrev.com/601913ded3a918ddf4db97adbaec292d5e53c4c1/src/heap/mark-compact.h
[modify] https://crrev.com/601913ded3a918ddf4db97adbaec292d5e53c4c1/src/heap/mark-compact.cc


### cl...@chromium.org (2023-01-16)

Detailed Report: https://clusterfuzz.com/testcase?key=5843270881181696

Fuzzer: None
Job Type: linux_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  old_entry.IsRegularEntry() in external-pointer-table-inl.h
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85174:85175

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5843270881181696

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### cl...@chromium.org (2023-01-16)

ClusterFuzz testcase 5843270881181696 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_d8_dbg&range=85308:85309

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-16)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-01-16)

[Empty comment from Monorail migration]

### am...@google.com (2023-01-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-01-18)

Congratulations on another one, Zhenghang! The VRP Panel has decided to award you $7,000 for this report + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us -- nice work! 

### am...@chromium.org (2023-01-18)

dear bot, --harmony-struct is enabled by default so this issue is SI-None, please stop changing our SI labels

### am...@google.com (2023-01-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-24)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-28)

Hello, we consider attachments/POCs included with reports to be an integral part of the report (https://g.co/chrome/vrp), so I've undeleted them. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1406729?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40062610)*
