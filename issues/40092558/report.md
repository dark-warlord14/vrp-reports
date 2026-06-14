# Use-after free in leveldb

| Field | Value |
|-------|-------|
| **Issue ID** | [40092558](https://issues.chromium.org/issues/40092558) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P0 |
| **Component** | Blink, Blink>Storage>IndexedDB |
| **Reporter** | mi...@gmail.com |
| **Assignee** | dg...@chromium.org |
| **Created** | 2011-07-11 |
| **Bounty** | $3,133.00 |

## Description

**VULNERABILITY DETAILS**  

use-after-free in browser with indexeddatabase

**VERSION**  

Chrome Version: trunk  

Operating System: linux 64bit

**REPRODUCTION CASE**  

sorry for the complicated setup:

html:

<script>
eval("webkitIndexedDB.open('transaction-crash-on-abort')");
</script>

served from <http://george.fi/jepa.html> (uh oh).

start the browser with:  

/home/user/chromium/src/tools/valgrind/valgrind.sh /home/user/chromium/src/out/Release/chrome --no-first-run --user-data-dir=$HOME/fuzz/user/4 <http://george.fi/jepa.html>

and have user-data-dir.zip in $HOME/fuzz/user/4

I didn't manage to create a database for local files :(

user data dir contains a database that has:  

INSERT INTO "Databases" VALUES(2,'transaction-crash-on-abort','','');

and there are a couple of small binary files in the indexeddb directory.

this bug will also crash chromium-browser daily build with segfault at RIP.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

Crash State:  

Invalid read of size 8  

at 0x26EFF09: leveldb::InternalKeyComparator::FindShortSuccessor(std::string\*) const by 0x26FC506: leveldb::TableBuilder::Finish()  

Address 0x264c8750 is 0 bytes inside a block of size 16 free'd  

Address 0x4141414141414169 is not stack'd, malloc'd or (recently) free'd  

at 0x26EFF0C: leveldb::InternalKeyComparator::FindShortSuccessor(std::string\*) const

## Attachments

- [jepa.html](attachments/jepa.html) (text/plain; charset=us-ascii, 83 B)
- [user-data-dir.zip](attachments/user-data-dir.zip) (application/zip; charset=binary, 6.5 KB)
- [vg.txt](attachments/vg.txt) (text/x-c; charset=us-ascii, 32.7 KB)
- [debug-valgrind-88944.txt](attachments/debug-valgrind-88944.txt) (text/x-c; charset=us-ascii, 32.7 KB)

## Timeline

### mi...@gmail.com (2011-07-11)

btw, I don't own a george.fi and there is no file like that hosted there. it's just something I've mapped to localhost in my hosts file.

### in...@chromium.org (2011-07-12)

Hans, can you please take a look.

### ha...@chromium.org (2011-07-12)

I'm on holiday with bad Internet connectivity, so I probably can't look into this properly until I get back, on 25 July.

David, can you take a look? Judging by that Valgrind output, it seems this might be a problem in the LevelDB compaction code. A first step would be to try and reproduce this with a binary that has debug symbols so we can get line numbers, and then ping Sanjay and see if he has any ideas.

### mi...@gmail.com (2011-07-12)

here's a valgrind log from debug build.



### ha...@chromium.org (2011-07-12)

Thanks, that's very helpful!

The problem is that we delete the leveldb::Comparator* after we delete the leveldb::Database. Turns out that wasn't safe. We should fix this byhaving a static instance of the comparator, and pass in the address of that.

### dg...@chromium.org (2011-07-12)

I can reproduce locally with given profile directory but would like to simplify the reduction so that it can go in a layout test.

miaubiz, do you still have the hacked up transaction-crash-on-abort.html that you used to create the sqlite database?

Also, do you know what steps you went through to get yourself in this position, where you have both a sqlite database and a leveldb database from the same origin without having finished a migration?  Did you run with --indexeddb-use-sqlite?

### sc...@gmail.com (2011-07-13)

@dgrogan: can you remind us which version of Chrome stable will first feature an enabled-by-default leveldb? We should probably fix it before then. I can tag the bug accordingly.

### dg...@chromium.org (2011-07-13)

m14

### mi...@gmail.com (2011-07-13)

@dgrogan: sorry I don't know how it happened, and I don't have the file. 

I didn't run with --indexeddb-use-sqlite, just

 --disable-plugins --user-data-dir=$HOME/fuzz/user/4 --no-first-run

It did however happen through the browser, by which I mean I didn't touch the files on disk directly. It seemed to happen, or start getting triggered somewhere around thursday/friday last week both on the ubuntu daily build of chromium-browser and on my homebuilt chrome builds.

### dg...@chromium.org (2011-07-14)

It looks like the problem is the reverse of the description in https://crbug.com/chromium/88944#c5.  The behavior now is that leveldb::Comparator is deleted before leveldb::DB.  When the leveldb::DB was destructed but still had compaction work, the compaction would fail because the Comparator was invalid.

Hans, I didn't understand your "static" suggestion, mostly because I didn't know which Comparator you meant, leveldb::Comparator or WebCore::LevelDBComparator.  It appears they both need to outlive leveldb::DB.

The current order of destruction:
IDBLevelDBBackingStore
--LevelDBComparator
--LevelDBDatabase
----ComparatorAdapter : leveldb::Comparator
----leveldb::DB

I bluntly changed the order to that listed below in http://webkit.org/b/64494 and the crash is gone.
IDBLevelDBBackingStore
--LevelDBDatabase
----leveldb::DB
----ComparatorAdapter : leveldb::Comparator
--LevelDBComparator

If that patch is kosher then great, I'll commit it, but it's pretty awkward.  Hans, if you have suggestions for what to pass in where or changing the Ownership hierarchy, I think that'd be better.  I'll take a crack at it in a few days if I don't hear from you, especially given that you're on holiday and not supposed to be doing work :)

