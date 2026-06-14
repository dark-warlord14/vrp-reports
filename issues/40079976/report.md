# Use-of-uninitialized-value in SkFlatDictionary<SkPaint, SkPaint::FlatteningTraits>::findAndReturnMutableF

| Field | Value |
|-------|-------|
| **Issue ID** | [40079976](https://issues.chromium.org/issues/40079976) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@chromium.org |
| **Assignee** | su...@chromium.org |
| **Created** | 2014-07-02 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4806825801154560

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  SkFlatDictionary<SkPaint, SkPaint::FlatteningTraits>::findAndReturnMutableF
  SkPictureRecord::drawPath
  SkBBoxRecord::drawPath
  

Minimized Testcase (0.87 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95gw1QQIQOOC7pFGMAbg4ew93ka-rsWj7eJkbhS9jv87dTnPA7AlXfXcDjz72ZNW9BVej6Y0CeX7X_xRfSUqce9KOulmLuaOSCN0FleHHl6bSE5mHSYnATGOV2P3kKSNRJX16Qh-1F8p2WtzeEFKaBX_w2giw
Filer: aarya@google.com

## Timeline

### in...@chromium.org (2014-07-02)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-07-02)

Sugoi@, we need someone to spearhead these MSAN bugs. Can someone from your team look into these. They should be easy to fix as it just needs intializing the vars.

### cl...@chromium.org (2014-07-02)

[Empty comment from Monorail migration]

### su...@chromium.org (2014-07-08)

Delegating to someone who knows about SkFlatDictionary.

### [Deleted User] (2014-07-08)

Looks like the same as https://code.google.com/p/chromium/issues/detail?id=381156 ?

We haven't changed that code since then, so I guess my analysis and questions from over there still stand: I can't see how it's possible to read fArray without having first allocated fCapacity zero pointers with calloc.  Does MSAN understand calloced memory is zeroed?

Is there a way to set up suppressions for MSAN?  I'd set up a MSAN bot for Skia, but we call into a lot of system code, particularly font and GPU drivers.

### [Deleted User] (2014-07-09)

It is actually the *index* that is poisoned. It is derived from a hash of a SkDashPathEffect object, in which fPhase and fInitialDashIndex may be uninitialized, if this branch is taken during construction:

https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/utils/SkDashPath.cpp&rcl=1404816569&l=75

The issue is benign, but we should still initialize those members properly.

> Is there a way to set up suppressions for MSAN?  I'd set up a MSAN bot for Skia, but we call into a lot of system code, particularly font and GPU drivers.

We don't support suppressions. In Chromium one can set a flag to rebuild all DSO dependencies with MSan instrumentation (about 50 packages). This eliminates most false positives coming from system code. If you're interested, we could think about making this setup reusable across projects. For Skia you'll likely need only a subset of those packages, so ideally each project should be able to choose which ones it needs.

### [Deleted User] (2014-07-09)

Oh interesting.  That makes a lot more sense.  Will dig into that SkDashPath code and make sure everything's initialized.


It's going to be tricky not supporting suppressions.  We deal pretty intimately with GPU drivers, which are pretty much all closed binary blobs.  E.g.:

UMR in __interceptor_strlen at offset 0 inside [0x60600000ee80, +37) 
==6670== WARNING: MemorySanitizer: use-of-uninitialized-value
    #0 0x7fa833eaa385 (/usr/lib/nvidia-331/libGL.so.1+0xc0385)

SUMMARY: MemorySanitizer: use-of-uninitialized-value ??:0 ??
Exiting

I guess we could restrict MSAN to testing the non-GPU parts of Skia on headless bots?  Even still, recompiling all dependencies is kind of a pain.  Is there any sort of --keep-going setting so we can run and filter away expected failures post-facto?

### eu...@google.com (2014-07-09)

Well, there is a flag, but it's not well tested and completely unused. Try
-mllvm -msan-keep-going=1


### [Deleted User] (2014-07-09)

> We deal pretty intimately with GPU drivers, which are pretty much all closed binary blobs.

In Chromium we run MSan builds with --use-gl=osmesa. I take it you don't have that option?

### eu...@google.com (2014-07-09)

But I doubt it will help you run without rebuilding dependencies. There will be a huge number of reports, very bad performance and it will be hard to understand if a report is caused by an uninstrumented system library or not. For example, if a library call did not initialize some memory that's allocated in your code and used in your code, report will only mention your code.


### [Deleted User] (2014-07-09)

Yeah, this does all sound tricky.  I think we'll just stick with Valgrind for now.

### cl...@chromium.org (2014-07-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5989586578702336

Fuzzer: Inferno_twister
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  SkFlatDictionary<SkPaint, SkPaint::FlatteningTraits>::findAndReturnMutableF
  SkPictureRecord::drawPoints
  SkBBoxRecord::drawPoints
  

Minimized Testcase (0.09 Kb):
Download: https://cluster-fuzz.appspot.com/download/AMIfv97Zg5jKSQUSFdwjDjaj3QwZNDobW2VfdVGpAiOuHgxniCA00n8aQl3KsExguNGYi3PPSmj8JwVMA62K55U2Kcs_8UXg_xqngIZX6m5r2k7idR2E6fSEEswnKyOtgg9bzjTs6JkfjWQX9qxGPFpg9dyNjDMoMQ
<style>
* { background-position-y: -57%; outline: dashed 35px; outline-offset: 2147483552px;

Filer: earthdok@chromium.org

### cl...@chromium.org (2014-07-11)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4999098132332544

Fuzzer: Inferno_twister
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  SkFlatDictionary<SkPaint, SkPaint::FlatteningTraits>::findAndReturnMutableF
  SkPictureRecord::drawRect
  SkBBoxRecord::drawRect
  

Minimized Testcase (0.50 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95ZqkyBWI5NXDUnouKYqEJHuecHlpE7-43tkEHTBL5bdFxZYlRFNzCAff8bt7k5JQK_zS2ExOIxxgolM8ddewyJwxWCgvr-5DM_pW0ArXWOO8RstbQe2hxtJe0L18wim0iuVqPxXWPvIdjUNhRTDDZGNXpUEQ
Filer: earthdok@chromium.org

### mb...@chromium.org (2014-07-11)

Bulk edit of uninitialized value bugs without milestones to M-37.

### cl...@chromium.org (2014-07-11)

ClusterFuzz has detected this issue as fixed in range 282042:282480.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4806825801154560

Fuzzer: Miaubiz_svg_fuzzer
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  SkFlatDictionary<SkPaint, SkPaint::FlatteningTraits>::findAndReturnMutableF
  SkPictureRecord::drawPath
  SkBBoxRecord::drawPath
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=282042:282480

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95gw1QQIQOOC7pFGMAbg4ew93ka-rsWj7eJkbhS9jv87dTnPA7AlXfXcDjz72ZNW9BVej6Y0CeX7X_xRfSUqce9KOulmLuaOSCN0FleHHl6bSE5mHSYnATGOV2P3kKSNRJX16Qh-1F8p2WtzeEFKaBX_w2giw

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-07-11)

ClusterFuzz has detected this issue as fixed in range 282042:282480.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5989586578702336

Fuzzer: Inferno_twister
Job Type: Linux_msan_chrome

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  - crash stack -
  SkFlatDictionary<SkPaint, SkPaint::FlatteningTraits>::findAndReturnMutableF
  SkPictureRecord::drawPoints
  SkBBoxRecord::drawPoints
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=282042:282480

Minimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv97Zg5jKSQUSFdwjDjaj3QwZNDobW2VfdVGpAiOuHgxniCA00n8aQl3KsExguNGYi3PPSmj8JwVMA62K55U2Kcs_8UXg_xqngIZX6m5r2k7idR2E6fSEEswnKyOtgg9bzjTs6JkfjWQX9qxGPFpg9dyNjDMoMQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### cl...@chromium.org (2014-07-20)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### in...@chromium.org (2014-07-28)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-28)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-07-30)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-08-01)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-09)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-17)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-08-24)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### ke...@chromium.org (2014-08-26)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-08-31)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-08)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-09-15)

mtklein@: Uh oh! This issue is still open and hasn't been updated in the last 7 days. Since this is a serious security vulnerability, we want to make sure progress is happening. Can you update the bug with current status, and what, if anything, is blocking?

If you are not the right Owner for this bug, please find someone else to own it as soon as possible and remove yourself as Owner.

If the issue is already fixed or you are to unable to reproduce it, please close the bug. (And thanks for fixing the bug!).

These nags can be disabled by adding a 'WIP' label and an optional codereview link.

- Your friendly ClusterFuzz

### mb...@chromium.org (2014-09-17)

Are the fixed reports on this one correct? If so, please update the status to Fixed.

### [Deleted User] (2014-09-17)

Yes, this code is both fixed and no longer running.

### cl...@chromium.org (2014-09-17)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@chromium.org (2014-09-23)

Matthew - Merge requested for M38 (Branch 2125)

### [Deleted User] (2014-09-23)

FYI, the change to merge is https://skia.googlesource.com/skia/+/1c577cd3ee331944b9061ee0eec147b211ee563c which applies to third_party/skia

As mentioned above, this issue is pretty benign (it may rarely cause a relatively unimportant cache miss) so you might not want to bother.

### [Deleted User] (2014-09-23)

Per https://crbug.com/chromium/391001#c37, punting to 39.  Removing Merge-Request label since 39 hasn't branched.

### ti...@chromium.org (2014-09-23)

Targeting to M39 based on c#37

### am...@chromium.org (2014-11-15)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks again for the fuzzer contribution! This report qualified for a $500 reward.

Sorry for not ccing you on this one earlier.

### ti...@google.com (2014-12-09)

Payment in progress.

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2014-12-24)

Bulk update: removing view restriction from closed bugs.

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

This issue was migrated from crbug.com/chromium/391001?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40079976)*
