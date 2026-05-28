# Intersection Observer v2 API fails to correctly determine target's visibility for dynamically changed z-indexes, enabling clickjacking against Google One Tap

| Field | Value |
|-------|-------|
| **Issue ID** | [422531206](https://issues.chromium.org/issues/422531206) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Linux, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | pd...@chromium.org |
| **Created** | 2025-06-05 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

While researching variations of [issue 333708039](https://issues.chromium.org/issues/333708039), it was discovered that the Intersection Observer v2 API fails to accurately determine a target's visibility. By initially placing an overlay element with a low z-index beneath the target iframe, and then dynamically changing or removing the overlay's z-index to bring it above the target after the page loads, an attacker can trick the API into reporting the target as visible when it is actually obscured.

##### Here's a breakdown of what is currently happening:

1. Attacker creates an overlay element with `z-index: "-9999"` positioned below the target iframe.
2. The target iframe uses Intersection Observer V2 for visibility detection.
3. The observer correctly reports the iframe as visible (since the overlay is below it).
4. Attacker changes the overlay’s z-index via JavaScript using `overlay.style.zIndex = "9999"`.
5. The overlay moves above the iframe in the stacking order.
6. The observer still reports the iframe as visible, even though it is now covered.

Since the Intersection Observer v2 API does not reliably determine visibility, any applications relying on it to prevent clickjacking attacks are vulnerable. One such example is the Google One Tap SDK, which embeds an iframe that uses this API to check if its login button is visible to the user when it is clicked. If the login button is not visible, it shows a popup asking for the user's consent to log in to the website. If the login button is visible, it immediately sends the user's identity to the website, allowing an attacker to leak the user's identity.

I have also attached a video reproducing the core attack (`repro-core.mov`) and the Google One Tap SDK attack (`repro-tap.mov`).

#### BISECT

By doing an initial bisect, I confirmed that the issue was not working on version 120.0.6099.56 (stable) and that the vulnerability started working on version 121.0.6167.75 (stable).

The commit responsible for that was: <https://chromium.googlesource.com/chromium/src/+/f0d3627a2514f7119906da2012b59f6597d8605b>

Looking into it, this commit enabled the IntersectionOptimization feature. By running the bisect again with the following command:

```
python3 bisect-builds.py -a mac -g m120 -b m121 --verify-range -- --enable-features=IntersectionOptimization --no-first-run --user-data-dir=/tmp http://localhost:8080/bypass.html

```

I was able to narrow it down to these changes:
<https://chromium.googlesource.com/chromium/src/+log/00ceb304e8ef1a64ee7ccfb25ce6deb39f5135c3..3e2df989cf54598113c005155dc9c75995c8177b>

After investigating, it became clear that the commit that introduced the issue is:
<https://chromium.googlesource.com/chromium/src/+/e90de993ac2b3222e6b1d6d993922a13273fae8d>

#### VERSION

Chrome Version: 137.0.7151.69 (Stable)   

Chrome Version: 139.0.7219.0 (Canary)   

Operating System: macOS 14.1.1 (23B81)

#### REPRODUCTION CASE

##### Steps to setup the PoC

1. Download the following files: `bypass.html`, `expected-no-overlay.html`, `expected-overlay.html`, `frame.html`, `gis.html`, `google-clickjacking.html`, and `cat.jpg`.
2. Move all files into the same folder.
3. Serve the files using a web server on port 8080 (this is important because localhost:8080 has been added as an allowed origin in Google One Tap, which is required for it to work).

##### Steps to reproduce the core issue

1. Go to <http://localhost:8080/expected-overlay.html> to verify how the Intersection Observer V2 API behaves when the target iframe is covered by an overlay. It should show a red background.
2. Go to <http://localhost:8080/expected-no-overlay.html> to verify how the API behaves when there is no overlay. It should show a green background.
3. Go to <http://localhost:8080/bypass.html> to reproduce the issue. Even though the iframe is covered by an overlay, the background still appears green.

##### Steps to reproduce the Google One Tap PoC

1. Make sure you are logged into your Google Account.
2. Navigate to <http://localhost:8080/google-clickjacking.html> and click the button.
3. Notice that your identity is leaked to the attacker's page.

#### CREDIT INFORMATION

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [bypass.html](attachments/bypass.html) (text/html, 1.4 KB)
- [cat.jpg](attachments/cat.jpg) (image/jpeg, 236.6 KB)
- [expected-no-overlay.html](attachments/expected-no-overlay.html) (text/html, 648 B)
- [expected-overlay.html](attachments/expected-overlay.html) (text/html, 1.0 KB)
- [frame.html](attachments/frame.html) (text/html, 1.3 KB)
- [gis.html](attachments/gis.html) (text/html, 945 B)
- [google-clickjacking.html](attachments/google-clickjacking.html) (text/html, 3.1 KB)
- [repro-tap.mov](attachments/repro-tap.mov) (video/quicktime, 1.7 MB)
- [repro-core.mov](attachments/repro-core.mov) (video/quicktime, 9.8 MB)

## Timeline

### sk...@google.com (2025-06-05)

Thank you for the bug report! I reproduced this on Linux M137 Stable. Setting the same severity/priority and owner as https://g-issues.chromium.org/issues/333708039

### ch...@google.com (2025-06-05)

Setting milestone because of s2 severity.

### ch...@google.com (2025-06-25)

szager: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-10)

szager: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-07-25)

