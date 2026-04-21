# Security: Capture Autofill Data using showPicker Spoofing

| Field | Value |
|-------|-------|
| **Issue ID** | [41493771](https://issues.chromium.org/issues/41493771) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Privacy, UI>Browser>Autofill |
| **Platforms** | Linux |
| **Reporter** | fa...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2024-01-23 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Using the showPicker() JavaScript function, a site could open a select option and autofill by calling the input autofill with a delay. Thus, both can be activated at the same time,by opening the select option on top of autofill to spoof the UI. When the user double-clicks the select option, autofill data can be captured without the user's knowledge.

Chrome autofill has clickjacking protection; when double-clicked, autofill is not activated. However, using the above method, the select option is not captured as a click, and autofill is activated from a double-click. A suggested fix could be to cancel the select option activation when autofill is activated.

**VERSION**  

Chrome Version: 122.0.6261.0 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

1. Download `poc.html`.
2. Serve the above-downloaded file locally.
3. Navigate to your local IP, for example, `localhost:8080/poc.html`, for testing.

**CREDIT INFORMATION**  

Reporter credit: Shaheen Fazim

## Attachments

- deleted (application/octet-stream, 0 B)
- [demo.mp4](attachments/demo.mp4) (video/mp4, 1.1 MB)
- [auotfill-border.mp4](attachments/auotfill-border.mp4) (video/mp4, 167.4 KB)
- [basic.html](attachments/basic.html) (text/plain, 2.8 KB)
- [demo-b.mp4](attachments/demo-b.mp4) (video/mp4, 634.5 KB)
- [demo-c.mp4](attachments/demo-c.mp4) (video/mp4, 2.4 MB)
- [basic-c.html](attachments/basic-c.html) (text/html, 2.8 KB)
- [screenshot.png](attachments/screenshot.png) (image/png, 127.6 KB)

## Timeline

### fa...@gmail.com (2024-01-23)

Currently, Stable is not affected, but I believe showpicker will be working in the next 121 version.

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### fa...@gmail.com (2024-01-23)

[Comment Deleted]

### fa...@gmail.com (2024-01-23)

Similar issue: crbug.com/1341430

### li...@chromium.org (2024-01-23)

Hello,

What OS did you run your PoC on? I tried to reproduce this on canary on Linux and the double-click is still blocked for autofill.

### fa...@gmail.com (2024-01-23)

Windows 11

### [Deleted User] (2024-01-23)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fa...@gmail.com (2024-01-23)

I just tested on Ubuntu using Chrome Beta, and it is working for me. The select option menu should not cover the autofill; instead, a small border of the autofill should be present. This way, when the user scrolls through the border, the autofill is activated. You have to modify it in this way to make this proof-of-concept work. I have over-modified it to only work for my partical case but with few code improvement we could work this universal.

### li...@chromium.org (2024-01-23)

Hmm I still can't reproduce it locally but that might be because the select menu isn't in quite the right spot. 

I'm setting the FoundIn to 121 since the reporter confirmed stable is not impacted, and when I try to reproduce on stable the PoC doesn't show the picker for me at all.
Also tentatively setting the OS to just Linux though I imagine it may be impact at least other desktop OS's.

Adding Jan who worked on  crbug.com/1341430.

[Monorail components: Privacy UI>Browser>Autofill]

### [Deleted User] (2024-01-23)

[Empty comment from Monorail migration]

### ad...@google.com (2024-01-23)

(I am a bot: this is an auto-cc on a security bug)

### fa...@gmail.com (2024-01-24)

Hi,
I've improved the proof of concept to offer better support by simplifying the code. Additionally, please note that Chrome doesn't support autofill from "file://". To make this work, we need to host the file on a local server and visit the hosted site.

### [Deleted User] (2024-01-24)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-25)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1520796?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Privacy, UI>Browser>Autofill]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-07)

jkeitel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2024-02-20)

