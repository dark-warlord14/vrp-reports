# Security: Use After Free in sqlite

| Field | Value |
|-------|-------|
| **Issue ID** | [41484271](https://issues.chromium.org/issues/41484271) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL, Internals>Storage>SQLite |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | gc...@gmail.com |
| **Assignee** | es...@chromium.org |
| **Created** | 2023-12-14 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

## Introduction

Note: This vulnerability exists in the latest version of Chrome Stable and in the mainline Chrome.

- Versions affected in Chrome: Chrome-Stable-116 to the latest
- Time introduced in Chromium: https://chromium-review.googlesource.com/c/chromium/src/+/4545677

- Time introduced in sqlite code: https://github.com/sqlite/sqlite/commit/af03eb3241c832d7352eedc11701eac55d3fc67e (should be earlier, here just let this optimization enter the default configuration)
- Introduced in sqlite release: sqlite 3.42.0

After this branch of sqlite: https://github.com/sqlite/sqlite/commit/5e4233a9e48b124d4d342b757b34e4ae849f5cf8
Some grammatical changes have occurred, causing the provided POC to become invalid. However, the vulnerability has not actually been fixed. Certain modifications to the POC may be required to trigger the vulnerability.
Note: However, this change does not affect Chrome, and the vulnerability still exists in the latest version of Chrome Stable and in the mainline Chrome. And you can Update sqlite version for temporary fix.

## Root Cause

[0] In the countOfViewOptimization function, pSub->pEList may be released in the loop.
```
while( pSub ){
  Expr *pTerm;
  pPrior = pSub->pPrior;
  pSub->pPrior = 0;
  pSub->pNext = 0;
  pSub->selFlags |= SF_Aggregate;
  pSub->selFlags &= ~SF_Compound;
  pSub->nSelectRow = 0;
  sqlite3ExprListDelete(db, pSub->pEList); // ==> [0]
  pTerm = pPrior ? sqlite3ExprDup(db, pCount, 0) : pCount;
  pSub->pEList = sqlite3ExprListAppend(pParse, 0, pTerm);
  pTerm = sqlite3PExpr(pParse, TK_SELECT, 0, 0);
  sqlite3PExprAddSelect(pParse, pTerm, pSub);
  if( pExpr==0 ){
    pExpr = pTerm;
  }else{
    pExpr = sqlite3PExpr(pParse, TK_PLUS, pTerm, pExpr);
  }
  pSub = pPrior;
}
```

[1] In the sqlite3Select function, the node may have been saved in pAggInfo before being released.
```
sNC.pParse = pParse;
sNC.pSrcList = pTabList;
sNC.uNC.pAggInfo = pAggInfo;
VVA_ONLY( sNC.ncFlags = NC_UAggInfo; )
pAggInfo->nSortingColumn = pGroupBy ? pGroupBy->nExpr : 0;
pAggInfo->pGroupBy = pGroupBy;
sqlite3ExprAnalyzeAggList(&sNC, pEList); // ==> [1]
sqlite3ExprAnalyzeAggList(&sNC, sSort.pOrderBy); // ==> [1]
if( pHaving ){
  if( pGroupBy ){
    assert( pWhere==p->pWhere );
    assert( pHaving==p->pHaving );
    assert( pGroupBy==p->pGroupBy );
    havingToWhere(pParse, p);
    pWhere = p->pWhere;
  }
  sqlite3ExprAnalyzeAggregates(&sNC, pHaving); // ==> [1]
}
pAggInfo->nAccumulator = pAggInfo->nColumn;
```

[2] In the resetAccumulator function, the pointer saved in pAggInfo is used, triggering UAF.
```
for(pFunc=pAggInfo->aFunc, i=0; i<pAggInfo->nFunc; i++, pFunc++){
  if( pFunc->iDistinct>=0 ){
    Expr *pE = pFunc->pFExpr;
    assert( ExprUseXList(pE) );
    if( pE->x.pList==0 || pE->x.pList->nExpr!=1 ){ // ==> [2]
      sqlite3ErrorMsg(pParse, "DISTINCT aggregates must have exactly one "
         "argument");
      pFunc->iDistinct = -1;
    }else{
      KeyInfo *pKeyInfo = sqlite3KeyInfoFromExprList(pParse, pE->x.pList,0,0); // ==> [2]
      pFunc->iDistAddr = sqlite3VdbeAddOp4(v, OP_OpenEphemeral,
          pFunc->iDistinct, 0, 0, (char*)pKeyInfo, P4_KEYINFO);
      ExplainQueryPlan((pParse, 0, "USE TEMP B-TREE FOR %s(DISTINCT)",
                        pFunc->pFunc->zName));
    }
  }
}
```


VERSION
Chrome Version: Chrome + [stable, beta, and dev]
Operating System: All OS

REPRODUCTION CASE

1. Download the newest asan chromium: https://www.googleapis.com/download/storage/v1/b/chromium-browser-asan/o/linux-release%2Fasan-linux-release-1237512.zip?generation=1702567883423831&alt=media

2. python3 -m http.server 8000

3. /path/to/chrome-wrapper --user-data-dir=./user http://localhost:8000/poc.html

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: tab
Crash State: see asan log

CREDIT INFORMATION
Reporter credit: anonymous

## Attachments

- [asan.log](attachments/asan.log) (text/plain, 47.8 KB)
- [poc.sql](attachments/poc.sql) (text/plain, 207 B)
- [poc.html](attachments/poc.html) (text/plain, 1.3 KB)
- [poc.html](attachments/poc_53182198.html) (text/plain, 1.4 KB)

## Timeline

### gc...@gmail.com (2023-12-14)

[Comment Deleted]

### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2023-12-14)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5465290362519552.

### th...@chromium.org (2023-12-14)

I'm able to reproduce this on Linux with the asan build linked above (M122). Note I had to refresh the page once before it crashed, so the poc might not be 100% stable. I'm working on confirming if it's also reproducible on M120. I will avoid setting the FoundIn for now. Speculatively setting OS to Desktop + Android platforms.

Setting the severity to high -- this is a UAF in the renderer process.

asully@: could you PTAL or triage as appropriate?

[Monorail components: Internals>Storage>SQLite]

### th...@chromium.org (2023-12-14)

Can reproduce in M120.

### [Deleted User] (2023-12-14)

[Empty comment from Monorail migration]

### as...@chromium.org (2023-12-14)

Thanks for the clear report and repro. Indeed we bumped to SQLite version 3.42.0 in M116, so I would imagine it repros from that point onwards

OP, you mention that https://github.com/sqlite/sqlite/commit/5e4233a9e48b124d4d342b757b34e4ae849f5cf8 invalidates the repro, but the vulnerability still exists. Has this been brought to the attention of the SQLite authors? Once it's fixed upstream, we can pull those changes into Chrome

The repro uses WebSQL, which is being deprecated and will soon be ripped out of Chromium entirely (yay!) so I'll defer to ayui@ for prioritization

[Monorail components: Blink>Storage>WebSQL]

### cl...@chromium.org (2023-12-14)

Testcase 5465290362519552 failed to reproduce the crash. Please inspect the program output at https://clusterfuzz.com/testcase?key=5465290362519552.

### gc...@gmail.com (2023-12-15)

Hi asully! In fact, the starting point for this change comes from here: https://sqlite.org/forum/forumpost/c9970a37ed
This is just a grammatical change, which may affect the triggering conditions of the vulnerability, but the vulnerability code itself has not been correctly fixed.
I think you can cc the author of sqlite to get the correct fix : ).

