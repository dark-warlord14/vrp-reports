# Heap-buffer-overflow in SkData::NewUninitialized

| Field | Value |
|-------|-------|
| **Issue ID** | [40082061](https://issues.chromium.org/issues/40082061) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Internals>Skia |
| **Reporter** | cl...@gmail.com |
| **Assignee** | re...@google.com |
| **Created** | 2015-05-11 |
| **Bounty** | $5,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5870588761997312

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xf4202bd4
Crash State:
  SkData::NewUninitialized
  SkPictureData::parseBufferTag
  SkPictureData::CreateFromBuffer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=321145:321361

Minimized Testcase (0.73 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Lz9bxcfKO0Gam2c4wWu3zJrv8qpV0gO1_BY08PLkbkQl7R1oQJR_nb5gzfNFnarCrCzbXwOWjgxKg6Rmlg00TpwL6q8_rctAmz9gOKmyaPhJa13HX7YcTti9S_qOxHsClLFgas_gHNwhqOWwq-nAZW1JWqg

Filer: mbarbella

## Timeline

### mb...@chromium.org (2015-05-11)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2015-05-14)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-05-18)

[Empty comment from Monorail migration]

### md...@chromium.org (2015-05-19)

This is an integer overflow at https://code.google.com/p/chromium/codesearch#chromium/src/third_party/skia/src/core/SkData.cpp&l=66

    char* storage = (char*)sk_malloc_throw(sizeof(SkData) + length);

the length value here is large enough to cause sizeof(SkData) + length to wrap around to 7, so the "new (storage) SkData(length)" on the next line fails.

### re...@google.com (2015-05-20)

https://codereview.chromium.org/1148873004

### re...@google.com (2015-05-20)

[Empty comment from Monorail migration]

### in...@chromium.org (2015-05-20)

https://skia.googlesource.com/skia/+/e12fcd5fff872dc8757d3dde56338ee75b6a9fb2

### am...@chromium.org (2015-05-20)

Is there a merge required here?

### cl...@chromium.org (2015-05-21)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2015-05-21)

ClusterFuzz has detected this issue as fixed in range 330758:330903.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5870588761997312

Uploader: mbarbella@google.com
Job Type: Linux_asan_filter_fuzz_stub_32bit

Crash Type: Heap-buffer-overflow WRITE 4
Crash Address: 0xf4202bd4
Crash State:
  SkData::NewUninitialized
  SkPictureData::parseBufferTag
  SkPictureData::CreateFromBuffer
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=321145:321361
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_filter_fuzz_stub_32bit&range=330758:330903

Minimized Testcase (0.73 Kb): https://cluster-fuzz.appspot.com/download/AMIfv96Lz9bxcfKO0Gam2c4wWu3zJrv8qpV0gO1_BY08PLkbkQl7R1oQJR_nb5gzfNFnarCrCzbXwOWjgxKg6Rmlg00TpwL6q8_rctAmz9gOKmyaPhJa13HX7YcTti9S_qOxHsClLFgas_gHNwhqOWwq-nAZW1JWqg

If you suspect that the result above is incorrect,try re-doing that job on the test case report page.

### pe...@chromium.org (2015-06-30)

Someone needs to take ownership and request merges appropriately.  This is a high-severity security fix, which should be going to M-44 once fix is verified.

Add the Merge-Request-44 label, to start the process of getting this into https://skia.googlesource.com/skia/+log/chrome/m44.

### ti...@google.com (2015-07-08)

@hcm - can you please help shepard this into M44?

Merge-Request to M44 (branch 2403) 

### pe...@google.com (2015-07-08)

[Automated comment] No bugdroid (commit) comments found, couldn't auto-approve, needs manual review.

### hc...@chromium.org (2015-07-08)

It looks like the fix was verified, and it just missed the 44 cut and has had plenty of time to bake.

reed@, if you see no other issues, can you cherry pick your change into the Skia chrome/m44 branch?

### hc...@chromium.org (2015-07-09)

Cherry-picked into Skia M44 branch (https://codereview.chromium.org/1225103003), will be picked up automatically in next Chromium 44 build.

### re...@google.com (2015-07-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-08-27)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-08-31)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-28)

@cloudfuzzer - $5,000 for this report. Buffer overflow write.

### aw...@chromium.org (2016-06-30)

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

This issue was migrated from crbug.com/chromium/486977?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082061)*
