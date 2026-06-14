# OOB read/write in v8::internal::ElementsAccessorBase<v8::internal::FastHoleyDoubleElementsAccessor

| Field | Value |
|-------|-------|
| **Issue ID** | [40052161](https://issues.chromium.org/issues/40052161) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Compiler |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | te...@chromium.org |
| **Created** | 2020-04-30 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS** :  

The attached oob.html file uses a JIT vulnerability in v8 to trigger a type confusion and change the length of an array. This leads to out of bounds read and write, which can be turned into a full renderer exploit.

The attached files apply to Chrome 81 and V8 8.1.307. Related code was changed so it doesn't trigger on Canary. Although the buggy code still remains.

Our understanding of the bug:  

In src/compiler/dead-code-eliminiation.cc in ReduceDeoptimizeOrReturnOrTerminateOrTailCall, it will replace Terminate with Throw.  

That replacement seems to be invalid as it can result in multiple control nodes attached to the same node in the effect-control-linearization phase. This can be seen in the minimized poc which triggers the following debug check.

# Fatal error in ../../v8/src/compiler/schedule.cc, line 297

# Debug check failed: BasicBlock::kNone == block->control() (none vs. throw).

This bug leads to an interesting primitive where instructions will be scheduled incorrectly. In the attached exploit we use this primitive to place a CheckMaps after arg1.val = -1.  

This will let us write -1 over an array length, as the write will occur before the CheckMaps.

The attached poc changes an array length to be -1 and uses that to read and write out of bounds, demonstrating exploitability.

CREDIT INFORMATION  

Reporter credit: Chris Salls and Jake Corina of Seaside Security, Chani Jindal of Shellphish

## Attachments

- [bug34_min.js](attachments/bug34_min.js) (text/plain, 441 B)
- [oob.html](attachments/oob.html) (text/plain, 1.2 KB)

## Timeline

### cl...@chromium.org (2020-04-30)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5633509006311424.

### cl...@chromium.org (2020-04-30)

Testcase 5633509006311424 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5633509006311424.

### ch...@gmail.com (2020-05-01)

This trigger for the bug doesn’t work on canary as some related code has changed so I’d guess that’s why clusterfuzz isn’t able to reproduce. It still works on 81/stable though. 

### pa...@chromium.org (2020-05-01)

Hmm, I tried to tell ClusterFuzz to use the revision at which M81 was branched. The Overview section of the CF report doesn't mention the branch, though. Perhaps I was holding it wrong. I'll try again.

### cl...@chromium.org (2020-05-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5129189383012352.

### cl...@chromium.org (2020-05-01)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5642219090935808.

### in...@chromium.org (2020-05-02)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### in...@chromium.org (2020-05-02)

Applied labels manually since testcase is flaky on ClusterFuzz.

### in...@chromium.org (2020-05-02)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-05-02)

ClusterFuzz testcase 5642219090935808 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-05-02)

Detailed Report: https://clusterfuzz.com/testcase?key=5642219090935808

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x7ec3124a7b28
Crash State:
  v8::internal::ElementsAccessorBase<v8::internal::FastHoleyDoubleElementsAccessor
  v8::internal::LookupIterator::State v8::internal::LookupIterator::LookupInRegula
  void v8::internal::LookupIterator::Start<true>
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=737169

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5642219090935808

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5642219090935808 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### [Deleted User] (2020-05-02)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-02)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@chromium.org (2020-05-04)

Georg, PTAL at this TF issue.

### ne...@chromium.org (2020-05-04)

[Empty comment from Monorail migration]

[Monorail components: -Blink>JavaScript Blink>JavaScript>Compiler]

### ne...@chromium.org (2020-05-04)

Thanks for the report. Tobias, could you take this one?

### ch...@gmail.com (2020-05-04)

Hi, I was wondering what's required for a "functional exploit" to earn the full bug bounty? This hard part for this bug is figuring out how to achieve oob r/w on an array.

### te...@chromium.org (2020-05-05)

Thanks a lot for this report, a fix is in flight.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/d4ddf645c3ca81ed12caf0dfa398716def23e1b7

commit d4ddf645c3ca81ed12caf0dfa398716def23e1b7
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Tue May 05 14:07:13 2020

[turbofan] fix bug in DeadCodeElimination

Bug: chromium:1076708
Change-Id: I88a5eae0e562e32f1915deff3c4150ec4be14c6c
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2181266
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Georg Neis <neis@chromium.org>
Auto-Submit: Tobias Tebbi <tebbi@chromium.org>
Reviewed-by: Georg Neis <neis@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67564}

[modify] https://crrev.com/d4ddf645c3ca81ed12caf0dfa398716def23e1b7/src/compiler/dead-code-elimination.cc


### te...@chromium.org (2020-05-05)

Fixed on ToT, requesting merge once we reach canary coverage.

### [Deleted User] (2020-05-05)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2020-05-05)

1. Yes, it's a security bug leading to renderer corruption and the fix is very small and straightforward.
2. https://chromium-review.googlesource.com/c/v8/v8/+/2181266
3. The provided repro doesn't reproduce on ToT, but the fix has been verified on M81 and we're certain that it is equally exploitable on ToT, it's just difficult to construct a repro.
4. The bug was undetected for a very long time.
5. No
6. -

### pb...@google.com (2020-05-05)

+adetaylor(Security TPM) for M81 and M83 merge assessment.

### ad...@google.com (2020-05-05)

Approving merge to M83, branch 4103, but please wait a couple of days to look for problems on Canary first.

