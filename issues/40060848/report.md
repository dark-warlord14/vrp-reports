# Security: Custom cursor can overlay parts of the permission prompt.

| Field | Value |
|-------|-------|
| **Issue ID** | [40060848](https://issues.chromium.org/issues/40060848) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Input |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ha...@gmail.com |
| **Assignee** | an...@chromium.org |
| **Created** | 2022-09-07 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

A site can set a custom cursor (128x128, for example) which can overlay parts of the permission prompt.

**VERSION**  

Chrome Version: 105.0.5195.102 (stable)  

Operating System: Windows 10 Version 21H2 (Build 19044.1889)

**REPRODUCTION CASE**

1. Download html and png file into same directory.
2. Open html file and click the middle of the emoji (if it is the top the custom cursor wouldn't show, so it should be the middle).
3. See the custom cursor overlay part of the permission prompt
4. A malicious person could possibly overlay the permission prompt with something less nefarious, which would result in the victim believing it (without immediately noticing the text changing when the cursor hovers above the permission prompt) and accept the prompt.

(Please excuse my horrible HTML skills)

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: Axel Chong

## Attachments

- [perm-overlay-poc.html](attachments/perm-overlay-poc.html) (text/plain, 566 B)
- [cursor-128x128.png](attachments/cursor-128x128.png) (image/png, 2.1 KB)

## Timeline

### [Deleted User] (2022-09-07)

[Empty comment from Monorail migration]

### ma...@chromium.org (2022-09-08)

Repros on linux 105.0.5195.102, 106.0.5249.21. Based on blame/other bugs assuming this exists in extended stable version as well.

Assuming this applies on all desktop platforms.

Setting severity low as overlaying part of the permission prompt is a special case of "allows web content to tamper with trusted browser UI", however the fact that the custom cursor disappears as you move over the dialog does mitigate it.

Assigning to csharrison based on https://crbug.com/chromium/880863. This is a variant in that the permission dialog renders inside the frame, so just clipping on the frame is insufficient.

[Monorail components: Blink>Input]

### [Deleted User] (2022-09-08)

[Empty comment from Monorail migration]

### cs...@chromium.org (2022-09-08)

I shouldn't own this - as much as I care about this issue I've since moved teams and can't focus on anti-abuse as much as I used.

The existing protection for this (beyond just max size protection), exists purely in the renderer. This was done for simplicity but introduces a few problems:
a. An owned renderer can bypass protections
b. It is difficult to extend the implementation to detect clipping parts of the browser UI that isn't known to the renderer.

I think permission prompts fall under (b), so my suggestion to someone taking this bug is to investigate moving the implementation of the protections here into the browser process which has a better understanding of where all the browser-privileged pixels are relative to the cursor. This also neatly solves (a).

### [Deleted User] (2022-09-08)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@chromium.org (2023-05-03)

Hi andypaicu@ assigning this issue to you since it has gone without an owner for some time. 
The good news here is that it appears resolved by https://chromium-review.googlesource.com/c/chromium/src/+/4154719 landed for https://crbug.com/chromium/1385714. 
Can you PTAL and confirm. If this is correct, please do not merge this issue into that the newer report as this is the earlier reported version of that issue and we would need to process this report for VRP. Thank you! 

### am...@chromium.org (2023-05-03)

[Empty comment from Monorail migration]

### ha...@gmail.com (2023-05-05)

Hi, friendly ping on this issue. andypaicu@

### am...@chromium.org (2023-05-08)

I'm going to close this as fixed given that this does appear to be an earlier reported duplicate of https://crbug.com/chromium/1360710. 
andypaicu@ please LMK if you do not believe this to be correct.


### am...@chromium.org (2023-05-08)

copy pasta error in https://crbug.com/chromium/1360710#c9, this an *earlier reported dupe of https://crbug.com/chromium/1385714

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### [Deleted User] (2023-05-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-05-12)

Congratulations, Axel! The VRP Panel has decided to award you $2,000 for this report. Thank you for your efforts and reporting this issue to us! 

### am...@google.com (2023-05-14)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-15)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-08-15)

This issue was migrated from crbug.com/chromium/1360710?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060848)*
