# Security: Upgrade sqlite to 3.33.0 due to CVE-2020-13871 and CVE-2020-15358?

| Field | Value |
|-------|-------|
| **Issue ID** | [40053108](https://issues.chromium.org/issues/40053108) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2020-13871, CVE-2020-15358 |
| **Reporter** | ri...@sap.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2020-08-18 |
| **Bounty** | $500.00 |

## Description

Hi Chromium Security Team,

We perform OSS Security scans of Chromium embedded Framework/Chromium. Our latest stable version (Chromium Embedded Framework 84.3.8, Chromium 84.0.4147.105) identified several vulnerabilities for SQLite 3.31.1, where the most are already adressed with the upgrade to SQLite 3.32.1 in https://bugs.chromium.org/p/chromium/issues/detail?id=1087629. However there were two more CVEs, which seem to me not being adressed yet:

CVE-2020-13871
  Details: https://nvd.nist.gov/vuln/detail/CVE-2020-13871
  Correction in SQLite: https://www.sqlite.org/src/info/79eff1d0383179c4
  CVSS severity score: 7.5
  Description: SQLite 3.32.2 has a use-after-free in resetAccumulator in select.c because the parse tree rewrite for window functions is too late.

CVE-2020-15358
  Details: https://nvd.nist.gov/vuln/detail/CVE-2020-15358
  Correction in SQLite: https://www.sqlite.org/src/info/10fa79d00f8091e5
  CVSS severity score: 5.5
  Description: In SQLite before 3.32.3, select.c mishandles query-flattener optimization, leading to a multiSelectOrderBy heap overflow because of misuse of transitive properties for constant propagation.

Both are corrected in SQLite 3.33.0, which came out on August 14: https://sqlite.org/releaselog/3_33_0.html. Would you mind to upgrade here?

Best regards,
Richard

## Timeline

### va...@chromium.org (2020-08-18)

huangdarwin@ -- do you know if the CVEs apply to Chrome's usage of SQLite?
If not, please set the Sec-Impact to None. Thanks.

[Monorail components: Internals>Storage]

### [Deleted User] (2020-08-18)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-18)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-08-19)

I'm fairly certain these do apply to our SQLite usage, so Security_Impact-Stable unfortunately sounds right. I'll make the update ASAP.

### hu...@chromium.org (2020-08-19)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-08-19)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc

commit 0324bd3ef1af08b478c9e9f82722d7e1e565d6bc
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Wed Aug 19 08:18:38 2020

Amalgamations for release 3.33.0

Bug: 1117367
Change-Id: Iac32816078bcadfd5366a531f2805333bcd6c6e4
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation_dev/rename_exports.h
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation/shell/shell.c
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation_dev/sqlite3.c
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation/rename_exports.h
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation_dev/README.md
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation/README.md
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation_dev/sqlite3.h
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation/sqlite3.c
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation/sqlite3.h
[add] https://crrev.com/0324bd3ef1af08b478c9e9f82722d7e1e565d6bc/amalgamation_dev/shell/shell.c


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50

commit 9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Thu Aug 20 21:55:25 2020

Roll src/third_party/sqlite/src/ 5e8c30a1e..0324bd3ef (222 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/5e8c30a1e0e0..0324bd3ef1af

$ git log 5e8c30a1e..0324bd3ef --date=short --no-merges --format='%ad %ae %s'
2020-08-19 huangdarwin Amalgamations for release 3.33.0
2020-08-14 drh Version 3.33.0
2020-08-13 dan Fix "make test" handling of environment variable QUICKTEST_OMIT so that it can be used to exclude test files in other than the main test directory.
2020-08-12 drh Improvement on the previous fix.
2020-08-12 drh Fix an assertion() fault in ALTER TABLE found by OSSFuzz.  Test case in TH3.
2020-08-11 drh Fix harmless USAN warnings from gcc9.
2020-08-11 drh New test cases for the use of the ieee754 and decimal extensions in the CLI.
2020-08-11 dan Modify a test for corruption within the wal checkpoint code to account for the pending-byte page. And for the fact that test configurations might move the pending-byte page.
2020-08-11 drh Minor comment fixes.  No changes to code.
2020-08-11 drh Remove an unused #define from sqliteInt.h.
2020-08-10 drh Simplify #ifdefs associated with Parse.eParseMode.  Fix an #ifdef error associated with SQLITE_OMIT_AUTOVACUUM.
2020-08-10 dan Fix a problem causing test failures in corruptL.test for some permutations.
2020-08-10 dan Fix a problem building fts3 separately from the amalgamation.
2020-08-10 dan Fix a shell tool build error caused by some combinations of options.
2020-08-10 drh Fix harmless compiler warnings that surface in newer versions of GCC.
2020-08-10 dan Fix another test script problem in walvfs.test.
2020-08-10 dan Fix minor test script problems.
2020-08-09 drh Fix a harmless compiler warning.
2020-08-08 drh Fix the check-in at [41474548ef3f7454] so that it computes the pointer in time for error checking at the end of the routine in the case of a non-OOM error.
2020-08-08 dan Fix test script busy2.test so that it works with the inmemory-journal permutation.
2020-08-08 dan Changes to busy2.test, corruptL.test and fkey5.test so that new test cases pass with all test permutations.
2020-08-08 dan Fix a test script problem causing an error for SQLITE_ENABLE_OVERSIZE_CELL_CHECK builds in corruptL.test.
2020-08-08 drh Move a pointer computation until after OOM checks to avoid a nuisance USAN warning.
2020-08-08 dan Change the name of sqlite3SelectTrace to sqlite3_unsupported_selecttrace.
2020-08-08 drh Update requirement marks due to wording improvements in the documentation.
2020-08-08 drh Reorder declarations in the decimal extension for C89.
2020-08-07 drh Do the oversize-WAL corruption test before the size hint is issued.
2020-08-07 dan Fix a file-descriptor leak in test script corruptL.test.
2020-08-07 dan Return an SQLITE_CORRUPT error if the final expected size of the database when checkpointing is not reasonable - where reasonable is defined (basically) as the sum of the sizes of the database and wal files.
2020-08-07 drh Add the --checkpoint option to speedtest1.
2020-08-06 drh Fix the columnar output modes in the CLI so that they work with parameters. See [https://sqlite.org/forum/forumpost/17ba6aac24] for details of the problem fixed.
2020-08-04 mistachkin Fix compilation issues with MSVC.
2020-07-31 drh Back out a NEVER() that turns out to be reachable.
2020-07-31 drh Remove an ALWAYS() that turns out to be reachable.
2020-07-30 drh Test for schema corruption is reachable after all.
2020-07-30 drh Provide an alternative "guaranteed-safe" method for overwriting the WAL index on recovery, in case some platform is found for which memcpy() cannot do this safely.
2020-07-30 drh Fix compiler warnings in MSVC.
2020-07-30 drh Fix unreachable branches.
2020-07-29 drh Fix signed/unsigned compiler warnings.
2020-07-28 drh Earlier detection of out-of-range page numbers in the btree layer.
2020-07-28 drh Add an sqlite3FaultSim() to make an OOM case more accessible and remove the ALWAYS() on the conditional that is false when the OOM actually occurs.
2020-07-27 drh On recovery, always overwrite the old with the new, even if they are the same. Add ALWAYS() macros on branches currently thought to be unreachable, pending additional testing.
2020-07-27 dan Fix a couple of test scripts to match the new wal recovery behaviour on this branch.
2020-07-27 drh Improved error reporting if walLockExclusive() fails.
2020-07-25 dan Allow a wal mode recovery to proceed even if there are readers.
2020-07-24 drh Remove a surplus space from a https://crbug.com/chromium/1117367#c2020-07-24 drh Fix other potentiall pointer aliasing problems associated with subclassing of the sqlite3_file object for various VFS implementations.
2020-07-24 drh Fix pointer aliasing problem in the in-memory journal code. Ref: [https://sqlite.org/forum/forumpost/d44eb2fc44|forum post d44eb2fc44]
2020-07-23 drh Add the OMIT_ZLIB compile-time option to sessionfuzz.c.  (Originally checked into the wrong branch.)
2020-07-23 drh Fix a typo in an error message.
(...)
2020-06-10 dan Ensure that the "push-down" optimization does not push constraints down into compound queries if any of the component queries uses window functions.
2020-06-10 drh Disable AggInfo consistency checks when unwinding after an OOM.
2020-06-09 drh Mark an always-true conditional with ALWAYS().
2020-06-09 dan Ensure that aggregate functions that (a) are part of SELECT statements with no FROM clause and (b) have one or more scalar sub-selects as arguments are assigned to the correct aggregate context.
2020-06-09 dan Modify a test file to avoid causing Tcl to allocate too much memory.
2020-06-09 drh Give the expression pointer fields of AggInfo distinctive names in order to simplify tracking of all their uses.
2020-06-09 drh Improved tree-view debugging output for aggregate functions.
2020-06-08 dan Fix a case where a corrupted fts3 record could cause an assert() failure, or spurious SQLITE_NOMEM error in builds with assert() disabled.
2020-06-07 drh Fix minor OOM problems.
2020-06-07 drh AggInfo objects might be referenced even after the sqlite3Select() function that created them has exited.  So AggInfo cannot be a stack variable.  And it must not be freed until the Parse object is destroyed.
2020-06-07 drh Alternative fix to ticket [c8d3b9f0a750a529]:  Prior to deleting or modifying an Expr not that is referenced by an AggInfo, modify the AggInfo to get its own copy of the original Expr.
2020-06-05 drh In the debugging treeview output, change the name of "SELECT-expr" expression nodes to be "subquery-expr", so as to not confuse them with actual SELECT nodes.
2020-06-05 drh Always use ?...? to indicate optional arguments in the output of ".help" in the CLI.  Change ".mode column" so that it automatically activates ".headers on" if headers have not been previously turned on or off.
2020-06-04 drh Add support for "box" mode in the CLI:  Like "table" except that it uses unicode box-drawing characters instead of ascii-art.
2020-06-04 drh Improved display of ".mode table" output for empty result sets.
2020-06-04 dan Use __has_extension(c_atomic) instead of __has_feature(c_atomic) to detect support for atomic load and store operations with clang.
2020-06-04 dan Use AtomicStore() to set values in the wal-index hash table.
2020-06-04 drh Work around a bug in clang-11.0.0.
2020-06-03 drh Fix for ticket [810dc8038872e212].  Thank to user "Maxulite" for tracking down the problem!
2020-06-03 drh Simplification to the interrupt handling logic in sqlite3VdbeExec() saves a few bytes of code space.
2020-06-03 drh Improve the query planner so that it is better able to find full index scan plan when there is an INDEXED BY clause.
2020-05-30 drh Draw the dashes below the headers in "explain" mode in the CLI.
2020-05-30 drh Improved VDBE comments on the ANALYZE code generator.  This change also fixes a harmless use of an uninitialized integer variable as an input to the %d format on a VDBE comment.
2020-05-29 mistachkin Enhancements to the incremental build support for MSVC.
2020-05-29 drh Remove a stray "&amp;" character in the CLI, detected by a clang warning.
2020-05-29 drh Add the "shelltest" target to the MSVC makefile as well.
2020-05-29 drh Fix the ".import" command of the CLI to clean up better after errors. Add the new "shelltest" makefile target on unix platforms.
2020-05-29 drh Improvements to help text for the CLI.
2020-05-29 drh Fix a memory leak in the CLI when an unknown or unrecognized argument is given to the ".dump" command.
2020-05-29 drh Improvements to columnar output in the CLI.  Columns automatically expand to contain the largest row.
2020-05-29 drh Space to hold the ".width" of columns in the CLI is now obtained from malloc() and hence is not limited in the number of columns supported.
2020-05-29 drh Incremental improvements to tabular output modes in the CLI.  The "markdown" and "table" modes no have headers turned on by default.
2020-05-29 dan Expand upon a comment in os_unix.c. No changes to code.
2020-05-29 drh In the json output mode of the CLI, do correct quoting of escape characters. Also, show BLOBs as JSON strings, possibly with embedded \u0000 bytes.
2020-05-28 drh Progress toward adding new output modes to the CLI:  json, table, and markdown.
2020-05-28 drh Enhance the ".quote" mode in the shell so that it honors .separator.
2020-05-28 drh When the sqlite_stat1 data is missing for some indexes of a table but is present for the table itself or for other indexes in the same table, then do not let the estimated number of rows in that table get too small, as doing so can deceive the query planner into ignoring a perfectly good index.
2020-05-27 drh Small performance improvement and size reduction in the expression code generator.
2020-05-27 drh Change a datatype from i16 to int to appease Converity and help eliminate a false-positive.
2020-05-26 drh Fix the cksumvfs extension so that it will not register itself more than once.
2020-05-26 drh Performance optimization in the transfer of error messages from statements to connections.
2020-05-26 drh Increase the version number to 3.33.0 to begin the next release cycle.
2020-05-26 drh Innocuous changes to help Coverity avoid false-positives.
2020-05-25 drh Attempt to work around a false-positive warning in the CGo compiler.
2020-05-01 dan Fix problems with UPDATE...FROM statements that modify rowid or primary-key values.
2020-04-30 dan Add OOM tests for the new code on this branch.
2020-04-30 dan Report an error if an UPDATE...FROM statement has an ORDER BY but no LIMIT clause. Add tests for multi-column primary keys.
2020-04-29 dan Fix problems with using LIMIT and FROM clauses as part of single UPDATE statement.
2020-04-29 dan Fix various bugs in new feature on this branch.
2020-04-27 dan Allow a FROM clause in UPDATE statements.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1117367
Change-Id: Ie37ce39b80489b01ea8569eafea79e5bf8c54d5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2364964
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Chris Mumford <cmumford@google.com>
Cr-Commit-Position: refs/heads/master@{#800336}

[modify] https://crrev.com/9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50/DEPS
[modify] https://crrev.com/9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50/third_party/sqlite/README.chromium
[modify] https://crrev.com/9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50/third_party/sqlite/README.md


### hu...@chromium.org (2020-08-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-21)

This bug requires manual review: We are only 3 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-08-21)

1. Possibly. This is a large binary change per https://crbug.com/chromium/1117367#c7, and may introduce new bugs, but does fix 2 CVEs with Security_Severity-High, so just wanted to bring this to Security+Release TPM attention.
2. https://crrev.com/c/2364964
3.This is currently on ToT and canary. I'd wait a week to ensure stability before pushing to M85.
4. No.
6. N/A.

### [Deleted User] (2020-08-22)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-24)

huangdarwin@, do you believe that the defense-in-depth measures we have in sqlite should prevent these from being practically exploitable from web content? If that's the case (even if we're not certain) I'm inclined to leave this until M86, otherwise we should merge to the first M85 refresh.

(I'm looking into why Vomit didn't tell us about these).

### ad...@google.com (2020-08-24)

OK. I think I've figured out why Vomit didn't report these. The CPEPrefix and version number in README.chromium was previously 3.31.2, whereas actually the version in use was 3.32.1. It is a bit unfortunate that our third party vulnerability reporting relies on these fragile version numbers: there's still lots of work to do to improve this area.

Meanwhile thanks richard.lorenz@ for the report.

### hu...@chromium.org (2020-08-24)

I believe defense-in-depth may make this not practically exploitable from web content, but I'm not certain. Leaving this until M86 sounds fine to me.

Oh yeah, sorry the CPEPrefix was previously out of sync with the actual version. (They're in sync again now)

### ad...@google.com (2020-08-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-26)

richard.lorenz@sap.com - thanks for this report. The VRP panel has decided to award $500. Someone from our finance team will be in touch.

### ad...@google.com (2020-08-26)

This is a major version upgrade so after discussion with Darwin, we should keep till M86 to avoid stability risk.

### ri...@sap.com (2020-08-27)

Hey there,

Thank you very much for the reward. Please donate it to a charity organization of your choice - I did not much, besides only informing you about this new version of sqlite ;-)
Looking forward to consuming the correction in Chromium Embedded Framework 86.

Best regards and many thanks,
Richard

### ad...@google.com (2020-09-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-12)

huangdarwin@ it looks like commit 9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50 actually landed in M87 not M86. How do you feel about merging this to M86 now it's had a huge amount of bake time in Canary? Obviously these are quite visible upstream bugs so it would be good to merge into M86 if you think it's safe enough.

### [Deleted User] (2020-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-12)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS),  pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-10-12)

Hi adetaylor@, this change was very large in lines-of-executable-code changed, as it updated the major version of Chrome's sqlite checkout. This historically (especially 1-2 years ago) meant seeing many security bugs of varying severity (low->high) in the weeks following the major upgrade. That said, agreed that this has had a large amount of bake time now, and I've gone through the sqlite bugs to verify that no new sqlite security bugs have been reported to us (externally or by clusterfuzz) since this major release was merged. In addition, for whatever reason (improved sqlite testing infra? caution during covid19? reduced chrome visibility into bugs?), sqlite has had very few security bugs this year outside of those caught for major releases. Therefore, I believe it should likely be safe to merge to M86.

Merge review survey:
1. Yes.
2. https://crrev.com/c/2364964
3. Yes, since 8/20 (for almost 2 months now :o )
4. No.
5. Security fix
6. No.
7. N/A

### ad...@google.com (2020-10-12)

OK, thank you for the considered analysis. In that case, yes, approving merge for M86 (branch 4240).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/827f698dc466052de1c43c535cb1553d02129b08

commit 827f698dc466052de1c43c535cb1553d02129b08
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Mon Oct 12 22:09:54 2020

Roll src/third_party/sqlite/src/ 5e8c30a1e..0324bd3ef (222 commits) (M86)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/5e8c30a1e0e0..0324bd3ef1af

$ git log 5e8c30a1e..0324bd3ef --date=short --no-merges --format='%ad %ae %s'
2020-08-19 huangdarwin Amalgamations for release 3.33.0
2020-08-14 drh Version 3.33.0
2020-08-13 dan Fix "make test" handling of environment variable QUICKTEST_OMIT so that it can be used to exclude test files in other than the main test directory.
2020-08-12 drh Improvement on the previous fix.
2020-08-12 drh Fix an assertion() fault in ALTER TABLE found by OSSFuzz.  Test case in TH3.
2020-08-11 drh Fix harmless USAN warnings from gcc9.
2020-08-11 drh New test cases for the use of the ieee754 and decimal extensions in the CLI.
2020-08-11 dan Modify a test for corruption within the wal checkpoint code to account for the pending-byte page. And for the fact that test configurations might move the pending-byte page.
2020-08-11 drh Minor comment fixes.  No changes to code.
2020-08-11 drh Remove an unused #define from sqliteInt.h.
2020-08-10 drh Simplify #ifdefs associated with Parse.eParseMode.  Fix an #ifdef error associated with SQLITE_OMIT_AUTOVACUUM.
2020-08-10 dan Fix a problem causing test failures in corruptL.test for some permutations.
2020-08-10 dan Fix a problem building fts3 separately from the amalgamation.
2020-08-10 dan Fix a shell tool build error caused by some combinations of options.
2020-08-10 drh Fix harmless compiler warnings that surface in newer versions of GCC.
2020-08-10 dan Fix another test script problem in walvfs.test.
2020-08-10 dan Fix minor test script problems.
2020-08-09 drh Fix a harmless compiler warning.
2020-08-08 drh Fix the check-in at [41474548ef3f7454] so that it computes the pointer in time for error checking at the end of the routine in the case of a non-OOM error.
2020-08-08 dan Fix test script busy2.test so that it works with the inmemory-journal permutation.
2020-08-08 dan Changes to busy2.test, corruptL.test and fkey5.test so that new test cases pass with all test permutations.
2020-08-08 dan Fix a test script problem causing an error for SQLITE_ENABLE_OVERSIZE_CELL_CHECK builds in corruptL.test.
2020-08-08 drh Move a pointer computation until after OOM checks to avoid a nuisance USAN warning.
2020-08-08 dan Change the name of sqlite3SelectTrace to sqlite3_unsupported_selecttrace.
2020-08-08 drh Update requirement marks due to wording improvements in the documentation.
2020-08-08 drh Reorder declarations in the decimal extension for C89.
2020-08-07 drh Do the oversize-WAL corruption test before the size hint is issued.
2020-08-07 dan Fix a file-descriptor leak in test script corruptL.test.
2020-08-07 dan Return an SQLITE_CORRUPT error if the final expected size of the database when checkpointing is not reasonable - where reasonable is defined (basically) as the sum of the sizes of the database and wal files.
2020-08-07 drh Add the --checkpoint option to speedtest1.
2020-08-06 drh Fix the columnar output modes in the CLI so that they work with parameters. See [https://sqlite.org/forum/forumpost/17ba6aac24] for details of the problem fixed.
2020-08-04 mistachkin Fix compilation issues with MSVC.
2020-07-31 drh Back out a NEVER() that turns out to be reachable.
2020-07-31 drh Remove an ALWAYS() that turns out to be reachable.
2020-07-30 drh Test for schema corruption is reachable after all.
2020-07-30 drh Provide an alternative "guaranteed-safe" method for overwriting the WAL index on recovery, in case some platform is found for which memcpy() cannot do this safely.
2020-07-30 drh Fix compiler warnings in MSVC.
2020-07-30 drh Fix unreachable branches.
2020-07-29 drh Fix signed/unsigned compiler warnings.
2020-07-28 drh Earlier detection of out-of-range page numbers in the btree layer.
2020-07-28 drh Add an sqlite3FaultSim() to make an OOM case more accessible and remove the ALWAYS() on the conditional that is false when the OOM actually occurs.
2020-07-27 drh On recovery, always overwrite the old with the new, even if they are the same. Add ALWAYS() macros on branches currently thought to be unreachable, pending additional testing.
2020-07-27 dan Fix a couple of test scripts to match the new wal recovery behaviour on this branch.
2020-07-27 drh Improved error reporting if walLockExclusive() fails.
2020-07-25 dan Allow a wal mode recovery to proceed even if there are readers.
2020-07-24 drh Remove a surplus space from a https://crbug.com/chromium/1117367#c2020-07-24 drh Fix other potentiall pointer aliasing problems associated with subclassing of the sqlite3_file object for various VFS implementations.
2020-07-24 drh Fix pointer aliasing problem in the in-memory journal code. Ref: [https://sqlite.org/forum/forumpost/d44eb2fc44|forum post d44eb2fc44]
2020-07-23 drh Add the OMIT_ZLIB compile-time option to sessionfuzz.c.  (Originally checked into the wrong branch.)
2020-07-23 drh Fix a typo in an error message.
(...)
2020-06-10 dan Ensure that the "push-down" optimization does not push constraints down into compound queries if any of the component queries uses window functions.
2020-06-10 drh Disable AggInfo consistency checks when unwinding after an OOM.
2020-06-09 drh Mark an always-true conditional with ALWAYS().
2020-06-09 dan Ensure that aggregate functions that (a) are part of SELECT statements with no FROM clause and (b) have one or more scalar sub-selects as arguments are assigned to the correct aggregate context.
2020-06-09 dan Modify a test file to avoid causing Tcl to allocate too much memory.
2020-06-09 drh Give the expression pointer fields of AggInfo distinctive names in order to simplify tracking of all their uses.
2020-06-09 drh Improved tree-view debugging output for aggregate functions.
2020-06-08 dan Fix a case where a corrupted fts3 record could cause an assert() failure, or spurious SQLITE_NOMEM error in builds with assert() disabled.
2020-06-07 drh Fix minor OOM problems.
2020-06-07 drh AggInfo objects might be referenced even after the sqlite3Select() function that created them has exited.  So AggInfo cannot be a stack variable.  And it must not be freed until the Parse object is destroyed.
2020-06-07 drh Alternative fix to ticket [c8d3b9f0a750a529]:  Prior to deleting or modifying an Expr not that is referenced by an AggInfo, modify the AggInfo to get its own copy of the original Expr.
2020-06-05 drh In the debugging treeview output, change the name of "SELECT-expr" expression nodes to be "subquery-expr", so as to not confuse them with actual SELECT nodes.
2020-06-05 drh Always use ?...? to indicate optional arguments in the output of ".help" in the CLI.  Change ".mode column" so that it automatically activates ".headers on" if headers have not been previously turned on or off.
2020-06-04 drh Add support for "box" mode in the CLI:  Like "table" except that it uses unicode box-drawing characters instead of ascii-art.
2020-06-04 drh Improved display of ".mode table" output for empty result sets.
2020-06-04 dan Use __has_extension(c_atomic) instead of __has_feature(c_atomic) to detect support for atomic load and store operations with clang.
2020-06-04 dan Use AtomicStore() to set values in the wal-index hash table.
2020-06-04 drh Work around a bug in clang-11.0.0.
2020-06-03 drh Fix for ticket [810dc8038872e212].  Thank to user "Maxulite" for tracking down the problem!
2020-06-03 drh Simplification to the interrupt handling logic in sqlite3VdbeExec() saves a few bytes of code space.
2020-06-03 drh Improve the query planner so that it is better able to find full index scan plan when there is an INDEXED BY clause.
2020-05-30 drh Draw the dashes below the headers in "explain" mode in the CLI.
2020-05-30 drh Improved VDBE comments on the ANALYZE code generator.  This change also fixes a harmless use of an uninitialized integer variable as an input to the %d format on a VDBE comment.
2020-05-29 mistachkin Enhancements to the incremental build support for MSVC.
2020-05-29 drh Remove a stray "&amp;" character in the CLI, detected by a clang warning.
2020-05-29 drh Add the "shelltest" target to the MSVC makefile as well.
2020-05-29 drh Fix the ".import" command of the CLI to clean up better after errors. Add the new "shelltest" makefile target on unix platforms.
2020-05-29 drh Improvements to help text for the CLI.
2020-05-29 drh Fix a memory leak in the CLI when an unknown or unrecognized argument is given to the ".dump" command.
2020-05-29 drh Improvements to columnar output in the CLI.  Columns automatically expand to contain the largest row.
2020-05-29 drh Space to hold the ".width" of columns in the CLI is now obtained from malloc() and hence is not limited in the number of columns supported.
2020-05-29 drh Incremental improvements to tabular output modes in the CLI.  The "markdown" and "table" modes no have headers turned on by default.
2020-05-29 dan Expand upon a comment in os_unix.c. No changes to code.
2020-05-29 drh In the json output mode of the CLI, do correct quoting of escape characters. Also, show BLOBs as JSON strings, possibly with embedded \u0000 bytes.
2020-05-28 drh Progress toward adding new output modes to the CLI:  json, table, and markdown.
2020-05-28 drh Enhance the ".quote" mode in the shell so that it honors .separator.
2020-05-28 drh When the sqlite_stat1 data is missing for some indexes of a table but is present for the table itself or for other indexes in the same table, then do not let the estimated number of rows in that table get too small, as doing so can deceive the query planner into ignoring a perfectly good index.
2020-05-27 drh Small performance improvement and size reduction in the expression code generator.
2020-05-27 drh Change a datatype from i16 to int to appease Converity and help eliminate a false-positive.
2020-05-26 drh Fix the cksumvfs extension so that it will not register itself more than once.
2020-05-26 drh Performance optimization in the transfer of error messages from statements to connections.
2020-05-26 drh Increase the version number to 3.33.0 to begin the next release cycle.
2020-05-26 drh Innocuous changes to help Coverity avoid false-positives.
2020-05-25 drh Attempt to work around a false-positive warning in the CGo compiler.
2020-05-01 dan Fix problems with UPDATE...FROM statements that modify rowid or primary-key values.
2020-04-30 dan Add OOM tests for the new code on this branch.
2020-04-30 dan Report an error if an UPDATE...FROM statement has an ORDER BY but no LIMIT clause. Add tests for multi-column primary keys.
2020-04-29 dan Fix problems with using LIMIT and FROM clauses as part of single UPDATE statement.
2020-04-29 dan Fix various bugs in new feature on this branch.
2020-04-27 dan Allow a FROM clause in UPDATE statements.

Created with:
  roll-dep src/third_party/sqlite/src

TBR=cmumford@google.com
(cherry picked from commit 9c2848796cc438e7d5a622f0f8ae2b4bf3bc3f50)

Bug: 1117367
Change-Id: Ie37ce39b80489b01ea8569eafea79e5bf8c54d5e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2364964
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Chris Mumford <cmumford@google.com>
Cr-Original-Commit-Position: refs/heads/master@{#800336}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2466502
Reviewed-by: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1226}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/827f698dc466052de1c43c535cb1553d02129b08/DEPS
[modify] https://crrev.com/827f698dc466052de1c43c535cb1553d02129b08/third_party/sqlite/README.chromium
[modify] https://crrev.com/827f698dc466052de1c43c535cb1553d02129b08/third_party/sqlite/README.md


### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-12-22)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1117367?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1087629]
[Monorail blocking: crbug.com/chromium/1161048]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40053108)*
