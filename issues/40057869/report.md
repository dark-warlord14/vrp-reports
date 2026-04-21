# Security: Continued cookie bypasses

| Field | Value |
|-------|-------|
| **Issue ID** | [40057869](https://issues.chromium.org/issues/40057869) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network>Cookies |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | la...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2021-11-09 |
| **Bounty** | $4,000.00 |

## Description

https://bugs.chromium.org/p/chromium/issues/detail?id=1244289#c29 reports that the fix to that bug isn't complete. Opening a new issue to ensure we take a look.



## Attachments

- [issue.patch](attachments/issue.patch) (text/plain, 6.0 KB)

## Timeline

### [Deleted User] (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

[Empty comment from Monorail migration]

### ts...@chromium.org (2021-11-09)

Copying some labels from referenced bug.

### [Deleted User] (2021-11-12)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-11-24)

rayankans: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-16)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-12-27)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-06)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-01-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@gmail.com (2022-01-20)

Hey, just wanted to ask if there is any update on this, especially since https://crbug.com/chromium/1244289 got disclosed (not sure if this was intended?). There is also a typo in the email of the "reward_to" label.

### la...@gmail.com (2022-01-20)

Here are also the steps to reproduce the issue (the only difference to https://crbug.com/chromium/1244289 is that there is now a redirect).

- Set a cookie with `SameSite=strict` here: https://foregoing-sulky-carpenter.glitch.me/
- Start a local webserver with `php -S 127.0.0.1:8000` hosting these files:

```test.html
<script>
  const url = "/redirect.php?url=https://foregoing-sulky-carpenter.glitch.me/echo-cookie";

  navigator.serviceWorker.ready.then(async (swReg) => {
    const request = new Request(url);

    const bgFetch = await swReg.backgroundFetch.fetch("test", [request]);

    const targetPage = await bgFetch.match(url);
    const response = await targetPage.responseReady;
    console.log("Background Fetch:", await response.text()); // contains cookie

    const normalFetch = await fetch(request);
    console.log("Fetch:", await normalFetch.text()); // no cookie
  });

  navigator.serviceWorker.register("sw.js");
</script>
```

```sw.js
// can be empty
```

```redirect.php
<?php
header("Location: " . $_GET["url"]);
```


### [Deleted User] (2022-02-02)

[Empty comment from Monorail migration]

### [Deleted User] (2022-03-07)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-17)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-28)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-03-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-05-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-05-25)

[Empty comment from Monorail migration]

### th...@chromium.org (2022-06-10)

Security marshal here.
 - rayankans@, could you take a look at this ticket?
 - amyressler@, could you help respond to https://crbug.com/chromium/1268580#c12?

### la...@gmail.com (2022-06-13)

This can be fixed by setting `request->update_first_party_url_on_redirect` to `false` for downloads initiated by background fetch as I mentioned in https://bugs.chromium.org/p/chromium/issues/detail?id=1320432#c13. I have separated the part of the patch from the comment that is relevant for fixing this issue.

### ad...@google.com (2022-06-13)

[Empty comment from Monorail migration]

### ad...@google.com (2022-06-17)

Hey qinmin@, do I understand correctly that some download-side changes are likely to be required here rather than background fetch stuff? Can you take care of it? This is medium severity but has accidentally been disclosed, so we'd like to get it fixed rather urgently if we can.

### gi...@appspot.gserviceaccount.com (2022-06-21)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bf1e93c6af21dad12088b615feda07a90a85c158

commit bf1e93c6af21dad12088b615feda07a90a85c158
Author: Min Qin <qinmin@chromium.org>
Date: Tue Jun 21 18:19:05 2022

[Background fetch] passing update_first_party_url_on_redirect=false for fetch

Background fetch doesn't work like regular download as it is not
considered a top frame navigation. This CL let background fetch to
pass update_first_party_url_on_redirect=false to DownloadURLParameters,
and handle it properly w.r.t samesite cookies.

BUG=1268580

Change-Id: I3a1cc33be8578d5d8c796dbbb21fa35a47bdda36
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3712307
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1016316}

