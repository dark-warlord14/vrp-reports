# Security: Bypass Spoofing download domain Chrome Windows 

| Field | Value |
|-------|-------|
| **Issue ID** | [40066578](https://issues.chromium.org/issues/40066578) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | fe...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2023-06-28 |
| **Bounty** | $1,000.00 |

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

I refer to this report for inspiration:  

<https://bugs.chromium.org/p/chromium/issues/detail?id=1238944>

Where I developed to download files using the redirect function symbol @ which caused a lot of download history to be closed from the original domain and only the prefix domain was visible.

**REPRODUCTION CASE** :

1. Open <https://huntertoday18.000webhostapp.com/spoofdown.html>
2. Click the link
3. Wait until download, and check the download link leads to <https://google.com@@@@@@@@@@@@@@@@@@@@@@@@@domain> download origin.

I have done testing on other browsers and found the best way to mitigate this vulnerability is done by firefox, which will display a warning to reassure the user with a confirmation warning as below:

```
You are about to log in to the site “download.virtualbox.org” with the username “google%2Ecom%40%40%40%40%40%40%40%40%40%40%40%40%40% 40%40%40%40%…”, but the website does not require authentication. This may be an attempt to trick you.  
  
Is “download.virtualbox.org” the site you want to visit?  

```

Affected version:  

Version 114.0.5735.199 (Official Build) (64-bit)

OS: Windows 11

**VERSION**  

Chrome Version: Version 114.0.5735.199 (Official Build) (64-bit)  

Operating System: Windows 11

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Om Apip

## Attachments

- [video1305727251.mp4](attachments/video1305727251.mp4) (video/mp4, 4.7 MB)
- [Poc-n.html](attachments/Poc-n.html) (text/plain, 5.9 KB)
- [firefox_POC.mp4](attachments/firefox_POC.mp4) (video/mp4, 1.7 MB)

## Timeline

### [Deleted User] (2023-06-28)

[Empty comment from Monorail migration]

### es...@chromium.org (2023-06-29)

Thanks for the report.

I'm tentatively marking this as Medium severity based on https://crbug.com/chromium/1281972, though I probably would have rated this Low because the chrome://downloads surface is relatively buried and I'm not sure we even consider the URLs on that page as security surfaces. Nevertheless, this seems worth fixing.

chlily@, does your team own chrome://downloads now, or would that be another team? Feel free to unassign yourself if n/a for your team. Thanks!

[Monorail components: UI>Browser>Downloads]

### [Deleted User] (2023-06-29)

[Empty comment from Monorail migration]

### ch...@chromium.org (2023-06-29)

Am I understanding correctly that this should be resolved by omitting the username/password parts of the URL and showing the domain name starting from the right side (eliding subdomains)?

### fe...@gmail.com (2023-06-29)

It should be very helpful, you can see the POC below if the url https://huntertoday18.000webhostapp.com/spoofdown.html is executed in Firefox, an alert will appear.
In addition, maybe you can also make the download url readable, the parent domain shouldn't need text in front of @ like google.com@, it should just be the main domain.

@chlily@chromium.org 





### [Deleted User] (2023-06-30)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-13)

chlily: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-07-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fe...@gmail.com (2023-07-26)

any update on this?

### fe...@gmail.com (2023-08-08)

any update on this?

### es...@chromium.org (2023-08-08)

[Empty comment from Monorail migration]

### za...@google.com (2023-08-10)

Hey chlily@ can you please update the status of this bug? Thanks! 

### ch...@chromium.org (2023-08-10)

Yep, am working on it. Should have a patch ready soon.

### ch...@chromium.org (2023-08-15)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-16)

[Empty comment from Monorail migration]

### fe...@gmail.com (2023-08-18)

any update on this?

### dp...@chromium.org (2023-08-18)

Candidate fix at https://chromium-review.googlesource.com/c/chromium/src/+/4775841.

### gi...@appspot.gserviceaccount.com (2023-08-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331

commit 7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331
Author: Lily Chen <chlily@chromium.org>
Date: Fri Aug 25 15:49:26 2023

[Downloads] Format and simplify/truncate URLs on chrome://downloads page

This tweaks the behavior of chrome://downloads items' displayed URLs
in several ways:

1. Sends a formatted display version of the URL from the browser, in
   particular with IDNs properly displayed in Unicode and extraneous
   portions of the URL omitted, which previously could be used to
   mislead the user, e.g. by making the actual hostname not visible
   (using a very long user/password).
3. Refuses to link displayed URLs if they were truncated due to the mojo
   message size limit (c.f. crbug.com/1070451). Such truncated URLs
   won't work properly anyway, so there is no point in linking them.

Screencasts and demo page:
https://drive.google.com/drive/folders/1b_HO0Knzm7yJAFLTVbKFCR2ARCZ916LM

Observe in screencasts:
1st link - Before: User can be misled by fake domain name in username.
           After:  The user/pass components are omitted.
2nd link - Before: The long data URL is clickable in chrome://downloads
                   despite having been truncated for being > 2 MB.
           After:  The long data URL is not clickable.
3rd link - Before: IDN is displayed in unreadable punycode.
           After:  IDN is displayed in readable characters.

Bug: 1458934
Change-Id: I0e38cdeb40b34aab7b534ebc213e3ff98829fed5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4775841
Reviewed-by: Demetrios Papadopoulos <dpapad@chromium.org>
Reviewed-by: Joe Mason <joenotcharles@google.com>
Reviewed-by: Xinghui Lu <xinghuilu@chromium.org>
Commit-Queue: Lily Chen <chlily@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1188357}

