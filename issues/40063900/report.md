# Security: heap-buffer-overflow on WebSQL sqlite3VdbeSorterInit

| Field | Value |
|-------|-------|
| **Issue ID** | [40063900](https://issues.chromium.org/issues/40063900) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P2 |
| **Component** | Internals>Storage |
| **Platforms** | Linux, Mac, Windows |
| **Reporter** | et...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2023-04-05 |
| **Bounty** | $1,000.00 |

## Description

Title : heap-buffer-overflow in WebSQL

**VULNERABILITY DETAILS**

## INTRODUCE

This vulnerability was introduced in March 2022 and has existed in chrome for over a year.  

The vulnerability was introduced by this branch: <https://github.com/sqlite/sqlite/commit/ece092e728e91a6cba1a4e6cd81606a38e4b2b12>

## Root Cause

[0] In the sqlite3KeyInfoFromExprList function, the iStart here may be greater than nExpr, resulting in an integer overflow when nExpr-iStart. Here nExpr will be 64 and iStart will be 65 when processing statements in poc:

```
SQLITE_PRIVATE KeyInfo \*sqlite3KeyInfoFromExprList(  
  Parse \*pParse,       /\* Parsing context \*/  
  ExprList \*pList,     /\* Form the KeyInfo object from this ExprList \*/  
  int iStart,          /\* Begin with this column of pList \*/  
  int nExtra           /\* Add this many extra columns to the end \*/  
){  
  int nExpr;  
  KeyInfo \*pInfo;  
  struct ExprList_item \*pItem;  
  sqlite3 \*db = pParse->db;  
  int i;  
  
  nExpr = pList->nExpr;  
  pInfo = sqlite3KeyInfoAlloc(db, nExpr-iStart, nExtra+1); // --->[0] Integer Overflow  
  // nExpr: 64  
  // iStart: 65  
	// nExpr - iStart = -1  
  if( pInfo ){  
    assert( sqlite3KeyInfoIsWriteable(pInfo) );  
    for(i=iStart, pItem=pList->a+iStart; i<nExpr; i++, pItem++){  
      pInfo->aColl[i-iStart] = sqlite3ExprNNCollSeq(pParse, pItem->pExpr);  
      pInfo->aSortFlags[i-iStart] = pItem->fg.sortFlags;  
    }  
  }  
  return pInfo;  
}  

```

[1] In the sqlite3KeyInfoAlloc function, apply for memory by calculating N+X, where X=66, N+X=65.

However, N was later converted into u16int type and saved in p->nKeyField, which is 0xffff, far greater than the allocated memory.

```
SQLITE_PRIVATE KeyInfo \*sqlite3KeyInfoAlloc(sqlite3 \*db, int N, int X){  
  int nExtra = (N+X)\*(sizeof(CollSeq\*)+1) - sizeof(CollSeq\*); // --->[1]  
  KeyInfo \*p = sqlite3DbMallocRawNN(db, sizeof(KeyInfo) + nExtra);  
  if( p ){  
    p->aSortFlags = (u8\*)&p->aColl[N+X];  
    p->nKeyField = (u16)N; // --->[1] Integer Overflow, p->nKeyField = 0xffff  
    p->nAllField = (u16)(N+X);  
    p->enc = ENC(db);  
    p->db = db;  
    p->nRef = 1;  
    memset(&p[1], 0, nExtra);  
  }else{  
    return (KeyInfo\*)sqlite3OomFault(db);  
  }  
  return p;  
}  

```

[2] In the subsequent sqlite3VdbeSorterInit function, nKeyField is used to calculate szKeyInfo, which will be a very large value: 0x80018, while the previously allocated memory is very small, causing an out-of-bounds read in the memcpy function.

```
szKeyInfo = sizeof(KeyInfo) + (pCsr->pKeyInfo->nKeyField-1)\*sizeof(CollSeq\*); // --->[2]  
sz = sizeof(VdbeSorter) + nWorker \* sizeof(SortSubtask);  
  
pSorter = (VdbeSorter\*)sqlite3DbMallocZero(db, sz + szKeyInfo);  
pCsr->uc.pSorter = pSorter;  
if( pSorter==0 ){  
  rc = SQLITE_NOMEM_BKPT;  
}else{  
  Btree \*pBt = db->aDb[0].pBt;  
  pSorter->pKeyInfo = pKeyInfo = (KeyInfo\*)((u8\*)pSorter + sz);  
  memcpy(pKeyInfo, pCsr->pKeyInfo, szKeyInfo); // --->[2]: oob-read  

```

\*\*Why does the situation of a smaller number being subtracted from a larger number occur? The reasons are as follows:\*\*

## Root Cause for Integer Overflow

The main cause of the vulnerability lies in the sqlite3WhereBegin function and the wherePathSolver function.

[0] The vulnerability is triggered when the number of expr in pOrderBy is >= 64. When this condition is met, the sqlite3WhereBegin function will process pResultSet as the new pOrderBy, where pResultSet is the result of the SELECT operation.

```
/\* An ORDER/GROUP BY clause of more than 63 terms cannot be optimized \*/  
testcase( pOrderBy && pOrderBy->nExpr==BMS-1 );  
if( pOrderBy && pOrderBy->nExpr>=BMS ) pOrderBy = 0; // --->[0]  
//....  
}else if( pOrderBy==0 ){  
    /\* Try to ORDER BY the result set to make distinct processing easier \*/  
    pWInfo->wctrlFlags |= WHERE_DISTINCTBY;  
    pWInfo->pOrderBy = pResultSet; // --->[0]  
}  

```

[1] However, the pOrderBy node on the syntax tree remains unchanged, with the number of expr being 64. But the number of expr in pResultSet may be greater than 64, as in the case of the PoC, which is 65. This causes an inconsistency in the number of nodes before and after, leading to subsequent integer overflow.

```
nOrderBy = pWInfo->pOrderBy->nExpr; // --->[1]  
// ....  
aFrom[0].isOrdered = nLoop>0 ? -1 : nOrderBy; // --->[1]  
// ....  
if( pWInfo->pOrderBy ){  
    pWInfo->nOBSat = pFrom->isOrdered; // --->[1]  
    if( pWInfo->wctrlFlags & WHERE_DISTINCTBY ){  
        if( pFrom->isOrdered==pWInfo->pOrderBy->nExpr ){  
            pWInfo->eDistinct = WHERE_DISTINCT_ORDERED;  
        }  
    }else{  
        pWInfo->revMask = pFrom->revLoop;  

```
## CRASH LOG

see asan.log

## Other

\*\*I found that this vulnerability has been fixed in SQLite two weeks ago, but Chrome has not been aware of this vulnerability in both the latest stable and mainline versions. Therefore, I am submitting it here to urge Chromium to continue tracking the stable releases of SQLite and improve its security.\*\*

Fix: <https://github.com/sqlite/sqlite/commit/b816ca9994e03a8bc829b49452b8158a731e81a9>

Patch for fix it:  

\*\*Check whether the pOrderBy->nExpr later is greater than the pOrderBy->nExpr earlier.\*\*

```
diff --git a/src/where.c b/src/where.c  
index 727c77948..f707fab12 100644  
--- a/src/where.c  
+++ b/src/where.c  
@@ -5299,6 +5299,10 @@ static int wherePathSolver(WhereInfo \*pWInfo, LogEst nRowEst){  
       if( pFrom->isOrdered==pWInfo->pOrderBy->nExpr ){  
         pWInfo->eDistinct = WHERE_DISTINCT_ORDERED;  
       }  
+      if( pWInfo->pSelect->pOrderBy  
+       && pWInfo->nOBSat > pWInfo->pSelect->pOrderBy->nExpr ){  
+        pWInfo->nOBSat = pWInfo->pSelect->pOrderBy->nExpr;  
+      }  
     }else{  
       pWInfo->revMask = pFrom->revLoop;  
       if( pWInfo->nOBSat<=0 ){  

```

**VERSION**  

newest version of chrome

**REPRODUCTION CASE**

1. Download newest release Chromium with asan:  
   
   wget [https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1122989.zip\?generation\=1680012946142901\&alt\=media](https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1122989.zip%5C?generation%5C=1680012946142901%5C&alt%5C=media)
2. Run: `./chrome poc.html`

**CREDIT INFORMATION**  

Reporter credit: Nan Wang(@eternalsakura13) and Guang Gong of 360 Vulnerability Research Institute

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 43.8 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.2 KB)

