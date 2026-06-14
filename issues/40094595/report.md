# Security: Possible OOB related to chrome_sqlite3_malloc

| Field | Value |
|-------|-------|
| **Issue ID** | [40094595](https://issues.chromium.org/issues/40094595) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Storage |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **CVE IDs** | CVE-2019-5827 |
| **Reporter** | ml...@stanford.edu |
| **Assignee** | hu...@chromium.org |
| **Created** | 2019-04-12 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Possible OOB with chrome\_sqlite3\_malloc

**REPRODUCTION CASE**  

There's a pattern of using sqlite malloc functions that call chrome\_sqlite3\_malloc in combination with traditional memory operations (e.g., memcpy). There may be invariants that make this ok, or a principle here that I am not aware of. Thanks for your time.

chrome\_sqlite3\_malloc takes an int size argument, while memcpy takes a size\_t size argument. On x86-64 this means that chrome\_sqlite\_3\_malloc's size argument is width 32, while memcpy's is width 64. This can lead to potentially concerning wrapping behavior for extreme allocation sizes (depending on the compiler, optimizations, etc).

For example:

Function fts3UpdateDocTotals  

(<https://cs.chromium.org/chromium/src/third_party/sqlite/patched/ext/fts3/fts3_write.c?type=cs&q=fts3UpdateDocTotals&g=0&l=3399>)

(1) a = sqlite3\_malloc( (sizeof(u32)+10)\*nStat );  

(<https://cs.chromium.org/chromium/src/third_party/sqlite/patched/ext/fts3/fts3_write.c?type=cs&q=fts3UpdateDocTotals&g=0&l=3416>)  

...  

(2) memset(a, 0, sizeof(u32)\*(nStat) );  

(<https://cs.chromium.org/chromium/src/third_party/sqlite/patched/ext/fts3/fts3_write.c?type=cs&q=fts3UpdateDocTotals&g=0&l=3434>)

Depending on optimization level etc, this may turn into:

(1)  

size = mul i32 nstat 14  

chrome\_sqlite3\_malloc(size)

(2)  

tmp = sign extend nstat to i64  

size = shl tmp 2  

memset(size)

If nstat is a very large i32, the multiplication in step (1) \*may\* wrap. Nothing in (2) will wrap because of the sign extend, leading to an OOB.

## Timeline

### ct...@chromium.org (2019-04-12)

+pwnall@ as owner of third_party/sqlite.

+mpdenton@ who may be able to help evaluate the security concerns here.

[Monorail components: Internals>Storage]

### mp...@google.com (2019-04-12)

Indeed, I have a feeling there are a number of integer overflows in the sqlite code, especially FTS3. It would likely be useful to look through all the usages of sqlite_malloc with a multiplication as an argument, but perhaps that's every single allocation.... :)

As for #1, it looks like nStat is the number of user-defined FTS3 columns plus two, as mentioned in the comment. pwnall@ or Dr. Hipp, is there a limit on the number of user-definable FTS3 columns? If so, it may be useful to define an assert that (sizeof(u32)+10)*MAX_NSTAT doesn't overflow, so that this allocation's size can never overflow. #2 looks like a subset of #1, I think. If there is no maximum limit, then this is a high-severity security bug.

Perhaps we could change all multiplications within mallocs to instead invoke a macro that either (a) does the multiplication, or (b) does the multiplication and checks for overflow. (a) could be the default, but Chrome could turn (b) on for extra security.

### dr...@gmail.com (2019-04-13)

I cannot see the rest of this ticket so I don't know the specifics of the concern, but you have given me enough information to guess.  The https://www.sqlite.org/src/info/0b6ae032c28e7fe3 check-in should resolve the issue in multiple ways.

(1) I audited all memory allocation calls to ensure that the size is computed using 64-bit arithmetic and 64-bit variables.

(2) The limit on the number of columns (default: 2000, max: 32767) is now actively enforced for virtual tables.  This was a limit that was formerly overlooked.

Before change (2), the limit on the number of columns in a CREATE VIRTUAL TABLE statement was imposed by the maximum length of an SQL statement, which default to 1,000,000,000 bytes.  If every column has a one-byte name, and then a comma separator, that was a practical limit of a little less than 500M columns, which was enough to cause trouble before the fix in (1).

We are hoping to release SQLite version 3.28.0 with this fix before Easter.

You can also lower the maximum SQL length at compile-time, or at runtime.  At compile-time use the -DSQLITE_MAX_SQL_LENGTH=... option.  At runtime invoke sqlite3_limit(db,SQLITE_LIMIT_SQL_LENGTH,...).  Surely it would not hurt to limit the maximum SQL statement length to something like 100MB or even 10MB, for defensive purposes.  Lowering the SQL statement length limit to 100MB is more than sufficient to prevent the attack, assuming I am correctly guessing at the specifics of what the attack is.

### dr...@gmail.com (2019-04-13)

After posting the previous, suddenly I was able to see the rest of the ticket, and  the vulnerability I found is different from the one you found, I think.  Nevertheless, fix (2) from my previous comment should be sufficient to resolve the concern.  And (1) was also an issue which has now been fixed too.  There is now an additional check-in at https://www.sqlite.org/src/info/07ee06fd390bfebe which should address your issue.  I will double-check the assertion of the previous sentence tomorrow.

We will do another audit of memory allocation to try to find any similar issues before the 3.28.0 release comes out.

### pw...@chromium.org (2019-04-13)

huangdarwin@: Let's backport both patches --
https://www.sqlite.org/src/info/0b6ae032c28e7fe3 
https://www.sqlite.org/src/info/07ee06fd390bfebe


### ml...@stanford.edu (2019-04-13)

I can make the tool look at allocations as well in the next few days. Thanks all!

### ct...@chromium.org (2019-04-15)

Setting some security triage labels. Thanks for looking into this.

### hu...@chromium.org (2019-04-15)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/517ac71c9ee27f856f9becde8abea7d1604af9d4

commit 517ac71c9ee27f856f9becde8abea7d1604af9d4
Author: Darwin Huang <huangdarwin@chromium.org>
Date: Mon Apr 15 22:41:39 2019

sqlite: backport bugfixes for dbfuzz2

Bug: 952406
Change-Id: Icbec429742048d6674828726c96d8e265c41b595
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1568152
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#651030}
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/amalgamation/sqlite3.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/fts3/fts3_snippet.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/fts3/fts3_test.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/fts3/fts3_tokenize_vtab.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/fts3/fts3_tokenizer.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/fts3/fts3_write.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/fts5/fts5_tokenize.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/ext/rtree/geopoly.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/build.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/expr.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/main.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/test_fs.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/util.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/vdbeaux.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/vdbesort.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patched/src/vtab.c
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0001-Virtual-table-supporting-recovery-of-corrupted-datab.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0002-Custom-shell.c-helpers-to-load-Chromium-s-ICU-data.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0003-Fix-compilation-with-SQLITE_OMIT_WINDOWFUNC.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0004-Fix-dbfuzz2.c-compilation-errors-on-Windows.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0005-Fix-Heap-buffer-overflow-in-vdbeRecordCompareInt.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0006-fix-heap-buffer-overflow-in-cellsizeptr.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0007-fix-integer-overflow-in-checkList.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0008-Fix-Heap-use-after-free-in-releasePageNotNull.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0009-Fix-dangling-pointer-dereference.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0010-Fix-faulty-assert-statement.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0011-Add-dbfuzz2-progress-handler-patch.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0012-Use-fixed-width-integer-type.patch
[modify] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0013-Do-early-detection-for-corrupt-schema.patch
[add] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0014-Enforce-the-SQLITE_LIMIT_COLUMN-limit-on-virtual-tab.patch
[add] https://crrev.com/517ac71c9ee27f856f9becde8abea7d1604af9d4/third_party/sqlite/patches/0015-Use-64-bit-memory-allocator-in-extensions.patch


### hu...@chromium.org (2019-04-22)

Hey mlfbrown@, I believe this has been fixed by the fix in #9, so will mark this as Fixed. Please reply to this bug if this is not the case. Thank you!

### na...@google.com (2019-04-22)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-23)

Requesting merge to M74 because latest trunk commit (651030) appears to be after beta branch point (638880).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-04-23)

This bug requires manual review: Request affecting a post-stable build
Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), dgagnon@(ChromeOS), abdulsyed@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2019-04-23)

We already cut M74 RC and ready for stable release today for Android and Desktop. 

If approved and merged, this change will be in included in next M74 respin if any.

+adetaylor@ (Security TPM for merge review) and release TPMS as FYI

### ad...@chromium.org (2019-04-23)

Yes, I think this should be backported into the next M74 respin if any.

mlfbrown@stanford.edu, thanks for the report!

### hu...@chromium.org (2019-04-25)

adetaylor@, please review this for merge. https://crrev.com/c/1583390

### ad...@google.com (2019-04-25)

Thanks, but it's up to govind@ to mark this as Merge-Approved-74. Thanks for doing it though!

### na...@google.com (2019-04-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### go...@chromium.org (2019-04-25)

Approving merge to M74 branch 3729 based on https://crbug.com/chromium/952406#c16 and #17. 

### na...@google.com (2019-04-25)

Congrats - the panel decided to reward $500 for this report

### na...@google.com (2019-04-25)

[Empty comment from Monorail migration]

### cr...@appspot.gserviceaccount.com (2019-04-26)

The following revision refers to this bug: 
https://chromium.googlesource.com/chromium/src.git/+/df9af43837edf38930ad4618cb10cc4af3835120

Commit: df9af43837edf38930ad4618cb10cc4af3835120
Author: huangdarwin@chromium.org
Commiter: huangdarwin@chromium.org
Date: 2019-04-26 17:57:32 +0000 UTC

sqlite: backport bugfixes for dbfuzz2

Note that this is a separate cherry pick for M74.

(cherry picked from commit 517ac71c9ee27f856f9becde8abea7d1604af9d4)

Bug: 952406
Change-Id: Icbec429742048d6674828726c96d8e265c41b595
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1568152
Reviewed-by: Chris Mumford <cmumford@google.com>
Commit-Queue: Darwin Huang <huangdarwin@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#651030}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1583390
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/branch-heads/3729@{#937}
Cr-Branched-From: d4a8972e30b604f090aeda5dfff68386ae656267-refs/heads/master@{#638880}


### aw...@google.com (2019-04-30)

[Empty comment from Monorail migration]

### ad...@google.com (2019-04-30)

drhsqlite@gmail.com: do you plan to assign a CVE number here? Thanks!

### dr...@gmail.com (2019-04-30)

I don't asssign CVE numbers.  I didn't even know that was something I could do.

### ad...@google.com (2019-05-02)

Hi drhsqlite@gmail.com - thanks for the reply - I had a chat with awhalley@ about CVE numbers. The official way to do it is via https://cveform.mitre.org/ which presumably you can use at any time. Alternatively, we have a pre-allocated block and we believe we can use one of them for this. (We retrospectively submit short descriptions for the CVEs we allocate from the block).

Whichever you prefer - let us know.

The only reason we want a CVE number is for the release notes here:
https://chromereleases.googleblog.com/2019/04/stable-channel-update-for-desktop_30.html
People are already excitable in the twittersphere that we haven't provided a CVE yet: "OMG, it's so serious that they fixed it before they even allocated a CVE! Everyone's going to die!" (paraphrasing only very slightly)


### dr...@gmail.com (2019-05-02)

I think it would be best if you handled this.

I don't really understand CVEs.  I did some searching and reading on the subject this morning, but those efforts did not seem to increase my understanding by very much.  Since you seem to have more experience in this arena, I think the outcome might be better if you did it.  I will pay attention and try to learn.

### ad...@google.com (2019-05-02)

drhsqlite@gmail.com - you probably know as much as I do. awhalley@ is the expert.

In any case I've taken a CVE from our pool - CVE-2019-5827 - and added the label here. That CVE number refers to the issue reported in this bug, rather than anything else fixed in the patches that you did. At some stage in the future we will write a description for the CVE and submit it to MITRE.

Adding these labels to this bug should automatically cause our various nagging-bots to prompt us to do the description-writing-and-submission-stuff in future. For now, just allocating the number is all that happens, such that external people can refer to this bug in a consistent way.

### mm...@chromium.org (2019-05-13)

[Empty comment from Monorail migration]

### mm...@chromium.org (2019-05-17)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2019-07-30)

This issue was migrated from crbug.com/chromium/952406?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094595)*
