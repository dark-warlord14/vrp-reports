# Security: Use After Free in WebSQL

| Field | Value |
|-------|-------|
| **Issue ID** | [40054252](https://issues.chromium.org/issues/40054252) |
| **Status** | Assigned |
| **Severity** | S4-Minimal |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2020-12-21 |
| **Bounty** | $5,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36

Steps to reproduce the problem:
You can reproduce this bug in two ways
[0] 
Download sqlite 3.33.0 or 3.34.0
gcc -DSQLITE_DEBUG shell.c sqlite3.c -pthread -ldl -o sqlite3
./sqlite3 < poc.sql

sakura@sakuradeMacBook-Pro:~/CLionProjects/sqlite_test_c$ ./sqlite3 < poc.sql 
Assertion failed: (pExpr->pAggInfo==pAggInfo), function sqlite3Select, file sqlite3.c, line 136695.
Abort trap: 6

or

[1] patch chromium
https://source.chromium.org/chromium/chromium/src/+/master:third_party/sqlite/src/amalgamation/sqlite3.c

In Function sqlite3DbFreeNN, Remove `#ifdef SQLITE_DEBUG`, used to trigger memory sanitizer
```
SQLITE_PRIVATE void sqlite3DbFreeNN(sqlite3 *db, void *p){
  assert( db==0 || sqlite3_mutex_held(db->mutex) );
  assert( p!=0 );
  if( db ){
    if( db->pnBytesFreed ){
      measureAllocationSize(db, p);
      return;
    }
    if( ((uptr)p)<(uptr)(db->lookaside.pEnd) ){
#ifndef SQLITE_OMIT_TWOSIZE_LOOKASIDE
      if( ((uptr)p)>=(uptr)(db->lookaside.pMiddle) ){
        LookasideSlot *pBuf = (LookasideSlot*)p;
- #ifdef SQLITE_DEBUG
        memset(p, 0xaa, LOOKASIDE_SMALL);  /* Trash freed content */
- #endif
        pBuf->pNext = db->lookaside.pSmallFree;
        db->lookaside.pSmallFree = pBuf;
        return;
      }
#endif /* SQLITE_OMIT_TWOSIZE_LOOKASIDE */
      if( ((uptr)p)>=(uptr)(db->lookaside.pStart) ){
        LookasideSlot *pBuf = (LookasideSlot*)p;
- #ifdef SQLITE_DEBUG
        memset(p, 0xaa, db->lookaside.szTrue);  /* Trash freed content */
- #endif
        pBuf->pNext = db->lookaside.pFree;
        db->lookaside.pFree = pBuf;
        return;
      }
    }
  }
  assert( sqlite3MemdebugHasType(p, (MEMTYPE_LOOKASIDE|MEMTYPE_HEAP)) );
  assert( sqlite3MemdebugNoType(p, (u8)~(MEMTYPE_LOOKASIDE|MEMTYPE_HEAP)) );
  assert( db!=0 || sqlite3MemdebugNoType(p, MEMTYPE_LOOKASIDE) );
  sqlite3MemdebugSetType(p, MEMTYPE_HEAP);
  sqlite3_free(p);
}
```

At the end of the function `SQLITE_PRIVATE int sqlite3Select`, perform the following patch
```
select_end:
  sqlite3ExprListDelete(db, pMinMaxOrderBy);
- #ifdef SQLITE_DEBUG
  if( pAggInfo && !db->mallocFailed ){
    for(i=0; i<pAggInfo->nColumn; i++){
      Expr *pExpr = pAggInfo->aCol[i].pCExpr;
      assert( pExpr!=0 || db->mallocFailed );
      if( pExpr==0 ) continue;
+     if( pExpr->pAggInfo != pAggInfo )
+         exit(-1);
      assert( pExpr->pAggInfo==pAggInfo );
      assert( pExpr->iAgg==i );
    }
    for(i=0; i<pAggInfo->nFunc; i++){
      Expr *pExpr = pAggInfo->aFunc[i].pFExpr;
      assert( pExpr!=0 || db->mallocFailed );
      if( pExpr==0 ) continue;
      assert( pExpr->pAggInfo==pAggInfo );
      assert( pExpr->iAgg==i );
    }
  }
- #endif
```

What is the expected behavior?

What went wrong?
- The AggInfo structure contains the information needed to generate code for a SELECT that contains aggregate functions.
- [0] analyzeAggregate
```
analyzeAggregate
->
if( (k>=pAggInfo->nColumn)
&& (k = addAggInfoColumn(pParse->db, pAggInfo))>=0
)
```
->
Allocate memory and save the address to the pInfo->aCol field
```
static int addAggInfoColumn(sqlite3 *db, AggInfo *pInfo){
int i;
pInfo->aCol = sqlite3ArrayAllocate(
db,
pInfo->aCol,
sizeof(pInfo->aCol[0]),
&pInfo->nColumn,
&i
);
return i;
}
```
Initialize pCol, which comes from pInfo->aCol just allocated
Save the address of pExpr to pCol->pCExpr
```
pCol = &pAggInfo->aCol[k];
...
pCol->pCExpr = pExpr;
...
```

Save the pAggInfo address to pExpr->pAggInfo
```
pExpr->pAggInfo = pAggInfo;
pExpr->op = TK_AGG_COLUMN;
pExpr->iAgg = (i16)k;
```

```
(lldb) p pAggInfo
(AggInfo *) \$125 = 0x000062e00000bca0
(lldb) p pExpr->pAggInfo
(AggInfo *) $126 = 0x000062e00000bca0

(lldb) p &pExpr->pAggInfo
(AggInfo **) $128 = 0x000062e00000abd8

(lldb) p &*pExpr
(Expr *) $129 = 0x000062e00000aba0

(lldb) watchpoint set expression -- 0x000062e00000aba0
Watchpoint created: Watchpoint 1: addr = 0x7ffeee147fb8 size = 8 state = enabled type = w
    new value: 108714212240288
```

- [1] In the process of havingToWhere, sqlite3DbFreeNN will be triggered to deconstruct pExpr.

As shown in the figure and the stack traceback, when processing havingToWhere, sqlite3DbFreeNN is triggered and Expr will be destroyed

```
(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = watchpoint 1
  * frame #0: 0x00007fff6f20edd9 libsystem_platform.dylib`_platform_bzero$VARIANT$Haswell + 57
    frame #1: 0x0000000107375eec libclang_rt.asan_osx_dynamic.dylib`__asan_memset + 300
    frame #2: 0x0000000106ba8163 main`sqlite3DbFreeNN(db=0x0000617000000400, p=0x000062e00000aba0) at sqlite3.c:27815:9
    frame #3: 0x0000000106d4c8da main`sqlite3ExprDeleteNN(db=0x0000617000000400, p=0x000062e00000aba0) at sqlite3.c:101306:5
    frame #4: 0x0000000106d4b908 main`sqlite3ExprDelete(db=0x0000617000000400, p=0x000062e00000aba0) at sqlite3.c:101310:11
    frame #5: 0x0000000106dc430f main`sqlite3ExprAnd(pParse=0x00007ffee90c89a0, pLeft=0x000062e00000aba0, pRight=0x000062e000009ca0) at sqlite3.c:101115:5
    frame #6: 0x0000000106eee9e7 main`havingToWhereExprCb(pWalker=0x00007ffee90bed80, pExpr=0x000062e00000b820) at sqlite3.c:135425:16
    frame #7: 0x0000000106e051cf main`walkExpr(pWalker=0x00007ffee90bed80, pExpr=0x000062e00000b820) at sqlite3.c:98028:10
    frame #8: 0x0000000106e05148 main`sqlite3WalkExpr(pWalker=0x00007ffee90bed80, pExpr=0x000062e00000b820) at sqlite3.c:98056:18
    frame #9: 0x0000000106e7cd44 main`havingToWhere(pParse=0x00007ffee90c89a0, p=0x000062e00000aea0) at sqlite3.c:135456:3
    frame #10: 0x0000000106da644f main`sqlite3Select(pParse=0x00007ffee90c89a0, p=0x000062e00000aea0, pDest=0x00007ffee90c0800) at sqlite3.c:136264:9
    frame #11: 0x0000000106df946a main`sqlite3CodeSubselect(pParse=0x00007ffee90c89a0, pExpr=0x000062e00000b3a0) at sqlite3.c:103275:7
    frame #12: 0x0000000106deddc5 main`sqlite3ExprCodeTarget(pParse=0x00007ffee90c89a0, pExpr=0x000062e00000b3a0, target=21) at sqlite3.c:104446:16
    frame #13: 0x0000000106df626f main`sqlite3ExprCodeExprList(pParse=0x00007ffee90c89a0, pList=0x000062e00000baa0, target=21, srcReg=0, flags=1 '\x01') at sqlite3.c:104904:19
    frame #14: 0x0000000106eec687 main`innerLoopLoadRow(pParse=0x00007ffee90c89a0, pSelect=0x000062e00000af20, pInfo=0x00007ffee90c1ee0) at sqlite3.c:130347:3
    frame #15: 0x0000000106e76913 main`selectInnerLoop(pParse=0x00007ffee90c89a0, p=0x000062e00000af20, srcTab=-1, pSort=0x0000000000000000, pDistinct=0x00007ffee90c2540, pDest=0x00007ffee90c3ec0, iContinue=65, iBreak=62) at sqlite3.c:130801:7
    frame #16: 0x0000000106da8cc7 main`sqlite3Select(pParse=0x00007ffee90c89a0, p=0x000062e00000af20, pDest=0x00007ffee90c3ec0) at sqlite3.c:136519:7
    frame #17: 0x0000000106d72dc2 main`yy_reduce(yypParser=0x00007ffee90c7a70, yyruleno=82, yyLookahead=1, yyLookaheadToken=(z = ";", n = 1), pParse=0x00007ffee90c89a0) at sqlite3.c:158623:3
    frame #18: 0x0000000106d6d12b main`sqlite3Parser(yyp=0x00007ffee90c7a70, yymajor=1, yyminor=(z = ";", n = 1)) at sqlite3.c:159923:15
    frame #19: 0x0000000106b887e5 main`sqlite3RunParser(pParse=0x00007ffee90c89a0, zSql=";", pzErrMsg=0x00007ffee90c8980) at sqlite3.c:161204:5
    ...
```
LOOKASIDE_SMALL = 128

In the debug version, the first 128 bytes of the memory pointed to by pExpr are set to 0xaa, which is equivalent to a memory sanitizer.

- [2] Potential uaf check is triggered
After sqlite3DbFreeNN() destructs Expr, it can still be referenced to Expr through `Expr *pExpr = pAggInfo->aCol[i].pCExpr`. Because of sanitizer, the pointer to AggInfo saved in pExpr->pAggInfo is set to 0xaaaaaaaaaaaaaaaa , Crash occurs when assert is not satisfied.
```
SQLITE_PRIVATE int sqlite3Select(
  Parse *pParse,         /* The parser context */
  Select *p,             /* The SELECT statement being coded. */
  SelectDest *pDest      /* What to do with the query results */
){
...
...
select_end:
  sqlite3ExprListDelete(db, pMinMaxOrderBy);
#ifdef SQLITE_DEBUG
  if( pAggInfo && !db->mallocFailed ){
    for(i=0; i<pAggInfo->nColumn; i++){
      Expr *pExpr = pAggInfo->aCol[i].pCExpr;
      assert( pExpr!=0 || db->mallocFailed );
      if( pExpr==0 ) continue;
      assert( pExpr->pAggInfo==pAggInfo );// assert crash here
      assert( pExpr->iAgg==i );
    }
...
```
- [3] other
Because the SQL code that triggers this assert is very simple and satisfies Chrome's SQL whitelist.
By applying the patch I provided, you can observe the render crash.

After sqlite3DbFreeNN() constructs Expr, it can still be referenced to pExpr through `Expr *pExpr = pAggInfo->aCol[i].pCExpr`.

Although the corresponding SQLITE_DEBUG code does not exist in the release version, since the address of the destructed pExpr is always stored in pAggInfo, there may be potential points of use leading to the generation of uaf.

Did this work before? N/A 

Chrome version: 87.0.4280.88  Channel: stable
OS Version: OS X 10.15.7
Flash Version: 

Because I am not very familiar with sqlite, I only use fuzz to test it, I don’t know how to directly construct an asan crash in Chrome, but because this poc reflects the potential UAF risk and can be triggered in chrome, I report it to you.
If my understanding is wrong, please let me know.

## Attachments

- [Screenshot from 2020-12-21 10-58-34.png](attachments/Screenshot from 2020-12-21 10-58-34.png) (image/png, 182.3 KB)
- [oob.html](attachments/oob.html) (text/plain, 1.9 KB)
- [poc.sql](attachments/poc.sql) (text/plain, 92 B)

## Timeline

### [Deleted User] (2020-12-21)

[Empty comment from Monorail migration]

### et...@gmail.com (2020-12-21)

  if( pAggInfo && !db->mallocFailed ){
    for(i=0; i<pAggInfo->nColumn; i++){
      Expr *pExpr = pAggInfo->aCol[i].pCExpr;
      assert( pExpr!=0 || db->mallocFailed );
      if( pExpr==0 ) continue;
      assert( pExpr->pAggInfo==pAggInfo ); // crash here
      assert( pExpr->iAgg==i );
    }
...
(lldb) p pExpr->pAggInfo
(AggInfo *) $16 = 0xaaaaaaaaaaaaaaaa
(lldb) p *(Expr *)pExpr
(Expr) $17 = {
  op = '\x01' 1 '\x01'
  affExpr = '\0' 0 '\0'
  op2 = '\0' 0 '\0'
  vvaFlags = '\0' 0 '\0'
  flags = 65537
  u = (zToken = "", iValue = -1431699454)
  pLeft = 0x0000617000000400
  pRight = 0x000062e00000abd0
  x = {
    pList = 0x000060c0000001c0
    pSelect = 0x000060c0000001c0
  }
  nHeight = 0
  iTable = 0
  iColumn = 0
  iAgg = -21846
  iRightJoinTable = -21846
  pAggInfo = 0xaaaaaaaaaaaaaaaa
  y = {
    pTab = 0xaaaaaaaaaaaaaaaa
    pWin = 0xaaaaaaaaaaaaaaaa
    sub = (iAddr = -1431655766, regReturn = -1431655766)
  }
}
(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = signal SIGABRT
  * frame #0: 0x00007fff6f16033a libsystem_kernel.dylib`__pthread_kill + 10
    frame #1: 0x00007fff6f21ce60 libsystem_pthread.dylib`pthread_kill + 430
    frame #2: 0x00007fff6f0e7808 libsystem_c.dylib`abort + 120
    frame #3: 0x00007fff6f0e6ac6 libsystem_c.dylib`__assert_rtn + 314
    frame #4: 0x0000000106b94fb2 main`sqlite3Select(pParse=0x00007ffee92de9a0, p=0x000062e00000ae20, pDest=0x00007ffee92d9ec0) at sqlite3.c:136695:7
    frame #5: 0x0000000106b5d4b2 main`yy_reduce(yypParser=0x00007ffee92dda70, yyruleno=82, yyLookahead=1, yyLookaheadToken=(z = ";", n = 1), pParse=0x00007ffee92de9a0) at sqlite3.c:158623:3
    frame #6: 0x0000000106b5781b main`sqlite3Parser(yyp=0x00007ffee92dda70, yymajor=1, yyminor=(z = ";", n = 1)) at sqlite3.c:159923:15

### cl...@chromium.org (2020-12-21)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5690559888162816.

### pa...@chromium.org (2020-12-21)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>WebSQL]

### hu...@chromium.org (2020-12-22)

Per the description, the provided repro doesn't repro on Chrome stable (without patches), but it's very possible that this could lead to a UaF on Chrome Stable, so I'll tentatively mark this as impact-stable.

Sqlite v3.33.0 has been available since M86 (per https://crbug.com/1117367).

### hu...@chromium.org (2020-12-22)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Storage>WebSQL Internals>Storage]

### hu...@chromium.org (2020-12-22)

Dr. Hipp and Daniel (sqlite authors), please take a look? Fairly detailed information available in the description.

This should be easier to repro by building sqlite directly via gcc and the attached repro.sql. I could certainly try reproducing this in Chrome as well, but it seems a bit more complex to do that due to the need for some patches.

### dr...@gmail.com (2020-12-22)

The problem is easy to reproduce (without using Chrome) simply by redirecting the poc.sql file as input to the SQLite command-line shell:  "sqlite3 <poc.sql".

The assert() that fires is part of our defense-in-depth logic.  The poc.sql file does not cause any memory errors or other exploitable problems, as far as we can tell.  But it does result in data structures being set up in ways that we thought were impossible and have therefore not extensively analyzed and which could potentially be dangerous.  That is the whole point of this assert() (and others like it) - to cause crashes in fuzzers when those fuzzers find innovative ways of going outside of the established flight envelope.

So, this is not (yet) a vulnerability of any kind.  But it is useful information that will help us to improve SQLite.  We will analyze the situation more carefully over the next day or so and let you know what we find.

### [Deleted User] (2020-12-22)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-12-22)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### et...@gmail.com (2021-01-04)

Hello, is anyone still reviewing this issue?Thanks : ) 

### da...@gmail.com (2021-01-04)

Hi,

Looks like it was fixed here:

  https://sqlite.org/src/info/f62f983b56623f0e

Thanks,
Dan.


### et...@gmail.com (2021-01-04)

Hello, danie. After your review, whether this issue may cause a security problem(such as UAF)? thank you very much :)


### da...@gmail.com (2021-01-04)

This bug can cause a read-after-free of the internal data structure used to store the expression for the WHERE clause of the inner sub-query on release builds as well. That's about all we can say for sure.

Dan.


### et...@gmail.com (2021-01-05)

hello,  @huangdarwin, Because this can indeed lead to a UAF vulnerability, can you confirm that this is a security issue and assign me a cve, thank you very much :)

### [Deleted User] (2021-01-05)

huangdarwin: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2021-01-05)

