# Intersection Observer v2 API fails to reliably determine target's visibility, which enables clickjacking against Google One Tap

| Field | Value |
|-------|-------|
| **Issue ID** | [333708039](https://issues.chromium.org/issues/333708039) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Geometry |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | lo...@icloud.com |
| **Assignee** | sz...@chromium.org |
| **Created** | 2024-04-10 |
| **Bounty** | $5,000.00 |

## Description

VULNERABILITY DETAILS

The [Intersection Observer v2 API](https://web.dev/articles/intersectionobserver-v2) fails to correctly and reliably determine a target's visibility. The API determines that a target is visible, although it is hidden, i.e., by setting the opacity down to 0%.

The [Google One Tap SDK](https://developers.google.com/identity/gsi/web/guides/display-google-one-tap) embeds an iframe that uses this API to determine if its login button is visible to a user. If the login button is not visible, the button triggers a popup to appear that asks for the user's consent to log in to the website. If the login button is visible, the button immediately triggers the iframe to issue the user's identity to the website.

Since the Intersection Observer v2 API does not reliably determine the login button's visibility, clickjacking attacks are possible. Some malicious website can trick the victim into clicking the invisible login button of the GOT SDK, followed by Google issuing the victim's identity to the malicious website (= deanonymization).

While testing, I noticed that the API works in some cases, which might be due to caching / race condition. For example, if a.com frames a.com, then the API works as expected. However, when b.com frames a.com and a.com uses the API, then the visibility is reported inaccurate in most cases.

For example, start an incognito window and open the [same-site case](https://pocs.work/tools/framer/#https://pocs.work/demo/intersection-observer-v2/frame.html). The iframe should detect that its not visible (= red background). Now close it, start a new incognito window, and open the [cross-site case](https://pocs.lol/tools/framer/#https://pocs.work/demo/intersection-observer-v2/frame.html). The iframe should fail to detect that it is not visible (= green background).

VERSION

Chrome Version: 123.0.6312.107 stable

Operating System: macOS 14.3.1 (23D60)

REPRODUCTION CASE

- Create a clean chrome profile (no cache, default configs, etc.)
- Sign in to your Google account
- Go to <https://pocs.lol/pocs/2024/google-one-tap-clickjacking/>
- Click on the "click me to see funny cats" button
- Wait a few seconds
- Your email should appear on the website

See the video for a demonstration.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Louis Jannett (Ruhr University Bochum)

## Attachments

- [google-one-tap-clickjacking.mov](attachments/google-one-tap-clickjacking.mov) (video/quicktime, 20.8 MB)
- [intersection-observer-v2-poc.mov](attachments/intersection-observer-v2-poc.mov) (video/quicktime, 88.3 MB)
- [intersection-observer-v2-poc-ubuntu.mov](attachments/intersection-observer-v2-poc-ubuntu.mov) (video/quicktime, 64.4 MB)
- [poc-intersection-observer-v2-resize.mov](attachments/poc-intersection-observer-v2-resize.mov) (video/quicktime, 36.6 MB)

## Timeline

### an...@chromium.org (2024-04-10)

Thank you for the PoC and video. chrishtr@, can you take a look at this? Please feel free to re-route if necessary.

### pe...@google.com (2024-04-11)

Setting milestone because of s2 severity.

### pe...@google.com (2024-04-11)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sz...@chromium.org (2024-04-11)

I'm looking into this. I haven't been able to reproduce the behavior with the minimized test cases, but I do see the problem with the Google Single Sign-On. At this point I can't tell whether the issue is in the javascript on that site or in the IntersectionObserver V2 implementation.

### lo...@icloud.com (2024-04-12)

Thanks for taking a look at this. AFAIK it should be an issue with the Intersection Observer v2, as in some cases, it fails to detect that the observing element is not visible.

Please try following to reproduce the issue:

- Create a new profile or clear cache and site data
- Go to <https://pocs.work/tools/framer/#https://pocs.work/demo/intersection-observer-v2/frame.html>
  - You should see an iframe with a red background, meaning that the Observer v2 detected that it's not visible -> correct behavior
- Go to <https://pocs.lol/tools/framer/#https://pocs.work/demo/intersection-observer-v2/frame.html>
  - You should see an iframe with a green background, meaning that the Observer v2 *failed* to detect that it's not visible -> bug

IMHO, it's some sort of caching issue, since after refreshing several times, it's sometimes working as expected again. I tested it on macOS and Linux.

The Google SSO just makes use of this API to prevent clickjacking, but since it does not work reliably, clickjacking attacks are possible (see other poc video).

I attached another PoC video that shows the unexpected Observer v2 API behavior. Note that this PoC uses the same JavaScript implementation as the [blog post](https://web.dev/articles/intersectionobserver-v2), so there should not be an issue with that.

### lo...@icloud.com (2024-04-12)

Here's a PoC video with the latest version of Chromium on Ubuntu 22.04.3 LTS.

### lo...@icloud.com (2024-04-12)

Also, it seems that as soon as the window is resized (or scrolled), the Observer v2 starts to refresh (recalculate its visibility) and then detects that it is not visible anymore, see the attached poc video.

### pe...@google.com (2024-05-09)

szager: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-05-16)

Project: chromium/src
Branch: main

commit 78bd1f0eef2612f22dac87d0335e8714a0ecee89
Author: Stefan Zager <szager@chromium.org>
Date:   Thu May 16 05:52:33 2024

    [IntersectionObservation] Fix needs_occlusion_tracking bookkeeping
    
    This fixes three related bugs in occlusion tracking:
    
    1. When an IntersectionObserver using trackVisibility is created in an
    OOPIF, there is some latency in notifying the parent renderer that
    occlusion tracking is required for the iframe. During that interval,
    the parent renderer might send a 'guaranteed not occluded' message to
    the child, causing the IntersectionObserver to report a false
    positive. With this change, we will never tell an OOPIF that it's
    "guaranteed not occluded" if the OOPIF hasn't requested occlusion
    information. This is fixed in frame_view.cc.
    
    2. When an OOPIF runs LocalFrameView::RunIntersectionObserverSteps,
    it might get a transient `false` value when recomputing
    needs_occlusion_tracking, due to an early return from
    UpdateViewportIntersectionsForSubtree (which has a couple of
    early-return edge cases). When that happens, we should *not* relay
    the `false` value back to the parent process, because it can create
    a temporary gap in occlusion reporting from the parent. We should
    instead preserve the previous value until it can be successfully
    recomputed on a subsequent BeginMainFrame. This is fixed in
    local_frame_view.cc.
    
    2. For OOPIF's, needs_occlusion_tracking is stored in two places:
    on RemoteFrameOwner::needs_occlusion_tracking_ in the iframe process,
    and in RemoteFrameView::needs_occlusion_tracking_ in the parent
    process. When the first one changes in the iframe process, it IPC's
    to the parent process to synchronize the second one. To keep them
    consistent, there should be no other point of entry into
    RemoteFrameView::SetNeedsOcclusionTracking. Currently, that method is
    also called from RemoteFrameView::Dispose, but that call is unnecessary
    and it can cause the two values to get out of sync. This is fixed in
    remote_frame_view.cc.
    
    Bug: chromium:333708039
    Change-Id: Id1dd08eefb5aa201651b2c6950ea61f3b4a081a9
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5540331
    Commit-Queue: Stefan Zager <szager@chromium.org>
    Reviewed-by: Xianzhu Wang <wangxianzhu@chromium.org>
    Cr-Commit-Position: refs/heads/main@{#1301762}

M       third_party/blink/renderer/core/frame/frame_view.cc
M       third_party/blink/renderer/core/frame/local_frame_view.cc
M       third_party/blink/renderer/core/frame/remote_frame_view.cc
M       third_party/blink/web_tests/TestExpectations

https://chromium-review.googlesource.com/5540331


### sz...@chromium.org (2024-05-20)

louisjannett@ -- thank you for the bug report and the excellent reproduction, which helped greatly in debugging. With the fix from May 16, I can no longer reproduce the bug. The fix is available in the current dev channel release on Mac (127.0.6485.0), if you'd like to try it out.

### lo...@icloud.com (2024-05-21)

Thanks for resolving the vulnerability. I can confirm that it is fixed in 127.0.6485.0 (Official Build) dev (arm64).

### pe...@google.com (2024-06-04)

szager: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-06-13)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
$5,000 for high quality report (with functional exploit) of user information disclosure 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-06-13)

Congratulations Louis! Thank you for your efforts and reporting this issue to us. In the future (which we hope you'll report bugs to us in :) please kindly upload the POC directly to the report and avoid linking it. We do not want to encourage or provide the opportunity for engineers or others to click arbitrary links to potentially malicious web content. Separate POC files should be included so that can easily scp that file to our contained VMs for reproduction and investigation.
Thank you and nice work!

### lo...@icloud.com (2024-06-14)

Awesome, thanks for the reward! Alright, I will upload the PoC from now on.

### pe...@google.com (2024-09-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/333708039)*
