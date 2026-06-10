# Audio player's download functionality allows bypassing the "allow-downloads" flag of sandboxed iframes

| Field | Value |
|-------|-------|
| **Issue ID** | [40064543](https://issues.chromium.org/issues/40064543) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Media>Audio, Blink>SecurityFeature>IFrameSandbox, UI>Browser>Downloads |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | st...@chromium.org |
| **Created** | 2023-05-13 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

A sandboxed iframe is not supposed to be able to initiate a download unless the "allow-downloads" flag is set. However, it is possible to make the user click on the "Download" option of the audio player through a clickjacking attack, which ends up downloading a file.

An arbitrary file can be made to be downloaded by performing a server-side redirect when the user tries to download the original audio file.

The "Download" option should be checking whether the iframe is sandboxed and contains the proper flags before deciding whether the download should initiate.

For the attack to work, it requires the victim to click twice inside a malicious iframe. In a real attack, there would be buttons placed over the video player to trick the user into clicking on the "three dots" and the "Download" option. The PoC just places opacity over the iframe to demonstrate that it would be possible to do that.

For reference, this issue is similar to <https://crbug.com/chromium/1100761>, albeit more severe as this issue doesn't require any additional sandbox permission to work.

I have attached a video (repro.mkv) reproducing the attack.

**VERSION**  

Chrome Version:  

113.0.5672.92 (Official Build) stable (64-bit)  

114.0.5735.26 (Official Build) beta (64-bit)  

115.0.5762.4 (Official Build) dev (64-bit)

Operating System:  

Ubuntu 20.04

**REPRODUCTION CASE**

1. Download "index.html", "iframe.html", "iframe2.html", "horse.ogg", "file.txt", "download.php" and place them in the same directory.
2. Run the "php -S 0:8000" command in the directory the files were downloaded to.
3. Access <http://localhost:8000/>
4. Click on the "three dots" and then on the "Download" option, which will download a file even though the iframe doesn't have the "allow-downloads" flag set.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

## Attachments

- [iframe.html](attachments/iframe.html) (text/plain, 320 B)
- [index.html](attachments/index.html) (text/plain, 370 B)
- [iframe2.html](attachments/iframe2.html) (text/plain, 185 B)
- [file.txt](attachments/file.txt) (text/plain, 4 B)
- [download.php](attachments/download.php) (text/plain, 1.1 KB)
- [horse.ogg](attachments/horse.ogg) (application/octet-stream, 13.6 KB)
- [repro.mkv](attachments/repro.mkv) (application/octet-stream, 1.4 MB)
- [iframe.html](attachments/iframe.html) (text/html, 717 B)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 7.6 MB)

## Timeline

### [Deleted User] (2023-05-13)

[Empty comment from Monorail migration]

### ke...@chromium.org (2023-05-16)

Thanks for the report. I can verify this happens.

clamy@: Can you help triage? This looks like another case where download should be blocked.

[Monorail components: Blink>SecurityFeature>IFrameSandbox]

### [Deleted User] (2023-05-16)

[Empty comment from Monorail migration]

### ad...@google.com (2023-05-17)

(I am a bot: this is an auto-cc on a security bug)

### am...@chromium.org (2023-10-08)

assigning to arthursonzogni@ based on your previous work on bypasses of allow-downloads, such as https://crbug.com/chromium/1357366

[Monorail components: UI>Browser>Downloads]

### ar...@chromium.org (2023-10-11)

> assigning to arthursonzogni@ based on your previous work on bypasses of allow-downloads, such as https://crbug.com/chromium/1357366

I am no more working on the Web Platform Security team, and I won't have time for this quick unrelated adventure.
Maybe the Web Platform Security would be interested. + @clamy@chromium.org for priority/assignment.

### is...@google.com (2023-10-11)

This issue was migrated from crbug.com/chromium/1445271?no_tracker_redirect=1

[Multiple monorail components: Blink>SecurityFeature>IFrameSandbox, UI>Browser>Downloads]
[Monorail components added to Component Tags custom field.]

