# Trap in Builtins_InterpreterEntryTrampoline

| Field | Value |
|-------|-------|
| **Issue ID** | [40050810](https://issues.chromium.org/issues/40050810) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ta...@gmail.com |
| **Assignee** | ne...@chromium.org |
| **Created** | 2019-11-27 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36

Steps to reproduce the problem:
The following PoC found by fuzzing crashes both release and debug build of v8 8.0.0 (commit a5376b7e8f647b69184c54462e48e2a4423aff44 on Nov 11th)

PoC:

function opt() {
  var date = new Date();
  for (let i = 0; i < 100; i++) {
    switch (i / date.getMilliseconds()) {
      case 0:
      case date.getMilliseconds() % i:
        break;
    }
  }
}

function main() {
  for (let i = 0; i < 100; i--) {
    opt();
  }
}

main();

What is the expected behavior?

What went wrong?
Run in gdb with the PoC, we get:

Thread 1 "d8" received signal SIGTRAP, Trace/breakpoint trap.
0x00007e8b96d42c4b in ?? ()
(gdb) x/4i $pc - 0x7
   0x7e8b96d42c44:      jne    0x7e8b96d42e78
   0x7e8b96d42c4a:      int3   
=> 0x7e8b96d42c4b:      mov    $0x1,%eax
   0x7e8b96d42c50:      jmpq   0x7e8b96d42c67

Did this work before? N/A 

Chrome version: 78.0.3904.108  Channel: canary
OS Version: 
Flash Version: 

Found by Soyeon Park and Wen Xu from SSLab at Georgia Tech

## Timeline

### cl...@chromium.org (2019-11-27)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5321271667458048.

### pa...@chromium.org (2019-11-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### cl...@chromium.org (2019-11-27)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/6e5671e1cdd33f8f51b2afeab499881a83e52179 ([nojit] Embed InterpreterEntryTrampoline).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-11-27)

Detailed Report: https://clusterfuzz.com/testcase?key=5321271667458048

Fuzzer: 
Job Type: linux_asan_d8_dbg
Platform Id: linux

Crash Type: Trap
Crash Address: 0x000000000000
Crash State:
  Builtins_InterpreterEntryTrampoline
  Builtins_InterpreterEntryTrampoline
  Builtins_JSEntryTrampoline
  
Sanitizer: address (ASAN)

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=57562:57563

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5321271667458048

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5321271667458048 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


### jg...@chromium.org (2019-11-28)

I can repro on ToT. Relevant snippet:

0x4e900082ca8   188  a801           test al,0x1
0x4e900082caa   18a  0f859d020000   jnz 0x4e900082f4d  <+0x42d>
0x4e900082cb0   190  cc             int3l

$rax is expected to contain a heap object but actually contains smi zero.

### jg...@chromium.org (2019-11-28)

Our assumptions fail when the switch variable value is NaN.

### jg...@chromium.org (2019-11-28)

Gotta pass this on since I'm OOO starting now.

### ne...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### ne...@chromium.org (2019-11-28)

[Empty comment from Monorail migration]

### ne...@chromium.org (2019-11-29)

In this example, the bug leads to a controlled abort at runtime. But I could also imagine this to lead to type confusion, hence setting security severity to high.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/3363ddd4b9056d42dc6eb1f342401fddc97dc80a

commit 3363ddd4b9056d42dc6eb1f342401fddc97dc80a
Author: Georg Neis <neis@chromium.org>
Date: Fri Nov 29 11:46:49 2019

[turbofan] Fix simplified lowering of SpeculativeNumberModulus

If the inputs are Unsigned32OrMinusZeroOrNaN and we want to compile for
an Unsigned32 result, we still need to deopt if the RHS is zero (because
that must produce NaN).

Bug: chromium:1028862
Change-Id: Ib5b7cd10f8c4ec9a76b75a2b408729f1ca86ea3e
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1943150
Reviewed-by: Benedikt Meurer <bmeurer@chromium.org>
Reviewed-by: Michael Stanton <mvstanton@chromium.org>
Auto-Submit: Georg Neis <neis@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#65260}

[modify] https://crrev.com/3363ddd4b9056d42dc6eb1f342401fddc97dc80a/src/compiler/simplified-lowering.cc
[add] https://crrev.com/3363ddd4b9056d42dc6eb1f342401fddc97dc80a/test/mjsunit/compiler/regress-1028862.js


### sh...@chromium.org (2019-11-29)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-29)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-11-29)

ClusterFuzz testcase 5321271667458048 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8_dbg&range=65259:65260

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-11-29)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M78. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M79. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-29)

This bug requires manual review: We are only 10 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-11-29)

+adetaylor@ for M79 merge review. 

Note: CL listed at #11 is not yet made it to canary.

### go...@chromium.org (2019-11-30)

+adetaylor@ for M79 merge review this time for sure. 

### ad...@chromium.org (2019-11-30)

A normal high severity security bug, so yes please merge into M79, but only when you are confident of stability.

### go...@chromium.org (2019-11-30)

Please update bug with canary result on Monday morning before we approve merge to M79. 

### sh...@chromium.org (2019-11-30)

[Empty comment from Monorail migration]

### ne...@chromium.org (2019-12-02)

No known issues on Canary.

### go...@chromium.org (2019-12-02)

Approving merge to M79 branch 3945 based on https://crbug.com/chromium/1028862#c22. Please merge ASAP. Thank you.

### ne...@chromium.org (2019-12-02)

Merged to v8 7.9 as https://chromium.googlesource.com/v8/v8/+/06c5d6e6a7f843c53b86d5b0776ea64782a2948a

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-12-03)

We're not planning any further M78 releases. So rejecting merge to M78. 

### go...@chromium.org (2019-12-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $5,000 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### ta...@gmail.com (2019-12-11)

Could you change the credit of the cve in the release blog to Soyeon Park and Wen Xu at SSLab, Georgia Tech please, thanks a lot!

### ad...@chromium.org (2019-12-11)

Done, thanks for the update!

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1028862?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050810)*