## Timeline

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-04-05)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=6405704626405376.

### cl...@chromium.org (2023-04-05)

ClusterFuzz testcase 6405704626405376 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2023-04-05)

Detailed Report: https://clusterfuzz.com/testcase?key=6405704626405376

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: Heap-buffer-overflow READ {*}
Crash Address: 0x6160000815f0
Crash State:
  sqlite3VdbeExec
  chrome_sqlite3_step
  blink::SQLiteStatement::Step
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1126490

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=6405704626405376

To reproduce this, please build the target in this report and run it against the reproducer testcase. Please use the GN arguments provided at bottom of this report when building the binary. 

If you have trouble reproducing, please also export the environment variables listed under "[Environment]" in the crash stacktrace.

If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

A recommended severity was added to this bug. Please change the severity if it is inaccurate.

### an...@google.com (2023-04-05)

I am able to repro with M112 in a redshell VM. 
Given that this vulnerability is a year old, setting FoundIn to extended stable.
Assigning to asully@ based on OWNERs file. Please re-route as necessary.

[Monorail components: Internals>Storage]

### [Deleted User] (2023-04-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-04-05)

ClusterFuzz testcase 6405704626405376 appears to be flaky, updating reproducibility label.

### an...@google.com (2023-04-05)

Re-assigning to mek@ as it is an sqlite issue.