### sc...@gmail.com (2011-07-21)

The M14 branch point is Monday.... ideally, we could fix this before the branch point in order to avoid a merge?

### ha...@chromium.org (2011-07-25)

Sorry for being slow, I was away for the two last weeks.

I got it backwards in https://crbug.com/chromium/88944#c5, and after looking at David's patch this is probably simpler than I thought (I hadn't realized that we destroyed the comparator objects before the DB -- that's a bug).

I've commented on David's patch. Hopefully we can squeeze this in before the branch, but if we don't it should be a very simple merge.

### sc...@gmail.com (2011-07-25)

Thanks, Hans... I can do the merge if one is necessary.

### sc...@gmail.com (2011-07-26)

http://trac.webkit.org/changeset/91721

Thanks! I'll keep an eye on whether this makes the branch, and deal with it appropriately.

### dg...@chromium.org (2011-07-27)

Looks like it didn't make it.

### js...@chromium.org (2011-07-28)

Bulk move for WillMerge change.

### js...@chromium.org (2011-07-28)

Bulk move for WillMerge change.

### sc...@gmail.com (2011-07-29)

Indeed not. Merged to M14: http://trac.webkit.org/changeset/92021

### sc...@gmail.com (2011-07-29)

Ooh, need to send this one to the panel :)

### sc...@gmail.com (2011-08-02)

@miaubiz: congrats!!!!! This is worth a rarely-rewarded $3133.7 Chromium Security Reward :D
It's a web-triggerable memory corruption in the browser process, which is by definition a critical bug. Thanks for catching it early in the development cycle such that we were able to fix it before Chrome 14 went to stable.

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

### mi...@gmail.com (2011-08-02)

thank you sir!

regarding boilerplate text, there shouldn't be any affected users anymore since m14 and m15 are both fixed? 

i.e. can I talk about it publicly already?

### sc...@gmail.com (2011-08-02)

Yes, you can :) Fix should have gone out to dev channel in today's 14.0.835.15 release in fact.
I've removed the view restriction on the bug.

### sc...@gmail.com (2011-08-09)

Paid as part of a rollover jackpot $10,633.70 total payout :)

### js...@chromium.org (2011-10-05)

Batch update.

### bu...@chromium.org (2012-10-13)

This issue has been closed for some time. No one will pay attention to new comments.
If you are seeing this bug or have new data, please click New Issue to start a new bug.

### la...@google.com (2012-10-17)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-13)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-03-21)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### bu...@chromium.org (2013-04-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/88944?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink, Blink>Storage>IndexedDB]
[Monorail mergedwith: crbug.com/chromium/90245]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40092558)*
