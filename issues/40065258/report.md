# chrome.devtools.inspectedWindow.reload can run scripts on the Chrome Web Store

| Field | Value |
|-------|-------|
| **Issue ID** | [40065258](https://issues.chromium.org/issues/40065258) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | pf...@chromium.org |
| **Created** | 2023-06-03 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**

1. Download and install the extension file below
2. Visit chrome.google.com/webstore and open Inspect Element
3. Notice how inspectedWindow.eval fails but inspectedWindow.reload works

**Problem Description:**  

I'm not sure if this worked before. Judging by how inspectedWindow.eval fails for chrome.google.com/webstore, I'm assuming it's not supposed to be allowed to run on that domain. However, the injectedScript string passed to inspectedWindow.reload successfully runs scripts in the origin of chrome.google.com. This could be used to prompt a user to install another extension, or for an extension to disable another extension without the "management" permission due to high privileges on chrome.google.com/webstore.

**Additional Comments:**

\*\*Chrome version: \*\* 105.0.0.0 \*\*Channel: \*\* Stable

**OS:** Chrome OS

## Attachments

- [poc.zip](attachments/poc.zip) (application/octet-stream, 793 B)
- [Screen recording 2023-07-03 2.01.38 PM.webm](attachments/Screen recording 2023-07-03 2.01.38 PM.webm) (video/webm, 3.7 MB)
- [Screenshot 2023-07-03 2.02.45 PM.png](attachments/Screenshot 2023-07-03 2.02.45 PM.png) (image/png, 23.3 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 209 B)
- [devtools.js](attachments/devtools.js) (text/plain, 439 B)
- [devtools.html](attachments/devtools.html) (text/plain, 36 B)

## Timeline

### [Deleted User] (2023-06-03)

[Empty comment from Monorail migration]

### st...@google.com (2023-06-07)

Hi @mathia.is.fun@gmail.com is your POC an arbitrary chrome extension or something else?

### st...@google.com (2023-06-07)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-06-07)

The POC is just the extension, yes. Sorry I know this isn't a very groundbreaking bug

### [Deleted User] (2023-06-07)

[Empty comment from Monorail migration]

### ch...@google.com (2023-06-12)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/286799993). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed

[Monorail blocked-on: b/286799993]

### ja...@google.com (2023-06-12)

I don't see any platform relevance here; the bug seems to involve extension behavior. I think this is a chromium issue.

### ch...@google.com (2023-06-13)

Assigning back to the Chrome Team

### aj...@chromium.org (2023-06-13)

-> security queue for triage

### bo...@google.com (2023-06-13)

Hi extensions team, can you help assess what's going on in this case? 

This looks like is the code [1] responsible for protecting this URL pattern. Maybe this is an opportunity to address crbug.com/1355623? 

I didn't spot a directly related example in the severity guidelines [2] so the following may change, but for the sake of transparency: I'm assuming this would be high severity, but -1 to Medium because user action (i.e. installation of a specific extension ) is required to exploit.

[1] https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/web_request_permissions.cc;l=328-344;drc=f0c4fca34f1bd70964090bd11822757641352da2
[2] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md

[Monorail components: Platform>Extensions]

### [Deleted User] (2023-06-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-13)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-06-13)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### tj...@chromium.org (2023-06-13)

Nice find, this is a good one. The extensions devtools API is implemented quite adjacently to most extension APIs so it's not covered by the usual URL access checks and has its own. In this case eval (and a few other things) is protected by this check:
https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=1195;drc=ffd1424ae5737c0035102b48fe2bd8e888091c6b

It seems this was put in place to cover eval, but inspectedWindow.reload with injectedScript and ExtensionSidebarPane.setExpression might not have been fully covered. 

caseq@: I see you've got some context in this area, do you think we could just not include the injectedScript for reload if canInspectUrl comes back false somewhere in the reload function guts here? https://source.chromium.org/chromium/chromium/src/+/main:third_party/devtools-frontend/src/front_end/models/extensions/ExtensionServer.ts;l=687;drc=ffd1424ae5737c0035102b48fe2bd8e888091c6b
Although I'm not immediately sure if we have access to the URL there.

This has also highlighted that we need to add to the canInspectUrl check to also cover the new webstore domain. I've filed a bug for this at crbug.com/1454544

### ma...@gmail.com (2023-06-13)

[Comment Deleted]

### tj...@chromium.org (2023-06-20)

dsv@: Do you have any thoughts regarding my questions in https://crbug.com/chromium/1451146#c14?

### tj...@chromium.org (2023-06-28)

pfaffe@ I see you've been making some changes in this general area lately, do you think this is something you could take on?

### pf...@chromium.org (2023-06-29)

I can't reproduce this on M114 and up on chrome.google.com/webstore. Do I need to take any extra steps in addition to opening devtools with the extension installed? 

I can't access https://crbug.com/1454544, but based just on the description, may that have been the cause here?

### ma...@gmail.com (2023-06-29)

Well, I only tested it on 105 and 108

### pf...@chromium.org (2023-06-29)

Those are fairly old. Does this reproduce on a recent version for you?

### ma...@gmail.com (2023-06-30)

@pfa...@chromium.org, Have you tried opening inspect twice? Sometimes it fails the first time because of buggy API behavior I guess. I'm about to test on 114.

### ma...@gmail.com (2023-06-30)

Reproduced on 114. Had to open inspect like 5 times. No idea why it works like that.

### pf...@chromium.org (2023-07-03)

Still had no luck reproducing. Can you confirm that you're on the https://chrome.google.com/webstore and not being redirected?

### ma...@gmail.com (2023-07-03)

@23 here

### ma...@gmail.com (2023-07-03)

Huh, it didn't show the version, but here it is:

### ma...@gmail.com (2023-07-03)

[Comment Deleted]

### tj...@chromium.org (2023-07-05)

Can you double check that when the script manages to run that it actually has access to page content/privileged APIs? (e.g. checking chrome.management is defined)

The fact that it only reproduces on some of the attempts makes me wonder if it's some kind of race against the navigation actually committing the URL, in which case it may not actually have access to the privileged pieces.

### ma...@gmail.com (2023-07-05)

[Comment Deleted]

### pf...@chromium.org (2023-07-06)

[Empty comment from Monorail migration]

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


### pf...@chromium.org (2023-07-06)

I could not reproduce the reported issue but I landed a fix for a race in extension registration that was the likely cause. Could you verify whether this is fixed, please?

### ma...@gmail.com (2023-07-06)

[Comment Deleted]

### gi...@appspot.gserviceaccount.com (2023-07-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/b94a5dd538016c5367fac2495a261bb6beee89c0

commit b94a5dd538016c5367fac2495a261bb6beee89c0
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Jul 06 11:48:13 2023

Check hosts policy when loading extensions

Bug: 1451146
Change-Id: I59219bfa59c090264c7a074507520002b9d93384
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4667235
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/b94a5dd538016c5367fac2495a261bb6beee89c0/front_end/models/extensions/ExtensionServer.ts


### pf...@chromium.org (2023-07-07)

The has been released in Canary (117.0.5876.0)

### ma...@gmail.com (2023-07-07)

[Comment Deleted]

### pf...@chromium.org (2023-07-10)

Thanks for verifying the webstore fix! Looks like I deduped the other bug incorrectly then, I'll mark this one as fixed and will reopen the other.

### gi...@appspot.gserviceaccount.com (2023-07-10)

https://crbug.com/chromium/1461895 has been un-merged from this issue.


### gi...@appspot.gserviceaccount.com (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-10)

[Empty comment from Monorail migration]

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

1. https://crrev.com/c/4664806
2. In Canary since 117.0.5876.0
3. No known stability issues. Issues would also be confined to DevTools extensions
4. no
5. probably not

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

merges approved for 
https://crrev.com/c/4664806
https://crrev.com/c/4667235

please merge these fixes to M116, branch 5845 by EOD tomorrow (Wednesday, 12 July) so they can be included in the next M116/dev 
please merge these fixes to M115, branch 5790 at your earliest convenience so they can be included in the first M115 Stable respin (M115/Stable RC has already been cut to ship next Tuesday) 

### gi...@appspot.gserviceaccount.com (2023-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/8b8ce3077bd580379b3e444297360425a042039d

commit 8b8ce3077bd580379b3e444297360425a042039d
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Jul 06 11:48:13 2023

Check hosts policy when loading extensions

Bug: 1451146
Change-Id: I59219bfa59c090264c7a074507520002b9d93384
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4667235
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit b94a5dd538016c5367fac2495a261bb6beee89c0)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4684217

