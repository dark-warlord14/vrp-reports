# Security: SQLite CVE-2019-19926

| Field | Value |
|-------|-------|
| **Issue ID** | [40051261](https://issues.chromium.org/issues/40051261) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-19880, CVE-2019-19926 |
| **Reporter** | ri...@sap.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2020-01-16 |
| **Bounty** | $500.00 |

## Description

In https://crbug.com/chromium/1038863 richard.lorenz@sap.com reports:

> There was one more CVE opened for SQLite saying that the fix for CVE-2019-19880 is incomplete and does not fix the issue at another spot. It seems that in /src/select.c (https://crrev.com/c9b98f55e822079f00266d0118a004be49e1fb89/third_party/sqlite/patched/src/select.c(81.0.4022.0)
) line 2807 the following statement is missing:
>
>     if( pParse->nErr ) goto multi_select_end;
>
> see CVE: https://nvd.nist.gov/vuln/detail/CVE-2019-19926
> see SQLite Git issue: https://github.com/sqlite/sqlite/commit/8428b3b437569338a9d1e10c4cd8154acbe33089

Raising this crbug to ensure we've got that fix as appropriate.

https://crbug.com/chromium/1040488 says to take this new fix into ChromeOS, but I don't see a note of it for Chrome browser yet.

## Timeline

### ad...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### ct...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-01-16)

I'll take a look. The fossil link for the fix is here: https://sqlite.org/src/info/cba2a2a44cdf138a629109bb0ad088ed4ef67fc66bed3e0373554681a39615d2

### hu...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-01-16)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b

commit 4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Jan 17 19:15:35 2020

sqlite: Backport bugfixes.

Bug: 1042145, 1042578, 1042700
Change-Id: If611c01b0b4e507376d187292809d50b9c786932
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2006427
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#732953}

[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patched/src/select.c
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patched/test/join.test
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0001-Don-t-allow-shadow-tables-to-be-dropped-in-defensive.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0002-Improve-shadow-table-corruption-detection-in-fts3.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0003-Shadow-Table-Corruption-Detection-improvements-in-ft.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0004-Remove-reachable-NEVER-in-fts3.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0005-Better-corruption-detection-in-fts3.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0006-Detect-Prevent-infinite-recursion.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0007-Improve-corruption-detection-in-fts4.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0008-Further-improve-corruption-detection-in-fts3.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0009-Make-sure-WITH-stack-is-disabled-after-error.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0010-Avoid-zero-offset.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0011-Avoid-zero-offset-of-nullptr.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0012-Fix-buffer-overread.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0013-Fix-UB-warning.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0014-Avoid-temp-trigger-crash.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0015-Fix-fts3-integer-overflows.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0016-Avoid-infinite-recursion-in-ALTER-TABLE-code.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0017-Add-restrictions-on-shadow-table-changes-in-defensiv.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0018-Avoid-ambiguous-true-and-false-return.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0019-Fix-fts3-UB-uint64.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0020-Avoid-large-memory-alloc-for-corrupt-record.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0021-Avoid-invalid-pointer-dereference-in-ORDER-BY.patch
[modify] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0022-Fix-zipfile-extension-INSERT-with-NULL-pathname.patch
[add] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0023-Do-not-allow-constant-propagation-optimization-to-ap.patch
[add] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0024-Back-away-from-LEFT-JOIN-optimization.patch
[add] https://crrev.com/4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b/third_party/sqlite/patches/0025-Abort-early-in-sqlite3WindowRewrite.patch


### hu...@chromium.org (2020-01-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-22)

Requesting merge to stable M79 because latest trunk commit (732953) appears to be after stable branch point (706915).

Requesting merge to beta M80 because latest trunk commit (732953) appears to be after beta branch point (722274).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2020-01-22)

This bug requires manual review: We are only 12 days from stable.
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
Owners: govind@(Android), Kariahda@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-01-22)

huangdarwin@ pls help answer the questions in https://crbug.com/chromium/1042700#c11 for merge review. 

+adetaylor@  to help review as well

### ad...@chromium.org (2020-01-22)

Yes, we should merge unless it's believed to be a notably risky fix.

### sr...@google.com (2020-01-23)

friendly ping huangdarwin@ pls help update the bug with info for merge review.

### hu...@chromium.org (2020-01-23)

Re: https://crbug.com/chromium/1042700#c13 and 14
Sorry for the delay. We should be good to merge. I don't think the fix was notably risky.

Re: https://crbug.com/chromium/1042700#c11,
1. Yes.
2. https://crrev.com/c/2018244
3. Yes
4. Security bugs discovered after branch
5. no
6. n/a

### sr...@google.com (2020-01-24)

Merge approved for M80 branch:3987 , pls merge your changes asap

### sr...@google.com (2020-01-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c446806eabadfef12f225b9ea1a7720d966ac1de

commit c446806eabadfef12f225b9ea1a7720d966ac1de
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Jan 24 20:41:52 2020

sqlite: Backport bugfixes (M80).

(cherry picked from commit 4a9937c9bbbbe99b9c1ecd6b824cb26b2669177b)

Bug: 1042145, 1042578, 1042700
Change-Id: If611c01b0b4e507376d187292809d50b9c786932
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2006427
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#732953}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2018244
Cr-Commit-Position: refs/branch-heads/3987@{#705}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patched/src/select.c
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patched/test/join.test
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0001-Don-t-allow-shadow-tables-to-be-dropped-in-defensive.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0002-Improve-shadow-table-corruption-detection-in-fts3.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0003-Shadow-Table-Corruption-Detection-improvements-in-ft.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0004-Remove-reachable-NEVER-in-fts3.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0005-Better-corruption-detection-in-fts3.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0006-Detect-Prevent-infinite-recursion.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0007-Improve-corruption-detection-in-fts4.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0008-Further-improve-corruption-detection-in-fts3.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0009-Make-sure-WITH-stack-is-disabled-after-error.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0010-Avoid-zero-offset.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0011-Avoid-zero-offset-of-nullptr.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0012-Fix-buffer-overread.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0013-Fix-UB-warning.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0014-Avoid-temp-trigger-crash.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0015-Fix-fts3-integer-overflows.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0016-Avoid-infinite-recursion-in-ALTER-TABLE-code.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0017-Add-restrictions-on-shadow-table-changes-in-defensiv.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0018-Avoid-ambiguous-true-and-false-return.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0019-Fix-fts3-UB-uint64.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0020-Avoid-large-memory-alloc-for-corrupt-record.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0021-Avoid-invalid-pointer-dereference-in-ORDER-BY.patch
[modify] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0022-Fix-zipfile-extension-INSERT-with-NULL-pathname.patch
[add] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0023-Do-not-allow-constant-propagation-optimization-to-ap.patch
[add] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0024-Back-away-from-LEFT-JOIN-optimization.patch
[add] https://crrev.com/c446806eabadfef12f225b9ea1a7720d966ac1de/third_party/sqlite/patches/0025-Abort-early-in-sqlite3WindowRewrite.patch


### na...@google.com (2020-01-27)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-01-29)

Rejecting merge to M79 as we're not planning any further M79 release.

### na...@google.com (2020-01-30)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-30)

Congrats! The Panel decided to award $500 for this report!

### na...@google.com (2020-01-30)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-02)

[Empty comment from Monorail migration]

### ad...@google.com (2020-02-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-04-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### is...@google.com (2020-09-03)

This issue was migrated from crbug.com/chromium/1042700?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051261)*
