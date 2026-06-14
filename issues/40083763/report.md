# Security: Universal XSS using an intercepted native function

| Field | Value |
|-------|-------|
| **Issue ID** | [40083763](https://issues.chromium.org/issues/40083763) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **CVE IDs** | CVE-2016-1672 |
| **Reporter** | ma...@gmail.com |
| **Assignee** | rd...@chromium.org |
| **Created** | 2016-02-26 |
| **Bounty** | $7,500.00 |

## Description

**VULNERABILITY DETAILS**  

The fix for <https://crbug.com/chromium/546677> is insufficient to protect against overriding internal extensions code -- it is still possible to take over the built-in extension system with a combination of getters and setters. This allows web content to gain access to native functions that may be misused, for example |user\_gestures.RunWithUserGesture| can be leveraged to create new pages at an arbitrary javascript execution point, effectively bypassing ScopedPageLoadDeferrer.

**VERSION**  

Chrome 48.0.2564.116 (Stable)  

Chrome 49.0.2623.64 (Beta)  

Chrome 50.0.2657.0 (Dev)  

Chromium 50.0.2660.0 + Pepper Flash (Release build compiled today)

## Attachments

- [exploit.zip](attachments/exploit.zip) (application/octet-stream, 3.9 KB)

## Timeline

### oc...@chromium.org (2016-02-26)

Thanks for another great report.

### oc...@chromium.org (2016-02-26)

[Empty comment from Monorail migration]

[Monorail components: Platform>Extensions]

### cl...@chromium.org (2016-02-29)

[Empty comment from Monorail migration]

### rd...@chromium.org (2016-03-01)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-03-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/75b803b1c81ed9fa5513cbff550232b4fb915e7b

commit 75b803b1c81ed9fa5513cbff550232b4fb915e7b
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Wed Mar 02 00:13:47 2016

[Extensions] Harden against bindings interception

There's more we can do but this is a start.

BUG=590275
BUG=590118

Review URL: https://codereview.chromium.org/1748943002

Cr-Commit-Position: refs/heads/master@{#378621}

[modify] https://crrev.com/75b803b1c81ed9fa5513cbff550232b4fb915e7b/chrome/browser/extensions/extension_bindings_apitest.cc
[add] https://crrev.com/75b803b1c81ed9fa5513cbff550232b4fb915e7b/chrome/test/data/extensions/api_test/bindings/function_interceptions.html
[modify] https://crrev.com/75b803b1c81ed9fa5513cbff550232b4fb915e7b/extensions/renderer/module_system.cc
[modify] https://crrev.com/75b803b1c81ed9fa5513cbff550232b4fb915e7b/extensions/renderer/v8_helpers.h


### bu...@chromium.org (2016-03-02)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/75b803b1c81ed9fa5513cbff550232b4fb915e7b

commit 75b803b1c81ed9fa5513cbff550232b4fb915e7b
Author: rdevlin.cronin <rdevlin.cronin@chromium.org>
Date: Wed Mar 02 00:13:47 2016


### cl...@chromium.org (2016-03-03)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-03-10)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### rd...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-10)

Your change meets the bar and is auto-approved for M50 (branch: 2661)

### bu...@chromium.org (2016-03-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8a4fb2b8eea970c5a69ca00bf562c7803806af03

commit 8a4fb2b8eea970c5a69ca00bf562c7803806af03
Author: Devlin Cronin <rdevlin.cronin@chromium.org>
Date: Thu Mar 10 22:52:37 2016

[Extensions] Harden against bindings interception

There's more we can do but this is a start.

BUG=590275
BUG=590118

Review URL: https://codereview.chromium.org/1748943002

Cr-Commit-Position: refs/heads/master@{#378621}
(cherry picked from commit 75b803b1c81ed9fa5513cbff550232b4fb915e7b)

Review URL: https://codereview.chromium.org/1787433002 .

Cr-Commit-Position: refs/branch-heads/2661@{#186}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/8a4fb2b8eea970c5a69ca00bf562c7803806af03/chrome/browser/extensions/extension_bindings_apitest.cc
[add] https://crrev.com/8a4fb2b8eea970c5a69ca00bf562c7803806af03/chrome/test/data/extensions/api_test/bindings/function_interceptions.html
[modify] https://crrev.com/8a4fb2b8eea970c5a69ca00bf562c7803806af03/extensions/renderer/module_system.cc
[modify] https://crrev.com/8a4fb2b8eea970c5a69ca00bf562c7803806af03/extensions/renderer/v8_helpers.h


### cl...@chromium.org (2016-03-11)

[Empty comment from Monorail migration]

### ti...@google.com (2016-03-23)

This missed the Rel-2-M49 but merging in case there is an additional M49

### ti...@google.com (2016-03-23)

[Automated comment] Request affecting a post-stable build (M49), manual review required.

### ma...@gmail.com (2016-03-26)

Please see https://crbug.com/chromium/598165.

### am...@google.com (2016-03-28)

[Empty comment from Monorail migration]

### ss...@google.com (2016-03-29)

Merge approved for M49 (branch 2623)

### go...@chromium.org (2016-04-05)

We may have M49 Stable refresh release during this week. Please merge you change to M49 branch 2623 ASAP. Thank you.

### rd...@chromium.org (2016-04-05)

@18 - Per #15, the fix for this was incomplete.  Updating labels.

### ss...@google.com (2016-04-05)

Ok removing the merge approval in that case, based on c#19. Please re-request merge if and when we have a complete fix.

### cl...@chromium.org (2016-04-06)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges.

- Your friendly ClusterFuzz

### ti...@google.com (2016-05-23)

Related fix in https://crbug.com/chromium/598165 is prior to base branch of M-51. Updating labels and removing old labels based on #19 and #20.

### ti...@google.com (2016-05-25)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-25)

Not sure what happened to the text in #23, but congrats! $7,500 for this report. 

CVE-ID is CVE-2016-1672.

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### ti...@google.com (2016-06-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-07-13)

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

### no...@google.com (2020-12-12)

[Empty comment from Monorail migration]

### is...@google.com (2020-12-12)

This issue was migrated from crbug.com/chromium/590118?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083763)*
