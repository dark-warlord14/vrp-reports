# devicechange event leaks for macbook's internal camera in sandboxed documents.

| Field | Value |
|-------|-------|
| **Issue ID** | [387583503](https://issues.chromium.org/issues/387583503) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>MediaStream |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 133.0.6936.0 |
| **Reporter** | tr...@gmail.com |
| **Assignee** | gu...@chromium.org |
| **Created** | 2025-01-04 |
| **Bounty** | $1,000.00 |

## Description

# Steps to reproduce the problem

<https://jsfiddle.net/wyfvm0jd/>

1. Connect a macbook with an internal camera (maybe affects other manufacturers, not sure) to a second display.
2. In a sandboxed document with only "allow-scripts", listen for the `navigator.mediaDevices.ondevicechange` event.
3. Close the lid of the macbook.

# Problem Description

The event is not supposed to fire in this case. The document is not allowed to access the camera details. This can be checked by requesting a new MediaStream from the camera, it's correctly blocked.
Note that if an external camera is connected (I tested with an USB one), then the event doesn't fire, even for the internal one.

# Summary

devicechange event leaks for macbook's internal camera in sandboxed documents.

# Custom Questions

#### Reporter credit:

Kaiido

# Additional Data

Category: Security   

Chrome Channel: Canary   

Regression: N/A

## Attachments

- [variations.txt](attachments/variations.txt) (text/plain, 46.3 KB)

## Timeline

### tr...@gmail.com (2025-01-04)

Ps: this is not a regression, just tried on M99 and was still able to reproduce.

### xi...@chromium.org (2025-01-05)

Thanks for the report. I'm able to reproduce on Chrome Stable on MacOS. guidou@, could you help triage this issue? Setting severity to S2 since it leaks user information within a sandbox.

PoC in text:

<p>
Close the lid of you macbook while connected to an external monitor.<br>
See a new event is fired.<br>
Try to click the buttons, see how they're correctly blocked.
</p>
<iframe sandbox="allow-scripts" srcdoc="
<button>request camera</button>
<button>request microphone</button><br>
<script>
navigator.mediaDevices.ondevicechange = e => document.body.append('fired - ')
const [cam, mic] = document.querySelectorAll('button');
cam.onclick = e => navigator.mediaDevices.getUserMedia({ video: true });
mic.onclick = e => navigator.mediaDevices.getUserMedia({ audio: true });
</script>
"></iframe>

### pe...@google.com (2025-01-05)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ap...@google.com (2025-01-08)

Project: chromium/src  

Branch: main  

Author: Guido Urdaneta <[guidou@chromium.org](mailto:guidou@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6152197>

[MediaDevices] Check permission before firing devicechange event

---


Expand for full commit details
```
[MediaDevices] Check permission before firing devicechange event 
 
Bug: 387583503 
Change-Id: Iffb85a335719c263555bb4a2630da90cb756189d 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6152197 
Reviewed-by: Palak Agarwal <agpalak@chromium.org> 
Commit-Queue: Guido Urdaneta <guidou@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1403590}

```

---

Files:

- M `third_party/blink/renderer/modules/mediastream/BUILD.gn`
- M `third_party/blink/renderer/modules/mediastream/media_devices.cc`
- M `third_party/blink/renderer/modules/mediastream/media_devices.h`
- M `third_party/blink/renderer/modules/mediastream/media_devices_test.cc`
- A `third_party/blink/renderer/modules/mediastream/media_permission_testing_platform.cc`
- A `third_party/blink/renderer/modules/mediastream/media_permission_testing_platform.h`

---

Hash: 5182f8756d86cb441d3445fcb628f961e74bd6ca  

Date:  Wed Jan 08 08:27:06 2025


---

### sp...@google.com (2025-01-23)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-01-23)

Thank you for your efforts and reporting this issue to us!

### ch...@google.com (2025-04-18)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/387583503)*
