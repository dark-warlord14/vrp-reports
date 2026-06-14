# Security: Out of bounds index in array in function parameters

| Field | Value |
|-------|-------|
| **Issue ID** | [40050612](https://issues.chromium.org/issues/40050612) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Blink>JavaScript>Language |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | ad...@chromium.org |
| **Created** | 2019-11-05 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**  

**Please provide a brief explanation of the security issue.**

The following code crashes the latest d8 using a pointer at 0x414141414141.

class var6 extends Object {  

constructor ( a,b,c,d,e,f,g,h,i,j,k,l,m ) {  

super (3.54484805889626e-310 ) 1 ; // this float is 0x414141414141  

}  

};

What is happening here:  

Examining the crash we see that in AllocateParameterLocals, num\_parameters() is greater than the size of params\_. Causing it to index out of bounds. We can control how far out of bounds by adding more parameters as shown in the crash above.

This bug was introduced by the commit: 10883f561a6edb7f79896598e9b8cebb5c363fa6  

which adds ParseDerivedConstructorBody. ParseDerivedConstructorBody (in src/parsing/parser-base.h) incorrectly parses it by first doing ParseExpression() then ParseStatementListItem. Which allows `super (3.54484805889626e-310 ) 1` to be parsed. However this code fails to preparse (as it should). So it first gets preparsed, fails that, then gets parsed regularly, which succeeds and allocates parameters. But both the preparsing and the parsing each incremented num\_parameters\_ causing it to be too large when allocating parameters.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Chris Salls, Chani Jindal, Jake Corina  

This was found by a fuzzing project from UCSB.

## Attachments

- [bug_41414141.js](attachments/bug_41414141.js) (text/plain, 122 B)

## Timeline

### cl...@chromium.org (2019-11-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6552552797503488.

### cl...@chromium.org (2019-11-05)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Blink>JavaScript>Language]

### cl...@chromium.org (2019-11-05)

Automatically assigning owner based on suspected regression changelist https://chromium.googlesource.com/v8/v8/+/10883f561a6edb7f79896598e9b8cebb5c363fa6 ([hole-check-elimination] Simplest possible hole check elimination).

If this is incorrect, please let us know why and apply the Test-Predator-Wrong-CLs label. If you aren't the correct owner for this issue, please unassign yourself as soon as possible so it can be re-triaged.

### cl...@chromium.org (2019-11-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6552552797503488

Fuzzer: 
Job Type: linux_asan_d8
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x01273fff800a
Crash State:
  v8::internal::Variable::raw_name
  v8::internal::Scope::MustAllocate
  v8::internal::Scope::AllocateVariablesRecursively
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=linux_asan_d8&range=63912:63913

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6552552797503488

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/6552552797503488 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8.git/+/31813fbf61103f6a788bb1c5eec94a0896bd2952

commit 31813fbf61103f6a788bb1c5eec94a0896bd2952
Author: Joshua Litt <joshualitt@chromium.org>
Date: Tue Nov 05 22:22:54 2019

Revert "[hole-check-elimination] Simplest possible hole check elimination"

This reverts commit 10883f561a6edb7f79896598e9b8cebb5c363fa6.

Reason for revert: Causes bytecode mismatch

Bug:chromium:1020538, chromium:1021457

Original change's description:
> [hole-check-elimination] Simplest possible hole check elimination
>
> doc: https://docs.google.com/document/d/1Y9uF3hS2aUrwKU56vGxlvEs_IiGgmWSzau8097Y-XBM/edit
>
> Bug: v8:7427
> Change-Id: Iedd36c146cefff7e6687fdad48d263889c5c8347
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1778902
> Commit-Queue: Ross McIlroy <rmcilroy@chromium.org>
> Reviewed-by: Ross McIlroy <rmcilroy@chromium.org>
> Reviewed-by: Toon Verwaest <verwaest@chromium.org>
> Cr-Commit-Position: refs/heads/master@{#63913}

TBR=rmcilroy@chromium.org,leszeks@chromium.org,verwaest@chromium.org,joshualitt@chromium.org

Bug: v8:7427
Change-Id: Ib4369a3560e929692585c4546435684deae5ee9b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/1899163
Commit-Queue: Joshua Litt <joshualitt@chromium.org>
Reviewed-by: Joshua Litt <joshualitt@chromium.org>
Cr-Commit-Position: refs/heads/master@{#64789}

[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/ast/scopes.cc
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/ast/scopes.h
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/diagnostics/objects-printer.cc
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/interpreter/bytecode-generator.cc
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/objects/scope-info.cc
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/objects/scope-info.h
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/parsing/expression-scope.h
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/parsing/parser-base.h
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/src/parsing/preparse-data.cc
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/test/cctest/interpreter/bytecode_expectations/ClassAndSuperClass.golden
[modify] https://crrev.com/31813fbf61103f6a788bb1c5eec94a0896bd2952/test/cctest/interpreter/bytecode_expectations/SuperCallAndSpread.golden
[delete] https://crrev.com/b6edadc09b13bdd08ea7d3552056c6a5e1527170/test/mjsunit/super_hole_check.mjs


### sh...@chromium.org (2019-11-06)

Setting milestone and target because of Security_Impact=Beta and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-06)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### jo...@chromium.org (2019-11-06)

Has already been reverted.

### cl...@chromium.org (2019-11-06)

ClusterFuzz testcase 6552552797503488 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_d8&range=64788:64789

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-11-06)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-06)

This affects M79, so requesting a merge of the revert.

### sh...@chromium.org (2019-11-06)

This bug requires manual review: Reverts referenced in bugdroid comments after merge request.
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

### go...@chromium.org (2019-11-06)

Revert listed at #5 is not in canary yet, please update bug with canary result tomorrow.

+adetaylor@ for M79 merge review

### jo...@chromium.org (2019-11-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-06)

Seems wise to me.

### go...@chromium.org (2019-11-07)

[Empty comment from Monorail migration]

### jo...@chromium.org (2019-11-07)

The revert has  now landed in v8 branch 7.9

### ad...@chromium.org (2019-11-07)

Looks like we may have slightly jumped the gun on the merge, given that this is still marked as Merge-Review-79.

adetaylor, please advise whether it's OK to leave this merged in the V8 M79 branch.

### ad...@chromium.org (2019-11-07)

That's something for govind@ to comment on but I don't foresee too much trouble raining down on you :)

### go...@chromium.org (2019-11-08)

M79 revert merge is here - https://chromium.googlesource.com/v8/v8.git/+/5d914ab4b93a9e9b99279354d348c24e954b1824.

It is ok for this time, next time please wait for approval before merging to release branches. Thank you.

### ve...@chromium.org (2019-11-08)

[Empty comment from Monorail migration]

### ch...@gmail.com (2019-11-13)

Does this bug qualify for a CVE or bounty? As this is for an academic research project either of those would help in demonstrating our results.

### na...@google.com (2019-11-18)

[Empty comment from Monorail migration]

### na...@google.com (2019-11-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-11-21)

Congrats the Panel decided to reward $3,000 for this report!

### na...@google.com (2019-11-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1021457?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050612)*
