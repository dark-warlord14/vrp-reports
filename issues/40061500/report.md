# Security: Promise.any.call leak hole, leading to RCE

| Field | Value |
|-------|-------|
| **Issue ID** | [40061500](https://issues.chromium.org/issues/40061500) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>JavaScript>Runtime |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ki...@gmail.com |
| **Assignee** | sy...@chromium.org |
| **Created** | 2022-10-27 |
| **Bounty** | $15,000.00 |

## Description

**VULNERABILITY DETAILS**  

It seems to be a torque issue in v8, but I don't have a full root cause analysis. However, I have written an exploit in old version chrome and provided the poc.

**VERSION**  

Tested on v8 version 10.9.0(latest version), introduced on v8 version 8.6

**REPRODUCTION CASE**

- poc
  - Download the latest version v8 10.9.0
  - ./d8 poc.js, and will leak hole.
- exploit
  - leak hole is a powerful primitive.  
    
    For example in the wild vulnerability: <https://bugs.chromium.org/p/chromium/issues/detail?id=1315901,It> use the above primitive to exploit the vulnerability.  
    
    I have written the exploit with v8 9.7.106.19 in the same way, and although this exploit is not available in the latest version, it still demonstrates the high exploitability of this vulnerability.
  - Written in v8 9.7.106.19, compiled via `tools/dev/gm.py x64.release`,
  - ./d8 exp.js, the calculator will pop up.

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: tab

**CREDIT INFORMATION**  

Reporter credit: Zhenghang Xiao of Hunan University

## Attachments

- [poc.js](attachments/poc.js) (text/plain, 234 B)
- [exp.js](attachments/exp.js) (text/plain, 4.2 KB)

## Timeline

### [Deleted User] (2022-10-27)

[Empty comment from Monorail migration]

### ya...@google.com (2022-10-27)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

[Monorail components: Blink>JavaScript>Runtime]

### cf...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-10-27)

[Empty comment from Monorail migration]

### sy...@chromium.org (2022-10-27)

Root cause analysis is as follows.

Background
==========
Promise.any(iterable) [1] is a promise combinator that iterates all promises in the iterable arguments, combining them, using the "then" function, into a new promise that resolves if any input promise resolves and rejects if all input promises are rejected.

Bug
===

1. Promise.any handles builtin subclassing by treating its receiver as a constructor to be used to construct the promise to be returned. A user function can be passed with an overridden "then" method that synchronously resolves or rejects.

2. During iteration, the variable remainingElementsCount counts how many input promises there are. Recall the behavior of Promise.any is to reject the combined promise if all input promises are rejected. This variable is closed over by the reject handler: if the count == 0, then the combined promise is rejected [2].

3. remainingElementsCount is initialized to 1 (not 0!) so that if the first input promise that is synchronously rejected during iteration does not incorrectly reject the combined promise. (Since the input is an iterable, the number of input promises is unknown ahead of time.) Each iteration increments remainingElementsCount by 1. At the end of iteration, remainingElementsCount is decremented by 1.

4. When the combined promise is rejected, it is rejected with an AggregateError, which in turn contains an array of values for each input promise rejection. V8's implementation of Promise.any lazily constructs this errors array.

The V8 bug is in (4). The new capacity of errors array is incorrectly computed as the max(remainingElementsCount, index of the input promise + 1). Because remainingElementsCount is 1 higher than the true value during iteration of the input, synchronous rejection creates an errors array that is 1 element bigger. This element is never assigned to and remains the uninitialized TheHole value, which leaks to user script.

Fix up at https://chromium-review.googlesource.com/c/v8/v8/+/3988924

[1] https://tc39.es/ecma262/#sec-promise.any
[2] https://tc39.es/ecma262/#sec-promise.any-reject-element-functions step 10


### gi...@appspot.gserviceaccount.com (2022-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/e08fa94bbcc49f3a5c3aa1371986c6365e5a09fb

commit e08fa94bbcc49f3a5c3aa1371986c6365e5a09fb
Author: Shu-yu Guo <syg@chromium.org>
Date: Thu Oct 27 22:34:28 2022

[Promise.any] Fix errors allocation

Bug: chromium:1379054
Change-Id: Ibfcdd4ddc3c9a26471094074c8e7810d93abc898
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3988924
Commit-Queue: Marja Hölttä <marja@chromium.org>
Auto-Submit: Shu-yu Guo <syg@chromium.org>
Reviewed-by: Marja Hölttä <marja@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83968}

[modify] https://crrev.com/e08fa94bbcc49f3a5c3aa1371986c6365e5a09fb/src/builtins/promise-any.tq


