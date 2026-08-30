# Intersection Observer v2 API fails to reliably determine target's visibility, which enables clickjacking against Google One Tap

| Field | Value |
|-------|-------|
| **Issue ID** | [479203484](https://issues.chromium.org/issues/479203484) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@icloud.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2026-01-27 |
| **Bounty** | $5,000.00 |

## Description

#### VULNERABILITY DETAILS

While researching variations of [issue 333708039](https://issues.chromium.org/issues/333708039), it was discovered that the Intersection Observer v2 API fails to accurately determine a target's visibility when the occluding element uses CSS 3D transforms. By placing an overlay element with `transform-style: preserve-3d` and 3D transform properties such as `translateZ` and `rotateY` above the target iframe, an attacker can trick the API into reporting the target as visible when it is actually obscured.

##### Here's a breakdown of what is currently happening:

1. Attacker creates a container with `transform-style: preserve-3d`.
2. The target iframe is placed inside this container.
3. An overlay element is placed above the iframe with CSS 3D transforms (`translateZ(1px) rotateY(1deg)`).
4. The target iframe uses Intersection Observer V2 for visibility detection with `trackVisibility: true`.
5. The observer incorrectly reports the iframe as visible, even though the overlay completely covers it visually.

Since the Intersection Observer v2 API does not reliably determine visibility in 3D transform scenarios, any applications relying on it to prevent clickjacking attacks are vulnerable. One such example is the Google One Tap SDK, which embeds an iframe that uses this API to check if its login button is visible to the user when it is clicked. If the login button is not visible, it shows a popup asking for the user's consent to log in to the website. If the login button is visible, it immediately sends the user's identity to the website, allowing an attacker to leak the user's identity.

I have also attached a video reproducing the core attack (`repro-core.mp4`) and the Google One Tap SDK attack (`repro-tap.mp4`).

#### BISECT

By doing an initial bisect, it was identified that the affected ranges are between 626286 and 626301 (<https://chromium.googlesource.com/chromium/src/+log/c9d9b04bf831ea737d25dea59a31bd4c9f870fb2..0b65cb95ed32a8737c3cf4e82d7f602ac6624987>).

The commit responsible for that was: <https://chromium.googlesource.com/chromium/src/+/0b65cb95ed32a8737c3cf4e82d7f602ac6624987>.

Looking into it, this commit enabled the IOv2 feature by default. By running the bisect again with the following command:

```
python3 bisect-builds.py -a win64 -b M76 -g M65 --verify-range -- --no-first-run --enable-blink-features=IntersectionObserverV2 --user-data-dir=/tmp http://localhost:8080/bypass.html

```

I was able to narrow it down to these changes:
<https://chromium.googlesource.com/chromium/src/+log/1c149502277c1441eec693c3ec160462e150000b..4acd4805db0d79872a6ec904e28f1587bada7389>

After investigating, it became clear that the commit that introduced the issue is <https://chromium.googlesource.com/chromium/src/+/7bb6c9acc4a534866c72afb15c2ca33a3f78e34f>.

#### VERSION

Chrome Version: 144.0.7559.97 (Stable)   

Chrome Version: 145.0.7632.18 (Beta)   

Chrome Version: 146.0.7647.4 (Dev)   

Chrome Version: 146.0.7653.0 (Canary)   

Operating System: Windows 11 24H2

#### REPRODUCTION CASE

##### Steps to setup the PoC

1. Download the following files: `bypass.html`, `expected-overlay.html`, `frame.html`, `gis.html` and `google-clickjacking.html`.
2. Move all files into the same folder.
3. Serve the files using a web server on port 8080 (this is important because `localhost:8080` has been added as an allowed origin in Google One Tap, which is required for it to work).

##### Steps to reproduce the core issue

1. Go to <http://localhost:8080/expected-overlay.html> to verify how the Intersection Observer V2 API behaves when the target iframe is covered by an overlay. It should show a red background.
2. Go to <http://localhost:8080/bypass.html> to reproduce the issue. Even though the iframe is covered by an overlay, the background still appears green.

##### Steps to reproduce the Google One Tap PoC

1. Make sure you are logged into your Google Account.
2. Navigate to <http://localhost:8080/google-clickjacking.html> and click the button.
3. Notice that your identity is leaked to the attacker's page.

#### CREDIT INFORMATION

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [bypass.html](attachments/bypass.html) (text/html, 1.3 KB)
- [expected-overlay.html](attachments/expected-overlay.html) (text/html, 892 B)
- [frame.html](attachments/frame.html) (text/html, 2.0 KB)
- [gis.html](attachments/gis.html) (text/html, 974 B)
- [google-clickjacking.html](attachments/google-clickjacking.html) (text/html, 2.8 KB)
- [repro-core.mp4](attachments/repro-core.mp4) (video/mp4, 17.8 MB)
- [repro-tap.mp4](attachments/repro-tap.mp4) (video/mp4, 13.6 MB)

## Timeline

### el...@google.com (2026-01-27)

Security shepherd: thanks for the report. I haven't run your POC myself but the video looks convincing, as does the analysis of the bug. I'm routing this to szager@ who fixed issue 333708039.

### el...@google.com (2026-01-27)

Speculatively marking this as affecting desktop 144+ based on the report, too.

### ch...@google.com (2026-01-28)

The Found In field may only contain numeric values.
Some values couldn't be corrected but were removed, please verify that any important data wasn't lost.
You can see the changes by toggling full history on the issue.

### ch...@google.com (2026-01-29)

Setting milestone because of s2 severity.

### ch...@google.com (2026-02-11)

szager: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-02-26)

szager: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-03-13)

szager: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2026-05-12)

