# Diagcab file extension is not blocklisted to prevent users from downloading harmful files

| Field | Value |
|-------|-------|
| **Issue ID** | [40059843](https://issues.chromium.org/issues/40059843) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Windows |
| **Reporter** | j0...@gmail.com |
| **Assignee** | dr...@chromium.org |
| **Created** | 2022-06-03 |
| **Bounty** | $1,000.00 |

## Description

**Steps to reproduce the problem:**

1. Create a diagcab file
2. Download it from Chrome or Edge
3. The file is successfully downloaded without warnings

**Problem Description:**  

With the hype of #Follina, i've been testing for other bugs on Microsoft Support Diagnostics Tool. Some days ago, I found an interesting 2-clicks RCE which exploits a path traversal bug on MSDT which is yet 0day. This bug has publicly been known since 2020 [1]. MS decided closing the case as "wontfix". Today i've been able to perform further testing and have discovered that this file extension (diagcab) is not flagged by chromium-based downloader. It's actually one-click RCE for chromium-based browsers since it's just needed to click on the dialog shown once the file download is completed [2].

There is a public POC in the wild [3].

I think these extensions should be blocked since msdt has become an interesting target right now.

[1] <https://irsl.medium.com/the-trouble-with-microsofts-troubleshooters-6e32fc80b8bd>  

[2] <https://twitter.com/j00sean/status/1532416426702786560>  

[3] <https://github.com/irsl/microsoft-diagcab-rce-poc>

**Additional Comments:**

\*\*Chrome version: \*\* 102.0.0.0 \*\*Channel: \*\* Stable

**OS:** Windows

## Attachments

- [path-traversal-diagcab-gmail.png](attachments/path-traversal-diagcab-gmail.png) (image/png, 30.8 KB)
- [dogwalk-stable-chrome-diagcab-still-no-fix.png](attachments/dogwalk-stable-chrome-diagcab-still-no-fix.png) (image/png, 52.7 KB)
- [dogwalk-stable-chrome-diagcab-warning.png](attachments/dogwalk-stable-chrome-diagcab-warning.png) (image/png, 51.5 KB)

## Timeline

### j0...@gmail.com (2022-06-03)

There's a video in the twitter thread btw.

### j0...@gmail.com (2022-06-03)

Interestingly, as expected, this is not flagged by gmail neither. You can send diagcab files w/o issues over there.

### dt...@chromium.org (2022-06-06)

[Empty comment from Monorail migration]

[Monorail components: Services>Safebrowsing UI>Browser>Downloads]

### fl...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-06-09)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-06-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/cd290e7cbed7b2f95e4c2dc805e9d175f9161fc4

commit cd290e7cbed7b2f95e4c2dc805e9d175f9161fc4
Author: Daniel Rubery <drubery@chromium.org>
Date: Thu Jun 09 19:02:02 2022

Add download_file_types.asciipb entry for DIAGCAB

This file is an executable component of the Windows troubleshooting
platform, so we should treat it like an executable.

Bug: 1332392
Change-Id: Iebdff06d72db74a679c93cec97fb636bb2fb66e6
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3698763
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Reviewed-by: Rohit Bhatia <bhatiarohit@google.com>
Cr-Commit-Position: refs/heads/main@{#1012642}

[modify] https://crrev.com/cd290e7cbed7b2f95e4c2dc805e9d175f9161fc4/components/safe_browsing/content/resources/download_file_types.asciipb
[modify] https://crrev.com/cd290e7cbed7b2f95e4c2dc805e9d175f9161fc4/components/safe_browsing/content/resources/download_file_types_experiment.asciipb
[modify] https://crrev.com/cd290e7cbed7b2f95e4c2dc805e9d175f9161fc4/tools/metrics/histograms/enums.xml


### am...@chromium.org (2022-06-14)

Due to an issue with the monorail wizard workflow, this issue was not originally labeled as a security bug and, therefore, this issue did not make it to the security team bug queue for triage. This wizard workflow issue was just discovered today, so updating now accordingly. 

drubery@ -- since you are owner and also security team, can you please add relevant security labels for this one and provide some after the fact sheriffing? Thank you! 

### dr...@chromium.org (2022-06-14)

Ah, sorry I didn't notice this wasn't restricted! I've added the appropriate labels.

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-14)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-14)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2022-06-14)

[Empty comment from Monorail migration]

### dr...@chromium.org (2022-06-14)

Fixed. No merges necessary because we can push file type policy updates by component updater (which I've done).

### [Deleted User] (2022-06-14)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

[Empty comment from Monorail migration]

### [Deleted User] (2022-06-15)

Requesting merge to beta M103 because latest trunk commit (1012642) appears to be after beta branch point (1002911).

Not requesting merge to dev (M104) because latest trunk commit (1012642) appears to be prior to dev branch point (1012729). If this is incorrect, please replace the Merge-NA-104 label with Merge-Request-104. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-06-15)

Merge review required: M103 has already been cut for stable release.

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
Owners: govind (Android), harrysouders (iOS), dgagnon (ChromeOS), pbommana (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2022-06-15)

No thanks sheriffbot. File type policies are pushed by component update, so all Chrome users already have the change.

### j0...@gmail.com (2022-07-04)

When is this planned to be released in stable channel?
I've just noticed Edge has recently applied the patch so i wonder whether there is issued some CVE id, or not yet.