### sa...@chromium.org (2022-10-28)

Another great find! While the exploit uses the "Map.prototype.delete technique" which no longer works on current Chrome [1], we should assume that leaking TheHole can be exploited in other ways as well. Setting the severity accordingly.

[1] https://chromium.googlesource.com/v8/v8/+/66c8de2cdac10cad9e622ecededda411b44ac5b3

### gi...@appspot.gserviceaccount.com (2022-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/6127ada1beda0571edd7b833236231980c709c91

commit 6127ada1beda0571edd7b833236231980c709c91
Author: Matthias Liedtke <mliedtke@chromium.org>
Date: Fri Oct 28 10:03:27 2022

Revert "[Promise.any] Fix errors allocation"

This reverts commit e08fa94bbcc49f3a5c3aa1371986c6365e5a09fb.

Reason for revert: Failing promise-overflow-2 test in CI: https://ci.chromium.org/ui/p/v8/builders/ci/V8%20Linux64%20-%20debug/43509/overview

Original change's description:
> [Promise.any] Fix errors allocation
>
> Bug: chromium:1379054
> Change-Id: Ibfcdd4ddc3c9a26471094074c8e7810d93abc898
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3988924
> Commit-Queue: Marja Hölttä <marja@chromium.org>
> Auto-Submit: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Marja Hölttä <marja@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#83968}

Bug: chromium:1379054
Change-Id: Ia3b90cc50adef5a27727b280b9499a9a902d9d60
No-Presubmit: true
No-Tree-Checks: true
No-Try: true
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3990784
Owners-Override: Matthias Liedtke <mliedtke@chromium.org>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Commit-Queue: Matthias Liedtke <mliedtke@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83974}

[modify] https://crrev.com/6127ada1beda0571edd7b833236231980c709c91/src/builtins/promise-any.tq


### ki...@gmail.com (2022-10-28)

[Comment Deleted]

### ki...@gmail.com (2022-10-28)

[Comment Deleted]

### sy...@chromium.org (2022-10-28)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-10-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/8b35091b2d244c975975e1c78e4cd09cb479b5dc

commit 8b35091b2d244c975975e1c78e4cd09cb479b5dc
Author: Shu-yu Guo <syg@chromium.org>
Date: Fri Oct 28 17:21:27 2022

Reland "[Promise.any] Fix errors allocation"

This is a reland of commit e08fa94bbcc49f3a5c3aa1371986c6365e5a09fb

Changes since revert:

Use max(remainingElements - 1, index + 1) instead of index + 1 as
newCapacity computation to avoid excessive allocations causing the
timeout.

Original change's description:
> [Promise.any] Fix errors allocation
>
> Bug: chromium:1379054
> Change-Id: Ibfcdd4ddc3c9a26471094074c8e7810d93abc898
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3988924
> Commit-Queue: Marja Hölttä <marja@chromium.org>
> Auto-Submit: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Marja Hölttä <marja@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#83968}

Bug: chromium:1379054
Change-Id: Ic788b8d0b42f4e24eaf8b2f2d05b24390fda247b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3990627
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/heads/main@{#83987}

[modify] https://crrev.com/8b35091b2d244c975975e1c78e4cd09cb479b5dc/tools/v8heapconst.py
[modify] https://crrev.com/8b35091b2d244c975975e1c78e4cd09cb479b5dc/src/builtins/promise-any.tq


### sy...@chromium.org (2022-10-28)

saelo@ could you PTAL and set the right labels here to ensure merge requests are triggered?

### [Deleted User] (2022-10-28)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### me...@chromium.org (2022-10-28)

On 107 this hits a DCHECK:
abort: CSA_DCHECK failed: TaggedNotEqual(key, TheHoleConstant()) [../../v8/src/builtins/builtins-collections-gen.cc:1768]

syg, could you please confirm that this means the bug is in M107 (and possibly M106)?

### sy...@chromium.org (2022-10-28)

> syg, could you please confirm that this means the bug is in M107 (and possibly M106)?

I confirm this is in M107 and M106. AFAICT it's existed since e90c5ddb02246554e1ff54ef951fbe50066a4390, which is M85.

### me...@chromium.org (2022-10-29)

I get the same DCHECK on 106, so this is probably FoundIn-106.

### ki...@gmail.com (2022-11-01)

[Comment Deleted]

### me...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### sa...@google.com (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-01)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

This high+ V8 security issue with stable impact requires a lightweight post mortem. Please take some time to answer questions asked in this form [1] to help us improve V8 security. [1] https://docs.google.com/forms/d/e/1FAIpQLSdSMCiEpIFLLFkMbgtulK1sf1B-idQmkFaA4XP2Rz5mN1cqWg/viewform?usp=pp_url&entry.307501673=1379054&entry.364066060=External&entry.763880440=Extended&entry.1678852700=High&entry.763402679=Blink>JavaScript>Runtime&entry.975983575=syg@chromium.org Please ensure to copy the full link, as otherwise some issue meta data might not be populated automatically. 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-02)

This is sufficiently serious that it should be merged to extended stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M106. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M107. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M108. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

Merge review required: M108 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

Merge review required: M107 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), eakpobaro (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-11-02)