[modify] https://crrev.com/8b8ce3077bd580379b3e444297360425a042039d/front_end/models/extensions/ExtensionServer.ts


### gi...@appspot.gserviceaccount.com (2023-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/15667aaea13e9aedafb31551d0eb23ecc0f46e01

commit 15667aaea13e9aedafb31551d0eb23ecc0f46e01
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Jul 06 11:48:13 2023

Check hosts policy when loading extensions

Bug: 1451146
Change-Id: I59219bfa59c090264c7a074507520002b9d93384
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4667235
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit b94a5dd538016c5367fac2495a261bb6beee89c0)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4684218

[modify] https://crrev.com/15667aaea13e9aedafb31551d0eb23ecc0f46e01/front_end/models/extensions/ExtensionServer.ts


### [Deleted User] (2023-07-14)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-07-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/8b8ce3077bd580379b3e444297360425a042039d

commit 8b8ce3077bd580379b3e444297360425a042039d
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Jul 06 11:48:13 2023

Check hosts policy when loading extensions

Bug: 1451146
Change-Id: I59219bfa59c090264c7a074507520002b9d93384
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4667235
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit b94a5dd538016c5367fac2495a261bb6beee89c0)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4684217

[modify] https://crrev.com/8b8ce3077bd580379b3e444297360425a042039d/front_end/models/extensions/ExtensionServer.ts


