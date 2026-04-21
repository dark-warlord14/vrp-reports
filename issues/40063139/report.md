# Security: Safe Browsing bypass via data URI, no warning if SB fails

| Field | Value |
|-------|-------|
| **Issue ID** | [40063139](https://issues.chromium.org/issues/40063139) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Unknown |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ym...@ym.kim |
| **Assignee** | dr...@chromium.org |
| **Created** | 2023-02-17 |
| **Bounty** | $3,000.00 |

## Description

Note the issue was originally reported in <https://crbug.com/1416794#c8>, but as the issue was closed as WontFix, I'm resubmitting the issue in case it gets missed. This report reports two vulnerabilties:

1. Download Protection Service does not shorten URL in referrer chains
2. Even if the danger type was DOWNLOAD\_DANGER\_TYPE\_MAYBE\_DANGEROUS\_CONTENT, if Safe Browsing check fails, no warning is shown to the user

**VULNERABILITY DETAILS**

1. Safe Browsing (<https://sb-ssl.google.com/safebrowsing/clientreport/download>) fails with 413 (Payload Too Large), if the body exceed about 20MB.

AddEventUrlToReferrerChain[1] does not shorten data URIs in the URL and server redirect chain, so the download check can be bypassed if the data URI exceeds ~8MB.

PPAPIDownloadRequest[2] may also be vulnerable, but I'm not sure whether the requestor origin can be a data URI.

As mentioned in the original issue, this is actively exploited in the wild, not sure intended or not, as downloader trojans use data URIs to bypass the domain check.

Please find attached the suggested patch.

2. Even if the danger type was DOWNLOAD\_DANGER\_TYPE\_MAYBE\_DANGEROUS\_CONTENT, if Safe Browsing check is not perfomed or failed, the DownloadCheckResult is set to UNKNOWN[3] and the danger type is reset to DOWNLOAD\_DANGER\_TYPE\_NOT\_DANGEROUS[4]. As a result, no warning is shown to the user, and this may give the user a false sense of security and inconsistent experience.

If the result is unknown for any other reasons Safe Browsing actually reporting unknown, the download should be treated as dangerous as if the Safe Browsing is disabled[5] or at least uncommon.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/download_protection/download_protection_service.cc;l=72-84;drc=f37b11fe3cfd8d5f8294ef27d5c6c723a4028d89>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc;l=197;drc=f37b11fe3cfd8d5f8294ef27d5c6c723a4028d89>  

[3] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/safe_browsing/download_protection/check_client_download_request_base.cc;l=478;drc=f37b11fe3cfd8d5f8294ef27d5c6c723a4028d89>  

[4] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/chrome_download_manager_delegate.cc;l=1298;drc=f37b11fe3cfd8d5f8294ef27d5c6c723a4028d89>  

[5] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/download/chrome_download_manager_delegate.cc;l=696;drc=f37b11fe3cfd8d5f8294ef27d5c6c723a4028d89>

**VERSION**  

Chrome Version: 110.0.5481.100 stable  

Operating System: Windows 11 21H2

**REPRODUCTION CASE**

1. Enable Safe Browsing in chrome://settings/security.
2. Open chrome://safe-browsing/#tab-download-protection.
3. Serve the attached poc.html over HTTP and navigate to the page.
4. Click "7MB" and check the Download response (ClientDownloadResponse) is received.
5. Click "8MB" and check the Download response (ClientDownloadResponse) is not received.
6. Check the warning, e.g., "This type of file can harm your computer", is not shown.

**CREDIT INFORMATION**  

Reporter credit: Young Min Kim (@ylemkimon), CompSec Lab at Seoul National University

## Attachments

- [poc.html](attachments/poc.html) (text/plain, 375 B)
- [suggested.patch](attachments/suggested.patch) (text/plain, 1.6 KB)
- [big-debug.asm](attachments/big-debug.asm) (text/plain, 5.1 KB)
- [big-debug.zip](attachments/big-debug.zip) (application/octet-stream, 23.3 KB)

## Timeline

### [Deleted User] (2023-02-17)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-18)

[Empty comment from Monorail migration]

### th...@chromium.org (2023-02-18)

Thanks for the report! I'm able to reproduce the 8 MB version having a ClientDownloadResponse while the 7 MB version does not. I can also see that the SBClientDownload.CheckDownloadStats histogram has a value of 10 for the 7 MB one ("safe") while the 8 MB version has a value of 5 ("server ping failed"). I think we should be able to simulate what happens for an unsafe download (rather than a safe one) with a local build, temporarily modifying the verdict to unsafe. 

drubery@: Could you PTAL to see if this is able to bypass the ping for unsafe downloads?

Setting severity medium since this is somewhat similar to "A bug that allows arbitrary pages to bypass security interstitials" though I could be convinced this should be higher since it's a download, not an interstitial.

[Monorail components: Services>Safebrowsing]

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### [Deleted User] (2023-02-18)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-18)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-02-18)

[Empty comment from Monorail migration]

### ym...@ym.kim (2023-02-25)

There seem to be more ways to make the request larger than 20 MB. Please let me know if they need separate issues to be filed.

3. BinaryFeatureExtractor does not truncate debug data over 20 MB.

VULNERABILITY DETAILS
3. BinaryFeatureExtractor attaches the whole debug data (IMAGE_DEBUG_DIRECTORY) in ClientDownloadRequest[1], but does not truncate even if it exceeds 20 MB.

Since the debugging information does not affect the execution, the attacker can easily pad IMAGE_DEBUG_DIRECTORY with dummy data and bypass safe browsing check.

[1] https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/safe_browsing/binary_feature_extractor_win.cc;l=166;drc=856552dde046dcfc782793484b5f4af4743552a1

REPRODUCTION CASE
1. Enable Safe Browsing in chrome://settings/security.
2. Open chrome://safe-browsing/#tab-download-protection.
3. Download big-debug.exe (included in big-debug.zip or assembled via `nasm -f bin -o big-debug.exe big-debug.asm`) over HTTP.
4. Check the Download response (ClientDownloadResponse) is not received.
5. Check the warning, e.g., "This type of file can harm your computer", is not shown.

### [Deleted User] (2023-03-04)

drubery: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### dr...@chromium.org (2023-03-06)

Thanks for the details! https://chromium-review.googlesource.com/c/chromium/src/+/4303145 deals with data:// URLs in the referrer chain. I'll fix the others on this bug.

### gi...@appspot.gserviceaccount.com (2023-03-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/1ed1dd3a1bf3e808449466373b27b745a2ba694d

commit 1ed1dd3a1bf3e808449466373b27b745a2ba694d
Author: Daniel Rubery <drubery@chromium.org>
Date: Tue Mar 07 02:04:15 2023

Limit ability for downloads to generate large ClientDownloadRequests

This can leads to timeouts in the network stack or the server rejecting
the request.

Bug: 1417325
Change-Id: Ia159e9ba9235ff30ff29be2aa142c670336f5f5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4311341
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1113729}

[modify] https://crrev.com/1ed1dd3a1bf3e808449466373b27b745a2ba694d/chrome/common/safe_browsing/binary_feature_extractor_win.cc
[modify] https://crrev.com/1ed1dd3a1bf3e808449466373b27b745a2ba694d/chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc
[modify] https://crrev.com/1ed1dd3a1bf3e808449466373b27b745a2ba694d/tools/metrics/histograms/metadata/sb_client/histograms.xml


### dr...@chromium.org (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-10)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-13)

The bot skipped this one as it does with some medium severity issues; since this fix was landed on 113, lets go ahead and merge this back to at least 112/Beta. 
Please let me know if there are any concerns with backmerging this. 

### dr...@chromium.org (2023-03-13)

There is one relevant CL not on this bug: https://chromium-review.googlesource.com/c/chromium/src/+/4303145. I assume the merge approval is for that one as well?

### am...@chromium.org (2023-03-14)

yes, thank you for checking! Sorry, I forgot to complete my thought on https://crbug.com/chromium/1417325#c15, please merge the CL in https://crbug.com/chromium/1417325#c11 and https://chromium-review.googlesource.com/c/chromium/src/+/4303145 (in https://crbug.com/chromium/1417325#c10) to M112 / branch 5615 at your earliest convenience. 

### sr...@google.com (2023-03-14)

This issue has been approved for a merge to M112, I am cutting Beta RC build for M112 today afternoon around 3pm PST, please help complete all the merges to M112 today asap so the changes can be included into beta release and can get more beta channel coverage.

### dr...@chromium.org (2023-03-14)

Merges https://crrev.com/c/4335531 and https://crrev.com/c/4336430 are in the process of landing now. They should definitely be done by 3 pm PST.

### gi...@appspot.gserviceaccount.com (2023-03-14)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/0e1618d677c04cc766a57efc34e910b5aeda2cf1

commit 0e1618d677c04cc766a57efc34e910b5aeda2cf1
Author: Daniel Rubery <drubery@chromium.org>
Date: Tue Mar 14 18:02:50 2023

[M112] Limit ability for downloads to generate large ClientDownloadRequests

This can leads to timeouts in the network stack or the server rejecting
the request.

(cherry picked from commit 1ed1dd3a1bf3e808449466373b27b745a2ba694d)

Bug: 1417325
Change-Id: Ia159e9ba9235ff30ff29be2aa142c670336f5f5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4311341
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1113729}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4335531
Cr-Commit-Position: refs/branch-heads/5615@{#483}
Cr-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}

