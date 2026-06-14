# [LangFuzz] Crash at v8::internal::StoreBuffer::Compact with invalid write

| Field | Value |
|-------|-------|
| **Issue ID** | [40078626](https://issues.chromium.org/issues/40078626) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Linux |
| **Reporter** | de...@googlemail.com |
| **Assignee** | ul...@chromium.org |
| **Created** | 2014-01-03 |
| **Bounty** | $3,000.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101 Firefox/28.0

Steps to reproduce the problem:
1. Run the following JS code in d8 as used in the specified Chrome version (SVN r18421, branch 3.23, 64 bit):

function boom() {
  var args = [];
  for (var i = 0; i < 125000; i++)
    args.push(i);
  return Array.apply(Array, args);
}
var array = boom();
function fib(n) {
  var f0 = 0, f1 = 1;
  for (; n > 0; n = n -1) {
    f0 + f1;
    f0 = array;
  }
}
fib(75);

What is the expected behavior?
No crash.

What went wrong?
d8 crashes with a GC corruption:

==15142== Invalid write of size 8
==15142==    at 0x6D3923: v8::internal::StoreBuffer::Compact() (in 3.23/out/x64.release/d8)
==15142==    by 0x5C4A5C: v8::internal::MarkCompactCollector::MigrateObject(unsigned char*, unsigned char*, int, v8::internal::AllocationSpace) (in 3.23/out/x64.release/d8)
==15142==    by 0x5C55F5: v8::internal::MarkCompactCollector::DiscoverAndPromoteBlackObjectsOnPage(v8::internal::NewSpace*, v8::internal::NewSpacePage*) (in 3.23/out/x64.release/d8)
==15142==    by 0x5C5C43: v8::internal::MarkCompactCollector::EvacuateNewSpace() (in 3.23/out/x64.release/d8)
==15142==    by 0x5DD285: v8::internal::MarkCompactCollector::EvacuateNewSpaceAndCandidates() (in 3.23/out/x64.release/d8)
==15142==    by 0x5DF273: v8::internal::MarkCompactCollector::SweepSpaces() (in 3.23/out/x64.release/d8)
==15142==    by 0x5DF361: v8::internal::MarkCompactCollector::CollectGarbage() (in 3.23/out/x64.release/d8)
==15142==    by 0x500DE6: v8::internal::Heap::PerformGarbageCollection(v8::internal::GarbageCollector, v8::internal::GCTracer*) (in 3.23/out/x64.release/d8)
==15142==    by 0x501404: v8::internal::Heap::CollectGarbage(v8::internal::AllocationSpace, v8::internal::GarbageCollector, char const*, char const*) (in 3.23/out/x64.release/d8)
==15142==    by 0x6104E0: v8::internal::JSObject::SetFastElementsCapacityAndLength(v8::internal::Handle<v8::internal::JSObject>, int, int, v8::internal::JSObject::SetFastElementsCapacitySmiMode) (in 3.23/out/x64.release/d8)
==15142==    by 0x63187E: v8::internal::JSObject::SetDictionaryElement(v8::internal::Handle<v8::internal::JSObject>, unsigned int, v8::internal::Handle<v8::internal::Object>, PropertyAttributes, v8::internal::StrictModeFlag, bool, v8::internal::SetPropertyMode) (in 3.23/out/x64.release/d8)
==15142==    by 0x632380: v8::internal::JSObject::SetElementWithoutInterceptor(v8::internal::Handle<v8::internal::JSObject>, unsigned int, v8::internal::Handle<v8::internal::Object>, PropertyAttributes, v8::internal::StrictModeFlag, bool, v8::internal::SetPropertyMode) (in 3.23/out/x64.release/d8)
==15142==  Address 0x21de18914000 is not stack'd, malloc'd or (recently) free'd

I was not able to reproduce this properly in my release build of Chromium, but I suspect this is due to different GC timings and with a little effort, this could be solved. A test for d8 is also likely to be more valuable to find the actual problem.

Did this work before? Yes V8 branch 3.22 seems to work fine.

Chrome version: 33.0.1750.5  Channel: dev
OS Version: Ubuntu Linux 12.04 LTS
Flash Version: Shockwave Flash 11.2 r202

In branch 3.22 I get this weird error:

test.js:3: illegal access
  for (var i = 0; i < 125000; i++)
                               ^

instead of a crash.

## Timeline

### cl...@chromium.org (2014-01-03)

[Empty comment from Monorail migration]

### aa...@google.com (2014-01-03)

[Empty comment from Monorail migration]

### ma...@chromium.org (2014-01-03)

Assign to current V8 sheriff.

### ul...@chromium.org (2014-01-03)

The stack trace looks similar to https://code.google.com/p/chromium/issues/detail?id=329772

decoder.oh, can you reproduce this reliably in standalone d8 or does it require running with valgrind?

In the latter case, could you please post command line you use to invoke it?

I tried r18421 with
# out/x64.release/d8 test-1.js
and 
# tools/run-valgrind.py out/x64.release/d8 test-1.js
and could not reproduce the crash.





### de...@googlemail.com (2014-01-03)

It seems that due to a configuration mistake in the fuzzer, it was using v8-trunk, not v8-3.23. I confirmed that the issue reproduces on v8-trunk, latest revision.

Maybe this still helps you to track down your GC regression :)