### pf...@chromium.org (2023-07-14)

amyressler@: In order for the changes to cleanly apply (wrt to build and test), i'm afraid I will also need https://crrev.com/c/4664805. May I merge that as well?

### am...@chromium.org (2023-07-14)

pfaffe@ thanks for checking, yes -- please go ahead and merge https://crrev.com/c/4664805 to both 115/5790 and 116/5845 at your earliest convenience 

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/7d0fbc7eeb585f469eeecc0a1cb937da070d2f7e

commit 7d0fbc7eeb585f469eeecc0a1cb937da070d2f7e
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Wed Jul 05 11:34:31 2023

Tidy up ExtensionServer helpers

- Eliminate second path to add extensions for tests: We can use the
  regular extension registration path in tests except for the iframe.
  Pull the iframe setup into a separate method that tests can stub away.
- Correctly reset the devtools API object between tests. With the switch
  to new headless we were always hitting the catch in cleanup().

Bug: 1451146
Change-Id: I2d23f15690d9e04afac8df9190e222cb442dc5a4
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664805
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit a88e571bc5923241886ed68bb9a46a456b302f0e)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685556

[modify] https://crrev.com/7d0fbc7eeb585f469eeecc0a1cb937da070d2f7e/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/7d0fbc7eeb585f469eeecc0a1cb937da070d2f7e/test/unittests/front_end/models/extensions/helpers.ts


### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/f2af58b5e89924ea8e8def5643c9c798db163748

commit f2af58b5e89924ea8e8def5643c9c798db163748
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Wed Jul 05 11:34:31 2023

Tidy up ExtensionServer helpers

- Eliminate second path to add extensions for tests: We can use the
  regular extension registration path in tests except for the iframe.
  Pull the iframe setup into a separate method that tests can stub away.
- Correctly reset the devtools API object between tests. With the switch
  to new headless we were always hitting the catch in cleanup().

Bug: 1451146
Change-Id: I2d23f15690d9e04afac8df9190e222cb442dc5a4
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664805
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit a88e571bc5923241886ed68bb9a46a456b302f0e)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685557

[modify] https://crrev.com/f2af58b5e89924ea8e8def5643c9c798db163748/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/f2af58b5e89924ea8e8def5643c9c798db163748/test/unittests/front_end/models/extensions/helpers.ts


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


### aj...@google.com (2023-07-20)

Adding attachments for posterity - it's very helpful to have the raw files uploaded rather than a .zip

### am...@google.com (2023-07-21)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-07-21)

Congratulations! The VRP Panel has decided to award you $3,000 for this high-quality report. A member of our finance team will be in touch with you soon to arrange payment. In the interim, please let us know what name or other identifier you would like us to use in acknowledging you for finding and reporting this issue. 
Thank you for your efforts and reporting this issue to us -- nice work! 