### gc...@gmail.com (2023-12-15)

Hi, thefrog! In fact on my computer the reproduction is very stable. I'm not sure why it needs to be refreshed sometimes, maybe it's caused by chrome cache or me not cleaning the sqlite context? .
I wrote a new POC here. I set it to refresh every second and clean up the SQLite context before each execution. This will allow you to reproduce it stably on Asan Chrome. I hope it can help you!

### ay...@chromium.org (2023-12-15)

+ SQLite folks, can you take a look? Thanks!

### [Deleted User] (2023-12-15)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-15)

[Empty comment from Monorail migration]

### dr...@gmail.com (2023-12-15)

The problem appears to have been resolved by the check-in at https://sqlite.org/src/info/4470f657d2069972 which first appeared in the 3.44.1 release of SQLite.

A further change made moments ago at https://sqlite.org/src/info/da442578856c8713 should prevent any similar problems in the future.

### es...@chromium.org (2023-12-15)

Thanks Dr H, [1] does seem to do the trick (I can repro the POC without it, but not with it, when it's cherry picked on Chrome's version of SQLite which is 3.43.2)

Do you think there's any danger/problem from cherry picking that fix to 3.43.2 so we don't have to backport all of 3.44.1 (or newer) to stable Chrome?

### es...@chromium.org (2023-12-15)