### de...@googlemail.com (2014-01-03)

Ah, now it also reproduces on 3.23, but you need to use --expose_gc:

$ LangFuzz/3.23/out/x64.release/d8 --expose_gc min.js
Segmentation fault

I don't know exactly why that option matters here because gc() isn't explicitly called. But the branch is affected :) Sorry for the confusion.

### ul...@chromium.org (2014-01-03)

Thanks, decoder.oh.

With --expose_gc, I can reproduce the crash.

### cl...@chromium.org (2014-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-05)

ClusterFuzz is analyzing your testcase. See https://cluster-fuzz.appspot.com/testcase?key=5653405448011776

### mb...@chromium.org (2014-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-05)

[Empty comment from Monorail migration]

### ul...@chromium.org (2014-01-07)

I think I found the bug. In StoreBuffer::ExemptPopularPages:
https://code.google.com/p/v8/source/browse/trunk/src/store-buffer.cc#227
the check (old_counter == threshold) doesn't make sense to me. I think it should be (old_counter >= threshold). With this fix, the crash doesn't reproduce.

Michael, Hannes, do you agree? If yes, I'll upload the fix.

### ia...@chromium.org (2014-01-07)

[Empty comment from Monorail migration]

### hp...@chromium.org (2014-01-07)

Yes Ulan, LGTM. Upload the fix.

### ul...@chromium.org (2014-01-07)

Thanks, Hannes. The fix is here: https://codereview.chromium.org/125983002/

### in...@chromium.org (2014-01-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-01-09)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ul...@chromium.org (2014-01-16)

We got canary coverage. Merged to V8 branch 3.23 (M33):  http://code.google.com/p/v8/source/detail?r=18637

I will merge to V8 branch 3.22 (M32) after getting merge approval.

### dh...@google.com (2014-01-16)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-17)

ulan how safe is this? it didn't go to m33 beta yet but i am cutting stable so i need you to let me know. else it will have to wait till round 3 if we have one.

### ul...@chromium.org (2014-01-20)

kareng@, this should be safe.

### ka...@google.com (2014-01-21)

[Empty comment from Monorail migration]

### ka...@google.com (2014-01-21)

[Empty comment from Monorail migration]

### jk...@chromium.org (2014-01-21)

Merged the fix to V8's 3.22 branch: http://code.google.com/p/v8/source/detail?r=18724

### in...@chromium.org (2014-01-23)

[Empty comment from Monorail migration]

### dh...@google.com (2014-01-23)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-01-27)

Thanks for the report! This one qualifies for a $3000 reward because it seems like the address that is written to is controllable.

### ti...@chromium.org (2014-02-28)

[Empty comment from Monorail migration]

### ti...@chromium.org (2014-03-17)

Processing via our e-payment system can take a few weeks, but reward should be on its way to you. Please do NOT publicly disclose details until a fix has been released to all our users. Thanks again for your help!

### cl...@chromium.org (2014-04-17)

Bulk update: removing view restriction from closed bugs.

### cl...@chromium.org (2014-05-16)

This bug is a regression and does not impact stable. Removing incorrectly added Release-1-M32 label.

- Your friendly ClusterFuzz

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

This issue was migrated from crbug.com/chromium/331444?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40078626)*