[modify] https://crrev.com/0e1618d677c04cc766a57efc34e910b5aeda2cf1/chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc
[modify] https://crrev.com/0e1618d677c04cc766a57efc34e910b5aeda2cf1/chrome/common/safe_browsing/binary_feature_extractor_win.cc
[modify] https://crrev.com/0e1618d677c04cc766a57efc34e910b5aeda2cf1/tools/metrics/histograms/metadata/sb_client/histograms.xml


### am...@google.com (2023-03-17)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-03-17)

Congratulations and great find, Young Min Kim! The VRP panel has decided to award you $3,000 for this report. Thank you for your efforts in discovering and reporting this issue to us -- excellent work! 

### am...@google.com (2023-03-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2023-03-31)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### pg...@google.com (2023-04-04)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-16)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-07-06)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### vo...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### [Deleted User] (2023-07-13)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### vo...@google.com (2023-07-13)

1. https://crrev.com/c/4680623
2. Low - small change, no conflicts
3. M112
4. Yes

### gm...@google.com (2023-07-13)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-07-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b6c7df41274534b9dfa4f959e0d87cd3483d43d1

commit b6c7df41274534b9dfa4f959e0d87cd3483d43d1
Author: Daniel Rubery <drubery@chromium.org>
Date: Mon Jul 17 02:27:55 2023