[Empty comment from Monorail migration]

### dr...@gmail.com (2023-12-15)

I cherry-picked the change onto the tip of the 3.43 branch here: https://sqlite.org/src/timeline?r=branch-3.43.  Recommend you use check-in https://sqlite.org/src/info/122cd0badad2ce2b.

### gi...@appspot.gserviceaccount.com (2023-12-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/a901bc7adf12d103a78289b1cdb6c7f990c6c14d

commit a901bc7adf12d103a78289b1cdb6c7f990c6c14d
Author: Evan Stade <estade@chromium.org>
Date: Fri Dec 15 23:17:01 2023

Roll src/third_party/sqlite/src/ a7a54e1dd..cd9486849 (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/a7a54e1dd9b6..cd9486849ba3

$ git log a7a54e1dd..cd9486849 --date=short --no-merges --format='%ad %ae %s'
2023-12-15 estade Fix a spurious "misuse of aggregate function" error that could occur when an aggregate function was used within the FROM clause of a sub-select of the select that owns the aggregate. e.g. "SELECT (SELECT x FROM (SELECT sum(t1.a) AS x)) FROM t1". [forum:/forumpost/c9970a37ed | Forum post c9970a37ed].

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1511689
Change-Id: I567df9a71a056c11f232c28d06fa6e9a7b91e4d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5125270
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1238314}

[modify] https://crrev.com/a901bc7adf12d103a78289b1cdb6c7f990c6c14d/third_party/sqlite/src
[modify] https://crrev.com/a901bc7adf12d103a78289b1cdb6c7f990c6c14d/DEPS


### es...@chromium.org (2023-12-18)

thanks Dr H.

Requesting merge of [1] to 120 based on Target-120 label

The fix has been released to Canary with no observed side effects so far, and I manually verified it addresses (breaks) the POC.

For M120, merging this roll will also pull in a couple other patches that fixed fuzzer failures after 120 branched. On 121, only the latest cherry-picked SQLite patch is new in this roll.

* Why does your merge fit within the merge criteria for these milestones (Chrome Browser, Chrome OS)?

"important security issues (medium severity or higher) requested by the security team"

* What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/5125270

* Have the changes been released and tested on canary?

yes

* Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

no

