# Chrome on Android: spoofing issue caused by bottom address bar

| Field | Value |
|-------|-------|
| **Issue ID** | [454354281](https://issues.chromium.org/issues/454354281) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Omnibox |
| **Platforms** | Android |
| **Chrome Version** | 143.0.0.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-10-23 |
| **Bounty** | $3,000.00 |

## Description

# Steps to reproduce the problem

(Similar to issue [issue 437147699](https://issues.chromium.org/issues/437147699)).

1. Open index.html or <https://lbstyle.github.io/bin.html> in an incognito window (to reproduce constantly).
2. Tap the "Click" button.
3. Tap inside the first input field and wait.
4. When the alert pops up, tap OK.

# Problem Description

The address bar (omnibox) shows google.com, but the page content is incorrect.

# Summary

Chrome on Android: spoofing issue caused by bottom address bar

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- [alert.html](attachments/alert.html) (text/html, 357 B)
- [index.html](attachments/index.html) (text/html, 278 B)
- [screen.mp4](attachments/screen.mp4) (video/mp4, 548.1 KB)

## Timeline

### xi...@chromium.org (2025-10-23)

Thanks for the report. I'm able to reproduce. It does look like a legitimate spoofing issue since the address bar is showing the wrong URL. +pnoland@ to take a look. Thanks!

### pn...@google.com (2025-10-23)

So two issues are apparent:

1. The capture is stale. This is probably the same cause as 452372365; i.e. onContentViewScrollingChanged doesn't get called again due to the alert dialog
2. The toolbar doesn't scroll all the way off when entering fullscreen mode

### pn...@google.com (2025-10-23)

I have a fix for #2, which may be the root cause for other "stale snapshot while controls are bottom-anchored" spoof scenarios.

### ch...@google.com (2025-10-24)

Setting milestone because of s2 severity.

### ch...@google.com (2025-10-24)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### dx...@google.com (2025-10-24)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7081525>

Push browser controls update whenever bottom controls height changes

---


Expand for full commit details
```
     
    The old logic failed to push updates when height changed at 0% shown 
    ratio. This was a problem because the offset needs to change when the 
    height changes at 0% to reflect the new height (i.e. the offset should 
    become the new height) to avoid leaving the controls partially visible. 
    The new logic matches existing logic for top controls. 
     
    Bug: 454354281 
    Change-Id: I733d103e8cda58a4dbeefe1fa71282924f7bcd27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7081525 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1535059}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_android.cc`
- M `content/browser/renderer_host/render_widget_host_view_android.h`
- M `content/browser/renderer_host/render_widget_host_view_android_unittest.cc`

---

Hash: [e81ab324244b7c87c500cc0dc022c40089f86bee](https://chromiumdash.appspot.com/commit/e81ab324244b7c87c500cc0dc022c40089f86bee)  

Date: Fri Oct 24 16:00:23 2025


---

### pe...@google.com (2025-10-27)

The NextAction date has arrived: 2025-10-27
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pn...@google.com (2025-10-27)

This no longer repros for me in Canary; reporter, can you reproduce it?

### ch...@gmail.com (2025-10-27)

I can't repro this on Canary.

### ch...@google.com (2025-10-28)

Security Merge Request Consideration: Requesting merge to beta (M142) because latest trunk commit (1535059) appears to be after beta branch point (1522585).
Security Merge Request - Manual Review: Merge review required: M142 is already shipping to stable.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [142].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@google.com (2025-10-28)

1. <https://chromium-review.googlesource.com/7081525>
2. Yes
3. No
4. No
5. No

### ya...@chromium.org (2025-10-29)

Please proceed with merging.

### go...@google.com (2025-10-30)

[Bulk Edit]

Please merge your change to M142 ASAP so we can take it in for next M142  refresh, RC cut 10:00 AM PT Monday. 

### dx...@google.com (2025-10-30)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7096502>

[m142] Push browser controls update whenever bottom controls height changes

---


Expand for full commit details
```
     
    The old logic failed to push updates when height changed at 0% shown 
    ratio. This was a problem because the offset needs to change when the 
    height changes at 0% to reflect the new height (i.e. the offset should 
    become the new height) to avoid leaving the controls partially visible. 
    The new logic matches existing logic for top controls. 
     
    (cherry picked from commit e81ab324244b7c87c500cc0dc022c40089f86bee) 
     
    Bug: 454354281 
    Change-Id: I733d103e8cda58a4dbeefe1fa71282924f7bcd27 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7081525 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Reviewed-by: Nasko Oskov <nasko@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1535059} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7096502 
    Cr-Commit-Position: refs/branch-heads/7444@{#2281} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `content/browser/renderer_host/render_widget_host_view_android.cc`
- M `content/browser/renderer_host/render_widget_host_view_android.h`
- M `content/browser/renderer_host/render_widget_host_view_android_unittest.cc`

---

Hash: [6febf1d4544f3eb456af27bf1b0a13e359109b7b](https://chromiumdash.appspot.com/commit/6febf1d4544f3eb456af27bf1b0a13e359109b7b)  

Date: Thu Oct 30 15:42:33 2025


---

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $3000.00 for this report.

Rationale for this decision:
Security UI Spoofing


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-02-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI Spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/454354281)*
