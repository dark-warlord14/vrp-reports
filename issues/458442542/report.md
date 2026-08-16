#  Popup window tab doesn't show the origin correctly

| Field | Value |
|-------|-------|
| **Issue ID** | [458442542](https://issues.chromium.org/issues/458442542) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>TopChrome>TabStrip>HoverCards |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | sa...@gmail.com |
| **Created** | 2025-11-07 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS

This vulnerability is similar to this: 
https://issues.chromium.org/issues/40075024, https://issues.chromium.org/issues/448421954

but in this bug Popup window tab doesn't show correctly. in the popup window it shows subdomain.paypal.auth.docs.google.com which should be about:blank

VERSION
Chrome Version 144.0.7513.0 (Official Build) canary (64-bit)
Operating System: Windows 11

REPRODUCTION CASE
1. Open tabdomain.html
1. Click on button  in tabdomain.html
2. Hover over the tab

## Attachments

- [tabdomain.html](attachments/tabdomain.html) (text/html, 208 B)
- [longdomain1.jpg](attachments/longdomain1.jpg) (image/jpeg, 176.9 KB)

## Timeline

### dc...@chromium.org (2025-11-07)

This appears to be a fairly recent regression/change. It repros in canary but not in dev for me (I tested on both Mac and Windows).

Dev version: 144.0.7500.2 (Official Build) dev (arm64)
Canary version: 144.0.7513.0 (Official Build) canary (arm64)

### ch...@google.com (2025-11-07)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### fl...@google.com (2025-11-21)

Hey, just want to make sure you take a look at https://g-issues.chromium.org/issues/462477500 as well when looking at this bug.

I marked it as a duplicate because it seems similar enough that I think it *might* be the same code implicated both times... but I don't know enough about the code stack on Windows vs Android to know if it's actually two separate bugs.

I'll also update the impacted OSes as well.

### ag...@google.com (2026-04-16)

It looks like right now for a url of "about:blank#long-sketchy.domain.looking.thing" the omnibox displays "about:blank", the mini toolbar displays "about:blank#long-sketchy..." and the hovercard displays "...sketchy.domain.looking.thing". The hovercard is definitely the most wrong but I was hoping to confirm what was most right between the omnibox and hte minitoolbar so everything could be aligned. Chris, do you have thoughts on this?


### ct...@google.com (2026-04-16)

I think the Omnibox behavior seems the most useful to the user -- showing the fragment is fairly distracting, and in space constrained UIs (like hovercard and mini toolbar) I think it would be better to just not try to show the fragment at all.

(From some quick testing, it is maybe notable that the Omnibox doesn't seem to suppress the fragment if the navigation was user-typed into the Omnibox. But for hovercard/mini toolbar I think the simpler logic of just not showing the fragment ever here is fine or even better and avoids additional complexity.)

### dx...@google.com (2026-05-04)

Project: chromium/src  

Branch:  main  

Author:  Hafiizh [sas.kunz@gmail.com](mailto:sas.kunz@gmail.com)  

Link:    <https://chromium-review.googlesource.com/7761368>

hovercard: Fix hover card domain label for about:blank tabs

---


Expand for full commit details
```
     
    Previously, the hover card domain label for about:blank tabs was not 
    handled explicitly, which could cause incorrect domain text to be 
    displayed. This patch adds an explicit check for about:blank URLs and 
    sets the domain label to url::kAboutBlankURL16 accordingly. 
     
    Bug: 458442542 
    Change-Id: Ib34c977395919b5c6e7b89cc424867922452aa0f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7761368 
    Commit-Queue: Alison Gale <agale@chromium.org> 
    Auto-Submit: Bug Bounty Channel <sas.kunz@gmail.com> 
    Reviewed-by: Foromo Daniel Soromou <koretadaniel@chromium.org> 
    Reviewed-by: Alison Gale <agale@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1624740}

```

---

Files:

- M `AUTHORS`
- M `chrome/browser/ui/views/frame/multi_contents_view_mini_toolbar.cc`
- M `chrome/browser/ui/views/tabs/hovercard/hover_card_anchor_target.cc`

---

Hash: [4565bd201d41b752c3a5df16298d8d0470e75dbd](https://chromiumdash.appspot.com/commit/4565bd201d41b752c3a5df16298d8d0470e75dbd)  

Date: Mon May 4 16:20:30 2026


---

### sp...@google.com (2026-05-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Security UI spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/458442542)*