* [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative?

no

* If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

no

[1] https://crrev.com/a901bc7adf12d103a78289b1cdb6c7f990c6c14d

### [Deleted User] (2023-12-18)

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
Owners: govind (Android), govind (iOS), matthewjoseph (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-18)

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
Owners: harrysouders (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-12-18)

[Description Changed]

### am...@chromium.org (2023-12-18)

Thanks Dr. H for the quick response on this and pointing to the upstream commits. It looks like this initial fix was landed on 2 November, well before the report of this issue, and the more recent change  on 15 December was landed as mitigation against potential variants in the future? Please let me know if my interpretation is incorrect here. 

estade@ -- thanks answering this merge question above and getting this fix rolled into Chromium. Security issues should be closed when the fix (or in this case the first roll of that fix into Chromium) has been landed. The bot can add the appropriate merge request labels. 

In this case, I'm evaluating the fixes landed upstream: https://sqlite.org/src/info/4470f657d2069972 and https://sqlite.org/src/info/da442578856c8713&& the canary data for 122.0.6188.0 which is the Canary on which the roll in c#18 was landed. 

There appear to be no issues on Canary, confirming estade@ comments above, approving https://crrev.com/c/5125270 for merge to M121 and M120. Please merge this fix to branches 6167 and 6099 respectively, so this fix can be included in the next update of M121 Beta and M120 Stable the first week of January (since we are now in release freeze). Thank you! 

### es...@chromium.org (2023-12-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d150cce76d68125ae7ef23188ba6e1effddfbf70

commit d150cce76d68125ae7ef23188ba6e1effddfbf70
Author: Evan Stade <estade@chromium.org>
Date: Mon Dec 18 22:13:40 2023

[M121] Roll src/third_party/sqlite/src/ a7a54e1dd..cd9486849 (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/a7a54e1dd9b6..cd9486849ba3

$ git log a7a54e1dd..cd9486849 --date=short --no-merges --format='%ad %ae %s'
2023-12-15 estade Fix a spurious "misuse of aggregate function" error that could occur when an aggregate function was used within the FROM clause of a sub-select of the select that owns the aggregate. e.g. "SELECT (SELECT x FROM (SELECT sum(t1.a) AS x)) FROM t1". [forum:/forumpost/c9970a37ed | Forum post c9970a37ed].

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit a901bc7adf12d103a78289b1cdb6c7f990c6c14d)

Bug: 1511689
Change-Id: I567df9a71a056c11f232c28d06fa6e9a7b91e4d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5125270
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1238314}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5132380
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Auto-Submit: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/6167@{#451}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/d150cce76d68125ae7ef23188ba6e1effddfbf70/third_party/sqlite/src
[modify] https://crrev.com/d150cce76d68125ae7ef23188ba6e1effddfbf70/DEPS


### [Deleted User] (2023-12-18)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### es...@chromium.org (2023-12-18)

1. Was this issue a regression for the milestone it was found in?

yes

2. Is this issue related to a change or feature merged after the latest LTS Milestone?

yes (first affected M120)

### gi...@appspot.gserviceaccount.com (2023-12-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/ec6d50002f5b15122a8569f3f04ad3dea724011b

commit ec6d50002f5b15122a8569f3f04ad3dea724011b
Author: Evan Stade <estade@chromium.org>
Date: Mon Dec 18 23:04:24 2023

[M120] Roll src/third_party/sqlite/src/ a7a54e1dd..cd9486849 (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/a7a54e1dd9b6..cd9486849ba3

$ git log a7a54e1dd..cd9486849 --date=short --no-merges --format='%ad %ae %s'
2023-12-15 estade Fix a spurious "misuse of aggregate function" error that could occur when an aggregate function was used within the FROM clause of a sub-select of the select that owns the aggregate. e.g. "SELECT (SELECT x FROM (SELECT sum(t1.a) AS x)) FROM t1". [forum:/forumpost/c9970a37ed | Forum post c9970a37ed].

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit a901bc7adf12d103a78289b1cdb6c7f990c6c14d)

Bug: 1511689
Change-Id: I567df9a71a056c11f232c28d06fa6e9a7b91e4d3
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5125270
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Commit-Queue: Evan Stade <estade@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1238314}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5132379
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Auto-Submit: Evan Stade <estade@chromium.org>
Cr-Commit-Position: refs/branch-heads/6099@{#1543}
Cr-Branched-From: e6ee4500f7d6549a9ac1354f8d056da49ef406be-refs/heads/main@{#1217362}

[modify] https://crrev.com/ec6d50002f5b15122a8569f3f04ad3dea724011b/third_party/sqlite/src
[modify] https://crrev.com/ec6d50002f5b15122a8569f3f04ad3dea724011b/DEPS


### dr...@gmail.com (2023-12-19)

Interpretation in https://crbug.com/chromium/1511689#c23 is correct:  The commit from 2023-12-15 was defensive, to prevent this from coming up again.  The 2023-11-02 commit was sufficient to resolve the issue.

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-19)

[Empty comment from Monorail migration]

### am...@chromium.org (2024-01-03)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-03)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-03)

Thank you for this report as it allowed us to pull in the necessary upstream update of sqlite. Since this issue was already resolved upstream at the time of your report, the Chrome VRP would like to extend to you a $1,000 thank you reward for your efforts here. A member of the p2p-vrp finance team will be in touch with you soon to arrange payment. Thank you again for taking the time to report this upstream issue to us. 

### am...@google.com (2024-01-05)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-11)

[Empty comment from Monorail migration]

### rz...@google.com (2024-01-17)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-17)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2024-01-17)

1. 2 CLs, https://crrev.com/c/5200513 and a roll-deps CL
2. Low, only a simple conflict
3. 120, 121
4. Yes

### na...@google.com (2024-01-22)

Merge approved for LTS-114

### gi...@appspot.gserviceaccount.com (2024-01-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/8c90e8c7c17e3f1f1a8f4d2ac931b3693c558fc5

commit 8c90e8c7c17e3f1f1a8f4d2ac931b3693c558fc5
Author: Roger Zanoni <rzanoni@google.com>
Date: Wed Jan 24 21:39:48 2024

[M114-LTS] Fix a spurious "misuse of aggregate function" error that could occur when an aggregate function was used within the FROM clause of a sub-select of the select that owns the aggregate. e.g. "SELECT (SELECT x FROM (SELECT sum(t1.a) AS x)) FROM t1". [forum:/forumpost/c9970a37ed | Forum post c9970a37ed].

M114 merge issues:
  src/resolve.c:
    Conflicting spaces on one of the nNestedSelect decrement added
    lines.

Bug: 1511689
FossilOrigin-Name: 4470f657d2069972d02a00983252dec1f814d90c0d8d0906e320e955111e8c11
(cherry picked from commit 5e4233a9e48b124d4d342b757b34e4ae849f5cf8)
Change-Id: I16f402a541ee693ca3c8c2fb176ab6e9d8dac10e
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/deps/sqlite/+/5200513
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Commit-Queue: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Ayu Ishii <ayui@chromium.org>

[modify] https://crrev.com/8c90e8c7c17e3f1f1a8f4d2ac931b3693c558fc5/src/sqliteInt.h
[modify] https://crrev.com/8c90e8c7c17e3f1f1a8f4d2ac931b3693c558fc5/src/resolve.c
[modify] https://crrev.com/8c90e8c7c17e3f1f1a8f4d2ac931b3693c558fc5/test/aggnested.test
[modify] https://crrev.com/8c90e8c7c17e3f1f1a8f4d2ac931b3693c558fc5/test/window1.test


### gi...@appspot.gserviceaccount.com (2024-01-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/d8f0ad2b1d0d82bb20d06f5bbca61289b1b28124

commit d8f0ad2b1d0d82bb20d06f5bbca61289b1b28124
Author: Roger Zanoni <rzanoni@google.com>
Date: Thu Jan 25 17:53:53 2024

[M114-LTS] Roll src/third_party/sqlite/src/ f6752b7ed..8c90e8c7c (1 commit)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/f6752b7ed1fe..8c90e8c7c17e

$ git log f6752b7ed..8c90e8c7c --date=short --no-merges --format='%ad %ae %s'
2024-01-24 rzanoni [M114-LTS] Fix a spurious "misuse of aggregate function" error that could occur when an aggregate function was used within the FROM clause of a sub-select of the select that owns the aggregate. e.g. "SELECT (SELECT x FROM (SELECT sum(t1.a) AS x)) FROM t1". [forum:/forumpost/c9970a37ed | Forum post c9970a37ed].

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1511689
Change-Id: I2a7b23c80a5a4ad285d62d941e32a9b8423bad9b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5236647
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Michael Ershov <miersh@google.com>
Reviewed-by: Ayu Ishii <ayui@chromium.org>
Reviewed-by: Michael Ershov <miersh@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1673}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/d8f0ad2b1d0d82bb20d06f5bbca61289b1b28124/DEPS


### rz...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1511689?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>WebSQL, Internals>Storage>SQLite]
[Monorail mergedwith: crbug.com/chromium/1512485]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-26)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41484271)*
