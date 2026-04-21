# Bottom Minibar Fails to Display URL – Potential Phishing via Spoof Bar

| Field | Value |
|-------|-------|
| **Issue ID** | [461532432](https://issues.chromium.org/issues/461532432) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | UI>Browser>Mobile>Toolbar |
| **Platforms** | Android |
| **Chrome Version** | 144.0.0.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-11-18 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Go to <https://lbstyle.github.io/testcase.html>
2. Tap inside the textarea field.
3. Tap the button labeled “Go to google.com”.

# Problem Description

Observed behavior: The spoof bar minibar does not display the current URL. This could allow a malicious page to overlay a fake minibar with a fake URL, potentially tricking users into entering sensitive information.

# Summary

Bottom Minibar Fails to Display URL – Potential Phishing via Spoof Bar

# Additional Data

Category: Security   

Chrome Channel: Not sure   

Regression: N/A \

## Attachments

- testcase.html (text/html, 2.7 KB)
- screen.mp4 (video/mp4, 6.2 MB)
- screen-20251124-192944.mp4 (video/mp4, 6.2 MB)

## Timeline

### ch...@gmail.com (2025-11-18)

Just suggesting @pnoland could be the right owner for this bug, since he has fixed previous minibar issues.

### th...@chromium.org (2025-11-19)

Not a Security Shephard, but trying to help make progress on triage.

### pn...@google.com (2025-11-19)

I can repro in stable but not Canary; reporter, which version did you repro with?

### ch...@gmail.com (2025-11-19)

144.0.7531.0 (Official Build) canary - Pixel 7 Pro.

### ch...@gmail.com (2025-11-19)

I tested again on version 144.0.7533.2 and I’m still able to reproduce the issue. However, when I tested on another device (Samsung), I couldn’t reproduce it there

### pn...@google.com (2025-11-19)

I've been able to reproduce intermittently with 144.0.7531.0

### za...@google.com (2025-11-20)

I succeeded in reproducing yesterday it but it's flaky. I suspect `FullscreenHtmlApiHandlerBase`[1] could be the culprit here because it waits for an `OnLayoutChangeListener` to restore the UI, which seems unreliable when the keyboard is active. The poc triggers a race by hitting `requestFullscreen`, shwoing the keyboard, and then firing `exitFullscreen` about 120ms later. If the layout pass misses the window, the browser controls stick in the hidden state, leaving a gap for the spoof. Reproduction is pretty flaky on my end though, it might vary by device speed. I used xcid to reproduce it could be due to low performance on the emulator.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/fullscreen/FullscreenHtmlApiHandlerBase.java;l=736?q=resetExitFullscreenLayoutChangeListener#:~:text=735-,736,-737>

### za...@google.com (2025-11-20)

Hi pnoland@, since you are in OWNERS for //chrome/android/.../fullscreen/, could you take a look at this security bug? (I see you are looking into this already, thank you). The issue is that the bottom origin bar is being suppressed which allows a spoof. Ideally, we want to ensure the mini origin bar is always shown. Assigning to you for initial investigation; please feel free to re-assign if there is a better owner for the bottom toolbar logic. Thank you.

### pn...@google.com (2025-11-20)

I think we need to force a relayout of the control container at some point in this flow; forcing one via debugger seemed to resolve the issue, which is of a flavor that we've tasted before.

### ch...@google.com (2025-11-21)

Setting milestone because of s2 severity.

### dx...@google.com (2025-11-21)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7186537>

Force relayout when constraints change to SHOWN or BOTH

---


Expand for full commit details
```
     
    The linked bug occurs due to not doing a relayout when exiting 
    fullscreen. Without the relayout, the view does not redraw despite being 
    VISIBLE and positioned in the correct location. This can occur even when 
    transitioning to the BOTH state. 
     
    Bug: 461532432 
    Change-Id: I3112a3d05c8ddaee2538d5e17880604f4374046c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7186537 
    Reviewed-by: Peilin Wang <peilinwang@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1548734}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java`

---

Hash: [044d94f7f47fe37c0fea4556f89d336307f33e0a](https://chromiumdash.appspot.com/commit/044d94f7f47fe37c0fea4556f89d336307f33e0a)  

Date: Fri Nov 21 22:42:42 2025


---

### ch...@gmail.com (2025-11-21)

Thanks as ever for the quick fix, Patrick!

### ch...@gmail.com (2025-11-24)

I just verified on Canary. Fixed.

### ch...@google.com (2025-11-25)

Security Merge Request Consideration: Requesting merge to beta (M143) because latest trunk commit (1548734) appears to be after beta branch point (1536371).
Security Merge Request - Manual Review: Merge review required: M143 has already been cut for stable release.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [143].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@google.com (2025-11-25)

1. <https://chromium-review.googlesource.com/7186537>
2. Yes
3. No
4. No
5. No
6. n/a

### ya...@google.com (2025-11-25)

Please proceed with the merge. Thanks!

### dx...@google.com (2025-11-25)

Project: chromium/src  

Branch:  refs/branch-heads/7499  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7204604>

Force relayout when constraints change to SHOWN or BOTH

---


Expand for full commit details
```
     
    The linked bug occurs due to not doing a relayout when exiting 
    fullscreen. Without the relayout, the view does not redraw despite being 
    VISIBLE and positioned in the correct location. This can occur even when 
    transitioning to the BOTH state. 
     
    (cherry picked from commit 044d94f7f47fe37c0fea4556f89d336307f33e0a) 
     
    Bug: 461532432 
    Change-Id: I3112a3d05c8ddaee2538d5e17880604f4374046c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7186537 
    Reviewed-by: Peilin Wang <peilinwang@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1548734} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7204604 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7499@{#2684} 
    Cr-Branched-From: b30439823e5177773584139e72e0593e36863899-refs/heads/main@{#1536371}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java`

---

Hash: [7b6a1c1792b8f43acf77e83971973aa074c868c9](https://chromiumdash.appspot.com/commit/7b6a1c1792b8f43acf77e83971973aa074c868c9)  

Date: Tue Nov 25 20:16:00 2025


---

### sp...@google.com (2025-12-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

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

### ch...@google.com (2026-03-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI Spoofing

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/461532432)*
