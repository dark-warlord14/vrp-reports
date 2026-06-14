# Use-of-uninitialized-value in ebml_read_num

| Field | Value |
|-------|-------|
| **Issue ID** | [40083755](https://issues.chromium.org/issues/40083755) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Media>FFmpeg |
| **Platforms** | Linux |
| **Reporter** | cl...@chromium.org |
| **Assignee** | hu...@chromium.org |
| **Created** | 2016-02-24 |
| **Bounty** | $1,500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6299764108296192

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  ebml_read_num
  ebml_parse
  matroska_parse_seekhead_entry
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=376801:376900

Minimized Testcase (18.01 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95EzbR7Co9GCjTik35eTo7CxE9TH3y-8o0d0guBUMJ_xoPC8t-T9_6QkgrdbK47bAqWEl3djwhvmy5p_roHo8rocuwtWBbGgugeVvCXElM0QU9eavO7de3oz25I1FBnM5s6r_cw3KQqnei0oixiT4j3m6gf3fAVAV1FoHWytG3Vs_RqPlQ

Filer: aarya

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

## Timeline

### oc...@chromium.org (2016-02-24)

Dale, could you please take a look, or help find an owner?

[Monorail components: Internals>Media>FFmpeg]

### da...@chromium.org (2016-02-24)

xhwang@ is working on the ffmpeg roll for m50.

### xh...@chromium.org (2016-02-26)

hubbe: This seems to be caused by your MultiBuffer CL. Could you please take a look?

Author: hubbe
Component: chromium
Changelist: https://chromium.googlesource.com/chromium/src//+/dd6151100c52e52929d5e09f5f7fb15653c67f14
Time: Mon Nov 30 22:22:13 2015
The CL last changed line 325 of file resource_multibuffer_data_provider.cc, which is stack frame 2.

### cl...@chromium.org (2016-02-27)

ClusterFuzz has detected this issue as fixed in range 377688:377898.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6299764108296192

Fuzzer: attekett_surku_fuzzer
Job Type: linux_msan_chrome
Platform Id: linux

Crash Type: Use-of-uninitialized-value
Crash Address: 
Crash State:
  ebml_read_num
  ebml_parse
  matroska_parse_seekhead_entry
  
Regressed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=376801:376900
Fixed: https://cluster-fuzz.appspot.com/revisions?job=linux_msan_chrome&range=377688:377898

Minimized Testcase (18.01 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95EzbR7Co9GCjTik35eTo7CxE9TH3y-8o0d0guBUMJ_xoPC8t-T9_6QkgrdbK47bAqWEl3djwhvmy5p_roHo8rocuwtWBbGgugeVvCXElM0QU9eavO7de3oz25I1FBnM5s6r_cw3KQqnei0oixiT4j3m6gf3fAVAV1FoHWytG3Vs_RqPlQ

See https://dev.chromium.org/Home/chromium-security/bugs/reproducing-clusterfuzz-bugs for more information.

If you suspect that the result above is incorrect, try re-doing that job on the test case report page.

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### hu...@chromium.org (2016-03-07)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2016-03-24)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-25)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### go...@chromium.org (2016-03-25)

Please merge your change to M50 branch (2661) by EOD Monday(03/28), so we can take it for next week beta cut. Thank you.

### go...@chromium.org (2016-03-28)

Please merge your change to M50 branch 2661 ASAP as we're getting close to M50 beta candidate cut for this week. Thank you.

### hu...@chromium.org (2016-03-28)

I think this was fixed before the m50 branch cut, so no need to merge anything AFAIK. Unless I'm mistaken, this was fixed in: https://codereview.chromium.org/1729223003


### go...@chromium.org (2016-03-28)

Yeah, seems like NO M50 merge is needed here.

CL: https://codereview.chromium.org/1729223003
CL Committed: https://crrev.com/fdfdd80259808aa3329001efd9ca1fab00091ffb
Cr-Commit-Position: refs/heads/master@{#377709}
  
M50 Branched Chromium at revision: 378081. Removing "Merge-Approved-50" label. Please correct me if I'm missing anything here. Thank you.



### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-13)

Thanks again for the fuzzer contribution, Atte! This one qualified for a $1500 reward.

### sh...@chromium.org (2016-04-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-22)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-24)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-06-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

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

### sh...@chromium.org (2018-07-28)

[Empty comment from Monorail migration]

### is...@google.com (2018-07-28)

This issue was migrated from crbug.com/chromium/589512?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083755)*