### he...@gmail.com (2026-01-16)

Hey, I was looking through some of my older bugs that are still open and noticed that after the migration, the severity for this one was changed from S2 to S3.

I think this was probably accidental and should be reverted. Iframe sandbox bypasses have been treated as medium severity over the year (see [bug 40057349](https://issues.chromium.org/issues/40057349) and [bug 40052658](https://issues.chromium.org/issues/40052658) for similar cases).

Thanks!

### ch...@google.com (2026-01-21)

clamy: Uh oh! This issue still open and hasn't been updated in the last 832 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2026-01-21)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### ch...@google.com (2026-02-05)

clamy: Uh oh! This issue still open and hasn't been updated in the last 847 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### es...@chromium.org (2026-02-06)

steimel@ or dalecurtis@, I poked around a bit but can't find the code where the "Download" option on the 3 dot menu of an <audio> element is implemented -- do you know where this happens, i.e. where would be a good place to check iframe sandbox attributes before initiating a download?

I'm downgrading this to S3 because I can't find a way to actually overlay something on top of the <audio> element such that the element can still be interacted with, and without being able to do that, I think this would be difficult to actually exploit. Might be worth reconsidering S2 if it turns out that it is possible to overlay something on top of the element such that the clicks fall through to the 3 dot and the menu item.

### he...@gmail.com (2026-02-06)

#13, I don't think there is any specific clickjacking protection for `<audio>` elements. It is possible to add an overlay with `pointer-events: none;` over it while still being able to interact with the controls.

I have attached `iframe.html` to demonstrate that. You can swap it with the original `iframe.html` to reproduce it.

I also added a video reproducing the updated PoC (`repro.mp4`).

### es...@chromium.org (2026-02-06)

Thanks! I think I will still leave this as S3. It looks like we've triaged sandboxed iframe download bypasses in the past inconsistently, sometimes S2 and S3, but we're thinking about downgrading clickjacking bugs' severity in general, and this one requires 2 rather than 1 click.

### da...@chromium.org (2026-02-09)

Looks like it's implemented here:

- <https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/modules/media_controls/elements/media_control_download_button_element.cc;l=76;drc=f9c50cd568a79e2350cdc285435d8cd991bdcac1>

### st...@chromium.org (2026-02-18)

Just tried this locally on Chrome 145 on Linux and the download button doesn't seem to show up for me. Is this still reproducible?

### st...@chromium.org (2026-02-18)

I was able to modify the test page to get it to repro. I'll change the media controls to not show the download button in a sandboxed page that doesn't allow downloads

### dx...@google.com (2026-02-19)

Project: chromium/src  

Branch:  main  

Author:  Tommy Steimel [steimel@chromium.org](mailto:steimel@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7590057>

[Media Controls] Hide download button when sandbox flags disallow it

---


Expand for full commit details
```
     
    Currently, the default Blink media controls display a (functional) 
    download button, even when inside a sandboxed iframe that does not 
    allow downloads. This CL hides the download button when the element 
    is in a sandboxed iframe that disallows downloads. 
     
    Bug: 40064543 
    Change-Id: Ie25b48bb994ed66c8621429a3447cc279e67fbfb 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7590057 
    Commit-Queue: Tommy Steimel <steimel@chromium.org> 
    Reviewed-by: Benjamin Keen <bkeen@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1587180}

```

---

Files:

- M `third_party/blink/renderer/modules/media_controls/elements/media_control_download_button_element.cc`
- A `third_party/blink/web_tests/media/controls/download-button-hidden-when-sandboxed.html`

---

Hash: [ad95dd50a86da6f46e3ae113a487689e99f4c4cc](https://chromiumdash.appspot.com/commit/ad95dd50a86da6f46e3ae113a487689e99f4c4cc)  

Date: Thu Feb 19 16:41:43 2026


---

### sp...@google.com (2026-05-27)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Baseline. Security mitigation bypass


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ch...@google.com (2026-05-29)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064543)*
