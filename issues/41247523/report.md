# Download Protection: SPARSEBUNDLE and SPARSEIMAGE files not checked on Mac OS X

| Field | Value |
|-------|-------|
| **Issue ID** | [41247523](https://issues.chromium.org/issues/41247523) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **Reporter** | ya...@nightwatchcybersecurity.com |
| **Assignee** | ji...@chromium.org |
| **Created** | 2016-04-05 |
| **Bounty** | $6,000.00 |

## Description

**VERSION**  

Chrome Version: 49.0.2623.87 Official Build  

Operating System: Mac OS X El Capitan, version 10.11.3

**REPRODUCTION CASE**  

SPARSEBUNDLE and SPARSEIMAGE files are not checked by download protection on Mac OS. Problem is that you can take any DMG file and renamed it, and serve it that way. Mac OS will treat both the same. To replicate this issue, take any DMG file, stick it on a web server, and rename to an .SPARSEIMAGE or .SPARSEBUNDLE. Then download on Mac and double click. It will act the same way as a DMG.

We can try to provide a patch.

Same behavior as  

<https://bugs.chromium.org/p/chromium/issues/detail?id=596354> but found later on

## Timeline

### ya...@nightwatchcybersecurity.com (2016-04-05)

This also affects the following extensions:
CDR
DMGPART
DVDR
DART
DC42
DISKCOPY42
IMGPART
NDIF
UDIF

### np...@chromium.org (2016-04-05)

jialiul -- Can you confirm try these and confirm this behavior?  Then we should treat these like DMGs and report+parse them.

### rs...@chromium.org (2016-04-05)

FYI real .sparsebundle files cannot be directly downloaded from the web, since they are directories (.sparseimage files are plain files). Neither are currently supported by the DMG analyzer within Chromium, though. But renaming a .dmg to one of those extensions would trigger DiskUtility to open it regardless of the extension.

### ji...@chromium.org (2016-04-05)

Confirmed. Unfortunately, these types are not in our dangerous file type list, and they can be opened the same way as dmg. 

### rs...@chromium.org (2016-04-05)

If we wanted to avoid using extension lists for this, it is possible to query the system for what application will open the file. That can be done with -[NSWorkspace URLForApplicationToOpenURL:].

### ya...@nightwatchcybersecurity.com (2016-04-06)

In addition to the extensions in comment, also .TOAST

### np...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### ji...@chromium.org (2016-04-18)

Merge request due to security implication. Thanks!

### bu...@chromium.org (2016-04-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/cd719f651b57e7235f30b974e763e569f2cc9aeb

commit cd719f651b57e7235f30b974e763e569f2cc9aeb
Author: jialiul <jialiul@chromium.org>
Date: Mon Apr 18 20:08:21 2016

Add more mac executable extensions

BUG=600613

Review URL: https://codereview.chromium.org/1881763002

Cr-Commit-Position: refs/heads/master@{#387995}

[modify] https://crrev.com/cd719f651b57e7235f30b974e763e569f2cc9aeb/chrome/browser/download/download_extensions.cc
[modify] https://crrev.com/cd719f651b57e7235f30b974e763e569f2cc9aeb/chrome/browser/safe_browsing/download_protection_service.cc
[modify] https://crrev.com/cd719f651b57e7235f30b974e763e569f2cc9aeb/chrome/common/safe_browsing/download_protection_util.cc
[modify] https://crrev.com/cd719f651b57e7235f30b974e763e569f2cc9aeb/content/browser/download/download_stats.cc
[modify] https://crrev.com/cd719f651b57e7235f30b974e763e569f2cc9aeb/tools/metrics/histograms/histograms.xml


### va...@chromium.org (2016-04-18)

research@nightwatchcybersecurity.com: Thanks for reporting the issue. As confirmed by jialiul@, we can reproduce this issue locally.

I'll investigate whether it falls within the guidelines of the VRP program (it most likely does) and will update the issue shortly thereafter.

### va...@chromium.org (2016-04-18)

I can confirm that the issue does indeed fall within the guidelines of the Download Protection bypass VRP. Sending to the panel for reward review.

### va...@chromium.org (2016-04-18)

[Empty comment from Monorail migration]

### am...@chromium.org (2016-04-18)

[Empty comment from Monorail migration]

### ti...@google.com (2016-04-19)

Pls confirm the change has baked in canary and verified safe? Thanks.

### ti...@google.com (2016-04-19)

[Automated comment] Request affecting a post-stable build (M50), manual review required.

### ti...@google.com (2016-04-19)

jialiul@ is waiting for canary to ramp up a little more to get meaningful data from UMA, we chatted and agreed not to include in this week's M50 stable refresh but potential future ones.

### ji...@chromium.org (2016-04-20)

tinazh@, I has verified this change in canary. Request permission to merge into later M50 stable refresh. Thanks! 

### ji...@chromium.org (2016-04-20)

[Empty comment from Monorail migration]

### go...@chromium.org (2016-04-22)

Approving merge M50 branch 2661 based on https://crbug.com/chromium/600613#c17 & #18.

### bu...@chromium.org (2016-04-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac

commit e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac
Author: Jialiu Lin <jialiul@chromium.org>
Date: Fri Apr 22 18:36:02 2016

Add more mac executable extensions

BUG=600613

Review URL: https://codereview.chromium.org/1881763002

Cr-Commit-Position: refs/heads/master@{#387995}
(cherry picked from commit cd719f651b57e7235f30b974e763e569f2cc9aeb)

Review URL: https://codereview.chromium.org/1919463002 .

Cr-Commit-Position: refs/branch-heads/2661@{#622}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac/chrome/browser/download/download_extensions.cc
[modify] https://crrev.com/e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac/chrome/browser/safe_browsing/download_protection_service.cc
[modify] https://crrev.com/e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac/chrome/common/safe_browsing/download_protection_util.cc
[modify] https://crrev.com/e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac/content/browser/download/download_stats.cc
[modify] https://crrev.com/e5a9304bd17eea442cc8a2a4f7a4bc75ac86bdac/tools/metrics/histograms/histograms.xml


### va...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-25)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-02)

Thanks again for your report.

Someone from our finance team should get in contact within 7 days to collect payment details. If that doesn't happen, please contact me directly at timwillis@ or update this bug.

### in...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### in...@chromium.org (2017-03-09)

[Empty comment from Monorail migration]

### va...@chromium.org (2017-03-10)

For all Download Protection VRP bugs: removing label Restrict-View-Google and adding Restrict-View-SecurityTeam instead.

### sh...@chromium.org (2017-03-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2017-03-11)

This issue was migrated from crbug.com/chromium/600613?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, Services>Safebrowsing>VRP]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41247523)*
