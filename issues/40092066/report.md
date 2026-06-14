# Heap memory corruption in web database support (SQLite/ICU)

| Field | Value |
|-------|-------|
| **Issue ID** | [40092066](https://issues.chromium.org/issues/40092066) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals |
| **Reporter** | ya...@gmail.com |
| **Assignee** | js...@chromium.org |
| **Created** | 2011-06-21 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

The regular expression engine of ICU used by Chrome is prone to a heap memory corruption bug when processing certain regular expressions. This bug can be triggered in Chrome via Web SQL Database support, which is backed by SQLite that use ICU's regular expression engine to support REGEXP operator in SQL statements.

**VERSION**  

The issue has been reproduced in the following browser/OS combinations:  

Chrome 12.0.742.100 / Ubuntu 10.04 LTS  

Chromium 14.0.798.0 (Developer Build 89782 Linux) / Ubuntu 10.04 LTS

**REPRODUCTION CASE**  

For reproduction in the browser, load the attached testcase.htm in Chrome and this should result in a sad tab. If not, refresh a few times. If the browser is started under GDB and single process mode is used, the output should look like the following:

$ gdb ./chrome-linux/chrome  

GNU gdb (GDB) 7.1-ubuntu  

Copyright (C) 2010 Free Software Foundation, Inc.  

License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>  

This is free software: you are free to change and redistribute it.  

There is NO WARRANTY, to the extent permitted by law. Type "show copying"  

and "show warranty" for details.  

This GDB was configured as "i486-linux-gnu".  

For bug reporting instructions, please see:  

<http://www.gnu.org/software/gdb/bugs/>...  

Reading symbols from /home/yang/Desktop/chrome-linux/chrome...(no debugging symbols found)...done.  

(gdb) set args --single-process  

(gdb) r  

Starting program: /home/yang/Desktop/chrome-linux/chrome --single-process  

[Thread debugging using libthread\_db enabled]  

[New Thread 0xb7e7bb70 (LWP 2419)]  

[New Thread 0xb767ab70 (LWP 2420)]  

[New Thread 0xb6896b70 (LWP 2421)]  

[New Thread 0xb6095b70 (LWP 2422)]  

[New Thread 0xb5894b70 (LWP 2423)]  

[New Thread 0xb5093b70 (LWP 2424)]  

[New Thread 0xb4091b70 (LWP 2426)]  

[New Thread 0xb4892b70 (LWP 2425)]  

[New Thread 0xb3890b70 (LWP 2427)]  

[New Thread 0xb386fb70 (LWP 2428)]  

[New Thread 0xb306eb70 (LWP 2429)]  

[2414:2425:481172553:ERROR:proxy\_service\_factory.cc(66)] Cannot use V8 Proxy resolver in single process mode.  

[New Thread 0xad72fb70 (LWP 2430)]  

[New Thread 0xacf2eb70 (LWP 2431)]  

[2414:2425:481696581:ERROR:proxy\_service\_factory.cc(66)] Cannot use V8 Proxy resolver in single process mode.  

[New Thread 0xac487b70 (LWP 2433)]  

[New Thread 0xa98feb70 (LWP 2434)]  

[New Thread 0xa9038b70 (LWP 2435)]  

[New Thread 0xa8f56b70 (LWP 2436)]  

[New Thread 0xa8237b70 (LWP 2437)]  

[2414:2425:485943140:ERROR:histogram.cc(283)] Error Deserializing Histogram Unknown histogram\_type: 3  

[Thread 0xa8f56b70 (LWP 2436) exited]  

[2414:2425:486560523:ERROR:histogram.cc(283)] Error Deserializing Histogram Unknown histogram\_type: 3  

[New Thread 0xa8f56b70 (LWP 2438)]

Program received signal SIGSEGV, Segmentation fault.  

[Switching to Thread 0xb4892b70 (LWP 2425)]  

0x0886a099 in tcmalloc::CentralFreeList::FetchFromSpans() ()  

(gdb)

To better illustrate this issue, compile the attached icu\_test.cpp and link against ICU 4.6, run the executable and the output should look like:

$ g++ -o icu\_test -I /usr/local/include/ icu\_test.cpp -licuuc -licui18n  

icu\_test.cpp:10:23: warning: trigraph ??) ignored, use -trigraphs to enable  

$ ./icu\_test  

\*\*\* glibc detected \*\*\* ./icu\_test: realloc(): invalid next size: 0x091a0e58 \*\*\*  

======= Backtrace: =========  

/lib/tls/i686/cmov/libc.so.6(+0x6b591)[0x3f5591]  

/lib/tls/i686/cmov/libc.so.6(+0x70cbd)[0x3facbd]  

