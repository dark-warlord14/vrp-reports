# Security: GC freeing reachable objects in JSON parser

| Field | Value |
|-------|-------|
| **Issue ID** | [40056056](https://issues.chromium.org/issues/40056056) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **CVE IDs** | CVE-2021-30541 |
| **Reporter** | ri...@cognitivecredit.com |
| **Assignee** | vi...@chromium.org |
| **Created** | 2021-05-31 |
| **Bounty** | $5,000.00 |

## Description

This V8 bug was apparently reported by Node:
https://bugs.chromium.org/p/v8/issues/detail?id=11837

====
The repro is simple: d8 --gc-global poc.js

let content = read("very-large-json-with-numbers.json")
JSON.parse(content)
====

Filing a tracking bug so that it goes through all our reward/release note/CVE processes.

As a renderer UaF this would be High severity.

## Timeline

### [Deleted User] (2021-05-31)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and Security_Impact labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues Impact guidelines: https://chromium.googlesource.com/chromium/src/+/master/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@chromium.org (2021-05-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-01)

victorgomes@ reports that this does not affect shipping Chrome, but only V8. (That's right, Victor, yes?) So setting to Security_Impact-None.


### [Deleted User] (2021-06-01)

[Empty comment from Monorail migration]

### ad...@google.com (2021-06-01)

If it's true that this doesn't affect users of stable Chrome, this would normally not attract a CVE or a mention in the Chrome release notes, but I understand from Victor that this does affect Node and that it would therefore be helpful to have a CVE allocated.

I've therefore allocated CVE-2021-30541. As this is slightly outside our normal processes, it may be a number of weeks before we submit the CVE description. +amyressler who will have to do some hoop-jumping. Sorry Amy!

(If this turns out to affect shipping versions of Chrome after all, then all the process is much more automatic.)

### vi...@chromium.org (2021-06-07)

Regarding https://crbug.com/chromium/1214842#c3: the bug does affect Chrome (as early as M83).

Although we don't have a reliable repro, parsing a sufficiently large JSON string in Chrome could trigger a global GC at the precise location in the parser where reachable objects would be freed. I guess it would be very hard for an attacker to predict when this happens, but that's possible. :/

The flag passed to d8 `--gc-global` just ensures that we run as many global GC as possible to reliably repro the issue.

### vi...@chromium.org (2021-06-07)

Adding Matteo Collina who helped to debug this on the Node side.

### vi...@chromium.org (2021-06-17)

Not sure what the next steps are here...

### ts...@chromium.org (2021-06-19)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript]

### ad...@google.com (2021-06-21)

Per https://crbug.com/chromium/1214842#c6 this impacts stable. Adjusting suitably. There are fixes on https://bugs.chromium.org/p/v8/issues/detail?id=11837 so marking this as fixed, and Sheriffbot should apply merge labels tomorrow morning.

### [Deleted User] (2021-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-22)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2021-06-22)

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M91. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M92. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-06-22)

This bug requires manual review: M92's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), benmason@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@chromium.org (2021-06-23)

Regarding https://crbug.com/chromium/1214842#c15:
1. Yes
2. https://chromium.googlesource.com/v8/v8.git/+/81181a8ad80ac978a6a8732d05f615c645df95d2
3. Yes
4. It affects from M83, but I think it is okay to merge only in M91 and M92.
5. Security fix.
6. No
7. N/A
8. No

### sr...@google.com (2021-06-23)

adetaylor@ amyresller@ please chime in and approve if you think its good to take into M92 , long standing bug 

### am...@chromium.org (2021-06-23)

Seems good to get this in m92; approved for merge to M92- please merge to branch 4515 asap! Thanks!! 

### go...@chromium.org (2021-06-24)

Please merge your change to M92 branch 4515 ASAP, Thank you.

### vi...@chromium.org (2021-06-24)

https://chromium-review.googlesource.com/c/v8/v8/+/2982602

### am...@chromium.org (2021-06-24)

Thanks, Victor. Sorry about the branch comment. One day I'll get used to V8 branching being different! 


### vi...@chromium.org (2021-06-24)

No worries, I actually don't know what happened. It's being trying to merge for hours now. Not sure if that's normal.

### vi...@chromium.org (2021-06-25)

Merged now: https://chromium-review.googlesource.com/c/v8/v8/+/2988414
I've forgot the bug number there.

### [Deleted User] (2021-06-28)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vi...@chromium.org (2021-06-28)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-06-28)

At this time there isn't another security refreshed planned for M91. Merge approved to M91 to prepare for any potential unplanned security refresh scenarios before M92. Please merge at your convenience. Thanks! 

### gi...@appspot.gserviceaccount.com (2021-06-29)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e76178b896f2f51252c259123e3ec5eb9e81b753

commit e76178b896f2f51252c259123e3ec5eb9e81b753
Author: Victor Gomes <victorgomes@chromium.org>
Date: Mon May 31 11:16:54 2021

Merged: [JSON] Fix GC issue in BuildJsonObject

We must ensure that the sweeper is not running or has already swept
mutable_double_buffer. Otherwise the GC can add it to the free list.

Change-Id: If0fc7617acdb6690f0567215b78f8728e1643ec0
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Bug: v8:11837, chromium:1214842
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2993033
Reviewed-by: Michael Lippautz <mlippautz@chromium.org>
Reviewed-by: Toon Verwaest <verwaest@chromium.org>
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Commit-Position: refs/branch-heads/9.1@{#75}
Cr-Branched-From: 0e4ac64a8cf298b14034a22f9fe7b085d2cb238d-refs/heads/9.1.269@{#1}
Cr-Branched-From: f565e72d5ba88daae35a59d0f978643e2343e912-refs/heads/master@{#73847}

[modify] https://crrev.com/e76178b896f2f51252c259123e3ec5eb9e81b753/src/heap/heap.cc
[modify] https://crrev.com/e76178b896f2f51252c259123e3ec5eb9e81b753/src/heap/heap.h
[modify] https://crrev.com/e76178b896f2f51252c259123e3ec5eb9e81b753/src/json/json-parser.cc


### vi...@chromium.org (2021-06-29)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-02)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-07-02)

Congratulations! The VRP Panel has decided to award you $5000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Please let me know how you would like to be credited in our release notes for this issue, such as the name or handle you would like used. Thank you for this report! 

### ri...@cognitivecredit.com (2021-07-02)

That sounds very nice, thank you. You can just use my regular full name Richard Wheeldon - if you need an e-mail, use richard.wheeldon@cognitivecredit.com.


### am...@google.com (2021-07-02)

[Empty comment from Monorail migration]

### ad...@google.com (2021-07-14)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-02)

[Empty comment from Monorail migration]

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### gi...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-08-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/19bc8e73914d5b95fad302405f108d1c7ed78edd

commit 19bc8e73914d5b95fad302405f108d1c7ed78edd
Author: Victor Gomes <victorgomes@chromium.org>
Date: Mon May 31 11:16:54 2021

[M90-LTS][JSON] Fix GC issue in BuildJsonObject

We must ensure that the sweeper is not running or has already swept
mutable_double_buffer. Otherwise the GC can add it to the free list.

(cherry picked from commit 81181a8ad80ac978a6a8732d05f615c645df95d2)

Bug: v8:11837
Bug: chromium:1214842
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: Ifd9cf15f1c94f664fd6489c70bb38b59730cdd78
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/2928181
Commit-Queue: Victor Gomes <victorgomes@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#74859}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3067222
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Reviewed-by: Jana Grill <janagrill@google.com>
Cr-Commit-Position: refs/branch-heads/9.0@{#68}
Cr-Branched-From: bd0108b4c88e0d6f2350cb79b5f363fbd02f3eb7-refs/heads/9.0.257@{#1}
Cr-Branched-From: 349bcc6a075411f1a7ce2d866c3dfeefc2efa39d-refs/heads/master@{#73001}

[modify] https://crrev.com/19bc8e73914d5b95fad302405f108d1c7ed78edd/src/heap/heap.cc
[modify] https://crrev.com/19bc8e73914d5b95fad302405f108d1c7ed78edd/src/heap/heap.h
[modify] https://crrev.com/19bc8e73914d5b95fad302405f108d1c7ed78edd/src/json/json-parser.cc


### rz...@google.com (2021-08-05)

[Empty comment from Monorail migration]

### [Deleted User] (2021-10-05)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1214842?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/v8/11837]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40056056)*