[Monorail components: -Internals>Storage]

### me...@chromium.org (2023-04-05)

asully@ is the right owner for sqlite issues afaik

### [Deleted User] (2023-04-05)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-05)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-04-05)

[Empty comment from Monorail migration]

[Monorail components: Internals>Storage]

### as...@chromium.org (2023-04-05)

Hi OP, thanks for the detailed report and for including the upstream commit where this was fixed (https://github.com/sqlite/sqlite/commit/b816ca9994e03a8bc829b49452b8158a731e81a9)

Looks like the fix is indeed included in the latest SQLite 3.42.2 release. Upgrading versions is tracked in https://crbug.com/chromium/1426903 and will be completed shortly

### as...@chromium.org (2023-04-06)

Upgrade to 3.41.2 is complete

Requesting merge of https://crrev.com/c/4404861 to 112 and 113

### as...@chromium.org (2023-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), eakpobaro (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-04-06)

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2023-04-06)

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches

For M113 - undoubtedly yes. This is a relatively straightforward fix to a medium severity security bug
For M112 - I think so, though I'm not sure if the fact that it's flakily reproducible mitigates this at all. Open to input from security/release folks

2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c/4404861

3. Have the changes been released and tested on canary?

Not yet, the CL just landed

+anunoy could you confirm this is no longer reproducible from TOT in your redshell VM?

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

N/A

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### [Deleted User] (2023-04-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-04-07)

ClusterFuzz testcase 6405704626405376 is verified as fixed in https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&range=1127282:1127289

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### an...@chromium.org (2023-04-07)

FYI Merge reviewer(s): ClusterFuzz has now verified the fix.

### am...@chromium.org (2023-04-07)

hey asully@ thanks for the quick work on this one and for your responses to the merge questionnaire. I think it's best to backmerge this to both 113 as well as 112. I don't consider flaky reproducibility to be considered a mitigation here, especially since it was stable enough that clusterfuzz can reproduce and also that 112 is due to become Extended Stable once 113 is promoted to Stable. 

Since the upgrade CL just landed less than 24 hours ago, I do want to let this get a bit more bake time on Canary, and I can revisit for merge review on Monday / early next week. This should provide well enough time to get this merged for next M113 beta and M112/Stable respin. 

 

### as...@chromium.org (2023-04-07)

SGTM! In the meantime, I've prepared the merge CLs

M112: https://crrev.com/c/4409001
M113: https://crrev.com/c/4409783

### am...@chromium.org (2023-04-10)

