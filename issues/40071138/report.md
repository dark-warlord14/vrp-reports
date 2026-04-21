# Security: Cookie leaking from the request object in chrome.devtools.network in onRequestFinished event

| Field | Value |
|-------|-------|
| **Issue ID** | [40071138](https://issues.chromium.org/issues/40071138) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Windows |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ds...@chromium.org |
| **Created** | 2023-09-01 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

<https://chromium.googlesource.com/devtools/devtools-frontend/+/90ebdff4cc6efa1c3fbf3026d2be4de268c3afe6> fixed an issue in <https://bugs.chromium.org/p/chromium/issues/detail?id=1471253> where cookie values were uncleared for enterprise-policy blocked hosts. However the fix was limited to getHAR() function.

In <https://developer.chrome.com/docs/extensions/reference/devtools_network>, there exist an event listener onRequestFinished() that returns request object which do not clear cookie values as well.

**VERSION**  

Chrome Version: 118.0.5981.1 (Official Build) canary-dcheck (64-bit) (cohort: DCHECK-64)  

Operating System: Windows 10

## **REPRODUCTION CASE** 0. Add runtime\_blocked\_hosts value:

{"\*":{"runtime\_blocked\_hosts":["\*://example.org"]}}

Go to regedit.exe on windows,

Computer\HKEY\_CURRENT\_USER\SOFTWARE\Policies\Google\Chrome

and add a new key

ExtensionSettings

with value

## {"\*":{"runtime\_blocked\_hosts":["\*://example.org"]}}

1. Run document.cookie = "a=b;SameSite=None;Secure" in devtools on <https://example.org>
2. Install extension
3. Open devtools to see the full request object and see that the cookie is present.

Note that the attack is not limited to SameSite=None cookies, it can also read cookies if a request is made from subdomain.example.org to example.org if subdomain.example.org is in the runtime allowed host list but example.org is not, for example.

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [background.js](attachments/background.js) (text/plain, 74 B)
- [devtools.html](attachments/devtools.html) (text/plain, 35 B)
- [devtools.js](attachments/devtools.js) (text/plain, 182 B)
- [manifest.json](attachments/manifest.json) (text/plain, 184 B)

## Timeline

### [Deleted User] (2023-09-01)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-09-01)

see https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4835537

### za...@chromium.org (2023-09-01)

Hi dsv@ chrome security shepherd here, can you take a look at this bug, it's similar to crbug.com/1471253

[Monorail components: Platform>Extensions>API]

### [Deleted User] (2023-09-01)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-02)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-15)

dsv: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-09-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/a9e7d752bc53598a113125c61f4aeb917335b673

commit a9e7d752bc53598a113125c61f4aeb917335b673
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Sep 18 10:39:05 2023

Do not notify extensions of NetworkRequestFinished events if extension does not have access to the request destination.

Change-Id: I3e128324fa70b71a6451bd0414e6e8750a0b9ca1
Bug: 1478150
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4835537
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>

[modify] https://crrev.com/a9e7d752bc53598a113125c61f4aeb917335b673/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/a9e7d752bc53598a113125c61f4aeb917335b673/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### ds...@chromium.org (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-09-18)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@gmail.com (2023-09-19)

To VRP panel: can you assess https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4835537 for patch bonus (I think when dsv@ made some changes to the patch the commit message (including the author) was overwritten and therefore Git Watcher shows dsv@ as the author.)

### [Deleted User] (2023-09-19)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-20)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ds...@chromium.org (2023-09-21)

1. https://chromium.googlesource.com/devtools/devtools-frontend/+/a9e7d752bc53598a113125c61f4aeb917335b673
2. Yes
3. Yes
4. No
5. See the issue summary

### [Deleted User] (2023-09-22)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M118. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-09-22)

118 merge approved for https://crrev.com/c/4835537, please merge this fix to branch 5993 at your earliest convenience (and before EOD Tuesday, 26 September) 

### gi...@appspot.gserviceaccount.com (2023-09-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/devtools/devtools-frontend/+/bcf0ed097be848d234fb5290c1e4d69672dc5405

commit bcf0ed097be848d234fb5290c1e4d69672dc5405
Author: Danil Somsikov <dsv@chromium.org>
Date: Mon Sep 18 10:39:05 2023

Do not notify extensions of NetworkRequestFinished events if extension does not have access to the request destination.

Change-Id: I3e128324fa70b71a6451bd0414e6e8750a0b9ca1
Bug: 1478150
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4835537
Reviewed-by: Danil Somsikov <dsv@chromium.org>
Commit-Queue: Danil Somsikov <dsv@chromium.org>
Reviewed-by: Philip Pfaffe <pfaffe@chromium.org>
(cherry picked from commit a9e7d752bc53598a113125c61f4aeb917335b673)
Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/4891508

[modify] https://crrev.com/bcf0ed097be848d234fb5290c1e4d69672dc5405/front_end/models/extensions/ExtensionServer.ts
[modify] https://crrev.com/bcf0ed097be848d234fb5290c1e4d69672dc5405/test/unittests/front_end/models/extensions/ExtensionServer_test.ts


### am...@google.com (2023-09-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-29)

Thank you for this report, Axel. The Chrome VRP Panel has decided to award you $500 award / patch bonus for the report. Given the limited security implications from this issue, we have focused the award on your efforts in providing a patch instead. Thank you for your efforts in helping us make faster fixes to Chrome. 

### am...@google.com (2023-09-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1478150?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40071138)*
