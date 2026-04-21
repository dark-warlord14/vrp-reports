# chrome.devtools.inspectedWindow origin limitations are very broken and can be bypassed

| Field | Value |
|-------|-------|
| **Issue ID** | [40066798](https://issues.chromium.org/issues/40066798) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>DevTools>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | da...@google.com |
| **Created** | 2023-07-03 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**  

Watch the video attached.

**Problem Description:**  

On:

- chrome:// pages
- chrome-extension:// component origins  
  
  the devtools frame doesn't load at all. This can be seen by the fact that there are no alerts.

This is probably what should happen when an extension does not have access to a page.

But it seems like extensions are only partially limited in this way.

On:

- chrome:// origins that don't have the actual chrome:// protocol
- chrome-error:// URLs
- about:blank
- data: URLs
- Chrome Web Store ([crbug.com/1451146](https://crbug.com/1451146))
- and probably more...  
  
  the devtools frame does load but you aren't supposed to use inspectedWindow.eval.

However, inspectedWindow.reload (and probably ExtensionSidebarPane.setExpression) do execute scripts in the context of the inspected page.

The fix I see is that the cases in the second list should have the same behavior as the cases in the first list. By this I mean the extension devtools frame in devtools://devtools should not be loaded at all.

**Additional Comments:**

\*\*Chrome version: \*\* 114.0.0.0 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [Untitled_ Jul 3, 2023 2_27 PM.mp4](attachments/Untitled_ Jul 3, 2023 2_27 PM.mp4) (video/mp4, 6.4 MB)

## Timeline

### [Deleted User] (2023-07-03)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-03)

This is somewhat related to https://crbug.com/1451146 but I figured I'd file another because this includes a lot more and is more about the extension frame being loaded instead of the chrome.inspectedWindow.eval limitations themselves.

### ds...@chromium.org (2023-07-04)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-04)

Oh, and also chrome-untrusted://crosh also has no limitations on inspectedWindow.eval.

### pf...@chromium.org (2023-07-06)

This likely has the same root cause as 1451146

### gi...@appspot.gserviceaccount.com (2023-07-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/aa7dddc46479419e55d426f61817636b702935a9

commit aa7dddc46479419e55d426f61817636b702935a9
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Jul 06 11:42:18 2023

Defer initialization of extensions when the main target isn't there yet

When the target isn't fully initialized or its inspected url isn't set
yet extension registration would fail-open. With this CL we defer
loading extensions until there is an inspected url.

Bug: 1451146, 1461895
Change-Id: Iac7a3323f561f538706c59b8e10c75ce0e3364b6
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664806
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/aa7dddc46479419e55d426f61817636b702935a9/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/aa7dddc46479419e55d426f61817636b702935a9/test/unittests/front_end/models/extensions/helpers.ts
[modify] https://crrev.com/aa7dddc46479419e55d426f61817636b702935a9/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### pf...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

[Monorail components: Platform>DevTools>Platform]

### gi...@appspot.gserviceaccount.com (2023-07-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/475e75f753101d7b248df3a2ccff95c30ab4659d

commit 475e75f753101d7b248df3a2ccff95c30ab4659d
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 10 10:08:13 2023

Block extensions on chrome-untrusted:// targets

Fixed: 1461895
Change-Id: Ic8b35ca87082c6ccbce6a7ab6937af03e31354b1
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4675376
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/475e75f753101d7b248df3a2ccff95c30ab4659d/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/475e75f753101d7b248df3a2ccff95c30ab4659d/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-07-10)

Dear owner, thanks for fixing this bug. We’ve reopened it because security bugs need Security_Severity and FoundIn labels set, which will enable the bots to request merges to the correct branches ( as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact (security@chromium.org) to arrange to set these labels and then this bug can be marked closed again. Thank you! Severity guidelines: https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues FoundIn guidelines: https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security Thanks for your time! 

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2023-07-10)

I now added chrome-untrusted: to the list of blocked schemes. In general, the rule of thumb is that we only disallow extensions on chrome internals. So we consider, e.g. data: urls to be fine. chrome-untrusted: is a bit of a special case, because although in general it doesn't look to be extremely different from web content from a security perspective, chrome-untrusted://crosh and chrome-untrusted://terminal are a different story.

dsv@: sending this your way for the severity question in c#9

### ma...@gmail.com (2023-07-10)

[Comment Deleted]

### ds...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### pf...@chromium.org (2023-07-10)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-10)

[Comment Deleted]

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-10)

[Comment Deleted]

### [Deleted User] (2023-07-10)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pf...@chromium.org (2023-07-11)

@c#20 Does the PoC work on 117.0.5882.0 which has the fix above? Was the fix insufficient?

### ma...@gmail.com (2023-07-11)

@22, no. It the root part of that bug is fixed along with this bug.

### ma...@gmail.com (2023-07-11)

The crbug I linked is mainly about another issue. I just mentioned this in there because it could be abused along with it.

### pf...@chromium.org (2023-07-11)

Thanks for verifying the fix!

For the merge request:
1. https://crrev.com/c/4675376
2. In Canary as of 117.0.5882.0
3. No known stability issues, stability issues would be confined to devtools extensions
4. No known compatibility issues
5. No

### [Deleted User] (2023-07-11)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-11)

I noticed this backmerge request is being specified to https://crrev.com/c/4675376 in c#25.
It seems prudent to also also backmerge https://crrev.com/c/4664806 and https://crrev.com/c/4675376. Is there a reason against backmerging these CLs as well? 

In any case, the latest fix just landed a few hours ago, so I'm going to let this get a bit more bake time before doing merge approvals here regardless. 
Also, RC for M115 has already been cut so we're not running against Stable release deadlines for now either. 

### am...@chromium.org (2023-07-11)

[Comment Deleted]

### am...@chromium.org (2023-07-11)

In reviewing https://crbug.com/chromium/1451146, I'm seeing the merge request for https://crrev.com/c/4664806 is indeed being requested there. I'll review that one there in tandem with the other CL landed to that issue. 
Let's allow https://crrev.com/c/4675376 a bit more bake time since it was just landed earlier today. I can revisit this one tomorrow or Thursday for merge review. 

### [Deleted User] (2023-07-12)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M115. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

This is sufficiently serious that it should be merged to dev. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M116. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [115, 116].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-07-13)