Hey eternalsakuraalpha@, yes, this does seem like a security issue in Chromium, per https://crbug.com/chromium/1160602#c14. Therefore, I'll leave the Security_Severity-High label we previously added.

To get a CVE, I believe I need to first patch this in Chromium (backport https://crbug.com/chromium/1160602#c12's patch), and then mark this as "Fixed" for some automated process to handle this, but I'll cc adetaylor@ as well for now to confirm the CVE process.

### hu...@chromium.org (2021-01-05)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-05)

The bug merged in in https://crbug.com/chromium/1160602#c18 was filed later, but provides a concrete and easy-to-repro UaF/trace without a patch in Chromium. Merging here to organize.

### ad...@chromium.org (2021-01-05)

Yes, we allocate CVE numbers when we release a fix.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/702a79c7d77331cbe2838c4b3c5fab529f75f7c2

commit 702a79c7d77331cbe2838c4b3c5fab529f75f7c2
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Tue Jan 05 20:15:33 2021

Fix a problem handling sub-queries with both a correlated WHERE clause and a "HAVING 0" clause where the parent query is itself an aggregate.

FossilOrigin-Name: f62f983b56623f0ec34f9a54ce1c21b013a20399162f5ee6ee43b23f10c2ecd5
(cherry picked from commit f39168e468af3b1d6b6d37efdcb081eced6724b2)
Bug: 1160602
Change-Id: I76aaeedc167c8ed8a9b47805cd6ebb29fba0a704

[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/src/select.c
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/amalgamation_dev/sqlite3.h
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/manifest.uuid
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/amalgamation/sqlite3.c
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/manifest
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/amalgamation/sqlite3.h
[modify] https://crrev.com/702a79c7d77331cbe2838c4b3c5fab529f75f7c2/test/having.test


### et...@gmail.com (2021-01-07)

cve credit: Nan Wang(@eternalsakura13) and Guang Gong of 360 Alpha Lab 
thanks :)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f45eb0a910b0dd653a013b81aed4395afdfd4395

commit f45eb0a910b0dd653a013b81aed4395afdfd4395
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Thu Jan 07 09:00:07 2021

Roll src/third_party/sqlite/src/ d9581878f..702a79c7d (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/d9581878fcf8..702a79c7d773

$ git log d9581878f..702a79c7d --date=short --no-merges --format='%ad %ae %s'
2020-12-30 huangdarwin Fix a problem handling sub-queries with both a correlated WHERE clause and a "HAVING 0" clause where the parent query is itself an aggregate.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1160602
Change-Id: Ie960e77153efcb9205cb8369d03623a44a883597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2613955
Auto-Submit: Darwin Huang <huangdarwin@chromium.org>
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#840978}

[modify] https://crrev.com/f45eb0a910b0dd653a013b81aed4395afdfd4395/DEPS


### hu...@chromium.org (2021-01-07)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-07)

This affects sqlite v3.33.0+, so should affect M86+[1].

M88 is fairly close[2] to stable cut, so this may not have much time to bake, but I believe the patch is quite small/safe, with only ~1 line[3][4] of executable diff, and does fix a UaF, which is considered Security_Severity-High. Therefore, requesting merge to M88 (maybe right before stable cut on 2021-01-12 to allow some time to bake).

[1]: https://crrev.com/c/2466502
[2]: https://chromiumdash.appspot.com/schedule
[3]: https://sqlite.org/src/info/f62f983b56623f0e
[4]: https://crrev.com/c/2607419

### [Deleted User] (2021-01-07)

This bug requires manual review: We are only 11 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2021-01-07)

@adetaylor to chime in his thoughts on the timeline for M88 and see how to get this fix into M88 stable RC. or first re-spin

### ad...@google.com (2021-01-07)

The change itself is small. Approving merge to M88, branch 4324 - but Darwin, please could you wait for 24 hours of Canary coverage first?

### cl...@chromium.org (2021-01-07)

ClusterFuzz testcase 5647227661123584 is verified as fixed in https://clusterfuzz.com/revisions?job=libfuzzer_chrome_asan_debug&range=840975:840981

If this is incorrect, please add the ClusterFuzz-Wrong label and re-open the issue.

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-08)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-09)

