# Bypass :// Characters in Download Security UI lead to Origin Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [392818696](https://issues.chromium.org/issues/392818696) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 131.0.0.0 |
| **Reporter** | fr...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2025-01-28 |
| **Bounty** | $500.00 |

## Description

# Steps to reproduce the problem

1.Prepare spoof.html
2. Access the spoof.html
3. Download the file
4. You will see that the :// blacklist is getting bypassed and allow attacker to create a fake origin

# Problem Description

By default, Chrome’s Security UI blocks :// from appearing as a filename in the Download UI. One reason Chrome may block these characters is to prevent spoofing techniques in the Download UI. However, in this case, I was able to bypass this restriction using ∶⧸⧸ (Ratio U+2236 + Long Division Slash U+29F8, x2). With this bypass method, an attacker can create a fake origin in the filename, such as creating a different origin source like `From https://google.com` to a malicious file in the Download Origin UI.

# Summary

Bypass :// Characters in Download Security UI lead to Origin Spoofing

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A

## Attachments

- spoof.html (text/html, 2.0 KB)
- bypass ::: chrome.mov (video/quicktime, 7.8 MB)

## Timeline

### fr...@gmail.com (2025-01-28)

Sorry, the steps to reproduce is not generated correctly, here is the new one:

1. Prepare spoof.html
2. Access the spoof.html
3. Download the file
4. You will see that the :// blacklist is getting bypassed and allow attacker to create a fake origin

### an...@chromium.org (2025-01-28)

chlily@, meacer@: can you take a look? This appears to be yet another lookalike bug but in the download UI. Is there a canonical bug for this?

### ch...@chromium.org (2025-01-28)

Hm I see. This is happening because we are formatting the referrer url for security lookalikes (<https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/downloads/downloads_list_tracker.cc;l=159;drc=aaeff707bc4de78c1c72a6c04ed737e49648236f>) but the filename is not processed for url lookalikes.

I'll defer to chrome/browser/lookalikes/OWNERS: Do we need to be checking for lookalike urls in displayed text that is not supposed to contain a url?

### an...@chromium.org (2025-01-28)

Thanks for the quick response chlily@! CCing the other lookalikes OWNERS as well.

### an...@chromium.org (2025-01-29)

meacer@, I've assigned this issue to you to get an answer for [comment #4](https://issues.chromium.org/issues/392818696#comment4). If we do need to perform a lookalike check for the download text, please re-route it back to chlily@. Thanks!

Assigned medium severity provisionally. Also set FoundIn to M132 (current stable) based on age of relevant code referenced in [comment#4](https://issues.chromium.org/issues/392818696#comment4).

### me...@google.com (2025-01-29)

It wouldn't be feasible to apply lookalike checks to like filenames without significant work. Presently, lookalike checks expect hostnames as input. Arbitrary strings like filenames would almost never be flagged as lookalikes, unless they also look like hostnames. Passing "From <https://google.com>" to the lookalike checks would just return a "not-lookalike" result.

We could do something simpler such as escaping confusable characters. For example, we can display https∶⧸⧸google.com as https:#x29F8;#x29F8;google.com or something like that. That doesn't solve the problem with actual characters though. If the file is named https:\\google.com (which is legit on Mac), that's just just as convincing.

I'm not sure what a good solution is here. The filename is untrusted and shouldn't be used to convey trust to the user. Maybe we can elide the filename so that it's less useful as an attack vector?

### ch...@chromium.org (2025-01-30)

> The filename is untrusted and shouldn't be used to convey trust to the user. Maybe we can elide the filename so that it's less useful as an attack vector?

Sure, sgtm. That should be easy.

### an...@chromium.org (2025-01-30)

Thanks meacer@ & chlily@! I changed the component to UI>Browser>Downloads. Feel free to change it if that is not correct.

### pe...@google.com (2025-01-30)

Setting milestone because of s2 severity.

### pe...@google.com (2025-01-30)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2025-02-06)

Project: chromium/src  

Branch: main  

Author: Lily Chen <[chlily@chromium.org](mailto:chlily@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6237214>

[Downloads] Truncate/elide overly long filenames

---


Expand for full commit details
```
[Downloads] Truncate/elide overly long filenames 
 
This adjusts the CSS on chrome://downloads to elide the filename if it 
would otherwise wrap, thereby limiting it to one line. Also adds a title 
attribute to the filename display, so that hovering over an elided 
filename will display the full filename. 
 
Screenshots: 
https://drive.google.com/drive/folders/1LrF74w51di8eNfs6bO9DmSGhLy45KdTl 
 
Bug: 392818696 
Change-Id: I234bf55844396bf29120db034b1128d460f95e06 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6237214 
Commit-Queue: Lily Chen <chlily@chromium.org> 
Reviewed-by: John Lee <johntlee@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1417034}

```

---

Files:

- M `chrome/browser/resources/downloads/item.css`
- M `chrome/browser/resources/downloads/item.html.ts`

---

Hash: fdf50ecfb6bcba3e7b19ca8aad93b28e2e37ef65  

Date:  Thu Feb 06 14:51:47 2025


---

### fr...@gmail.com (2025-02-08)

Thanks for the fix! when will the new update for this fix release?

### ch...@chromium.org (2025-02-10)

The fix is in Chrome 135:

Beta Promotion Wed, Mar 5, 2025

Stable Release Tue, Apr 1, 2025

### fr...@gmail.com (2025-02-10)

Thanks! How about the VRP reward? Is there any update?

### am...@chromium.org (2025-02-10)

Reward decisions are only made after the bug is fixed. VRP Panel meets once a week to make reward decisions. This issue will be assessed for potential reward later this week or next depending on queue. Thanks for your patience in the meantime.

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
Thank you reward for report of issue with low potential for user harm and issue requiring the user engage with the downloads workflow in a non-standard way. We were able to make a beneficial change from this report, so we wanted to acknowledge that contribution with a small reward.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Thank you again for your efforts and reporting this issue to us!

### fr...@gmail.com (2025-02-14)

Thanks for the bounty!

### pg...@google.com (2025-03-29)

@reporter, how would you like to be credited for this report?

### fr...@gmail.com (2025-03-30)

Sorry for the late response. Yes i want to be credited for this report, you can credit my name “Farras Givari”.

Thanks

### pg...@google.com (2025-03-31)

Updating OSes as this does not appear to be a Mac specific issue (but please correct me if i am wrong!)

### ch...@google.com (2025-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Thank you reward for report of issue with low potential for user harm and issue requiring the user engage with the downloads workflow in a non-standard way. We were able to make a beneficial change from this report, so we wanted to acknowledge that contribution with a small reward.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/392818696)*
