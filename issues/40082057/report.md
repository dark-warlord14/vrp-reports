# Stack-buffer-overflow in SkPackBits::Unpack8

| Field | Value |
|-------|-------|
| **Issue ID** | [40082057](https://issues.chromium.org/issues/40082057) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | hc...@chromium.org |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4850438600392704

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Stack-buffer-overflow WRITE {*}
Crash Address: 0x7f13a2a961a0
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  

Minimized Testcase (0.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95xhahb1WrHetK7cz9iOV1mcklp1LgIbysTBxxHtNYQqpYHGvj0K5TFsy541aRVGw5JJVXdGbeM-RIu-mlL3HtFR6__1-T9hVgjoR8HDJynbsR3YKlfFj3XQLxOIjDndSDftnnGwPOW32bwMyRi8dUdMn6yeg

Filer: mbarbella

## Timeline

### mb...@chromium.org (2015-05-11)

Bulk edit: I'm starting to look at some of the crashes from the batch of test cases we got now, but could use help with triage.

### mb...@chromium.org (2015-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-05-20)

sugoi@ - It looks like Unpack8() really needs to check the destination size, because the output can expand to 128 times the input. And the only callers I can find are this site and test code, so it should be a straight forward enough fix.

### su...@chromium.org (2015-05-20)

Delegating to reed@

### js...@chromium.org (2015-05-20)

I've been told that appealing to mtklien@ might result in the most expedient fix. Although, if the barrier to getting the CL landed in the skia repo isn't too high I'd be happy to do simply write it myself (it's an easy enough patch).

### [Deleted User] (2015-05-20)

Sure!  If you're familiar with Chromium, writing a Skia patch is easy.  You can usually just cd into third_party/skia and work there, or have a look at https://skia.org/user/quick/linux to start from scratch.  Send the CL my way.

### cl...@chromium.org (2015-05-21)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4810294212165632

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xf46b1190
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  

Minimized Testcase (0.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95QUdnyznVEJx30PR0FdjSsZJm5fVlP920hid6jx99QkdEndpq_tAOtRvxP7zTm3P0yl5CfvHqzVvWKGHVIkU36DW4ZKWdhsRmE268bbyVidY5v6FOBlJfX7Ack0XwlcDrTtnf1NKdH6028xri5OXGPUJfmCw

Filer: mbarbella

### [Deleted User] (2015-05-21)

[Empty comment from Monorail migration]

### js...@chromium.org (2015-05-21)

The question I have here is that there are five Pack variants, but as far as I can tell only that Pack8 version is ever used, and it's used in only one place. Since all the unused variants have the obvious same problems, my inclination is to remove them rather than fix them.

### [Deleted User] (2015-05-21)

That SGTM.

### cl...@chromium.org (2015-05-22)

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4850438600392704

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub

Crash Type: Stack-buffer-overflow WRITE {*}
Crash Address: 0x7f13a2a961a0
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  

Minimized Testcase (0.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95xhahb1WrHetK7cz9iOV1mcklp1LgIbysTBxxHtNYQqpYHGvj0K5TFsy541aRVGw5JJVXdGbeM-RIu-mlL3HtFR6__1-T9hVgjoR8HDJynbsR3YKlfFj3XQLxOIjDndSDftnnGwPOW32bwMyRi8dUdMn6yeg



### js...@chromium.org (2015-05-22)

Patch up for review at: https://codereview.chromium.org/1152163004/

### bu...@chromium.org (2015-06-04)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/699b852e48da8f71c19fcaa13bb109efd68e5c7d

commit 699b852e48da8f71c19fcaa13bb109efd68e5c7d
Author: jschuh <jschuh@chromium.org>
Date: Thu Jun 04 22:10:37 2015

Remove unused PackBits methods and fix length checks

Also a bit of general cleanup.

BUG=chromium:486944

Review URL: https://codereview.chromium.org/1152163004

[modify] http://crrev.com/699b852e48da8f71c19fcaa13bb109efd68e5c7d/include/core/SkPackBits.h
[modify] http://crrev.com/699b852e48da8f71c19fcaa13bb109efd68e5c7d/src/core/SkPackBits.cpp
[modify] http://crrev.com/699b852e48da8f71c19fcaa13bb109efd68e5c7d/src/effects/SkTableColorFilter.cpp
[modify] http://crrev.com/699b852e48da8f71c19fcaa13bb109efd68e5c7d/tests/PackBitsTest.cpp


### js...@chromium.org (2015-06-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-06-05)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-06-13)

ClusterFuzz has detected this issue as fixed in range 332881:334220.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4810294212165632

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Stack-buffer-overflow WRITE 1
Crash Address: 0xf46b1190
Crash State:
  SkPackBits::Unpack8
  SkTable_ColorFilter::CreateProc
  SkValidatingReadBuffer::readFlattenable
  
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=332881:334220

Minimized Testcase (0.21 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95QUdnyznVEJx30PR0FdjSsZJm5fVlP920hid6jx99QkdEndpq_tAOtRvxP7zTm3P0yl5CfvHqzVvWKGHVIkU36DW4ZKWdhsRmE268bbyVidY5v6FOBlJfX7Ack0XwlcDrTtnf1NKdH6028xri5OXGPUJfmCw

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### ti...@google.com (2015-07-08)

Merge-Requested to M44 (branch 2403).

### pe...@google.com (2015-07-08)

[Automated comment] Less than 2 weeks to go before stable on M44, manual review required.

### pe...@google.com (2015-07-09)

Merge approved for M44 (2403) skia branch.  Please get the merge done before end of business PST Monday.

### pe...@chromium.org (2015-07-13)

FYI: You only have ~4 hours to get this merge finished, or it'll miss stable.

### pe...@chromium.org (2015-07-13)

And now you have 1 hour.

### js...@chromium.org (2015-07-14)

Sorry, I was on leave and didn't realize this was assigned to me. @hcm, can you assign this to someone to merge, since I have no idea how skia branch merges work?

### hc...@chromium.org (2015-07-14)

Though we missed the main stable cut, working on a merge in https://codereview.chromium.org/1235163002/

### bu...@chromium.org (2015-07-14)

The following revision refers to this bug:
  https://skia.googlesource.com/skia.git/+/ee68678f0051e71efeb6affc3f4a071b7ac1c1bd

commit ee68678f0051e71efeb6affc3f4a071b7ac1c1bd
Author: hcm <hcm@skia.org>
Date: Tue Jul 14 16:32:48 2015

Remove unused PackBits methods and fix length checks

Also a bit of general cleanup.

BUG=chromium:486944

Review URL: https://codereview.chromium.org/1152163004
NOTREECHECKS=true
NOTRY=true
NOPRESUBMIT=true

Review URL: https://codereview.chromium.org/1235163002

[modify] http://crrev.com/ee68678f0051e71efeb6affc3f4a071b7ac1c1bd/include/core/SkPackBits.h
[modify] http://crrev.com/ee68678f0051e71efeb6affc3f4a071b7ac1c1bd/src/core/SkPackBits.cpp
[modify] http://crrev.com/ee68678f0051e71efeb6affc3f4a071b7ac1c1bd/src/effects/SkTableColorFilter.cpp
[modify] http://crrev.com/ee68678f0051e71efeb6affc3f4a071b7ac1c1bd/tests/PackBitsTest.cpp


### pe...@chromium.org (2015-07-18)

[Empty comment from Monorail migration]

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-11)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2016-06-28)

cloudfuzzer: +$5,000 to your tab.

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

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

This issue was migrated from crbug.com/chromium/486944?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082057)*