Merges approved for https://crrev.com/c/4675376. 
Please merge this fix to M116/branch 5845 and M115/branch 5790 at your earliest convenience. 

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/bbb6c19f11a76e7e3d6cc56f9d978974060f4384

commit bbb6c19f11a76e7e3d6cc56f9d978974060f4384
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 17 11:10:19 2023

Defer initialization of extensions when the main target isn't there yet

When the target isn't fully initialized or its inspected url isn't set
yet extension registration would fail-open. With this CL we defer
loading extensions until there is an inspected url.

Bug: 1451146, 1461895
Change-Id: Iac7a3323f561f538706c59b8e10c75ce0e3364b6
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664806
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit aa7dddc46479419e55d426f61817636b702935a9)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4679110

[modify] https://crrev.com/bbb6c19f11a76e7e3d6cc56f9d978974060f4384/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/bbb6c19f11a76e7e3d6cc56f9d978974060f4384/test/unittests/front_end/models/extensions/helpers.ts
[modify] https://crrev.com/bbb6c19f11a76e7e3d6cc56f9d978974060f4384/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### [Deleted User] (2023-07-17)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/f5dfe0a0d38f4ce408b235dac0870da45e2f2676

commit f5dfe0a0d38f4ce408b235dac0870da45e2f2676
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 17 11:02:05 2023

Defer initialization of extensions when the main target isn't there yet

When the target isn't fully initialized or its inspected url isn't set
yet extension registration would fail-open. With this CL we defer
loading extensions until there is an inspected url.

Bug: 1451146, 1461895
Change-Id: Iac7a3323f561f538706c59b8e10c75ce0e3364b6
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664806
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit aa7dddc46479419e55d426f61817636b702935a9)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4679109

