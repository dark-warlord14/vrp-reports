# Security: opens a new window in fullscreen mode at same time ,  leading to address bar spoof

| Field | Value |
|-------|-------|
| **Issue ID** | [41486190](https://issues.chromium.org/issues/41486190) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Fullscreen, Blink>WindowDialog, UI>Browser>FullScreen |
| **Platforms** | Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sa...@gmail.com |
| **Assignee** | li...@google.com |
| **Created** | 2023-12-21 |
| **Bounty** | Confirmed (amount unknown) |

## Description

**VULNERABILITY DETAILS**

I found a bar spoofing vulnerability, when a window opens in fullscreen mode and opens a new window at same time what happens is that it immediately exits fullscreen mode.  

However, this does not happen when opening an open a new window at the same time as fullscreen mode with "open link in new window" what happens is you open a new window and a fullscreen notification will appear and the previous window goes into fullscreen mode

The impact is that the victim thinks that the full screen notification comes from a new open window and not from the previous window because the focus is on the new open window. and this causes address bar spoofing in the previous window

**VERSION**  

Chrome Version: Version 120.0.6051.2 (Official Build) dev (64-bit)  

Operating System: Windows

**REPRODUCTION CASE**

1. open fullscreenspf.html
2. double click on the button

**CREDIT INFORMATION**  

Reporter credit: Hafiizh (<https://www.linkedin.com/in/hafiizh-7aa6bb31/>)

## Attachments

- [bandicam 2023-12-21 14-00-02-731.mp4](attachments/bandicam 2023-12-21 14-00-02-731.mp4) (video/mp4, 1.9 MB)
- [fullscreenspf.html](attachments/fullscreenspf.html) (text/plain, 2.8 KB)
- [fullscreenspf.html](attachments/fullscreenspf.html) (text/plain, 270 B)
- [bandicam 2025-01-16 09-41-51-757.mp4](attachments/bandicam 2025-01-16 09-41-51-757.mp4) (video/mp4, 1.2 MB)

## Timeline

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### bb...@google.com (2023-12-21)

OK, I can do this on linux as well, and I suspect this is cross-platform. Given this one really doesn't require super special user interaction I am tenatively calling this a medium.



[Monorail components: UI>Browser>FullScreen]

### bb...@google.com (2023-12-21)

@takumif can you PTAL, or reassign? thanks. 

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### [Deleted User] (2023-12-21)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-21)

This is a serious security regression. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-12-21)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ta...@google.com (2023-12-21)

IIUC the same thing can basically be done with browser-in-the-browser without the need for an extra click, so unless this is a regression, I'd rather we prioritize the longer-term effort to reduce our reliance on the fullscreen toast than to address individual issues like this.

### [Deleted User] (2023-12-21)

[Empty comment from Monorail migration]

### ms...@chromium.org (2023-12-21)

The novelty here is that the second click calls window.open() to focus the named pre-existing popup window opened by the first click.
That raises the popup to front, over the opener, as that window enters fullscreen, without consuming an activation signal. Offhand fix ideas:
(1) window.open() focusing a named popup should consume transient activation (making the requestFullscreen fail).
(2) window.open() focusing a named popup should call ForSecurityDropFullscreen(), which should make the opener exit fullscreen.
Minimized repro file attached

[Monorail components: Blink>Fullscreen Blink>WindowDialog]

### be...@google.com (2023-12-22)

Adding Hotlist-RBS-Removed for tracking purposes.

### [Deleted User] (2023-12-22)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2024-01-04)

takumif: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

takumif: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-18)

This issue was migrated from crbug.com/chromium/1513620?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Fullscreen, Blink>WindowDialog, UI>Browser>FullScreen]
[Monorail components added to Component Tags custom field.]

### sa...@gmail.com (2024-02-19)

Hello any updates?

### sa...@gmail.com (2024-03-06)

Hello any updates?

### sa...@gmail.com (2024-06-05)

Hello any updates?

### sa...@gmail.com (2024-07-02)

hello any updates?

### sa...@gmail.com (2024-08-02)

hello any updates?

### sa...@gmail.com (2024-10-08)

hello any updates?

### pe...@google.com (2024-11-05)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### pe...@google.com (2024-11-20)

liberato: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sa...@gmail.com (2025-01-16)

hi i can't reproduce it in Version 134.0.6957.0 (Official Build) canary (64-bit) the focus is already on the active window not on the popup window and the popup window is quickly closed, it seems this bug has been fixed can you check it again?

### dr...@chromium.org (2025-11-04)

Given this was reported fixed in M134, there's no value in identifying the fixing CL. Setting Fixed By Code Changes to NA and closing again.

### sp...@google.com (2025-11-13)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

The panel determined that this was not a convincing spoof and a "reasonable and prudent" user would never end up in a situation where this would impact their safety and security.

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-02-11)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> The panel determined that this was not a convincing spoof and a "reasonable and prudent" user would never end up in a situation where this would impact their safety and security.
> 
> 
> Note that the fact that this issue is not being rewarded does not mean
> that the product team won't fix the issue. We have filed a bug with the product
> team and they will review your report and decide if a fix is required. We'll
> let you know if the issue was fixed.
> 
> Regards, \
> Google Security Bot
> 
> *How did we do? Pleas

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/41486190)*
