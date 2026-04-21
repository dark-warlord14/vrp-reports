# Security: Another UAF in WebSQL sqlite3Select

| Field | Value |
|-------|-------|
| **Issue ID** | [40060336](https://issues.chromium.org/issues/40060336) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL, Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | ay...@chromium.org |
| **Created** | 2022-07-20 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**

# Note

1. I found this unique case while reviewing the crash. This bug \*\*is a completely different bug from\*\* <https://bugs.chromium.org/p/chromium/issues/detail?id=1343348>, \*\*nor is it a patch bypass.\*\*
2. Based on our current testing, it has been in Chrome for at least 7 years and is still present in the latest version of Chrome. \*\*The earliest version that has been successfully verified is SQLite 3.9.0, 2015.\*\*
3. Since I have submitted multiple non-interactive WebSQL vulnerabilities before, clusterfuzz can't reproduce it, \*\*I think you should tag ClusterFuzz-Wrong and not use it to reproduce.\*\*  
   
   I've tested the scope of this vulnerability for you, so please feel free to merge it into the earliest LTS release you're currently maintaining, as it's really exist for too long.
4. This is also a serious UAF, which can cause similar effects to the previous vulnerability(issue-1343348) and can cause arbitrary address read under certain conditions, please read the following.

# Root Cause

[0] When the sqlite3Select function is processing the select statement, it will traverse the pEList, pOrderBy and pHaving node on the select statement, and save all the pointers of AGG\_FUNCTION and AGG\_COLUMN to pAggInfo.

[1] After that, the sqlite3Select function calls the selectInnerLoop function to generate code for the pEList node. If the pEList node at this time is still a multiSelect statement, the sqlite3Select function will be recursively called for code generation, and the sqlite3Select function will then call the multiSelect function.

[2] The multiSelect function will then call the resolveAlias function to process the pOrderBy node in the select statement. Because of the data change, this function \*\*will delete all child nodes on the pOrderBy node\*\* and replace it with new data. Note that the pOrderBy node itself will not be deleted.

[3] However, in the deleted child node of pOrderBy, there may be an AGG\_FUNCTION, and its pointer is recorded in the previous pAggInfo. This pointer will be used in the subsequent resetAccumulator function, which causes a UAF vulnerability.

[0]

```
sqlite3ExprAnalyzeAggList(&sNC, pEList);  
sqlite3ExprAnalyzeAggList(&sNC, sSort.pOrderBy);  
if( pHaving ){  
  if( pGroupBy ){  
    assert( pWhere==p->pWhere );  
    assert( pHaving==p->pHaving );  
    assert( pGroupBy==p->pGroupBy );  
    havingToWhere(pParse, p);  
    pWhere = p->pWhere;  
  }  
  sqlite3ExprAnalyzeAggregates(&sNC, pHaving);  
}  

```

[1]

```
finalizeAggFunctions(pParse, pAggInfo);   
sqlite3ExprIfFalse(pParse, pHaving, addrOutputRow+1, SQLITE_JUMPIFNULL);  
selectInnerLoop(pParse, p, -1, &sSort,  
                &sDistinct, pDest,  
                addrOutputRow+1, addrSetAbort); //---->[1]  

```
```
if( p->pPrior ){  
  rc = multiSelect(pParse, p, pDest); //---->[1]  
#if TREETRACE_ENABLED  
  SELECTTRACE(0x1,pParse,p,("end compound-select processing\n"));  
  if( (sqlite3TreeTrace & 0x2000)!=0 && ExplainQueryPlanParent(pParse)==0 ){  
    sqlite3TreeViewSelect(0, p, 0);  
  }  
#endif  
  if( p->pNext==0 ) ExplainQueryPlanPop(pParse);  
  return rc;  
}  

```
```
/\* Compound SELECTs that have an ORDER BY clause are handled separately.  
\*/  
if( p->pOrderBy ){  
    return multiSelectOrderBy(pParse, p, pDest); //---->[1]  
}else{  
    //......  
}  

```
```
pPrior->pOrderBy = sqlite3ExprListDup(pParse->db, pOrderBy, 0);  
sqlite3ResolveOrderGroupBy(pParse, p, p->pOrderBy, "ORDER"); //---->[1]  
sqlite3ResolveOrderGroupBy(pParse, pPrior, pPrior->pOrderBy, "ORDER");  //---->[1]  

```
```
for(i=0, pItem=pOrderBy->a; i<pOrderBy->nExpr; i++, pItem++){  
  if( pItem->u.x.iOrderByCol ){  
    if( pItem->u.x.iOrderByCol>pEList->nExpr ){  
      resolveOutOfRangeError(pParse, zType, i+1, pEList->nExpr, 0);  
      return 1;  
    }  
    resolveAlias(pParse, pEList, pItem->u.x.iOrderByCol-1, pItem->pExpr,0); //---->[1]  
  }  
}  

```

[2]

```
ExprSetProperty(pExpr, EP_Static);  
sqlite3ExprDelete(db, pExpr); //---->[2]  
memcpy(pExpr, pDup, sizeof(\*pExpr));  

```

[3]

```
selectInnerLoop(pParse, p, -1, &sSort,  
                &sDistinct, pDest,  
                addrOutputRow+1, addrSetAbort);  
sqlite3VdbeAddOp1(v, OP_Return, regOutputRow);  
VdbeComment((v, "end groupby result generator"));  
  
/\* Generate a subroutine that will reset the group-by accumulator  
\*/  
sqlite3VdbeResolveLabel(v, addrReset);  
resetAccumulator(pParse, pAggInfo); //---->[3]  

```
```
static void resetAccumulator(Parse \*pParse, AggInfo \*pAggInfo) {  
//......  
for(pFunc=pAggInfo->aFunc, i=0; i<pAggInfo->nFunc; i++, pFunc++){  
    if( pFunc->iDistinct>=0 ){  
	      Expr \*pE = pFunc->pFExpr;  
	      assert( ExprUseXList(pE) );  
	      if( pE->x.pList==0 || pE->x.pList->nExpr!=1 ){ //---->[3]  
	        sqlite3ErrorMsg(pParse, "DISTINCT aggregates must have exactly one "  
	           "argument");  
	        pFunc->iDistinct = -1;  
	      }else{  
	        KeyInfo \*pKeyInfo = sqlite3KeyInfoFromExprList(pParse, pE->x.pList,0,0);  
	        pFunc->iDistAddr = sqlite3VdbeAddOp4(v, OP_OpenEphemeral,  
	            pFunc->iDistinct, 0, 0, (char\*)pKeyInfo, P4_KEYINFO);  
	        ExplainQueryPlan((pParse, 0, "USE TEMP B-TREE FOR %s(DISTINCT)",  
	                          pFunc->pFunc->zName));  
	      }  
	    }  
	  }  
//......  
}  

```
# potential exploitable

It is a uaf vulnerability caused by the deletion of the OrderBy node, but the pointer is still stored in pAggInfo.  

At the same time, the use points of the two uaf vulnerabilities are the same.  

Therefore, the exploitability of this vulnerability can refer to the previous uaf vulnerability.  

For heap spraying, please refer to the previous vulnerability(issue-1343348), here I only supplement the part of arbitrary address read:

## Info Leak

[0] In the resetAccumulator function, we can arbitrarily control what the pE pointer points to, so we can fake any pE->x.pList and pass it to the sqlite3KeyInfoFromExprList function.

```
sqlite3VdbeAddOp3(v, OP_Null, 0, pAggInfo->mnReg, pAggInfo->mxReg);  
for(pFunc=pAggInfo->aFunc, i=0; i<pAggInfo->nFunc; i++, pFunc++){  
  if( pFunc->iDistinct>=0 ){  
    Expr \*pE = pFunc->pFExpr;  
    assert( ExprUseXList(pE) );  
    if( pE->x.pList==0 || pE->x.pList->nExpr!=1 ){  
      sqlite3ErrorMsg(pParse, "DISTINCT aggregates must have exactly one "  
         "argument");  
      pFunc->iDistinct = -1;  
    }else{  
      KeyInfo \*pKeyInfo = sqlite3KeyInfoFromExprList(pParse, pE->x.pList,0,0); // --->[0]  
      pFunc->iDistAddr = sqlite3VdbeAddOp4(v, OP_OpenEphemeral,  
          pFunc->iDistinct, 0, 0, (char\*)pKeyInfo, P4_KEYINFO);  
      ExplainQueryPlan((pParse, 0, "USE TEMP B-TREE FOR %s(DISTINCT)",  
                        pFunc->pFunc->zName));  
    }  

```

[1] Next, in the sqlite3KeyInfoFromExprList function, we can control each pIem->pExpr and then enter the sqlite3ExprNNCollSeq function.

```
if( pInfo ){  
  assert( sqlite3KeyInfoIsWriteable(pInfo) );  
  for(i=iStart, pItem=pList->a+iStart; i<nExpr; i++, pItem++){  
    pInfo->aColl[i-iStart] = sqlite3ExprNNCollSeq(pParse, pItem->pExpr); //---->[1]  
    pInfo->aSortFlags[i-iStart] = pItem->fg.sortFlags;  
  }  
}  

```

[2] Next we will enter the sqlite3ExprCollSeq function, note that the pExpr parameter here can be controlled arbitrarily.  

There are multiple branches in this function that can be exploited by an attacker.

```
SQLITE_PRIVATE CollSeq \*sqlite3ExprCollSeq(Parse \*pParse, const Expr \*pExpr){  
sqlite3 \*db = pParse->db;  
CollSeq \*pColl = 0;  
const Expr \*p = pExpr;  
while( p ){  
  int op = p->op;  
  if( op==TK_REGISTER ) op = p->op2;  
  if( op==TK_AGG_COLUMN || op==TK_COLUMN || op==TK_TRIGGER ){  
    assert( ExprUseYTab(p) );  
    if( p->y.pTab!=0 ){  
      /\* op==TK_REGISTER && p->y.pTab!=0 happens when pExpr was originally  
      \*\* a TK_COLUMN but was previously evaluated and cached in a register \*/  
      int j = p->iColumn;  
      if( j>=0 ){  
        const char \*zColl = sqlite3ColumnColl(&p->y.pTab->aCol[j]);  
        pColl = sqlite3FindCollSeq(db, ENC(db), zColl, 0);  
      }  
      break;  
    }  
  }  
  if( op==TK_CAST || op==TK_UPLUS ){  
    p = p->pLeft;  
    continue;  
  }  
  if( op==TK_VECTOR ){  
    assert( ExprUseXList(p) );  
    p = p->x.pList->a[0].pExpr;  
    continue;  
  }  
  if( op==TK_COLLATE ){  
    assert( !ExprHasProperty(p, EP_IntValue) );  
    pColl = sqlite3GetCollSeq(pParse, ENC(db), 0, p->u.zToken);  
    break;  
  }  
//......  

```

[3] We can choose the sqlite3GetCollSeq function to use, and control zName to be an address where we want to leak information. At the end of this function, the sqlite3ErrorMsg function will output the content pointed to by zName, which will cause information-leak.

```
SQLITE_PRIVATE CollSeq \*sqlite3GetCollSeq(  
  Parse \*pParse,        /\* Parsing context \*/  
  u8 enc,               /\* The desired encoding for the collating sequence \*/  
  CollSeq \*pColl,       /\* Collating sequence with native encoding, or NULL \*/  
  const char \*zName     /\* Collating sequence name \*/  
){  
  CollSeq \*p;  
  sqlite3 \*db = pParse->db;  
  
  p = pColl;  
  if( !p ){  
    p = sqlite3FindCollSeq(db, enc, zName, 0);  
  }  
  if( !p || !p->xCmp ){  
    /\* No collation sequence of this type for this encoding is registered.  
    \*\* Call the collation factory to see if it can supply us with one.  
    \*/  
    callCollNeeded(db, enc, zName);  
    p = sqlite3FindCollSeq(db, enc, zName, 0);  
  }  
  if( p && !p->xCmp && synthCollSeq(db, p) ){  
    p = 0;  
  }  
  assert( !p || p->xCmp );  
  if( p==0 ){  
    sqlite3ErrorMsg(pParse, "no such collation sequence: %s", zName); //---->[4]  
    pParse->rc = SQLITE_ERROR_MISSING_COLLSEQ;  
  }  
  return p;  
}  

```
# Patch

This is a for SQLite-3.39.1: <https://sqlite.org/2022/sqlite-amalgamation-3390100.zip>

```
@@ -101530,11 +101530,17 @@  
   Expr \*pOrig;           /\* The iCol-th column of the result set \*/  
   Expr \*pDup;            /\* Copy of pOrig \*/  
   sqlite3 \*db;           /\* The database connection \*/  
+  Expr\* pTmp;  
   
   assert( iCol>=0 && iCol<pEList->nExpr );  
   pOrig = pEList->a[iCol].pExpr;  
   assert( pOrig!=0 );  
   db = pParse->db;  
+  pTmp = sqlite3Malloc(sizeof(\*pExpr));  
+  if (!pTmp){  
+    sqlite3OomFault(db);  
+    return;  
+  }  
   pDup = sqlite3ExprDup(db, pOrig, 0);  
   if( db->mallocFailed ){  
     sqlite3ExprDelete(db, pDup);  
@@ -101553,8 +101559,11 @@  
     \*\* sqlite3DbFree(db, pDup) on the last line of this block, so be sure to  
     \*\* make a copy of the token before doing the sqlite3DbFree().  
     \*/  
-    ExprSetProperty(pExpr, EP_Static);  
-    sqlite3ExprDelete(db, pExpr);  
+    memcpy(pTmp, pExpr, sizeof(\*pExpr));  
+    sqlite3ParserAddCleanup(pParse,  
+      (void(\*)(sqlite3\*,void\*))sqlite3ExprDelete,  
+      pTmp);  
+    pTmp = 0;  
     memcpy(pExpr, pDup, sizeof(\*pExpr));  
     if( !ExprHasProperty(pExpr, EP_IntValue) && pExpr->u.zToken!=0 ){  
       assert( (pExpr->flags & (EP_Reduced|EP_TokenOnly))==0 );  

```

This is a temporary solution to consider, and it provides a suggestion to fix the sqlite3ExprDelete function call in the resolveAlias function.

**VERSION**  

Chrome Version: Chrome + stable, beta, and dev  

Operating System: All

**REPRODUCTION CASE**

# Reproduce

1. Download Chromium with asan from: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1026222.zip?generation=1658328132136422&alt=media>
2. python3 -m http.server 8000
3. Run: `/path/to/asan-linux-release-1026222/chrome-wrapper --user-data-dir=./userdata http://127.0.0.1:8000/poc.html 2>&1 | /media/sakura/sakura_T7/chromium/src/tools/valgrind/asan/asan_symbolize.py`
4. click Trigger Button

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see asan log

**CREDIT INFORMATION**  

Reporter credit:  

Ziling Chen and Nan Wang(@eternalsakura13) of 360 Vulnerability Research Institute

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 24.5 KB)
- [poc.sql](attachments/poc.sql) (text/plain, 245 B)
- [poc.html](attachments/poc.html) (text/plain, 2.0 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 9.6 MB)

