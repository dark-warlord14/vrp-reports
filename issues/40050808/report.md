# sqlite3_shadow_table_fuzzer: Heap-buffer-overflow in sqlite3Fts3GetVarint

| Field | Value |
|-------|-------|
| **Issue ID** | [40050808](https://issues.chromium.org/issues/40050808) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | cl...@chromium.org |
| **Assignee** | hu...@chromium.org |
| **Created** | 2019-11-26 |
| **Bounty** | $3,000.00 |

## Description

Detailed Report: https://clusterfuzz.com/testcase?key=5101132481167360

Fuzzing Engine: libFuzzer
Fuzz Target: sqlite3_shadow_table_fuzzer
Job Type: libfuzzer_chrome_asan
Platform Id: linux

Crash Type: Heap-buffer-overflow READ 1
Crash Address: 0x602000002b4f
Crash State:
  sqlite3Fts3GetVarint
  fts3IncrmergeHintPop
  sqlite3Fts3Incrmerge
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Regressed: https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=719104:719109

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5101132481167360

Issue filed automatically.

See https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/reproducing.md for instructions on reproducing this bug locally.

## Timeline

### cl...@chromium.org (2019-11-26)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Storage]

### cl...@chromium.org (2019-11-26)

Automatically adding ccs based on OWNERS file / target commit history.

If this is incorrect, please add the ClusterFuzz-Wrong label.

### in...@chromium.org (2019-11-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-11-27)

Setting milestone and target because of Security_Impact=Head and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-27)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-27)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2019-11-29)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-02)

Adding appropriate labels for the external fuzzer contribution.

### mm...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

huangdarwin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2019-12-13)

Dr. Hipp and Daniel, please take a look? Test case and stack trace below:

Test Case:

CREATE VIRTUAL TABLE f USING fts3(a,b);
CREATE TABLE 'f_stat'(id INTEGER PRIMARY KEY, value BLOB);
INSERT INTO f_stat VALUES (1,x'00');
INSERT INTO f(f) VALUES ('merge=97,250');

========================================================================================================

Stack Trace:

==1620011==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000002b4f at pc 0x7f9f6aede241 bp 0x7fff56ce5f50 sp 0x7fff56ce5f48
READ of size 1 at 0x602000002b4f thread T0
    #0 0x7f9f6aede240 in sqlite3Fts3GetVarint third_party/sqlite/amalgamation/sqlite3.c:161861:3
    #1 0x7f9f6af126de in fts3IncrmergeHintPop third_party/sqlite/amalgamation/sqlite3.c:176498:8
    #2 0x7f9f6af1106c in sqlite3Fts3Incrmerge third_party/sqlite/amalgamation/sqlite3.c:176567:12
    #3 0x7f9f6af088ad in fts3DoIncrmerge third_party/sqlite/amalgamation/sqlite3.c:176715:12
    #4 0x7f9f6af05496 in fts3SpecialInsert third_party/sqlite/amalgamation/sqlite3.c:177008:10
    #5 0x7f9f6af04920 in sqlite3Fts3UpdateMethod third_party/sqlite/amalgamation/sqlite3.c:177265:10
    #6 0x7f9f6aeeb6e0 in fts3UpdateMethod third_party/sqlite/amalgamation/sqlite3.c:164952:10
    #7 0x7f9f6adaf061 in sqlite3VdbeExec third_party/sqlite/amalgamation/sqlite3.c:91316:10
    #8 0x7f9f6ad3bab2 in sqlite3Step third_party/sqlite/amalgamation/sqlite3.c:82287:10
    #9 0x7f9f6ad31527 in sqlite3_step third_party/sqlite/amalgamation/sqlite3.c:82352:16
    #10 0x7f9f6ad4526c in sqlite3_exec third_party/sqlite/amalgamation/sqlite3.c:119934:12
    #11 0x564f315c2f58 in RunSqlQuery(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&, int*) third_party/sqlite/fuzz/shadow_table_fuzzer.cc:106:3