[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/components/download/public/background_service/download_params.h
[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/bf1e93c6af21dad12088b615feda07a90a85c158/components/download/content/internal/download_driver_impl.cc


### qi...@chromium.org (2022-06-21)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-22)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-06-27)

this fix has only made it to 105 so far, since this is a medium severity issue this should at least be merged to 104; updated label accordingly so this can go into our merge review queue 

### [Deleted User] (2022-06-27)

Merge review required: M104 is already shipping to beta.

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
Owners: eakpobaro (Android), harrysouders (iOS), obenedict (ChromeOS), srinivassista (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### qi...@chromium.org (2022-06-27)

1. Security fix
2. https://chromium-review.googlesource.com/c/chromium/src/+/3712307
3. Yes
4. Np
5. N/A
6.N/A

### am...@chromium.org (2022-06-28)

M104 merge approved, please merge this fix to branch 5112 at your earliest convenience so this fix can be included in Wednesday's release of M104 beta -- thank you! 

### sr...@google.com (2022-06-28)

This bug has been approved for Merge to M104 and the merge has not been completed , Please merge your change asap to M104 branch before 2pm PST today ( tuesday Jun 28) as I will be cutting Beta RC build at that time for this week's beta release. I would like to get these  CL's merged asap so we get good beta coverage 

### gi...@appspot.gserviceaccount.com (2022-06-28)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca

commit bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca
Author: Min Qin <qinmin@chromium.org>
Date: Tue Jun 28 16:27:43 2022

[M104][Background fetch] passing update_first_party_url_on_redirect=false for fetch

Background fetch doesn't work like regular download as it is not
considered a top frame navigation. This CL let background fetch to
pass update_first_party_url_on_redirect=false to DownloadURLParameters,
and handle it properly w.r.t samesite cookies.

BUG=1268580

(cherry picked from commit bf1e93c6af21dad12088b615feda07a90a85c158)

Change-Id: I3a1cc33be8578d5d8c796dbbb21fa35a47bdda36
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3712307
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1016316}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3727786
Cr-Commit-Position: refs/branch-heads/5112@{#397}
Cr-Branched-From: b13d3fe7b3c47a56354ef54b221008afa754412e-refs/heads/main@{#1012729}

[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/components/download/public/background_service/download_params.h
[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/bd9724c9fe6333eddd9c18a7b35ba9f7541ad1ca/components/download/content/internal/download_driver_impl.cc


### [Deleted User] (2022-06-28)

LTS Milestone M102

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-06-29)


LTS Milestone M96

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### am...@google.com (2022-06-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-06-29)

Congratulations! The VRP Panel has decided to award you $4,000 for this report, including the additional POC and a patch that helped us root cause and helped provide information towards our fix in the end. Thank you for your efforts and information us this issue was not fully resolved! 

### rz...@google.com (2022-06-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-30)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2022-06-30)

[Empty comment from Monorail migration]

### rz...@google.com (2022-06-30)

M96:
1. Just https://crrev.com/c/3734903
2. Low, only a simple naming conflict
3. 104
4. Yes

### rz...@google.com (2022-06-30)

M102:
1. Just https://crrev.com/c/3736391
2. Low, no conflicts
3. 104
4. Yes

### gm...@google.com (2022-06-30)

Delaying LTS merges until 104 goes to Stable.

### am...@google.com (2022-07-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### gm...@google.com (2022-08-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aef34f0b559eb2c9e96af9bce25046c353dacab2

commit aef34f0b559eb2c9e96af9bce25046c353dacab2
Author: Min Qin <qinmin@chromium.org>
Date: Fri Aug 12 09:38:20 2022

[M102-LTS][Background fetch] passing update_first_party_url_on_redirect=false for fetch

Background fetch doesn't work like regular download as it is not
considered a top frame navigation. This CL let background fetch to
pass update_first_party_url_on_redirect=false to DownloadURLParameters,
and handle it properly w.r.t samesite cookies.

BUG=1268580

(cherry picked from commit bf1e93c6af21dad12088b615feda07a90a85c158)

Change-Id: I3a1cc33be8578d5d8c796dbbb21fa35a47bdda36
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3712307
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1016316}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3736391
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Cr-Commit-Position: refs/branch-heads/5005@{#1294}
Cr-Branched-From: 5b4d9450fee01f821b6400e947b3839727643a71-refs/heads/main@{#992738}

[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/components/download/public/background_service/download_params.h
[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/aef34f0b559eb2c9e96af9bce25046c353dacab2/components/download/content/internal/download_driver_impl.cc


### gi...@appspot.gserviceaccount.com (2022-08-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da

commit b9e03b68f8439b995a9f0b70a2cc4705c3aec9da
Author: Min Qin <qinmin@chromium.org>
Date: Fri Aug 12 10:40:52 2022

[M96-LTS][Background fetch] passing update_first_party_url_on_redirect=false for fetch

M96 merge issues:
  components/download/internal/common/download_utils.cc
    Naming conflict for is_main_frame/is_outermost_main_frame

Background fetch doesn't work like regular download as it is not
considered a top frame navigation. This CL let background fetch to
pass update_first_party_url_on_redirect=false to DownloadURLParameters,
and handle it properly w.r.t samesite cookies.

BUG=1268580

(cherry picked from commit bf1e93c6af21dad12088b615feda07a90a85c158)

Change-Id: I3a1cc33be8578d5d8c796dbbb21fa35a47bdda36
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3712307
Commit-Queue: Min Qin <qinmin@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1016316}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3734903
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/4664@{#1674}
Cr-Branched-From: 24dc4ee75e01a29d390d43c9c264372a169273a7-refs/heads/main@{#929512}

[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/content/browser/download/download_browsertest.cc
[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/components/download/internal/common/download_utils.cc
[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/components/download/public/common/download_url_parameters.cc
[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/components/download/public/background_service/download_params.h
[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/components/download/public/common/download_url_parameters.h
[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/components/background_fetch/background_fetch_delegate_base.cc
[modify] https://crrev.com/b9e03b68f8439b995a9f0b70a2cc4705c3aec9da/components/download/content/internal/download_driver_impl.cc


### rz...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1268580?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057869)*
