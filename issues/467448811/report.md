# Mini bar not rendered when omnibox is hidden (similar to issue 461532432)

| Field | Value |
|-------|-------|
| **Issue ID** | [467448811](https://issues.chromium.org/issues/467448811) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile>Toolbar |
| **Platforms** | Android |
| **Chrome Version** | 145.0.0.0 |
| **Reporter** | ch...@gmail.com |
| **Assignee** | pn...@google.com |
| **Created** | 2025-12-10 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Open the testcase.
2. Scroll down to the middle of the page until the omnibox disappears (normal fullscreen scroll behavior).
3. Tap inside the <textarea>.

# Problem Description

This issue appears very similar to Chromium [issue 461532432](https://issues.chromium.org/issues/461532432).

In Chrome Canary on Android, when the omnibox auto-hides during scroll, tapping inside a <textarea> causes the keyboard’s accessory bar (the mini bar above the virtual keyboard) to not render at all.
The space where the accessory bar normally appears is still allocated, but it is completely empty (no icons, no background, just blank UI).

This empty UI zone appears exactly where a user expects browser controls.
A website can use CSS to place a fake omnibox just below it, enabling UI spoofing.

# Summary

Mini bar not rendered when omnibox is hidden (similar to [issue 461532432](https://issues.chromium.org/issues/461532432))

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A \

## Attachments

- [testcase.html](attachments/testcase.html) (text/html, 3.3 KB)
- [screen-20251210-152442.mp4](attachments/screen-20251210-152442.mp4) (video/mp4, 3.5 MB)

## Timeline

### ch...@gmail.com (2025-12-10)

Tested on a Pixel 9 Pro XL, where the issue is consistently reproducible.

### li...@chromium.org (2025-12-10)

Reassigning to @pn...@google.com due to similarity to [crbug.com/461532432](https://crbug.com/461532432) -- do you mind taking a look at this?

### pn...@google.com (2025-12-10)

Reporter, are you able to repro in Chrome Stable M142 or M143? Trying to figure out if a recent change is to blame here.

### pn...@google.com (2025-12-10)

To be clear this is actionable without that piece of data, but it would help me narrow things down.

### ch...@gmail.com (2025-12-10)

No, I couldn't repro this in Stable or Dev.

### pe...@google.com (2025-12-10)

Thank you for providing more feedback. Adding the requester to the CC list.

### pn...@google.com (2025-12-10)

I think this is actually a symptom of a larger issue, which is that the bottom controls don't scroll off at all in Canary. We show the native texture, but fail to ever adjust its position.

### pn...@google.com (2025-12-10)

> I think this is actually a symptom of a larger issue, which is that the bottom controls don't scroll off at all in Canary. We show the native texture, but fail to ever adjust its position.

Nevermind, these are independent. Disabling BCIV fixes the "bottom controls don't scroll off" issue, but the invisible mini origin bar can still occur.

### ch...@google.com (2025-12-11)

Setting milestone because of s2 severity.

### dx...@google.com (2025-12-11)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7253201>

Force relayout for tab-driven constraint changes

---


Expand for full commit details
```
     
    This logic currently only runs for browserdelegate-driven constraint 
    changes, which misses e.g. form-field focus driven SHOWN. 
     
    Bug: 467448811 
    Change-Id: I5662353216c8faea84a98e2f3edfa584cd6adf2c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7253201 
    Reviewed-by: Wenyu Fu <wenyufu@chromium.org> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1557729}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManagerUnitTest.java`

---

Hash: [d9cb337ff4a744969259fa8cac73512f4f5fe2a4](https://chromiumdash.appspot.com/commit/d9cb337ff4a744969259fa8cac73512f4f5fe2a4)  

Date: Thu Dec 11 23:20:05 2025


---

### pe...@google.com (2025-12-12)

The NextAction date has arrived: 2025-12-12
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### pn...@google.com (2025-12-12)

Reporter, are you able to repro on the latest Canary (7576) ?

### ch...@gmail.com (2025-12-12)

I am no longer able to repro on 145.0.7576.0. 

### ch...@google.com (2025-12-13)

Security Merge Request Consideration: Requesting merge to beta (M144) because latest trunk commit (1557729) appears to be after beta branch point (1552494).
Security Merge Request - Manual Review: Merge review required: M144 is already shipping to beta.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [144].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### pn...@google.com (2025-12-15)

Disclaimer: we were never able to repro this on M144, but I can't prove that it isn't possible. The fix didn't seem related to recent code changes, although again I can't guarantee that it wasn't; the browser controls system is complex.

1. <https://chromium-review.googlesource.com/7253201>
2. Yes
3. No
4. No
5. No
6. n/a

### dr...@chromium.org (2025-12-16)

No crashes seen in Canary, approving merge for M144.

### dx...@google.com (2025-12-16)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7266391>

[M144] Force relayout for tab-driven constraint changes

---


Expand for full commit details
```
     
    This logic currently only runs for browserdelegate-driven constraint 
    changes, which misses e.g. form-field focus driven SHOWN. 
     
    (cherry picked from commit d9cb337ff4a744969259fa8cac73512f4f5fe2a4) 
     
    Bug: 467448811 
    Change-Id: I5662353216c8faea84a98e2f3edfa584cd6adf2c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7253201 
    Reviewed-by: Wenyu Fu <wenyufu@chromium.org> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1557729} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7266391 
    Cr-Commit-Position: refs/branch-heads/7559@{#1439} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManager.java`
- M `chrome/android/junit/src/org/chromium/chrome/browser/fullscreen/BrowserControlsManagerUnitTest.java`

---

Hash: [5f5a87faefd6ed513d9959f8d85b61b32ff2ed4c](https://chromiumdash.appspot.com/commit/5f5a87faefd6ed513d9959f8d85b61b32ff2ed4c)  

Date: Tue Dec 16 22:45:50 2025


---

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Security UI spoofing baseline lower impact


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2025-12-22)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-26)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### go...@google.com (2026-01-05)

Please merge your change to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable release on Wednesday, Jan 7th.  Thank you.

### pn...@google.com (2026-01-05)

This was merged (<https://chromium-review.googlesource.com/c/chromium/src/+/7266391>) but the correct tag wasn't applied

### dx...@google.com (2026-01-05)

Project: chromium/src  

Branch:  main  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7392925>

Change tool mode for image gen w/ attachment

---


Expand for full commit details
```
     
    Bug: 467448811 
    Change-Id: I0432cffa1c413ce4ff6d6ac37dccbacb8fc586d0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7392925 
    Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1564576}

```

---

Files:

- M `chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/suggestions/AutocompleteMediator.java`
- M `components/omnibox/browser/android/java/src/org/chromium/components/omnibox/AutocompleteInput.java`
- M `components/omnibox/browser/android/java/src/org/chromium/components/omnibox/AutocompleteInputUnitTest.java`

---

Hash: [d84397c9f79864b31baf2ca6b443957a69c82f92](https://chromiumdash.appspot.com/commit/d84397c9f79864b31baf2ca6b443957a69c82f92)  

Date: Mon Jan 5 20:55:35 2026


---

### pn...@google.com (2026-01-05)

Woops, tagged the wrong bug. That change is not related to this bug.

### dx...@google.com (2026-01-06)

Project: chromium/src  

Branch:  main  

Author:  Tomasz Wiszkowski [ender@google.com](mailto:ender@google.com)  

Link:    <https://chromium-review.googlesource.com/7399025>

Show canned suggestions in NB mode.

---


Expand for full commit details
```
     
    So it turns out that canned suggestions work only if suggest signals 
    are not passed. Who knew. 
     
    Bug: 467448811 
    Change-Id: I42955dceeb0c818cae0b413e631a5b6d3fb8ed0f 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7399025 
    Commit-Queue: Tomasz Wiszkowski <ender@google.com> 
    Reviewed-by: Patrick Noland <pnoland@chromium.org> 
    Auto-Submit: Tomasz Wiszkowski <ender@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1564996}

```

---

Files:

- M `chrome/browser/android/omnibox/autocomplete_controller_android.cc`

---

Hash: [f7d3652cdf832b6ff140d13ab34b4cdced91d9ba](https://chromiumdash.appspot.com/commit/f7d3652cdf832b6ff140d13ab34b4cdced91d9ba)  

Date: Tue Jan 6 16:18:25 2026


---

### dx...@google.com (2026-01-06)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Patrick Noland [pnoland@google.com](mailto:pnoland@google.com)  

Link:    <https://chromium-review.googlesource.com/7397001>

[M144] Change tool mode for image gen w/ attachment

---


Expand for full commit details
```
     
    Original change's description: 
    > Change tool mode for image gen w/ attachment 
    >  
    > Bug: 467448811 
    > Change-Id: I0432cffa1c413ce4ff6d6ac37dccbacb8fc586d0 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7392925 
    > Reviewed-by: Tomasz Wiszkowski <ender@google.com> 
    > Commit-Queue: Patrick Noland <pnoland@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1564576} 
     
    (cherry picked from commit d84397c9f79864b31baf2ca6b443957a69c82f92) 
     
    Bug: 473811754,467448811 
    Change-Id: I0432cffa1c413ce4ff6d6ac37dccbacb8fc586d0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7397001 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Chrome Cherry Picker <chrome-cherry-picker@chops-service-accounts.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/branch-heads/7559@{#3112} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `chrome/browser/ui/android/omnibox/java/src/org/chromium/chrome/browser/omnibox/suggestions/AutocompleteMediator.java`
- M `components/omnibox/browser/android/java/src/org/chromium/components/omnibox/AutocompleteInput.java`
- M `components/omnibox/browser/android/java/src/org/chromium/components/omnibox/AutocompleteInputUnitTest.java`

---

Hash: [e254526e9836a425a5e93d3eca798e91acc0e763](https://chromiumdash.appspot.com/commit/e254526e9836a425a5e93d3eca798e91acc0e763)  

Date: Tue Jan 6 18:25:34 2026


---

### ch...@google.com (2026-03-21)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> Security UI spoofing baseline lower impact

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/467448811)*