/lib/tls/i686/cmov/libc.so.6(realloc+0xdd)[0x3faf9d]  

/usr/local/lib/libicuuc.so.46(uprv\_realloc\_46+0x94)[0x679e34]  

/usr/local/lib/libicuuc.so.46(\_ZN6icu\_469UVector6414expandCapacityEiR10UErrorCode+0x99)[0x683e89]  

/usr/local/lib/libicui18n.so.46(\_ZN6icu\_4612RegexMatcher9StateSaveEPNS\_12REStackFrameExR10UErrorCode+0xd6)[0xb5b5f6]  

/usr/local/lib/libicui18n.so.46(\_ZN6icu\_4612RegexMatcher12MatchChunkAtEiaR10UErrorCode+0x7a2)[0xb4e002]  

/usr/local/lib/libicui18n.so.46(\_ZN6icu\_4612RegexMatcher7matchesExR10UErrorCode+0x172)[0xb573c2]  

/usr/local/lib/libicui18n.so.46(uregex\_matches64\_46+0x77)[0xb5f357]  

/usr/local/lib/libicui18n.so.46(uregex\_matches\_46+0x34)[0xb5f3d4]  

./icu\_test[0x8048b0a]  

/lib/tls/i686/cmov/libc.so.6(\_\_libc\_start\_main+0xe6)[0x3a0bd6]  

./icu\_test[0x8048901]  

======= Memory map: ========  

...

BTW, this issue is not specific to ICU 4.6, it still exits in the trunk of ICU as of Jun. 16, 2011.

## Attachments

- [testcase.htm](attachments/testcase.htm) (text/html; charset=us-ascii, 556 B)
- [icu_test.cpp](attachments/icu_test.cpp) (text/x-c; charset=us-ascii, 736 B)

## Timeline

### sc...@gmail.com (2011-06-21)

Thanks Yang, this is an excellent report.

In valgrind:

==2613== Invalid write of size 8
==2613==    at 0x1242AB8: icu_46::RegexMatcher::MatchChunkAt(int, signed char, UErrorCode&) (rematch.cpp:5279)
==2613==    by 0x123730B: icu_46::RegexMatcher::matches(long, UErrorCode&) (rematch.cpp:1641)
==2613==    by 0x3507383: uregex_matches64_46 (uregex.cpp:509)
==2613==    by 0x35072DD: uregex_matches_46 (uregex.cpp:494)
==2613==    by 0x156E089: icuRegexpFunc (sqlite3.c:125781)
==2613==    by 0x150E9DA: sqlite3VdbeExec (sqlite3.c:63842)
==2613==    by 0x150B01F: sqlite3Step (sqlite3.c:60868)
==2613==    by 0x150B20F: sqlite3_step (sqlite3.c:60933)
==2613==    by 0x37694AD: WebCore::SQLiteStatement::step() (SQLiteStatement.cpp:107)
==2613==    by 0x29BED62: WebCore::SQLStatement::execute(WebCore::Database*) (SQLStatement.cpp:110)
==2613==    by 0x28A47A4: WebCore::SQLTransaction::runCurrentStatement() (SQLTransaction.cpp:372)
==2613==    by 0x28A4663: WebCore::SQLTransaction::runStatements() (SQLTransaction.cpp:324)
==2613==  Address 0x27bae010 is not stack'd, malloc'd or (recently) free'd
==2613== 
==2613== 
==2613== Process terminating with default action of signal 11 (SIGSEGV)


### sc...@gmail.com (2011-06-21)

Scott, any idea who's a good idea to fix a nasty bug in icu, as exposed by sqlite?
Jungshik, do you still work on icu?


### sh...@chromium.org (2011-06-21)

Side note: Autofill recently switched to ICU regexp (https://crbug.com/chromium/84158) to work around a jsc issue.  I think.

The SQLite regexp syntax is implemented in terms of a user-defined (well, developer-defined) function.  We're using the one in third_party/sqlite/src/ext/icu/icu.c, but we could switch it out (possibly breaking some users of WebDatabase, depending on how matching changes).

As far as ICU itself, Jungshik is who I'd look to.  I seem to recall Brian Stell working on some ICU stuff back in the Gears days, but I don't think I've seen him being involved with Chrome a lot.

### in...@chromium.org (2011-06-22)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-06-23)

Argh... I'll look into this tomorrow with other ICU folks. 



### sk...@chromium.org (2011-06-24)

In order to reduce attack surface, we should try to use one reg.exp. implementation everywhere. Is it possible to re-use the v8 code here?

### sk...@chromium.org (2011-06-24)

Odd - I dont' recall assigning security@ as the owner and did not intend to.

### js...@chromium.org (2011-06-27)

I'm talking to a person who wrote the code.   

### sc...@gmail.com (2011-06-27)

@jshin: thanks so much :)

