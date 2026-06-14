# 2 Vulnerabilities in websql & sqlite (Tracking Bug)

| Field | Value |
|-------|-------|
| **Issue ID** | [40050707](https://issues.chromium.org/issues/40050707) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>WebSQL, Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Windows, ChromeOS |
| **CVE IDs** | CVE-2019-13734, CVE-2019-13750, CVE-2019-13751 |
| **Reporter** | le...@gmail.com |
| **Assignee** | pw...@chromium.org |
| **Created** | 2019-11-16 |
| **Bounty** | $2,000.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36

Steps to reproduce the problem:
These vulnerabilities are different from the 3 bugs we have used on Tianfu Cup 2019. But they need the defense-in-depth bypass to trigger in chrome.

NOTE: ONLY VULN 1 & 2 ARE TRIGGERABLE IN CHROME.

Please note 1-2 depends on the memory that was previously used, so in chrome it may need further debug to make it work for a higher success rate. But if you run the poc in SQLite shell, these 2 will almost trigger the problem everytime.

1. open the webpage.

============================

1.	Negative size passed to memcpy() in fts3NodeAddTerm

---
Negative size is controllable. If a database is corrupted. When sqlite tries to merge two segments, it will call fts3SegWriterAdd. 

This function will try to calculate nPrefix and nSuffix by:
  nPrefix = fts3PrefixCompress(pWriter->zTerm, pWriter->nTerm, zTerm, nTerm);
nSuffix = nTerm-nPrefix;

If we got a small nPrefix , for example 0 and go through this function:

    rc = fts3NodeAddTerm(p, &pWriter->pTree, isCopyTerm, zTerm, nPrefix+1);

We will have nTerm (0 + 1) = 1, according to the definition of fts3NodeAddTerm:

static int fts3NodeAddTerm(
  Fts3Table *p,                   /* Virtual table handle */
  SegmentNode **ppTree,           /* IN/OUT: SegmentNode handle */ 
  int isCopyTerm,                 /* True if zTerm/nTerm is transient */
  const char *zTerm,              /* Pointer to buffer containing term */
  int nTerm                       /* Size of term in bytes */
)

There’s a similar fts3PrefixCompress here too:
    nPrefix = fts3PrefixCompress(pTree->zTerm, pTree->nTerm, zTerm, nTerm);
nSuffix = nTerm-nPrefix;

But this time the code forgot to test if nSuffix or nPrefix is greater than 0.
And the code fts3PrefixCompress also have a problem, it only compared n to nPrev, but ignored nNext. 

static int fts3PrefixCompress(
  const char *zPrev,              /* Buffer containing previous term */
  int nPrev,                      /* Size of buffer zPrev in bytes */
  const char *zNext,              /* Buffer containing next term */
  int nNext                       /* Size of buffer zNext in bytes */
){
  int n;
  UNUSED_PARAMETER(nNext);
  for(n=0; n<nPrev && zPrev[n]==zNext[n]; n++);
  return n;
}

So, if we have for example: pTree->zTerm = AAAAA, pTree->nTerm = 5, and zTerm = AAAAB, nTerm = 1. The nPrefix will be 4 , and nSuffix will be -3 (1 - nPrefix).

And the negative nSuffix will be used here, cause a SIGSEGV:
      memcpy(&pTree->aData[nData], &zTerm[nPrefix], nSuffix);

I have tried this but if we have a big table which will overflow the result nPrefix, make it become a negative number, here the nSuffix will be wrong too,and memcpy will copy read out of bounds. 

Patch:
+if(nSuffix <= 0)
+ Return FTS_CORRUPTED_TAB;

2.	Negative size passed to memcpy() in fts3IncrmergePush
Almost the same reason compares to 4. But this time it happends in fts3IncrmergePush.

Patch:
+if(nSuffix <= 0)
+ Return FTS_CORRUPTED_TAB;

3.	Memory leak in fts4, matchinfo()

 To an fts4 table, if attacker corrupted table docsize, set it to smaller than it should, and try to read matchinfo with flag “l” , “a” or other flags that read data from docsize, the loop, when calling sqlite3Fts3GetVarint will read out-of-bounds and simply return that data back to matchinfo, and will leak memory data after it. (Not triggerable in Chrome since FTS4 is strictly disabled)

          for(iCol=0; iCol<pInfo->nCol; iCol++){
            sqlite3_int64 nToken;
            a += sqlite3Fts3GetVarint(a, &nToken);
            pInfo->aMatchinfo[iCol] = (u32)nToken;
          }
Patch:
        Check if the loop is go beyond the end of a.

https://crbug.com/chromium/1 Nullptr in fts3IncrmergeLoad
aRoot could be nullptr when the shadow table is corrupted, and cause a nullptr-dereference in here:
int nHeight = (int)aRoot[0];

https://crbug.com/chromium/2 Stack overflow in fts3SelectLeaf
piLeaf could be nullptr when shadow table is corrupted, and cause recursive call to fts3SelectLeaf and use up all of the stack memory.

Patch:
-	assert(!piLeaf2 || !piLeaf || rc != SQLITE_OK || (*piLeaf <= *piLeaf2));
	+ if (!piLeaf2 || !piLeaf || rc != SQLITE_OK || (*piLeaf <= *piLeaf2)) {
	+	rc = SQLITE_CORRUPT;
	+ }

https://crbug.com/chromium/3 nullptr in sqlite3WindowLink
Should test pSel after:
 Select *pSel = pNC->pWinSelect;

PoC:
CREATE VIEW a AS SELECT NULL INTERSECT SELECT NULL ORDER BY s() OVER R;
CREATE TABLE a0 AS SELECT 0;
ALTER TABLE a0 RENAME TO S;

What is the expected behavior?

What went wrong?
Page crashed due to memcpy.

Did this work before? N/A 

Chrome version: 78.0.3904.97  Channel: stable
OS Version: 10.0
Flash Version:

## Attachments

- [4-chrome_poc_copy_neg.html](attachments/4-chrome_poc_copy_neg.html) (text/plain, 10.1 KB)
- [4-poc_copy_negative.txt](attachments/4-poc_copy_negative.txt) (text/plain, 10.0 KB)
- [5-chrome_poc_copy_neg.html](attachments/5-chrome_poc_copy_neg.html) (text/plain, 87.6 KB)
- [5-poc_incrmerge.txt](attachments/5-poc_incrmerge.txt) (text/plain, 9.5 KB)
- [6-fts4_memory_disclosure.txt](attachments/6-fts4_memory_disclosure.txt) (text/plain, 309 B)
- [bug1-poc_nullptr.txt](attachments/bug1-poc_nullptr.txt) (text/plain, 418 B)
- [bug2-poc_stackoverflow.txt](attachments/bug2-poc_stackoverflow.txt) (text/plain, 5.9 KB)
- [bug3-poc_windowfunc.txt](attachments/bug3-poc_windowfunc.txt) (text/plain, 136 B)
- deleted (application/octet-stream, 0 B)
- [poc_divide_by_zero.txt](attachments/poc_divide_by_zero.txt) (text/plain, 7.0 KB)
- [fuzzer_fts3_fts4_.cpp](attachments/fuzzer_fts3_fts4_.cpp) (text/plain, 14.2 KB)

## Timeline

### le...@gmail.com (2019-11-16)

.txt files should be .sql files

### ad...@google.com (2019-11-16)

Thanks for the report!

I'm going to split this into multiple bugs.

The defense-in-depth bypass referenced is presumably https://crbug.com/chromium/1025464. Assuming Security_Severity-High for now.

[Monorail components: Internals>Storage]

### ad...@google.com (2019-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-16)

[Empty comment from Monorail migration]

### ad...@google.com (2019-11-16)

OK, I've duly split this into sub-bugs and this remains merely a tracking bug to link them together.

Thanks again for the report  leonwxqian@!

### wf...@chromium.org (2019-11-16)

[Empty comment from Monorail migration]

[Monorail components: Blink>Storage>WebSQL]

### le...@gmail.com (2019-11-16)

Hi @adetaylor, thank you very much for spilting the bugs!

### sh...@chromium.org (2019-11-16)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-16)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-11-16)

[Empty comment from Monorail migration]

### pw...@chromium.org (2019-11-17)

I'll add the top-level bug for the defense-in-depth bypass as a dependency, so we can track the whole tree from here. 

### le...@gmail.com (2019-11-18)

Add a fuzzer for shadow tables that I've used to find some of those problems.

I used this fuzzer with sqlite shell, with defense in depth turned to OFF to find problems easier.

Set USE_FTS4 to 0 to fuzz (only) FTS3, or 1 to fuzz (only) FTS4.

#define USE_FTS4 0

Compile:

clang -c -g -fsanitize=address -fsanitize-coverage=trace-pc-guard sqlite3.c
clang++ -g -fsanitize=address -fsanitize-coverage=trace-pc-guard sqlite3.o fuzzer_fts3_fts4_.cpp ~/libFuzzer.a -o a


----------------------------------------

Also add a poc for a divide by zero bug it found this morning (not triggerable in chrome, only sqlite+fts4)

----------------------------------------

Wenxiang Qian of Tencent Blade Team

### le...@gmail.com (2019-11-18)

[Empty comment from Monorail migration]

### dr...@gmail.com (2019-11-18)

Fix for the poc_divide_by_zero.txt problem checked in at https://www.sqlite.org/src/info/10f8a3b718e0f47b

### dr...@gmail.com (2019-11-18)

All of the issues identified here should now be fixed on the SQLite trunk.

To reiterate, the single fix for the defense-in-depth bypass seen at https://www.sqlite.org/src/info/70390bbca49e7066 is sufficient to prevent any problems in Chrome.  All the other patches are needed only when the attacker has the capability to inject corrupted shadow tables, which should no longer be possible in Chrome after the https://www.sqlite.org/src/info/70390bbca49e7066 fix.

### mm...@chromium.org (2019-11-18)

leonwxqian@, have you heard of Chrome Fuzzer Program: https://www.google.com/about/appsecurity/chrome-rewards/#fuzzerprogram ?

Would you be interested in submitting your fuzzer through it and (potentially) receiving more rewards automatically (+$1,000 bonus on each valid vulnerability) after we start running it on ClusterFuzz?

### le...@gmail.com (2019-11-18)

Yes, cool, I'd like to submit my fuzzer through it :)

Does my code meet your requirements? If not I can do some work on it.

### mm...@chromium.org (2019-11-18)

Great to hear that! I think the code might need some cleanup. We'll help you to sort it out in code review, but if possible you can take a look at Chromium coding guidelines: https://www.chromium.org/developers/coding-style

As for adding a fuzz target, follow this doc: https://chromium.googlesource.com/chromium/src/+/master/testing/libfuzzer/getting_started.md

And if you never contributed to Chromium repo yourself, this will be helpful: https://chromium.googlesource.com/chromium/src/+/master/docs/contributing.md

If you have any questions, please send them to clusterfuzz-dev@chromium.org to keep the fuzzing discussion outside of this bug :)

