# Security: Heap-use-after-free via GCCallback

| Field | Value |
|-------|-------|
| **Issue ID** | [40084094](https://issues.chromium.org/issues/40084094) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **CVE IDs** | CVE-2016-1662 |
| **Reporter** | ro...@robwu.nl |
| **Assignee** | jo...@chromium.org |
| **Created** | 2016-04-14 |
| **Bounty** | $3,000.00 |

## Description

Chrome version: 52.0.2709.0 and earlier

GCCallback in extensions/renderer/gc_callback.cc contains a UAF vulnerability that can be controlled with high precision (=arbitrary JS execution before the first delete, before the second delete, and after the second delete).


Here is how the vulnerability works:
1. Construct a GCCallback::RunCallback in a frame (there are multiple ways to do that, https://cs.chromium.org/BindToGC). 
2. While the JS callback is run, remove the frame (invalidating the JavaScript context in the process).
3. GCCallback::OnContextInvalidated is triggered because of 2.
4. Step 3 deletes |this|.
5. Now the JS function from step 2 returns, and control goes back to step 1.
6. Step 1 deletes |this| again. = double-free.

Combined with https://crbug.com/chromium/603725 or https://crbug.com/chromium/591164, this can be exploited by any web page without user interaction.
Without these bugs, this bug can still be exploited from any extension or app (without user interaction except installing the extension/app).


I've an ASAN trace generated with Chrome 49.0.2623.75 because I didn't build the latest stable (50) with ASAN yet. The vulnerable code is still present on master, so that shouldn't matter.

## Attachments

- [uaf-during-gc-callback50.html](attachments/uaf-during-gc-callback50.html) (text/plain, 10.2 KB)
- [heap-use-after-free-asan.log](attachments/heap-use-after-free-asan.log) (text/plain, 14.7 KB)

## Timeline

### ts...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### ro...@robwu.nl (2016-04-15)

This bug affects all channels.

### bu...@chromium.org (2016-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/34c97b31e61e8329e19188b46a489412a16d2b63

commit 34c97b31e61e8329e19188b46a489412a16d2b63
Author: jochen <jochen@chromium.org>
Date: Fri Apr 15 12:03:12 2016

Don't execute the fallback if we already started running the gc callback

BUG=603732
R=vogelheim@chromium.org

Review URL: https://codereview.chromium.org/1887423002

Cr-Commit-Position: refs/heads/master@{#387578}

[modify] https://crrev.com/34c97b31e61e8329e19188b46a489412a16d2b63/extensions/renderer/gc_callback.cc


### jo...@chromium.org (2016-04-15)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-04-15)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### jo...@chromium.org (2016-04-19)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-19)

Your change meets the bar and is auto-approved for M51 (branch: 2704)

### go...@chromium.org (2016-04-19)

We're VERY close to M51 beta candidate cut. Please merge your change to M51 branch 2704 asap. Thank you.

### bu...@chromium.org (2016-04-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/9865e744d09069f6f6c39e8d351b87ab1dae9ef3

commit 9865e744d09069f6f6c39e8d351b87ab1dae9ef3
Author: Jochen Eisinger <jochen@chromium.org>
Date: Wed Apr 20 06:36:43 2016

Don't execute the fallback if we already started running the gc callback

BUG=603732
R=vogelheim@chromium.org

Review URL: https://codereview.chromium.org/1887423002

Cr-Commit-Position: refs/heads/master@{#387578}
(cherry picked from commit 34c97b31e61e8329e19188b46a489412a16d2b63)

Review URL: https://codereview.chromium.org/1903123002 .

Cr-Commit-Position: refs/branch-heads/2704@{#142}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/9865e744d09069f6f6c39e8d351b87ab1dae9ef3/extensions/renderer/gc_callback.cc


### jo...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-21)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### go...@chromium.org (2016-04-22)

Before we approve merge to M50, Could you please confirm whether this bug is baked/verified in Canary and safe to merge? 

### jo...@chromium.org (2016-04-22)

Yes, it has Canary coverage and is safe

### go...@chromium.org (2016-04-26)

Approving merge to M50 branch 2661, based on https://crbug.com/chromium/603732#c13. Please merge asap. Thank you.

### go...@chromium.org (2016-04-26)

Please merge your change to M50 branch 2661 before @1:00 PM PST tomorrow (Wednesday) so we can take it for this week Stable release.

### bu...@chromium.org (2016-04-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3692cce1b48f5d15b9813988207f8ee1f5c72c91

commit 3692cce1b48f5d15b9813988207f8ee1f5c72c91
Author: Jochen Eisinger <jochen@chromium.org>
Date: Wed Apr 27 06:58:55 2016

Don't execute the fallback if we already started running the gc callback

BUG=603732
R=vogelheim@chromium.org

Review URL: https://codereview.chromium.org/1887423002

Cr-Commit-Position: refs/heads/master@{#387578}
(cherry picked from commit 34c97b31e61e8329e19188b46a489412a16d2b63)

Review URL: https://codereview.chromium.org/1925543002 .

Cr-Commit-Position: refs/branch-heads/2661@{#638}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/3692cce1b48f5d15b9813988207f8ee1f5c72c91/extensions/renderer/gc_callback.cc


### ti...@google.com (2016-04-27)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

Hey Rob - $3,000 for this report. I'll start payment today.

CVE-ID is CVE-2016-1662

Thanks as always!

### ti...@google.com (2016-05-02)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-10)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-22)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/603732?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084094)*
