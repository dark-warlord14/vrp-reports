# Security: Universal XSS using widget updates in ContainerNode::parserRemoveChild

| Field | Value |
|-------|-------|
| **Issue ID** | [40083251](https://issues.chromium.org/issues/40083251) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>DOM |
| **CVE IDs** | CVE-2016-1630 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ko...@chromium.org |
| **Created** | 2015-11-22 |
| **Bounty** | $8,000.00 |

## Description

**VULNERABILITY DETAILS**  

There are 3 methods where ContainerNode::removeBetween is invoked:

1. ContainerNode::removeChild
2. ContainerNode::parserRemoveChild
3. ContainerNode::removeChildren

The calls in #1 and #3 are within the scope of HTMLFrameOwnerElement::UpdateSuspendScope, but #2 is unprotected. Thus, if the parser removes a plugin node with an associated widget (plugins may take a while to load, but it's easy to handle with document.write, where the timing of parser actions can be arbitrarily controlled), updates fired during the detachment can corrupt the DOM tree.

**VERSION**  

Chrome 46.0.2490.86 (Stable)  

Chrome 47.0.2526.69 (Beta)  

Chrome 48.0.2564.10 (Dev)  

Chromium 49.0.2572.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/zip, 267.5 KB)

## Timeline

### ma...@gmail.com (2015-11-22)

Please see https://codereview.chromium.org/1464223002 for a fix proposal. An automated testcase would probably need the facilities mentioned in https://codereview.chromium.org/1444183003/#msg19

### wf...@chromium.org (2015-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-23)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-11-24)

ClusterFuzz is analyzing your testcase. Developers can follow the progress at https://cluster-fuzz.appspot.com/testcase?key=5767072539213824

### wf...@chromium.org (2015-11-24)

Thanks for your report, Marius.

Based on previous bugs in this area I'm assigning to kouhei - can you triage and/or assign to others as appropriate?

### dc...@chromium.org (2015-11-25)

[Empty comment from Monorail migration]

### dc...@chromium.org (2015-11-26)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-12-04)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/05926d6f4e749cd49a16fa04a35e3498eb1b01a0

commit 05926d6f4e749cd49a16fa04a35e3498eb1b01a0
Author: marius.mlynski <marius.mlynski@gmail.com>
Date: Fri Dec 04 06:45:19 2015

Defer widget updates in ContainerNode::parserRemoveChild.

ContainerNode::parserRemoveChild is the only consumer of ContainerNode::removeBetween that doesn't defer widget updates during the call. This could potentially lead to problems with scripts running at an inopportune time.

This patch adds a RAII guard that runs deferred widget updates at the end of parserRemoveChild.

BUG=560011

Review URL: https://codereview.chromium.org/1464223002

Cr-Commit-Position: refs/heads/master@{#363154}

[modify] http://crrev.com/05926d6f4e749cd49a16fa04a35e3498eb1b01a0/third_party/WebKit/Source/core/dom/ContainerNode.cpp


### in...@chromium.org (2015-12-04)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-12-04)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### ti...@google.com (2015-12-10)

Tina - merge request for M48.

### ti...@google.com (2015-12-10)

Congrats your change is auto-approved for M48 (branch: 2564)

### ti...@google.com (2016-01-09)

Bump - this needs to be in M48 and isn't merged.

@kouhei - can you please merge in the fix? It's from an external contributor.

### ti...@google.com (2016-01-11)

@inferno - kouhei is OOO, can you please follow up with the merge here?

### bu...@chromium.org (2016-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ca5ef94e715de68255be76e3d9a9bd4b57ac1ff3

commit ca5ef94e715de68255be76e3d9a9bd4b57ac1ff3
Author: Oliver Chang <ochang@chromium.org>
Date: Mon Jan 11 18:26:54 2016

Defer widget updates in ContainerNode::parserRemoveChild.

ContainerNode::parserRemoveChild is the only consumer of ContainerNode::removeBetween that doesn't defer widget updates during the call. This could potentially lead to problems with scripts running at an inopportune time.

This patch adds a RAII guard that runs deferred widget updates at the end of parserRemoveChild.

TBR=kouhei@chromium.org
BUG=560011

Review URL: https://codereview.chromium.org/1464223002

Cr-Commit-Position: refs/heads/master@{#363154}
(cherry picked from commit 05926d6f4e749cd49a16fa04a35e3498eb1b01a0)

Review URL: https://codereview.chromium.org/1574913003 .

Cr-Commit-Position: refs/branch-heads/2564@{#522}
Cr-Branched-From: 1283eca15bd9f772387f75241576cde7bdec7f54-refs/heads/master@{#359700}

[modify] http://crrev.com/ca5ef94e715de68255be76e3d9a9bd4b57ac1ff3/third_party/WebKit/Source/core/dom/ContainerNode.cpp


### ti...@google.com (2016-01-11)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-01-14)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/ca5ef94e715de68255be76e3d9a9bd4b57ac1ff3

commit ca5ef94e715de68255be76e3d9a9bd4b57ac1ff3
Author: Oliver Chang <ochang@chromium.org>
Date: Mon Jan 11 18:26:54 2016


### ma...@gmail.com (2016-02-26)

Could you please assign a CVE number to this bug and include it in release notes anytime soon? Thanks.

### ti...@google.com (2016-02-29)

Tagging for M-49 release notes

### ti...@google.com (2016-03-02)

Congrats - $8000 for this report ($7500 for the bug, $500 for the patch). I'll follow up with a CVE-ID later today.

### ti...@google.com (2016-03-02)

CVE-2016-1630

### sh...@chromium.org (2016-03-11)

This security bug has been closed for more than 14 weeks. Removing view restrictions.

For more details visit https://sites.google.com/a/chromium.org/dev/issue-tracking/autotriage - Your friendly Sheriffbot

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

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

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/560011?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocking: crbug.com/chromium/561683]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083251)*