==1620011==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000002b4f at pc 0x7f9f6aede241 bp 0x7fff56ce5f50 sp 0x7fff56ce5f48
READ of size 1 at 0x602000002b4f thread T0
    #0 0x7f9f6aede240 in sqlite3Fts3GetVarint third_party/sqlite/amalgamation/sqlite3.c:161861:3
    #1 0x7f9f6af126de in fts3IncrmergeHintPop third_party/sqlite/amalgamation/sqlite3.c:176498:8
    #2 0x7f9f6af1106c in sqlite3Fts3Incrmerge third_party/sqlite/amalgamation/sqlite3.c:176567:12
    #3 0x7f9f6af088ad in fts3DoIncrmerge third_party/sqlite/amalgamation/sqlite3.c:176715:12
    #4 0x7f9f6af05496 in fts3SpecialInsert third_party/sqlite/amalgamation/sqlite3.c:177008:10
    #5 0x7f9f6af04920 in sqlite3Fts3UpdateMethod third_party/sqlite/amalgamation/sqlite3.c:177265:10
    #6 0x7f9f6aeeb6e0 in fts3UpdateMethod third_party/sqlite/amalgamation/sqlite3.c:164952:10
    #7 0x7f9f6adaf061 in sqlite3VdbeExec third_party/sqlite/amalgamation/sqlite3.c:91316:10
    #8 0x7f9f6ad3bab2 in sqlite3Step third_party/sqlite/amalgamation/sqlite3.c:82287:10
    #9 0x7f9f6ad31527 in sqlite3_step third_party/sqlite/amalgamation/sqlite3.c:82352:16
    #10 0x7f9f6ad4526c in sqlite3_exec third_party/sqlite/amalgamation/sqlite3.c:119934:12
    #11 0x564f315c2f58 in RunSqlQuery(std::__Cr::basic_string<char, std::__Cr::char_traits<char>, std::__Cr::allocator<char> >&, int*) third_party/sqlite/fuzz/shadow_table_fuzzer.cc:106:3

SUMMARY: AddressSanitizer: heap-buffer-overflow third_party/sqlite/amalgamation/sqlite3.c:161861:3 in sqlite3Fts3GetVarint
Shadow bytes around the buggy address:
  0x0c047fff8510: fa fa 00 fa fa fa 00 fa fa fa fd fa fa fa fd fa
  0x0c047fff8520: fa fa fd fa fa fa fd fd fa fa 00 fa fa fa fd fa
  0x0c047fff8530: fa fa fd fa fa fa fd fa fa fa fd fd fa fa fd fd
  0x0c047fff8540: fa fa fd fa fa fa fd fa fa fa 00 00 fa fa fd fa
  0x0c047fff8550: fa fa fd fa fa fa fd fd fa fa fd fa fa fa fd fd
=>0x0c047fff8560: fa fa fd fa fa fa fd fa fa[fa]00 fa fa fa fd fa
  0x0c047fff8570: fa fa fd fa fa fa fd fd fa fa fd fd fa fa fd fa
  0x0c047fff8580: fa fa fd fa fa fa fd fa fa fa fd fa fa fa fd fa
  0x0c047fff8590: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff85a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c047fff85b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:00
  Partially addressable: 01 02 03 04 05 06 07
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc


### dr...@gmail.com (2019-12-13)

Same story as https://crbug.com/chromium/1029506 and https://crbug.com/chromium/1029027 - fixed by check-in https://sqlite.org/src/info/e01fdbf9f700e1bd according to bisect.

### hu...@chromium.org (2019-12-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b87a7be55a14220b4ce69ab178d7ba6238664c85

commit b87a7be55a14220b4ce69ab178d7ba6238664c85
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Wed Dec 18 19:45:03 2019

sqlite: Backport bugfixes.

Bug: 1028722, 1029027, 1029210, 1029506, 1032390, 1028402, 1029002, 1030709
Change-Id: I0a51eceb98bd6724ed279386b0fb5dc85ee177db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1970738
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#726058}

[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/ext/fts3/fts3.c
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/ext/fts3/fts3Int.h
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/ext/fts3/fts3_write.c
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/src/trigger.c
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/src/util.c
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/test/attach4.test
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patched/test/fts3corrupt4.test
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0001-Don-t-allow-shadow-tables-to-be-dropped-in-defensive.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0002-Improve-shadow-table-corruption-detection-in-fts3.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0003-Shadow-Table-Corruption-Detection-improvements-in-ft.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0004-Remove-reachable-NEVER-in-fts3.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0005-Better-corruption-detection-in-fts3.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0006-Detect-Prevent-infinite-recursion.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0007-Improve-corruption-detection-in-fts4.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0008-Further-improve-corruption-detection-in-fts3.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0009-Make-sure-WITH-stack-is-disabled-after-error.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0010-Avoid-zero-offset.patch
[modify] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0011-Avoid-zero-offset-of-nullptr.patch
[add] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0012-Fix-buffer-overread.patch
[add] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0013-Fix-UB-warning.patch
[add] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0014-Avoid-temp-trigger-crash.patch
[add] https://crrev.com/b87a7be55a14220b4ce69ab178d7ba6238664c85/third_party/sqlite/patches/0015-Fix-fts3-integer-overflows.patch


### cl...@chromium.org (2019-12-18)

ClusterFuzz testcase 5101132481167360 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan&range=726056:726062

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### sh...@chromium.org (2019-12-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-20)

Requesting merge to beta M80 because latest trunk commit (726058) appears to be after beta branch point (722274).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-12-20)

