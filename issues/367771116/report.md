# Extension popup can render over downloaded file prompts

| Field | Value |
|-------|-------|
| **Issue ID** | [367771116](https://issues.chromium.org/issues/367771116) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2024-09-18 |
| **Bounty** | $1,000.00 |

## Description

VULNERABILITY DETAILS
This vulnerability is almost the same as
 https://issues.chromium.org/issues/40058873, https://issues.chromium.org/issues/361711121 
 but it occurs on downloaded file  prompt


VERSION
Chrome Version 130.0.6723.4 (Official Build) canary (64-bit)
Operating System: Windows 10

REPRODUCTION CASE

1. Install attached extension: manifest-keyboard.json + bg-keyboard.js + popup.html. Rename the manifest file to manifest.json

2. Reload manifest-keyboard.json extension using chrome://extensions
Press Ctrl+A when requested by the attacker page.

3. Click the Web page then Press Ctrl+A when requested by the attacker page.

CREDIT INFORMATION
Externally reported security bugs may appear in Chrome release notes. If this bug is included, how would you like to be credited?
Reporter credit: [goes here]

## Attachments

- [extensionpopup-.zip](attachments/extensionpopup-.zip) (application/zip, 7.5 KB)
- [bandicam 2024-09-18 14-33-42-940.mp4](attachments/bandicam 2024-09-18 14-33-42-940.mp4) (video/mp4, 2.3 MB)
- [downloadspoof.png](attachments/downloadspoof.png) (image/png, 105.8 KB)
- [manifest.json](attachments/manifest.json) (application/json, 467 B)
- [popup.html](attachments/popup.html) (text/html, 2.3 KB)
- [popup-screenshare.html](attachments/popup-screenshare.html) (text/html, 430 B)
- [bg-keyboard.js](attachments/bg-keyboard.js) (text/javascript, 2.2 KB)
- [bandicam 2025-03-25 12-32-53-235.mp4](attachments/bandicam 2025-03-25 12-32-53-235.mp4) (video/mp4, 1.5 MB)
- [bandicam 2025-03-29 07-59-21-393.mp4](attachments/bandicam 2025-03-29 07-59-21-393.mp4) (video/mp4, 2.2 MB)
- [bandicam 2025-03-29 08-25-04-755.mp4](attachments/bandicam 2025-03-29 08-25-04-755.mp4) (video/mp4, 1.8 MB)
- [bandicam 2025-03-29 08-45-30-613.mp4](attachments/bandicam 2025-03-29 08-45-30-613.mp4) (video/mp4, 1.5 MB)

## Timeline

### ma...@google.com (2024-09-18)

Hello, can you please attach the poc as individual uncompressed/unarchived files? Otherwise we can't process your report. Thank you.

### ma...@google.com (2024-09-18)

Setting some provisional labels. (I didn't attempt a repro of this yet, and can't look at the PoC yet, but the video looks plausible.)

I agree this looks similar to the other issues and we would not want the extension popup to show on top here.

Assigning to kerenzhu@, based on the referenced issues. Could you PTAL? Thank you!

### sa...@gmail.com (2024-09-18)

redacted

### pe...@google.com (2024-09-19)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sa...@gmail.com (2025-01-06)

hello any updates?

### sa...@gmail.com (2025-02-05)

hello any updates?

### sa...@gmail.com (2025-03-25)

hello  any updates?

### sa...@gmail.com (2025-03-25)

redacted

### ke...@chromium.org (2025-03-25)

Some other changes might have fixed the bug as a side-effect. Last time I looked at it, there were some tests I had difficulty fixing.

### sa...@gmail.com (2025-03-25)

hello, shouldn't the status be fixed (not wont fixed) because there are Some other changes might have fixed the bug as a side-effect. because this is related to Chrome VRP. same as bug https://issues.chromium.org/issues/40064688 where it is not fixed but there is a change effect from the others so that it affects bug https://issues.chromium.org/issues/40064688 so that the bug status is changed to fixed because it is related to chrome vrp related to rewards etc.

### ke...@chromium.org (2025-03-25)

Marking as Fixed, I'll let Chrome VRP folks make the call.

### am...@chromium.org (2025-03-28)

This looks like this was resolved by <https://crrev.com/c/5995850>, same as issues [crbug.com/359949844](https://crbug.com/359949844) and [crbug.com/376497151](https://crbug.com/376497151). Sharing the same root cause, this does not appear eligible for it's own reward, but we'll discuss at a future panel session.

### sa...@gmail.com (2025-03-28)

after fixed issues crbug.com/359949844 and crbug.com/376497151, this bug still reproduced not resolved this bug. I don't know which CL is affected by this bug.

### sa...@gmail.com (2025-03-28)

in this cl https://crrev.com/c/5995850 the affected fix is ​​limited to pwa prompt (pwa_confirmation_bubble_view.cc) and fedcm (account_selection_view.cc) not download bubble

### sa...@gmail.com (2025-03-29)

redacted

### sa...@gmail.com (2025-03-29)

In Version 135.0.6999.0 (Developer Build) (64-bit) still reproduced

### sa...@gmail.com (2025-03-29)

This bug fix is ​​in In Version 136.0.7075.0 (Developer Build) (64-bit) in this version I can no longer reproduce it (https://commondatastorage.googleapis.com/chromium-browser-snapshots/index.html?prefix=Win_x64/1433940/) (2025-03-18)

### sp...@google.com (2025-04-03)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI spoof


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-03)

Congratulations -- thank you for your efforts and reporting this issue to us.

### ch...@google.com (2025-07-02)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI spoof

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/367771116)*
