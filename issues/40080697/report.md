# UNKNOWN in media::container_names::DetermineContainer

| Field | Value |
|-------|-------|
| **Issue ID** | [40080697](https://issues.chromium.org/issues/40080697) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | jr...@chromium.org |
| **Created** | 2014-10-22 |
| **Bounty** | $500.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4578994040078336

Fuzzer: Cdiehl_peach
Job Type: Linux_asan_chrome_media

Crash Type: UNKNOWN
Crash Address: 0x624f80048910
Crash State:
  media::container_names::DetermineContainer
  media::FFmpegGlue::OpenContext
  void base::internal::ReturnAsParamAdapter<bool>
  

Minimized Testcase (318.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95JL5rQtgSQe580KoMgoaSslSntku4vLNpFQPMBWlvfB7QghmCmWCBYx0uWlsexcEzbaTcaJXuFr4iFrDnQQEzTay_oLb_cOzjsxxomZO2VMn3IM7ggOoJiK3UwwvEXs4GiF4-r-MC6MDN2NXQhBloMYEFbgrAqmOnaMgoLPQ80QFFjrSQ

Filer: inferno

## Timeline

### in...@chromium.org (2014-10-22)

Dale, can you please take a look.

### cl...@chromium.org (2014-10-22)

[Empty comment from Monorail migration]

### in...@chromium.org (2014-10-23)

xhwang@, do you have time to take a look this one ?

### xh...@chromium.org (2014-10-23)

jrummell: This crash happens in DetermineContainer(). Can you take a look?

### xh...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### xh...@chromium.org (2014-10-24)

[Empty comment from Monorail migration]

### bu...@chromium.org (2014-10-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b2006ac87cec58363090e7d5e10d5d9e3bbda9f9

commit b2006ac87cec58363090e7d5e10d5d9e3bbda9f9
Author: jrummell <jrummell@chromium.org>
Date: Sat Oct 25 00:36:28 2014

Add extra checks to avoid integer overflow.

BUG=425980
TEST=no crash with ASAN

Review URL: https://codereview.chromium.org/659743004

Cr-Commit-Position: refs/heads/master@{#301249}

[modify] https://chromium.googlesource.com/chromium/src.git/+/b2006ac87cec58363090e7d5e10d5d9e3bbda9f9/media/base/container_names.cc


### in...@chromium.org (2014-10-25)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-10-25)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### cl...@chromium.org (2014-10-30)

ClusterFuzz has detected this issue as fixed in latest custom build.

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=4578994040078336

Fuzzer: Cdiehl_peach
Job Type: Linux_asan_chrome_media

Crash Type: UNKNOWN
Crash Address: 0x624f80048910
Crash State:
  media::container_names::DetermineContainer
  media::FFmpegGlue::OpenContext
  void base::internal::ReturnAsParamAdapter<bool>
  

Minimized Testcase (318.09 Kb): https://cluster-fuzz.appspot.com/download/AMIfv95JL5rQtgSQe580KoMgoaSslSntku4vLNpFQPMBWlvfB7QghmCmWCBYx0uWlsexcEzbaTcaJXuFr4iFrDnQQEzTay_oLb_cOzjsxxomZO2VMn3IM7ggOoJiK3UwwvEXs4GiF4-r-MC6MDN2NXQhBloMYEFbgrAqmOnaMgoLPQ80QFFjrSQ

If you suspect that the result above is incorrect, try re-doing that job on the testcase report page.


### in...@chromium.org (2014-10-30)

Please merge to M39 (2171 branch) soon.

### in...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### am...@chromium.org (2014-10-30)

merge approved for m39 branch 2171.

### bu...@chromium.org (2014-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/047c3fcf527f2c6262d8ad135631dc5149ec6e60

commit 047c3fcf527f2c6262d8ad135631dc5149ec6e60
Author: John Rummell <jrummell@chromium.org>
Date: Thu Oct 30 23:17:15 2014

Merge to M39: Add extra checks to avoid integer overflow.

BUG=425980
TEST=no crash with ASAN

Review URL: https://codereview.chromium.org/659743004

Cr-Commit-Position: refs/heads/master@{#301249}
(cherry picked from commit b2006ac87cec58363090e7d5e10d5d9e3bbda9f9)

R=xhwang@chromium.org

Review URL: https://codereview.chromium.org/695673002

Cr-Commit-Position: refs/branch-heads/2171@{#312}
Cr-Branched-From: 267aeeb8d85c8503a7fd12bd14654b8ea78d3974-refs/heads/master@{#297060}

[modify] https://chromium.googlesource.com/chromium/src.git/+/047c3fcf527f2c6262d8ad135631dc5149ec6e60/media/base/container_names.cc


### in...@chromium.org (2014-11-05)

[Empty comment from Monorail migration]

### mb...@chromium.org (2014-11-17)

Thanks for the fuzzer contribution! This one qualified for a $500 reward.

### ti...@google.com (2014-12-09)

Payment in process.

### ti...@google.com (2014-12-22)

Processing via our e-payment system can take up to six weeks, but the reward should be on its way to you. Thanks again for your help!

### cl...@chromium.org (2015-02-02)

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

This issue was migrated from crbug.com/chromium/425980?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/426560]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080697)*