This is just a little too late for the final scheduled M81 refresh. I'll keep the Merge-Request-81 label just in case we end up doing an unscheduled respin, but it's most likely that this will be released with the initial version of M83.

### be...@chromium.org (2020-05-05)

This has been approved for a merge, please merge ASAP. Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/de2c0a3b2bf9922d72556a277ea2d5b648471fa6

commit de2c0a3b2bf9922d72556a277ea2d5b648471fa6
Author: Georg Neis <neis@chromium.org>
Date: Tue May 05 19:34:03 2020

[turbofan] Turn some DCHECKs into CHECKs in Schedule methods

Bug: chromium:1076708
Change-Id: I7f065791310606e11fe89936a36f0fe7cb0d38e7
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2182639
Auto-Submit: Georg Neis <neis@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/heads/master@{#67576}

[modify] https://crrev.com/de2c0a3b2bf9922d72556a277ea2d5b648471fa6/src/compiler/schedule.cc


### [Deleted User] (2020-05-06)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/fb9aa71a2d8a41a73b0cf58ac132f702ab17a2e5

commit fb9aa71a2d8a41a73b0cf58ac132f702ab17a2e5
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Thu May 07 16:15:36 2020

Merged: [turbofan] fix bug in DeadCodeElimination

Revision: d4ddf645c3ca81ed12caf0dfa398716def23e1b7

BUG=chromium:1076708
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

TBR: neis@chromium.org
Change-Id: I8acdb4715a6786d954d5be49b909b136b4067969
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2187624
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Commit-Position: refs/branch-heads/8.3@{#18}
Cr-Branched-From: 1668abddd8147c49c8f2f90b78dc2701f3794a30-refs/heads/8.3.110@{#1}
Cr-Branched-From: 04a7a680a2838e1789f277495181e709e14a17ba-refs/heads/master@{#66926}

[modify] https://crrev.com/fb9aa71a2d8a41a73b0cf58ac132f702ab17a2e5/src/compiler/dead-code-elimination.cc


### te...@chromium.org (2020-05-07)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-11)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-14)

Congrats! The Panel decided to award $7,500 for this report. 

In response to your earlier question about how to get the reward amount for a functional exploit  you need to to include the extra step of including code execution. For example by demonstrating the function you are doing the read/write on and the ASLR bypass on. 

### ch...@gmail.com (2020-05-14)

Thanks for the award!

### na...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-05-15)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-05-18)

[Empty comment from Monorail migration]

### ke...@google.com (2020-05-18)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-05-19)

Hey V8 folks, how feasible would it be to merge this to the M81 V8 branch? The reason for asking this is that Chrome OS will likely do an extra respin of M81 (because the initial M83 Chrome OS release looks likely to be delayed) and therefore we'd like to have this fix in M81. I would attempt the cherry-pick myself but unsure how the V8 repo works.

### ne...@chromium.org (2020-05-19)

It's totally feasible, in fact tebbi@ requested a merge to 81, see the label.

### ne...@chromium.org (2020-05-19)

+vahl for help with merging to Chrome OS M81.

### va...@chromium.org (2020-05-19)

Please cherry pick the change into branch "refs/branch-heads/8.1" and check if the 8.1 builds and tests are green at https://ci.chromium.org/p/v8/builders/ci/V8%20Presubmit%20-%20previous%20branch/8

ChromeOS need to validate the build further 

### va...@chromium.org (2020-05-19)

[Empty comment from Monorail migration]

### jo...@chromium.org (2020-05-20)

Cherry-pick at https://chromium-review.googlesource.com/c/v8/v8/+/2208932.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/2eb04d82cc353dd0b58bbffd21ee01d498ad506c

commit 2eb04d82cc353dd0b58bbffd21ee01d498ad506c
Author: Tobias Tebbi <tebbi@chromium.org>
Date: Wed May 20 07:42:56 2020

Merged: [turbofan] fix bug in DeadCodeElimination

Revision: d4ddf645c3ca81ed12caf0dfa398716def23e1b7

BUG=chromium:1076708
NOTRY=true
NOPRESUBMIT=true
NOTREECHECKS=true

(cherry picked from commit fb9aa71a2d8a41a73b0cf58ac132f702ab17a2e5)

TBR: neis@chromium.org
Change-Id: I8acdb4715a6786d954d5be49b909b136b4067969
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2187624
Reviewed-by: Tobias Tebbi <tebbi@chromium.org>
Commit-Queue: Tobias Tebbi <tebbi@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/8.3@{#18}
Cr-Original-Branched-From: 1668abddd8147c49c8f2f90b78dc2701f3794a30-refs/heads/8.3.110@{#1}
Cr-Original-Branched-From: 04a7a680a2838e1789f277495181e709e14a17ba-refs/heads/master@{#66926}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2208932
Cr-Commit-Position: refs/branch-heads/8.1@{#67}
Cr-Branched-From: a4dcd39d521d14c4b1cac020812e44ee04a7f244-refs/heads/8.1.307@{#1}
Cr-Branched-From: f22c213304ec3542df87019aed0909b7dafeaa93-refs/heads/master@{#66031}

[modify] https://crrev.com/2eb04d82cc353dd0b58bbffd21ee01d498ad506c/src/compiler/dead-code-elimination.cc


### jo...@chromium.org (2020-05-20)

Thanks Tobias!

### ad...@chromium.org (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-25)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ne...@chromium.org (2020-05-26)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1076708?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### su...@gmail.com (2024-06-02)

deleted

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052161)*
