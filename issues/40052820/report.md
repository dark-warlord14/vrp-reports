# Security:  LdaNamedProperty is generated for typed_array["4294967295"], which causes wrong inline cache and OOB access

| Field | Value |
|-------|-------|
| **Issue ID** | [40052820](https://issues.chromium.org/issues/40052820) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript, Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | r3...@gmail.com |
| **Assignee** | jk...@chromium.org |
| **Created** | 2020-07-12 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

See attachment

**VERSION**  

Operating System: Ubuntu 18.04 LTS  

Chromium: 85.0.4183.15  

v8: 8.5.210.8 (3505cf00eb4c59b87f4b5ec9fc702f7935fdffd0)

**REPRODUCTION CASE**

```
const kSize = 4294967296;  
function vuln() {  
        const v22 = new Uint8Array(kSize);  
        return v22["4294967295"];  
}  
  
while (true) {  
        vuln();  
}  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: v8 crash  

Crash State:

# 

# Fatal error in ../../src/objects/lookup.cc, line 924

# Debug check failed: !IsElement(\*holder\_).

# 

# 

# 

#FailureMessage Object: 0x7ffedf7b25b0  

==== C stack trace ===============================

```
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x21) [0x7f5b8a83bc51]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8_libplatform.so(+0x5681a) [0x7f5b8a7c381a]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x26f) [0x7f5b8a8249df]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8_libbase.so(+0x3a32c) [0x7f5b8a82432c]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7f5b8a824a97]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(v8::internal::LookupIterator::GetFieldIndex() const+0x19a) [0x7f5b88f1ac5a]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(v8::internal::LoadIC::ComputeHandler(v8::internal::LookupIterator\*)+0x248e) [0x7f5b88be9a9e]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(v8::internal::LoadIC::UpdateCaches(v8::internal::LookupIterator\*)+0x555) [0x7f5b88be62d5]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(v8::internal::LoadIC::Load(v8::internal::Handle<v8::internal::Object>, v8::internal::Handle<v8::internal::Name>, bool)+0x8e9) [0x7f5b88be5639]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(+0x258254d) [0x7f5b88bf454d]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(v8::internal::Runtime_LoadIC_Miss(int, unsigned long\*, v8::internal::Isolate\*)+0x128) [0x7f5b88bf4048]  
/home/pc/v/v8/d8/v8/out.gn/x64.debug/libv8.so(+0x1abab9f) [0x7f5b8812cb9f]  