Project: chromium/src  

Branch:  main  

Author:  Stefan Zager [szager@chromium.org](mailto:szager@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7835432>

[IntersectionObserver] Fix occlusion detection with 3D transform

---


Expand for full commit details
```
     
    For regular (i.e. event-targeting) hit testing, z-axis ordering is 
    based on the z-axis position of the center of a PaintLayer. That's 
    not good enough for occlusion testing. 
     
    With this CL, when a hit test for occlusion encounters a 3d transform, 
    it computes the z-axis position of the four corners of the PaintLayer, 
    and if any of them are above any point in the occlusion target (i.e. 
    the HitTestRequest::stop_node_) then the PaintLayer is considered 
    occluding. This is not 100% accurate, but it will never result in a 
    false positive (i.e., reporting the target as unoccluded when it 
    actually is), which is a hard requirement of IntersectionObserver. 
     
    The corner-checking code makes a simplifying assumption that the 
    stop_node_ has no 3D projection, which is enforced by a call to 
    LayoutObject::HasDistortingVisualEffects from IntersectionObserver. 
     
    Bug: 479203484 
    Change-Id: Ida70f919efc73149d32112900b019987f27a5a7e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7835432 
    Reviewed-by: Philip Rogers <pdr@chromium.org> 
    Commit-Queue: Stefan Zager <szager@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1629048}

```

---

Files:

- M `third_party/blink/renderer/core/layout/hit_testing_test.cc`
- M `third_party/blink/renderer/core/paint/paint_layer.cc`
- A `third_party/blink/web_tests/external/wpt/intersection-observer/v2/3d-transform-occlusion.html`

---

Hash: [bd827703400c306193f3a9e5ca30abc3f694147c](https://chromiumdash.appspot.com/commit/bd827703400c306193f3a9e5ca30abc3f694147c)  

Date: Tue May 12 04:33:55 2026


---

### dx...@google.com (2026-05-18)

Project: chromium/src  

Branch:  main  

Author:  Philip Rogers [pdr@chromium.org](mailto:pdr@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7854105>

Fix occlusion by not overwriting z\_offset in IsHitCandidateForDepthOrder

---


Expand for full commit details
```
     
    https://crrev.com/1629048 introduced an intersection observer v2 
    regression due to z_offset being overwritten with smaller values. This 
    patch ensure z_offset only increases. 
     
    Bug: 479203484 
    Fixed: 513624405 
    Change-Id: Ic5b3b8633979cf7ffeb57f9739e8fe4dd9417518 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7854105 
    Reviewed-by: Stefan Zager <szager@chromium.org> 
    Commit-Queue: Philip Rogers <pdr@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1632217}

```

---

Files:

- M `third_party/blink/renderer/core/paint/paint_layer.cc`
- A `third_party/blink/web_tests/external/wpt/intersection-observer/v2/3d-transform-occlusion-2.html`

---

Hash: [70cf74a48fd1dabef56cd3f83e6930ad78a92874](https://chromiumdash.appspot.com/commit/70cf74a48fd1dabef56cd3f83e6930ad78a92874)  

Date: Mon May 18 16:36:53 2026


---

### sp...@google.com (2026-06-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
Baseline. Security UI spoofiing with Bisect.


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-08-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/479203484)*
