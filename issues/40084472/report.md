# Security: Universal XSS via same document navigations

| Field | Value |
|-------|-------|
| **Issue ID** | [40084472](https://issues.chromium.org/issues/40084472) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>HTML>Frame |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2016-06-06 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

FrameLoader::loadInSameDocument is vulnerable to a problem similar to the one described in <https://crbug.com/chromium/613266>:

---

## void FrameLoader::loadInSameDocument(const KURL& url, (...)) { (...) // If we have a provisional request for a different document, a fragment scroll should cancel it. detachDocumentLoader(m\_provisionalDocumentLoader); if (!m\_frame->host()) return; (...) }

Calling FrameLoader::startLoad in the middle of detaching |m\_provisionalDocumentLoader| will cause the new provisional loader to be cleared prematurely. In this case, |m\_provisionalDocumentLoader| isn't set up afterwards, so the attacker has to take care of it explicitly after the hash navigation in order to avoid crashes.

**VERSION**  

Chrome 51.0.2704.79 (Stable)  

Chrome 52.0.2743.24 (Beta)  

Chrome 53.0.2756.0 (Dev)  

Chromium 53.0.2760.0 (Release build compiled today)

## Attachments

- [exploit.html](attachments/exploit.html) (text/plain, 828 B)

## Timeline

### fe...@chromium.org (2016-06-06)

Thanks for the report.

japhet@, could you please look at this one too? It seems like 613266 didn't fully solve this problem.

[Monorail components: Blink>HTML>Frame]

### sh...@chromium.org (2016-06-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/be655fd4fb9ab3291a855a939496111674037a2f

commit be655fd4fb9ab3291a855a939496111674037a2f
Author: japhet <japhet@chromium.org>
Date: Sat Jun 18 01:02:39 2016

Always use FrameNavigationDisabler during DocumentLoader detach.

BUG=617495

Review-Url: https://codereview.chromium.org/2079473002
Cr-Commit-Position: refs/heads/master@{#400558}

[modify] https://crrev.com/be655fd4fb9ab3291a855a939496111674037a2f/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### sh...@chromium.org (2016-06-20)

japhet: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ja...@chromium.org (2016-06-20)

I'm inclined to let this bake a couple of days before merging, if there are no objections.

### ja...@chromium.org (2016-06-24)

I don't see any evidence of regressions from the bugfix. Should this be merged to M51 and/or M52?

### cl...@chromium.org (2016-06-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### sh...@chromium.org (2016-06-25)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-27)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### ti...@google.com (2016-06-27)

[Automated comment] There appears to be on-going work (i.e. bugroid changes), needs manual review.

### go...@chromium.org (2016-06-27)

Before we approve merge to M52, Could you please confirm whether this change is baked/verified in Canary and safe to merge?

Also is this change applicable to all OS or any specific OS?

### ja...@chromium.org (2016-06-28)

All OSes are affected.

This fix has been on canaries for a little over a week, and I haven't been able to find any crashes or regression reports that appear to be related to this change, so I think this is baked.

### go...@chromium.org (2016-06-28)

Thank you. Approving merge to M52 branch 2743 based on https://crbug.com/chromium/617495#c12. Please merge asap. Thank you.

### bu...@chromium.org (2016-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/019484e056b10a33a91b1342de1cd1d08d18d605

commit 019484e056b10a33a91b1342de1cd1d08d18d605
Author: Nate Chapin <japhet@chromium.org>
Date: Tue Jun 28 22:03:05 2016

Always use FrameNavigationDisabler during DocumentLoader detach.

BUG=617495

Review-Url: https://codereview.chromium.org/2079473002
Cr-Commit-Position: refs/heads/master@{#400558}
(cherry picked from commit be655fd4fb9ab3291a855a939496111674037a2f)

Review URL: https://codereview.chromium.org/2103703004 .

Cr-Commit-Position: refs/branch-heads/2743@{#511}
Cr-Branched-From: 2b3ae3b8090361f8af5a611712fc1a5ab2de53cb-refs/heads/master@{#394939}

[modify] https://crrev.com/019484e056b10a33a91b1342de1cd1d08d18d605/third_party/WebKit/Source/core/loader/FrameLoader.cpp


### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-20)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-25)

And $7,500 for this one!

### aw...@chromium.org (2016-07-25)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-08-31)

[Empty comment from Monorail migration]

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

### ad...@google.com (2021-03-25)

[Empty comment from Monorail migration]

### is...@google.com (2021-03-25)

This issue was migrated from crbug.com/chromium/617495?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40084472)*
