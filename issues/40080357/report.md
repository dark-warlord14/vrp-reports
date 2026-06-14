# Heap-buffer-overflow in SkOpSegment::findNextOp

| Field | Value |
|-------|-------|
| **Issue ID** | [40080357](https://issues.chromium.org/issues/40080357) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SVG, Internals>Skia |
| **Reporter** | cl...@chromium.org |
| **Assignee** | ca...@google.com |
| **Created** | 2014-09-03 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5786390890545152

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x619000052838
Crash State:
  SkOpSegment::findNextOp
  Op
  blink::RenderSVGResourceClipper::tryPathOnlyClipping
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842

Minimized Testcase (0.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95b5oq0ImT6ZDJ8Vj7w-RdFX6c484ceM_yIseUqI6P9yXkCp2o0DRZuuQqcU6yojeqXkiK9s6Y4WJA4PRfquY__0gZ-ttuDbNgGHPq8p41e6vQNJ6684AYCL51U2WdntQVyI-ifQKjGiFxk0KrC2GwTkIyuDA

Filer: inferno

## Timeline

### in...@chromium.org (2014-09-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-03)

[Empty comment from Monorail migration]

### pa...@chromium.org (2014-09-05)

Say, reed, could you help find someone on your team to look into this? Might be SVG tickling a Skia bug?

### cl...@chromium.org (2014-09-06)

[Empty comment from Monorail migration]

### [Deleted User] (2014-09-08)

[Empty comment from Monorail migration]

### ca...@google.com (2014-09-08)

fixed in skia with https://codereview.chromium.org/556433002/

### cl...@chromium.org (2014-09-10)

ClusterFuzz has detected this issue as fixed in range 293942:293978.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=5786390890545152

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_mp

Crash Type: Heap-buffer-overflow READ 8
Crash Address: 0x619000052838
Crash State:
  SkOpSegment::findNextOp
  Op
  blink::RenderSVGResourceClipper::tryPathOnlyClipping
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=287661:287842
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_asan_chrome_mp&range=293942:293978

Minimized Testcase (0.46 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95b5oq0ImT6ZDJ8Vj7w-RdFX6c484ceM_yIseUqI6P9yXkCp2o0DRZuuQqcU6yojeqXkiK9s6Y4WJA4PRfquY__0gZ-ttuDbNgGHPq8p41e6vQNJ6684AYCL51U2WdntQVyI-ifQKjGiFxk0KrC2GwTkIyuDA

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### ca...@google.com (2014-09-10)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-09-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ca...@google.com (2014-09-10)

[Empty comment from Monorail migration]

### ca...@google.com (2014-09-10)

merged into skia/chrome/m38_2125

### hc...@chromium.org (2014-09-10)

Matt, Cary has integrated this change in our Skia M38 branch...Chrome M38 points to our branch ToT, so it should get picked up in subsequent builds, unless you need it promoted somewhere specifically.

### ti...@chromium.org (2014-09-24)

Cary - to be clear, is a merge required here for this to land in M38? Based on c#12, seems like no merge required.

If no merge required, please change the Merge-Approved label to Merge-Merged. Otherwise, pleas merge the fix to M38 / branch 2125.

### hc...@chromium.org (2014-09-25)

It's in now.

### ti...@chromium.org (2014-10-07)

$1500 for this report ($1000 for the bug, $500 ClusterFuzz bonus). 

Reward panel notes: It's not immediately clear that you could do something nasty and reliable here. If you can and want to spend some time here proving your case, please update the bug and we can consider topping-up the reward amount.

### ti...@google.com (2014-12-08)

[Empty comment from Monorail migration]

### ti...@google.com (2014-12-09)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-12-17)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### is...@google.com (2016-10-02)

This issue was migrated from crbug.com/chromium/410552?no_tracker_redirect=1

[Multiple monorail components: Blink>SVG, Internals>Skia]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080357)*
