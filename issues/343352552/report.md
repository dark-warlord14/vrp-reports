# WebGL Fullscreen Security UI Bypass

| Field | Value |
|-------|-------|
| **Issue ID** | [343352552](https://issues.chromium.org/issues/343352552) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Fullscreen |
| **Platforms** | Windows |
| **Reporter** | a....@certitude.consulting |
| **Assignee** | li...@google.com |
| **Created** | 2024-05-29 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
WebGL allows malicious actors to overload GPUs and stall rendering of all Chromium/OS UI elements. Utilizing this, it is possible to obscure the dialog making users aware the browser is entering fullscreen mode (see WHATWG Fullscreen API Living Standard: users should always be informed when something is displayed in fullscreen [1]).

After a user interaction (required to use the fullscreen API), the GPU rendering can be blocked. Meanwhile the browser enters fullscreen. This is not visible to users since any rendering is stalled by resource exhaustion. After rendering has recovered, the browser should be in fullscreen, with the fullscreen notification completely skipped.

Our testing shows that the exploit only works in Windows-based systems, Linux systems are unaffected, as we were not able to reproduce the described behavior in those. This indicates that some Windows-specific implementation may be the reason for this behavior.

The exploit can be utilized for example to create convincing Windows lock-screen look-alike phishing site (if you want a more fleshed-out PoC we can provide a video and/or source code for a full demonstration).

[1] https://fullscreen.spec.whatwg.org/#security-and-privacy-considerations

VERSION
Chrome Version: 124.0.6367.208 stable
Operating System: Windows 10 Pro, 22H2

REPRODUCTION CASE
The attached file 'minimal_chrome.html' demonstrates the exploit. It may be required to adjust the STRESS, FULLSCREEN_WAIT and RENDERTIME values, depending on the device. The given values give consistent results when testing on a Lenovo Thinkpad P14s Gen 3 using the integrated Intel Iris Xe Graphics for rendering.

CREDIT INFORMATION
Reporter credit:
Wolfgang Ettlinger (aff. Certitude Consulting GmbH)
Alexander Hurbean (aff. Certitude Consulting GmbH)

## Attachments

- [minimal_chrome.html](attachments/minimal_chrome.html) (text/html, 3.7 KB)
- [fullscreen.mp4](attachments/fullscreen.mp4) (video/mp4, 61.9 MB)

## Timeline

### mp...@google.com (2024-05-30)

Thank you for your report, do you think you could attach a screen recording of your exploit?

### mp...@google.com (2024-05-31)

I'll assign to those handling fullscreen bugs. No need for a convincing spoof video, just a proof of concept video, as we are well aware of the importance of the fullscreen notification. :) Thanks again for the report!

### a....@certitude.consulting (2024-05-31)

The attached "fullscreen.mp4" is a fully working proof-of-concept attack of this bypass being used in a fullscreen phishing attack.

A user navigates to a blog and must click to accept a cookie prompt, after which the browser renders random noise (this is just "fluff" to confuse users, we render random noise to a canvas). In the background the described fullscreen abuse is running, overloading the GPU through WebGL while the browser enters fullscreen. When rendering recovers, the users find themselves on a fullscreen fake login page mimicking the Windows login, having seen no fullscreen notification.

If the full working code of the shown fullscreen phishing demo is also requested, we can supply that too gladly.

### pe...@google.com (2024-05-31)

Setting milestone because of s2 severity.

### pe...@google.com (2024-06-14)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-06-29)

takumif: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### a....@certitude.consulting (2024-07-10)

Hi!
Since we haven't had an update on this issue, we just wanted to ask for a short status update from your side.

### a....@certitude.consulting (2025-09-12)

Hi,

We saw that there is a broader approach to adressing all fullscreen issues in <https://issues.chromium.org/u/1/issues/391919449>. Could you give us a timeline on these ongoing efforts, as we would to like publish our findings.

Please note: According to our Certitude Consulting responsible disclosure policy, we normally grant the vendor 90 days to fix reported issues (it has been over a year now).

> In case a vendor is unresponsive, is uncooperative or fails to provide a patch within 90 days without a reasonable explanation, Certitude can release the advisory information without coordinating with the vendor.

Kind regards,
Alexander Hurbean

### a....@certitude.consulting (2026-02-25)

Hi,

as this vulnerability has been reported to you almost 2 years ago (May 2024) with minimal communication from your side w.r.t. the resolution of the reported vulnerability Certitude Consulting will disclose a public advisory containing details about the vulnerability on 2026-03-11.

Thank you for your understanding,
Alexander Hurbean
Certitude Consulting GmbH

### a....@certitude.consulting (2026-03-05)

Hi,

we have chosen to postpone the publication date to 2026-03-18.

Kind regards,
Alexander Hurbean
Certitude Consulting

### a....@certitude.consulting (2026-03-10)

Hi,

due to internal reasons we have chosen to futher postpone the publication date to 2026-04-02.

Kind regards,
Alexander Hurbean
Certitude Consulting

### dx...@google.com (2026-03-31)

Project: chromium/src  

Branch:  main  

Author:  Frank Liberato [liberato@chromium.org](mailto:liberato@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7615417>

Don't start the exclusive access bubble timer until commit

---


Expand for full commit details
```
     
    Bug: 343352552 
    Change-Id: If0f8704a23c51e1431f9919ea88b989f74de4a4c 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7615417 
    Reviewed-by: Mike Wasserman <msw@chromium.org> 
    Commit-Queue: Frank Liberato <liberato@chromium.org> 
    Reviewed-by: Muyao Xu <muyaoxu@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1608174}

```

---

Files:

- M `chrome/browser/ui/exclusive_access/exclusive_access_bubble.cc`
- M `chrome/browser/ui/exclusive_access/exclusive_access_bubble.h`
- M `chrome/browser/ui/exclusive_access/exclusive_access_bubble_unittest.cc`
- M `chrome/browser/ui/exclusive_access/exclusive_access_test.cc`
- M `chrome/browser/ui/exclusive_access/fullscreen_controller_interactive_browsertest.cc`
- M `chrome/browser/ui/views/exclusive_access_bubble_views.cc`
- M `chrome/browser/ui/views/exclusive_access_bubble_views.h`

---

Hash: [fdac21de070f3523b7315a268092d528a542a6d6](https://chromiumdash.appspot.com/commit/fdac21de070f3523b7315a268092d528a542a6d6)  

Date: Tue Mar 31 23:30:44 2026


---

### aj...@google.com (2026-06-04)

Low severity as this requires a period of blocking before the page becomes responsive again.

### sp...@google.com (2026-06-04)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Security UI spoofing.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-19)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/343352552)*
