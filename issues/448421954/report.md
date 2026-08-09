# Security: Popup window tab doesn't show the origin elided from the right

| Field | Value |
|-------|-------|
| **Issue ID** | [448421954](https://issues.chromium.org/issues/448421954) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>TopChrome>TabStrip>HoverCards |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Reporter** | ch...@gmail.com |
| **Assignee** | dp...@google.com |
| **Created** | 2025-10-01 |
| **Bounty** | $500.00 |

## Description

VULNERABILITY DETAILS
This vulnerability is similar to this one: https://issues.chromium.org/issues/40075024 but in this bug Popup window tab doesn't show correctly. in the popup window it shows https://pwr.wtf.کورد/ which should be https://کورد.pwr.wtf/

VERSION
Chrome Version 142.0.7444.0 (Official Build) canary (64-bit)
Operating System: Windows 11

REPRODUCTION CASE
1. Go to  https://کورد.pwr.wtf/poc.html?
2. Hover over the tab 

## Attachments

- [nc.jpg](attachments/nc.jpg) (image/jpeg, 63.1 KB)

## Timeline

### ca...@chromium.org (2025-10-01)

I was able to reproduce this on current stable. Triaging as low severity since the correct origin is still shown in the Omnibox

### ca...@chromium.org (2025-10-01)

dpenning: Can you PTAL (and re-assign as appropriate)? This is similar to crbug.com/40075024 which you fixed, but this is specifically an issue when displaying URLs with RTL components.

### ch...@google.com (2025-10-02)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2026-04-10)

hi may you add cc: koretadaniel@chromium.org to access this bug too?

### dx...@google.com (2026-04-14)

Project: chromium/src  

Branch:  main  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7762370>

[Hovercards] Use the correct directionality for hovercard domains

---


Expand for full commit details
```
     
    Relevant documentation: 
    https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/url_display_guidelines/url_display_guidelines.md#rtl 
     
    Screenshot: https://screenshot.googleplex.com/AGAkRJEPEq9DzEn 
     
    Note that the title of the page is the opposite direction but titles 
    aren't urls so that should be okay. 
     
    Bug: 448421954 
    Change-Id: If556b49e0764c6f73edebeb490d3c4b0c5dccb41 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7762370 
    Reviewed-by: David Yeung <dayeung@chromium.org> 
    Commit-Queue: Alison Gale <agale@chromium.org> 
    Reviewed-by: Eshwar Stalin <estalin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1614711}

```

---

Files:

- M `chrome/browser/ui/views/tabs/hovercard/fade_label_view.cc`
- M `chrome/browser/ui/views/tabs/hovercard/fade_label_view.h`
- M `chrome/browser/ui/views/tabs/hovercard/hover_card_anchor_target.cc`
- M `chrome/browser/ui/views/tabs/hovercard/tab_hover_card_bubble_view_unittest.cc`
- M `ui/views/controls/label.cc`
- M `ui/views/controls/label.h`
- M `ui/views/controls/label_unittest.cc`

---

Hash: [cb262a7368abf1bab2ebbd122e2f8eabc4bc4066](https://chromiumdash.appspot.com/commit/cb262a7368abf1bab2ebbd122e2f8eabc4bc4066)  

Date: Tue Apr 14 21:28:05 2026


---

### sp...@google.com (2026-05-26)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

does not pass reasonable prudent user test

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-07-22)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/448421954)*
