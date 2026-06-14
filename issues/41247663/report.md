# Download Protection: Additional Compressed Formats for Mac OS

| Field | Value |
|-------|-------|
| **Issue ID** | [41247663](https://issues.chromium.org/issues/41247663) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P4 |
| **Component** | Unknown |
| **Reporter** | ya...@nightwatchcybersecurity.com |
| **Assignee** | np...@chromium.org |
| **Created** | 2016-04-06 |
| **Bounty** | $2,000.00 |

## Description

**VERSION**  

Chrome Version: 49.0.2623.87 Official Build  

Operating System: Mac OS X El Capitan, version 10.11.3

**REPRODUCTION CASE**  

The following file extensions are opened by the Archive Mounter utility on Mac OS, even if they are a different extension (GZ versus ZIP). To reproduce, take any .ZIP file, and rename as one of the following extensions. Double click and the file will still be opened as ZIP. Chrome does not check these.

.AS  

.CPGZ  

.PAX  

.XIP

We can try to provide a patch if it would qualify under Patch Rewards.

## Attachments

- [comp.patch](attachments/comp.patch) (application/octet-stream, 5.8 KB)
- [mac_additional_archives.patch](attachments/mac_additional_archives.patch) (application/octet-stream, 2.3 KB)

## Timeline

### np...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-04-06)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-04-19)

Attaching patch

### ya...@nightwatchcybersecurity.com (2016-04-22)

Better POC here:
https://theowl.xyz/cr/600907/test.as
https://theowl.xyz/cr/600907/test.cpgz
https://theowl.xyz/cr/600907/test.pax
https://theowl.xyz/cr/600907/test.xip

For the XIP case only, we observed Gatekeeper showing a warning, not for the rest.

Use case would be malware packaged inside one of these files, user downloads, double clicks, and double clicks.

### va...@chromium.org (2016-05-06)

[Empty comment from Monorail migration]

### ya...@nightwatchcybersecurity.com (2016-05-13)

Just wondering if this issue is still being looked at

### ya...@nightwatchcybersecurity.com (2016-05-29)

@vakh - we are attaching a patch for the new dynamic file type system

### va...@chromium.org (2016-06-03)

Thanks for the report and the patch. I'm looking into it and should have an update in the next 1-2 days.

### ya...@nightwatchcybersecurity.com (2016-06-03)

Thank you

### va...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-06-09)

I can confirm the following behavior:
.AS  : REASON_NOT_BINARY_FILE, (Could have been .gz)
.CPGZ: REASON_NOT_BINARY_FILE, (Could have been .gz)
.PAX : REASON_NOT_BINARY_FILE, (Could have been .zip) 
.XIP : REASON_NOT_BINARY_FILE, (Could have been .zip)

It looks like .PAX is working as intended and is being checked.

nparker: can you please take a look and fix?

### va...@chromium.org (2016-06-09)

> It looks like .PAX is working as intended and is being checked.
Please ignore this statement from my previous comment.

### np...@chromium.org (2016-06-09)

vakh -- Did we confirm these types are automatically opened/unpacked?

### va...@chromium.org (2016-06-09)

> vakh -- Did we confirm these types are automatically opened/unpacked?
Yes, I did that.

### bu...@chromium.org (2016-06-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8e11fd0f247034347d72abd6b8c29cfec6074b16

commit 8e11fd0f247034347d72abd6b8c29cfec6074b16
Author: nparker <nparker@chromium.org>
Date: Fri Jun 10 16:47:12 2016

Add additional compressed formats for Mac OS

R=vakh
BUG=600907
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2051213003
Cr-Commit-Position: refs/heads/master@{#399208}

[modify] https://crrev.com/8e11fd0f247034347d72abd6b8c29cfec6074b16/chrome/browser/resources/safe_browsing/download_file_types.asciipb
[modify] https://crrev.com/8e11fd0f247034347d72abd6b8c29cfec6074b16/tools/metrics/histograms/histograms.xml


### np...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-06-10)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8e11fd0f247034347d72abd6b8c29cfec6074b16

commit 8e11fd0f247034347d72abd6b8c29cfec6074b16
Author: nparker <nparker@chromium.org>
Date: Fri Jun 10 16:47:12 2016

Add additional compressed formats for Mac OS

R=vakh
BUG=600907
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2051213003
Cr-Commit-Position: refs/heads/master@{#399208}

[modify] https://crrev.com/8e11fd0f247034347d72abd6b8c29cfec6074b16/chrome/browser/resources/safe_browsing/download_file_types.asciipb
[modify] https://crrev.com/8e11fd0f247034347d72abd6b8c29cfec6074b16/tools/metrics/histograms/histograms.xml


### va...@chromium.org (2016-06-15)

I'm happy to announce that the panel decide to award $2000 for this report.

research@nightwatchcybersecurity.com: Thank you for the report! I've set the wheels in motion for you to get the reward.

### bu...@chromium.org (2016-06-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/e5a6877b2df8b2cc36e959285e095df410e734cf

commit e5a6877b2df8b2cc36e959285e095df410e734cf
Author: nparker <nparker@chromium.org>
Date: Wed Jun 15 17:58:28 2016

Increment download_file_types version since I missed it before

I missed this in https://codereview.chromium.org/2051213003 and hence
it wont get pushed till I land+push this.

R=jialiul
BUG=600907
CQ_INCLUDE_TRYBOTS=tryserver.chromium.linux:closure_compilation

Review-Url: https://codereview.chromium.org/2067263002
Cr-Commit-Position: refs/heads/master@{#399950}

[modify] https://crrev.com/e5a6877b2df8b2cc36e959285e095df410e734cf/chrome/browser/resources/safe_browsing/download_file_types.asciipb


### ya...@nightwatchcybersecurity.com (2016-06-16)

thank you

### ya...@nightwatchcybersecurity.com (2016-06-23)

We haven't heard from anyone regarding the reward

### ti...@google.com (2016-06-23)

Thanks for letting us know - I'll chase this up. Feel free to email me directly at timwillis@ if you haven't seen emails relating to this payment by mid-next week.

### va...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### va...@chromium.org (2016-06-23)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-01)

[Empty comment from Monorail migration]

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

This issue was migrated from crbug.com/chromium/600907?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, Services>Safebrowsing>VRP]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41247663)*