Thanks,
j00sean.

### er...@microsoft.com (2022-07-06)

Re #22: Chrome's file type danger list is served via a Component, so it's already updated in Stable Chrome. 

Without the updater, Commit cd290e7c... initially landed in 104.0.5112.0.

### j0...@gmail.com (2022-07-06)

Re #23: Sorry to disagree but I don't see that in the latest stable chrome (103.0.5060.114).
https://chromereleases.googleblog.com/2022/07/stable-channel-update-for-desktop.html

What about the CVE?

### er...@microsoft.com (2022-07-06)

Re #24: Go to chrome://components and look at what File Type Policies version you have. Check for updates?

### am...@chromium.org (2022-07-06)

The fix commit (cd290e7cbed7b2f95e4c2dc805e9d175f9161fc4) specifically on this bug does not appear to have made it to 103 and has only been merged back as far as to 104. Security bug discoveries from externally reported issues are acknowledged in security fix notes on the release blog and receive CVE IDs at the time the fix for that issue ships in the a Stable channel release of Chrome. This fix should ship in M104 Stable channel release, which is currently planned on 2 August.

### j0...@gmail.com (2022-07-06)

It's ok, thanks for the clarification. A bit late, IMHO, since this is publicly known. Thanks any way!
Re #25: It was version 51, updates checked.

### dr...@chromium.org (2022-07-06)

Version 51 is expected. It can be tricky to test these file type policy changes, since Safe Browsing verdicts frequently override them. I would do the following:
- Start Chrome with a clean user data directory (we check browsing history for the ALLOW_ON_USER_GESTURE danger level)
- Disable Safe Browsing (temporarily please)
- Download the file.

That shows a warning for me.

### j0...@gmail.com (2022-07-06)

Same result :-)

### dr...@chromium.org (2022-07-06)

Excellent. Sounds like this is all WAI then.

### j0...@gmail.com (2022-07-07)

👌

### am...@google.com (2022-07-28)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-07-28)

Congratulations! The VRP Panel has decided to award you $1,000 for this report. Please let us know what name/handle/other identifier you would like us to use in acknowledging you for this issue. Thank you for your efforts and reporting this issue to us. 



### j0...@gmail.com (2022-07-29)

c32: This line "Please be honest if you have already disclosed anything publicly or to third parties" in the boilerplate reminder makes me in fact to have to be honest and remember you how this bug report begins, this stuff was publicly disclosed by Imre Rad (@ImreRad), more than 2 yrs ago and by me some weeks/months ago and is publicly known as DogWalk vulnerability.
I know this bug has been fixed not only because of #DogWalk, but because diagcab files are actually executable files (due to their nature). If it exists an exploit in a PDF Reader installed by default, that doesn't mean PDF files have to be considered malicious files, so a vulnerability doesn't make a file extension being marked as unsafe to download. However the diagcab files main issue was also publicly disclosed recently by Rich Warren (@buffaloverflow) [1] and by another researchers a long time ago [2], 6 years to be precise, and in turn, was used by threat actors around that date.
So i'm not sure whether or not this deserves a bounty but just let's lays the cards on the table :-)

c33: Regarding credits, let me coordinate it with the other folks implied on this, basically the researchers who were mentioned above.

[1] https://twitter.com/buffaloverflow/status/1534813580801069057
[2] https://www.proofpoint.com/uk/threat-insight/post/windows-troubleshooting-platform-leveraged-deliver-malware

### am...@google.com (2022-07-29)

[Empty comment from Monorail migration]

### j0...@gmail.com (2022-08-01)

If the reward process continues...Please, CC Imre Rad who's the researcher who initially found this behavior and is going to be the person who's going to reclaim the reward. On this case i'm just a bug report writer or bug re-discoverer :-)

### j0...@gmail.com (2022-08-01)

[Comment Deleted]

### am...@chromium.org (2022-08-01)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-01)

Hi, thank you for being forthcoming about the source of this discovery. We did already know about the existing windows POC on twitter as that was reported by Microsoft after just after your report. In our opinion, you took the time to see if see if this file extension was allowed Chrome downloads and took the time to report it to us and this reward belongs to you. 
Please let me know what name/handle/tag you would like us to use in acknowledging you for this issue in our security fix notes being published tomorrow for this release. Also, if you would like us to include others (with their consent - of course) I am happy to do that as well. 

### am...@google.com (2022-08-02)

[Empty comment from Monorail migration]

### j0...@gmail.com (2022-08-02)

Hi,

Yeah i get you. But according my rules this report just uses the same info than posted by Imre, so the bounty belongs to him. He had noticed about this chromium issue, it's not any variant, either i have brought to light any further info about severity, just attack surface, ie, fun with Windows url protocols on htmlfile activex in Word, browsers and Readers. I have a longer explanation but don't want to bore you. Imre and I are agreed, that's the important :-)

Of course, i'm sorry for the delay about credits. I'm just waiting for Rich's consent, i understand i can't use whoever's name without the right permission and didn't get it yet. So given that i'm in touch with Imre and have his consent to credit him, it would be (following disclosure timeline by the way): "Imre Rad (@ImreRad) and @j00sean".

Thank you!

### am...@google.com (2022-08-12)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-08-12)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-20)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1332392?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Services>Safebrowsing, UI>Browser>Downloads]
[Monorail mergedwith: crbug.com/chromium/1332526]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40059843)*
