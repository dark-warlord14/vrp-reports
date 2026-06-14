# Security: Spoofing Download URL wiith Long Domain

| Field | Value |
|-------|-------|
| **Issue ID** | [41487478](https://issues.chromium.org/issues/41487478) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Linux, Mac |
| **Reporter** | fe...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2024-01-01 |
| **Bounty** | $500.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

I refer to the download domain that has been patched by the Chromium team:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1069246>  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1458934>

However, it appears that there is one focal point that can still be exploited by the attacker, where if the attacker provides a long URL as the download domain, unfortunately, Chrome displays the entire domain and if it is long it will be truncated and the core domain cannot be seen like the POC I provided.

In the video, I try to provide a comparison of the handling in implementing the history download domain which is displayed in the download, where Firefox prefers to display the core domain, not the entire domain and it seems that Android Chrome applies it but the desktop does not.

Recommendation:  

Chromium should only display the core domain, when the download occurs not all of it can be cut off.

**VERSION**  

Chrome Version: Version 120.0.6099.130 (Official Build) (64-bit)  

Operating System: Windows 11

**REPRODUCTION CASE**

1. Go to <https://bug.omapip.my.id/download.html>
2. Click button
3. Check the download history and the URL. it will be from "<https://long-domain-tester-accounts-subdo-tester-domain-accounts-google.commm>...", while the original URL is "<https://long-domain-tester-accounts-subdo-tester-domain-accounts-google.commmmmmmmmm.bug.omapip.my.id>"

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Om Apip

## Attachments

- [poc_chrome_long_url_download.mp4](attachments/poc_chrome_long_url_download.mp4) (video/mp4, 11.2 MB)
- [download.html](attachments/download.html) (text/plain, 1.7 KB)

## Timeline

### [Deleted User] (2024-01-01)

[Empty comment from Monorail migration]

### fe...@gmail.com (2024-01-01)

Sorry I forgot to put the title, could you help me make this title on there?
"Spoofing Download URL wiith Long Domain"

Thanks

### ph...@chromium.org (2024-01-02)

[Primary security shepherd]  Thanks for the report and provided context.
I can reproduce on linux and mac.  Assigning the same owner and components as the related https://crbug.com/chromium/1458934.
chlily@: Would you take a look please?

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2024-01-02)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-02)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ph...@chromium.org (2024-01-04)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ch...@chromium.org (2024-01-11)

Should be fixed by crrev.com/c/5170825

GitWatcher didn't pick it up, but here's the CL description:


[Downloads] Elide beginning of display URL on chrome://downloads

To avoid URL spoofs by truncation of very long download URLs, this CL
changes the elision of the display URL on chrome://downloads from
eliding the end to eliding the beginning. Because the eTLD+1 aka
registrable domain of the URL is at the end, we want to always display
that as it is security-relevant.

Note that eliding the beginning may truncate the scheme (http/https) of
the URL. This is acceptable because, due to insecure download warnings,
the user has already been alerted of any insecure (http) downloads, so
the scheme of the download URL is a less important signal.

Screenshots:
https://drive.google.com/drive/folders/1G5ChkHbM82HjFrHPVerzwf4UB1MmQmiZ

Bug: 1514925
Change-Id: I61639cdf4b6682a2ba8961822f22bd7621e8ad13
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5170825
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: Lily Chen <chlily@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1244238}


### ch...@chromium.org (2024-01-11)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-12)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-13)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-14)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-15)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@chromium.org (2024-01-16)

1. Which CLs should be backmerged? (Please include Gerrit links.)

https://chromium-review.googlesource.com/c/chromium/src/+/5170825

2. Has this fix been verified on Canary to not pose any stability regressions?
Yes

3. Does this fix pose any potential non-verifiable stability risks?
No

4. Does this fix pose any known compatibility risks?
No

5. Does it require manual verification by the test team? If so, please describe required testing.
No

### [Deleted User] (2024-01-16)

