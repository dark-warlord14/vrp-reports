# IMG files are not checked on Mac OS

| Field | Value |
|-------|-------|
| **Issue ID** | [41245012](https://issues.chromium.org/issues/41245012) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | Mac |
| **Reporter** | ya...@nightwatchcybersecurity.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2016-03-21 |
| **Bounty** | $1,500.00 |

## Description

**VERSION**  

Chrome Version: 49.0.2623.87 Official Build  

Operating System: Mac OS X El Capitan, version 10.11.3

**REPRODUCTION CASE**  

IMG files are not checked by download protection on Mac OS. Problem is that you can take any DMG file and renamed it as an IMG file and serve it that way. Mac OS will treat both the same. To replicate this issue, take any DMG file, stick it on a web server, and renamed to an IMG. Then download on Mac and double click. It will act the same way as a DMG

We will be providing a patch as well.

## Attachments

- [img.patch](attachments/img.patch) (application/octet-stream, 1.9 KB)
- [second.patch](attachments/second.patch) (application/octet-stream, 2.7 KB)
- [third.patch](attachments/third.patch) (application/octet-stream, 3.6 KB)

## Timeline

### ya...@nightwatchcybersecurity.com (2016-03-21)

attaching patch

### cl...@chromium.org (2016-03-21)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-03-21)

Thanks for the report!

rsesek -- Can you corroborate this?  And are the other types we should be checking on Mac?  Thanks

### rs...@chromium.org (2016-03-21)

Yes, we only check .dmg files at the moment. I don't think the patch in #1 is complete, since it doesn't look like the file will be scanned by the DMG analyzer.

### ya...@nightwatchcybersecurity.com (2016-03-21)

We are attaching a more complete patch covering the analyzer.

HOWEVER, there are some internal differences in formats between the two (IMG is Mac OS 9 and lower), so we are not sure whether the DMG analyzer will work on all IMG files. 

### ya...@nightwatchcybersecurity.com (2016-03-21)

We did some more digging, and it looks like the same issue happens if you rename a DMG file to .ISO and .SMI. Should we file a separate bug for those, or update this one, and make a new patch?

### np...@chromium.org (2016-03-21)

Let's keep it in this bug, since they're different classes of the same thing.

### me...@chromium.org (2016-03-21)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-03-21)

We are adding a patch for IMG, ISO and SMI files. For ISO specifically, it is already checked, but this patch adds it to the DMZ analyzer as well.

Does this report qualify for VRP?

### np...@chromium.org (2016-03-24)

Yes, it qualifies.  Congrats! And thank you for the excellent patch.  I have a CL with it pending.  I'll get the appropriate labels attached here shortly.

### bu...@chromium.org (2016-03-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/74ab4f95a557f6cfb425555a0c7021e80d9319dc

commit 74ab4f95a557f6cfb425555a0c7021e80d9319dc
Author: nparker <nparker@chromium.org>
Date: Fri Mar 25 16:15:07 2016

Report and parse .img, .iso, and .smi as DMGs when downloading

These files are all opened by Disk Utility.

70% of this patch was written by research@nightwatchcybersecurity.com

BUG=596354

Review URL: https://codereview.chromium.org/1827303002

Cr-Commit-Position: refs/heads/master@{#383277}

[modify] https://crrev.com/74ab4f95a557f6cfb425555a0c7021e80d9319dc/chrome/browser/safe_browsing/download_protection_service.cc
[modify] https://crrev.com/74ab4f95a557f6cfb425555a0c7021e80d9319dc/chrome/common/safe_browsing/download_protection_util.cc
[modify] https://crrev.com/74ab4f95a557f6cfb425555a0c7021e80d9319dc/tools/metrics/histograms/histograms.xml


### np...@chromium.org (2016-03-25)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-03-28)

@nparker - How do we claim the VRP?

### np...@chromium.org (2016-03-28)

This bug will go through our VRP review board to decide on the reward.  I should have more info by Friday.

### np...@chromium.org (2016-03-30)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-04-01)

We found two additional extensions that exhibit similar behavior. Should we file a new bug?

### ya...@nightwatchcybersecurity.com (2016-04-04)

@nparker - any news on VRP?

Also, what should we do about the two new extensions?

### ya...@nightwatchcybersecurity.com (2016-04-05)

additional extensions filed as a bug here:
https://bugs.chromium.org/p/chromium/issues/detail?id=600613

### np...@chromium.org (2016-04-05)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-04-11)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-04-12)

How do we claim VRP?

### np...@chromium.org (2016-04-14)

The ball is in our court -- we will contact you as part of a weekly sweep of VRP bugs.

### ya...@nightwatchcybersecurity.com (2016-04-15)

@nparker - what about other SafeBrowsing bugs we submitted?

### np...@chromium.org (2016-04-15)

Those are in our triage queue. They will eventually have a reward-{$$, ineligible} label or will be marked WontFix.

### va...@chromium.org (2016-04-18)

research@nightwatchcybersecurity.com: I'm sorry for the delay in triaging those bugs but I will try to do that this week. Thanks again for submitting them.

### va...@chromium.org (2016-04-25)

I just realized that I had not applied one label due to which this reward did not get paid in the current cycle. Adding it now. Sorry for the delay in getting the reward out.

### ya...@nightwatchcybersecurity.com (2016-04-25)

No problem and thank you

### ya...@nightwatchcybersecurity.com (2016-04-25)

Does VRP for this include the patch or do we need to email patch rewards separately?

### va...@chromium.org (2016-04-26)

It does include the reward for the patch.

### ya...@nightwatchcybersecurity.com (2016-05-01)

@vakh@chromium.org - thank you. We still have about 4 open SB bugs, are these going to be looked at also?

Thanks

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

This issue was migrated from crbug.com/chromium/596354?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, Services>Safebrowsing>VRP]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41245012)*