This bug requires manual review: M80's targeted beta branch promotion date has already passed, so this requires manual review
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

### sr...@google.com (2019-12-20)

huangdarwin@ the CL looks like a new SQL lite update., Is it safe to merge to M80 branch ? 

### sr...@google.com (2019-12-20)

There seems to be 5 bugs where clusterfuzz added merge labels for M80 and all are related to sqllite. pls help confirm if they are all safe to merge or what the plan is 

adding adetaylor@ here for review

### ad...@google.com (2019-12-20)

This message is repeated on five similar bugs:
Sheriffbot and ClusterFuzz have together conspired to mark this as a regression, but it's not. The regression range simply contains the addition of the (apparently excellent) fuzzer so I am adjusting labels to say that this impacts stable on the assumption that these bugs have been around for a while.

It's found five bugs and they're all fixed in the same commit; although they're individually deemed Medium by ClusterFuzz, I'd say it's worth merging them all back to M79. Certainly to M80, then to M79 if they turn out to be trouble-free in M80.

### hu...@chromium.org (2019-12-20)

Hey srinivassista@, yes this is a new sqlite update to fix some security bugs. I think it should be safe to merge to M80. I've also discussed with adetaylor@, and as 2/3 sqlite reviewers are not available now, we may just want to merge to m80 at first, and consider re-evaluating merging to m79 in 2020-01-01, after it sits in m80 for a bit.

For reference, the change is here: https://crrev.com/c/1978843

### hu...@chromium.org (2019-12-23)

This should be safe to merge to M80.

1. Yes, as per https://crbug.com/1029506#c17
2. https://crrev.com/c/1978843
3. Yes
4. Security bug discovered after branch
5. No
6. N/A

### hu...@chromium.org (2019-12-30)

This has baked in canary for >1 week now, since Chrome 81.0.4001.3 (released 2019-12-20), without any issue. Could we please have merge approval to merge to M80? Thanks!

### sr...@google.com (2020-01-02)

Approved for M80, branch:3987. 

Per offline conversation with huangdarwin@  with respect to the number of files changed in the CL's , (The only file whose changes change executable code is sqlite3.c So there's actually not too many lines of executable diff, and it should be fairly safe) , Adding this info here as FYI.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/163aede25fdad037f55550e326ebceaa849fe16d

commit 163aede25fdad037f55550e326ebceaa849fe16d
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Thu Jan 02 20:49:31 2020

sqlite: Backport bugfixes (M80).

Backport onto M80

(cherry picked from commit b87a7be55a14220b4ce69ab178d7ba6238664c85)