Sorry adetaylor@, I misspoke when saying this cherry-picking change to M88 is only 1 line of diff... In reality, the CL to fix this specific bug is only 1 line of diff, but putting it on M88 will require updating sqlite from v.3.33.0 to v3.34.0, which is a very large change.

I'll restore this to merge-request to re-request the merge approval. This may still be worth a merge due to the UaF, and because we haven't seen any new sqlite issues come up since v3.34.0 has been in canary (about 1.5 weeks ago), but isn't a small change anymore. Could you please re-review whether we should put this into M88? Thanks!

To summarize, putting this change into M88 will require these 2 patches, both of which haven't had any issues spotted yet:
- https://crrev.com/c/2600334 - Merged 2020-12-29 - sqlite v3.34.0 update (171 commits, many lines executable diff)
- https://crrev.com/c/2613955 - Merged 2021-01-07 - Fix for this issue's UaF (1 commit, 1 line executable diff)

### [Deleted User] (2021-01-09)

This bug requires manual review: We are only 9 days from stable.
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
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), srinivassista @(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2021-01-09)

1. Yes. UaFs are security bugs. In this case the executable diff after merge might be a bit large, but we'd be shipping an identical version of sqlite as tested in canary so I don't think risk is too great.
2. https://crrev.com/c/2618998
3. Yes (as of 2020-01-07)
4. No.
5. Security_Severity-High discovered after branch.
6. No.
7. N/A

