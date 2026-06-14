# Signal SIGSEGV in v

| Field | Value |
|-------|-------|
| **Issue ID** | [359729268](https://issues.chromium.org/issues/359729268) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>API, Blink>JavaScript>Runtime |
| **Platforms** | Linux |
| **Reporter** | ki...@gmail.com |
| **Assignee** | ha...@intel.com |
| **Created** | 2024-08-14 |
| **Bounty** | $8,000.00 |

## Description

VULNERABILITY DETAILS
## INTRODUCE
After bisect, it was determined that following commit caused this problem.

- Commit Info
    - Version: 95402
    - link: https://crrev.com/17d7d98b92926852a3e3ba90aba17b80ef869512 
- Commit Message

```
commit 17d7d98b92926852a3e3ba90aba17b80ef869512
Author: Hao Xu <hao.a.xu@intel.com>
Date:   Fri Jul 19 16:54:03 2024 +0800

    Reland "Support GetEnumeratedKeyedProperty bytecode in Maglev/Turbofan"
    
    This is a reland of commit 19cf1a317f65f0b94eba7082400cfd2608e0df29
    
    We should reset current_for_in_state.enum_cache_indices on resumable
    loop headers. Because it is not stored in any local register, we will
    lose this value in the loop body.
    
    Original change's description:
    > Support GetEnumeratedKeyedProperty bytecode in Maglev/Turbofan
    >
    > Bug: v8:14245
    > Change-Id: I1e84623b45969b9efee02e5469b7a3ecf747972a
    > Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5634288
    > Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    > Commit-Queue: Hao A Xu <hao.a.xu@intel.com>
    > Cr-Commit-Position: refs/heads/main@{#94956}
    
    Bug: v8:14245
    Change-Id: Iaf98f657056d925367b11bc53be249f7eadff31a
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5723307
    Commit-Queue: Hao A Xu <hao.a.xu@intel.com>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95402}

```

## CRASH LOG
- Debug output

```bash
# CMD: /tmp/d8-linux-debug-v8-component-95637/d8 --allow-natives-syntax --fuzzing --always-turbofan poc.js
# OUTPUT ==============================================================
Received signal 11 SEGV_MAPERR ffffffffffffffff

```

## Other
Please note to include the flags `--allow-natives-syntax --fuzzing --always-turbofan` for clusterfuzz classification.

VERSION
Tested on v8 version: 12.9.0 - 12.9.0

REPRODUCTION CASE
1. Download debug v8 from: gs://v8-asan/linux-debug/d8-linux-debug-v8-component-95637.zip
2. Run: `d8 --allow-natives-syntax --fuzzing --always-turbofan poc.js`

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab

CREDIT INFORMATION
Reporter credit: Zhenghang Xiao (@Kipreyyy)  

## Attachments

- [poc.js](attachments/poc.js) (text/javascript, 344 B)

## Timeline

### cl...@appspot.gserviceaccount.com (2024-08-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5261376777814016.

### 24...@project.gserviceaccount.com (2024-08-14)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the hotlistid:4801165.

### 24...@project.gserviceaccount.com (2024-08-14)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/17d7d98b92926852a3e3ba90aba17b80ef869512 (Reland "Support GetEnumeratedKeyedProperty bytecode in Maglev/Turbofan"

This is a reland of commit 19cf1a317f65f0b94eba7082400cfd2608e0df29

We should reset current_for_in_state.enum_cache_indices on resumable
loop headers. Because it is not stored in any local register, we will
lose this value in the loop body.

Original change's description:
> Support GetEnumeratedKeyedProperty bytecode in Maglev/Turbofan
>
> Bug: v8:14245
> Change-Id: I1e84623b45969b9efee02e5469b7a3ecf747972a
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5634288
> Reviewed-by: Leszek Swirski <leszeks@chromium.org>
> Commit-Queue: Hao A Xu <hao.a.xu@intel.com>
> Cr-Commit-Position: refs/heads/main@{#94956}

Bug: v8:14245
Change-Id: Iaf98f657056d925367b11bc53be249f7eadff31a
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5723307
Commit-Queue: Hao A Xu <hao.a.xu@intel.com>
Reviewed-by: Leszek Swirski <leszeks@chromium.org>
Cr-Commit-Position: refs/heads/main@{#95402}
).

If this is incorrect, please let us know why and apply the hotlistid:5433122. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### 24...@project.gserviceaccount.com (2024-08-14)

Detailed Report: https://clusterfuzz.com/testcase?key=5261376777814016

Fuzzer: None
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0xffffffffffffffff
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  Builtins_JSEntry
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95401:95402

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5261376777814016

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### ki...@gmail.com (2024-08-14)

Please CC [leszeks@chromium.org](mailto:leszeks@chromium.org) to take a look this issue

### ha...@intel.com (2024-08-15)

@leszek I can reproduce this issue, and it seems the reason is that we don't trigger deoptimization as expected. In the graph building phase it looks fine, so I need some time to investigate this issue.
I've created a revert of the CL (<https://chromium-review.googlesource.com/c/v8/v8/+/5788840>), could you please take a look?

### pe...@google.com (2024-08-15)

Setting milestone because of s2 severity.

### pe...@google.com (2024-08-15)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security Impact hotlist or the Severity field, and remove the ReleaseBlock hotlist.

### pe...@google.com (2024-08-15)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ha...@intel.com (2024-08-16)

Thanks for reporting this issue. I've identified the cause and submitted a CL to fix it. @leszek Please take a look.
<https://chromium-review.googlesource.com/c/v8/v8/+/5788840>

### ap...@google.com (2024-08-16)

Project: v8/v8
Branch: main

commit e0a1822435cb8c0a22fa0e6b7ff84212141e1988
Author: Hao Xu <hao.a.xu@intel.com>
Date:   Fri Aug 16 16:09:37 2024

    [bugfix] Fix incorrect use of CheckHeapObject node in Turbofan
    
    The node should have a value output.
    
    Bug: chromium:359729268
    Change-Id: I635545dec51ddefb1f56793d4f616956cafd41a7
    Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/5788840
    Commit-Queue: Hao A Xu <hao.a.xu@intel.com>
    Reviewed-by: Leszek Swirski <leszeks@chromium.org>
    Commit-Queue: Leszek Swirski <leszeks@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#95665}

M       src/compiler/js-native-context-specialization.cc
A       test/mjsunit/compiler/regress-359729268.js

https://chromium-review.googlesource.com/5788840


### 24...@project.gserviceaccount.com (2024-08-17)

ClusterFuzz testcase 5261376777814016 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=95664:95665

If this is incorrect, please add the hotlistid:5433040 and re-open the issue.

### pe...@google.com (2024-08-21)

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M129. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
**Merge approved:** your change passed merge requirements and is auto-approved for M129. Please go ahead and merge the CL to branch 6668 (refs/branch-heads/6668) manually. Please contact milestone owner if you have questions.
Merge instructions: <https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/merge_request.md>
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), srinivassista (Desktop)
Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [129].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### sp...@google.com (2024-08-21)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $8000.00 for this report.

Rationale for this decision:
$7,000 for report of memory corruption in a sandboxed process + $1,000 bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-08-22)

Congratulations Zhenghang! Thank you for your efforts and reporting this issue to us -- nice work!

### le...@chromium.org (2024-08-22)

Already in 12.9.

### pe...@google.com (2024-11-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/359729268)*