Friendly ping.

### jk...@google.com (2024-02-21)

Hi Fazim,

Thank you for the report, but I cannot reproduce any double click exploit on a system that I have. I am also uncertain that this would be exploitable in the wild because the size of the popup would have to near perfectly match the size of the picker dialog.

@battre, what's your opinion on this? We could, in theory, try to observe attempts to show a picker and hide on those. I am not convinced, though, whether we should.

Thanks,
Jan

### fa...@gmail.com (2024-02-21)

Hi,

Currently, the new proof of concept (POC) has been tested and is functioning smoothly on the Windows version of Chrome, as demonstrated in the new demo. Two points to note in the exploits are:

1. The select picker can open on top of the autofill.
2. When the user moves the mouse over the border of the autofill and then double-clicks on the content of the select picker, the autofill is selected. (The select picker can be customized to be smaller, utilizing the autofill background and covering only the autofill text.)

If the first condition is not working, please let me know, as it is a crucial part of the exploit where the select picker should open on top of the autofill. The customization for the second condition can be adjusted depending on the operating system or device resolution.

### fa...@gmail.com (2024-03-05)

Friendly ping.

### ba...@chromium.org (2024-03-05)

I agree with Jan's assessment and don't see this as a super high priority.

I think that it would be nice to close autofill popups whenever other popups appear as a general principle but P2 seems appropriate to me.

### pe...@google.com (2024-03-07)

jkeitel: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### fa...@gmail.com (2024-04-12)

Friendly ping.

### fa...@gmail.com (2024-05-09)

Hi, friendly ping.

### fa...@gmail.com (2024-05-21)

Hi kindly update on this issue.

### vy...@google.com (2024-05-31)

Hi, we are currently working on a general solution which should cover this issue as well, we'll update the status as soon as it is done, thanks for your patience!

### fa...@gmail.com (2024-11-26)

Hello team, Thanks for your reply from few months ago. Could you let me know how things are currently?

### fa...@gmail.com (2024-12-21)

Hi assignee, can u update on this issue? Thanks!

### br...@google.com (2024-12-24)

Hi Fazim, I will be taking a look at this and updating you shortly, thanks for the ping.

### fa...@gmail.com (2025-01-14)

Thanks for letting me know. I’ll wait for your update.

### fa...@gmail.com (2025-02-19)

Hi its been a month, any updates on this issue? Thanks!

### sy...@google.com (2025-03-28)

Hi, I've tested the provided website on the newest stable release(`134.0.6998.166`) and cannot reproduce this issue.

I can see in the devtools console the following error: `Uncaught NotAllowedError: Failed to execute 'showPicker' on 'HTMLInputElement': HTMLInputElement::showPicker() requires a user gesture.`.
Can you confirm on your side whether everything now works as expected?

### fa...@gmail.com (2025-03-28)

Yes, I can verify that it is fixed now. I'm getting the same error as above, the select picker is correctly suppressed and no longer opens on top of autofill.

### fa...@gmail.com (2025-03-31)

Hi, may we close this issue as fixed, if it has been resolved?

### sy...@google.com (2025-04-01)

I believe that this bug was fixed as part of fixing the following issue: [crbug.com/41494315](https://crbug.com/41494315).

[jarhar@chromium.org](mailto:jarhar@chromium.org) could you confirm that this is the case?

### ja...@chromium.org (2025-04-01)

Since the repro relies on showPicker being called on two different elements off of one user activation, yeah that fixed this.

### ch...@google.com (2025-04-01)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### sp...@google.com (2025-04-10)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
report of lower impact security UI issue 


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-04-10)

Congratulations Shaheen! Thank you for your efforts and reporting this issue to us.

### fa...@gmail.com (2025-04-10)

Yay, thank you!

### ch...@google.com (2025-04-30)

deleted

### ch...@google.com (2025-07-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> report of lower impact security UI issue

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41493771)*