## Timeline

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### aj...@google.com (2022-07-20)

[Empty comment from Monorail migration]

### aj...@google.com (2022-07-20)

(I have not attempted a repro but this follows https://crbug.com/chromium/1343348 so I have CC'd the same folks)

### et...@gmail.com (2022-07-20)

About reproduce:
1. please use chromium with asan，The download link I provided is the latest chromium release with asan that can be downloaded at present, you can use that
2. If you want to try to reproduce in sqlite, you can also try this poc sql, of course the above poc.sql should also be reproduced, but it may not be as extensive.
I verified all from 3.9.0-3.40.0
````
CREATE TABLE t0(c0);
CREATE TABLE t1(c0);
CREATE TABLE t2(c0);
WITH t1 AS (SELECT * FROM ( SELECT 1 ) UNION ALL VALUES ( 1 ), ( 1 ) ) SELECT (SELECT ( SELECT sum(DISTINCT c0 IN t2) ) FROM t1 ORDER BY 1 ) FROM t0 GROUP BY 0xffffffff;
````

### dr...@gmail.com (2022-07-20)

The problem has now been resolved by check-in e1f1cfe7f4387b60 (https://sqlite.org/src/timeline?c=e1f1cfe7f4387b60).

You may want to consider using the latest check-in on branch-3.39 (https://sqlite.org/src/timeline?r=branch-3.39).  Branch-3.39 contains fixes for all known problems that were present in the latest release (3.39.1).  The tip of branch-3.39 will probably be released as 3.39.2 sometime soon.

These check-ins will get synced to the GitHub mirror for SQLite at some point (the cron that does that runs once per hour) but they have not yet landed as I write this so I cannot give you the GIt hash nor provide links.

### dr...@gmail.com (2022-07-20)

GitHub hashes and URLs are now available:

Trunk fix:  https://github.com/sqlite/sqlite/commit/3245f3be67907a31431a4506908d981ab1354523

Branch-3.39 check-in that is recommended for chromium:  https://github.com/sqlite/sqlite/commits/fd34e75b0a8994b2b96900c3237bc536127447d4

### as...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>WebSQL Internals>Storage]

### ay...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### rs...@chromium.org (2022-07-20)

Thanks for the report and fixing this so quickly. Assigning to ayui@ for another SQLite roll.

### [Deleted User] (2022-07-20)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### ay...@chromium.org (2022-07-20)

drhsqlite@ - Thanks for the quick fix! Could you create a new release that contains the fixes?

### rz...@google.com (2022-07-21)

[Empty comment from Monorail migration]

### dr...@gmail.com (2022-07-21)

SQLite version 3.39.2 is now available.  The GitHub link is https://github.com/sqlite/sqlite/commit/202b2a7b54ea2dd13a8a5adfd75523abe4dcf17f

### [Deleted User] (2022-07-21)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef

commit e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef
Author: Ayu Ishii <ayui@chromium.org>
Date: Thu Jul 21 17:54:42 2022

Amalgamations for release 3.39.2

Bug: 1345947
Change-Id: I5b5aed62a9c1530f26ca001840baad0c73b03862
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/sqlite/+/3780989
Reviewed-by: Joshua Bell <jsbell@chromium.org>

[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation_dev/README.md
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation_dev/sqlite3.c
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation/sqlite3.c
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation_dev/rename_exports.h
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation/shell/shell.c
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation_dev/shell/shell.c
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation/sqlite3.h
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation/README.md
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation/rename_exports.h
[add] https://crrev.com/e6b63421941617bf5ccac6b4a62d7a7b4a2c3fef/amalgamation_dev/sqlite3.h


### gi...@appspot.gserviceaccount.com (2022-07-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/4d60f205cee7a736b12d729cf946a620787e1a37

commit 4d60f205cee7a736b12d729cf946a620787e1a37
Author: Ayu Ishii <ayui@chromium.org>
Date: Thu Jul 21 22:32:54 2022

sqlite: Upgrade to 3.39.2

Roll src/third_party/sqlite/src/ 88f6139ea..e6b634219 (11 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/88f6139eadb1..e6b634219416

$ git log 88f6139ea..e6b634219 --date=short --no-merges --format='%ad %ae %s'
2022-07-21 ayui Amalgamations for release 3.39.2
2022-07-21  Version 3.39.2
2022-07-21  In the query planner, restore the former aggressiveness in reordering of FROM clause terms that existed prior to version 3.39.0 for queries that contain no RIGHT or FULL JOINs.
2022-07-20  Simplify the logic that converts the "1" expression in "ORDER BY 1" into a copy of the expression that defines the first output column.
2022-07-18  Increase the size of loop variables in the printf() implementation to avoid harmless compiler warnings.
2022-07-15 mistachkin Fix harmless compiler warnings seen with MSVC.
2022-07-15 Dan Kennedy Fix a memory leak in fts3 that could occur when processing a corrupt database.
2022-07-15  Fix the whereKeyStats() routine (part of STAT4 processing only) so that it is able to cope with row-value comparisons against the primary key index of a WITHOUT ROWID table. [forum:/forumpost/3607259d3c|Forum post 3607259d3c].
2022-07-15 Dan Kennedy Update some faulty assert() statements in fts3.
2022-07-14  Bump the version number up to 3.39.2.
2022-07-14  When applying the omit-ORDER-BY optimization, defer deleting the AST of the deleted ORDER BY clause until after code generation ends.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1345947
Change-Id: Ie752c0ffdc7ea03af66a1813c8103e947da16e44
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3780773
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Joshua Bell <jsbell@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1027006}

[modify] https://crrev.com/4d60f205cee7a736b12d729cf946a620787e1a37/third_party/sqlite/README.chromium
[modify] https://crrev.com/4d60f205cee7a736b12d729cf946a620787e1a37/DEPS


### ay...@chromium.org (2022-07-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-22)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-26)

[Empty comment from Monorail migration]

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2022-07-28)

Congratulations, Ziling Chen and Nan Wang! The VRP Panel has decided to award you $7500 for this report. Thank you for your efforts and great work! 

### rz...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-07-29)

1. https://crrev.com/c/3791343 and one more CL to roll the dep on chromium after merging this one
2. Low, no conflicts
3. 105
4. Yes

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-07-31)

Hi, @amyressler
Will Chrome stable 104 update the sqlite version(to 3.39.2) to fix this vulnerability and assign a CVE?  :)

### gm...@google.com (2022-08-01)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-12)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-12)

1. https://crrev.com/c/3827341 and a CL for rolling DEPS
2. Low, no conflicts
3. 105
4. Yes

### gm...@google.com (2022-08-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-08-31)

re https://crbug.com/chromium/1345947#c2:
hi, @ ajgo, @ayui, @asully
Hello, ziling and I have submitted two new WebSQL vulnerabilities (OOB Write and UAF), if you have time to help look at it, thank :)
https://bugs.chromium.org/p/chromium/issues/detail?id=1358392
https://bugs.chromium.org/p/chromium/issues/detail?id=1358381