Bug: 1028722, 1029027, 1029210, 1029506, 1032390, 1028402, 1029002, 1030709
Change-Id: I0a51eceb98bd6724ed279386b0fb5dc85ee177db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1970738
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#726058}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1978843
Reviewed-by: Marijn Kruisselbrink <mek@chromium.org>
Cr-Commit-Position: refs/branch-heads/3987@{#381}
Cr-Branched-From: c4e8da9871cc266be74481e212f3a5252972509d-refs/heads/master@{#722274}

[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/ext/fts3/fts3.c
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/ext/fts3/fts3Int.h
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/ext/fts3/fts3_write.c
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/src/trigger.c
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/src/util.c
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/test/attach4.test
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patched/test/fts3corrupt4.test
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0001-Don-t-allow-shadow-tables-to-be-dropped-in-defensive.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0002-Improve-shadow-table-corruption-detection-in-fts3.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0003-Shadow-Table-Corruption-Detection-improvements-in-ft.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0004-Remove-reachable-NEVER-in-fts3.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0005-Better-corruption-detection-in-fts3.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0006-Detect-Prevent-infinite-recursion.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0007-Improve-corruption-detection-in-fts4.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0008-Further-improve-corruption-detection-in-fts3.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0009-Make-sure-WITH-stack-is-disabled-after-error.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0010-Avoid-zero-offset.patch
[modify] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0011-Avoid-zero-offset-of-nullptr.patch
[add] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0012-Fix-buffer-overread.patch
[add] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0013-Fix-UB-warning.patch
[add] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0014-Avoid-temp-trigger-crash.patch
[add] https://crrev.com/163aede25fdad037f55550e326ebceaa849fe16d/third_party/sqlite/patches/0015-Fix-fts3-integer-overflows.patch


### na...@google.com (2020-01-09)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-01-09)

Congrats! The Panel decided to reward $3,000 for this report!

### hu...@chromium.org (2020-01-10)

As with https://crbug.com/1035371#c25, I believe adetaylor@ agreed that this CL (https://crrev.com/c/1979402) should be backported to m79 as well, due to the large number of security vulnerabilities. Please note that sqlite3.c is the only file with executable code, so the diff isn't actually too large.

### go...@chromium.org (2020-01-13)

Approving merge to M79 branch 3945 based on https://crbug.com/chromium/1028722#c30. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-01-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/29bd2aea30d34a144c61646a58afbacb0e5003e1

commit 29bd2aea30d34a144c61646a58afbacb0e5003e1
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Mon Jan 13 02:11:53 2020

sqlite: Backport bugfixes (M79).

Backport onto M79.

(cherry picked from commit b87a7be55a14220b4ce69ab178d7ba6238664c85)

Bug: 1028722, 1029027, 1029210, 1029506, 1032390, 1028402, 1029002, 1030709
Change-Id: I0a51eceb98bd6724ed279386b0fb5dc85ee177db
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1970738
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#726058}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1979402
Cr-Commit-Position: refs/branch-heads/3945@{#1034}
Cr-Branched-From: e4635fff7defbae0f9c29e798349f6fc0cce4b1b-refs/heads/master@{#706915}

[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/ext/fts3/fts3.c
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/ext/fts3/fts3Int.h
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/ext/fts3/fts3_write.c
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/src/trigger.c
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/src/util.c
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/test/attach4.test
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patched/test/fts3corrupt4.test
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0001-Don-t-allow-shadow-tables-to-be-dropped-in-defensive.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0002-Improve-shadow-table-corruption-detection-in-fts3.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0003-Shadow-Table-Corruption-Detection-improvements-in-ft.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0004-Remove-reachable-NEVER-in-fts3.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0005-Better-corruption-detection-in-fts3.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0006-Detect-Prevent-infinite-recursion.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0007-Improve-corruption-detection-in-fts4.patch
[modify] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0008-Further-improve-corruption-detection-in-fts3.patch
[add] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0012-Fix-buffer-overread.patch
[add] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0013-Fix-UB-warning.patch
[add] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0014-Avoid-temp-trigger-crash.patch
[add] https://crrev.com/29bd2aea30d34a144c61646a58afbacb0e5003e1/third_party/sqlite/patches/0015-Fix-fts3-integer-overflows.patch


### ad...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-01-13)

[Empty comment from Monorail migration]

### go...@chromium.org (2020-01-14)

+cindyb@ (Chrome OS M79 Release TPM)

### ad...@google.com (2020-01-15)

[Empty comment from Monorail migration]

### ad...@google.com (2020-01-15)

[Empty comment from Monorail migration]

### na...@google.com (2020-02-20)

What's the reporter's email address so I can process the payment of this award?

### hu...@chromium.org (2020-02-20)

leonwxqian@gmail.com

### ad...@google.com (2020-03-04)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-26)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### le...@gmail.com (2020-04-21)

Hello natashapabrai@,
Seems like I haven't received the reward yet. I updated my supplier enrollment information in January. Does it have anything to do with the supplier enrollment information? Thank you.

### aw...@google.com (2020-05-29)

Hello leonwxqian@ — it looks like this is the first libfuzzer fuzzer submitted by an external contributor! Though sadly that meant our automation wasn't quite working properly. This will get picked up on our next submission to our finance team for processing, so it might be a few more weeks yet I'm afraid. Thanks for the ping and your patience.

### le...@gmail.com (2020-05-29)

Wow! I'm surprised to know this is the first external libfuzzer fuzzer😀

Thank you for your response to my inquiry and thank you for your help.😊

### ad...@google.com (2020-08-27)

leonwxqian@ I fear you may still not have received your reward for this one yet, as I have spotted another flaw in this brand new process. If that's the case, I'm very sorry! Please could you confirm? (The same applies to https://crbug.com/chromium/1029569).

### le...@gmail.com (2020-08-28)

Thanks for the update! Yes, I haven't receive the reward for https://crbug.com/chromium/1028722 & 1029569 yet.

### ad...@google.com (2020-08-28)

Very sorry about that! I'll kick off another payment run tomorrow covering both bugs.

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-09-03)

This bug and https://crbug.com/chromium/1029569 have now both been sent to our finance team for payment. Apologies again for the delay.

### le...@gmail.com (2020-09-04)

That's fine, no problem at all 😊
Thank you very much for your help!

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1028722?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1035663, crbug.com/chromium/1035710]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050808)*