```

Received signal 4 ILL\_ILLOPN 7f5b8a838ca1  

Illegal instruction

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: 2019 of Pangu Lab

## Attachments

- [wp.md](attachments/wp.md) (text/plain, 4.4 KB)

## Timeline

### cl...@chromium.org (2020-07-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5085292989579264.

### mm...@google.com (2020-07-13)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2020-07-13)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Runtime]

### cl...@chromium.org (2020-07-13)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/94dd3e992ef52dc72001b1c46bdb50431a89dffa ([v8] Allow for 4GB TypedArrays).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2020-07-13)

Detailed Report: https://clusterfuzz.com/testcase?key=5085292989579264

Fuzzer: 
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: DCHECK failure
Crash Address: 
Crash State:
  !IsElement(*holder_) in lookup.cc
  v8::internal::LookupIterator::GetFieldIndex
  v8::internal::LoadIC::ComputeHandler
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=68423:68424

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5085292989579264

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5085292989579264 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### ki...@chromium.org (2020-07-14)

[Empty comment from Monorail migration]

### mm...@google.com (2020-07-14)

[Empty comment from Monorail migration]

### mm...@google.com (2020-07-14)

[Empty comment from Monorail migration]

### mm...@google.com (2020-07-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-07-14)

[Empty comment from Monorail migration]

### ki...@chromium.org (2020-07-14)

[Empty comment from Monorail migration]

### jk...@chromium.org (2020-07-14)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/c90353e3c7f01aa93e88b474aa21b4ad9abe804d

commit c90353e3c7f01aa93e88b474aa21b4ad9abe804d
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Tue Jul 14 12:09:04 2020

Fix "named" loads for large TypedArray indices

The named LoadIC code was missing a check for "names" that
convert to TypedArray indices. This was flushed out by the
recent bump of the max TypedArray size from 2^32-1 to 2^32.
Named StoreICs had the same bug; fixed here as well.

Bug: v8:4153
Fixed: chromium:1104608
Change-Id: I6bd2552d6ccc238104f92e7b95d19970d4a75dae
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2295606
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Commit-Position: refs/heads/master@{#68840}

[modify] https://crrev.com/c90353e3c7f01aa93e88b474aa21b4ad9abe804d/src/ic/ic.cc
[modify] https://crrev.com/c90353e3c7f01aa93e88b474aa21b4ad9abe804d/test/mjsunit/mjsunit.status
[add] https://crrev.com/c90353e3c7f01aa93e88b474aa21b4ad9abe804d/test/mjsunit/regress/regress-crbug-1104608.js


### jk...@chromium.org (2020-07-14)

Thanks for the report! 

This will need backmerging to M85. Setting a reminder.

FWIW, I haven't been able to reproduce the problem with Chrome 85, because I kept running into allocation failures. Not sure how "reliable" those are though. With the d8 shell I could reproduce the problem: DCHECK failure in Debug mode, OOB access in Release mode.

### cl...@chromium.org (2020-07-14)

ClusterFuzz testcase 5085292989579264 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=68839:68840

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2020-07-14)

[Empty comment from Monorail migration]

### r3...@gmail.com (2020-07-16)

[Comment Deleted]

### r3...@gmail.com (2020-07-16)

I think the primary factor is the memory limit for different computers. Since backing store of TypedArray with size 0x100000000 is always allocated using mmap/VirtualAlloc, whether the allocation is successful largely depends on OS and computer memory. In addition, the reason why it works on d8 is probably the memory used by d8 is less than chromium renderer process, since renderer process also need to store many stuff other than v8.

### jk...@chromium.org (2020-07-16)

#18: Turns out I goofed up my test case (memory was not the issue). I *can* repro in Chrome.

CF says it's fixed (#15) and we have Canary coverage in 86.0.4203.2. Requesting merge.

### [Deleted User] (2020-07-17)

Your change meets the bar and is auto-approved for M85. Please go ahead and merge the CL to branch 4183 (refs/branch-heads/4183) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### be...@chromium.org (2020-07-20)

This has been approved for a merge, please merge ASAP.

### [Deleted User] (2020-07-20)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2020-07-20)

[Empty comment from Monorail migration]

### sr...@google.com (2020-07-20)

Please complete your merges to M85 branch today before 2pm PST so that this change can be included in the Dev Release tomorrow. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-07-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/393f852b992903ed219355e84ef1006fac09c0e6

commit 393f852b992903ed219355e84ef1006fac09c0e6
Author: Jakob Kummerow <jkummerow@chromium.org>
Date: Mon Jul 20 18:48:13 2020

Fix "named" loads for large TypedArray indices

The named LoadIC code was missing a check for "names" that
convert to TypedArray indices. This was flushed out by the
recent bump of the max TypedArray size from 2^32-1 to 2^32.
Named StoreICs had the same bug; fixed here as well.

(cherry picked from commit c90353e3c7f01aa93e88b474aa21b4ad9abe804d)

Bug: v8:4153
Fixed: chromium:1104608
Change-Id: I6bd2552d6ccc238104f92e7b95d19970d4a75dae
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2295606
Reviewed-by: Igor Sheludko <ishell@chromium.org>
Commit-Queue: Jakob Kummerow <jkummerow@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#68840}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2307226
Cr-Commit-Position: refs/branch-heads/8.5@{#26}
Cr-Branched-From: a7f8bc434b35c3122a859f094fa541febd74ec7c-refs/heads/8.5.210@{#1}
Cr-Branched-From: dd58472158b209e36f3f8646e9adfb31ffa61483-refs/heads/master@{#68510}

[modify] https://crrev.com/393f852b992903ed219355e84ef1006fac09c0e6/src/ic/ic.cc
[modify] https://crrev.com/393f852b992903ed219355e84ef1006fac09c0e6/test/mjsunit/mjsunit.status
[add] https://crrev.com/393f852b992903ed219355e84ef1006fac09c0e6/test/mjsunit/regress/regress-crbug-1104608.js


### jk...@chromium.org (2020-07-20)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-07-21)

jkummerow@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations! The VRP panel has awarded $5000 for this report. A member of our finance team will be in touch to arrange payment.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### r3...@gmail.com (2020-07-24)

Thank you very much, the reward is very generous :D

### sa...@google.com (2020-07-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2020-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2020-10-20)

This issue was migrated from crbug.com/chromium/1104608?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>JavaScript, Blink>JavaScript>Runtime]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052820)*