### bx...@google.com (2011-06-28)

I think I have found the issue, but it needs to be fixed upstream in ICU.  It looks like there was an off-by-one error because URX_JMP_SAV_X instructions weren't getting updated during an insertOp().

jshin, does this patch look alright/what can we do about getting this fixed upstream?



Index: regexcmp.cpp
===================================================================
--- regexcmp.cpp	(revision 88321)
+++ regexcmp.cpp	(working copy)
@@ -1962,6 +1962,7 @@
             opType == URX_CTR_LOOP     ||
             opType == URX_CTR_LOOP_NG  ||
             opType == URX_JMP_SAV      ||
+            opType == URX_JMP_SAV_X    ||
             opType == URX_RELOC_OPRND)    && opValue > where) {
             // Target location for this opcode is after the insertion point and
             //   needs to be incremented to adjust for the insertion.
@@ -4320,4 +4321,3 @@
 
 U_NAMESPACE_END
 #endif  // !UCONFIG_NO_REGULAR_EXPRESSIONS
-


### js...@chromium.org (2011-06-28)

Yeah. I talked to the person who wrote the ICU regex engine (Andy Heninger) yesterday and the fix made by him is exactly the same as yours. :-)

http://bugs.icu-project.org/trac/changeset/30244

Let me patch in that change to our version. 



### bu...@chromium.org (2011-06-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=90787

------------------------------------------------------------------------
r90787 | jshin@chromium.org | Tue Jun 28 10:34:38 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/README.chromium?r1=90787&r2=90786&pathrev=90787
 A http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/patches/regex.patch?r1=90787&r2=90786&pathrev=90787
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/source/i18n/regexcmp.cpp?r1=90787&r2=90786&pathrev=90787
 M http://src.chromium.org/viewvc/chrome/trunk/deps/third_party/icu46/source/test/testdata/regextst.txt?r1=90787&r2=90786&pathrev=90787

ICU Regex patch.

Apply the upstream patch ( http://bugs.icu-project.org/trac/changeset/30244 ) to our
copy of ICU.



BUG=86900
TEST=In debug build, run Chrome and load testcase.htm file. It should not result in a sad tab.
Review URL: http://codereview.chromium.org/7276039
------------------------------------------------------------------------

### bu...@chromium.org (2011-06-28)

The following revision refers to this bug:
    http://src.chromium.org/viewvc/chrome?view=rev&revision=90794

------------------------------------------------------------------------
r90794 | jshin@chromium.org | Tue Jun 28 10:53:33 PDT 2011

Changed paths:
 M http://src.chromium.org/viewvc/chrome/trunk/src/DEPS?r1=90794&r2=90793&pathrev=90794

Roll icu to r90787 to get an upstream regex patch (also independently made by bxx )

BUG=86900
TEST=In debug build, run Chrome and load testcase.htm file (attached to the bug). It should not result in a sad tab.
TBR=jschuh
Review URL: http://codereview.chromium.org/7253044
------------------------------------------------------------------------

### in...@chromium.org (2011-06-28)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-06-29)

M13 DEPS got updated to get this fix.  

Security team will decide what to do with M12. 

### sc...@gmail.com (2011-06-29)

Thanks for merging to M13!! No more M12s as far as I know => FixUnreleased

### sc...@gmail.com (2011-07-20)

@yangdingning: great to see you back! We're delighted to offer you a provisional $1000 Chromium Security Reward for a very interesting bug!

----
Boilerplate text:
Please do NOT publicly disclose details until a fix has been released to all our
users. Early public disclosure may cancel the provisional reward.
Also, please be considerate about disclosure when the bug affects a core library
that may be used by other products.
Please do NOT share this information with third parties who are not directly
involved in fixing the bug. Doing so may cancel the provisional reward.
Please be honest if you have already disclosed anything publicly or to third parties.
----

### sc...@gmail.com (2011-07-21)

[Empty comment from Monorail migration]

### sc...@gmail.com (2011-08-04)

[Empty comment from Monorail migration]

### js...@chromium.org (2011-10-05)

Batch update.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

Lifting view restrictions.

### js...@chromium.org (2012-04-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### bu...@chromium.org (2012-11-14)

The following revision refers to this bug:
    http://goto.ext.google.com/viewvc/chrome-internal?view=rev&revision=15928

------------------------------------------------------------------------
r15928 | jungshik@google.com | 2011-06-28T22:14:48.156584Z

------------------------------------------------------------------------

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-26)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-26)

This issue was migrated from crbug.com/chromium/86900?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092066)*
