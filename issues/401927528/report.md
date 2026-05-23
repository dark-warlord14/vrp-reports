# DevTools Recorder Can Flip Internal Flags Without User Awareness

| Field | Value |
|-------|-------|
| **Issue ID** | [401927528](https://issues.chromium.org/issues/401927528) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>DevTools>Recorder |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | bi...@gmail.com |
| **Assignee** | al...@google.com |
| **Created** | 2025-03-10 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

# VULNERABILITY DETAILS

Chrome DevTools Recorder currently allows regular users to automate steps on `chrome://` URLs. This opens the door for social engineering attacks, where users can be tricked into executing pre-recorded scripts that flips flags without clear user consent.

This issue also bleeds to ChromeOS where extensions requires explicit permission to allow injecting script in `chrome://file-manager/*` URLs, which is currently disabled by default. By flipping a certain flag (`#extensions-on-chrome-urls`), the attacker could start another system attack.

# VERSION

Tested in:
Chrome Version: 134.0.6998.36 (Official Build) (64-bit)
Operating System: Windows NT: 10.0.19044

# REPRODUCTION CASE

I've attached an HTML page that looks like a valid tutorial on enabling 60FPS for web mobile games. It guides users to download and run a DevTools Recorder script that flips `#extensions-on-chrome-urls` flag without their full awareness. Follow the guide in the HTML file:

1. Download attached HTML file.
2. Download the recorder script provided in the tutorial page.
3. Import the and replay the recorder file in DevTools Recorder.

Since the `chrome://flags` can automatically jump to certain flags, this makes the victim unaware that the target flag has been flipped. Furthermore, the warning at the very top of the page is not visible upon Relaunch as seen in the video

In this particular example, the flag is used to allows chrome extensions to run in chrome:// URLs.

## SUGGESTED SOLUTION

To perform recorder steps in `chrome://*` URLs, the user should explicitly enable a flag in `chrome://flags`.

# CREDIT INFORMATION

Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: vanillawebdev

## Attachments

- [devtools-recorder-misuse-demo.html](attachments/devtools-recorder-misuse-demo.html) (text/html, 4.6 KB)
- [devtools recorder misuse demo.webm](attachments/devtools recorder misuse demo.webm) (video/webm, 11.5 MB)
- [download.json](attachments/download.json) (application/json, 1.3 KB)
- [devtools_recorder_toggle-extensions-on-chrome-urls_flag.json](attachments/devtools_recorder_toggle-extensions-on-chrome-urls_flag.json) (application/json, 3.0 KB)

## Timeline

### ph...@chromium.org (2025-03-10)

I can reproduce this on Linux M134.

kimanh@: Could you help take a look at this bug, or find a right owner for it please?

### ph...@google.com (2025-03-10)

The recording.

### al...@google.com (2025-03-10)

Note that social engineering is [not considered](https://docs.google.com/document/d/1Oca97_xlg7OA0cnhMdEUHJtEW95_cghd7YIF5NN2_B4/edit?resourcekey=0-NyitQ-xJX3W9uw35mn8GSw&tab=t.0#bookmark=id.ky6qse511ztp) to be a vulnerability according to the Chrome DevTools Security Framework.

### bi...@gmail.com (2025-03-10)

Very well, I understand. However, I hope you can consider the part where steps are allowed to run in chrome://\* as a vulnerability.

Update:
In the previous attachment, I removed some steps. Turns out it fails to flip a flag in ChromeOS. Here’s a new POC that works in ChromeOS. This one only toggles the `#extensions-on-chrome-urls` flag. The recording was made on Windows.

### dx...@google.com (2025-03-14)

Project: devtools/devtools-frontend  

Branch: main  

Author: Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6343138>

[Recorder] Confirm recording import the first time

---


Expand for full commit details
```
     
    Uses the same pattern that is used to confirm pasting. 
     
    Fixed: 402071098 
    Bug: 401927528 
    Change-Id: I1317fa81bff3cb5a17e4923596e10af05350fb82 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6343138 
    Commit-Queue: Alex Rudenko <alexrudenko@chromium.org> 
    Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>

```

---

Files:

- M `front_end/panels/recorder/BUILD.gn`
- M `front_end/panels/recorder/RecorderController.ts`
- M `front_end/ui/visual_logging/KnownContextValues.ts`

---

Hash: a702323c7c0f226bd02c3971de19f9bbc98a4de1  

Date:  Fri Mar 14 08:15:20 2025


---

### dx...@google.com (2025-03-14)

Project: chromium/src  

Branch: main  

Author: chromium-autoroll [chromium-autoroll@skia-public.iam.gserviceaccount.com](mailto:chromium-autoroll@skia-public.iam.gserviceaccount.com)  

Link:      <https://chromium-review.googlesource.com/6354816>

Roll DevTools Frontend from d7d0c1592864 to a702323c7c0f (2 revisions)

---


Expand for full commit details
```
     
    https://chromium.googlesource.com/devtools/devtools-frontend.git/+log/d7d0c1592864..a702323c7c0f 
     
    2025-03-14 alexrudenko@chromium.org [Recorder] Confirm recording import the first time 
    2025-03-14 pfaffe@chromium.org Avoid regex in font matcher 
     
    If this roll has caused a breakage, revert this CL and stop the roller 
    using the controls here: 
    https://autoroll.skia.org/r/devtools-frontend-chromium 
    Please CC devtools-waterfall-sheriff-onduty@rotations.google.com,liviurau@google.com on the revert to ensure that a human 
    is aware of the problem. 
     
    To report a problem with the AutoRoller itself, please file a bug: 
    https://issues.skia.org/issues/new?component=1389291&template=1850622 
     
    Documentation for the AutoRoller is here: 
    https://skia.googlesource.com/buildbot/+doc/main/autoroll/README.md 
     
    Bug: chromium:401927528 
    Change-Id: Ib661ca63522bd3aa00d3636971852045bb280ec4 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6354816 
    Bot-Commit: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Commit-Queue: chromium-autoroll <chromium-autoroll@skia-public.iam.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1432623}

```

---

Files:

- M `DEPS`
- M `third_party/devtools-frontend/src`

---

Hash: 24da6f9040bd9f0bc7d9fb0bead52d4cd8921648  

Date:  Fri Mar 14 11:13:45 2025


---

### dx...@google.com (2025-03-17)

Project: devtools/devtools-frontend  

Branch: main  

Author: Alex Rudenko [alexrudenko@chromium.org](mailto:alexrudenko@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6355192>

[Recorder] restrict navigation

---


Expand for full commit details
```
     
    Fixed: 401927528 
    Change-Id: Ica9e5f2e1b28aa7ee6c0b2ee7cd43390c2eebd5b 
    Reviewed-on: https://chromium-review.googlesource.com/c/devtools/devtools-frontend/+/6355192 
    Auto-Submit: Alex Rudenko <alexrudenko@chromium.org> 
    Commit-Queue: Wolfgang Beyer <wolfi@chromium.org> 
    Reviewed-by: Wolfgang Beyer <wolfi@chromium.org>

```

---

Files:

- M `front_end/panels/recorder/RecorderController.ts`
- M `front_end/panels/recorder/models/RecordingPlayer.ts`
- M `test/e2e/recorder/replay_test.ts`

---

Hash: 03eabb6cc14fc382a2a47047e01d49963a95fc10  

Date:  Fri Mar 14 15:06:08 2025


---

### ch...@google.com (2025-03-26)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### am...@chromium.org (2025-03-26)

While social engineering is not considered a security issue within Chrome's threat model, extensions shouldn't be allowed to call on chrome:// URLs, so we would consider this to be a security issue, albeit a low severity one considering the preconditions to exploit requiring direct engagement with devtools and extension with a lower impact and potential exploitability.

### sp...@google.com (2025-03-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact exploitation mitigation bypass 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-03-26)

Congratulations vanillawebdev! Thank you for your efforts and reporting this issue to us.

### ch...@google.com (2025-07-03)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact exploitation mitigation bypass

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/401927528)*
