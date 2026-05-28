# User can unknowingly Execute External File Hidden behind PiP during Interaction

| Field | Value |
|-------|-------|
| **Issue ID** | [363930141](https://issues.chromium.org/issues/363930141) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Media>PictureInPicture |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2024-09-02 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

-------------------------

VULNERABILITY DETAILS
An attacker can exploit a combination of opening a Picture-in-Picture (PiP) window and a hidden popup behind it. By manipulating the focus onto the concealed popup, an attacker can hijack keypresses when a user interacts with the website. This could lead to the unintended execution of a downloaded file. When the PiP window is closed on top of the downloaded file, the browser automatically shifts focus to this file, and with just two Enter key presses, the victim could unknowingly execute the file.

Using the method mentioned above, I have crafted an engaging game that requires the user to click on the PiP window to gather rewards and then asks the victim to press Enter twice to claim these rewards.

VERSION
Chrome Version: 128.0.6613.114 (Official Build) (64-bit)
Operating System: Windows 11

REPRODUCTION CASE
1. Download the attached `poc.html` file.
2. Open the `poc.html` file in the latest Chromium browser.
3. Interact with the game and observe how the executable is successfully launched without the user's awareness.

In this proof of concept, I used an example executable file from Sysinternals: [adrestore.exe](https://live.sysinternals.com/adrestore.exe). However, this could be any arbitrary executable. The files are opened behind the PiP window, and when the user presses Enter twice, the first Enter closes the PiP window, and the second Enter opens the executable. This interaction can also occur without PiP, as any popup opened and closed in front of a downloaded file will automatically focus on the downloaded file, allowing the Enter key to initiate the launch of the file.

Please attach files directly, not in zip or other archive formats, and if you've created a demonstration site please also attach the files needed to reproduce the demonstration locally.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: Shaheen Fazim

## Attachments

- [screenrecord.mp4](attachments/screenrecord.mp4) (video/mp4, 2.0 MB)
- [poc.html](attachments/poc.html) (text/html, 5.3 KB)
- [screenrecording.mp4](attachments/screenrecording.mp4) (video/mp4, 1.4 MB)

## Timeline

### ad...@google.com (2024-09-02)

I can reproduce this (more or less) on OS X Chrome 128. The second enter key press doesn't launch `adrestore.exe`, but enter then space bar would have done so.

I'm not completely sure I regard this particular flow as a valid spoof. The second enter press (or space in the case of OS X) does occur when the downloads list is visible. But still, the downloads list does seem like an especially security-critical surface, and it's bad if it's displayed behind PiP. I'm going to rate this as Medium severity provisionally since, although this flow is hard would be hard to convince users to do, the consequence is directly executing downloaded code outside the sandbox.

I'm going to initially send this to the Downloads team who will have better ideas about the expected layering between the downloads and PiP layers - Downloads folks, you may want to send it through to the PiP team after adding whatever comments are appropriate.

### pe...@google.com (2024-09-02)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-02)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### xi...@chromium.org (2024-09-03)

Thanks for the report. S2 seems reasonable since it is aligned with the previous clickjacking report on the download UI (<https://crbug.com/40927191>).

I can reproduce on Linux as well. It requires the partial view to be displaying when pressing 'Enter', so it needs to be pressed within 5 seconds after the download completes.

We already have clickjacking protection when the main button is pressed[1]. However, this is not effective here, because when VisibilityChanged[2] is called with is\_visible set to true, the view is actually still blocked by the PiP window. In other words, the download UI thought that the user has seen the UI for more than 0.5 seconds, but the user actually didn't see it.

+liberato@, could you take a look? It seems related to <https://crbug.com/40947034>. Thanks!

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc;drc=02c4c92d88aecbc14e715fd7fcac842d5dd814fe;bpv=1;bpt=1;l=828>
[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc;l=766;drc=02c4c92d88aecbc14e715fd7fcac842d5dd814fe;bpv=1;bpt=1>

### ja...@chromium.org (2024-09-12)

[secondary security shepherd]

Hi liberato@, could you take a look at [comment#5](https://issues.chromium.org/issues/363930141#comment5) and respond? Thank you!

### li...@google.com (2024-09-12)

we have some notion of pip windows occluding sensitive ui [1]. the download bubble probably just needs to register as a pip occlusion observer, and use that as part of its visibility calculation.

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/picture_in_picture/picture_in_picture_occlusion_observer.h;drc=5685dad7ee8f3149df55ccca6b559d4d65b4d022;l=11>

### pe...@google.com (2024-09-29)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-10-14)

liberato: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2024-10-22)

Hi liberato@, can you check out this issue?

### fa...@gmail.com (2025-01-21)

Hi, can we update on this issue.

### fa...@gmail.com (2025-04-03)

Hi, it seems this issue is fixed in the latest version of Chrome. It was resolved somewhere between Version `134.0.6998.178` and Version `135.0.7049.42`. Until Version `134`, it worked, but after updating to `135`, it no longer works. I noticed that instead of the download view opening in the popup behind PiP, it is now hidden and only becomes visible on top after clicking the download icon.

### aj...@chromium.org (2025-04-15)

Hi fazim - could you upload a video of it no longer reproducing? Perhaps you could bisect to find the fix CL?

### fa...@gmail.com (2025-04-16)

The issue was fixed whe testing on 135.0.7049.42, but it seems the problem is still present when testing on version 135.0.7049.96 after just updating the stable version. Odd.

### fa...@gmail.com (2025-12-11)

Testing on the latest version now, it seems the issue is fixed. Can we close this as resolved? Thank you.

### ch...@chromium.org (2025-12-11)

It's possible this appears fixed due to [crrev.com/c/7041986](https://crrev.com/c/7041986), which I considered only a partial mitigation because it depends on the timing of the Enter keypress.

### ch...@chromium.org (2025-12-11)

I'm working on a fix for a related issue which should address this too. If not, then I'll add a PiP occlusion tracker to the download bubble directly.

### dx...@google.com (2025-12-15)

Project: chromium/src  

Branch:  main  

Author:  Lily Chen [chlily@chromium.org](mailto:chlily@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7254096>

[Download Bubble] Use BubbleCloser to close bubble from inactive

---


Expand for full commit details
```
     
    The download bubble normally relies on close-on-deactivate behavior from 
    BubbleDialogDelegate to allow the user to close it by pressing Esc, 
    clicking elsewhere, etc. However, it is sometimes created with 
    ShowInactive(), to avoid stealing focus which may be disruptive to the 
    user. In an already inactive state, close-on-deactivate cannot occur, so 
    there would have been no way to close the bubble. 
     
    We had two separate workarounds for this issue. First, the bubble 
    subscribes to BrowserList activation events and activates itself when 
    the browser it is attached to becomes active, relying on 
    close-on-deactivate to work as usual once the bubble is active. Later, 
    we added a BubbleCloser utility which uses EventMonitor to directly 
    close the bubble in response to input events. 
     
    This CL removes the former (self-activation) workaround in favor of just 
    using BubbleCloser. The self-activation workaround was causing issues 
    with unexpected input to the download bubble, when it was active but 
    occluded by other elements. 
     
    Bug: 440892551, 363930141, 421877606, 421348748, 398173038, 464313652 
    Change-Id: I2f195b1568391960cd67c84c536c5c6885faa665 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7254096 
    Commit-Queue: Lily Chen <chlily@chromium.org> 
    Reviewed-by: Daniel Rubery <drubery@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1559032}

```

---

Files:

- M `chrome/browser/ui/views/download/bubble/download_bubble_interactive_uitest.cc`
- M `chrome/browser/ui/views/download/bubble/download_toolbar_ui_controller.cc`
- M `chrome/browser/ui/views/download/bubble/download_toolbar_ui_controller.h`

---

Hash: [63716080a676f0520d732c631e0e80eff59bf6c4](https://chromiumdash.appspot.com/commit/63716080a676f0520d732c631e0e80eff59bf6c4)  

Date: Mon Dec 15 23:22:24 2025


---

### dx...@google.com (2025-12-22)

Project: chromium/src  

Branch:  main  

Author:  Lily Chen [chlily@chromium.org](mailto:chlily@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7275653>

[Download Bubble] Add PiP occlusion tracker

---


Expand for full commit details
```
     
    Track all PictureInPicture windows in order to prevent the main button 
    and quick action button controls from activating when the download 
    bubble is occluded by a PiP, to prevent clickjacking. 
     
    Change-Id: Ie29fe62a391ae71b56a731a9402d4824d1456664 
    Bug: 440892551, 363930141, 421348748 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7275653 
    Reviewed-by: Xinghui Lu <xinghuilu@chromium.org> 
    Commit-Queue: Lily Chen <chlily@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1561982}

```

---

Files:

- M `chrome/browser/ui/views/download/BUILD.gn`
- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view.cc`
- M `chrome/browser/ui/views/download/bubble/download_bubble_row_view.h`

---

Hash: [704eae4e9117736ef10b3d69ca1fd771aecf46df](https://chromiumdash.appspot.com/commit/704eae4e9117736ef10b3d69ca1fd771aecf46df)  

Date: Mon Dec 22 22:22:57 2025


---

### ch...@google.com (2025-12-23)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2026-01-09)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
low impact UI spoofing with user gestures


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### dr...@chromium.org (2026-01-09)

[security triage] Looks like our automation dropped the ball here, but since this is Medium severity we should consider this for a merge to M144. Manually doing the merge request now, and I'll review the fix shortly.

### dr...@chromium.org (2026-01-12)

On a further look, there's nothing to merge here. On the day this was fixed, our automation should have tagged this for a merge to M144 Beta. But today M144 has been cut for Stable and M145 is about to be in Beta. We don't merge Medium severity bugs into Stable, so we'll have to be content with this being fixed in M145.

### ch...@google.com (2026-04-01)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/363930141)*