Merge review required: M106 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: eakpobaro (Android), harrysouders (iOS), ceb (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sy...@chromium.org (2022-11-03)

The answer for merge is the same for all of 108, 107, and 106, and are below.

1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines

This is a fix for a Severity-High security bug that exists in these versions.

2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/v8/v8/+/3990627

Because it touches v8heapconst.py, it'll need to be manually rebased against each release branch.

3. Have the changes been released and tested on canary?

Yes.

4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No.

5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents

N/A

6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No.

### am...@chromium.org (2022-11-10)

did not have any OS selected, so this issue did not go into the security merge review queue 


### am...@chromium.org (2022-11-10)

Thanks for landing these fixes syg@! 

Unfortunately since this didn't make it in to the merge queue earlier due to the OS labeling issues (see https://crbug.com/chromium/1379054#c32), this missed stable/107 and extended/106 respins, so no further planned releases of 107 or 106. 

Merge approved to 108, please merge to the relevant branch for M108 in the V8 repo at your earliest convenience. Thank you! 

### gi...@appspot.gserviceaccount.com (2022-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/c7914874242157310157e94a4ee4785afa3d4b8e

commit c7914874242157310157e94a4ee4785afa3d4b8e
Author: Shu-yu Guo <syg@chromium.org>
Date: Fri Oct 28 17:21:27 2022

Merged: Reland "[Promise.any] Fix errors allocation"

Bug: chromium:1379054

(cherry picked from commit 8b35091b2d244c975975e1c78e4cd09cb479b5dc)

Change-Id: Iec8f8bb51f4434d6ae86887cf742f2883a9b7bef
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4004804
Reviewed-by: Adam Klein <adamk@chromium.org>
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Commit-Position: refs/branch-heads/10.8@{#34}
Cr-Branched-From: f1bc03fd6b4c201abd9f0fd9d51fb989150f97b9-refs/heads/10.8.168@{#1}
Cr-Branched-From: 237de893e1c0a0628a57d0f5797483d3add7f005-refs/heads/main@{#83672}

[modify] https://crrev.com/c7914874242157310157e94a4ee4785afa3d4b8e/tools/v8heapconst.py
[modify] https://crrev.com/c7914874242157310157e94a4ee4785afa3d4b8e/src/builtins/promise-any.tq


### [Deleted User] (2022-11-11)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2022-11-11)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### gi...@appspot.gserviceaccount.com (2022-11-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7d4b08cd9d891d0dbb2cf37050614768e0e0f880

commit 7d4b08cd9d891d0dbb2cf37050614768e0e0f880
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Fri Nov 11 02:19:27 2022

Roll v8 10.8 from 36ec48cf2113 to 754c768786f3 (2 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/36ec48cf2113..754c768786f3

2022-11-11 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.8.168.18
2022-11-10 syg@chromium.org Merged: Reland "[Promise.any] Fix errors allocation"

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-0
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.8: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m108: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1379054
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: I8f087d74f27b040094ea3071967fb8a337f3f889
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4022626
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5359@{#752}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/7d4b08cd9d891d0dbb2cf37050614768e0e0f880/DEPS


### am...@chromium.org (2022-11-11)

Congratulations, Zhenghang Xiao! The VRP Panel has decided to award you $15,000 for this report. While this exploit you provided does not presently work on shipped versions of Chrome, it clearly demonstrates exploitability potential and we appreciate your efforts in this regard and have decided to award you the V8 exploit bonus. 
A member of our finance team will be in touch with you soon to arrange payment. 
Thank you for your efforts in discovering and reporting this issue to us -- nice work! 

### rz...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### rz...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### [Deleted User] (2022-11-11)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2022-11-11)

1. Just https://crrev.com/c/4020423
2. Low, just one conflict on a generated file
3. 108
4. Yes

### am...@google.com (2022-11-11)

[Empty comment from Monorail migration]

### gm...@google.com (2022-11-15)

[Empty comment from Monorail migration]

### ki...@gmail.com (2022-11-28)

[Comment Deleted]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

Confirming that the credit information is set to "Zhenghang Xiao (@Kipreyyy)"!

### gm...@google.com (2022-12-06)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/v8/v8/+/add0f3e6f30fee2ba62ff39cfb64fb828142dc53

commit add0f3e6f30fee2ba62ff39cfb64fb828142dc53
Author: Shu-yu Guo <syg@chromium.org>
Date: Fri Oct 28 17:21:27 2022

[M102-LTS] Reland "[Promise.any] Fix errors allocation"

M102 merge issues:
  Conflicts on tools/v8heapconst.py; Reverted the conflicting
  changes and generated a new v8heapconst.py following the
  tests/mkgrokdump/README instructions

This is a reland of commit e08fa94bbcc49f3a5c3aa1371986c6365e5a09fb

Changes since revert:

Use max(remainingElements - 1, index + 1) instead of index + 1 as
newCapacity computation to avoid excessive allocations causing the
timeout.

Original change's description:
> [Promise.any] Fix errors allocation
>
> Bug: chromium:1379054
> Change-Id: Ibfcdd4ddc3c9a26471094074c8e7810d93abc898
> Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3988924
> Commit-Queue: Marja Hölttä <marja@chromium.org>
> Auto-Submit: Shu-yu Guo <syg@chromium.org>
> Reviewed-by: Marja Hölttä <marja@chromium.org>
> Cr-Commit-Position: refs/heads/main@{#83968}

(cherry picked from commit 8b35091b2d244c975975e1c78e4cd09cb479b5dc)

Bug: chromium:1379054
No-Try: true
No-Presubmit: true
No-Tree-Checks: true
Change-Id: Ic788b8d0b42f4e24eaf8b2f2d05b24390fda247b
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/3990627
Commit-Queue: Shu-yu Guo <syg@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#83987}
Reviewed-on: https://chromium-review.googlesource.com/c/v8/v8/+/4020423
Reviewed-by: Shu-yu Guo <syg@chromium.org>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/10.2@{#39}
Cr-Branched-From: 374091f382e88095694c1283cbdc2acddc1b1417-refs/heads/10.2.154@{#1}
Cr-Branched-From: f0c353f6315eeb2212ba52478983a3b3af07b5b1-refs/heads/main@{#79976}

[modify] https://crrev.com/add0f3e6f30fee2ba62ff39cfb64fb828142dc53/tools/v8heapconst.py
[modify] https://crrev.com/add0f3e6f30fee2ba62ff39cfb64fb828142dc53/src/builtins/promise-any.tq


### gi...@appspot.gserviceaccount.com (2022-12-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/61ebe2f7fbce525be737486efb0f811cc4835aca

commit 61ebe2f7fbce525be737486efb0f811cc4835aca
Author: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Date: Tue Dec 06 16:59:51 2022

Roll v8 10.2 from 9661c82fb04e to 819b6859dee5 (4 revisions)

https://chromium.googlesource.com/v8/v8.git/+log/9661c82fb04e..819b6859dee5

2022-12-06 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.2.154.22
2022-12-06 thibaudm@chromium.org [M102-LTS] Check all store modes for COW backing store access
2022-12-06 v8-ci-autoroll-builder@chops-service-accounts.iam.gserviceaccount.com Version 10.2.154.21
2022-12-06 syg@chromium.org [M102-LTS] Reland "[Promise.any] Fix errors allocation"

If this roll has caused a breakage, revert this CL and stop the roller
using the controls here:
https://autoroll.skia.org/r/v8-chromium-release-2
Please CC v8-waterfall-sheriff@grotations.appspotmail.com on the revert to ensure that a human
is aware of the problem.

To file a bug in v8 10.2: https://bugs.chromium.org/p/v8/issues/entry
To file a bug in Chromium m102: https://bugs.chromium.org/p/chromium/issues/entry

To report a problem with the AutoRoller itself, please file a bug:
https://bugs.chromium.org/p/skia/issues/entry?template=Autoroller+Bug

Documentation for the AutoRoller is here:
https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md

Bug: chromium:1379054,chromium:1382434
Tbr: v8-waterfall-sheriff@grotations.appspotmail.com
Change-Id: Icb3b8013e2beb186af16463ffdad4d35760a73f4
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4082505
Commit-Queue: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Bot-Commit: Chrome Release Autoroll <chromium-release-autoroll@skia-public.iam.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1397}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/61ebe2f7fbce525be737486efb0f811cc4835aca/DEPS


### rz...@google.com (2022-12-07)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-02-09)

Hello Zhenghang, attachments and POCs are considered to be part of the original report, so I’ve undeleted them. 

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1379054?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40061500)*