[modify] https://crrev.com/f5dfe0a0d38f4ce408b235dac0870da45e2f2676/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/f5dfe0a0d38f4ce408b235dac0870da45e2f2676/test/unittests/front_end/models/extensions/helpers.ts
[modify] https://crrev.com/f5dfe0a0d38f4ce408b235dac0870da45e2f2676/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/e1ee7c138cb50acd260d4b6d4f387d4b93604401

commit e1ee7c138cb50acd260d4b6d4f387d4b93604401
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 17 12:39:59 2023

Block extensions on chrome-untrusted:// targets

Fixed: 1461895
Change-Id: Ic8b35ca87082c6ccbce6a7ab6937af03e31354b1
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4675376
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit 475e75f753101d7b248df3a2ccff95c30ab4659d)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685571

[modify] https://crrev.com/e1ee7c138cb50acd260d4b6d4f387d4b93604401/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/e1ee7c138cb50acd260d4b6d4f387d4b93604401/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/96e54da7d3b5724087d1e63590cf7ed16d92a1a7

commit 96e54da7d3b5724087d1e63590cf7ed16d92a1a7
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 17 11:34:50 2023

Block extensions on chrome-untrusted:// targets

Fixed: 1461895
Change-Id: Ic8b35ca87082c6ccbce6a7ab6937af03e31354b1
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4675376
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit 475e75f753101d7b248df3a2ccff95c30ab4659d)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685560

[modify] https://crrev.com/96e54da7d3b5724087d1e63590cf7ed16d92a1a7/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/96e54da7d3b5724087d1e63590cf7ed16d92a1a7/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/e1ee7c138cb50acd260d4b6d4f387d4b93604401

commit e1ee7c138cb50acd260d4b6d4f387d4b93604401
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 17 12:39:59 2023

Block extensions on chrome-untrusted:// targets

Fixed: 1461895
Change-Id: Ic8b35ca87082c6ccbce6a7ab6937af03e31354b1
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4675376
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit 475e75f753101d7b248df3a2ccff95c30ab4659d)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685571

[modify] https://crrev.com/e1ee7c138cb50acd260d4b6d4f387d4b93604401/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/e1ee7c138cb50acd260d4b6d4f387d4b93604401/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### am...@google.com (2023-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-21)

Congratulations on another one! The VRP Panel has decided to award you $1,000 for this report. The reward amount was decided based on the limited impact of this issue on its own. Thank you for your effort and reporting this issue to us! 

### ma...@gmail.com (2023-07-21)

Thank you for the bounty!

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-24)

[Empty comment from Monorail migration]

### gm...@google.com (2023-07-25)

Rejecting merge to LTS-108 per https://bugs.chromium.org/p/chromium/issues/detail?id=1451146. If not merged to 114 extended, we need to evaluate for LTC-114.

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-08-03)

Can you set reporter credit to "Derin Eryilmaz" on https://chromereleases.googleblog.com/2023/08/stable-channel-update-for-desktop.html for this bug and 1451146?

### rz...@google.com (2023-09-18)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/19e49ea40f03bb0dc6f507152083a6640dccd3e1

commit 19e49ea40f03bb0dc6f507152083a6640dccd3e1
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Mon Jul 17 11:10:19 2023

[M114-LTS] Defer initialization of extensions when the main target isn't there yet

When the target isn't fully initialized or its inspected url isn't set
yet extension registration would fail-open. With this CL we defer
loading extensions until there is an inspected url.

Bug: 1451146, 1461895
Change-Id: Iac7a3323f561f538706c59b8e10c75ce0e3364b6
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664806
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
(cherry picked from commit aa7dddc46479419e55d426f61817636b702935a9)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4679110
(cherry picked from commit bbb6c19f11a76e7e3d6cc56f9d978974060f4384)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4810314
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/19e49ea40f03bb0dc6f507152083a6640dccd3e1/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/19e49ea40f03bb0dc6f507152083a6640dccd3e1/test/unittests/front_end/models/extensions/helpers.ts
[modify] https://crrev.com/19e49ea40f03bb0dc6f507152083a6640dccd3e1/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### na...@google.com (2023-10-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1461895?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066798)*
