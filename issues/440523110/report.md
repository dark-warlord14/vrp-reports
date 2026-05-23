# (Split View) UI spoofing Upload leads leaking confidential files, Photos to Attacker

| Field | Value |
|-------|-------|
| **Issue ID** | [440523110](https://issues.chromium.org/issues/440523110) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>TopChrome>TabStrip>SplitView |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 140.0.7339.24  |
| **Reporter** | pu...@gmail.com |
| **Assignee** | ag...@google.com |
| **Created** | 2025-08-22 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

1. Enable the #side-by-side flag
2. Open poc.html in Chrome Browser
3. Right click and open in Split view
4. This causes the Attacker file dialog to on omnibox e.g.: drive.google.com
   and then Select any file or photo
5. Successfully Uploaded in Attacker site

# Problem Description

When the user performs a right-click, this malicious listener is activated, and it displays the attacker's fabricated file upload dialog with Omnibox spoof, The file dialog itself isn't coming from Google's official website, but rather from an Attacker site

This is the primary goal. By convincing a user that they are on a legitimate website using Omnibox spoofing

This causes the Attacker page file dialog to open in the middle of the screen and above omnibox showing legitimate website Eg: <https://drive.google.com/drive/> that was just opened and might confuse the user into leaking sensitive information (their Photos, confidential files) to an attacker. This can make user into Believing it was opened/requested by the "drive.google.com" tab.

the user's most critical security checkpoint: the address bar. The user believes they are on a safe, legitimate domain, which dramatically increases the likelihood of a successful attack

# Summary

(Split View) UI spoofing Upload leads leaking confidential files, Photos to Attacker

# Additional Data

Category: Security   

Chrome Channel: Beta   

Regression: N/A \

## Attachments

- deleted (application/octet-stream, 0 B)
- [Repro.mp4](attachments/Repro.mp4) (video/mp4, 577.8 KB)
- [poc.html](attachments/poc.html) (text/html, 1012 B)
- deleted (application/octet-stream, 0 B)
- [chrome.png](attachments/chrome.png) (image/png, 173.5 KB)

## Timeline

### pu...@gmail.com (2025-08-22)

**Steps to reproduce the problem**

1.Enable the #side-by-side flag

2.Open poc.html

3.Right click and open in Split view

4.This causes the Attacker file dialog to open in the center of the screen with omnibox showing e.g.: drive.google.com and then you Select any file or photo

`Result:` Successfully Uploaded in Attacker site

### pu...@gmail.com (2025-08-22)

I have attached Screenshot of Chrome (in split view)

hopefully it will be helpful

### an...@chromium.org (2025-08-22)

Thanks for the report. I was able to reproduce this on Chrome (MacOS). Assigning severity S2 (user information disclosure via spoof). Setting FoundIn to 139 based on current rollout (Canary, Dev).

### an...@chromium.org (2025-08-22)

@stluong, assigning to you based on a similar split-view spoof, please re-route as you see fit. Thanks!

Seems like part of the issue here is that we aren't forcing focus back onto the inactive tab when it tries to trigger this in the "background".

### st...@google.com (2025-08-22)

This work might be covered by crbug.com/422176169 where I am trying to center dialogs based on its respective tab that triggered the dialog. I'm not sure if the file picker positioning follows the same code path but can look into it after the dialog centering issue is fixed.

### ch...@google.com (2025-08-23)

Setting milestone because of s2 severity.

### ch...@google.com (2025-08-23)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ag...@google.com (2025-08-25)

This should actually be handled by crbug.com/433818130. Background tabs shouldn't be able to open alerts, dialogs, file pickers, etc. In this example, the Google Drive site is active so the other one shouldn't be able to open it.

### ag...@google.com (2025-08-26)

Lowering to P2 because this feature won't be launched till M141

### ag...@google.com (2025-09-03)

Bugjuggler: (b/440523110 unblocked && b/440523110 has no open children) -> agale@

### bu...@google.com (2025-09-03)

Hi. I've received your bug and will wait for b/440523110 to be unblocked and wait for b/440523110's children to be closed and then assign the bug to agale.

### dx...@google.com (2025-09-08)

Project: chromium/src  

Branch:  main  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6916005>

[SxS] Prevent opening file picker from inactive tab in split

---


Expand for full commit details
```
     
    For security purposes, only the active tab should be able to open a 
    filed picker so the user knows which site is receiving the files. 
     
    Change-Id: If73e028c4041b40d2cfc935cb37f2b61b32416fd 
    Bug: 441139337,440523110 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6916005 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Commit-Queue: Alison Gale <agale@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1512743}

```

---

Files:

- M `chrome/browser/ui/browser.cc`
- M `chrome/browser/ui/browser.h`
- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/public/browser/web_contents_delegate.cc`
- M `content/public/browser/web_contents_delegate.h`

---

Hash: [d4c4449f8891183a1afc71a15b8b9b6596a5aad3](https://chromiumdash.appspot.com/commit/d4c4449f8891183a1afc71a15b8b9b6596a5aad3)  

Date: Mon Sep 8 23:21:45 2025


---

### bu...@google.com (2025-09-08)

Bug is closed; my job here is done.

### dx...@google.com (2025-09-11)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6941305>

[M141] [SxS] Prevent opening file picker from inactive tab in split

---


Expand for full commit details
```
     
    Original change's description: 
    > [SxS] Prevent opening file picker from inactive tab in split 
    >  
    > For security purposes, only the active tab should be able to open a 
    > filed picker so the user knows which site is receiving the files. 
    >  
    > Change-Id: If73e028c4041b40d2cfc935cb37f2b61b32416fd 
    > Bug: 441139337,440523110 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6916005 
    > Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    > Commit-Queue: Alison Gale <agale@chromium.org> 
    > Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1512743} 
     
    (cherry picked from commit d4c4449f8891183a1afc71a15b8b9b6596a5aad3) 
     
    Bug: 444254840,441139337,440523110 
    Change-Id: If73e028c4041b40d2cfc935cb37f2b61b32416fd 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6941305 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#692} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `chrome/browser/ui/browser.cc`
- M `chrome/browser/ui/browser.h`
- M `content/browser/web_contents/web_contents_impl.cc`
- M `content/browser/web_contents/web_contents_impl_browsertest.cc`
- M `content/public/browser/web_contents_delegate.cc`
- M `content/public/browser/web_contents_delegate.h`

---

Hash: [58c833ab4ef834cb9b9d70b4bb154e8bf79c8401](https://chromiumdash.appspot.com/commit/58c833ab4ef834cb9b9d70b4bb154e8bf79c8401)  

Date: Thu Sep 11 21:22:13 2025


---

### sp...@google.com (2025-09-19)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Security UI spoofing, Baseline // Lower Impact


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### pe...@google.com (2025-10-01)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ag...@google.com (2025-10-01)

This isn't being launched till M141 so no merge is necessary

### qk...@google.com (2025-10-02)

Labeled as not applicable for M132/138 LTS because the issue doesn't happen before M141.

### ch...@google.com (2025-12-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI spoofing, Baseline // Lower Impact

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/440523110)*
