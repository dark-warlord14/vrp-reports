# File picker dialog can be shown over on different tab when focused on it (on split view)

| Field | Value |
|-------|-------|
| **Issue ID** | [444653104](https://issues.chromium.org/issues/444653104) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>TopChrome>TabStrip>SplitView |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ag...@google.com |
| **Created** | 2025-09-12 |
| **Bounty** | $500.00 |

## Description


VULNERABILITY DETAILS

the vulnerability is similar as https://issues.chromium.org/issues/40063021 but this bug occurs when the tab focus changes to the neighboring tab (happens in split view)


VERSION
Version 142.0.7409.0 (Official Build) canary (64-bit)
Operating System: Windows 11

REPRODUCTION CASE
1. Open uyx.html
2. right click on link 
3  select open in split view

## Attachments

- [bandicam 2025-09-13 02-29-30-559.mp4](attachments/bandicam 2025-09-13 02-29-30-559.mp4) (video/mp4, 2.2 MB)
- [uyx.html](attachments/uyx.html) (text/html, 1.3 KB)

## Timeline

### mp...@google.com (2025-09-12)

It does seem like the file picker dialog is a challenge in split screen mode. Perhaps it should be clearer which site is showing the file picker dialog, or we should show a separate confirmation dialog ("Are you sure you want to upload a.jpg to evil.com"). Or file picker dialogs just shouldn't be shown until the other split screen tab regains focus.

### ch...@google.com (2025-09-13)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mp...@google.com (2025-09-16)

Assigning agale@ based on [crbug.com/440523110](https://crbug.com/440523110). I think this is just a different path to open the file picker.

### en...@chromium.org (2025-10-27)

Chiming in here quite late, but it does feels to me that <https://chromium-review.googlesource.com/6941305> would address this issue as well. Alison, does that match your understanding as well?

### fe...@chromium.org (2025-10-27)

I wasn't aware of <https://crrev.com/c/6941305> . I have been working on similar problems with the file chooser but unrelated to split view.

Showing the file chooser is inherently racy because it has a bunch of async steps and just checking at the start does not guarantee that the state is still compatible by the time the chooser is actually shown. <https://crrev.com/c/6966639> closed off these races for the visibility, however there is more to do, related to RenderFrameHost lifecycle. <https://crrev.com/c/6986448> introduces a generic helper that handles both visibility and lifecycle. Once I land that, it could be extended to also account for split-view.

### en...@chromium.org (2025-10-28)

Thanks, Fergal! I was indeed wondering if we need to worry about race condition. Fantastic to hear that you already have an elegant solution in review. I'll let you and Alison work out how to extend your generic solution to cover split view as well.

### ag...@google.com (2025-10-28)

To answer the question from #5, my CL fixed one path to open the file picker but there are other paths. I have a CL I'm about to send out which will cover the other ways I'm aware of to open the file picker: https://chromium-review.googlesource.com/c/chromium/src/+/7087491

Fergal, that is great you are working on a more robust way to control races for the file chooser. Can you cc me on the two bugs you are addressing? I also have crbug.com/454484864 which might also be related. That is less about race conditions and more about handling visibility/activeness changes that happen after the file picker is opened.

### dx...@google.com (2025-11-13)

Project: chromium/src  

Branch:  main  

Author:  Alison Gale [agale@chromium.org](mailto:agale@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7087491>

[SxS] Block opening file picker from inactive tab

---


Expand for full commit details
```
     
    This only handles the first bug which is when the tab is inactive when 
    the file request happens. Will need to follow up to observe tab 
    activation changes to update when a tab becomes inactive. 
     
    Bug: 444653104 
    Change-Id: Ica1845ddaab9820d2bf1ecc419578042f2fce6f0 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7087491 
    Commit-Queue: Alison Gale <agale@chromium.org> 
    Reviewed-by: Bo Liu <boliu@chromium.org> 
    Reviewed-by: Charlie Reis <creis@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1544520}

```

---

Files:

- M `chrome/browser/ui/views/file_system_access/file_system_access_browsertest.cc`
- M `content/browser/file_system_access/file_system_chooser_browsertest.cc`
- M `content/browser/web_contents_based_canceller.cc`
- M `content/browser/web_contents_based_canceller.h`
- M `content/common/features.cc`
- M `content/common/features.h`

---

Hash: [c72906f92191aa760ae462ad5d879ab95ebbc472](https://chromiumdash.appspot.com/commit/c72906f92191aa760ae462ad5d879ab95ebbc472)  

Date: Thu Nov 13 21:19:00 2025


---

### fe...@google.com (2025-11-18)

Reopening this as I don't see another bug for the racey version. If there is another bug, feel free to close this one.

### sa...@gmail.com (2025-11-18)

Are there any other bugs besides this one? I don't think there are any more bugs similar to this one.

### ag...@google.com (2025-11-24)

The racey version is tracked in [crbug.com/454484864](https://crbug.com/454484864).

### sp...@google.com (2025-12-18)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $500.00 for this report.

Rationale for this decision:
mitigated low impact ui spoofing requiring multiple complex gestures


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

> mitigated low impact ui spoofing requiring multiple complex gestures

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/444653104)*