Thanks asully@! 
113 merge approved, please merge this fix to branch 5672 so this fix can be included by EOD tomorrow, Tuesday April 11 so this fix can be included in next M113/beta
112 merge approved, please merge this fix to branch 5615 by EOD Thursday, 13 April so this fix can be include in next week's M112/Stable respin

### gi...@appspot.gserviceaccount.com (2023-04-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/66c1ea762bd355b6c6990196e5c1014ee16c05f3

commit 66c1ea762bd355b6c6990196e5c1014ee16c05f3
Author: Austin Sullivan <asully@chromium.org>
Date: Tue Apr 11 17:54:39 2023

[M112] sqlite: Upgrade to 3.41.2

Roll src/third_party/sqlite/src/ 7dd277f31..f6752b7ed (37 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/7dd277f31ccd..f6752b7ed1fe

$ git log 7dd277f31..f6752b7ed --date=short --no-merges --format='%ad %ae %s'
2023-04-06 asully sqlite: Cherry-pick fix to allow shell to build recovery... again
2023-03-24 asully Amalgamations for release 3.41.2
2023-03-22  Version 3.41.2
2023-03-22  Increment the version number in the TEA configure script to 3.41.2.
2023-03-21  Fix a valgrind error and potential buffer overread when handling a corrupt database.
2023-03-20  Fix a problem causing a cursor to retain an out-of-date cell-info cache when processing a DISTINCT query on values that are identical according to their collation sequence, but different on disk.
2023-03-20  Fix problems with the sqlite3_error_offset() function and its use in the CLI.
2023-03-19  Increase the size of ref-count values in the pager layer to 64-bits, to avoid any reasonable possiblity of overflowing the counters.
2023-03-19  Avoid a buffer overread in fts3 that could occur when processing a corrupt record.
2023-03-17 Dan Kennedy Fix a potential buffer overread in the recovery extension.
2023-03-17  Ensure that an error does not delete the Table object out from under the xConstruct method of a virtual table. dbsqlfuzz 7cc8804a1c6d4e3d554d79096e6ea75a7c1c7d2d
2023-03-17  Increase the version number to 3.41.2
2023-03-17  Fix assert() statements that would (incorrectly) fire if an IF NOT EXISTS trigger that already exists contained two or more RETURNING clauses.
2023-03-16  Correctly handle SELECT DISTINCT ... ORDER BY when all of the result set terms are constant and there are more result set terms than ORDER BY terms.
2023-03-16  Do not use the one-pass optimization on an UPDATE if there is a subquery in the WHERE clause, since if the subquery is hidden behind a short-circuit operator, the subquery might not be evaluated until after one or more rows have been updated.
2023-03-16  Remove a NEVER() from btreeNext().
2023-03-16  Fix a broken assert() in the recovery extension.
2023-03-15  Disallow the one-pass optimization for DELETE if the WHERE clause contains a subquery.
2023-03-14  Fix Bloom filters on an expression index.
2023-03-11  The cherry-pick merge at [371838562a675c1b] caused a performance regression for some queries, which is here fixed.
2023-03-10  Version 3.41.1
2023-03-09  In the Bloom filter optimization, hash all strings and blobs into the same value, because we do not know if two different strings might compare equal even if they have different byte sequences, due to collating functions. Formerly, the hash of a string or blob was just its length.  This could all be improved.
2023-03-09 Dan Kennedy Fix countofview.test so that it works with SQLITE_OMIT_PROGRESS_CALLBACK builds.
2023-03-09  Update the version number to 3.41.1
2023-03-09  Merge count-of-view optimization fixes from trunk.  But count-of-view is still off by default for this branch.
2023-03-09  Fix a possible NULL pointer dereference due to the sqlite3_interrupt() enhancement in the 3.41.0 release.
2023-03-08  Keep the historical datatype ("INT", not "NUM") for a table created as follows: "CREATE TABLE t1 AS SELECT CAST(123 AS INT) AS value;".  The use of FLEXNUM only occurs on compound queries.
2023-03-08  Fix an assertion fault added by [65ffee234787213c].
2023-03-04  Cherry-pick the agg-with-indexed-expr optimization fix from trunk.
2023-03-03  Do not use an expression index on a generated column if generated column has the wrong affinity.
2023-03-03  Enhance PRAGMA integrity_check so that it can detect when there are extra bytes at the end of an index record, which might cause OP_IdxRowid to malfunction.
2023-03-03  When it is known when preparing a statement that X cannot be NULL, transform the expression (X IS NULL) to integer value 1 instead of 'true'. This is because under some circumstances, "Y IS TRUE" may not be equivalent to "Y IS 1".
2023-03-02  When flattening the right operand of a LEFT JOIN, ensure that the OP_IfNullRow opcode does not NULL-out a subquery result that was computed within OP_Once.
2023-03-01  When flattening a view that is the right operand of a LEFT JOIN always insert the TK_IF_NULL_ROW expression nodes, even for TK_COLUMN expressions, as the TK_COLUMN might be a column from an outer query and hence still need to be NULLed out.
2023-03-01  Make sure subtypes do not cross a subquery boundary even if the function that returned the value with a subtype is buried down inside a larger expression.
2023-02-26  When a table-valued function appears as the right table of a RIGHT JOIN, the argument constraints on the table-valued function should be considered part of the ON clause of the RIGHT JOIN.
2023-02-23  Provide -DHAVE_LOG2=0 and -DHAVE_LOG10=0 compile-time options for use on systems that lack the log2() and log10() standard math library routines, to cause SQLite to substitute its own alternatives.

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit 4c1b1f8039c53009cfb9abef8ac003d616fa1a09)