### gm...@google.com (2022-09-12)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-13)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/d9eae184eb4aa7aca296ab59aba86a1dae451898

commit d9eae184eb4aa7aca296ab59aba86a1dae451898
Author: drh <>
Date: Tue Sep 13 15:37:52 2022

[M102-LTS] Simplify the logic that converts the "1" expression in "ORDER BY 1" into a
copy of the expression that defines the first output column.

Bug: 1345947
FossilOrigin-Name: e1f1cfe7f4387b60443bd31742e2f49db1a2d0443200318a898ba0da216619be
(cherry picked from commit 3245f3be67907a31431a4506908d981ab1354523)
Change-Id: Ie42c9f6638ae1c7bdbd9606a919c6c20ab5df4a7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/sqlite/+/3827341
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>

[modify] https://crrev.com/d9eae184eb4aa7aca296ab59aba86a1dae451898/src/resolve.c
[modify] https://crrev.com/d9eae184eb4aa7aca296ab59aba86a1dae451898/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/d9eae184eb4aa7aca296ab59aba86a1dae451898/amalgamation/sqlite3.c
[modify] https://crrev.com/d9eae184eb4aa7aca296ab59aba86a1dae451898/manifest
[modify] https://crrev.com/d9eae184eb4aa7aca296ab59aba86a1dae451898/amalgamation/sqlite3.h
[modify] https://crrev.com/d9eae184eb4aa7aca296ab59aba86a1dae451898/amalgamation_dev/sqlite3.h


### gi...@appspot.gserviceaccount.com (2022-09-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a295e5f221db468664688f9e03c9f66ba7cd621c

commit a295e5f221db468664688f9e03c9f66ba7cd621c
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Sep 14 16:52:13 2022

[M102-LTS] Roll src/third_party/sqlite/src/ 9328fbe3d..d9eae184e (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/9328fbe3d1e0..d9eae184eb4a

$ git log 9328fbe3d..d9eae184e --date=short --no-merges --format='%ad %ae %s'
2022-09-13  [M102-LTS] Simplify the logic that converts the "1" expression in "ORDER BY 1" into a copy of the expression that defines the first output column.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1345947
Change-Id: I19397c7f14ffe359d1ac9c44d8555fac9c23ba2f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3894439
Owners-Override: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1352}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/a295e5f221db468664688f9e03c9f66ba7cd621c/DEPS


### rz...@google.com (2022-09-15)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1345947?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>WebSQL, Internals>Storage]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060336)*