szager: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-09)

szager: Uh oh! This issue still open and hasn't been updated in the last 58 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-08-24)

szager: Uh oh! This issue still open and hasn't been updated in the last 73 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-08)

szager: Uh oh! This issue still open and hasn't been updated in the last 88 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-23)

szager: Uh oh! This issue still open and hasn't been updated in the last 104 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-08)

szager: Uh oh! This issue still open and hasn't been updated in the last 119 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-10-23)

szager: Uh oh! This issue still open and hasn't been updated in the last 134 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pd...@chromium.org (2025-11-05)

z-index invalidations are handled [here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/paint_layer.cc;drc=9569250cb866392ff93b7664b7b5974f88d4a3fc;l=2363). Maybe we need a call to `SetIntersectionObservationState`? This should already happen for paint invalidation via [this](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/paint/pre_paint_tree_walk.cc;drc=e9787bf37665a37b5c7f09c2cca23a7443c317dc;l=636) but maybe we avoid paint invalidation in this case?

### ch...@google.com (2025-11-07)

szager: Uh oh! This issue still open and hasn't been updated in the last 148 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-11-22)

szager: Uh oh! This issue still open and hasn't been updated in the last 163 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pd...@google.com (2025-11-30)

Stefan, should this be P1?

### ch...@google.com (2025-12-07)

szager: Uh oh! This issue still open and hasn't been updated in the last 178 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-12-22)

szager: Uh oh! This issue still open and hasn't been updated in the last 193 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-06)

szager: Uh oh! This issue still open and hasn't been updated in the last 208 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-01-08)

Project: chromium/src  

Branch:  main  

Author:  Philip Rogers [pdr@chromium.org](mailto:pdr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7411729>

Recompute intersection observations on z-index changes

---


Expand for full commit details
```
     
    Intersection observations are recomputed when paint is invalidated (see 
    PaintInvalidator::InvalidatePaint), but z-index changes do not always 
    invalidate paint, so we need to ensure intersection observations are 
    recomputed in those cases. 
     
    Fixed: 422531206 
    Change-Id: I6101353f459fa1579136155f278a28ff4ec2e595 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7411729 
    Commit-Queue: Philip Rogers <pdr@chromium.org> 
    Auto-Submit: Philip Rogers <pdr@chromium.org> 
    Reviewed-by: Stefan Zager <szager@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1565993}

```

---

Files:

- M `third_party/blink/renderer/core/paint/paint_layer.cc`
- A `third_party/blink/web_tests/external/wpt/intersection-observer/v2/z-index-changes.html`

---

Hash: [50046fdcc3b66587530d7ec09e8f58c8b467a755](https://chromiumdash.appspot.com/commit/50046fdcc3b66587530d7ec09e8f58c8b467a755)  

Date: Thu Jan 8 00:11:29 2026


---

### sp...@google.com (2026-01-16)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high quality web platform privilege escalation with a bisect bonus


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### he...@gmail.com (2026-01-26)

Hey, thanks for the reward!

I just wanted to ask a quick clarifying question before wrapping things up. Could you please let me know whether the bisect bonus was factored into this reward? Specifically, was this assessed as a $4,000 issue with an additional $1,000 bisect bonus, or was it evaluated as a single $5,000 issue?

I'm asking, given that in my opinion, this was a 1:1 variant of [bug 333708039](https://issues.chromium.org/issues/333708039), which was awarded $5,000 without a bisect. I had initially expected a similar total for this report as well (plus the $1,000 bisect bonus).

I just wanted to confirm whether the bisect was already factored in the calculation ($4,000 + $1,000) or if it may have been overlooked.

Thanks again!

### wf...@chromium.org (2026-02-04)

The panel confirmed that the reward here was $4000 for the Web platform privilege escalation and a $1000 bisect bonus.

### he...@gmail.com (2026-02-04)

Bummer, but thanks for confirming.

### ch...@google.com (2026-04-17)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/422531206)*