[M108-LTS] Limit ability for downloads to generate large ClientDownloadRequests

This can leads to timeouts in the network stack or the server rejecting
the request.

(cherry picked from commit 1ed1dd3a1bf3e808449466373b27b745a2ba694d)

(cherry picked from commit 0e1618d677c04cc766a57efc34e910b5aeda2cf1)

Bug: 1417325
Change-Id: Ia159e9ba9235ff30ff29be2aa142c670336f5f5d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4311341
Commit-Queue: Daniel Rubery <drubery@chromium.org>
Cr-Original-Original-Commit-Position: refs/heads/main@{#1113729}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4335531
Cr-Original-Commit-Position: refs/branch-heads/5615@{#483}
Cr-Original-Branched-From: 9c6408ef696e83a9936b82bbead3d41c93c82ee4-refs/heads/main@{#1109224}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4680623
Owners-Override: Simon Hangl <simonha@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Simon Hangl <simonha@google.com>
Reviewed-by: Victor-Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/5359@{#1492}
Cr-Branched-From: 27d3765d341b09369006d030f83f582a29eb57ae-refs/heads/main@{#1058933}

[modify] https://crrev.com/b6c7df41274534b9dfa4f959e0d87cd3483d43d1/chrome/common/safe_browsing/binary_feature_extractor_win.cc
[modify] https://crrev.com/b6c7df41274534b9dfa4f959e0d87cd3483d43d1/chrome/browser/safe_browsing/download_protection/ppapi_download_request.cc
[modify] https://crrev.com/b6c7df41274534b9dfa4f959e0d87cd3483d43d1/tools/metrics/histograms/metadata/sb_client/histograms.xml


### vo...@google.com (2023-07-17)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1417325?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/1416794]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063139)*
