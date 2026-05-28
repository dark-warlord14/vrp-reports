# Spoof on Address Bar

| Field | Value |
|-------|-------|
| **Issue ID** | [443408317](https://issues.chromium.org/issues/443408317) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Reporter** | sa...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-09-06 |
| **Bounty** | $1,000.00 |

## Description

When opening a long domain using link with 2-4 characters, the address bar reduces by 1, for example:

a.w ww.aaaaa.auths.account.google.c appears in the address bar as www.aaaaa.auths.account.google.c (so the victim will think it's www.aaaaa.auths.account.google.com).

b. https://www.aaaaa.auths.account.google.run appears in the address bar as www.aaaaa.auths.account.google.ru (so the victim will think it's www.aaaaa.auths.account.google.ru). .ru is the domain for Russia.

c. https://www.aaaaa.auths.account.facebook.io/ appears in the address bar as www.aaaaa.auths.account.google.i (so the victim will think it's www.aaaaa.auths.account.google.it). .it is the domain for Italy.
and example: other
by reducing the number of domain names, this causes spoofing in the address bar.

OS: Android 15
Device: Samsung A56
Chrome Version:  142.0.7396.0 Canary 

Steps to reproduce:
1. open http://http://you-can-billowy-nimble-login-secure-docs-google-source-attacker.com/spoofshortdomain.html
2. click the link


## Attachments

- [spoofdomain.mp4](attachments/spoofdomain.mp4) (video/mp4, 4.8 MB)
- [googlevk.jpg](attachments/googlevk.jpg) (image/jpeg, 24.5 KB)
- [googlevk1.jpg](attachments/googlevk1.jpg) (image/jpeg, 24.5 KB)
- [spoofdomainx.html](attachments/spoofdomainx.html) (text/html, 1.0 KB)
- [fixurladdressbar.mp4](attachments/fixurladdressbar.mp4) (video/mp4, 1.7 MB)
- [fixurladdressbar.jpg](attachments/fixurladdressbar.jpg) (image/jpeg, 26.4 KB)

## Timeline

### ah...@google.com (2025-09-08)

Thanks for the report and the videos!

I wasn't able to repro with an emulator.

Provisionally setting severity to medium as per the security guidelines.

Provisionally setting FoundIn to the current extended stable.

### ah...@google.com (2025-09-08)

@pn...@google.com Could you please take a look?

thanks,

### ch...@google.com (2025-09-09)

Setting milestone because of s2 severity.

### ch...@google.com (2025-09-09)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-09-18)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6965664>

Fix url bar width when action container is gone

---


Expand for full commit details
```
     
    The url bar should be constrained by the padding of the parent 
    container. When the action container is gone, this doesn't happen 
    properly; the url bar is clipped but is measured without considering 
    this padding. This causes it to miscalculate the scroll pos when 
    emphasizing the tld. We can fix this by setting a margin for when the 
    url action container is gone equal to the end padding of the parent. 
     
    Bug: 443408317 
    Change-Id: Ie3504baec49048b874e41bac4a2201f4da17142d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965664 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1517483}

```

---

Files:

- M `chrome/android/java/res/layout/url_bar.xml`

---

Hash: [6274f4749acb91c4fc07860ffaa0502a75a60620](https://chromiumdash.appspot.com/commit/6274f4749acb91c4fc07860ffaa0502a75a60620)  

Date: Thu Sep 18 19:23:25 2025


---

### sa...@gmail.com (2025-09-18)

Hi pn..@google.com, Has this bug been fixed? If so, the bug status should be set to fixed.

### pn...@google.com (2025-09-18)

Let's test in Canary tomorrow and flip the status if it appears to be resolved

### sa...@gmail.com (2025-09-18)

I will test it tommorow

### sa...@gmail.com (2025-09-19)

i confirmed this bug already fix on 142.0.7422.0 . the end of the url is very clear and not truncated

### ch...@google.com (2025-09-19)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@google.com (2025-09-19)

1. <https://chromium-review.git.corp.google.com/c/chromium/src/+/6965664>
2. Yes
3. No
4. No
5. No

### pe...@google.com (2025-09-19)

The NextAction date has arrived: 2025-09-19
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### ya...@chromium.org (2025-09-19)

This has been approved for a merge. Please merge to M141 (7390)

### dx...@google.com (2025-09-19)

Project: chromium/src  

Branch:  refs/branch-heads/7390  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/6969715>

Fix url bar width when action container is gone

---


Expand for full commit details
```
     
    The url bar should be constrained by the padding of the parent 
    container. When the action container is gone, this doesn't happen 
    properly; the url bar is clipped but is measured without considering 
    this padding. This causes it to miscalculate the scroll pos when 
    emphasizing the tld. We can fix this by setting a margin for when the 
    url action container is gone equal to the end padding of the parent. 
     
    (cherry picked from commit 6274f4749acb91c4fc07860ffaa0502a75a60620) 
     
    Bug: 443408317 
    Change-Id: Ie3504baec49048b874e41bac4a2201f4da17142d 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6965664 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1517483} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6969715 
    Commit-Queue: Tomasz Wiszkowski <ender@google.com> 
    Cr-Commit-Position: refs/branch-heads/7390@{#1336} 
    Cr-Branched-From: d481efce5eb300acbb896686676ebd0352a6f1db-refs/heads/main@{#1509326}

```

---

Files:

- M `chrome/android/java/res/layout/url_bar.xml`

---

Hash: [3a910cf96561c2b60ad70b952d4deaf782422828](https://chromiumdash.appspot.com/commit/3a910cf96561c2b60ad70b952d4deaf782422828)  

Date: Fri Sep 19 23:06:14 2025


---

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
security ui spoofing baseline // lower impact


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-27)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/443408317)*