(See https://crbug.com/chromium/1160602#c32 for more info)

### pw...@chromium.org (2021-01-09)

I'll doing the merge assuming this request gets approved while huangdarwin@ is OOO.

### ad...@google.com (2021-01-11)

OK, so by the time we actually release this (on Jan 19th) it will have had nearly 2.5 weeks in Canary. Re-approving merge to M88, branch 4324.

### go...@chromium.org (2021-01-11)

Please merge your change to M88 branch 4324 ASAP so we can take it in for M88 Stable RC cut tomorrow. Thank you.

### sr...@google.com (2021-01-11)

Please complete your merge before Tuesday Jan 12 2pm PST, if you are in a different time zone , stable RC will be cut tomorrow so we need your help to get these all completed to be included in the final build for M88

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/fc8a77fa1428041a0e19df31e4502babf5e20445

commit fc8a77fa1428041a0e19df31e4502babf5e20445
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Tue Jan 12 00:41:46 2021

Roll src/third_party/sqlite/src/ 0324bd3ef..702a79c7d (172 commits) (M88)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/0324bd3ef..702a79c7d773

Contains commits from:
- https://crrev.com/c/2600334, a sqlite upgrade from v3.33.0 to v3.34.0
- https://crrev.com/c/2613955, a sub-query cherry-pick fix after v.3.34.0

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1160602
Change-Id: Ie960e77153efcb9205cb8369d03623a44a883597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618998
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/branch-heads/4324@{#1649}
Cr-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}

[modify] https://crrev.com/fc8a77fa1428041a0e19df31e4502babf5e20445/DEPS


### ad...@google.com (2021-01-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@google.com (2021-01-14)

Congratulations! The VRP panel has decided to award you $5000 for this report! Nice job and thank you!

### ad...@google.com (2021-01-14)

[Empty comment from Monorail migration]

### am...@google.com (2021-01-19)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-01-26)

Thank you for pushing the CL through, pwnall@! :)