### hu...@chromium.org (2019-11-19)

[Empty comment from Monorail migration]

### le...@gmail.com (2019-11-19)

Thank you for your information  @mmoroz, I am working on my code to meet the style requirements, when I'm done with the compile & test related work, I'll start the code review. :)

### hu...@chromium.org (2019-11-20)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-11-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/4d4e06ddc3b2804340f343e0551076ae25f06941

commit 4d4e06ddc3b2804340f343e0551076ae25f06941
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Thu Nov 21 20:15:53 2019

sqlite: Backport bugfixes.

Bug: 1025464, 1025465, 1025466, 1025467, 1025470, 1025471, 1025472, 1025473
Change-Id: I225d2f087dca947c320d40c1bab52da796ddf3a2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1925699
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Reviewed-by: Chris Mumford <cmumford@google.com>
Cr-Commit-Position: refs/heads/master@{#717774}

[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/README.chromium
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/ext/fts3/fts3.c
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/ext/fts3/fts3Int.h
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/ext/fts3/fts3_snippet.c
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/ext/fts3/fts3_write.c
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/src/build.c
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/test/altertab.test
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/test/fts4aa.test
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/test/fts4merge5.test
[modify] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patched/test/without_rowid7.test
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0001-Don-t-allow-shadow-tables-to-be-dropped-in-defensive.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0002-Improve-shadow-table-corruption-detection-in-fts3.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0003-Shadow-Table-Corruption-Detection-improvements-in-ft.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0004-Remove-reachable-NEVER-in-fts3.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0005-Better-corruption-detection-in-fts3.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0006-Detect-Prevent-infinite-recursion.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0007-Improve-corruption-detection-in-fts4.patch
[add] https://crrev.com/4d4e06ddc3b2804340f343e0551076ae25f06941/third_party/sqlite/patches/0008-Further-improve-corruption-detection-in-fts3.patch


### hu...@chromium.org (2019-11-21)

[Empty comment from Monorail migration]

### hu...@chromium.org (2019-11-21)

See comments on https://crbug.com/1025464#c11 (and onwards in that bug).

Survey response:
1. Yes, it should fit within the Merge Decision Guidelines. This is a Security_Severity-High bug, as labelled by the security team,  and this bug tracks several other security bugs of both medium and high severity.
2. https://crrev.com/c/1928298
3. The change has landed onto master, and should enter canary by tomorrow.
4. These changes are required as they are security-critical changes, discovered after branch in a security competition.
5. No
6. N/A

### hu...@chromium.org (2019-11-21)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-22)

Please update bug with canary result on Monday morning. 

+adetaylor@ for M79 merge review as well.

### hu...@chromium.org (2019-11-22)

pwnall@ has agreed to help push forward reviewing + pushing submit on the CLs while I'm OOO. Thanks!

### sh...@chromium.org (2019-11-22)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2019-11-22)

Adding huangdarwin@ back so he can keep tabs on this as well.

### ad...@chromium.org (2019-11-23)

govind@ The same CL fixes a load of bugs. The most important one to ship is https://crbug.com/chromium/1025464, so let's keep merge discussions on there - how does that sound? (I'm keen on merging/shipping the rest too)

### sh...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### go...@chromium.org (2019-11-25)

Re #32: Sure, please request merge in https://crbug.com/chromium/1025464 and remove "Merge-Review-79" label from here. 

### ad...@google.com (2019-11-25)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-02)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-03)

[Empty comment from Monorail migration]

### na...@google.com (2019-12-05)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-05)

Congrats! The Panel decided to reward $2,000 for this report!

### na...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-06)

[Empty comment from Monorail migration]

### le...@gmail.com (2019-12-06)

@natashapabrai Thank you!

BTW, do these vulnerabilities have CVEs assigned now (including those in TFC)?

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-10)

The scripts assigned a CVE for this, but as it's a tracking bug covering multiple vulnerabilities I won't actually be submitting a description for it. All the sub-bugs should have CVEs and descriptions.

### le...@gmail.com (2019-12-12)

Hi , could you please change the credit in https://chromereleases.googleblog.com/2019/12/stable-channel-update-for-desktop.html

[$TBD][1025466] High CVE-2019-13734, and
[$TBD][1025464] Medium CVE-2019-13750,  and 
[$TBD][1025465] Medium CVE-2019-13751

To:
Reported by Wenxiang Qian of Tencent Blade Team?

We used a random hash as team name in Tianfu Cup and it looks very odd😂... Thank you very much!

### aw...@google.com (2020-01-06)

[Empty comment from Monorail migration]

### [Deleted User] (2020-02-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1025467?no_tracker_redirect=1

[Multiple monorail components: Blink>Storage>WebSQL, Internals>Storage]
[Monorail blocked-on: crbug.com/chromium/1025463, crbug.com/chromium/1025470, crbug.com/chromium/1025471, crbug.com/chromium/1025472, crbug.com/chromium/1025473]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050707)*
