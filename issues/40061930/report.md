# Turbofan-Optimization Bug: "Check failed: IsBigInt()"

| Field | Value |
|-------|-------|
| **Issue ID** | [40061930](https://issues.chromium.org/issues/40061930) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | kw...@gmail.com |
| **Assignee** | pa...@google.com |
| **Created** | 2022-11-28 |
| **Bounty** | $7,000.00 |

## Description

**Steps to reproduce the problem:**  

Run the below 'poc.js' on the release build of the v8-11.0.109.

// poc.js  

function opt() {  

function aux(a, b) {  

if (b) {  

b >> a;  

} else {  

let c = 0;  

while (c < 7) {  

c++;  

}  

}  

}  

let p = Promise;  

++p;  

aux(1n, 1n);  

aux(1n, p);  

return aux("number", p);  

}

for (let i = 0; i < 10000; i++) {  

opt();  

}  

opt();

**Problem Description:**  

It yields the below crash.

# 

# Fatal error in , line 0

# Check failed: IsBigInt().

# 

# 

# 

#FailureMessage Object: 0x7f610585f250

Here is the stack trace collected from the debug build.  

==== C stack trace ===============================

```
d8s/11.0.109d/libv8_libbase.so(v8::base::debug::StackTrace::StackTrace()+0x1e) [0x7f8aca20567e]  
d8s/11.0.109d/libv8_libplatform.so(+0x4b36d) [0x7f8aca15b36d]  
d8s/11.0.109d/libv8_libbase.so(V8_Fatal(char const\*, int, char const\*, ...)+0x16f) [0x7f8aca1d3d3f]  
d8s/11.0.109d/libv8_libbase.so(+0x567cc) [0x7f8aca1d37cc]  
d8s/11.0.109d/libv8_libbase.so(V8_Dcheck(char const\*, int, char const\*)+0x27) [0x7f8aca1d3df7]  
d8s/11.0.109d/libv8.so(v8::internal::compiler::ObjectRef::AsBigInt() const+0x48) [0x7f8acedc8a88]  
11.0.109d/libv8.so(void v8::internal::compiler::RepresentationSelector::VisitNode<(v8::internal::compiler::Phase)0>(v8::internal::compiler::Node\*, v8::internal::compiler::Truncation, v8::internal::compiler::SimplifiedLowering\*)+0x57c4) [0x7f8acf102124]  

```

**Additional Comments:**

**Chrome version:** Channel:Not sure

**OS:** Linux

## Timeline

### [Deleted User] (2022-11-28)

[Empty comment from Monorail migration]

### kw...@gmail.com (2022-11-28)

Can anyone erase the directory path in the problem description? I don't want to expose that information, but seems I can't edit the report.

### ct...@chromium.org (2022-11-28)

[Description Changed]

### ct...@chromium.org (2022-11-28)

Thanks for the report. I've edited the issue description to strip out the path information. I think the original description may still be accessible to people with EditIssue permissions though.

### cl...@chromium.org (2022-11-29)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5114021624872960.

### cl...@chromium.org (2022-11-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-11-29)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Compiler]

### cl...@chromium.org (2022-11-29)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/2690e2e3a39f6c1325dae0743682c714cbbc98db ([turbofan] Support BigInt shift operations).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2022-11-29)

Detailed Report: https://clusterfuzz.com/testcase?key=5114021624872960

Fuzzer: None
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: CHECK failure
Crash Address: 
Crash State:
  IsBigInt()
  v8::internal::compiler::BigIntRef::BigIntRef
  v8::internal::compiler::ObjectRef::AsBigInt
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=84395:84396

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5114021624872960

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### pa...@google.com (2022-11-29)

Thanks for the report. The bug can be reproduced when the rhs of a big shift operation is a heap constant but not a bigint and the result of the shift operation is truncated (or unused). We should check if the heap constant is a bigint. Otherwise, it is unsafe to cast it to BigInt.

### ca...@chromium.org (2022-11-30)

Setting severity high to match other similar v8 bugs

### [Deleted User] (2022-11-30)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-30)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@google.com (2022-11-30)

The regression is found in M110 instead of M109.

### ca...@chromium.org (2022-11-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-01)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/90fe7dc9ce484a4f2bae35c7aef7af0c06a7b799

commit 90fe7dc9ce484a4f2bae35c7aef7af0c06a7b799
Author: Qifan Pan <panq@google.com>
Date: Wed Nov 30 11:38:48 2022

[turbofan] Fix BigInt shift operations

This CL fixed missing instance type checks for constant shift
amounts and corrected the use info for the lhs.

Bug: chromium:1393865, v8:9407
Change-Id: Id6e65f4e26a0436960b12196f29663429876398b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4061075
Commit-Queue: Qifan Pan <panq@google.com>
Reviewed-by: Nico Hartmann <nicohartmann@chromium.org>
Cr-Commit-Position: refs/heads/main@{#84596}

[modify] https://crrev.com/90fe7dc9ce484a4f2bae35c7aef7af0c06a7b799/src/compiler/representation-change.cc
[modify] https://crrev.com/90fe7dc9ce484a4f2bae35c7aef7af0c06a7b799/src/compiler/simplified-lowering.cc
[modify] https://crrev.com/90fe7dc9ce484a4f2bae35c7aef7af0c06a7b799/test/cctest/compiler/test-representation-change.cc
[add] https://crrev.com/90fe7dc9ce484a4f2bae35c7aef7af0c06a7b799/test/mjsunit/regress/regress-1393865.js


### cl...@chromium.org (2022-12-01)

ClusterFuzz testcase 5114021624872960 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=84595:84596

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-12-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-12-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-12-09)

Congratulations! The VRP Panel has decided to award you $7,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### kw...@gmail.com (2022-12-09)

Thanks a lot.

### am...@google.com (2022-12-10)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-17)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M110. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge approved: your change passed merge requirements and is auto-approved for M110. Please go ahead and merge the CL to branch 5481 (refs/branch-heads/5481) manually. Please contact milestone owner if you have questions.
Merge instructions: https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md
Owners: govind (Android), harrysouders (iOS), ceb (ChromeOS), danielyip (Desktop)

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pa...@google.com (2022-12-19)

The fix is already in M110. Nothing needs to be backmerged.

### am...@chromium.org (2022-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-09)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1393865?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061930)*
