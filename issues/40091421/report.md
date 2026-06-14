# Security: Extension is able to inject script into chrome://newtab/

| Field | Value |
|-------|-------|
| **Issue ID** | [40091421](https://issues.chromium.org/issues/40091421) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions>API |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ka...@chromium.org |
| **Created** | 2018-05-18 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Extensions are able to read and modify the contents of chrome://newtab/ and it's iframes.

**VERSION**  

Chrome Version: 66.0.3359.181 stable  

Operating System: Microsoft Windows 10 Pro 10.0.16299 Build 16299, macOS 10.13.4

**REPRODUCTION CASE**

1. Open Chrome browser.
2. Install the attached extension or Dark Reader extension from the Chrome Web Store.
3. Navigate somewhere (e.g. <https://www.google.com/>).
4. Open new incognito window (Ctrl+Shift+N) or new Guest window.
5. Navigate somewhere (e.g. <https://www.google.com/>).
6. Focus on another application for at least 2 minutes.
7. Focus on initial window.
8. Open new tab, the script is injected there.

## Attachments

- [chrome-newtab-security.zip](attachments/chrome-newtab-security.zip) (application/octet-stream, 3.4 KB)
- [chrome-newtab-contentscript-bug-480p.mov](attachments/chrome-newtab-contentscript-bug-480p.mov) (video/quicktime, 16.8 MB)
- [chrome-newtab-contentscript-bug-720p.mov](attachments/chrome-newtab-contentscript-bug-720p.mov) (video/quicktime, 31.4 MB)
- [scrooge.jpg](attachments/scrooge.jpg) (image/jpeg, 58.8 KB)

## Timeline

### el...@chromium.org (2018-05-18)

This seems to be an exact dupe of https://crbug.com/chromium/842919 which is public.

https://crbug.com/chromium/662610 appears to be a prior version of this which was marked as fixed. In contrast, https://crbug.com/chromium/497807 complains that this doesn't always work. Fixed https://crbug.com/chromium/797461 notes that injection used to be possible in the offline NTP.

Based on the attached POC, this simply appears to take advantage of the fact that when a user is online, the URL chrome://newtab is actually just a virtual URL for the underlying URL https://www.google.com/_/chrome/newtab

[Monorail components: Platform>Extensions>API]

### sh...@gmail.com (2018-05-18)

I've posted the https://crbug.com/chromium/842919 when didn't know how to reproduce it. But after I've found a simple way, I've decided that it's worth the reward.

Since Chrome 61 extensions are not able to inject content scripts into new tab, they should use the Settings Overrides API.

### me...@chromium.org (2018-05-18)

I followed these instructions and I could not reproduce this. 

Do you have a better way to reproduce this?

rdevlin.cronin@ could you please take a look at this, or suggest a better owner?

### sh...@gmail.com (2018-05-18)

Here is a video

### sh...@gmail.com (2018-05-18)

I've re-read the tiers and decided to share a video with higher quality. Also used a clean profile.

### rd...@chromium.org (2018-05-18)

Nifty.

I was able to reproduce this following the steps from #0.  karandeepb@, do you think you can take a look?

### ka...@chromium.org (2018-05-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-05-19)

[Empty comment from Monorail migration]

### ka...@chromium.org (2018-05-25)

Here's a more reliable way to repro this:
- Install the extension from the bug report.
- Ensure google.com is the only opened tab in your browser.
- Open incognito browser and open google.com
- Ensure from command line that no ntp process is open (with flag --instant-process). Kill it if there is any. (This helps ensure that opening the NTP subsequently leads to creation of a new render process). 
- On the non-incognito browser open the NTP.

The check that is responsible for preventing this is in RendererPermissionsPolicyDelegate::IsRestrictedUrl. 

See https://cs.chromium.org/chromium/src/chrome/renderer/extensions/renderer_permissions_policy_delegate.cc?type=cs&sq=package:chromium&g=0&l=36. 

There are two reasons this might fail:
- I *think* that I was able to repro a race b/w setting up the new tab page url in the NTP process (in SearchBouncer) and checking SearchBouncer::IsNewTabPage for content scripts at document_start. Can verify if needed.
- We can actually send the wrong NTP url to the renderer (SearchBouncer). This happens because InstantService listens for content::NOTIFICATION_RENDERER_PROCESS_CREATED notification but it does handle multiple profiles correctly. (This is why this repro's when we have an incognito profile). While sending the NTP url to the renderer, it should check that its Profile matches with the RenderProcessHost's profile. This can possibly lead to other bugs since SearchBouncer::IsNewTabPage can return the wrong result. Will file a bug for this. 

A very easy fix is to check whether the current process is an instant renderer and disallow script injection. Will issue a patch.

### tr...@chromium.org (2018-05-28)

Wow, nice find about the cross-process NTP URL leakage! I'm quite surprised that not more is broken due to this; I guess simultaneous multi-profile usage is just rare.

### bu...@chromium.org (2018-05-30)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8247b125c7b6888dc1c3932e19d6d8fe5a74a460

commit 8247b125c7b6888dc1c3932e19d6d8fe5a74a460
Author: Karan Bhatia <karandeepb@chromium.org>
Date: Wed May 30 22:29:17 2018

Extensions: Prevent content script injection in the New tab Page.

r487664 disallowed content script injection in the New Tab Page. However, the
check in RendererPermissionsPolicyDelegate::IsRestrictedUrl for the same, might
not work due to the following reasons:
  - There might be a race between checking if the extension can inject the
    script and setting the new tab url in the renderer (SearchBouncer).
  - The New Tab page url in the SearchBouncer might be set incorrectly due to
    incorrect handling of multiple profiles by InstantService.

Fix this by checking if the current renderer process is an Instant (NTP)
renderer. This should work since the NTP renderer process should not be shared
with other sites.

BUG=844428, 662610

Change-Id: I45f6b27fb2680d3b8df6e1da223452ffee09b0d8
Reviewed-on: https://chromium-review.googlesource.com/1068607
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Commit-Queue: Karan Bhatia <karandeepb@chromium.org>
Cr-Commit-Position: refs/heads/master@{#563031}
[modify] https://crrev.com/8247b125c7b6888dc1c3932e19d6d8fe5a74a460/chrome/browser/extensions/content_script_apitest.cc
[modify] https://crrev.com/8247b125c7b6888dc1c3932e19d6d8fe5a74a460/chrome/renderer/extensions/renderer_permissions_policy_delegate.cc
[add] https://crrev.com/8247b125c7b6888dc1c3932e19d6d8fe5a74a460/chrome/test/data/extensions/api_test/ntp_content_script/background.js
[add] https://crrev.com/8247b125c7b6888dc1c3932e19d6d8fe5a74a460/chrome/test/data/extensions/api_test/ntp_content_script/content_script.js
[add] https://crrev.com/8247b125c7b6888dc1c3932e19d6d8fe5a74a460/chrome/test/data/extensions/api_test/ntp_content_script/fake_ntp.html
[add] https://crrev.com/8247b125c7b6888dc1c3932e19d6d8fe5a74a460/chrome/test/data/extensions/api_test/ntp_content_script/manifest.json


### ka...@chromium.org (2018-05-30)

Should be fixed now. This is a Security_Severity-Low, would leave it up to the Release Managers to see if this warrants a merge.

### sh...@chromium.org (2018-05-31)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-04)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-06-08)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2018-06-09)

Nice one shutovby@, the Chrome VRP panel decided to award $500 for this report. A member of our finance team will be in touch to arrange payment. Also, how would you like to be credited in the Chrome release notes?

### aw...@google.com (2018-06-09)

[Empty comment from Monorail migration]

### sh...@gmail.com (2018-06-09)

Thank you awhalley@, let it be "Alexander Shutov (Dark Reader extension)".

Maybe it's worth renaming the issue title to "Extension can run script at New Tab Page" for the release notes to make it human-friendly.

### sh...@gmail.com (2018-07-24)

The issue happens in Stable 68.0.3440.75

I've also noticed that step 6 (focus on another application for at least 2 minutes) is no more necessary to reproduce the issue in Chrome 67 and 68. Focusing on Incognito window for a minute makes the issue happen on initial window. So, if I used to reproduce it once a week and it was hard to understand what's the case, now I face it every time when I open Incognito or Guest window (or all the time until I close the browser).

So, now the steps to reproduce look like:
1. Open Chrome browser.
2. Install the attached extension or Dark Reader extension from the Chrome Web Store.
3. Navigate somewhere (e.g. https://www.google.com/).
4. Open new incognito window (Ctrl+Shift+N) or new Guest window (navigation not necessary).
5. Wait for a minute.
6. Focus on initial window.
7. Open new tab, the script is injected there.

Thanks for the reward, it will let me work on Dark Reader 2 weeks more. Please, consider renaming the issue into "Extension can run script at New Tab Page", it can help us get some more users trust to extensions after Stylish incident.

p.s. Seems like it is not reproduced in Canary 70.

### aw...@google.com (2018-07-25)

Thanks shutovby@ - the fix in https://crbug.com/chromium/844428#c11 landed in Chrome 69, so it should be fixed there as well as 70.

### sh...@gmail.com (2018-09-04)

Missing in Release Notes https://chromereleases.googleblog.com/2018/09/stable-channel-update-for-desktop.html

### aw...@google.com (2018-09-05)

Thanks for spotting! It was missing a milestone label so didn't get caught by my automation. Will fix now.

### aw...@chromium.org (2018-09-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-09-06)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@google.com (2018-10-15)

[Empty comment from Monorail migration]

### aw...@chromium.org (2019-06-27)

[Empty comment from Monorail migration]

### is...@google.com (2019-06-27)

This issue was migrated from crbug.com/chromium/844428?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/842919]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091421)*