Bug: 1426903, 1430644
Change-Id: Idc39b0c87be7152582c78f7eb6e53dd2d04b2b48
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4404861
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1127286}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4409001
Cr-Commit-Position: refs/branch-heads/5615@{#1208}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/66c1ea762bd355b6c6990196e5c1014ee16c05f3/third_party/sqlite/README.chromium
[modify] https://crrev.com/66c1ea762bd355b6c6990196e5c1014ee16c05f3/DEPS


### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations Nan Wang and Guang Gong! The VRP Panel has decided to award you $1,000 as a thank you for this report. These issues were known and resolved upstream, and the fixes included in a updated that we planned to roll, however, you report provided a catalyst to get the update moving and rolled into Chromium. Thank you for your efforts in reporting this issue to us , which helped to move that forward! 

### gi...@appspot.gserviceaccount.com (2023-04-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b45bc0a62c6e4aa92e9c7dec4f28c66ec3c85755

commit b45bc0a62c6e4aa92e9c7dec4f28c66ec3c85755
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Apr 14 19:38:19 2023

[M113] sqlite: Upgrade to 3.41.2

Roll src/third_party/sqlite/src/ 7dd277f31..f6752b7ed (37 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/7dd277f31ccd..f6752b7ed1fe

$ git log 7dd277f31..f6752b7ed --date=short --no-merges --format='%ad %ae %s'
2023-04-06 asully sqlite: Cherry-pick fix to allow shell to build recovery... again
2023-03-24 asully Amalgamations for release 3.41.2
2023-03-22  Version 3.41.2
2023-03-22  Increment the version number in the TEA configure script to 3.41.2.
2023-03-21  Fix a valgrind error and potential buffer overread when handling a corrupt database.
2023-03-20  Fix a problem causing a cursor to retain an out-of-date cell-info cache when processing a DISTINCT query on values that are identical according to their collation sequence, but different on disk.
2023-03-20  Fix problems with the sqlite3_error_offset() function and its use in the CLI.
2023-03-19  Increase the size of ref-count values in the pager layer to 64-bits, to avoid any reasonable possiblity of overflowing the counters.
2023-03-19  Avoid a buffer overread in fts3 that could occur when processing a corrupt record.
2023-03-17 Dan Kennedy Fix a potential buffer overread in the recovery extension.
2023-03-17  Ensure that an error does not delete the Table object out from under the xConstruct method of a virtual table. dbsqlfuzz 7cc8804a1c6d4e3d554d79096e6ea75a7c1c7d2d
2023-03-17  Increase the version number to 3.41.2
2023-03-17  Fix assert() statements that would (incorrectly) fire if an IF NOT EXISTS trigger that already exists contained two or more RETURNING clauses.
2023-03-16  Correctly handle SELECT DISTINCT ... ORDER BY when all of the result set terms are constant and there are more result set terms than ORDER BY terms.
2023-03-16  Do not use the one-pass optimization on an UPDATE if there is a subquery in the WHERE clause, since if the subquery is hidden behind a short-circuit operator, the subquery might not be evaluated until after one or more rows have been updated.
2023-03-16  Remove a NEVER() from btreeNext().
2023-03-16  Fix a broken assert() in the recovery extension.
2023-03-15  Disallow the one-pass optimization for DELETE if the WHERE clause contains a subquery.
2023-03-14  Fix Bloom filters on an expression index.
2023-03-11  The cherry-pick merge at [371838562a675c1b] caused a performance regression for some queries, which is here fixed.
2023-03-10  Version 3.41.1
2023-03-09  In the Bloom filter optimization, hash all strings and blobs into the same value, because we do not know if two different strings might compare equal even if they have different byte sequences, due to collating functions. Formerly, the hash of a string or blob was just its length.  This could all be improved.
2023-03-09 Dan Kennedy Fix countofview.test so that it works with SQLITE_OMIT_PROGRESS_CALLBACK builds.
2023-03-09  Update the version number to 3.41.1
2023-03-09  Merge count-of-view optimization fixes from trunk.  But count-of-view is still off by default for this branch.
2023-03-09  Fix a possible NULL pointer dereference due to the sqlite3_interrupt() enhancement in the 3.41.0 release.
2023-03-08  Keep the historical datatype ("INT", not "NUM") for a table created as follows: "CREATE TABLE t1 AS SELECT CAST(123 AS INT) AS value;".  The use of FLEXNUM only occurs on compound queries.
2023-03-08  Fix an assertion fault added by [65ffee234787213c].
2023-03-04  Cherry-pick the agg-with-indexed-expr optimization fix from trunk.
2023-03-03  Do not use an expression index on a generated column if generated column has the wrong affinity.
2023-03-03  Enhance PRAGMA integrity_check so that it can detect when there are extra bytes at the end of an index record, which might cause OP_IdxRowid to malfunction.
2023-03-03  When it is known when preparing a statement that X cannot be NULL, transform the expression (X IS NULL) to integer value 1 instead of 'true'. This is because under some circumstances, "Y IS TRUE" may not be equivalent to "Y IS 1".
2023-03-02  When flattening the right operand of a LEFT JOIN, ensure that the OP_IfNullRow opcode does not NULL-out a subquery result that was computed within OP_Once.
2023-03-01  When flattening a view that is the right operand of a LEFT JOIN always insert the TK_IF_NULL_ROW expression nodes, even for TK_COLUMN expressions, as the TK_COLUMN might be a column from an outer query and hence still need to be NULLed out.
2023-03-01  Make sure subtypes do not cross a subquery boundary even if the function that returned the value with a subtype is buried down inside a larger expression.
2023-02-26  When a table-valued function appears as the right table of a RIGHT JOIN, the argument constraints on the table-valued function should be considered part of the ON clause of the RIGHT JOIN.
2023-02-23  Provide -DHAVE_LOG2=0 and -DHAVE_LOG10=0 compile-time options for use on systems that lack the log2() and log10() standard math library routines, to cause SQLite to substitute its own alternatives.

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit 4c1b1f8039c53009cfb9abef8ac003d616fa1a09)

Bug: 1426903, 1430644
Change-Id: Idc39b0c87be7152582c78f7eb6e53dd2d04b2b48
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4404861
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1127286}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4409783
Cr-Commit-Position: refs/branch-heads/5672@{#578}
Cr-Branched-From: 5f2a72468eda1eb945b3b5a2298b5d1cd678521e-refs/heads/main@{#1121455}

[modify] https://crrev.com/b45bc0a62c6e4aa92e9c7dec4f28c66ec3c85755/third_party/sqlite/README.chromium
[modify] https://crrev.com/b45bc0a62c6e4aa92e9c7dec4f28c66ec3c85755/DEPS


### am...@chromium.org (2023-04-17)

VRP reward information sent to finance team for payment processing on 14 April, updating labels accordingly 

### am...@chromium.org (2023-04-17)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1430644?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063900)*