This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here, so you will need to investigate what - if anything - needs to be merged to M121. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.

Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [121].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2024-01-18)

121 Stable RC has already been cut for next week's release, so we could go without merging this. However, because this fix is sufficiently safe to go ahead and merge, approving for merge to M121. Please go ahead and merge this fix (https://crrev.com/c/5170825) to branch 6167 at your earliest convenience so this fix can be included in the next M121 Stable update. Thank you! 

### gi...@appspot.gserviceaccount.com (2024-01-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/c2e0c0a0808ad1b08717585b355c210a792f08a3

commit c2e0c0a0808ad1b08717585b355c210a792f08a3
Author: Lily Chen <chlily@chromium.org>
Date: Fri Jan 19 15:35:59 2024

[M121][Downloads] Elide beginning of display URL on chrome://downloads

To avoid URL spoofs by truncation of very long download URLs, this CL
changes the elision of the display URL on chrome://downloads from
eliding the end to eliding the beginning. Because the eTLD+1 aka
registrable domain of the URL is at the end, we want to always display
that as it is security-relevant.

Note that eliding the beginning may truncate the scheme (http/https) of
the URL. This is acceptable because, due to insecure download warnings,
the user has already been alerted of any insecure (http) downloads, so
the scheme of the download URL is a less important signal.

Screenshots:
https://drive.google.com/drive/folders/1G5ChkHbM82HjFrHPVerzwf4UB1MmQmiZ

(cherry picked from commit d6a1ebbeb21f52ce6c4f9c7b1ae6770248951e65)

Bug: 1514925
Change-Id: I61639cdf4b6682a2ba8961822f22bd7621e8ad13
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5170825
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Reviewed-by: John Lee <johntlee@chromium.org>
Commit-Queue: Lily Chen <chlily@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1244238}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5213105
Cr-Commit-Position: refs/branch-heads/6167@{#1507}
Cr-Branched-From: 222e786949e76e342d325ea0d008b4b6273f3a89-refs/heads/main@{#1233107}

[modify] https://crrev.com/c2e0c0a0808ad1b08717585b355c210a792f08a3/chrome/browser/ui/webui/downloads/downloads_list_tracker_unittest.cc
[modify] https://crrev.com/c2e0c0a0808ad1b08717585b355c210a792f08a3/chrome/browser/ui/webui/downloads/downloads_list_tracker.cc
[modify] https://crrev.com/c2e0c0a0808ad1b08717585b355c210a792f08a3/chrome/browser/resources/downloads/item.html


### fe...@gmail.com (2024-01-21)

Hi guys, any update for the bounty? 

### pg...@google.com (2024-01-22)

[Empty comment from Monorail migration]

### fe...@gmail.com (2024-01-23)

Hi team, the version chrome has been released but why i haven't seen yet my bounty 

https://chromereleases.googleblog.com/2024/01/stable-channel-update-for-desktop_23.html?m=1

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### pg...@google.com (2024-01-23)

[Empty comment from Monorail migration]

### am...@google.com (2024-01-25)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2024-01-25)

Thank you for your report Om Apip. In assessment of this issue the Chrome VRP Panel has determined that the potential for user harm resulting from this issue is unlikely. We were, however, able to make a beneficial change to Chrome based on your report. As such, we have extended to you a $500 thank you reward. Thank you for your efforts and reporting this issue to us! 

### fe...@gmail.com (2024-01-26)

thanks guys

### am...@google.com (2024-01-27)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-27)

This issue was migrated from crbug.com/chromium/1514925?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1515541]
[Monorail components added to Component Tags custom field.]

### fe...@gmail.com (2024-02-05)

Hi team, it seems my bounty hasn't been sent until now, is there any update? 

### am...@chromium.org (2024-02-05)

Hello, thank you for reaching out. The security team does not handle payments. As per c#29 it appears we sent the reward information to the p2p-vrp finance team for processing on 26 January. Please reach out to p2p-vrp@google.com for assistance. 

### pe...@google.com (2024-04-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41487478)*