### ma...@gmail.com (2023-07-21)

Wow, thanks for the bounty!

### am...@google.com (2023-07-22)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-24)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-24)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-25)

To correctly cherry-picked the changes on M108-LTS, we'll have to cherry-pick at least the following 3 changes:
- https://crrev.com/c/4685557
- https://crrev.com/c/4664806
- https://crrev.com/c/4667235

But to make tests work properly and avoid resolving a ton of conflicts and diverging from the main branch, we would have to add 3 more changes (refactoring that happened after M108 branch point):
- https://crrev.com/c/4110804
- https://crrev.com/c/4117074
- https://crrev.com/c/4637291

In this case the complexity and amount of changes is too high for a medium severity bug. We could potentially just merge the first three changes and disabled the tests that are broken but I doubt it's the right decision here for LTS stability.

### gm...@google.com (2023-07-25)

Thanks @voit. We will reject a merge to M-108. Can you please evaluate for LTC-114?

### gm...@google.com (2023-07-25)

@amyressler, @pfaffe, are we merging this to 114 extended?

### am...@chromium.org (2023-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2023-08-02)

[Empty comment from Monorail migration]

### pg...@google.com (2023-08-03)

[Empty comment from Monorail migration]

### vo...@google.com (2023-08-24)

[Empty comment from Monorail migration]

### vo...@google.com (2023-09-05)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-05)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-09-07)

1. 3 changes https://chromium-review.googlesource.com/q/topic:%225735_1451146%22
2. Medium - no conflicts but a lot of changes and they depend on 2 more changes from https://crbug.com/1429353 (they are already approved for LTS)
3. Merged to M115
4. Yes but after we merge https://crbug.com/1429353

### gm...@google.com (2023-09-18)

@voit I will delay approval as this next 114 build is critical. We can discuss further for next respin.

### gm...@google.com (2023-09-26)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/4842b0c63edd14e5b50814bcebd8d8570a31125e

commit 4842b0c63edd14e5b50814bcebd8d8570a31125e
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Wed Jul 05 11:34:31 2023

[M114-LTS] Tidy up ExtensionServer helpers

- Eliminate second path to add extensions for tests: We can use the
  regular extension registration path in tests except for the iframe.
  Pull the iframe setup into a separate method that tests can stub away.
- Correctly reset the devtools API object between tests. With the switch
  to new headless we were always hitting the catch in cleanup().

Bug: 1451146
Change-Id: I2d23f15690d9e04afac8df9190e222cb442dc5a4
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4664805
Commit-Queue: Philip Pfaffe <pfaffe@chromium.org>
(cherry picked from commit a88e571bc5923241886ed68bb9a46a456b302f0e)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4685556
(cherry picked from commit 7d0fbc7eeb585f469eeecc0a1cb937da070d2f7e)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4840771
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Reviewed-by: Danil Somsikov <dsv@chromium.org>

[modify] https://crrev.com/4842b0c63edd14e5b50814bcebd8d8570a31125e/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/4842b0c63edd14e5b50814bcebd8d8570a31125e/test/unittests/front_end/models/extensions/helpers.ts


### gi...@appspot.gserviceaccount.com (2023-09-27)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/f9df648a798f283892e68d6bcebcafb7b2c13554

commit f9df648a798f283892e68d6bcebcafb7b2c13554
Author: Philip Pfaffe <pfaffe@chromium.org>
Date: Thu Jul 06 11:48:13 2023

[M114-LTS] Check hosts policy when loading extensions

Bug: 1451146
Change-Id: I59219bfa59c090264c7a074507520002b9d93384
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4667235
Auto-Submit: Philip Pfaffe <pfaffe@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
(cherry picked from commit b94a5dd538016c5367fac2495a261bb6beee89c0)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4684217
(cherry picked from commit 8b8ce3077bd580379b3e444297360425a042039d)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4841394
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>

[modify] https://crrev.com/f9df648a798f283892e68d6bcebcafb7b2c13554/front_end/models/extensions/ExtensionServer.ts


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


### vo...@google.com (2023-09-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1451146?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail blocked-on: b/286799993]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40065258)*