[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/test/data/webui/js/mojo_type_util_test.ts
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/ui/webui/downloads/downloads_list_tracker_unittest.cc
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/resources/downloads/item.ts
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/ui/webui/downloads/BUILD.gn
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/test/data/webui/downloads/test_support.ts
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/test/data/webui/downloads/manager_test.ts
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/ui/webui/downloads/downloads.mojom
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/ui/webui/resources/js/mojo_type_util.ts
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/resources/downloads/item.html
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/test/data/webui/downloads/BUILD.gn
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/ui/webui/downloads/downloads_list_tracker.h
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/browser/ui/webui/downloads/downloads_list_tracker.cc
[modify] https://crrev.com/7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331/chrome/test/data/webui/downloads/item_test.ts


### ch...@chromium.org (2023-08-26)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-27)

[Empty comment from Monorail migration]

### fe...@gmail.com (2023-08-29)

i have tested and the bug is patched, thanks for the patch.

### fe...@gmail.com (2023-09-11)

Hi team,

Any update on this? 

### am...@chromium.org (2023-09-11)

Thanks for reaching out. There was just recently a two-week hiatus of VRP Panel sessions. This bug is in the queue and will certainly be evaluated at a future VRP Panel session. 

### am...@google.com (2023-09-14)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-09-14)

Thank you for the report Om! The Chrome VRP Panel has decided to award you $1,000 for this report and your efforts as we were able to make a security beneficial change. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-09-17)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-09)

[Empty comment from Monorail migration]

### fe...@gmail.com (2023-10-11)

Hi team, the vulnerability has been patched and the latest version released, but it seems I have not received payment

### am...@chromium.org (2023-10-11)

Hello, as per https://crbug.com/chromium/1458934#c28, reward information was sent to finance for processing on 16 September. Since this is your first reward from a VRP within Google, you must first be enrolled in the Google payment system. As per finance, you were sent an invitation to enroll in 18 September. Please ensure you have responded to that enrollment request. If so, please send questions about payment status to p2p-vrp@google.com, this is the finance team who processes VRP payment and will be able to help you. 

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-25)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-27)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-27)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gm...@google.com (2023-10-27)

[Empty comment from Monorail migration]

### vo...@google.com (2023-10-30)

1. one https://crrev.com/c/4978246
2. Low - simple conflicts in tests
3. Landed to M118, not merged anywhere else
4. Yes

### gi...@appspot.gserviceaccount.com (2023-10-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe

commit 49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe
Author: Zakhar Voit <voit@google.com>
Date: Mon Oct 30 11:52:44 2023

[M114-LTS][Downloads] Format and simplify/truncate URLs on chrome://downloads page

This tweaks the behavior of chrome://downloads items' displayed URLs
in several ways:

1. Sends a formatted display version of the URL from the browser, in
   particular with IDNs properly displayed in Unicode and extraneous
   portions of the URL omitted, which previously could be used to
   mislead the user, e.g. by making the actual hostname not visible
   (using a very long user/password).
3. Refuses to link displayed URLs if they were truncated due to the mojo
   message size limit (c.f. crbug.com/1070451). Such truncated URLs
   won't work properly anyway, so there is no point in linking them.

Screencasts and demo page:
https://drive.google.com/drive/folders/1b_HO0Knzm7yJAFLTVbKFCR2ARCZ916LM

Observe in screencasts:
1st link - Before: User can be misled by fake domain name in username.
           After:  The user/pass components are omitted.
2nd link - Before: The long data URL is clickable in chrome://downloads
                   despite having been truncated for being > 2 MB.
           After:  The long data URL is not clickable.
3rd link - Before: IDN is displayed in unreadable punycode.
           After:  IDN is displayed in readable characters.

(cherry picked from commit 7a1e2fc5492bd5f7f06bb8583c460f5ed2a2b331)

Bug: 1458934
Change-Id: I0e38cdeb40b34aab7b534ebc213e3ff98829fed5
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4775841
Commit-Queue: Lily Chen <chlily@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1188357}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4978246
Commit-Queue: Oleh Lamzin <lamzin@google.com>
Owners-Override: Oleh Lamzin <lamzin@google.com>
Auto-Submit: Zakhar Voit <voit@google.com>
Reviewed-by: Oleh Lamzin <lamzin@google.com>
Reviewed-by: Achuith Bhandarkar <achuith@chromium.org>
Cr-Commit-Position: refs/branch-heads/5735@{#1628}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/ui/webui/resources/js/BUILD.gn
[add] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/test/data/webui/js/mojo_type_util_test.ts
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/ui/webui/downloads/downloads_list_tracker_unittest.cc
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/resources/downloads/item.ts
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/ui/webui/downloads/BUILD.gn
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/test/data/webui/downloads/test_support.ts
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/test/data/webui/downloads/manager_test.ts
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/ui/webui/downloads/downloads.mojom
[add] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/ui/webui/resources/js/mojo_type_util.ts
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/resources/downloads/item.html
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/test/data/webui/downloads/BUILD.gn
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/ui/webui/downloads/downloads_list_tracker.h
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/browser/ui/webui/downloads/downloads_list_tracker.cc
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/test/data/webui/downloads/item_test.ts
[modify] https://crrev.com/49401d4cf72c813f6f2bdc3ef671d6456a4e3ebe/chrome/test/data/webui/js/BUILD.gn


### vo...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1458934?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40066578)*
