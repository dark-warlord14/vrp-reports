# googlelogoligature ligature can disguise security-sensitive surfaces

| Field | Value |
|-------|-------|
| **Issue ID** | [391788835](https://issues.chromium.org/issues/391788835) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>LookalikeChecks |
| **Platforms** | Android |
| **Reporter** | yu...@gmail.com |
| **Assignee** | me...@chromium.org |
| **Created** | 2025-01-23 |
| **Bounty** | $15,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md

Please see the following link for instructions on filing security bugs: https://www.chromium.org/Home/chromium-security/reporting-security-bugs

Reports may be eligible for reward payments under the Chrome VRP: https://g.co/chrome/vrp

NOTE: Security bugs are normally made public once a fix has been widely deployed.

-------------------------

VULNERABILITY DETAILS

Security-sensitive surfaces can be spoofed due to the presence of the google logo ligature (googlelogoligature) in the font used in Chrome for Android

https://docs.google.com/document/d/1_xJz3J9kkAPwk3pma6K3X12SyPTyyaJDSCxTfF8Y5sU/mobilebasic
VERSION

Chrome Version: Chrome 132.0.6834.79 stable
Operating System: Android 15; Pixel 9 Build/AP4A.241205.013

REPRODUCTION CASE
http://googlelogoligature.net/

FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION
Type of crash: [tab, browser, etc.]
Crash State: [see link above: stack trace *with symbols*, registers, exception record]
Client ID (if relevant): [see link above]

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: yuki yamaoto

## Attachments

- [Screenshot_20250124-021309.png](attachments/Screenshot_20250124-021309.png) (image/png, 132.1 KB)
- [Screenshot_20250124-021345.png](attachments/Screenshot_20250124-021345.png) (image/png, 220.4 KB)
- Screenshot_20250124-021519.png (image/png, 170.1 KB)
- Screenshot 2025-01-23 at 11.04.40 AM.png (image/png, 285.8 KB)

## Timeline

### ct...@chromium.org (2025-01-23)

Thank you for finding this and sending us this report! We were genuinely surprised to see this when I shared it in our URL spoof team chat.

Setting some initial security triage labels:

- Sev-Medium (S2) since this can be used for a very good spoof against google.com, but it does not allow complete or arbitrary control over the Omnibox origin (which would be Sev-High)
- FoundIn-132 since this goes back to *at least* extended stable

Passing this to meacer@ to think about how we might address this.

This appears to repro as far back as a Pixel 6 running Android 13 but with modern Chrome (tested with M134 Canary) but *not* with the older Chrome version that's preinstalled on my emulator (tested with M109).

Notably there appear to be a number of these ligatures, which I think we could use to make the spoof even better -- see attached screenshot of `glogoligatureoogle.com`. I *think* if we could enumerate all the ligatures for this font we could probably identify all of the ones that are confusables and add them to our skeleton mapping (maybe only on Android build if possible)?

### nh...@chromium.org (2025-01-23)

Looking through the Google Sans font, I found the following ligatures that could be used for similar spoofs:

calt (contextual alternates):

Google_logo
G_logo
e_logo
google_logo
google_G
google_g
g_logo
l_logo
o_logo
super_G_logo
super_g_logo

liga (standard ligatures):

Googlelogoligature
Glogoligature
Google_logo
elogoligature
googlelogoligature
glogoligature
google_logo
llogoligature
ologoligature

### yu...@gmail.com (2025-01-23)

Additional items I know of are listed below.

- G_logo
- o_logo
- g_logo
- l_logo
- e_logo
- Glogoligature
- ologoligature
- glogoligature
- llogoligature
- elogoligature

### ct...@chromium.org (2025-01-23)

Chatting about this bug internally, the lowercase `g` google.com spoof makes this feel more like a Sev-High than a Sev-Medium. The severity guidelines call out "arbitrary control of the apparent origin in the omnibox", but IMO the spirit of that is "can you spoof our most high value domains in a way that users won't notice" and I think this qualifies.

### yu...@gmail.com (2025-01-23)

I registered an Issue on google's side because it is likely to affect other applications that use the same font. However, it was marked as ”Won't Fix”.
What should I do?

### yu...@gmail.com (2025-01-24)

I guess using "g" allows an attacker to spoof all Japanese government domains (.go.jp).

### pe...@google.com (2025-01-24)

Setting milestone because of s0/s1 severity.

### pe...@google.com (2025-01-24)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### jd...@chromium.org (2025-01-31)

meacer@: just bumping this up towards the top of your list, since it's S1.

### ap...@google.com (2025-02-04)

Project: chromium/src  

Branch: main  

Author: Mustafa Emre Acer <[meacer@chromium.org](mailto:meacer@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6227546>

[Lookalikes] Disallow hostnames containing certain ligatures

---


Expand for full commit details
```
[Lookalikes] Disallow hostnames containing certain ligatures 
 
On some platforms, system fonts contain ligatures that render the 
Google logo. This can be used to spoof hostnames. 
 
This CL blocks hostnames containing unsafe ligatures with an 
interstitial. 
 
Bug: 391788835 
Change-Id: Ida694f42b2540ec61b78c7f9f6d0732a768c16c9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6227546 
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org> 
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1415328}

```

---

Files:

- M `chrome/browser/lookalikes/lookalike_url_navigation_throttle_browsertest.cc`
- M `components/lookalikes/core/lookalike_url_util.cc`

---

Hash: 8831e558be2ff9567efce5f1e9ea54e47d41490a  

Date:  Mon Feb 03 17:53:06 2025


---

### me...@google.com (2025-02-06)

This is fixed on Canary. Confirmed with a site that serves a response.

### pe...@google.com (2025-02-07)

Security Merge Request Consideration: Requesting merge to extended stable (M132) because latest trunk commit (1415328) appears to be after extended stable branch point (1381561).
Security Merge Request Consideration: Requesting merge to stable (M133) because latest trunk commit (1415328) appears to be after stable branch point (1402768).
Security Merge Request Consideration: Not requesting merge to beta (M134) because latest trunk commit (1415328) appears to be prior to beta branch point (1415337). If this is incorrect please remove NA-134 from the 'Merge' field and add 134 to the 'Merge-Request' field If other changes are required to fix this bug completely please request a merge if necessary.
Security Merge Request - Manual Review: Merge review required: M132 is already shipping to stable.

Security Merge Request - Manual Review: Merge review required: M133 is already shipping to stable.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [132, 133].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### am...@chromium.org (2025-02-07)

Thanks for the quick work on this meacer@
I reviewed canary data however, I don't really have any expectations of stability issues related to this change.
But I don't know if there are any other risks with shipping this ligature change in the browser URL. I'm tentatively approving for backmerge to Stable and Extended Stable, but please confirm there are no risks or concerns with backmerging this change at this time.

If there are no concerns, please backmerge to M133 Stable / branch 6943 and M132 Extended Stable / branch 6834 as soon as possible / before 9am PT on Monday, 10 February. Otherwise, please let me know of any concerns and we can make another plan here.

### me...@google.com (2025-02-07)

cthomp@ and I checked that no domains are affected by this.

[crrev.com/c/6244108](https://crrev.com/c/6244108) is the M133 merge

[crrev.com/c/6245515](https://crrev.com/c/6245515) is the M132 merge

### ap...@google.com (2025-02-07)

Project: chromium/src  

Branch: refs/branch-heads/6943  

Author: Mustafa Emre Acer <[meacer@chromium.org](mailto:meacer@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6245515>

[Merge M133][Lookalikes] Disallow hostnames containing certain ligatures

---


Expand for full commit details
```
[Merge M133][Lookalikes] Disallow hostnames containing certain ligatures 
 
On some platforms, system fonts contain ligatures that render the 
Google logo. This can be used to spoof hostnames. 
 
This CL blocks hostnames containing unsafe ligatures with an 
interstitial. 
 
(cherry picked from commit 8831e558be2ff9567efce5f1e9ea54e47d41490a) 
 
Bug: 391788835 
Change-Id: Ida694f42b2540ec61b78c7f9f6d0732a768c16c9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6227546 
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org> 
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415328} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6245515 
Reviewed-by: Chris Thompson <cthomp@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6943@{#1486} 
Cr-Branched-From: 72dd0b377c099e1e0230cc7345d5a5125b46ae7d-refs/heads/main@{#1402768}

```

---

Files:

- M `chrome/browser/lookalikes/lookalike_url_navigation_throttle_browsertest.cc`
- M `components/lookalikes/core/lookalike_url_util.cc`

---

Hash: f724c99d861fac1fe4f70c18b0384752d0f96e1e  

Date:  Fri Feb 07 15:47:26 2025


---

### ap...@google.com (2025-02-08)

Project: chromium/src  

Branch: refs/branch-heads/6834  

Author: Mustafa Emre Acer <[meacer@chromium.org](mailto:meacer@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6244108>

[Merge M132][Lookalikes] Disallow hostnames containing certain ligatures

---


Expand for full commit details
```
[Merge M132][Lookalikes] Disallow hostnames containing certain ligatures 
 
On some platforms, system fonts contain ligatures that render the 
Google logo. This can be used to spoof hostnames. 
 
This CL blocks hostnames containing unsafe ligatures with an 
interstitial. 
 
(cherry picked from commit 8831e558be2ff9567efce5f1e9ea54e47d41490a) 
 
Bug: 391788835 
Change-Id: Ida694f42b2540ec61b78c7f9f6d0732a768c16c9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6227546 
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org> 
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415328} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6244108 
Reviewed-by: Chris Thompson <cthomp@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6834@{#4994} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/browser/lookalikes/lookalike_url_navigation_throttle_browsertest.cc`
- M `components/lookalikes/core/lookalike_url_util.cc`

---

Hash: 7f4dd84f8272fc3ee5f98c5c833a1b42d684c756  

Date:  Fri Feb 07 16:03:16 2025


---

### sp...@google.com (2025-02-14)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $15000.00 for this report.

Rationale for this decision:
$10,000 for report of high-quality && high-impact security UI issue + $5,000 bonus for unique, novel cool bug -- this was a very neat discovery!


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-02-14)

Congratulations Yuki! This was a really neat finding. It's been awhile since we've seen a security UI bug that has make our jaws drop. Thank you for your efforts and reporting this really novel issue to us -- we're floored this has been awhile for awhile and no one has discovered it. Great work!

### yu...@gmail.com (2025-02-14)

Thank you very much! I am so glad you appreciate my report.

### ap...@google.com (2025-02-21)

Project: chromium/src  

Branch: refs/branch-heads/6834\_160  

Author: Mustafa Emre Acer <[meacer@chromium.org](mailto:meacer@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6288589>

[CfM-R132][Lookalikes] Disallow hostnames containing certain ligatures

---


Expand for full commit details
```
[CfM-R132][Lookalikes] Disallow hostnames containing certain ligatures 
 
On some platforms, system fonts contain ligatures that render the 
Google logo. This can be used to spoof hostnames. 
 
This CL blocks hostnames containing unsafe ligatures with an 
interstitial. 
 
Bug: 391788835 
Change-Id: Ida694f42b2540ec61b78c7f9f6d0732a768c16c9 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6227546 
Reviewed-by: Joe DeBlasio <jdeblasio@chromium.org> 
Commit-Queue: Mustafa Emre Acer <meacer@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1415328} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6288589 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Cr-Commit-Position: refs/branch-heads/6834_160@{#14} 
Cr-Branched-From: cdae089eab830291f81deb011febbbdc520a019e-refs/branch-heads/6834@{#4409} 
Cr-Branched-From: 47a3549fac11ee8cb7be6606001ede605b302b9f-refs/heads/main@{#1381561}

```

---

Files:

- M `chrome/browser/lookalikes/lookalike_url_navigation_throttle_browsertest.cc`
- M `components/lookalikes/core/lookalike_url_util.cc`

---

Hash: f20deed85b9e7a00c5fe6dae3eb5bbd1d47f9ef7  

Date:  Fri Feb 21 10:27:54 2025


---

### ch...@google.com (2025-05-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/391788835)*
