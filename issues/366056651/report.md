# Unintended File Upload via `webkitdirectory` triggered by Keyboard interactions on macOS Chrome

| Field | Value |
|-------|-------|
| **Issue ID** | [366056651](https://issues.chromium.org/issues/366056651) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File>Directory |
| **Platforms** | Mac |
| **Reporter** | fa...@gmail.com |
| **Assignee** | el...@chromium.org |
| **Created** | 2024-09-12 |
| **Bounty** | $1,000.00 |

## Description

#### SUMMARY

The file picker, when using webkitdirectory, can unknowingly upload user files without their awareness during website interaction, as the default prompt in the macOS version of Chrome is set to "Allow.

As a result, user files are uploaded to the attacker's website due to an alert appearing on top of the prompt during the interaction.

This issue is similar to the one discussed in [342194497](https://issues.chromium.org/issues/342194497) and other cases where a prompt is triggered by keyboard interactions and can be abused by websites using game-like scenarios, leading to the user unknowingly approving sensitive actions.

#### VULNERABILITY DETAILS

The proof of concept below only works on macOS Chrome, and not on the Windows version.

Testing shows that Windows, by default, does not trigger an "Allow" prompt but instead cancels it.

However, macOS triggers "Allow" and proceeds to upload the file after the interaction.

A potential fix could involve setting the default response on macOS prompts to `Cancel` instead of `Allow`.

The interaction leading to the upload of files from the user’s system is as follows:

1. First, the website asks the user to hold down the Enter key. When using the `webkitdirectory` code on input, by default, user files are pre-selected. The confirmation is done by simply pressing Enter.

However, this confirmation is typically blocked by a security prompt.

2. Second, the security prompt is spoofed by another alert box that appears in front of it. This alert asks the user to press Enter twice.

Since macOS defaults to "Allow" for confirmation, the second press of Enter immediately uploads the user's directory.

---

#### VERSION

- Chrome Version:
  
  - 130.0.6713.0 (Official Build) Canary (64-bit)
  - 128.0.6613.138 (Official Build) (64-bit) Stable
- Operating System:
  
  - macOS Sonoma 14.6.1

---

#### REPRODUCTION CASE

1. Download the `poc.html` file.
2. Open the `poc.html` file in the latest macOS Chrome browser.
3. Hold down the Enter key, then press Enter twice.
4. Observe that user files are uploaded to the malicious website.

---

**Observed:**  

User files can be uploaded without the user’s awareness because, on macOS, the Chrome "Allow" prompt is selected by default.

**Expected:**  

Chrome should ensure that "Cancel" is selected by default on macOS, just as it is on the Windows version of the browser.

---

#### CREDIT INFORMATION

Reporter credit: Shaheen Fazim

## Attachments

- [poc.html](attachments/poc.html) (text/html, 1.9 KB)
- [screenrecord.mp4](attachments/screenrecord.mp4) (video/mp4, 1.7 MB)
- [mac-prompt.png](attachments/mac-prompt.png) (image/png, 23.5 KB)
- [win-prompt.png](attachments/win-prompt.png) (image/png, 33.8 KB)
- [Screen Recording 1404-09-20 at 21.16.42.mov](attachments/Screen Recording 1404-09-20 at 21.16.42.mov) (video/quicktime, 2.9 MB)

## Timeline

### fa...@gmail.com (2024-09-12)

Hi, a clarification: instead of "Allow," the correct term in the prompt is "Upload". This was mistakenly repeated above.

Additionally, when comparing the prompts on Windows and macOS, the default selection on macOS is "Upload" (see mac-prompt.png), whereas on Windows, it is set to "Cancel" (see win-prompt.png).

### an...@chromium.org (2024-09-12)

Thanks for the report!

This issue seems to be the same as discussed in: <https://issues.chromium.org/40085079>.
Specifically, these comments are about the MacOS default button (Upload vs Cancel).

<https://issues.chromium.org/u/3/issues/40085079#comment158>
<https://issues.chromium.org/u/3/issues/40085079#comment159>

Assigning to ellyjones@ (one of the OWNERS of the file upload confirmation dialog and CCd in the comments above). Please re-route as appropriate. Thanks!
Also CCing pbos@ who worked on the previous issue.

Setting Severity to S2 based on the previous issue, FoundIn to M128 (current extended stable), and OS to Mac.

### el...@chromium.org (2024-09-12)

That behavior is more or less by design. On macOS, Enter always selects the default option in a dialog. I suppose we could change the default on this dialog to Cancel? That seems like kind of a weird default to have for a file upload but maybe there is precedent from permission dialogs.

### an...@chromium.org (2024-09-12)

Cancel is the default we use for Windows so maybe we can do the same for MacOS? Not sure why we didn't do that as part of the previous issue's fix - maybe there were other factors involved.

### pb...@chromium.org (2024-09-12)

I would also argue that we should have better clickjacking protection than default focus, since default focus forces us to make our user journeys worse.

There's some stubs for this with DialogDelegate::TriggerInputProtection, but I assume that that's not applied universally. I also don't know if we've vetted it as "sufficient" for all clickjacking-type schemes.

### pe...@google.com (2024-09-13)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-13)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### pe...@google.com (2024-09-27)

ellyjones: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### el...@chromium.org (2024-10-01)

I'm triaging this as Pri-2 given the need for user interaction.

### pe...@google.com (2024-10-16)

ellyjones: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2024-11-26)

Hi ellyjones@, Could you share any updates on this issue.

### el...@chromium.org (2024-11-27)

I have no updates on this one.

### fa...@gmail.com (2025-12-11)

Hi, I reported a similar issue to Apple a while ago affecting Safari, and they have fixed the Enter key issue with WebKitDirectory. Long pressing Enter no longer triggers the problem. Therefore, this security issue is fixed on chrome too. Can we close this issue as resolved? Thank you.

### fa...@gmail.com (2025-12-11)

long-pressing Enter no longer automatically triggers WebKitDirectory to select files for upload.

### aj...@chromium.org (2025-12-22)

owner: if you can identify a fixing change please add it, it looks like all the associated attempts were abandoned.

### fa...@gmail.com (2025-12-23)

They were attempted by me, but the last change was almost a fix. During testing it seemed that the fix was no longer needed, the pressing enter key to auto-accept fileupload issue in the WebKit directory was fixed by Apple later. Thank you.

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

### ch...@google.com (2026-03-31)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> low impact UI spoofing with user gestures

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/366056651)*
