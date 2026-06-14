# Stack-buffer-overflow in _XData32

| Field | Value |
|-------|-------|
| **Issue ID** | [40080736](https://issues.chromium.org/issues/40080736) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Reporter** | cl...@chromium.org |
| **Assignee** | pk...@chromium.org |
| **Created** | 2014-10-30 |
| **Bounty** | $2,000.00 |

## Description

Detailed report: https://cluster-fuzz.appspot.com/testcase?key=6521056239026176

Fuzzer: Attekett_surku_fuzzer
Job Type: Linux_asan_chrome_media

Crash Type: Stack-buffer-overflow READ 8
Crash Address: 0x7f5cc094c2c0
Crash State:
  _XData32
  XChangeProperty
  ui::SelectionOwner::ProcessTarget
  

Unminimized Testcase: https://cluster-fuzz.appspot.com/download/AMIfv95h8mvnWmYAfFiJvJejAdRalefWGFj-oS0ttcixuN3Wvlw1OBScEljClpgim-tXk5yPtNuQolTfcvALtFk636csDIb5qlAKX96_iz8y1U_Gtc-N0gmze900Z4hgiLHLV_8_t6PdjHupfQrufquL5vPZWipwfHObnhlN3IFqsJWkiVIsz2s


Filer: inferno

## Timeline

### in...@chromium.org (2014-10-30)

This is found by both Attekett and Christoph's fuzzer at the same time. Probably reward split.

### cl...@chromium.org (2014-10-30)

[Empty comment from Monorail migration]

### pk...@chromium.org (2014-11-02)

CL is up at https://codereview.chromium.org/697863002/
inferno@, Is there a good way of checking whether a particular CL fixes the reported issue?

### in...@chromium.org (2014-11-02)

Sorry, but this report (see Reproducible:no in report) was a one-time crasher. We just have to go with speculative fix. We will reopen if we see the stack again. With 4000 bots, it is high chance to rehit it quick. 

### pk...@chromium.org (2014-11-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2014-11-03)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### bu...@chromium.org (2014-11-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f09a3116b3c3bff8d4c98dd65d659471a7eeff6f

commit f09a3116b3c3bff8d4c98dd65d659471a7eeff6f
Author: pkotwicz <pkotwicz@chromium.org>
Date: Sun Nov 02 22:24:50 2014

Pass in long to XChangeProperty() instead of an int when using format=32

BUG=428557
TEST=None

Review URL: https://codereview.chromium.org/697863002

Cr-Commit-Position: refs/heads/master@{#302404}

[modify] https://chromium.googlesource.com/chromium/src.git/+/f09a3116b3c3bff8d4c98dd65d659471a7eeff6f/ui/base/x/selection_owner.cc


### in...@chromium.org (2014-12-15)

[Empty comment from Monorail migration]

### ti...@google.com (2015-01-22)

Fuzzer collision! It's $1000 for bug here, plus $500 for each of your fuzzers. As you both found it, we'll split the $1000 and give you $500 each, so that works out to be $1000 to each of you.

Note for future self: $1000 to attekett, $1000 to Christoph.

### cl...@chromium.org (2015-02-09)

Bulk update: removing view restriction from closed bugs.

### ti...@google.com (2015-03-09)

[Empty comment from Monorail migration]

### ti...@google.com (2015-04-15)

Reward payment made to attekett@ - leaving "reward-inprocess" label on for Christoph.

### ti...@google.com (2015-06-25)

Payment to Christoph sent. Removing in-process label.

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

This issue was migrated from crbug.com/chromium/428557?no_tracker_redirect=1

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40080736)*