### ac...@chromium.org (2021-01-26)

[Empty comment from Monorail migration]

### [Deleted User] (2021-01-26)

[Empty comment from Monorail migration]

### gi...@google.com (2021-01-27)

[Empty comment from Monorail migration]

### ac...@chromium.org (2021-01-27)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2021-01-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/079b03a379719f70c2ea66d3153a2dd19942cb43

commit 079b03a379719f70c2ea66d3153a2dd19942cb43
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Wed Jan 27 07:49:14 2021

Roll src/third_party/sqlite/src/ 0324bd3ef..702a79c7d (172 commits) (M86-LTS)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/0324bd3ef..702a79c7d773

Contains commits from:
- https://crrev.com/c/2600334, a sqlite upgrade from v3.33.0 to v3.34.0
- https://crrev.com/c/2613955, a sub-query cherry-pick fix after v.3.34.0

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit fc8a77fa1428041a0e19df31e4502babf5e20445)

Bug: 1160602
Change-Id: Ie960e77153efcb9205cb8369d03623a44a883597
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2618998
Commit-Queue: Victor Costan <pwnall@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Original-Commit-Position: refs/branch-heads/4324@{#1649}
Cr-Original-Branched-From: c73b5a651d37a6c4d0b8e3262cc4015a5579c6c8-refs/heads/master@{#827102}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2651351
Reviewed-by: Darwin Huang <huangdarwin@chromium.org>
Commit-Queue: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/4240@{#1531}
Cr-Branched-From: f297677702651916bbf65e59c0d4bbd4ce57d1ee-refs/heads/master@{#800218}

[modify] https://crrev.com/079b03a379719f70c2ea66d3153a2dd19942cb43/DEPS


### ac...@chromium.org (2021-01-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-02-09)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1160602?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1161869]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40054252)*
