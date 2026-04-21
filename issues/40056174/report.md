# Security: UAF in websql

| Field | Value |
|-------|-------|
| **Issue ID** | [40056174](https://issues.chromium.org/issues/40056174) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ch...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2021-06-11 |
| **Bounty** | $500.00 |

## Description

The attached file triggers an oob in websql. Sometimes you might need to click the button multiple times to cause a crash. 

This results in iCol being an out of bounds index in this function: sqlite3ExprCodeGetColumnOfTable, which results in pCol pointing out of bounds.

This can result in a leak though the branch that returns an error
        sqlite3ErrorMsg(pParse, "generated column loop on \"%s\"", pCol->zName);
or it can possibly lead to a heap overflow through the codepath where it goes through exprDup then to sqlite3ExprListDup. 

An example stack trace is:

base::debug::StackTrace::StackTrace()
#2 0x5570ff6d8281 base::debug::(anonymous namespace)::StackDumpSignalHandler()
#3 0x7f301617c390 (/lib/x86_64-linux-gnu/libpthread-2.23.so+0x1138f)
#4 0x7f30118837c6 strlen
#5 0x557100f6098c dupedExprSize
#6 0x557100f60859 exprDup
#7 0x557100f58b00 sqlite3ExprCodeGeneratedColumn
#8 0x557100f5cafc sqlite3ExprCodeGetColumnOfTable
#9 0x557100f58cf2 sqlite3ExprCodeGetColumn
#10 0x557100f567c9 sqlite3ExprCodeTarget
#11 0x557100f59e78 sqlite3ExprCodeExprList
#12 0x557100f73174 selectInnerLoop
#13 0x557100f44f0b sqlite3Select
#14 0x557100f906eb updateFromSelect
#15 0x557100f8fc1a updateVirtualTable
#16 0x557100f49383 sqlite3Update
#17 0x557100f3d125 yy_reduce
#18 0x557100efb8f5 sqlite3RunParser
#19 0x557100f37135 sqlite3Prepare
#20 0x557100efa94f sqlite3LockAndPrepare
#21 0x557100efab03 chrome_sqlite3_prepare_v3
#22 0x5571049f55eb blink::SQLiteStatement::Prepare()
#23 0x5571049ffad9 blink::SQLStatementBackend::Execute()
#24 0x5571049eabb9 blink::SQLTransactionBackend::RunCurrentStatementAndGetNextState()
#25 0x5571049ea304 blink::SQLTransactionBackend::RunStatements()
#26 0x5571049ea822 blink::SQLTransactionBackend::PerformNextStep()
#27 0x5571049fca6f blink::DatabaseTask::Run()
#28 0x5570ff69ac83 base::TaskAnnotator::RunTask()
#29 0x5570ff6abc20 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWorkImpl()
#30 0x5570ff6ab91a base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::DoWork()
#31 0x5570ff65cd2a base::MessagePumpDefault::Run()
#32 0x5570ff6ac2c7 base::sequence_manager::internal::ThreadControllerWithMessagePumpImpl::Run()
#33 0x5570ff67dc7b base::RunLoop::Run()
#34 0x5570feff0e36 blink::scheduler::WorkerThread::SimpleThreadImpl::Run()
#35 0x5570ff6e94ac base::(anonymous namespace)::ThreadFunc()
#36 0x7f30161726ba start_thread
#37 0x7f30118ff51d clone


## Attachments

- [oob1.html](attachments/oob1.html) (text/plain, 750 B)

## Timeline

### [Deleted User] (2021-06-11)

[Empty comment from Monorail migration]

### mp...@chromium.org (2021-06-13)

Thanks for the report and test case. I get a UAF rather than an OOB so I'll rename this (if you also get an OOB feel free to include that stack trace).

This repros in both Chrome (with the PoC) and sqlite_shell (using just the SQL).

Here's the SQL:
create VIRTUAL table var14 using fts3 ( var2 );
WITH  var14 AS ( SELECT 1) UPDATE var14 SET var2 = NULL FROM 'var14' ;

Here are my stack traces:
=================================================================
==3968407==ERROR: AddressSanitizer: heap-use-after-free on address 0x6030000023bc at pc 0x55874c109d92 bp 0x7ffd4a351890 sp 0x7ffd4a351888
READ of size 2 at 0x6030000023bc thread T0
    #0 0x55874c109d91 in sqlite3ExprCodeGetColumnOfTable third_party/sqlite/src/amalgamation/sqlite3.c:104237:43
    #1 0x55874c0f9cca in sqlite3ExprCodeGetColumn third_party/sqlite/src/amalgamation/sqlite3.c:104281:3
    #2 0x55874c0f0e93 in sqlite3ExprCodeTarget third_party/sqlite/src/amalgamation/sqlite3.c:104598:14
    #3 0x55874c0fea20 in sqlite3ExprCodeExprList third_party/sqlite/src/amalgamation/sqlite3.c:105417:19
    #4 0x55874c15e854 in innerLoopLoadRow third_party/sqlite/src/amalgamation/sqlite3.c:131707:3
    #5 0x55874c15e854 in selectInnerLoop third_party/sqlite/src/amalgamation/sqlite3.c:132161:7
    #6 0x55874c0b850a in sqlite3Select third_party/sqlite/src/amalgamation/sqlite3.c:137756:7
    #7 0x55874c1d59d7 in updateFromSelect third_party/sqlite/src/amalgamation/sqlite3.c:140185:3
    #8 0x55874c1d3152 in updateVirtualTable third_party/sqlite/src/amalgamation/sqlite3.c:141147:5
    #9 0x55874c0c5932 in sqlite3Update third_party/sqlite/src/amalgamation/sqlite3.c:140553:5
    #10 0x55874c09e1d5 in yy_reduce third_party/sqlite/src/amalgamation/sqlite3.c:160839:3
    #11 0x55874bfb5c00 in sqlite3Parser third_party/sqlite/src/amalgamation/sqlite3.c:161711:15
    #12 0x55874bfb5c00 in sqlite3RunParser third_party/sqlite/src/amalgamation/sqlite3.c:162962:5
    #13 0x55874c0884db in sqlite3Prepare third_party/sqlite/src/amalgamation/sqlite3.c:130861:5
    #14 0x55874bfb34be in sqlite3LockAndPrepare third_party/sqlite/src/amalgamation/sqlite3.c:130935:10
    #15 0x55874bfb300b in chrome_sqlite3_prepare_v2 third_party/sqlite/src/amalgamation/sqlite3.c:131020:8
    #16 0x55874b9fc917 in shell_exec third_party/sqlite/src/amalgamation/shell/shell.c:13591:10
    #17 0x55874ba23e17 in runOneSqlLine third_party/sqlite/src/amalgamation/shell/shell.c:20615:8
    #18 0x55874b9febf4 in process_input third_party/sqlite/src/amalgamation/shell/shell.c:20715:17
    #19 0x55874b9eaf9b in sqlite_shell_main third_party/sqlite/src/amalgamation/shell/shell.c:21516:12
    #20 0x7f5e15357d09 in __libc_start_main csu/../csu/libc-start.c:308:16

0x6030000023bc is located 12 bytes inside of 32-byte region [0x6030000023b0,0x6030000023d0)
freed by thread T0 here:
    #0 0x55874b9b0062 in free /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:127:3
    #1 0x55874c139655 in chrome_sqlite3_free third_party/sqlite/src/amalgamation/sqlite3.c:27978:5
    #2 0x55874c139655 in sqlite3HashClear third_party/sqlite/src/amalgamation/sqlite3.c:33226:5
    #3 0x55874c139655 in sqlite3ColumnsFromExprList third_party/sqlite/src/amalgamation/sqlite3.c:133202:3
    #4 0x55874c132115 in resolveFromTermToCte third_party/sqlite/src/amalgamation/sqlite3.c:136251:5
    #5 0x55874c132115 in selectExpander third_party/sqlite/src/amalgamation/sqlite3.c:136395:21
    #6 0x55874c10cd67 in sqlite3WalkSelect third_party/sqlite/src/amalgamation/sqlite3.c:98570:10
    #7 0x55874c12dc03 in sqlite3SelectExpand third_party/sqlite/src/amalgamation/sqlite3.c:136671:3
    #8 0x55874c12dc03 in sqlite3SelectPrep third_party/sqlite/src/amalgamation/sqlite3.c:136756:3
    #9 0x55874c0b555e in sqlite3Select third_party/sqlite/src/amalgamation/sqlite3.c:137219:3
    #10 0x55874c1d59d7 in updateFromSelect third_party/sqlite/src/amalgamation/sqlite3.c:140185:3
    #11 0x55874c1d3152 in updateVirtualTable third_party/sqlite/src/amalgamation/sqlite3.c:141147:5
    #12 0x55874c0c5932 in sqlite3Update third_party/sqlite/src/amalgamation/sqlite3.c:140553:5
    #13 0x55874c09e1d5 in yy_reduce third_party/sqlite/src/amalgamation/sqlite3.c:160839:3
    #14 0x55874bfb5c00 in sqlite3Parser third_party/sqlite/src/amalgamation/sqlite3.c:161711:15
    #15 0x55874bfb5c00 in sqlite3RunParser third_party/sqlite/src/amalgamation/sqlite3.c:162962:5
    #16 0x55874c0884db in sqlite3Prepare third_party/sqlite/src/amalgamation/sqlite3.c:130861:5
    #17 0x55874bfb34be in sqlite3LockAndPrepare third_party/sqlite/src/amalgamation/sqlite3.c:130935:10
    #18 0x55874bfb300b in chrome_sqlite3_prepare_v2 third_party/sqlite/src/amalgamation/sqlite3.c:131020:8
    #19 0x55874b9fc917 in shell_exec third_party/sqlite/src/amalgamation/shell/shell.c:13591:10
    #20 0x55874ba23e17 in runOneSqlLine third_party/sqlite/src/amalgamation/shell/shell.c:20615:8
    #21 0x55874b9febf4 in process_input third_party/sqlite/src/amalgamation/shell/shell.c:20715:17
    #22 0x55874b9eaf9b in sqlite_shell_main third_party/sqlite/src/amalgamation/shell/shell.c:21516:12
    #23 0x7f5e15357d09 in __libc_start_main csu/../csu/libc-start.c:308:16

previously allocated by thread T0 here:
    #0 0x55874b9b02cd in malloc /b/s/w/ir/cache/builder/src/third_party/llvm/compiler-rt/lib/asan/asan_malloc_linux.cpp:145:3
    #1 0x55874c2167c1 in sqlite3MemMalloc third_party/sqlite/src/amalgamation/sqlite3.c:23957:7
    #2 0x55874bf84b44 in mallocWithAlarm third_party/sqlite/src/amalgamation/sqlite3.c:27849:7
    #3 0x55874bf84b44 in sqlite3Malloc third_party/sqlite/src/amalgamation/sqlite3.c:27879:5
    #4 0x55874c086d02 in sqlite3HashInsert third_party/sqlite/src/amalgamation/sqlite3.c:33436:25
    #5 0x55874c13916d in sqlite3ColumnsFromExprList third_party/sqlite/src/amalgamation/sqlite3.c:133198:18
    #6 0x55874c132115 in resolveFromTermToCte third_party/sqlite/src/amalgamation/sqlite3.c:136251:5
    #7 0x55874c132115 in selectExpander third_party/sqlite/src/amalgamation/sqlite3.c:136395:21
    #8 0x55874c10cd67 in sqlite3WalkSelect third_party/sqlite/src/amalgamation/sqlite3.c:98570:10
    #9 0x55874c12dc03 in sqlite3SelectExpand third_party/sqlite/src/amalgamation/sqlite3.c:136671:3
    #10 0x55874c12dc03 in sqlite3SelectPrep third_party/sqlite/src/amalgamation/sqlite3.c:136756:3
    #11 0x55874c0b555e in sqlite3Select third_party/sqlite/src/amalgamation/sqlite3.c:137219:3
    #12 0x55874c1d59d7 in updateFromSelect third_party/sqlite/src/amalgamation/sqlite3.c:140185:3
    #13 0x55874c1d3152 in updateVirtualTable third_party/sqlite/src/amalgamation/sqlite3.c:141147:5
    #14 0x55874c0c5932 in sqlite3Update third_party/sqlite/src/amalgamation/sqlite3.c:140553:5
    #15 0x55874c09e1d5 in yy_reduce third_party/sqlite/src/amalgamation/sqlite3.c:160839:3
    #16 0x55874bfb5c00 in sqlite3Parser third_party/sqlite/src/amalgamation/sqlite3.c:161711:15
    #17 0x55874bfb5c00 in sqlite3RunParser third_party/sqlite/src/amalgamation/sqlite3.c:162962:5
    #18 0x55874c0884db in sqlite3Prepare third_party/sqlite/src/amalgamation/sqlite3.c:130861:5
    #19 0x55874bfb34be in sqlite3LockAndPrepare third_party/sqlite/src/amalgamation/sqlite3.c:130935:10
    #20 0x55874bfb300b in chrome_sqlite3_prepare_v2 third_party/sqlite/src/amalgamation/sqlite3.c:131020:8
    #21 0x55874b9fc917 in shell_exec third_party/sqlite/src/amalgamation/shell/shell.c:13591:10
    #22 0x55874ba23e17 in runOneSqlLine third_party/sqlite/src/amalgamation/shell/shell.c:20615:8
    #23 0x55874b9febf4 in process_input third_party/sqlite/src/amalgamation/shell/shell.c:20715:17
    #24 0x55874b9eaf9b in sqlite_shell_main third_party/sqlite/src/amalgamation/shell/shell.c:21516:12
    #25 0x7f5e15357d09 in __libc_start_main csu/../csu/libc-start.c:308:16

SUMMARY: AddressSanitizer: heap-use-after-free third_party/sqlite/src/amalgamation/sqlite3.c:104237:43 in sqlite3ExprCodeGetColumnOfTable
Shadow bytes around the buggy address:
  0x0c067fff8420: fa fa fd fd fd fa fa fa 00 00 00 fa fa fa fd fd
  0x0c067fff8430: fd fd fa fa fd fd fd fd fa fa 00 00 00 00 fa fa
  0x0c067fff8440: 00 00 00 fa fa fa 00 00 00 00 fa fa 00 00 00 fa
  0x0c067fff8450: fa fa fd fd fd fd fa fa fd fd fd fd fa fa 00 00
  0x0c067fff8460: 00 fa fa fa 00 00 00 fa fa fa 00 00 00 00 fa fa
=>0x0c067fff8470: 00 00 00 00 fa fa fd[fd]fd fd fa fa 00 00 00 00
  0x0c067fff8480: fa fa 00 00 00 00 fa fa fd fd fd fd fa fa fa fa
  0x0c067fff8490: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff84a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff84b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c067fff84c0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
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
==3968407==ABORTING


[Monorail components: Blink>Storage>WebSQL]

### mp...@chromium.org (2021-06-13)

Dr. Hipp and Daniel, could you take a look? See the above comment.

### [Deleted User] (2021-06-13)

[Empty comment from Monorail migration]

### dr...@gmail.com (2021-06-13)

This problem arose when Postgres-compatible UPDATE FROM support was added with version 3.33.0, specifically in check-in (https://sqlite.org/src/timeline?c=88baf1eb0706503).  The problem was fixed by check-in (https://sqlite.org/src/timeline?c=0f0959c6f95046e8).

### [Deleted User] (2021-06-13)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2021-06-14)

Thanks. For future reviewers, a heads up that I'll cherry-pick https://sqlite.org/src/info/0f0959c6f95046e8

### hu...@chromium.org (2021-06-15)

[Empty comment from Monorail migration]

[Monorail components: -Blink>Storage>WebSQL Internals>Storage]

### hu...@chromium.org (2021-06-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-06-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/2be5a4e3efd34e2ffcbaa65b105802b1791dc752

commit 2be5a4e3efd34e2ffcbaa65b105802b1791dc752
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Tue Jun 15 23:54:41 2021

When constructing the synthensized SELECT statement that is used to choose
the rows in an UPDATE FROM, make sure the first table is really the table
being updated, and not some common-table expression that happens to have the
same name.  [forum:/forumpost/a274248080|forum post a274248080].  More
changes associated with CTE name resolution are pending.

FossilOrigin-Name: 0f0959c6f95046e8e7887716e0a7de95da18d1e926ab1f919527083a56541db5
(cherry picked from commit 1168f810929ede4d8d323a6acf721ff9cd89de90)
Bug: 1218707
Change-Id: Idfec0bff8422f3ec34b142e5782f7104502d38f8

[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/amalgamation/sqlite3.c
[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/amalgamation/sqlite3.h
[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/amalgamation_dev/sqlite3.h
[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/manifest
[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/src/build.c
[modify] https://crrev.com/2be5a4e3efd34e2ffcbaa65b105802b1791dc752/src/update.c


### gi...@appspot.gserviceaccount.com (2021-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/009cada961a9a313aa208ffb9e2666457b275637

commit 009cada961a9a313aa208ffb9e2666457b275637
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Jun 18 22:51:26 2021

Roll src/third_party/sqlite/src/ 1e382b22c..09b4d6e90 (2 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/1e382b22c960..09b4d6e90623

$ git log 1e382b22c..09b4d6e90 --date=short --no-merges --format='%ad %ae %s'
2021-06-15 huangdarwin Avoid a buffer overread in fts3 that could occur when handling corrupt data structures.
2021-06-15 huangdarwin When constructing the synthensized SELECT statement that is used to choose the rows in an UPDATE FROM, make sure the first table is really the table being updated, and not some common-table expression that happens to have the same name.  [forum:/forumpost/a274248080|forum post a274248080].  More changes associated with CTE name resolution are pending.

Created with:
  roll-dep src/third_party/sqlite/src

Bug: 1209517, 1218707
Change-Id: Id564411566baa26d327fe78b6b89571cb353891b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2970700
Auto-Submit: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#894011}

[modify] https://crrev.com/009cada961a9a313aa208ffb9e2666457b275637/DEPS


### hu...@chromium.org (2021-06-18)

This should be fixed now (clusterfuzz may mark it as verified)

### [Deleted User] (2021-06-20)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-20)

[Empty comment from Monorail migration]

### hu...@chromium.org (2021-06-21)

Requesting merge to M92 (beta), but not M91 (stable), as the change required isn't too large and is security-critical but M91 is a bit late in the process, so might be okay not to have this in M91. I'll defer to security folks if they'd like to see this in M91 though.

### [Deleted User] (2021-06-21)

This bug requires manual review: DEPS changes referenced in bugdroid comments.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
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
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2021-06-21)

1. Yes
2. https://crrev.com/c/2970700
3. Yes (over the weekend)
4. No (unless security would prefer for this to be merged into M91 as a security bug)
5. security bug
6. no
7. n/a

### sr...@google.com (2021-06-22)

merge approved for M92 branch:4515 please merge to the branch before 3pm PST today so we can include in tomorrow's beta release.

### go...@chromium.org (2021-06-22)

Please merge your change to M92 branch 4515 ASAP so we can take it in for tomorrow's Beta Release. Android Beta RC cut today @1:00 PM PT. Thank you.

### hu...@chromium.org (2021-06-22)

Oops I just saw this. I'll try to get it in asap but not sure if it'll be in by 1pm PT

### hu...@chromium.org (2021-06-22)

CL is under review now at https://crrev.com/c/2979286

### gi...@appspot.gserviceaccount.com (2021-06-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/45278d955b0bfb186a9cfb8caaa8c3605d32e43b

commit 45278d955b0bfb186a9cfb8caaa8c3605d32e43b
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Tue Jun 22 23:12:25 2021

Roll src/third_party/sqlite/src/ 1e382b22c..09b4d6e90 (2 commits) (M92)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/1e382b22c960..09b4d6e90623

$ git log 1e382b22c..09b4d6e90 --date=short --no-merges --format='%ad %ae %s'
2021-06-15 huangdarwin Avoid a buffer overread in fts3 that could occur when handling corrupt data structures.
2021-06-15 huangdarwin When constructing the synthensized SELECT statement that is used to choose the rows in an UPDATE FROM, make sure the first table is really the table being updated, and not some common-table expression that happens to have the same name.  [forum:/forumpost/a274248080|forum post a274248080].  More changes associated with CTE name resolution are pending.

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit 009cada961a9a313aa208ffb9e2666457b275637)

Bug: 1209517, 1218707
Change-Id: Id564411566baa26d327fe78b6b89571cb353891b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2970700
Auto-Submit: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#894011}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2979286
Cr-Commit-Position: refs/branch-heads/4515@{#916}
Cr-Branched-From: 488fc70865ddaa05324ac00a54a6eb783b4bc41c-refs/heads/master@{#885287}

[modify] https://crrev.com/45278d955b0bfb186a9cfb8caaa8c3605d32e43b/DEPS


### am...@google.com (2021-06-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-23)

Thank you for reporting this issue to us. Based on https://crbug.com/chromium/1218707#c5 it appears there was already a fix for this issue. The VRP Panel has decided to award you $500 for this report as a thank you as it allowed us to ensure the merge for this fix was prioritized. A member of our finance team will be in touch soon to arrange payment. 
Please let me know what name or handle you would like us to use to credit you for this issue. 
Thank you! 

### hu...@chromium.org (2021-06-24)

Re https://crbug.com/chromium/1218707#c24, not sure if this changes things, but while there was a fix for the issue's root cause already, this issue was not known by Chrome (and was just known by sqlite folks) before it was reported to crbug.

### ch...@gmail.com (2021-06-30)

Thanks for the award. I think the amount is fine given that it was already known by sqlite. I was hoping it wasn't known by anyone when I reported :)
You can credit me as:
Chris Salls (@salls) of Makai Security

### am...@google.com (2021-06-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-27)

[Empty comment from Monorail migration]

### rz...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### gi...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-07-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c22f18b50b825f594cb1a9a429d9a6c5837f3ba8

commit c22f18b50b825f594cb1a9a429d9a6c5837f3ba8
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Wed Jul 28 11:05:46 2021

[M90-LTS] Roll src/third_party/sqlite/src/ 144e06fa..09b4d6e90 (5 commits)

https://chromium.googlesource.com/chromium/deps/sqlite.git/+log/144e06fad937..09b4d6e90623

$ git log 144e06fa..09b4d6e90 --date=short --no-merges --format='%ad %ae %s'
2021-06-15 huangdarwin@chromium.org Avoid a buffer overread in fts3 that could occur when handling corrupt data structures.
2021-06-15 huangdarwin@chromium.org When constructing the synthensized SELECT statement that is used to choose the rows in an UPDATE FROM, make sure the first table is really the table being updated, and not some common-table expression that happens to have the same name.  [forum:/forumpost/a274248080|forum post a274248080].  More changes associated with CTE name resolution are pending.
2021-06-08 huangdarwin@chromium.org Fix the UNION ALL flattener optimization so that it works better with recursive CTEs. dbsqlfuzz 88ed5c66789fced139d148aed823cba7c0926dd7
2021-05-19 huangdarwin@chromium.org sqlite: Fix an undefined-integer-overflow problem in fts3.c.
2021-05-10 huangdarwin@chromium.org sqlite: Improved detection of oversized cells in balance_nonroot(), especially in index b-trees when a cell is being moved from a child page into the parent page in order to become a new divider cell.

Created with:
  roll-dep src/third_party/sqlite/src

(cherry picked from commit 009cada961a9a313aa208ffb9e2666457b275637)

Bug: 1209517, 1218707, 1216885, 1204066, 1198216
Change-Id: Id564411566baa26d327fe78b6b89571cb353891b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2970700
Auto-Submit: Darwin Huang <huangdarwin@chromium.org>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#894011}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3055412
Reviewed-by: Jana Grill <janagrill@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1547}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/c22f18b50b825f594cb1a9a429d9a6c5837f3ba8/DEPS


### rz...@google.com (2021-07-28)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1218707?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056174)*
